"""
Multi-Agent Configuration Management for AgentTeam
Centralized configuration handling with validation for multiple agents
Supports manager agent that creates and coordinates specialized agents
"""
import os
from dataclasses import dataclass
from typing import Optional, Dict, List, Union
from enum import Enum


class AgentType(Enum):
    """Available agent types in the system"""
    MANAGER = "manager"
    PRODUCT_OWNER = "product_owner"
    DEVELOPER = "developer"
    TESTER = "tester"
    DEVOPS = "devops"


@dataclass
class AgentConfig:
    """Configuration for a single agent"""
    agent_type: AgentType
    agent_name: str
    slack_token: str
    slack_channel: str
    jira_username: str
    jira_api_token: str
    jira_default_project: Optional[str] = None
    
    def get_safe_summary(self) -> str:
        """Get a safe summary of agent configuration (without secrets)"""
        return f"""{self.agent_name} ({self.agent_type.value}):
• Slack Channel: {self.slack_channel}
• Slack Token: {self.slack_token[:20]}...
• Jira User: {self.jira_username}
• Jira Project: {self.jira_default_project}"""


@dataclass
class MultiAgentConfig:
    """Configuration class for multi-agent AgentTeam system"""
    
    # Shared configuration
    openai_api_key: Optional[str] = None
    jira_base_url: str = ""
    default_slack_channel: str = ""
    
    # Agent configurations
    agents: Dict[AgentType, AgentConfig] = None
    
    # System settings
    max_active_agents: int = 5
    agent_creation_timeout: int = 300
    inter_agent_timeout: int = 120
    project_coordination_channel: str = ""
    log_level: str = "INFO"
    workflow_timeout: int = 300  # 5 minutes default
    
    def __post_init__(self):
        if self.agents is None:
            self.agents = {}
    
    @classmethod
    def from_environment(cls) -> 'MultiAgentConfig':
        """Create multi-agent configuration from environment variables"""
        
        # Load shared configuration
        shared_config = {
            'openai_api_key': os.getenv('OPENAI_API_KEY'),
            'jira_base_url': os.getenv('JIRA_BASE_URL', ''),
            'default_slack_channel': os.getenv('DEFAULT_SLACK_CHANNEL_ID', ''),
            'max_active_agents': int(os.getenv('MAX_ACTIVE_AGENTS', '5')),
            'agent_creation_timeout': int(os.getenv('AGENT_CREATION_TIMEOUT', '300')),
            'inter_agent_timeout': int(os.getenv('INTER_AGENT_TIMEOUT', '120')),
            'project_coordination_channel': os.getenv('PROJECT_COORDINATION_CHANNEL_ID', ''),
            'log_level': os.getenv('LOG_LEVEL', 'INFO'),
            'workflow_timeout': int(os.getenv('WORKFLOW_TIMEOUT', '300')),
        }
        
        # Load agent configurations
        agents = {}
        
        # Define agent type mappings
        agent_mappings = {
            AgentType.MANAGER: 'MANAGER',
            AgentType.PRODUCT_OWNER: 'PRODUCT_OWNER', 
            AgentType.DEVELOPER: 'DEVELOPER',
            AgentType.TESTER: 'TESTER',
            AgentType.DEVOPS: 'DEVOPS'
        }
        
        for agent_type, env_prefix in agent_mappings.items():
            agent_config = cls._load_agent_config(agent_type, env_prefix)
            if agent_config:
                agents[agent_type] = agent_config
        
        shared_config['agents'] = agents
        return cls(**shared_config)
    
    @classmethod
    def _load_agent_config(cls, agent_type: AgentType, env_prefix: str) -> Optional[AgentConfig]:
        """Load configuration for a specific agent type"""
        
        # Check if agent configuration exists
        agent_name = os.getenv(f'{env_prefix}_AGENT_NAME')
        if not agent_name:
            return None
            
        slack_token = os.getenv(f'{env_prefix}_SLACK_BOT_TOKEN')
        slack_channel = os.getenv(f'{env_prefix}_SLACK_CHANNEL_ID')
        jira_username = os.getenv(f'{env_prefix}_JIRA_USERNAME')
        jira_api_token = os.getenv(f'{env_prefix}_JIRA_API_TOKEN')
        jira_project = os.getenv(f'{env_prefix}_JIRA_DEFAULT_PROJECT')
        
        # Validate required fields
        if not all([slack_token, slack_channel, jira_username, jira_api_token]):
            missing = []
            if not slack_token: missing.append(f'{env_prefix}_SLACK_BOT_TOKEN')
            if not slack_channel: missing.append(f'{env_prefix}_SLACK_CHANNEL_ID')
            if not jira_username: missing.append(f'{env_prefix}_JIRA_USERNAME')
            if not jira_api_token: missing.append(f'{env_prefix}_JIRA_API_TOKEN')
            
            print(f"Warning: Incomplete configuration for {agent_name}. Missing: {', '.join(missing)}")
            return None
        
        return AgentConfig(
            agent_type=agent_type,
            agent_name=agent_name,
            slack_token=slack_token,
            slack_channel=slack_channel,
            jira_username=jira_username,
            jira_api_token=jira_api_token,
            jira_default_project=jira_project
        )
    
    def get_agent_config(self, agent_type: AgentType) -> Optional[AgentConfig]:
        """Get configuration for a specific agent type"""
        return self.agents.get(agent_type)
    
    def get_available_agents(self) -> List[AgentType]:
        """Get list of available agent types"""
        return list(self.agents.keys())
    
    def has_manager_agent(self) -> bool:
        """Check if manager agent is configured"""
        return AgentType.MANAGER in self.agents
    
    def validate(self) -> bool:
        """Validate the multi-agent configuration"""
        
        # Validate shared configuration
        if not self.jira_base_url or not self.jira_base_url.startswith(('http://', 'https://')):
            raise ValueError("JIRA_BASE_URL must be a valid URL")
        
        if self.workflow_timeout < 60:
            raise ValueError("WORKFLOW_TIMEOUT must be at least 60 seconds")
        
        if self.max_active_agents < 1 or self.max_active_agents > 10:
            raise ValueError("MAX_ACTIVE_AGENTS must be between 1 and 10")
        
        # Validate each agent configuration
        for agent_type, agent_config in self.agents.items():
            if not agent_config.slack_token.startswith('xoxb-'):
                raise ValueError(f"{agent_config.agent_name} SLACK_BOT_TOKEN must start with 'xoxb-'")
            
            if not agent_config.slack_channel.startswith('C'):
                raise ValueError(f"{agent_config.agent_name} SLACK_CHANNEL_ID must start with 'C'")
        
        # Ensure manager agent exists
        if not self.has_manager_agent():
            raise ValueError("Manager agent configuration is required for multi-agent system")
        
        return True
    
    def get_safe_summary(self) -> str:
        """Get a safe summary of multi-agent configuration (without secrets)"""
        agent_summary = "\n".join([f"• {config.get_safe_summary()}" for config in self.agents.values()])
        
        return f"""Multi-Agent Configuration Summary:
• Jira Base URL: {self.jira_base_url}
• OpenAI Key: {'✅ Set' if self.openai_api_key else '❌ Not set'}
• Max Active Agents: {self.max_active_agents}
• Project Coordination Channel: {self.project_coordination_channel}
• Log Level: {self.log_level}
• Workflow Timeout: {self.workflow_timeout}s

Configured Agents ({len(self.agents)}):
{agent_summary}"""


# Legacy Config class for backward compatibility
@dataclass
class Config:
    """Legacy configuration class for backward compatibility"""
    
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
        """Create legacy configuration from environment variables"""
        
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
        """Validate the legacy configuration"""
        
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
        return f"""Legacy Configuration Summary:
• Slack Channel: {self.slack_channel}
• Slack Token: {self.slack_token[:20]}...
• OpenAI Key: {'✅ Set' if self.openai_api_key else '❌ Not set'}
• Log Level: {self.log_level}
• Workflow Timeout: {self.workflow_timeout}s"""