#!/usr/bin/env python3
"""
AgentTeam Main Entry Point
Refactored architecture with FIXED interactive response handling
Now using Jira for professional project management
"""
import os
import sys
import logging
from typing import Optional

# Import our refactored components
from agents.agent_ian import AgentIan
from utils.logging_config import setup_logging
from utils.config import Config
from jira.config import JiraConfig

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)


def test_interactive_response(config: Config, jira_config: JiraConfig) -> bool:
    """Test AgentIan's interactive response capability"""
    print("🧪 Testing AgentIan's Interactive Response Capability")
    
    # Create AgentIan
    agent_ian = AgentIan(
        jira_config.base_url,
        jira_config.username,
        jira_config.api_token,
        config.slack_token, 
        config.slack_channel,
        jira_config.default_project_key
    )
    
    # Test authentication first
    if not agent_ian.authenticate():
        print("❌ Authentication failed - cannot test interactive responses")
        return False
    
    print("\n🧪 Running interactive workflow test...")
    print("💬 Check your Slack channel - AgentIan will ask you a question!")
    print("⏳ You have 2 minutes to respond...")
    
    # Run the interactive test
    test_result = agent_ian.test_interactive_workflow()
    
    print(f"\n📊 Interactive Test Results:")
    print(f"   Success: {test_result['success']}")
    print(f"   Tracking Code: {test_result.get('tracking_code', 'N/A')}")
    print(f"   Response Received: {test_result.get('response_received', False)}")
    
    if test_result.get('response_text'):
        response_preview = test_result['response_text'][:100]
        print(f"   Your Response: {response_preview}{'...' if len(test_result['response_text']) > 100 else ''}")
    
    if test_result['success'] and test_result.get('response_received'):
        print("\n✅ Interactive response system is working perfectly!")
        print("🎉 AgentIan successfully waited for and processed your response!")
    elif test_result['success'] and not test_result.get('response_received'):
        print("\n⚠️ Test completed but no response received.")
        print("💡 Try sending a message in Slack after AgentIan asks the question.")
    else:
        print(f"\n❌ Test failed: {test_result.get('error', 'Unknown error')}")
    
    return test_result['success']


def debug_slack_integration(config: Config, jira_config: JiraConfig) -> bool:
    """Debug Slack integration separately"""
    print("🔍 Testing Slack Integration - Enhanced Message Detection Debug")
    
    print(f"💬 Using Slack token: {config.slack_token[:20]}...")
    print(f"📢 Using channel ID: {config.slack_channel}")
    
    # Create AgentIan for debugging
    agent_ian = AgentIan(
        jira_config.base_url,
        jira_config.username,
        jira_config.api_token,
        config.slack_token, 
        config.slack_channel,
        jira_config.default_project_key
    )
    
    # Test authentication first
    if not agent_ian.authenticate():
        print("❌ Authentication failed - cannot test Slack integration")
        return False
    
    # Run Slack debug test
    print("\n🧪 Running enhanced message detection test...")
    test_result = agent_ian.debug_slack_integration()
    
    print(f"\n📊 Enhanced Test Results:")
    print(f"   Success: {test_result['success']}")
    
    if test_result['success']:
        print(f"   Bot User ID: {test_result['bot_user_id']}")
        print(f"   Test Timestamp: {test_result['test_timestamp']}")
        print(f"   Tracking Code: {test_result['tracking_code']}")
        print(f"   Filtered Messages Found: {test_result['filtered_messages']}")
        print(f"   Total Recent Messages: {test_result['total_recent_messages']}")
        
        print(f"\n🔍 Recent Message Analysis:")
        for i, msg_details in enumerate(test_result['recent_message_details']):
            print(f"   {i+1}. User: {msg_details['user']}, Bot ID: {msg_details['bot_id']}")
            print(f"      Subtype: {msg_details['subtype']}, Is Human: {msg_details['is_human']}")
            print(f"      Text: '{msg_details['text']}'")
        
        if test_result['filtered_messages'] == 0:
            print("\n⚠️  No human messages detected. Try:")
            print("   1. Send a simple message in the Slack channel")
            print("   2. Make sure the bot is added to the channel")
            print("   3. Check that the channel ID is correct")
        else:
            print(f"\n✅ Message detection is working! Found {test_result['filtered_messages']} human messages.")
            
    else:
        print(f"   Error: {test_result.get('error')}")
    
    print(f"\n💡 Next Steps:")
    print(f"   1. If message detection works, try: python main.py --test-interactive")
    print(f"   2. This will test the full response waiting workflow")
    print(f"   3. Make sure to respond when AgentIan asks a question!")
    
    return test_result['success']


def run_full_workflow(config: Config, jira_config: JiraConfig) -> bool:
    """Run the complete AgentIan workflow with interactive features"""
    print("🤖 Starting Enhanced AgentIan - Product Owner Agent")
    
    # Initialize AgentIan
    agent_ian = AgentIan(
        jira_config.base_url,
        jira_config.username,
        jira_config.api_token,
        config.slack_token,
        config.slack_channel,
        jira_config.default_project_key
    )
    
    print(f"🔗 Connecting to Jira at: {jira_config.base_url}")
    print(f"📋 Using Jira project: {jira_config.default_project_key}")
    print(f"💬 Slack integration enabled for channel: {config.slack_channel}")
    
    # Authenticate with all services
    if not agent_ian.authenticate():
        print("❌ Authentication failed. Exiting.")
        return False
    
    # Get Jira project details
    print("📋 Connecting to Jira project...")
    
    # Show current project status
    print("📚 Getting current project status...")
    status = agent_ian.get_project_status()
    
    if "error" not in status:
        print(f"🎯 Working with project: {status['project_name']} ({status['project_key']})")
        print(f"📖 Found {status['total_stories']} existing user story(ies)")
        for story in status.get('stories', []):
            assigned = f" → {story['assigned_to']}" if story['assigned_to'] else ""
            print(f"   📄 {story['title']} (Status: {story['status']}{assigned})")
    else:
        print(f"⚠️ Could not fetch project status: {status['error']}")
        print("Continuing with workflow...")
    
    # Show AgentIan capabilities
    print(f"\n{agent_ian.get_capabilities_summary()}")
    
    # Test project goals with INTERACTIVE workflow
    print("\n🎯 Starting AgentIan's INTERACTIVE Workflow...")
    print("💬 IMPORTANT: Watch your Slack channel! AgentIan will ask questions and wait for your responses!")
    
    test_goals = [
        "Build a modern web application for task management with user authentication, real-time collaboration, and mobile-responsive design",
        "Create a REST API for a blogging platform with posts, comments, user management, and content moderation features", 
        "Develop a mobile-friendly e-commerce website with product catalog, shopping cart, payment integration, and order tracking"
    ]
    
    # Process the first project goal with INTERACTIVE features
    project_goal = test_goals[0]
    print(f"\n🚀 Processing INTERACTIVE project goal: {project_goal}")
    print("💬 Check your Slack channel for questions! AgentIan will wait for your responses!")
    
    # Send initial notification
    agent_ian.send_status_update(
        f"🚀 Starting INTERACTIVE project analysis!\n\n"
        f"**Goal:** {project_goal}\n\n"
        f"I'll analyze this, ask clarifying questions, WAIT for your responses, and create detailed user stories based on your input!"
    )
    
    # Execute the INTERACTIVE workflow
    result = agent_ian.process_project_goal_with_interaction(project_goal)
    
    print(f"\n🎯 INTERACTIVE Workflow Results:")
    print(f"   Success: {result['success']}")
    print(f"   Final State: {result['state']}")
    print(f"   Stories Created: {result['stories_created']}")
    
    if result.get('clarification_needed'):
        print(f"   🤔 Clarification Was Requested: Yes")
        if result.get('clarification_response'):
            response_preview = result['clarification_response'][:100]
            print(f"   💬 Your Response: {response_preview}...")
            print(f"   ✅ AgentIan successfully processed your input!")
        else:
            print(f"   ⏰ No response received within timeout")
    
    if result.get('error'):
        print(f"   ❌ Error: {result['error']}")
        return False
    
    if result['success']:
        print(f"\n✅ AgentIan successfully processed the project goal!")
        print(f"📄 Check your Jira project: {jira_config.base_url}/browse/{jira_config.default_project_key}")
        print(f"💬 Review the full conversation in Slack")
        
        # Send final status update
        agent_ian.send_status_update(
            f"🎉 INTERACTIVE project analysis complete! ✅\n\n"
            f"Created {result['stories_created']} user stories based on your input.\n"
            f"Ready for the development team to begin work!"
        )
    
    return result['success']


def show_usage():
    """Show usage information"""
    print("""
🤖 AgentTeam - Enhanced AgentIan Usage:

Commands:
  python main.py                      Run full interactive workflow
  python main.py --debug-slack        Debug Slack integration only  
  python main.py --test-interactive   Test interactive response system
  python main.py --help              Show this help message

Environment Variables Required:
  OPENAI_API_KEY         OpenAI API key for future LLM integration
  SLACK_BOT_TOKEN        Your Slack bot token (xoxb-...)  
  SLACK_CHANNEL_ID       Target Slack channel ID (C...)
  JIRA_BASE_URL          Jira instance URL (e.g., https://daveramsbottom.atlassian.net)
  JIRA_USERNAME          Jira username/email
  JIRA_API_TOKEN         Jira API token (not password)
  JIRA_DEFAULT_PROJECT   Jira project key (e.g., AT for "Agent Team")

Examples:
  # Test interactive responses
  python main.py --test-interactive
  
  # Debug Slack message detection
  python main.py --debug-slack
  
  # Run full interactive workflow  
  python main.py

Testing Steps:
  1. First run: python main.py --debug-slack
  2. Then run: python main.py --test-interactive  
  3. Finally run: python main.py (full workflow)
""")


def main():
    """Main entry point"""
    # Handle command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] in ["--help", "-h"]:
            show_usage()
            return
        elif sys.argv[1] == "--debug-slack":
            # Load configuration
            try:
                config = Config.from_environment()
                jira_config = JiraConfig.from_env()
            except Exception as e:
                print(f"❌ Configuration error: {e}")
                return
            
            # Run Slack debug only
            success = debug_slack_integration(config, jira_config)
            if success:
                print("\n✅ Slack integration test completed successfully!")
                print("💡 Next: Try 'python main.py --test-interactive' to test response waiting!")
            else:
                print("\n❌ Slack integration test failed!")
            return
        elif sys.argv[1] == "--test-interactive":
            # Load configuration
            try:
                config = Config.from_environment()
                jira_config = JiraConfig.from_env()
            except Exception as e:
                print(f"❌ Configuration error: {e}")
                return
            
            # Run interactive response test
            success = test_interactive_response(config, jira_config)
            if success:
                print("\n🎉 Interactive response system working perfectly!")
                print("💡 Next: Try 'python main.py' for the full workflow!")
            else:
                print("\n❌ Interactive response test failed!")
                print("💡 Try 'python main.py --debug-slack' first to verify basic Slack connection.")
            return
    
    # Load configuration for full workflow
    try:
        config = Config.from_environment()
        jira_config = JiraConfig.from_env()
        print("✅ Configuration loaded successfully")
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        print("\nPlease check your environment variables. Use --help for details.")
        return
    
    # Run full workflow
    print("\n" + "="*70)
    print("🚀 ENHANCED AGENTTEAM - INTERACTIVE AGENTIAN WORKFLOW")
    print("="*70)
    
    success = run_full_workflow(config, jira_config)
    
    print("\n" + "="*70)
    if success:
        print("✅ AgentIan INTERACTIVE workflow completed successfully!")
        print("🔍 Next steps:")
        print(f"   • Review user stories in Jira: {jira_config.base_url}/browse/{jira_config.default_project_key}") 
        print("   • Check conversation history in Slack")
        print("   • Ready for AgentPete (Developer) to start work")
        print("   • Your clarifications were incorporated into the stories!")
    else:
        print("❌ AgentIan workflow encountered errors")
        print("🔍 Troubleshooting:")
        print("   • Check logs for detailed error information")
        print("   • Verify Jira and Slack connections") 
        print("   • Try --debug-slack to test basic integration")
        print("   • Try --test-interactive to test response waiting")
    
    print("="*70)
    print("🤖 Enhanced AgentTeam session complete!")


if __name__ == "__main__":
    main()