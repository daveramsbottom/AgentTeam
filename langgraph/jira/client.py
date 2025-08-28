# jira/client.py
"""
Enhanced Jira API Client with comprehensive issue and task management
"""
import requests
import logging
import base64
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass
from datetime import datetime
import json

logger = logging.getLogger(__name__)


@dataclass
class JiraIssue:
    """Represents a Jira Issue (Story/Epic/etc.)"""
    id: str
    key: str
    summary: str
    description: str
    issue_type: str
    status: str
    status_id: str
    priority: str
    priority_id: str
    assigned_to: Optional[str]
    assigned_to_id: Optional[str]
    reporter: Optional[str]
    reporter_id: Optional[str]
    story_points: Optional[int]
    labels: List[str]
    created_date: datetime
    updated_date: datetime
    project_id: str
    project_key: str
    
    @classmethod
    def from_jira_data(cls, data: Dict[str, Any]) -> 'JiraIssue':
        """Create JiraIssue from Jira API response"""
        fields = data['fields']
        
        # Handle assignee
        assignee = fields.get('assignee')
        assigned_to = assignee.get('displayName') if assignee else None
        assigned_to_id = assignee.get('accountId') if assignee else None
        
        # Handle reporter
        reporter = fields.get('reporter')
        reporter_name = reporter.get('displayName') if reporter else None
        reporter_id = reporter.get('accountId') if reporter else None
        
        # Handle story points (might be in customfield)
        story_points = None
        # Common story points field names
        for field_key in fields.keys():
            if 'story' in field_key.lower() and 'point' in field_key.lower():
                story_points = fields.get(field_key)
                break
        
        return cls(
            id=data['id'],
            key=data['key'],
            summary=fields['summary'],
            description=fields.get('description', ''),
            issue_type=fields['issuetype']['name'],
            status=fields['status']['name'],
            status_id=fields['status']['id'],
            priority=fields.get('priority', {}).get('name', 'Medium'),
            priority_id=fields.get('priority', {}).get('id', '3'),
            assigned_to=assigned_to,
            assigned_to_id=assigned_to_id,
            reporter=reporter_name,
            reporter_id=reporter_id,
            story_points=story_points,
            labels=fields.get('labels', []),
            created_date=datetime.fromisoformat(fields['created'].replace('Z', '+00:00')),
            updated_date=datetime.fromisoformat(fields['updated'].replace('Z', '+00:00')),
            project_id=fields['project']['id'],
            project_key=fields['project']['key']
        )


@dataclass
class JiraTask:
    """Represents a Jira Task (Sub-task)"""
    id: str
    key: str
    summary: str
    description: str
    status: str
    status_id: str
    assigned_to: Optional[str]
    assigned_to_id: Optional[str]
    parent_issue: Optional[str]
    labels: List[str]
    created_date: datetime
    project_id: str
    project_key: str
    
    @classmethod
    def from_jira_data(cls, data: Dict[str, Any]) -> 'JiraTask':
        """Create JiraTask from Jira API response"""
        fields = data['fields']
        
        # Handle assignee
        assignee = fields.get('assignee')
        assigned_to = assignee.get('displayName') if assignee else None
        assigned_to_id = assignee.get('accountId') if assignee else None
        
        # Handle parent issue
        parent = fields.get('parent')
        parent_key = parent.get('key') if parent else None
        
        return cls(
            id=data['id'],
            key=data['key'],
            summary=fields['summary'],
            description=fields.get('description', ''),
            status=fields['status']['name'],
            status_id=fields['status']['id'],
            assigned_to=assigned_to,
            assigned_to_id=assigned_to_id,
            parent_issue=parent_key,
            labels=fields.get('labels', []),
            created_date=datetime.fromisoformat(fields['created'].replace('Z', '+00:00')),
            project_id=fields['project']['id'],
            project_key=fields['project']['key']
        )


class JiraClient:
    """Enhanced Jira API client with comprehensive project management capabilities"""
    
    def __init__(self, base_url: str, username: str, api_token: str):
        """
        Initialize Jira client
        
        Args:
            base_url: Jira instance URL (e.g., 'https://yourcompany.atlassian.net')
            username: Jira username/email
            api_token: Jira API token (not password)
        """
        self.base_url = base_url.rstrip('/')
        self.username = username
        self.api_token = api_token
        self.session = requests.Session()
        self._project_cache = {}
        self._status_cache = {}
        self._priority_cache = {}
        self._issue_type_cache = {}
        
        # Set up authentication
        auth_string = f"{username}:{api_token}"
        auth_bytes = auth_string.encode('ascii')
        auth_b64 = base64.b64encode(auth_bytes).decode('ascii')
        
        # Set default headers
        self.session.headers.update({
            'Authorization': f'Basic {auth_b64}',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
        
        logger.info(f"🔧 JiraClient initialized for {base_url}")
    
    def _text_to_adf(self, text: str) -> Dict[str, Any]:
        """Convert plain text to Atlassian Document Format (ADF)"""
        if not text:
            return {
                "type": "doc",
                "version": 1,
                "content": []
            }
        
        # Split text into paragraphs
        paragraphs = text.split('\n\n')
        content = []
        
        for paragraph in paragraphs:
            if paragraph.strip():
                # Check if it's a list item or heading
                lines = paragraph.split('\n')
                
                if paragraph.startswith('**') and paragraph.endswith(':**'):
                    # This is a heading
                    heading_text = paragraph.replace('**', '').replace(':', '')
                    content.append({
                        "type": "heading",
                        "attrs": {"level": 3},
                        "content": [
                            {
                                "type": "text",
                                "text": heading_text
                            }
                        ]
                    })
                elif any(line.strip().startswith(('- ', '• ')) for line in lines):
                    # This is a list
                    list_items = []
                    for line in lines:
                        line = line.strip()
                        if line.startswith(('- ', '• ')):
                            item_text = line[2:].strip()  # Remove the bullet
                            list_items.append({
                                "type": "listItem",
                                "content": [
                                    {
                                        "type": "paragraph",
                                        "content": [
                                            {
                                                "type": "text",
                                                "text": item_text
                                            }
                                        ]
                                    }
                                ]
                            })
                    
                    if list_items:
                        content.append({
                            "type": "bulletList",
                            "content": list_items
                        })
                else:
                    # Regular paragraph
                    content.append({
                        "type": "paragraph",
                        "content": [
                            {
                                "type": "text",
                                "text": paragraph.strip()
                            }
                        ]
                    })
        
        return {
            "type": "doc",
            "version": 1,
            "content": content
        }
    
    def test_connection(self) -> bool:
        """
        Test connection and authentication with Jira
        
        Returns:
            True if connection successful, False otherwise
        """
        logger.info("🔐 Testing Jira connection...")
        
        try:
            response = self.session.get(f"{self.base_url}/rest/api/3/myself")
            response.raise_for_status()
            
            user_info = response.json()
            logger.info(f"✅ Jira connection successful. Logged in as: {user_info.get('displayName')}")
            return True
            
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Jira connection failed: {e}")
            return False
    
    def get_projects(self) -> List[Dict[str, Any]]:
        """Get all projects accessible to the user"""
        logger.info("📋 Fetching projects...")
        
        try:
            response = self.session.get(f"{self.base_url}/rest/api/3/project")
            response.raise_for_status()
            projects = response.json()
            
            logger.info(f"Found {len(projects)} projects")
            return projects
            
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Error fetching projects: {e}")
            return []
    
    def get_project_details(self, project_key: str) -> Optional[Dict[str, Any]]:
        """Get detailed information about a specific project"""
        if project_key in self._project_cache:
            return self._project_cache[project_key]
        
        try:
            response = self.session.get(f"{self.base_url}/rest/api/3/project/{project_key}")
            response.raise_for_status()
            project = response.json()
            
            self._project_cache[project_key] = project
            logger.info(f"📁 Retrieved project: {project.get('name')}")
            return project
            
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Error fetching project {project_key}: {e}")
            return None
    
    def get_project_goal(self, project_key: str) -> Optional[str]:
        """
        Extract project goal from a dedicated "Project Goal" Epic
        This provides a visible, team-accessible way to set project goals
        """
        try:
            # Look for an Epic with summary containing "Project Goal" or similar
            goal_epic = self._find_project_goal_epic(project_key)
            
            if goal_epic and goal_epic.description:
                logger.info(f"🎯 Found project goal in Epic '{goal_epic.summary}': {goal_epic.description[:100]}...")
                return goal_epic.description.strip()
            
            # Try legacy project description approach as fallback
            project_details = self.get_project_details(project_key)
            if project_details:
                description = project_details.get('description')
                if description and len(description.strip()) > 20:
                    logger.info(f"🎯 Found project goal in project description: {description[:100]}...")
                    return description.strip()
            
            # Fallback to project name if no goal found
            if project_details:
                name = project_details.get('name', '')
                if name:
                    goal = f"Work on the {name} project"
                    logger.info(f"🎯 Generated basic goal from project name: {goal}")
                    return goal
            
            # Final fallback
            logger.warning(f"⚠️ No project goal found for {project_key}. Consider creating a 'Project Goal' Epic.")
            return f"Manage tasks and stories for project {project_key}"
            
        except Exception as e:
            logger.error(f"❌ Error getting project goal for {project_key}: {e}")
            return f"Work on project {project_key}"

    def _find_project_goal_epic(self, project_key: str) -> Optional['JiraIssue']:
        """Find the Epic that contains the project goal"""
        try:
            # Search for Epics with goal-related summaries
            goal_keywords = ["Project Goal", "PROJECT GOAL", "Main Objective", "MAIN OBJECTIVE", "🎯"]
            
            for keyword in goal_keywords:
                jql = f'project = "{project_key}" AND issuetype = Epic AND summary ~ "{keyword}"'
                
                params = {
                    'jql': jql,
                    'fields': 'summary,description',
                    'maxResults': 5
                }
                
                response = self.session.get(f"{self.base_url}/rest/api/3/search", params=params)
                response.raise_for_status()
                search_result = response.json()
                
                if search_result['issues']:
                    # Return the first matching Epic
                    epic_data = search_result['issues'][0]
                    logger.info(f"🎯 Found project goal Epic: {epic_data['fields']['summary']}")
                    return JiraIssue.from_jira_data(epic_data)
            
            # If no exact match, look for the first Epic (fallback)
            jql = f'project = "{project_key}" AND issuetype = Epic'
            params = {
                'jql': jql,
                'fields': 'summary,description',
                'maxResults': 1,
                'orderBy': 'created DESC'
            }
            
            response = self.session.get(f"{self.base_url}/rest/api/3/search", params=params)
            response.raise_for_status()
            search_result = response.json()
            
            if search_result['issues']:
                epic_data = search_result['issues'][0]
                logger.info(f"📋 Using first Epic as project goal: {epic_data['fields']['summary']}")
                return JiraIssue.from_jira_data(epic_data)
            
            return None
            
        except Exception as e:
            logger.error(f"❌ Error finding project goal Epic: {e}")
            return None
    
    def update_project_goal(self, project_key: str, new_goal: str) -> bool:
        """
        Update or create a "Project Goal" Epic with the new goal
        This provides a visible, team-accessible way to manage project goals
        """
        try:
            # Check if a project goal Epic already exists
            goal_epic = self._find_project_goal_epic(project_key)
            
            if goal_epic:
                # Update existing Epic
                logger.info(f"🔄 Updating existing project goal Epic: {goal_epic.key}")
                return self._update_epic_description(goal_epic.key, new_goal)
            else:
                # Create new project goal Epic
                logger.info(f"✨ Creating new project goal Epic for {project_key}")
                return self._create_project_goal_epic(project_key, new_goal)
            
        except Exception as e:
            logger.error(f"❌ Error updating project goal for {project_key}: {e}")
            return False

    def _update_epic_description(self, epic_key: str, new_description: str) -> bool:
        """Update an Epic's description"""
        try:
            adf_content = self._convert_to_adf(new_description)
            update_data = {
                "fields": {
                    "description": adf_content
                }
            }
            
            response = self.session.put(
                f"{self.base_url}/rest/api/3/issue/{epic_key}",
                json=update_data
            )
            response.raise_for_status()
            
            logger.info(f"✅ Updated Epic {epic_key} with new project goal")
            return True
            
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Error updating Epic {epic_key}: {e}")
            return False

    def _create_project_goal_epic(self, project_key: str, goal_description: str) -> bool:
        """Create a new project goal Epic"""
        try:
            adf_content = self._convert_to_adf(goal_description)
            
            # Get project ID for Epic creation
            project_details = self.get_project_details(project_key)
            if not project_details:
                logger.error(f"❌ Cannot get project details for {project_key}")
                return False
            
            issue_data = {
                "fields": {
                    "project": {
                        "key": project_key
                    },
                    "summary": "🎯 Project Goal",
                    "description": adf_content,
                    "issuetype": {
                        "name": "Epic"
                    }
                }
            }
            
            # Add Epic Name field if required (some Jira instances require it)
            try:
                issue_data["fields"]["customfield_10011"] = "Project Main Objective"  # Common Epic Name field
            except:
                pass  # Epic Name field may not exist in all instances
            
            response = self.session.post(
                f"{self.base_url}/rest/api/3/issue",
                json=issue_data
            )
            response.raise_for_status()
            
            created_issue = response.json()
            epic_key = created_issue["key"]
            logger.info(f"✅ Created project goal Epic: {epic_key}")
            return True
            
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Error creating project goal Epic: {e}")
            return False
    
    def get_issues(self, project_key: str, issue_types: List[str] = None) -> List[JiraIssue]:
        """Get issues for a project, optionally filtered by issue type"""
        logger.info(f"📖 Fetching issues for project {project_key}...")
        
        try:
            # Build JQL query
            jql = f"project = {project_key}"
            if issue_types:
                type_filter = "(" + " OR ".join([f'issuetype = "{t}"' for t in issue_types]) + ")"
                jql += f" AND {type_filter}"
            
            params = {
                'jql': jql,
                'fields': '*all',
                'maxResults': 1000
            }
            
            response = self.session.get(f"{self.base_url}/rest/api/3/search", params=params)
            response.raise_for_status()
            search_result = response.json()
            
            issues = [JiraIssue.from_jira_data(issue) for issue in search_result['issues']]
            logger.info(f"Found {len(issues)} issues")
            return issues
            
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Error fetching issues: {e}")
            return []
    
    def get_user_stories(self, project_key: str) -> List[JiraIssue]:
        """Get user stories for a project"""
        return self.get_issues(project_key, ['Story'])
    
    def get_issue_by_key(self, issue_key: str) -> Optional[JiraIssue]:
        """Get a specific issue by key"""
        try:
            response = self.session.get(
                f"{self.base_url}/rest/api/3/issue/{issue_key}",
                params={'fields': '*all'}
            )
            response.raise_for_status()
            issue_data = response.json()
            
            return JiraIssue.from_jira_data(issue_data)
            
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Error fetching issue {issue_key}: {e}")
            return None
    
    def create_issue(self, issue_data: Dict[str, Any]) -> Optional[JiraIssue]:
        """
        Create a new issue
        
        Args:
            issue_data: Issue information including summary, description, project, etc.
            
        Returns:
            Created JiraIssue object or None if failed
        """
        logger.info(f"✨ Creating issue: {issue_data.get('fields', {}).get('summary', 'Untitled')}")
        
        try:
            response = self.session.post(f"{self.base_url}/rest/api/3/issue", json=issue_data)
            response.raise_for_status()
            created_issue = response.json()
            
            # Fetch the full issue details
            issue = self.get_issue_by_key(created_issue['key'])
            if issue:
                logger.info(f"✅ Created issue {issue.key}: {issue.summary}")
            return issue
            
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Error creating issue: {e}")
            if hasattr(e, 'response') and e.response is not None:
                logger.error(f"Response: {e.response.text}")
            return None
    
    def create_user_story(self, project_key: str, summary: str, description: str = "", 
                         story_points: Optional[int] = None, assignee_id: Optional[str] = None) -> Optional[JiraIssue]:
        """Create a user story with simplified interface"""
        
        # Convert plain text description to Atlassian Document Format
        description_adf = self._text_to_adf(description) if description else None
        
        issue_data = {
            "fields": {
                "project": {"key": project_key},
                "summary": summary,
                "issuetype": {"name": "Story"}
            }
        }
        
        # Only add description if we have one
        if description_adf:
            issue_data["fields"]["description"] = description_adf
        
        # Add assignee if provided
        if assignee_id:
            issue_data["fields"]["assignee"] = {"accountId": assignee_id}
        
        # Add story points if provided (need to find the correct custom field)
        if story_points is not None:
            # This might need to be adjusted based on your Jira configuration
            story_points_field = self.get_story_points_field(project_key)
            if story_points_field:
                issue_data["fields"][story_points_field] = story_points
        
        return self.create_issue(issue_data)
    
    def update_issue(self, issue_key: str, updates: Dict[str, Any]) -> Optional[JiraIssue]:
        """Update an existing issue"""
        logger.info(f"🔄 Updating issue {issue_key}")
        
        try:
            update_data = {"fields": updates}
            response = self.session.put(
                f"{self.base_url}/rest/api/3/issue/{issue_key}",
                json=update_data
            )
            response.raise_for_status()
            
            # Fetch updated issue
            updated_issue = self.get_issue_by_key(issue_key)
            if updated_issue:
                logger.info(f"✅ Updated issue {updated_issue.key}")
            return updated_issue
            
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Error updating issue {issue_key}: {e}")
            return None
    
    def get_subtasks(self, parent_key: str) -> List[JiraTask]:
        """Get subtasks for a parent issue"""
        logger.info(f"📋 Fetching subtasks for {parent_key}")
        
        try:
            jql = f"parent = {parent_key}"
            params = {
                'jql': jql,
                'fields': '*all',
                'maxResults': 100
            }
            
            response = self.session.get(f"{self.base_url}/rest/api/3/search", params=params)
            response.raise_for_status()
            search_result = response.json()
            
            tasks = [JiraTask.from_jira_data(task) for task in search_result['issues']]
            logger.info(f"Found {len(tasks)} subtasks")
            return tasks
            
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Error fetching subtasks: {e}")
            return []
    
    def create_subtask(self, parent_key: str, summary: str, description: str = "", 
                      assignee_id: Optional[str] = None) -> Optional[JiraTask]:
        """Create a subtask under a parent issue"""
        
        # Get parent issue to determine project
        parent_issue = self.get_issue_by_key(parent_key)
        if not parent_issue:
            logger.error(f"❌ Parent issue {parent_key} not found")
            return None
        
        issue_data = {
            "fields": {
                "project": {"key": parent_issue.project_key},
                "parent": {"key": parent_key},
                "summary": summary,
                "description": description,
                "issuetype": {"name": "Sub-task"}
            }
        }
        
        # Add assignee if provided
        if assignee_id:
            issue_data["fields"]["assignee"] = {"accountId": assignee_id}
        
        try:
            response = self.session.post(f"{self.base_url}/rest/api/3/issue", json=issue_data)
            response.raise_for_status()
            created_issue = response.json()
            
            # Convert to JiraTask
            full_issue = self.get_issue_by_key(created_issue['key'])
            if full_issue:
                # Convert JiraIssue to JiraTask for subtasks
                task = JiraTask(
                    id=full_issue.id,
                    key=full_issue.key,
                    summary=full_issue.summary,
                    description=full_issue.description,
                    status=full_issue.status,
                    status_id=full_issue.status_id,
                    assigned_to=full_issue.assigned_to,
                    assigned_to_id=full_issue.assigned_to_id,
                    parent_issue=parent_key,
                    labels=full_issue.labels,
                    created_date=full_issue.created_date,
                    project_id=full_issue.project_id,
                    project_key=full_issue.project_key
                )
                logger.info(f"✅ Created subtask {task.key}: {task.summary}")
                return task
            
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Error creating subtask: {e}")
            if hasattr(e, 'response') and e.response is not None:
                logger.error(f"Response: {e.response.text}")
            return None
    
    def get_issue_statuses(self, project_key: str) -> List[Dict[str, Any]]:
        """Get available statuses for issues in a project"""
        if project_key in self._status_cache:
            return self._status_cache[project_key]
        
        try:
            response = self.session.get(f"{self.base_url}/rest/api/3/project/{project_key}/statuses")
            response.raise_for_status()
            statuses_by_type = response.json()
            
            # Flatten statuses from all issue types
            all_statuses = []
            for issue_type_statuses in statuses_by_type:
                for status in issue_type_statuses.get('statuses', []):
                    if status not in all_statuses:
                        all_statuses.append(status)
            
            self._status_cache[project_key] = all_statuses
            return all_statuses
            
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Error fetching statuses: {e}")
            return []
    
    def get_priorities(self) -> List[Dict[str, Any]]:
        """Get available priorities"""
        try:
            response = self.session.get(f"{self.base_url}/rest/api/3/priority")
            response.raise_for_status()
            priorities = response.json()
            
            return priorities
            
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Error fetching priorities: {e}")
            return []
    
    def get_project_users(self, project_key: str) -> List[Dict[str, Any]]:
        """Get users who can be assigned to issues in the project"""
        try:
            response = self.session.get(
                f"{self.base_url}/rest/api/3/user/assignable/search",
                params={'project': project_key, 'maxResults': 1000}
            )
            response.raise_for_status()
            users = response.json()
            
            formatted_users = []
            for user in users:
                formatted_users.append({
                    'account_id': user.get('accountId'),
                    'username': user.get('name', user.get('emailAddress', '')),
                    'display_name': user.get('displayName'),
                    'email': user.get('emailAddress'),
                    'active': user.get('active', True)
                })
            
            logger.info(f"Found {len(formatted_users)} assignable users")
            return formatted_users
            
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Error fetching project users: {e}")
            return []
    
    def assign_issue_to_user(self, issue_key: str, account_id: str) -> bool:
        """Assign an issue to a user"""
        return self.update_issue(issue_key, {'assignee': {'accountId': account_id}}) is not None
    
    def transition_issue(self, issue_key: str, transition_id: str) -> bool:
        """Transition an issue to a different status"""
        try:
            transition_data = {
                "transition": {
                    "id": transition_id
                }
            }
            
            response = self.session.post(
                f"{self.base_url}/rest/api/3/issue/{issue_key}/transitions",
                json=transition_data
            )
            response.raise_for_status()
            
            logger.info(f"✅ Transitioned issue {issue_key}")
            return True
            
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Error transitioning issue {issue_key}: {e}")
            return False
    
    def get_issue_transitions(self, issue_key: str) -> List[Dict[str, Any]]:
        """Get available transitions for an issue"""
        try:
            response = self.session.get(f"{self.base_url}/rest/api/3/issue/{issue_key}/transitions")
            response.raise_for_status()
            transitions_data = response.json()
            
            return transitions_data.get('transitions', [])
            
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Error fetching transitions for {issue_key}: {e}")
            return []
    
    def add_issue_comment(self, issue_key: str, comment: str) -> bool:
        """Add a comment to an issue"""
        try:
            comment_data = {
                "body": {
                    "type": "doc",
                    "version": 1,
                    "content": [
                        {
                            "type": "paragraph",
                            "content": [
                                {
                                    "type": "text",
                                    "text": comment
                                }
                            ]
                        }
                    ]
                }
            }
            
            response = self.session.post(
                f"{self.base_url}/rest/api/3/issue/{issue_key}/comment",
                json=comment_data
            )
            response.raise_for_status()
            
            logger.info(f"✅ Added comment to issue {issue_key}")
            return True
            
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Error adding comment to issue {issue_key}: {e}")
            return False
    
    def get_story_points_field(self, project_key: str) -> Optional[str]:
        """Find the custom field ID for story points in a project"""
        try:
            response = self.session.get(f"{self.base_url}/rest/api/3/field")
            response.raise_for_status()
            fields = response.json()
            
            # Look for story points field
            for field in fields:
                if 'story' in field.get('name', '').lower() and 'point' in field.get('name', '').lower():
                    return field['id']
            
            return None
            
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Error fetching custom fields: {e}")
            return None
    
    def get_project_summary(self, project_key: str) -> Dict[str, Any]:
        """Get a comprehensive summary of a project"""
        logger.info(f"📊 Generating project summary for project {project_key}")
        
        project = self.get_project_details(project_key)
        if not project:
            return {"error": "Project not found"}
        
        issues = self.get_issues(project_key)
        users = self.get_project_users(project_key)
        
        # Analyze issues by status
        issue_status_counts = {}
        total_story_points = 0
        stories = []
        tasks = []
        
        for issue in issues:
            status = issue.status
            issue_status_counts[status] = issue_status_counts.get(status, 0) + 1
            
            if issue.story_points:
                total_story_points += issue.story_points
            
            if issue.issue_type == 'Story':
                stories.append(issue)
            elif issue.issue_type == 'Sub-task':
                tasks.append(issue)
        
        # Analyze assignment
        assigned_issues = sum(1 for issue in issues if issue.assigned_to_id)
        unassigned_issues = len(issues) - assigned_issues
        
        return {
            "project": {
                "id": project["id"],
                "key": project["key"],
                "name": project["name"],
                "description": project.get("description", ""),
                "project_type": project.get("projectTypeKey", ""),
                "lead": project.get("lead", {}).get("displayName", "")
            },
            "issues": {
                "total": len(issues),
                "stories": len(stories),
                "tasks": len(tasks),
                "total_story_points": total_story_points,
                "assigned": assigned_issues,
                "unassigned": unassigned_issues,
                "by_status": issue_status_counts,
                "recent_stories": [
                    {
                        "key": story.key,
                        "summary": story.summary,
                        "status": story.status,
                        "story_points": story.story_points,
                        "assigned_to": story.assigned_to
                    }
                    for story in sorted(stories, key=lambda s: s.created_date, reverse=True)[:5]
                ]
            },
            "team": {
                "total_users": len(users),
                "active_users": sum(1 for user in users if user['active']),
                "users": [
                    {
                        "display_name": user["display_name"],
                        "username": user["username"],
                        "email": user.get("email", "")
                    }
                    for user in users[:10]  # Limit to first 10 users
                ]
            }
        }