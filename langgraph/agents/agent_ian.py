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
        FIXED: Process a project goal with proper human interaction
        
        Args:
            project_goal: The project description/goal to analyze
            
        Returns:
            Dict with workflow execution results including human responses
        """
        logger.info(f"🎯 Processing project goal with human interaction: {project_goal}")
        
        # Step 1: Send initial analysis message
        self.slack_client.send_message(
            f"🎯 **Starting Project Analysis**\n\n"
            f"**Project Goal:** {project_goal}\n\n"
            f"Analyzing requirements and preparing questions...",
            username=self.name
        )
        
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
                    ack_message += f"🤖 Now analyzing your requirements and creating intelligent user stories..."
                    
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
        
        # Create enhanced project description
        enhanced_goal = f"{project_goal}\n\nAdditional Details:\n{clarification_response}"
        
        # Generate user stories based on enhanced requirements
        stories = self._generate_user_stories(enhanced_goal, clarification_response)
        
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
        
        # Send completion message
        completion_message = f"🎉 **Project Analysis Complete!**\n\n"
        completion_message += f"**Created {len(created_stories)} user stories:**\n"
        for i, story in enumerate(stories, 1):
            completion_message += f"{i}. {story['title']}\n"
        
        completion_message += f"\n✅ All stories have been added to your Jira project!"
        completion_message += f"\n🔗 Check your project at: {self.jira_client.base_url}/browse/{self.project_key}"
        
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
        
        # Generate basic user stories
        stories = self._generate_user_stories(project_goal)
        
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
        
        # Send completion message
        completion_message = f"✅ **Project Analysis Complete!**\n\n"
        completion_message += f"**Created {len(created_stories)} user stories:**\n"
        for i, story in enumerate(stories, 1):
            completion_message += f"{i}. {story['title']}\n"
        
        completion_message += f"\n🔗 Check your project at: {self.jira_client.base_url}/browse/{self.project_key}"
        
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
    
    def get_capabilities_summary(self) -> str:
        """Get a summary of AgentIan's capabilities"""
        return f"""🤖 **{self.name} - {self.role}**

**Capabilities:**
{chr(10).join([f"• {cap}" for cap in self.capabilities])}

**Interactive Workflow Steps:**
1. 🔍 Analyze project goals
2. 🤔 Ask clarifying questions and WAIT for responses
3. 💬 Process human feedback
4. 📝 Break down into user stories
5. 🎯 Create stories in Jira
6. 👥 Assign tasks to team members
7. ✅ Provide completion summary

**Integration:**
• 📋 Jira Project Management
• 💬 Slack Communication (with response waiting!)
• 📄 LangGraph Workflow Engine

**New Interactive Features:**
• 🧪 Test interactive workflow
• ⏳ Wait for human responses with timeout
• 💬 Process and acknowledge responses
• 🔍 Enhanced debugging and logging
"""
    
    def __str__(self) -> str:
        return f"AgentIan(role={self.role}, capabilities={len(self.capabilities)})"
    
    def __repr__(self) -> str:
        return f"AgentIan(jira_url='{self.jira_client.base_url}', slack_channel='{self.slack_client.channel_id}', project_key='{self.project_key}')"