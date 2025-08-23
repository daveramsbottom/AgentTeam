#!/usr/bin/env python3
"""
AgentTeam Main Entry Point
Refactored architecture with modular components
"""
import os
import sys
import logging
from typing import Optional

# Import our refactored components
from agents.agent_ian import AgentIan
from utils.logging_config import setup_logging
from utils.config import Config

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)


def debug_slack_integration(config: Config) -> bool:
    """Debug Slack integration separately"""
    print("🔍 Testing Slack Integration - Enhanced Message Detection Debug")
    
    print(f"💬 Using Slack token: {config.slack_token[:20]}...")
    print(f"📢 Using channel ID: {config.slack_channel}")
    
    # Create AgentIan for debugging
    agent_ian = AgentIan(
        config.taiga_url, 
        config.taiga_username, 
        config.taiga_password,
        config.slack_token, 
        config.slack_channel
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
    print(f"   1. If no messages detected, send a test message in Slack")
    print(f"   2. The enhanced filtering should better distinguish human vs bot messages")
    print(f"   3. Check the analysis above to see if your message is marked as 'Is Human: True'")
    
    return test_result['success']


def run_full_workflow(config: Config) -> bool:
    """Run the complete AgentIan workflow"""
    print("🤖 Starting Enhanced AgentIan - Product Owner Agent")
    
    # Initialize AgentIan
    agent_ian = AgentIan(
        config.taiga_url,
        config.taiga_username, 
        config.taiga_password,
        config.slack_token,
        config.slack_channel
    )
    
    print(f"🔗 Connecting to Taiga at: {config.taiga_url}")
    print(f"💬 Slack integration enabled for channel: {config.slack_channel}")
    
    # Authenticate with all services
    if not agent_ian.authenticate():
        print("❌ Authentication failed. Exiting.")
        return False
    
    # Get projects and find the Agent Team Project
    print("📋 Fetching projects...")
    projects = agent_ian.taiga_client.get_projects()
    
    if not projects:
        print("❌ No projects found or error fetching projects")
        return False
    
    print(f"📊 Found {len(projects)} project(s):")
    for project in projects:
        print(f"   - {project.get('name')} (ID: {project.get('id')})")
    
    # Focus on the Agent Team Project
    agent_project = None
    for project in projects:
        if "Agent Team" in project.get('name', ''):
            agent_project = project
            break
    
    if not agent_project:
        print("❌ Could not find 'Agent Team Project'")
        return False
    
    project_id = agent_project.get('id')
    project_name = agent_project.get('name')
    
    print(f"\n🎯 Working with project: {project_name} (ID: {project_id})")
    
    # Show current project status
    print("📚 Getting current project status...")
    status = agent_ian.get_project_status(project_id)
    
    if "error" not in status:
        print(f"📖 Found {status['total_stories']} existing user story(ies)")
        for story in status.get('stories', []):
            assigned = f" → {story['assigned_to']}" if story['assigned_to'] else ""
            print(f"   📄 {story['title']} (Status: {story['status']}{assigned})")
    
    # Show AgentIan capabilities
    print(f"\n{agent_ian.get_capabilities_summary()}")
    
    # Test project goals
    print("\n🎯 Testing AgentIan's Enhanced Workflow...")
    
    test_goals = [
        "Build a modern web application for task management with user authentication, real-time collaboration, and mobile-responsive design",
        "Create a REST API for a blogging platform with posts, comments, user management, and content moderation features", 
        "Develop a mobile-friendly e-commerce website with product catalog, shopping cart, payment integration, and order tracking"
    ]
    
    # Process the first project goal
    project_goal = test_goals[0]
    print(f"\n🚀 Processing enhanced project goal: {project_goal}")
    print("💬 Check your Slack channel for interactive questions and updates!")
    
    # Send initial capabilities message to Slack
    agent_ian.send_status_update(
        f"Ready to process project goal! 🚀\n\n"
        f"**Goal:** {project_goal}\n\n"
        f"I'll analyze this, ask clarifying questions if needed, and create detailed user stories."
    )
    
    # Execute the workflow
    result = agent_ian.process_project_goal(project_goal, project_id)
    
    print(f"\n🎯 Enhanced Workflow Results:")
    print(f"   Success: {result['success']}")
    print(f"   Final State: {result['state']}")
    print(f"   Stories Created: {result['stories_created']}")
    
    if result.get('clarification_needed'):
        print(f"   🤔 Clarification Was Requested")
        if result.get('clarification_responses'):
            response_preview = result['clarification_responses'][0][:100]
            print(f"   💬 Received Response: {response_preview}...")
    
    if result.get('error'):
        print(f"   ❌ Error: {result['error']}")
        return False
    
    if result['success']:
        print(f"\n✅ AgentIan successfully processed the project goal!")
        print(f"📄 Check your Taiga project: http://localhost:9000")
        print(f"💬 Review the full conversation in Slack")
        
        # Send final status update
        agent_ian.send_status_update(
            f"Project analysis complete! ✅\n\n"
            f"Created {result['stories_created']} user stories with detailed tasks.\n"
            f"Ready for the development team to begin work!"
        )
    
    return result['success']


def show_usage():
    """Show usage information"""
    print("""
🤖 AgentTeam - Enhanced AgentIan Usage:

Commands:
  python main.py                    Run full workflow
  python main.py --debug-slack      Debug Slack integration only  
  python main.py --help            Show this help message

Environment Variables Required:
  OPENAI_API_KEY      OpenAI API key for future LLM integration
  SLACK_BOT_TOKEN     Your Slack bot token (xoxb-...)  
  SLACK_CHANNEL_ID    Target Slack channel ID (C...)

Optional Environment Variables:
  TAIGA_API_URL       Taiga API URL (default: http://taiga-back:8000/api/v1)
  TAIGA_USERNAME      Taiga username (default: agentian)
  TAIGA_PASSWORD      Taiga password (default: password123)

Examples:
  # Run with debug
  python main.py --debug-slack
  
  # Run full workflow  
  python main.py
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
            except Exception as e:
                print(f"❌ Configuration error: {e}")
                return
            
            # Run Slack debug only
            success = debug_slack_integration(config)
            if success:
                print("\n✅ Slack integration test completed successfully!")
            else:
                print("\n❌ Slack integration test failed!")
            return
    
    # Load configuration for full workflow
    try:
        config = Config.from_environment()
        print("✅ Configuration loaded successfully")
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        print("\nPlease check your environment variables. Use --help for details.")
        return
    
    # Run full workflow
    print("\n" + "="*60)
    print("🚀 ENHANCED AGENTTEAM - AGENTIAN WORKFLOW")
    print("="*60)
    
    success = run_full_workflow(config)
    
    print("\n" + "="*60)
    if success:
        print("✅ AgentIan workflow completed successfully!")
        print("🔍 Next steps:")
        print("   • Review user stories in Taiga: http://localhost:9000") 
        print("   • Check conversation history in Slack")
        print("   • Ready for AgentPete (Developer) to start work")
    else:
        print("❌ AgentIan workflow encountered errors")
        print("🔍 Troubleshooting:")
        print("   • Check logs for detailed error information")
        print("   • Verify Taiga and Slack connections") 
        print("   • Try --debug-slack to test integration")
    
    print("="*60)
    print("🤖 Enhanced AgentTeam session complete!")


if __name__ == "__main__":
    main()