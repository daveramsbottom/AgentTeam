# jira/utils.py
"""
Jira utility functions and helpers
"""
import re
from typing import Dict, List, Optional, Any
from datetime import datetime


def parse_jira_key(key_or_url: str) -> Optional[str]:
    """
    Extract Jira issue key from various formats
    
    Args:
        key_or_url: Could be just key (PROJ-123) or full URL
        
    Returns:
        Clean issue key or None if invalid
    """
    if not key_or_url:
        return None
    
    # If it's a URL, extract the key
    if 'browse/' in key_or_url:
        match = re.search(r'browse/([A-Z]+-\d+)', key_or_url)
        if match:
            return match.group(1)
    
    # If it's just a key, validate format
    if re.match(r'^[A-Z]+-\d+$', key_or_url):
        return key_or_url
    
    return None


def format_jira_description(description: str) -> str:
    """
    Format description text for Jira (basic markdown-like formatting)
    
    Args:
        description: Plain text description
        
    Returns:
        Formatted description
    """
    if not description:
        return ""
    
    # Basic formatting conversions
    # Convert **bold** to *bold*
    description = re.sub(r'\*\*(.*?)\*\*', r'*\1*', description)
    
    # Convert bullet points to Jira format
    description = re.sub(r'^- ', '* ', description, flags=re.MULTILINE)
    description = re.sub(r'^\d+\. ', '# ', description, flags=re.MULTILINE)
    
    return description


def create_story_from_text(text: str, project_key: str) -> Dict[str, Any]:
    """
    Create a Jira story structure from free-form text
    
    Args:
        text: User story text (may include acceptance criteria)
        project_key: Jira project key
        
    Returns:
        Dictionary ready for Jira API
    """
    lines = text.strip().split('\n')
    summary = lines[0] if lines else "User Story"
    
    # Extract description from remaining lines
    description = '\n'.join(lines[1:]).strip() if len(lines) > 1 else ""
    
    # Format for Jira
    formatted_description = format_jira_description(description)
    
    return {
        "fields": {
            "project": {"key": project_key},
            "summary": summary,
            "description": formatted_description,
            "issuetype": {"name": "Story"}
        }
    }


def extract_story_points(text: str) -> Optional[int]:
    """
    Extract story points from text using common patterns
    
    Args:
        text: Text that may contain story points
        
    Returns:
        Story points as integer or None
    """
    # Look for patterns like "3 points", "SP: 5", "Story Points: 8"
    patterns = [
        r'(\d+)\s*(?:story\s*)?points?',
        r'sp:?\s*(\d+)',
        r'points?:?\s*(\d+)',
        r'effort:?\s*(\d+)'
    ]
    
    text_lower = text.lower()
    for pattern in patterns:
        match = re.search(pattern, text_lower)
        if match:
            try:
                return int(match.group(1))
            except ValueError:
                continue
    
    return None


def format_issue_summary(issue) -> str:
    """
    Create a formatted summary string for an issue
    
    Args:
        issue: JiraIssue or JiraTask object
        
    Returns:
        Formatted summary string
    """
    status_emoji = {
        'To Do': '📋',
        'In Progress': '🔄',
        'Done': '✅',
        'Blocked': '🚫',
        'Review': '👁️'
    }
    
    emoji = status_emoji.get(issue.status, '📌')
    assignee = f" (@{issue.assigned_to})" if issue.assigned_to else ""
    
    summary = f"{emoji} {issue.key}: {issue.summary}{assignee}"
    
    # Add story points if available
    if hasattr(issue, 'story_points') and issue.story_points:
        summary += f" [{issue.story_points}pts]"
    
    return summary


def group_issues_by_status(issues: List) -> Dict[str, List]:
    """
    Group issues by their status
    
    Args:
        issues: List of JiraIssue or JiraTask objects
        
    Returns:
        Dictionary with status as key and list of issues as value
    """
    grouped = {}
    for issue in issues:
        status = issue.status
        if status not in grouped:
            grouped[status] = []
        grouped[status].append(issue)
    
    return grouped


def calculate_velocity(issues: List, days: int = 14) -> Dict[str, Any]:
    """
    Calculate team velocity based on completed stories
    
    Args:
        issues: List of JiraIssue objects
        days: Number of days to look back
        
    Returns:
        Velocity metrics
    """
    cutoff_date = datetime.now().replace(tzinfo=None) - timedelta(days=days)
    
    completed_stories = []
    total_points = 0
    
    for issue in issues:
        if (hasattr(issue, 'issue_type') and issue.issue_type == 'Story' and 
            issue.status.lower() in ['done', 'closed', 'resolved'] and
            issue.updated_date.replace(tzinfo=None) >= cutoff_date):
            
            completed_stories.append(issue)
            if hasattr(issue, 'story_points') and issue.story_points:
                total_points += issue.story_points
    
    return {
        'period_days': days,
        'completed_stories': len(completed_stories),
        'total_story_points': total_points,
        'average_points_per_day': total_points / days if days > 0 else 0,
        'stories': completed_stories
    }


def validate_project_key(project_key: str) -> bool:
    """
    Validate Jira project key format
    
    Args:
        project_key: Project key to validate
        
    Returns:
        True if valid format, False otherwise
    """
    if not project_key:
        return False
    
    # Jira project keys are typically 2-10 uppercase letters
    return bool(re.match(r'^[A-Z]{2,10}, project_key))


def sanitize_summary(summary: str, max_length: int = 255) -> str:
    """
    Sanitize and truncate summary for Jira
    
    Args:
        summary: Issue summary
        max_length: Maximum allowed length
        
    Returns:
        Sanitized summary
    """
    if not summary:
        return "Untitled"
    
    # Remove newlines and extra whitespace
    cleaned = ' '.join(summary.split())
    
    # Truncate if too long
    if len(cleaned) > max_length:
        cleaned = cleaned[:max_length-3] + "..."
    
    return cleaned


def build_jql_query(project_key: str, filters: Dict[str, Any]) -> str:
    """
    Build JQL query from filters
    
    Args:
        project_key: Jira project key
        filters: Dictionary of filter criteria
        
    Returns:
        JQL query string
    """
    jql_parts = [f"project = {project_key}"]
    
    if 'assignee' in filters:
        if filters['assignee']:
            jql_parts.append(f"assignee = '{filters['assignee']}'")
        else:
            jql_parts.append("assignee is EMPTY")
    
    if 'status' in filters:
        statuses = filters['status']
        if isinstance(statuses, list):
            status_list = "(" + ",".join([f"'{s}'" for s in statuses]) + ")"
            jql_parts.append(f"status in {status_list}")
        else:
            jql_parts.append(f"status = '{statuses}'")
    
    if 'issue_type' in filters:
        types = filters['issue_type']
        if isinstance(types, list):
            type_list = "(" + ",".join([f"'{t}'" for t in types]) + ")"
            jql_parts.append(f"issuetype in {type_list}")
        else:
            jql_parts.append(f"issuetype = '{types}'")
    
    if 'labels' in filters:
        labels = filters['labels']
        if isinstance(labels, list):
            for label in labels:
                jql_parts.append(f"labels = '{label}'")
        else:
            jql_parts.append(f"labels = '{labels}'")
    
    if 'created_after' in filters:
        jql_parts.append(f"created >= '{filters['created_after']}'")
    
    if 'updated_after' in filters:
        jql_parts.append(f"updated >= '{filters['updated_after']}'")
    
    return " AND ".join(jql_parts)


# Import timedelta for velocity calculation
from datetime import timedelta