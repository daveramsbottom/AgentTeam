"""
AgentIan - Product Owner Agent
Enhanced version with FIXED Slack response handling and debugging
"""
import logging
import time
from typing import Dict, Any, Optional
from communication.slack_client import SlackClient
from workflows.workflow_engine import WorkflowEngine
from taiga.client import TaigaClient

logger = logging.getLogger(__name__)


class AgentIan:
    """
    Enhanced AgentIan - Product Owner Agent
    Handles project goal analysis, story breakdown, and team coordination
    """
    
    def __init__(self, taiga_url: str, username: str, password: str, 
                 slack_token: str, slack_channel: str):
        """Initialize AgentIan with all necessary clients"""
        
        # Initialize clients
        self.taiga_client = TaigaClient(taiga_url, username, password)
        self.slack_client = SlackClient(slack_token, slack_channel)
        
        # Initialize workflow engine
        self.workflow_engine = WorkflowEngine(self.taiga_client, self.slack_client)
        
        # Agent metadata
        self.name = "AgentIan"
        self.role = "Product Owner"
        self.capabilities = [
            "Project goal analysis",
            "User story breakdown",
            "Requirements clarification",
            "Task assignment",
            "Taiga project management",
            "Slack communication"
        ]
        
        logger.info(f"🤖 {self.name} initialized successfully")
    
    def authenticate(self) -> bool:
        """Authenticate with all services"""
        logger.info("🔐 Authenticating with services...")
        
        # Test Taiga authentication
        if not self.taiga_client.authenticate():
            logger.error("❌ Taiga authentication failed")
            return False
        
        # Test Slack connection
        slack_test = self.slack_client.test_connection()
        if not slack_test["success"]:
            logger.error(f"❌ Slack connection failed: {slack_test['error']}")
            return False
        
        logger.info("✅ All services authenticated successfully")
        return True
    
    def process_project_goal_with_interaction(self, project_goal: str, project_id: int) -> Dict[str, Any]:
        """
        FIXED: Process a project goal with proper human interaction
        
        Args:
            project_goal: The project description/goal to analyze
            project_id: The Taiga project ID to work with
            
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
                    
                    # Acknowledge the response
                    self.slack_client.send_message(
                        f"✅ **Thank you for the clarification!**\n\n"
                        f"I received: _{response[:150]}{'...' if len(response) > 150 else ''}_\n\n"
                        f"Now processing your requirements and creating user stories...",
                        username=self.name
                    )
                    
                    # Process the response and create stories
                    return self._process_with_clarification(project_goal, project_id, response, clarification_questions)
                    
                else:
                    logger.warning("⚠️ No response received within timeout")
                    self.slack_client.send_message(
                        "⏰ **No response received within 5 minutes.**\n\n"
                        "Proceeding with original requirements. You can always provide more details later!",
                        username=self.name
                    )
                    
                    # Process without clarification
                    return self._process_without_clarification(project_goal, project_id)
            else:
                logger.error("❌ Failed to send clarification request")
                return {"success": False, "error": "Failed to send clarification request"}
        else:
            # No clarification needed
            logger.info("✅ No clarification needed, processing directly")
            return self._process_without_clarification(project_goal, project_id)
    
    def _generate_clarification_questions(self, project_goal: str) -> list:
        """Generate clarification questions based on the project goal"""
        # Simple rule-based question generation for now
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
    
    def _process_with_clarification(self, project_goal: str, project_id: int, 
                                   clarification_response: str, questions: list) -> Dict[str, Any]:
        """Process the project goal with the clarification response"""
        logger.info("🔄 Processing project with clarification response...")
        
        # Create enhanced project description
        enhanced_goal = f"{project_goal}\n\nAdditional Details:\n{clarification_response}"
        
        # Generate user stories based on enhanced requirements
        stories = self._generate_user_stories(enhanced_goal, clarification_response)
        
        # Create stories in Taiga
        created_stories = []
        for story in stories:
            try:
                created_story = self.taiga_client.create_user_story(
                    project_id=project_id,
                    subject=story["title"],
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
        
        completion_message += f"\n✅ All stories have been added to your Taiga project!"
        completion_message += f"\n🔗 Check your project at: http://localhost:9000"
        
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
    
    def _process_without_clarification(self, project_goal: str, project_id: int) -> Dict[str, Any]:
        """Process the project goal without clarification"""
        logger.info("🔄 Processing project without clarification...")
        
        # Generate basic user stories
        stories = self._generate_user_stories(project_goal)
        
        # Create stories in Taiga
        created_stories = []
        for story in stories:
            try:
                created_story = self.taiga_client.create_user_story(
                    project_id=project_id,
                    subject=story["title"],
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
        
        completion_message += f"\n🔗 Check your project at: http://localhost:9000"
        
        self.slack_client.send_message(completion_message, username=self.name)
        
        return {
            "success": True,
            "state": "completed_without_clarification",
            "stories_created": len(created_stories),
            "clarification_needed": False,
            "stories": stories
        }
    
    def _generate_user_stories(self, project_goal: str, clarification: str = "") -> list:
        """Generate user stories based on project goal and optional clarification"""
        # Simple story generation for now - this would be enhanced with LLM integration
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
    def process_project_goal(self, project_goal: str, project_id: int) -> Dict[str, Any]:
        """
        Original method - now redirects to the interactive version
        """
        logger.info("🔄 Redirecting to interactive workflow...")
        return self.process_project_goal_with_interaction(project_goal, project_id)
    
    def debug_slack_integration(self) -> Dict[str, Any]:
        """Debug Slack integration and message detection"""
        logger.info("🔍 Running Slack integration debug...")
        return self.slack_client.debug_message_detection()
    
    def get_project_status(self, project_id: int) -> Dict[str, Any]:
        """Get current project status from Taiga"""
        try:
            project = self.taiga_client.get_project_details(project_id)
            stories = self.taiga_client.get_user_stories(project_id)
            
            if not project:
                return {"error": "Project not found"}
            
            status = {
                "project_name": project.get("name"),
                "project_id": project_id,
                "total_stories": len(stories) if stories else 0,
                "stories": []
            }
            
            if stories:
                for story in stories:
                    status["stories"].append({
                        "id": story.get("id"),
                        "title": story.get("subject"),
                        "status": story.get("status_extra_info", {}).get("name", "Unknown"),
                        "points": story.get("points"),
                        "assigned_to": story.get("assigned_to_extra_info", {}).get("username") if story.get("assigned_to") else None
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
5. 🎯 Create stories in Taiga
6. 👥 Assign tasks to team members
7. ✅ Provide completion summary

**Integration:**
• 📋 Taiga Project Management
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
        return f"AgentIan(taiga_url='{self.taiga_client.base_url}', slack_channel='{self.slack_client.channel_id}')"