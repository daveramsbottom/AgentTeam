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
from agents.enhanced_agent_ian import EnhancedAgentIan
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
    
    # Send intelligent initial notification
    agent_ian.send_status_update(
        f"🚀 **Starting Enhanced Project Analysis**\n\n"
        f"**Goal:** {project_goal}\n\n"
        f"**Process:** AI analysis → Clarifying questions → Enhanced user stories\n"
        f"**Features:** Intelligent status updates, story refinement, human-like communication\n\n"
        f"💬 Watch for my questions - I'll wait for your detailed responses!"
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
        
        # Send intelligent final status update using new reporting features
        print("📊 Generating intelligent project status report...")
        agent_ian.send_intelligent_status_report()
        
        # Run iterative refinement cycle for human-like continuous improvement
        print("🔄 Starting iterative story refinement cycle...")
        refinement_result = agent_ian.run_iterative_refinement_cycle(project_goal)
        
        if refinement_result.get('success'):
            print(f"✅ Refinement cycle completed: {refinement_result.get('status')}")
            if refinement_result.get('refinements_applied', 0) > 0:
                print(f"🔧 Applied {refinement_result['refinements_applied']} story improvements")
            if refinement_result.get('human_response'):
                print(f"💬 Human feedback received and processed")
        else:
            print(f"⚠️ Refinement cycle had issues: {refinement_result.get('error')}")
            
            # Fallback to basic refinement suggestions
            print("📝 Providing basic refinement suggestions as fallback...")
            refinement_analysis = agent_ian.propose_story_refinements(project_goal)
            
            if refinement_analysis.get('success') and refinement_analysis.get('refinements_needed', 0) > 0:
                refinement_msg = f"💡 **Story Refinement Suggestions**\n\n"
                refinement_msg += f"Found {refinement_analysis['refinements_needed']} potential improvements:\n\n"
                
                for refinement in refinement_analysis['story_refinements'][:3]:  # Show top 3
                    refinement_msg += f"• **{refinement['title']}**\n"
                    refinement_msg += f"  {refinement['suggestion']}\n\n"
                
                if refinement_analysis['phase_suggestions']:
                    refinement_msg += f"**Next Phase Recommendations:**\n"
                    for suggestion in refinement_analysis['phase_suggestions']:
                        refinement_msg += f"• {suggestion['suggestion']}\n"
                
                agent_ian.send_status_update(refinement_msg)
    
    return result['success']


def test_enhanced_agent(config: Config, jira_config: JiraConfig) -> bool:
    """Test Enhanced AgentIan with flexible architecture"""
    print("🚀 Testing Enhanced AgentIan - Flexible Architecture")
    
    # Create Enhanced AgentIan
    enhanced_ian = EnhancedAgentIan(
        jira_config.base_url,
        jira_config.username,
        jira_config.api_token,
        config.slack_token,
        config.slack_channel,
        jira_config.default_project_key
    )
    
    # Test authentication
    if not enhanced_ian.authenticate():
        print("❌ Enhanced AgentIan authentication failed")
        return False
    
    print("✅ Enhanced AgentIan authenticated successfully")
    print("\n🧪 Testing flexible architecture components...")
    
    # Test state machine
    state_info = enhanced_ian.state_machine.get_current_state_info()
    print(f"📊 State Machine: {state_info['current_state']} (timeout: {state_info['idle_timeout']}s)")
    
    # Test monitoring system status
    monitor_status = enhanced_ian.get_monitoring_status()
    print(f"🔍 Monitoring System: {monitor_status['active_monitors']} monitors, {monitor_status['registered_handlers']} handlers")
    
    # Test capabilities
    capabilities = enhanced_ian.get_enhanced_capabilities_summary()
    print(f"\n🤖 Enhanced Capabilities Preview:")
    print(capabilities.split('\n')[0])  # Show title
    print("   • 🧠 Intelligent context analysis")
    print("   • 🔄 Dynamic state machine workflows") 
    print("   • 📊 Real-time event monitoring")
    print("   • 💬 Human-like interactions")
    
    # Send test notification
    test_message = (
        "🧪 **Enhanced AgentIan Test Complete**\n\n"
        "**Architecture:** Flexible state machine + Event monitoring\n"
        "**Features:** Context-aware analysis, intelligent responses\n"
        "**Status:** Ready for continuous monitoring or direct interaction\n\n"
        "💡 Try asking me about project status or start continuous monitoring!"
    )
    
    enhanced_ian.slack_client.send_message(test_message, username=enhanced_ian.name)
    
    print("\n✅ Enhanced AgentIan test completed successfully!")
    print("💡 Next: Try 'python main.py --enhanced-monitoring' for continuous mode")
    
    return True


def run_enhanced_monitoring(config: Config, jira_config: JiraConfig) -> bool:
    """Run Enhanced AgentIan in continuous monitoring mode"""
    print("🔄 Starting Enhanced AgentIan - Continuous Monitoring Mode")
    
    # Create Enhanced AgentIan
    enhanced_ian = EnhancedAgentIan(
        jira_config.base_url,
        jira_config.username,
        jira_config.api_token,
        config.slack_token,
        config.slack_channel,
        jira_config.default_project_key
    )
    
    # Authenticate
    if not enhanced_ian.authenticate():
        print("❌ Authentication failed")
        return False
    
    print(f"🔗 Connected to: {jira_config.base_url}/browse/{jira_config.default_project_key}")
    print(f"💬 Monitoring Slack channel: {config.slack_channel}")
    
    # Start continuous monitoring
    try:
        enhanced_ian.start_continuous_monitoring()
        
        print("\n🤖 Enhanced AgentIan is now running in continuous mode!")
        print("💡 Features active:")
        print("   • 🔍 Slack message monitoring (30s intervals)")
        print("   • 📊 Jira backlog change detection (60s intervals)")
        print("   • 🧠 Intelligent context analysis for all requests")
        print("   • 🔄 Dynamic workflow state management")
        print("   • 💓 Automated health checks (5min intervals)")
        
        print("\n📱 Try these interactions:")
        print("   • Send any message in Slack - I'll analyze it intelligently")
        print("   • Ask for 'status' - I'll provide smart project updates") 
        print("   • Request 'help' - I'll show enhanced capabilities")
        print("   • Change story status in Jira - I'll detect and analyze impact")
        
        print("\n⚠️  Press Ctrl+C to stop monitoring")
        
        # Keep running until interrupted
        import signal
        import time
        
        def signal_handler(sig, frame):
            print("\n🛑 Shutting down Enhanced AgentIan...")
            enhanced_ian.stop_monitoring()
            print("✅ Enhanced AgentIan stopped successfully")
            sys.exit(0)
        
        signal.signal(signal.SIGINT, signal_handler)
        
        # Keep the main thread alive
        while True:
            time.sleep(60)  # Check every minute
            status = enhanced_ian.get_monitoring_status()
            if not status['is_running']:
                break
        
        return True
        
    except KeyboardInterrupt:
        print("\n🛑 Monitoring stopped by user")
        enhanced_ian.stop_monitoring()
        return True
    except Exception as e:
        print(f"❌ Error in continuous monitoring: {e}")
        enhanced_ian.stop_monitoring()
        return False


def show_usage():
    """Show usage information"""
    print("""
🤖 AgentTeam - Enhanced AgentIan Usage:

Commands:
  python main.py                        Run legacy interactive workflow
  python main.py --enhanced              Test enhanced AgentIan architecture
  python main.py --enhanced-monitoring   Run continuous monitoring mode (NEW!)
  python main.py --debug-slack          Debug Slack integration only  
  python main.py --test-interactive     Test interactive response system
  python main.py --help                Show this help message

🆕 Enhanced Features:
  --enhanced              Test flexible state machine + intelligent analysis
  --enhanced-monitoring   Continuous event-driven operation (recommended!)

Environment Variables Required:
  OPENAI_API_KEY         OpenAI API key for intelligent analysis
  SLACK_BOT_TOKEN        Your Slack bot token (xoxb-...)  
  SLACK_CHANNEL_ID       Target Slack channel ID (C...)
  JIRA_BASE_URL          Jira instance URL (e.g., https://daveramsbottom.atlassian.net)
  JIRA_USERNAME          Jira username/email
  JIRA_API_TOKEN         Jira API token (not password)
  JIRA_DEFAULT_PROJECT   Jira project key (e.g., AT for "Agent Team")

Examples:
  # Test enhanced architecture
  python main.py --enhanced
  
  # Run continuous intelligent monitoring (RECOMMENDED)
  python main.py --enhanced-monitoring
  
  # Legacy interactive mode
  python main.py --test-interactive

🚀 New Architecture Benefits:
  • 🧠 No more generic questions - intelligent context analysis
  • 🔄 Flexible state machine replaces hardcoded workflows  
  • 📊 Real-time backlog monitoring with change detection
  • 💬 Event-driven responses to Slack messages
  • 🤖 Human-like behavior with idle states and progress awareness
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
        elif sys.argv[1] == "--enhanced":
            # Load configuration
            try:
                config = Config.from_environment()
                jira_config = JiraConfig.from_env()
            except Exception as e:
                print(f"❌ Configuration error: {e}")
                return
            
            # Test enhanced AgentIan
            success = test_enhanced_agent(config, jira_config)
            if success:
                print("\n🚀 Enhanced AgentIan architecture test completed!")
                print("💡 Next: Try 'python main.py --enhanced-monitoring' for continuous operation!")
            else:
                print("\n❌ Enhanced AgentIan test failed!")
            return
        elif sys.argv[1] == "--enhanced-monitoring":
            # Load configuration
            try:
                config = Config.from_environment()
                jira_config = JiraConfig.from_env()
            except Exception as e:
                print(f"❌ Configuration error: {e}")
                return
            
            # Run enhanced monitoring mode
            success = run_enhanced_monitoring(config, jira_config)
            if success:
                print("\n✅ Enhanced monitoring completed successfully!")
            else:
                print("\n❌ Enhanced monitoring encountered errors!")
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
        print("🎉 AgentIan ENHANCED workflow completed successfully!")
        print("✨ What we accomplished together:")
        print("   • 🧠 AI-powered project analysis with intelligent clarification questions")
        print("   • 💬 Interactive requirements gathering with your direct input")
        print("   • ✨ Text enhancement and spell checking of all responses")
        print("   • 📊 Intelligent project status reporting")
        print("   • 🔄 Iterative story refinement with human approval")
        print("   • 🎯 Professional user stories with acceptance criteria")
        print("\n🚀 Ready for next phase:")
        print(f"   • 📋 Review stories: {jira_config.base_url}/browse/{jira_config.default_project_key}") 
        print("   • 💬 Check full conversation: Slack channel")
        print("   • 👨‍💻 Hand-off to AgentPete (Developer) for implementation")
        print("   • 🔄 Continue refinement cycles as project evolves")
        print("\n🤖 Your feedback has been incorporated throughout - this is collaborative AI at work!")
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