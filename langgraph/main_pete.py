#!/usr/bin/env python3
"""
AgentPete Main Entry Point
Starts the developer agent for monitoring and processing assigned tasks
"""
import os
import sys
import argparse
import asyncio
import logging
from typing import Optional

# Add the current directory to Python path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents.agent_pete import AgentPete
from jira.config import JiraConfig
from utils.config import Config
from utils.logging_config import setup_logging

logger = logging.getLogger(__name__)


def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description="AgentPete - AI-Powered Senior Developer Agent",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main_pete.py                    # Start continuous monitoring
  python main_pete.py --check-once       # Check for tasks once and exit
  python main_pete.py --debug-jira       # Test Jira connection only
  python main_pete.py --debug-slack      # Test Slack connection only
  python main_pete.py --status           # Show current status
        """
    )
    
    parser.add_argument(
        '--check-once', 
        action='store_true',
        help='Check for assigned tasks once and exit (no continuous monitoring)'
    )
    
    parser.add_argument(
        '--debug-jira',
        action='store_true', 
        help='Test Jira connection and list assigned tasks'
    )
    
    parser.add_argument(
        '--debug-slack',
        action='store_true',
        help='Test Slack connection and send test message'
    )
    
    parser.add_argument(
        '--status',
        action='store_true',
        help='Show current agent status and assigned tasks'
    )
    
    parser.add_argument(
        '--interval',
        type=int,
        default=60,
        help='Monitoring interval in seconds (default: 60)'
    )
    
    parser.add_argument(
        '--log-level',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
        default=os.getenv('LOG_LEVEL', 'INFO'),
        help='Set logging level'
    )
    
    return parser.parse_args()


def load_configuration() -> tuple[JiraConfig, Config]:
    """Load and validate configuration"""
    logger.info("📋 Loading configuration...")
    
    try:
        jira_config = JiraConfig.from_env()
        app_config = Config.from_environment()
        
        logger.info("✅ Configuration loaded successfully")
        logger.info(f"📊 Jira: {jira_config.base_url}")
        logger.info(f"📊 Project: {jira_config.default_project_key}")
        logger.info(f"📊 Slack Channel: {app_config.slack_channel}")
        
        return jira_config, app_config
        
    except Exception as e:
        logger.error(f"❌ Configuration error: {e}")
        logger.error("Please check your environment variables:")
        logger.error("  • JIRA_BASE_URL")
        logger.error("  • JIRA_USERNAME") 
        logger.error("  • JIRA_API_TOKEN")
        logger.error("  • JIRA_DEFAULT_PROJECT")
        logger.error("  • SLACK_BOT_TOKEN")
        logger.error("  • SLACK_CHANNEL_ID")
        raise


def create_agent_pete(jira_config: JiraConfig, app_config: Config) -> AgentPete:
    """Create and initialize AgentPete instance"""
    logger.info("🤖 Initializing AgentPete...")
    
    agent_pete = AgentPete(
        jira_base_url=jira_config.base_url,
        jira_username=jira_config.username,
        jira_api_token=jira_config.api_token,
        slack_token=app_config.slack_token,
        slack_channel=app_config.slack_channel,
        project_key=jira_config.default_project_key
    )
    
    logger.info(f"✅ {agent_pete.name} initialized successfully")
    return agent_pete


async def debug_jira_connection(agent_pete: AgentPete):
    """Debug Jira connection and show assigned tasks"""
    logger.info("🔧 Testing Jira connection...")
    
    if not agent_pete.authenticate():
        logger.error("❌ Jira authentication failed")
        return False
    
    logger.info("✅ Jira connection successful")
    
    # Check for assigned tasks
    new_tasks = agent_pete.check_for_assigned_tasks()
    
    if new_tasks:
        logger.info(f"📋 Found {len(new_tasks)} tasks assigned to {agent_pete.agent_username}:")
        for task in new_tasks:
            issue = task['issue']
            logger.info(f"  • {issue.key}: {issue.summary} ({issue.status})")
    else:
        logger.info(f"📋 No tasks currently assigned to {agent_pete.agent_username}")
    
    # Show general project info
    try:
        project_summary = agent_pete.jira_client.get_project_summary(agent_pete.project_key)
        logger.info(f"📊 Project Summary ({agent_pete.project_key}):")
        logger.info(f"  • Total Issues: {project_summary['issues']['total']}")
        logger.info(f"  • Stories: {project_summary['issues']['stories']}")
    except Exception as e:
        logger.warning(f"Could not retrieve project summary: {e}")
    
    return True


async def debug_slack_connection(agent_pete: AgentPete):
    """Debug Slack connection"""
    logger.info("🔧 Testing Slack connection...")
    
    slack_test = agent_pete.slack_client.test_connection()
    if not slack_test["success"]:
        logger.error(f"❌ Slack connection failed: {slack_test['error']}")
        return False
    
    logger.info("✅ Slack connection successful")
    logger.info(f"📱 Bot User ID: {slack_test.get('bot_user_id', 'Unknown')}")
    logger.info(f"📢 Channel: {slack_test.get('channel_name', 'Unknown')}")
    
    # Send test message
    test_message = f"""🧪 **AgentPete Connection Test**

This is a test message from {agent_pete.name} to verify Slack integration.

🤖 **Agent**: {agent_pete.name} ({agent_pete.role})
📋 **Project**: {agent_pete.project_key}
👤 **Monitoring**: Tasks assigned to '{agent_pete.agent_username}'

If you see this message, Slack integration is working correctly! ✅"""
    
    timestamp = agent_pete.slack_client.send_message(test_message)
    if timestamp:
        logger.info("✅ Test message sent successfully")
    else:
        logger.error("❌ Failed to send test message")
        return False
    
    return True


async def show_agent_status(agent_pete: AgentPete):
    """Show current agent status"""
    logger.info("📊 AgentPete Status Report")
    logger.info("=" * 50)
    
    # Agent metadata
    logger.info(f"🤖 Agent: {agent_pete.name} ({agent_pete.role})")
    logger.info(f"📋 Project: {agent_pete.project_key}")
    logger.info(f"👤 Monitoring: {agent_pete.agent_username}")
    logger.info(f"🔄 Monitoring Active: {agent_pete.monitoring_enabled}")
    
    # Check authentication
    if agent_pete.authenticate():
        logger.info("✅ All services authenticated")
    else:
        logger.error("❌ Authentication failed")
        return
    
    # Get task summary
    summary = agent_pete.get_task_summary()
    logger.info(f"📋 Assigned Tasks: {summary['total_assigned_tasks']}")
    logger.info(f"✅ Processed: {summary['processed_tasks']}")
    logger.info(f"🔄 New/In Progress: {summary['new_tasks']}")
    logger.info(f"❌ Errors: {summary['error_tasks']}")
    
    # Send status to Slack
    agent_pete.send_status_update()


async def run_single_check(agent_pete: AgentPete):
    """Run a single task check and exit"""
    logger.info("🔍 Running single task check...")
    
    if not agent_pete.start_task_monitoring():
        logger.error("❌ Failed to start task monitoring")
        return False
    
    try:
        result = agent_pete.run_monitoring_cycle()
        
        logger.info("📊 Check Results:")
        logger.info(f"  • New tasks found: {result['new_tasks_found']}")
        logger.info(f"  • Tasks processed: {len(result['processed_tasks'])}")
        logger.info(f"  • Errors: {len(result['errors'])}")
        logger.info(f"  • Duration: {result['duration_seconds']:.1f}s")
        
        if result['errors']:
            for error in result['errors']:
                logger.error(f"  ❌ {error['issue_key']}: {error['error']}")
        
        return result['success']
        
    finally:
        agent_pete.stop_monitoring()


async def run_continuous_monitoring(agent_pete: AgentPete, interval: int):
    """Run continuous task monitoring"""
    logger.info(f"🔄 Starting continuous monitoring (interval: {interval}s)")
    
    try:
        agent_pete.run_continuous_monitoring(check_interval=interval)
    except KeyboardInterrupt:
        logger.info("⏹️ Monitoring stopped by user")
    except Exception as e:
        logger.error(f"❌ Error in continuous monitoring: {e}")
        raise


async def main():
    """Main entry point"""
    args = parse_arguments()
    
    # Setup logging
    setup_logging(level=args.log_level)
    
    logger.info("🚀 Starting AgentPete - AI-Powered Senior Developer Agent")
    logger.info("=" * 60)
    
    try:
        # Load configuration
        jira_config, app_config = load_configuration()
        
        # Create agent
        agent_pete = create_agent_pete(jira_config, app_config)
        
        # Handle different modes
        if args.debug_jira:
            success = await debug_jira_connection(agent_pete)
            sys.exit(0 if success else 1)
            
        elif args.debug_slack:
            success = await debug_slack_connection(agent_pete)
            sys.exit(0 if success else 1)
            
        elif args.status:
            await show_agent_status(agent_pete)
            sys.exit(0)
            
        elif args.check_once:
            success = await run_single_check(agent_pete)
            sys.exit(0 if success else 1)
            
        else:
            # Default: continuous monitoring
            await run_continuous_monitoring(agent_pete, args.interval)
            
    except KeyboardInterrupt:
        logger.info("⏹️ AgentPete stopped by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"❌ Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    # Run the async main function
    asyncio.run(main())