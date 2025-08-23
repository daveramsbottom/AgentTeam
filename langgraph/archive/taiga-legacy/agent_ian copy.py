"""
AgentIan - Product Owner Agent
Refactored with modular architecture and enhanced Slack integration
"""
import logging
from typing import Dict, Any
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
    
    def process_project_goal(self, project_goal: str, project_id: int) -> Dict[str, Any]:
        """
        Main method to process a project goal through the complete workflow
        
        Args:
            project_goal: The project description/goal to analyze
            project_id: The Taiga project ID to work with
            
        Returns:
            Dict with workflow execution results
        """
        logger.info(f"🎯 Processing project goal: {project_goal}")
        
        return self.workflow_engine.execute_workflow(project_goal, project_id)
    
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
    
    def handle_clarification_request(self, questions: list, project_goal: str) -> str:
        """Handle a clarification request interactively"""
        logger.info("💭 Handling clarification request...")
        
        questions_text = "🤔 **I need clarification on your project:**\n\n"
        for i, question in enumerate(questions, 1):
            questions_text += f"{i}. {question}\n"
        
        questions_text += f"\nOriginal goal: _{project_goal}_"
        questions_text += "\n\nPlease provide detailed answers!"
        
        timestamp = self.slack_client.send_message(questions_text, add_tracking=True)
        
        if timestamp:
            response = self.slack_client.wait_for_response(timestamp, timeout=300)
            if response:
                self.slack_client.send_message("✅ Thanks! Processing your clarification...")
                return response
            else:
                self.slack_client.send_message("⏰ No response received, proceeding with original requirements.")
                return ""
        
        return ""
    
    def get_capabilities_summary(self) -> str:
        """Get a summary of AgentIan's capabilities"""
        return f"""🤖 **{self.name} - {self.role}**

**Capabilities:**
{chr(10).join([f"• {cap}" for cap in self.capabilities])}

**Workflow Steps:**
1. 🔍 Analyze project goals
2. 💭 Ask clarifying questions if needed
3. 📝 Break down into user stories
4. 🎯 Create stories in Taiga
5. 👥 Assign tasks to team members
6. ✅ Provide completion summary

**Integration:**
• 📋 Taiga Project Management
• 💬 Slack Communication
• 🔄 LangGraph Workflow Engine
"""
    
    def __str__(self) -> str:
        return f"AgentIan(role={self.role}, capabilities={len(self.capabilities)})"
    
    def __repr__(self) -> str:
        return f"AgentIan(taiga_url='{self.taiga_client.base_url}', slack_channel='{self.slack_client.channel_id}')"