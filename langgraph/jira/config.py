# jira/config.py
"""
Jira configuration management
"""
import os
from typing import Optional
from dataclasses import dataclass

@dataclass
class JiraConfig:
    """Jira configuration settings"""
    base_url: str
    username: str
    api_token: str
    default_project_key: Optional[str] = None
    
    @classmethod
    def from_env(cls) -> 'JiraConfig':
        """Load Jira configuration from environment variables"""
        base_url = os.getenv('JIRA_BASE_URL')
        username = os.getenv('JIRA_USERNAME')
        api_token = os.getenv('JIRA_API_TOKEN')
        default_project = os.getenv('JIRA_DEFAULT_PROJECT')
        
        if not base_url:
            raise ValueError("JIRA_BASE_URL environment variable is required")
        if not username:
            raise ValueError("JIRA_USERNAME environment variable is required")
        if not api_token:
            raise ValueError("JIRA_API_TOKEN environment variable is required")
        
        return cls(
            base_url=base_url,
            username=username,
            api_token=api_token,
            default_project_key=default_project
        )
    
    def validate(self) -> bool:
        """Validate configuration"""
        if not self.base_url.startswith(('http://', 'https://')):
            return False
        if not self.username or not self.api_token:
            return False
        return True


# Default configuration
def get_jira_config() -> JiraConfig:
    """Get Jira configuration from environment"""
    return JiraConfig.from_env()