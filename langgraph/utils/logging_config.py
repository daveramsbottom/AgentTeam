"""
Centralized Logging Configuration for AgentTeam
Provides consistent logging setup across all modules
"""
import logging
import sys
from typing import Optional


def setup_logging(level: str = "INFO", format_type: str = "detailed") -> None:
    """
    Set up centralized logging for AgentTeam
    
    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR)
        format_type: Format type ('simple', 'detailed', 'json')
    """
    
    # Convert string level to logging constant
    numeric_level = getattr(logging, level.upper(), logging.INFO)
    
    # Define different format styles
    formats = {
        'simple': '%(levelname)s: %(message)s',
        'detailed': '%(asctime)s | %(name)-20s | %(levelname)-8s | %(message)s',
        'json': '{"timestamp": "%(asctime)s", "logger": "%(name)s", "level": "%(levelname)s", "message": "%(message)s"}'
    }
    
    # Choose format
    log_format = formats.get(format_type, formats['detailed'])
    
    # Configure root logger
    logging.basicConfig(
        level=numeric_level,
        format=log_format,
        datefmt='%Y-%m-%d %H:%M:%S',
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    # Set specific logger levels for better control
    logger_configs = {
        'requests': logging.WARNING,
        'urllib3': logging.WARNING,
        'httpx': logging.WARNING,
        'openai': logging.WARNING,
        'slack_sdk': logging.WARNING,
    }
    
    for logger_name, logger_level in logger_configs.items():
        logging.getLogger(logger_name).setLevel(logger_level)
    
    # Create AgentTeam specific loggers
    setup_agent_loggers(numeric_level)
    
    # Log the setup
    logger = logging.getLogger(__name__)
    logger.info(f"🔧 Logging configured - Level: {level}, Format: {format_type}")


def setup_agent_loggers(level: int) -> None:
    """Set up specific loggers for AgentTeam components"""
    
    agent_loggers = [
        'agents.agent_ian',
        'agents.agent_pete', 
        'agents.agent_ron',
        'agents.agent_dave',
        'communication.slack_client',
        'workflows.workflow_engine',
        'workflows.story_breakdown',
        'taiga.client',
    ]
    
    for logger_name in agent_loggers:
        logger = logging.getLogger(logger_name)
        logger.setLevel(level)
        
        # Add emoji prefixes for different components
        if 'agent_' in logger_name:
            logger.addFilter(EmojiLogFilter('🤖'))
        elif 'slack' in logger_name:
            logger.addFilter(EmojiLogFilter('💬'))
        elif 'workflow' in logger_name:
            logger.addFilter(EmojiLogFilter('🔄'))
        elif 'taiga' in logger_name:
            logger.addFilter(EmojiLogFilter('📋'))


class EmojiLogFilter(logging.Filter):
    """Add emoji prefixes to log messages for better visual distinction"""
    
    def __init__(self, emoji: str):
        super().__init__()
        self.emoji = emoji
    
    def filter(self, record: logging.LogRecord) -> bool:
        # Only add emoji if message doesn't already start with one
        if not any(ord(char) > 127 for char in record.getMessage()[:2]):
            record.msg = f"{self.emoji} {record.msg}"
        return True


def get_logger(name: str) -> logging.Logger:
    """Get a logger with consistent naming"""
    return logging.getLogger(name)


def log_function_call(func_name: str, args: dict = None, level: str = "DEBUG"):
    """Decorator to log function calls"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            logger = get_logger(func.__module__)
            
            arg_str = ""
            if args or kwargs:
                arg_parts = []
                if args:
                    arg_parts.append(f"args={args}")
                if kwargs:
                    arg_parts.append(f"kwargs={kwargs}")
                arg_str = f" with {', '.join(arg_parts)}"
            
            getattr(logger, level.lower())(f"🔍 Calling {func_name}{arg_str}")
            
            try:
                result = func(*args, **kwargs)
                getattr(logger, level.lower())(f"✅ {func_name} completed successfully")
                return result
            except Exception as e:
                logger.error(f"❌ {func_name} failed: {e}")
                raise
                
        return wrapper
    return decorator


# Usage examples and testing
if __name__ == "__main__":
    # Test different logging configurations
    setup_logging(level="DEBUG", format_type="detailed")
    
    logger = get_logger(__name__)
    
    logger.debug("🔍 Debug message test")
    logger.info("ℹ️ Info message test") 
    logger.warning("⚠️ Warning message test")
    logger.error("❌ Error message test")
    
    # Test component-specific loggers
    slack_logger = get_logger("communication.slack_client")
    slack_logger.info("Slack client message")
    
    agent_logger = get_logger("agents.agent_ian")
    agent_logger.info("AgentIan message")
    
    workflow_logger = get_logger("workflows.workflow_engine")
    workflow_logger.info("Workflow engine message")