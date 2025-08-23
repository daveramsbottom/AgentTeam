# taiga/client.py
"""
Enhanced Taiga API Client with comprehensive story and task management
"""
import requests
import logging
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass
from datetime import datetime
import json

logger = logging.getLogger(__name__)


@dataclass
class TaigaStory:
    """Represents a Taiga User Story"""
    id: int
    subject: str
    description: str
    status: str
    status_id: int
    points: Optional[int]
    priority: str
    priority_id: int
    assigned_to: Optional[str]
    assigned_to_id: Optional[int]
    tags: List[str]
    created_date: datetime
    modified_date: datetime
    project_id: int
    ref: int
    
    @classmethod
    def from_taiga_data(cls, data: Dict[str, Any]) -> 'TaigaStory':
        """Create TaigaStory from Taiga API response"""
        return cls(
            id=data['id'],
            subject=data['subject'],
            description=data.get('description', ''),
            status=data.get('status_extra_info', {}).get('name', 'Unknown'),
            status_id=data.get('status', 0),
            points=data.get('points'),
            priority=data.get('priority_extra_info', {}).get('name', 'Normal'),
            priority_id=data.get('priority', 0),
            assigned_to=data.get('assigned_to_extra_info', {}).get('full_name'),
            assigned_to_id=data.get('assigned_to'),
            tags=data.get('tags', []),
            created_date=datetime.fromisoformat(data['created_date'].replace('Z', '+00:00')),
            modified_date=datetime.fromisoformat(data['modified_date'].replace('Z', '+00:00')),
            project_id=data['project'],
            ref=data['ref']
        )


@dataclass
class TaigaTask:
    """Represents a Taiga Task"""
    id: int
    subject: str
    description: str
    status: str
    status_id: int
    assigned_to: Optional[str]
    assigned_to_id: Optional[int]
    user_story: Optional[int]
    tags: List[str]
    created_date: datetime
    project_id: int
    ref: int
    
    @classmethod
    def from_taiga_data(cls, data: Dict[str, Any]) -> 'TaigaTask':
        """Create TaigaTask from Taiga API response"""
        return cls(
            id=data['id'],
            subject=data['subject'],
            description=data.get('description', ''),
            status=data.get('status_extra_info', {}).get('name', 'New'),
            status_id=data.get('status', 0),
            assigned_to=data.get('assigned_to_extra_info', {}).get('full_name'),
            assigned_to_id=data.get('assigned_to'),
            user_story=data.get('user_story'),
            tags=data.get('tags', []),
            created_date=datetime.fromisoformat(data['created_date'].replace('Z', '+00:00')),
            project_id=data['project'],
            ref=data['ref']
        )


class TaigaClient:
    """Enhanced Taiga API client with comprehensive project management capabilities"""
    
    def __init__(self, base_url: str, username: str, password: str):
        """
        Initialize Taiga client
        
        Args:
            base_url: Taiga API base URL (e.g., 'http://localhost:8000/api/v1')
            username: Taiga username
            password: Taiga password
        """
        self.base_url = base_url.rstrip('/')
        self.username = username
        self.password = password
        self.auth_token = None
        self.session = requests.Session()
        self._project_cache = {}
        self._status_cache = {}
        self._priority_cache = {}
        
        # Set default headers
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
        
        logger.info(f"🏗️ TaigaClient initialized for {base_url}")
    
    def authenticate(self) -> bool:
        """
        Authenticate with Taiga API
        
        Returns:
            True if authentication successful, False otherwise
        """
        logger.info("🔐 Authenticating with Taiga...")
        
        try:
            auth_url = f"{self.base_url}/auth"
            auth_data = {
                "username": self.username,
                "password": self.password,
                "type": "normal"
            }
            
            response = self.session.post(auth_url, json=auth_data)
            response.raise_for_status()
            
            auth_response = response.json()
            self.auth_token = auth_response.get('auth_token')
            
            if self.auth_token:
                self.session.headers.update({
                    'Authorization': f'Bearer {self.auth_token}'
                })
                logger.info("✅ Taiga authentication successful")
                return True
            else:
                logger.error("❌ No auth token received")
                return False
                
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Taiga authentication failed: {e}")
            return False
    
    def get_projects(self) -> List[Dict[str, Any]]:
        """Get all projects accessible to the user"""
        logger.info("📋 Fetching projects...")
        
        try:
            response = self.session.get(f"{self.base_url}/projects")
            response.raise_for_status()
            projects = response.json()
            
            logger.info(f"Found {len(projects)} projects")
            return projects
            
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Error fetching projects: {e}")
            return []
    
    def get_project_details(self, project_id: int) -> Optional[Dict[str, Any]]:
        """Get detailed information about a specific project"""
        if project_id in self._project_cache:
            return self._project_cache[project_id]
        
        try:
            response = self.session.get(f"{self.base_url}/projects/{project_id}")
            response.raise_for_status()
            project = response.json()
            
            self._project_cache[project_id] = project
            logger.info(f"📁 Retrieved project: {project.get('name')}")
            return project
            
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Error fetching project {project_id}: {e}")
            return None
    
    def get_user_stories(self, project_id: int) -> List[TaigaStory]:
        """Get all user stories for a project"""
        logger.info(f"📖 Fetching user stories for project {project_id}...")
        
        try:
            response = self.session.get(
                f"{self.base_url}/userstories",
                params={'project': project_id}
            )
            response.raise_for_status()
            stories_data = response.json()
            
            stories = [TaigaStory.from_taiga_data(story) for story in stories_data]
            logger.info(f"Found {len(stories)} user stories")
            return stories
            
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Error fetching user stories: {e}")
            return []
    
    def get_story_by_id(self, story_id: int) -> Optional[TaigaStory]:
        """Get a specific user story by ID"""
        try:
            response = self.session.get(f"{self.base_url}/userstories/{story_id}")
            response.raise_for_status()
            story_data = response.json()
            
            return TaigaStory.from_taiga_data(story_data)
            
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Error fetching story {story_id}: {e}")
            return None
    
    def create_user_story(self, story_data: Dict[str, Any]) -> Optional[TaigaStory]:
        """
        Create a new user story
        
        Args:
            story_data: Story information including subject, description, project, etc.
            
        Returns:
            Created TaigaStory object or None if failed
        """
        logger.info(f"✨ Creating user story: {story_data.get('subject', 'Untitled')}")
        
        try:
            response = self.session.post(f"{self.base_url}/userstories", json=story_data)
            response.raise_for_status()
            created_story = response.json()
            
            story = TaigaStory.from_taiga_data(created_story)
            logger.info(f"✅ Created story #{story.ref}: {story.subject}")
            return story
            
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Error creating user story: {e}")
            if hasattr(e, 'response') and e.response is not None:
                logger.error(f"Response: {e.response.text}")
            return None
    
    def update_user_story(self, story_id: int, updates: Dict[str, Any]) -> Optional[TaigaStory]:
        """Update an existing user story"""
        logger.info(f"📝 Updating user story {story_id}")
        
        try:
            response = self.session.patch(
                f"{self.base_url}/userstories/{story_id}",
                json=updates
            )
            response.raise_for_status()
            updated_story = response.json()
            
            story = TaigaStory.from_taiga_data(updated_story)
            logger.info(f"✅ Updated story #{story.ref}")
            return story
            
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Error updating user story {story_id}: {e}")
            return None
    
    def get_tasks(self, project_id: int, story_id: Optional[int] = None) -> List[TaigaTask]:
        """Get tasks for a project, optionally filtered by story"""
        logger.info(f"📋 Fetching tasks for project {project_id}")
        
        try:
            params = {'project': project_id}
            if story_id:
                params['user_story'] = story_id
            
            response = self.session.get(f"{self.base_url}/tasks", params=params)
            response.raise_for_status()
            tasks_data = response.json()
            
            tasks = [TaigaTask.from_taiga_data(task) for task in tasks_data]
            logger.info(f"Found {len(tasks)} tasks")
            return tasks
            
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Error fetching tasks: {e}")
            return []
    
    def create_task(self, task_data: Dict[str, Any]) -> Optional[TaigaTask]:
        """Create a new task"""
        logger.info(f"✨ Creating task: {task_data.get('subject', 'Untitled')}")
        
        try:
            response = self.session.post(f"{self.base_url}/tasks", json=task_data)
            response.raise_for_status()
            created_task = response.json()
            
            task = TaigaTask.from_taiga_data(created_task)
            logger.info(f"✅ Created task #{task.ref}: {task.subject}")
            return task
            
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Error creating task: {e}")
            if hasattr(e, 'response') and e.response is not None:
                logger.error(f"Response: {e.response.text}")
            return None
    
    def get_story_statuses(self, project_id: int) -> List[Dict[str, Any]]:
        """Get available statuses for user stories in a project"""
        if project_id in self._status_cache:
            return self._status_cache[project_id]
        
        try:
            response = self.session.get(f"{self.base_url}/userstory-statuses?project={project_id}")
            response.raise_for_status()
            statuses = response.json()
            
            self._status_cache[project_id] = statuses
            return statuses
            
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Error fetching story statuses: {e}")
            return []
    
    def get_priorities(self, project_id: int) -> List[Dict[str, Any]]:
        """Get available priorities for a project"""
        if project_id in self._priority_cache:
            return self._priority_cache[project_id]
        
        try:
            response = self.session.get(f"{self.base_url}/priorities?project={project_id}")
            response.raise_for_status()
            priorities = response.json()
            
            self._priority_cache[project_id] = priorities
            return priorities
            
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Error fetching priorities: {e}")
            return []
    
    def get_project_members(self, project_id: int) -> List[Dict[str, Any]]:
        """Get project members for task assignment"""
        try:
            response = self.session.get(f"{self.base_url}/memberships?project={project_id}")
            response.raise_for_status()
            memberships = response.json()
            
            members = []
            for membership in memberships:
                user_info = membership.get('user_extra_info', {})
                members.append({
                    'id': membership.get('user'),
                    'username': user_info.get('username'),
                    'full_name': user_info.get('full_name'),
                    'role': membership.get('role_name'),
                    'is_admin': membership.get('is_admin', False)
                })
            
            logger.info(f"Found {len(members)} project members")
            return members
            
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Error fetching project members: {e}")
            return []
    
    def assign_story_to_user(self, story_id: int, user_id: int) -> bool:
        """Assign a story to a user"""
        return self.update_user_story(story_id, {'assigned_to': user_id}) is not None
    
    def move_story_to_status(self, story_id: int, status_id: int) -> bool:
        """Move a story to a different status"""
        return self.update_user_story(story_id, {'status': status_id}) is not None
    
    def add_story_comment(self, story_id: int, comment: str) -> bool:
        """Add a comment to a story"""
        try:
            comment_data = {
                'comment': comment,
                'object_id': story_id,
                'content_type': 'userstories.userstory'
            }
            
            response = self.session.post(f"{self.base_url}/history/userstory", json=comment_data)
            response.raise_for_status()
            
            logger.info(f"✅ Added comment to story {story_id}")
            return True
            
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Error adding comment to story {story_id}: {e}")
            return False
    
    def get_project_summary(self, project_id: int) -> Dict[str, Any]:
        """Get a comprehensive summary of a project"""
        logger.info(f"📊 Generating project summary for project {project_id}")
        
        project = self.get_project_details(project_id)
        if not project:
            return {"error": "Project not found"}
        
        stories = self.get_user_stories(project_id)
        tasks = self.get_tasks(project_id)
        members = self.get_project_members(project_id)
        
        # Analyze stories by status
        story_status_counts = {}
        total_points = 0
        
        for story in stories:
            status = story.status
            story_status_counts[status] = story_status_counts.get(status, 0) + 1
            if story.points:
                total_points += story.points
        
        # Analyze task distribution
        task_status_counts = {}
        assigned_tasks = 0
        
        for task in tasks:
            status = task.status
            task_status_counts[status] = task_status_counts.get(status, 0) + 1
            if task.assigned_to_id:
                assigned_tasks += 1
        
        return {
            "project": {
                "id": project["id"],
                "name": project["name"],
                "description": project.get("description", ""),
                "created_date": project.get("created_date"),
                "total_story_points": project.get("total_story_points", 0)
            },
            "stories": {
                "total": len(stories),
                "total_points": total_points,
                "by_status": story_status_counts,
                "recent": [
                    {
                        "id": story.id,
                        "ref": story.ref,
                        "subject": story.subject,
                        "status": story.status,
                        "points": story.points
                    }
                    for story in sorted(stories, key=lambda s: s.created_date, reverse=True)[:5]
                ]
            },
            "tasks": {
                "total": len(tasks),
                "assigned": assigned_tasks,
                "unassigned": len(tasks) - assigned_tasks,
                "by_status": task_status_counts
            },
            "team": {
                "total_members": len(members),
                "members": [
                    {
                        "username": member["username"],
                        "full_name": member["full_name"],
                        "role": member["role"]
                    }
                    for member in members
                ]
            }
        }