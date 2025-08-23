"""
Configuration Management for AgentTeam
Centralized configuration handling with validation
"""
import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class Config:
    """Configuration class for AgentTeam with Jira integration"""
    
    # Slack configuration (required)
    slack_token: str
    slack_channel: str
    
    # OpenAI configuration
    openai_api_key: Optional[str] = None
    
    # Optional settings
    log_level: str = "INFO"
    workflow_timeout: int = 300  # 5 minutes default
    
    @classmethod
    def from_environment(cls) -> 'Config':
        """Create configuration from environment variables"""
        
        # Required environment variables
        required_vars = {
            'SLACK_BOT_TOKEN': 'slack_token',
            'SLACK_CHANNEL_ID': 'slack_channel',
        }
        
        config_dict = {}
        missing_vars = []
        
        # Check required variables
        for env_var, config_key in required_vars.items():
            value = os.getenv(env_var)
            if not value:
                missing_vars.append(env_var)
            else:
                config_dict[config_key] = value
        
        if missing_vars:
            raise ValueError(
                f"Missing required environment variables: {', '.join(missing_vars)}\n"
                f"Please set these environment variables before running AgentTeam."
            )
        
        # Optional variables with defaults
        config_dict.update({
            'openai_api_key': os.getenv('OPENAI_API_KEY'),
            'log_level': os.getenv('LOG_LEVEL', 'INFO'),
            'workflow_timeout': int(os.getenv('WORKFLOW_TIMEOUT', '300')),
        })
        
        return cls(**config_dict)
    
    def validate(self) -> bool:
        """Validate the configuration"""
        
        # Validate Slack token format
        if not self.slack_token.startswith('xoxb-'):
            raise ValueError("SLACK_BOT_TOKEN must start with 'xoxb-'")
        
        # Validate Slack channel format  
        if not self.slack_channel.startswith('C'):
            raise ValueError("SLACK_CHANNEL_ID must start with 'C'")
        
        # Validate timeout
        if self.workflow_timeout < 60:
            raise ValueError("WORKFLOW_TIMEOUT must be at least 60 seconds")
        
        return True
    
    def get_safe_summary(self) -> str:
        """Get a safe summary of configuration (without secrets)"""
        return f"""Configuration Summary:
• Slack Channel: {self.slack_channel}
• Slack Token: {self.slack_token[:20]}...
• OpenAI Key: {'✅ Set' if self.openai_api_key else '❌ Not set'}
• Log Level: {self.log_level}
• Workflow Timeout: {self.workflow_timeout}s"""