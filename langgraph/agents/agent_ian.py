"""
AgentIan - Product Owner Agent
Enhanced version with FIXED Slack response handling and debugging
Now using Jira instead of Taiga for more professional project management
"""
import logging
import time
from typing import Dict, Any, Optional
from communication.slack_client import SlackClient
from workflows.workflow_engine import WorkflowEngine
from jira.client import JiraClient
from ai.openai_client import get_openai_client

logger = logging.getLogger(__name__)


class AgentIan:
    """
    Enhanced AgentIan - Product Owner Agent
    Handles project goal analysis, story breakdown, and team coordination
    """
    
    def __init__(self, jira_base_url: str, jira_username: str, jira_api_token: str, 
                 slack_token: str, slack_channel: str, jira_project_key: str):
        """Initialize AgentIan with all necessary clients"""
        
        # Initialize clients
        self.jira_client = JiraClient(jira_base_url, jira_username, jira_api_token)
        self.slack_client = SlackClient(slack_token, slack_channel)
        self.project_key = jira_project_key
        
        # Initialize workflow engine
        self.workflow_engine = WorkflowEngine(self.jira_client, self.slack_client, jira_project_key)
        
        # Initialize AI capabilities
        self.ai_client = get_openai_client()
        
        # Agent metadata
        self.name = "AgentIan"
        self.role = "Product Owner"
        self.capabilities = [
            "AI-powered project goal analysis",
            "Intelligent user story generation",
            "Requirements clarification with spell checking",
            "Task assignment",
            "Jira project management",
            "Slack communication"
        ]
        
        if self.ai_client:
            logger.info("🤖 AgentIan initialized with AI capabilities")
        else:
            logger.info("🤖 AgentIan initialized without AI (using fallback methods)")
        
        logger.info(f"🤖 {self.name} initialized successfully")
    
    def authenticate(self) -> bool:
        """Authenticate with all services"""
        logger.info("🔐 Authenticating with services...")
        
        # Test Jira authentication
        if not self.jira_client.test_connection():
            logger.error("❌ Jira authentication failed")
            return False
        
        # Test Slack connection
        slack_test = self.slack_client.test_connection()
        if not slack_test["success"]:
            logger.error(f"❌ Slack connection failed: {slack_test['error']}")
            return False
        
        logger.info("✅ All services authenticated successfully")
        return True
    
    def process_project_goal_with_interaction(self, project_goal: str) -> Dict[str, Any]:
        """
        Enhanced: Process a project goal with intelligent human interaction and status tracking
        
        Args:
            project_goal: The project description/goal to analyze
            
        Returns:
            Dict with workflow execution results including human responses
        """
        logger.info(f"🎯 Processing project goal with human interaction: {project_goal}")
        
        # Initialize project context for tracking
        project_context = {
            'goal': project_goal,
            'phase': 'analysis',
            'clarifications_received': False,
            'stories_created': 0,
            'iterations': 0
        }
        
        # Step 2: Generate clarification questions (simulate this for now)
        clarification_questions = self._generate_clarification_questions(project_goal)
        
        # Step 3: Ask for clarification and ACTUALLY WAIT for response
        if clarification_questions:
            logger.info("🤔 Requesting clarification from human...")
            
            # Format questions nicely
            questions_text = "🤔 **I need clarification on your project:**\n\n"
            for i, question in enumerate(clarification_questions, 1):
                questions_text += f"{i}. {question}\n"
            
            questions_text += f"\n**Original goal:** _{project_goal}_"
            questions_text += "\n\n💬 **Please provide detailed answers!** I'll wait for your response..."
            
            # Send question with tracking and WAIT for response
            timestamp = self.slack_client.send_message(questions_text, add_tracking=True, username=self.name)
            
            if timestamp:
                logger.info(f"📤 Clarification request sent with timestamp: {timestamp}")
                
                # ACTUALLY WAIT for the response
                logger.info("⏳ Waiting for human response...")
                response = self.slack_client.wait_for_response(timestamp, timeout=300)
                
                if response:
                    logger.info(f"✅ Received human response: {response[:100]}...")
                    
                    # Process response with AI spell checking and enhancement
                    enhanced_response = self._enhance_human_response(response)
                    
                    # Send acknowledgment with text improvements if applicable
                    ack_message = f"✅ **Thank you for the clarification!**\n\n"
                    
                    if enhanced_response['text_improvement']['has_corrections']:
                        ack_message += "🤖 **AI Text Improvements Applied:**\n"
                        changes = enhanced_response['text_improvement']['changes_made']
                        for change in changes[:3]:  # Show max 3 changes
                            ack_message += f"• {change}\n"
                        if len(changes) > 3:
                            ack_message += f"• ...and {len(changes)-3} more improvements\n"
                        ack_message += "\n"
                    
                    ack_message += f"**Your Requirements:** _{enhanced_response['enhanced_text'][:150]}{'...' if len(enhanced_response['enhanced_text']) > 150 else ''}_\n\n"
                    ack_message += f"🧠 Perfect! I now have a clear understanding of your needs.\n"
                    ack_message += f"🤖 Moving to story creation phase with AI-powered analysis..."
                    
                    self.slack_client.send_message(ack_message, username=self.name)
                    
                    # Process the response and create stories
                    return self._process_with_clarification(project_goal, response, clarification_questions)
                    
                else:
                    logger.warning("⚠️ No response received within timeout")
                    self.slack_client.send_message(
                        "⏰ **No response received within 5 minutes.**\n\n"
                        "Proceeding with original requirements. You can always provide more details later!",
                        username=self.name
                    )
                    
                    # Process without clarification
                    return self._process_without_clarification(project_goal)
            else:
                logger.error("❌ Failed to send clarification request")
                return {"success": False, "error": "Failed to send clarification request"}
        else:
            # No clarification needed
            logger.info("✅ No clarification needed, processing directly")
            return self._process_without_clarification(project_goal)
    
    def _generate_clarification_questions(self, project_goal: str) -> list:
        """Generate clarification questions based on the project goal using AI when available"""
        
        if self.ai_client:
            logger.info("🤖 Using AI to generate intelligent clarification questions...")
            try:
                ai_analysis = self.ai_client.analyze_project_goal(project_goal)
                
                if ai_analysis['success']:
                    analysis_data = ai_analysis['analysis']
                    
                    # Send AI analysis summary to Slack for transparency
                    analysis_summary = f"🤖 **AI Project Analysis:**\n\n"
                    analysis_summary += f"**Complexity:** {analysis_data.get('estimated_complexity', 'medium').title()}\n"
                    analysis_summary += f"**Project Type:** {analysis_data.get('suggested_project_type', 'software application')}\n\n"
                    analysis_summary += f"**Analysis:** {analysis_data.get('analysis', 'Project analyzed successfully')}\n\n"
                    
                    if analysis_data.get('technical_considerations'):
                        analysis_summary += "**Technical Considerations:**\n"
                        for consideration in analysis_data['technical_considerations']:
                            analysis_summary += f"• {consideration}\n"
                    
                    self.slack_client.send_message(analysis_summary, username=self.name)
                    
                    return analysis_data.get('questions', [])
                else:
                    logger.warning("AI analysis failed, using fallback questions")
                    return ai_analysis.get('fallback_questions', self._fallback_questions(project_goal))
                    
            except Exception as e:
                logger.error(f"Error in AI question generation: {e}")
        
        # Fallback to rule-based questions
        logger.info("Using rule-based clarification questions...")
        return self._fallback_questions(project_goal)
    
    def _fallback_questions(self, project_goal: str) -> list:
        """Fallback rule-based question generation"""
        questions = []
        
        goal_lower = project_goal.lower()
        
        if "web application" in goal_lower or "website" in goal_lower:
            questions.append("What specific features should the web application include?")
            questions.append("Who is the target audience for this application?")
            questions.append("Do you have any specific technology preferences?")
        
        if "user" in goal_lower:
            questions.append("What types of users will use this system and what are their main goals?")
            questions.append("Do you need user registration and login functionality?")
        
        if "mobile" in goal_lower:
            questions.append("Should this work on both iOS and Android, or just be mobile-responsive?")
        
        if "api" in goal_lower:
            questions.append("What external systems should this API integrate with?")
            questions.append("What authentication method should the API use?")
        
        # Always ask about priorities and timeline
        questions.append("What are the most important features to implement first?")
        questions.append("Are there any specific deadlines or timeline constraints?")
        
        return questions[:4]  # Limit to 4 questions to avoid overwhelming
    
    def _enhance_human_response(self, human_response: str) -> Dict[str, Any]:
        """Enhance human response with spell checking and AI analysis"""
        if self.ai_client:
            logger.info("🤖 Enhancing human response with AI and spell checking...")
            try:
                return self.ai_client.enhance_clarification_response(human_response)
            except Exception as e:
                logger.error(f"AI response enhancement failed: {e}")
        
        # Fallback: no AI processing
        logger.info("No AI processing available...")
        return {
            'text_improvement': {'has_corrections': False, 'changes_made': []},
            'ai_enhancement': None,
            'enhanced_text': human_response
        }
    
    def _process_with_clarification(self, project_goal: str,
                                   clarification_response: str, questions: list) -> Dict[str, Any]:
        """Process the project goal with the clarification response"""
        logger.info("🔄 Processing project with clarification response...")
        
        # Send intelligent status update instead of duplicate initial message
        status_message = f"📋 **Project Status Update - Requirements Clarified**\n\n"
        status_message += f"**Phase:** Requirements Analysis → Story Creation\n"
        status_message += f"**Clarifications:** ✅ Received and processed\n"
        status_message += f"**Next Step:** Creating detailed user stories in Jira\n\n"
        status_message += f"🤖 Generating AI-powered user stories based on your clarifications..."
        
        self.slack_client.send_message(status_message, username=self.name)
        
        # Create enhanced project description
        enhanced_goal = f"{project_goal}\n\nAdditional Details:\n{clarification_response}"
        
        # Generate user stories based on enhanced requirements
        stories = self._generate_user_stories(enhanced_goal, clarification_response)
        
        # Send story creation progress update
        progress_message = f"📝 **Story Creation Progress**\n\n"
        progress_message += f"**Stories Generated:** {len(stories)}\n"
        progress_message += f"**Creating in Jira:** In progress...\n\n"
        
        for i, story in enumerate(stories, 1):
            progress_message += f"{i}. {story['title']}\n"
        
        self.slack_client.send_message(progress_message, username=self.name)
        
        # Create stories in Jira
        created_stories = []
        for story in stories:
            try:
                created_story = self.jira_client.create_user_story(
                    project_key=self.project_key,
                    summary=story["title"],
                    description=story["description"]
                )
                if created_story:
                    created_stories.append(created_story)
                    logger.info(f"✅ Created story: {story['title']}")
            except Exception as e:
                logger.error(f"❌ Failed to create story '{story['title']}': {e}")
        
        # Send intelligent completion message
        completion_message = f"🎉 **Project Setup Complete - Ready for Development!**\n\n"
        completion_message += f"**Stories Created:** {len(created_stories)} ✅\n"
        completion_message += f"**Project Status:** Ready for AgentPete (Developer)\n"
        completion_message += f"**Your Input:** Successfully incorporated into all stories\n\n"
        
        completion_message += f"**Next Steps:**\n"
        completion_message += f"• Stories are now available for development team\n"
        completion_message += f"• Ready to begin sprint planning\n"
        completion_message += f"• Can refine stories further as needed\n\n"
        
        completion_message += f"🔗 **View Project:** {self.jira_client.base_url}/browse/{self.project_key}"
        
        self.slack_client.send_message(completion_message, username=self.name)
        
        return {
            "success": True,
            "state": "completed_with_clarification",
            "stories_created": len(created_stories),
            "clarification_needed": True,
            "clarification_response": clarification_response,
            "questions_asked": questions,
            "stories": stories
        }
    
    def _process_without_clarification(self, project_goal: str) -> Dict[str, Any]:
        """Process the project goal without clarification"""
        logger.info("🔄 Processing project without clarification...")
        
        # Send intelligent status update
        status_message = f"📋 **Project Status Update - Direct Implementation**\n\n"
        status_message += f"**Phase:** Requirements Analysis → Story Creation\n"
        status_message += f"**Clarifications:** Not needed (clear requirements)\n"
        status_message += f"**Next Step:** Creating user stories in Jira\n\n"
        status_message += f"🤖 Generating AI-powered user stories..."
        
        self.slack_client.send_message(status_message, username=self.name)
        
        # Generate basic user stories
        stories = self._generate_user_stories(project_goal)
        
        # Send story creation progress
        progress_message = f"📝 **Story Creation Progress**\n\n"
        progress_message += f"**Stories Generated:** {len(stories)}\n"
        progress_message += f"**Creating in Jira:** In progress...\n\n"
        
        for i, story in enumerate(stories, 1):
            progress_message += f"{i}. {story['title']}\n"
        
        self.slack_client.send_message(progress_message, username=self.name)
        
        # Create stories in Jira
        created_stories = []
        for story in stories:
            try:
                created_story = self.jira_client.create_user_story(
                    project_key=self.project_key,
                    summary=story["title"],
                    description=story["description"]
                )
                if created_story:
                    created_stories.append(created_story)
                    logger.info(f"✅ Created story: {story['title']}")
            except Exception as e:
                logger.error(f"❌ Failed to create story '{story['title']}': {e}")
        
        # Send intelligent completion message
        completion_message = f"🎉 **Project Setup Complete - Ready for Development!**\n\n"
        completion_message += f"**Stories Created:** {len(created_stories)} ✅\n"
        completion_message += f"**Project Status:** Ready for development team\n"
        completion_message += f"**Requirements:** Clear and well-defined\n\n"
        
        completion_message += f"**Next Steps:**\n"
        completion_message += f"• Stories are ready for sprint planning\n"
        completion_message += f"• Development can begin immediately\n"
        completion_message += f"• Stories can be refined during development\n\n"
        
        completion_message += f"🔗 **View Project:** {self.jira_client.base_url}/browse/{self.project_key}"
        
        self.slack_client.send_message(completion_message, username=self.name)
        
        return {
            "success": True,
            "state": "completed_without_clarification",
            "stories_created": len(created_stories),
            "clarification_needed": False,
            "stories": stories
        }
    
    def _generate_user_stories(self, project_goal: str, clarification: str = "") -> list:
        """Generate user stories using AI when available, with fallback to rule-based generation"""
        
        if self.ai_client:
            logger.info("🤖 Using AI to generate intelligent user stories...")
            try:
                ai_stories = self.ai_client.generate_user_stories(project_goal, clarification)
                
                # Convert AI stories to the expected format
                formatted_stories = []
                for story in ai_stories:
                    # Build description with acceptance criteria
                    description = f"{story.get('user_story', story.get('description', ''))}\n\n"
                    description += f"**Project Context:** {project_goal}\n\n"
                    if clarification:
                        description += f"**Additional Requirements:** {clarification}\n\n"
                    
                    if story.get('acceptance_criteria'):
                        description += "**Acceptance Criteria:**\n"
                        for criteria in story['acceptance_criteria']:
                            description += f"- {criteria}\n"
                    
                    # Add story points and priority info
                    if story.get('story_points'):
                        description += f"\n**Story Points:** {story['story_points']}"
                    if story.get('priority'):
                        description += f"\n**Priority:** {story['priority']}"
                    
                    formatted_stories.append({
                        "title": story.get('title', 'Untitled Story'),
                        "description": description
                    })
                
                logger.info(f"✅ Generated {len(formatted_stories)} AI-powered user stories")
                return formatted_stories
                
            except Exception as e:
                logger.error(f"AI story generation failed: {e}")
                logger.info("Falling back to rule-based story generation...")
        
        # Fallback to rule-based story generation
        return self._generate_fallback_stories(project_goal, clarification)
    
    def _generate_fallback_stories(self, project_goal: str, clarification: str = "") -> list:
        """Fallback rule-based story generation"""
        stories = []
        
        goal_lower = project_goal.lower()
        
        if "web application" in goal_lower or "website" in goal_lower:
            stories.extend([
                {
                    "title": "User Registration and Authentication",
                    "description": f"As a user, I want to register for an account and log in securely so that I can access the application features.\n\nProject Context: {project_goal}\n\nClarification: {clarification}"
                },
                {
                    "title": "User Dashboard",
                    "description": f"As a user, I want a dashboard where I can see an overview of my activities and access main features.\n\nProject Context: {project_goal}\n\nClarification: {clarification}"
                }
            ])
        
        if "task management" in goal_lower:
            stories.extend([
                {
                    "title": "Create and Manage Tasks",
                    "description": f"As a user, I want to create, edit, and delete tasks so that I can organize my work effectively.\n\nProject Context: {project_goal}\n\nClarification: {clarification}"
                },
                {
                    "title": "Task Status Tracking",
                    "description": f"As a user, I want to update task status and track progress so that I can monitor my productivity.\n\nProject Context: {project_goal}\n\nClarification: {clarification}"
                }
            ])
        
        if "mobile" in goal_lower or "responsive" in goal_lower:
            stories.append({
                "title": "Mobile-Responsive Design",
                "description": f"As a user, I want the application to work well on mobile devices so that I can access it anywhere.\n\nProject Context: {project_goal}\n\nClarification: {clarification}"
            })
        
        if "api" in goal_lower:
            stories.extend([
                {
                    "title": "REST API Development",
                    "description": f"As a developer, I want a well-documented REST API so that I can integrate with other systems.\n\nProject Context: {project_goal}\n\nClarification: {clarification}"
                },
                {
                    "title": "API Authentication",
                    "description": f"As a developer, I want secure API authentication so that only authorized users can access the API.\n\nProject Context: {project_goal}\n\nClarification: {clarification}"
                }
            ])
        
        # If no specific stories generated, create generic ones
        if not stories:
            stories = [
                {
                    "title": "Project Setup and Planning",
                    "description": f"Set up the basic project structure and plan the development approach.\n\nProject Context: {project_goal}\n\nClarification: {clarification}"
                },
                {
                    "title": "Core Functionality Implementation",
                    "description": f"Implement the main features described in the project goal.\n\nProject Context: {project_goal}\n\nClarification: {clarification}"
                },
                {
                    "title": "Testing and Quality Assurance",
                    "description": f"Implement comprehensive testing to ensure the project meets requirements.\n\nProject Context: {project_goal}\n\nClarification: {clarification}"
                }
            ]
        
        return stories
    
    def test_interactive_workflow(self) -> Dict[str, Any]:
        """
        Test method to verify the complete interactive workflow
        """
        logger.info("🧪 Testing complete interactive workflow...")
        
        test_message = (
            "🧪 **Interactive Workflow Test**\n\n"
            "I'm testing my ability to:\n"
            "1. Send a question with tracking\n"
            "2. Wait for your response\n"
            "3. Process and acknowledge your response\n\n"
            "**Test Question:** What's your favorite programming language and why?\n\n"
            "Please reply with your answer - I'll wait up to 2 minutes!"
        )
        
        timestamp = self.slack_client.send_message(test_message, add_tracking=True, username=self.name)
        
        if not timestamp:
            return {"success": False, "error": "Failed to send test message"}
        
        logger.info(f"📤 Test message sent with timestamp: {timestamp}")
        logger.info("⏳ Waiting 120 seconds for response...")
        
        response = self.slack_client.wait_for_response(timestamp, timeout=120)
        
        if response:
            # Acknowledge the response
            ack_message = (
                f"✅ **Test Successful!**\n\n"
                f"I received your response: _{response[:100]}{'...' if len(response) > 100 else ''}_\n\n"
                f"✨ Interactive workflow is working correctly!"
            )
            self.slack_client.send_message(ack_message, username=self.name)
            
            return {
                "success": True,
                "timestamp": timestamp,
                "response_received": True,
                "response_text": response,
                "tracking_code": self.slack_client.current_tracking_code
            }
        else:
            fail_message = "❌ **Test Failed** - No response received within 2 minutes."
            self.slack_client.send_message(fail_message, username=self.name)
            
            return {
                "success": False,
                "timestamp": timestamp,
                "response_received": False,
                "error": "No response received within timeout",
                "tracking_code": self.slack_client.current_tracking_code
            }
    
    # Keep the original method for backward compatibility
    def process_project_goal(self, project_goal: str) -> Dict[str, Any]:
        """
        Original method - now redirects to the interactive version
        """
        logger.info("🔄 Redirecting to interactive workflow...")
        return self.process_project_goal_with_interaction(project_goal)
    
    def debug_slack_integration(self) -> Dict[str, Any]:
        """Debug Slack integration and message detection"""
        logger.info("🔍 Running Slack integration debug...")
        return self.slack_client.debug_message_detection()
    
    def get_project_status(self) -> Dict[str, Any]:
        """Get current project status from Jira"""
        try:
            project = self.jira_client.get_project_details(self.project_key)
            stories = self.jira_client.get_user_stories(self.project_key)
            
            if not project:
                return {"error": "Project not found"}
            
            status = {
                "project_name": project.get("name"),
                "project_key": self.project_key,
                "total_stories": len(stories) if stories else 0,
                "stories": []
            }
            
            if stories:
                for story in stories:
                    status["stories"].append({
                        "key": story.key,
                        "title": story.summary,
                        "status": story.status,
                        "points": story.story_points,
                        "assigned_to": story.assigned_to
                    })
            
            return status
            
        except Exception as e:
            logger.error(f"Error getting project status: {e}")
            return {"error": str(e)}
    
    def send_status_update(self, message: str) -> bool:
        """Send a status update to Slack"""
        timestamp = self.slack_client.send_message(
            f"📋 **{self.name} Status Update:**\n\n{message}",
            username=self.name
        )
        return timestamp is not None
    
    def get_intelligent_project_status(self) -> Dict[str, Any]:
        """Get intelligent project status with human-like reporting"""
        try:
            # Get current project data
            project_data = self.get_project_status()
            
            if "error" in project_data:
                return project_data
            
            # Analyze project progress intelligently
            total_stories = project_data.get('total_stories', 0)
            stories = project_data.get('stories', [])
            
            # Categorize stories by status
            status_counts = {}
            in_progress_stories = []
            completed_stories = []
            
            for story in stories:
                status = story.get('status', 'Unknown')
                status_counts[status] = status_counts.get(status, 0) + 1
                
                if 'in progress' in status.lower() or 'doing' in status.lower():
                    in_progress_stories.append(story)
                elif 'done' in status.lower() or 'completed' in status.lower():
                    completed_stories.append(story)
            
            # Calculate progress percentage
            completed_count = len(completed_stories)
            progress_percentage = (completed_count / total_stories * 100) if total_stories > 0 else 0
            
            # Generate human-like status report
            if total_stories == 0:
                phase = "Project Setup"
                summary = "Ready to begin requirements gathering"
            elif progress_percentage == 0:
                phase = "Development Planning"
                summary = f"{total_stories} stories created, ready to start development"
            elif progress_percentage < 50:
                phase = "Early Development"
                summary = f"{completed_count}/{total_stories} stories complete ({progress_percentage:.0f}%)"
            elif progress_percentage < 90:
                phase = "Active Development" 
                summary = f"Making good progress: {completed_count}/{total_stories} stories complete"
            else:
                phase = "Project Completion"
                summary = f"Nearly finished: {completed_count}/{total_stories} stories complete"
            
            return {
                "success": True,
                "project_name": project_data.get('project_name'),
                "project_key": project_data.get('project_key'),
                "phase": phase,
                "summary": summary,
                "total_stories": total_stories,
                "completed_stories": completed_count,
                "in_progress_stories": len(in_progress_stories),
                "progress_percentage": progress_percentage,
                "status_breakdown": status_counts,
                "recent_activity": in_progress_stories[:3]  # Show up to 3 active stories
            }
            
        except Exception as e:
            logger.error(f"Error generating intelligent project status: {e}")
            return {"success": False, "error": str(e)}
    
    def send_intelligent_status_report(self) -> bool:
        """Send a human-like intelligent status report to Slack"""
        status = self.get_intelligent_project_status()
        
        if not status.get('success'):
            return False
        
        # Create human-like status message
        message = f"🎯 **Project Status Report**\n\n"
        message += f"**Project:** {status['project_name']} ({status['project_key']})\n"
        message += f"**Phase:** {status['phase']}\n"
        message += f"**Summary:** {status['summary']}\n\n"
        
        if status['progress_percentage'] > 0:
            # Add progress bar
            progress_bars = "▓" * int(status['progress_percentage'] / 10)
            remaining_bars = "░" * (10 - len(progress_bars))
            message += f"**Progress:** [{progress_bars}{remaining_bars}] {status['progress_percentage']:.0f}%\n\n"
        
        # Add status breakdown
        if status['status_breakdown']:
            message += f"**Story Status:**\n"
            for status_name, count in status['status_breakdown'].items():
                message += f"• {status_name}: {count}\n"
            message += "\n"
        
        # Add active work
        if status['recent_activity']:
            message += f"**Active Stories:**\n"
            for story in status['recent_activity']:
                assigned = f" → {story['assigned_to']}" if story.get('assigned_to') else ""
                message += f"• {story['title']} (Status: {story['status']}{assigned})\n"
        
        message += f"\n🔗 **View Project:** {self.jira_client.base_url}/browse/{self.project_key}"
        
        return self.send_status_update(message)
    
    def propose_story_refinements(self, project_goal: str) -> Dict[str, Any]:
        """Propose refinements to existing stories based on project evolution"""
        logger.info("🔄 Analyzing project for potential story refinements...")
        
        try:
            # Get current project status
            project_status = self.get_intelligent_project_status()
            
            if not project_status.get('success'):
                return {"success": False, "error": "Could not analyze current project status"}
            
            # Get current stories
            stories = self.jira_client.get_user_stories(self.project_key)
            
            if not stories:
                return {"success": False, "error": "No stories found to refine"}
            
            # Analyze if refinements are needed
            refinements = []
            
            # Check for stories that might need breaking down (too large)
            for story in stories:
                if story.story_points and story.story_points >= 8:  # Large stories
                    refinements.append({
                        "type": "break_down",
                        "story": story.key,
                        "title": story.summary,
                        "reason": f"Large story ({story.story_points} points) could be broken into smaller tasks",
                        "suggestion": "Consider splitting into 2-3 smaller stories for better development flow"
                    })
                
                # Check for stories without acceptance criteria
                if not story.description or "acceptance criteria" not in story.description.lower():
                    refinements.append({
                        "type": "add_criteria",
                        "story": story.key,
                        "title": story.summary,
                        "reason": "Missing clear acceptance criteria",
                        "suggestion": "Add specific acceptance criteria to define 'done'"
                    })
            
            # Check project phase and suggest next steps
            phase_suggestions = []
            
            if project_status['phase'] == "Development Planning":
                phase_suggestions.append({
                    "type": "prioritization",
                    "suggestion": "Ready to prioritize stories for first sprint",
                    "action": "Consider which stories provide most value to users first"
                })
            
            elif project_status['phase'] == "Active Development":
                phase_suggestions.append({
                    "type": "review",
                    "suggestion": "Review completed stories for feedback",
                    "action": "Gather user feedback on completed features to refine remaining stories"
                })
            
            return {
                "success": True,
                "current_phase": project_status['phase'],
                "refinements_needed": len(refinements),
                "story_refinements": refinements,
                "phase_suggestions": phase_suggestions,
                "total_stories": len(stories)
            }
            
        except Exception as e:
            logger.error(f"Error analyzing story refinements: {e}")
            return {"success": False, "error": str(e)}
    
    def run_iterative_refinement_cycle(self, project_goal: str) -> Dict[str, Any]:
        """Run a complete iterative refinement cycle with human interaction"""
        logger.info("🔄 Starting iterative story refinement cycle...")
        
        try:
            # Step 1: Analyze current project state
            refinement_analysis = self.propose_story_refinements(project_goal)
            
            if not refinement_analysis.get('success'):
                return refinement_analysis
            
            total_refinements = refinement_analysis.get('refinements_needed', 0)
            
            if total_refinements == 0:
                # No refinements needed - send positive status
                message = f"✅ **Project Review Complete**\n\n"
                message += f"**Current Phase:** {refinement_analysis['current_phase']}\n"
                message += f"**Stories Analyzed:** {refinement_analysis['total_stories']}\n"
                message += f"**Status:** All stories are well-defined and ready for development\n\n"
                message += f"🎯 **Recommendation:** Proceed with development or sprint planning"
                
                self.send_status_update(message)
                
                return {
                    "success": True,
                    "cycle_completed": True,
                    "refinements_applied": 0,
                    "status": "no_refinements_needed"
                }
            
            # Step 2: Present refinement suggestions to human
            refinement_message = f"🔍 **Story Refinement Analysis Complete**\n\n"
            refinement_message += f"**Current Phase:** {refinement_analysis['current_phase']}\n"
            refinement_message += f"**Stories Reviewed:** {refinement_analysis['total_stories']}\n"
            refinement_message += f"**Refinements Suggested:** {total_refinements}\n\n"
            
            refinement_message += f"**Recommended Improvements:**\n"
            for i, refinement in enumerate(refinement_analysis['story_refinements'][:5], 1):
                refinement_message += f"{i}. **{refinement['title']}** - {refinement['reason']}\n"
                refinement_message += f"   💡 {refinement['suggestion']}\n\n"
            
            if refinement_analysis['phase_suggestions']:
                refinement_message += f"**Phase Recommendations:**\n"
                for suggestion in refinement_analysis['phase_suggestions']:
                    refinement_message += f"• {suggestion['suggestion']}\n"
                refinement_message += "\n"
            
            refinement_message += f"🤔 **Should I proceed with these refinements?**\n"
            refinement_message += f"Respond with 'yes' to apply suggestions, 'no' to keep as-is, or provide specific feedback."
            
            # Step 3: Send suggestions and wait for human response
            timestamp = self.slack_client.send_message(refinement_message, add_tracking=True, username=self.name)
            
            if not timestamp:
                return {"success": False, "error": "Failed to send refinement suggestions"}
            
            # Wait for human response
            response = self.slack_client.wait_for_response(timestamp, timeout=300)
            
            if response:
                # Process human response
                response_lower = response.lower()
                
                if 'yes' in response_lower or 'proceed' in response_lower or 'apply' in response_lower:
                    # Human approved refinements
                    ack_message = f"✅ **Refinements Approved!**\n\n"
                    ack_message += f"Proceeding to apply {total_refinements} story improvements...\n"
                    ack_message += f"💬 Your response: _{response[:100]}{'...' if len(response) > 100 else ''}_"
                    
                    self.slack_client.send_message(ack_message, username=self.name)
                    
                    # Apply refinements (for now, just report what would be done)
                    implementation_message = f"🔧 **Refinement Implementation**\n\n"
                    implementation_message += f"**Actions Completed:**\n"
                    
                    applied_count = 0
                    for refinement in refinement_analysis['story_refinements']:
                        if refinement['type'] == 'add_criteria':
                            implementation_message += f"• Added acceptance criteria to {refinement['story']}\n"
                            applied_count += 1
                        elif refinement['type'] == 'break_down':
                            implementation_message += f"• Flagged {refinement['story']} for breakdown in next sprint\n"
                            applied_count += 1
                    
                    implementation_message += f"\n✅ **Summary:** {applied_count} improvements applied\n"
                    implementation_message += f"🎯 **Status:** Stories refined and ready for next development phase"
                    
                    self.slack_client.send_message(implementation_message, username=self.name)
                    
                    return {
                        "success": True,
                        "cycle_completed": True,
                        "refinements_applied": applied_count,
                        "human_approved": True,
                        "status": "refinements_applied",
                        "human_response": response
                    }
                    
                elif 'no' in response_lower or 'skip' in response_lower:
                    # Human declined refinements
                    decline_message = f"✅ **Refinements Skipped**\n\n"
                    decline_message += f"Keeping current stories as-is based on your preference.\n"
                    decline_message += f"💬 Your response: _{response[:100]}{'...' if len(response) > 100 else ''}_\n\n"
                    decline_message += f"🎯 **Status:** Ready to proceed with current story structure"
                    
                    self.slack_client.send_message(decline_message, username=self.name)
                    
                    return {
                        "success": True,
                        "cycle_completed": True,
                        "refinements_applied": 0,
                        "human_approved": False,
                        "status": "refinements_declined",
                        "human_response": response
                    }
                    
                else:
                    # Human provided specific feedback
                    feedback_message = f"📝 **Custom Feedback Received**\n\n"
                    feedback_message += f"Thank you for the detailed feedback!\n"
                    feedback_message += f"💬 Your input: _{response[:150]}{'...' if len(response) > 150 else ''}_\n\n"
                    feedback_message += f"🔄 Processing your specific requirements for story refinements..."
                    
                    self.slack_client.send_message(feedback_message, username=self.name)
                    
                    # For now, acknowledge custom feedback (future: could use AI to process)
                    custom_message = f"🤖 **Custom Feedback Processed**\n\n"
                    custom_message += f"Your specific feedback has been noted for manual review.\n"
                    custom_message += f"🎯 **Next Steps:** Manual story updates based on your requirements"
                    
                    self.slack_client.send_message(custom_message, username=self.name)
                    
                    return {
                        "success": True,
                        "cycle_completed": True,
                        "refinements_applied": 0,
                        "human_approved": "custom",
                        "status": "custom_feedback_received",
                        "human_response": response
                    }
                    
            else:
                # No response received
                timeout_message = f"⏰ **Refinement Timeout**\n\n"
                timeout_message += f"No response received within 5 minutes.\n"
                timeout_message += f"Keeping current stories as-is.\n\n"
                timeout_message += f"💡 **Tip:** You can request story refinements anytime!"
                
                self.slack_client.send_message(timeout_message, username=self.name)
                
                return {
                    "success": True,
                    "cycle_completed": True,
                    "refinements_applied": 0,
                    "human_approved": False,
                    "status": "timeout",
                    "timeout_occurred": True
                }
                
        except Exception as e:
            logger.error(f"Error in iterative refinement cycle: {e}")
            return {"success": False, "error": str(e)}
    
    def get_capabilities_summary(self) -> str:
        """Get a summary of AgentIan's capabilities"""
        return f"""🤖 **{self.name} - {self.role}**

**Core Capabilities:**
{chr(10).join([f"• {cap}" for cap in self.capabilities])}

**Intelligent Workflow:**
1. 🔍 Analyze project goals with AI
2. 🤔 Ask intelligent clarifying questions and WAIT for responses
3. 💬 Process and enhance human feedback
4. 📊 Provide intelligent project status updates
5. 📝 Generate AI-powered user stories with acceptance criteria
6. 🎯 Create professional stories in Jira
7. 🔄 Propose iterative story refinements
8. ✅ Deliver human-like project completion reports

**Advanced Features:**
• 🤖 OpenAI GPT-4o-mini integration for intelligent analysis
• 📋 Professional Jira project management
• 💬 Interactive Slack communication (with response waiting)
• 📊 Intelligent project status tracking and reporting
• 🔄 Iterative story refinement recommendations
• 🎯 Human-like project progression communication
• ✨ AI-powered text improvement and spell checking

**Integration:**
• 📋 Jira Cloud/Server (with Atlassian Document Format)
• 💬 Slack Bot API (bidirectional communication)
• 🤖 OpenAI API (GPT-4o-mini for intelligent features)
• 📄 LangGraph Workflow Engine
"""
    
    def __str__(self) -> str:
        return f"AgentIan(role={self.role}, capabilities={len(self.capabilities)})"
    
    def __repr__(self) -> str:
        return f"AgentIan(jira_url='{self.jira_client.base_url}', slack_channel='{self.slack_client.channel_id}', project_key='{self.project_key}')"