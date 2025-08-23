"""
LangGraph Workflow Engine for AgentTeam
Handles the main workflow orchestration for AgentIan
Now using Jira instead of Taiga for project management
"""
import logging
from typing import Dict, Any
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages

from .states import WorkflowState, AgentIanState, DEFAULT_TEAM_MEMBERS
from .story_breakdown import StoryBreakdownEngine

logger = logging.getLogger(__name__)


class WorkflowEngine:
    """LangGraph workflow engine for AgentIan"""
    
    def __init__(self, jira_client, slack_client, project_key: str = None):
        self.jira_client = jira_client
        self.slack_client = slack_client
        self.project_key = project_key
        self.story_engine = StoryBreakdownEngine()
        self.workflow = self._build_workflow()
    
    def _build_workflow(self) -> StateGraph:
        """Build the LangGraph workflow"""
        workflow = StateGraph(AgentIanState)
        
        # Add nodes for each workflow step
        workflow.add_node("start", self._start_analysis)
        workflow.add_node("analyze_goal", self._analyze_goal)
        workflow.add_node("break_down_stories", self._break_down_stories)
        workflow.add_node("create_stories_in_jira", self._create_stories_in_jira)
        workflow.add_node("assign_tasks", self._assign_tasks)
        workflow.add_node("seek_clarification", self._seek_clarification)
        workflow.add_node("process_clarification", self._process_clarification)
        workflow.add_node("complete", self._complete_workflow)
        
        # Define workflow edges
        workflow.set_entry_point("start")
        workflow.add_edge("start", "analyze_goal")
        
        workflow.add_conditional_edges(
            "analyze_goal",
            self._should_seek_clarification,
            {
                "clarification": "seek_clarification",
                "continue": "break_down_stories"
            }
        )
        
        workflow.add_edge("seek_clarification", "process_clarification")
        workflow.add_edge("process_clarification", "break_down_stories")
        workflow.add_edge("break_down_stories", "create_stories_in_jira")
        workflow.add_edge("create_stories_in_jira", "assign_tasks")
        workflow.add_edge("assign_tasks", "complete")
        workflow.add_edge("complete", END)
        
        return workflow.compile()
    
    def _start_analysis(self, state: AgentIanState) -> AgentIanState:
        """Initialize the workflow"""
        logger.info(f"🚀 AgentIan starting analysis of project goal: {state['project_goal']}")
        
        state["current_state"] = WorkflowState.START.value
        state["stories"] = []
        state["clarification_needed"] = False
        state["clarification_questions"] = []
        state["clarification_responses"] = []
        state["slack_message_timestamp"] = None
        state["team_members"] = DEFAULT_TEAM_MEMBERS
        state["messages"] = add_messages(state["messages"], [
            {"role": "system", "content": f"Starting analysis of project goal: {state['project_goal']}"}
        ])
        
        return state
    
    def _analyze_goal(self, state: AgentIanState) -> AgentIanState:
        """Analyze the project goal for complexity and clarity"""
        logger.info("🔍 Analyzing project goal...")
        
        state["current_state"] = WorkflowState.ANALYZE_GOAL.value
        project_goal = state["project_goal"]
        
        # Use story breakdown engine for analysis
        analysis = self.story_engine.analyze_project_goal(project_goal)
        
        state["clarification_questions"] = analysis["questions"]
        state["clarification_needed"] = analysis["clarification_needed"]
        
        logger.info(f"Analysis complete. Clarification needed: {state['clarification_needed']}")
        if state["clarification_needed"]:
            logger.info(f"Questions to ask: {len(analysis['questions'])}")
        
        return state
    
    def _should_seek_clarification(self, state: AgentIanState) -> str:
        """Decide whether to seek clarification or continue"""
        return "clarification" if state["clarification_needed"] else "continue"
    
    def _seek_clarification(self, state: AgentIanState) -> AgentIanState:
        """Seek clarification from the human via Slack"""
        logger.info("💬 Seeking clarification from human via Slack...")
        
        state["current_state"] = WorkflowState.SEEK_CLARIFICATION.value
        
        # Format questions nicely for Slack
        questions_text = "🤔 **I need some clarification to create better user stories:**\n\n"
        for i, question in enumerate(state["clarification_questions"], 1):
            questions_text += f"{i}. {question}\n"
        
        questions_text += f"\nProject Goal: _{state['project_goal']}_"
        questions_text += "\n\nPlease provide answers so I can create detailed user stories!"
        
        # Send to Slack WITH tracking code
        timestamp = self.slack_client.send_message(questions_text, add_tracking=True)
        
        if timestamp:
            state["slack_message_timestamp"] = timestamp
            logger.info("✅ Clarification questions sent to Slack with tracking")
        else:
            logger.error("❌ Failed to send clarification to Slack")
            state["clarification_needed"] = False
        
        state["messages"] = add_messages(state["messages"], [
            {"role": "assistant", "content": f"Sent clarification questions to Slack: {questions_text}"}
        ])
        
        return state
    
    def _process_clarification(self, state: AgentIanState) -> AgentIanState:
        """Wait for and process human clarification from Slack"""
        logger.info("⏳ Waiting for clarification response from Slack...")
        
        state["current_state"] = WorkflowState.PROCESS_CLARIFICATION.value
        
        if state["slack_message_timestamp"]:
            # Wait for human response (5 minutes timeout)
            response = self.slack_client.wait_for_response(
                state["slack_message_timestamp"], 
                timeout=300
            )
            
            if response:
                # Send acknowledgment
                ack_message = (
                    f"✅ Thanks for the clarification! Processing your response:\n\n"
                    f"_{response[:200]}{'...' if len(response) > 200 else ''}_\n\n"
                    f"Creating detailed user stories now... 🚀"
                )
                self.slack_client.send_message(ack_message)
                
                state["clarification_responses"] = [response]
                logger.info("✅ Received and acknowledged clarification")
                
                # Update the project goal with clarification
                enhanced_goal = f"{state['project_goal']}\n\nAdditional Requirements: {response}"
                state["project_goal"] = enhanced_goal
                
            else:
                logger.warning("⏰ No response received, proceeding with original goal")
                timeout_message = (
                    "⏰ I didn't receive a response, so I'll proceed with the original requirements. "
                    "You can always refine the stories later!"
                )
                self.slack_client.send_message(timeout_message)
        
        state["messages"] = add_messages(state["messages"], [
            {"role": "system", "content": f"Processed clarification. Enhanced goal: {state['project_goal']}"}
        ])
        
        return state
    
    def _break_down_stories(self, state: AgentIanState) -> AgentIanState:
        """Break down the project goal into user stories and tasks"""
        logger.info("📝 Breaking down project into user stories...")
        
        state["current_state"] = WorkflowState.BREAK_DOWN_STORIES.value
        project_goal = state["project_goal"]
        
        # Use story breakdown engine
        stories = self.story_engine.create_stories_for_project(project_goal)
        state["stories"] = stories
        
        logger.info(f"Created {len(stories)} user stories")
        
        # Send progress update to Slack
        progress_message = (
            f"📊 **Story Breakdown Complete!**\n\n"
            f"I've created {len(stories)} user stories for your project:\n\n"
        )
        
        for i, story in enumerate(stories, 1):
            progress_message += f"{i}. **{story.title}** ({story.estimated_points} points)\n"
        
        progress_message += "\nNow creating these in Jira... 🎯"
        self.slack_client.send_message(progress_message)
        
        return state
    
    def _create_stories_in_jira(self, state: AgentIanState) -> AgentIanState:
        """Create the user stories in Jira"""
        logger.info("📋 Creating user stories in Jira...")
        
        state["current_state"] = WorkflowState.CREATE_STORIES.value
        project_key = self.project_key
        
        try:
            created_stories = []
            for story in state["stories"]:
                # Create user story in Jira
                description = (
                    f"{story.description}\n\n**Acceptance Criteria:**\n" + 
                    "\n".join([f"- {criteria}" for criteria in story.acceptance_criteria])
                )
                
                created_story = self.jira_client.create_user_story(
                    project_key=project_key,
                    summary=story.title,
                    description=description,
                    story_points=story.estimated_points
                )
                
                if created_story:
                    logger.info(f"✅ Created story: {story.title}")
                    created_stories.append(created_story)
                    
                    # Add a comment with task breakdown
                    task_breakdown = "**Task Breakdown:**\n" + "\n".join([
                        f"- {task.title} ({task.task_type}, {task.estimated_hours}h): {task.description}"
                        for task in story.tasks
                    ])
                    
                    self.jira_client.add_issue_comment(created_story.key, task_breakdown)
                else:
                    logger.error(f"❌ Failed to create story: {story.title}")
            
            logger.info(f"Successfully created {len(created_stories)} stories in Jira")
            
            # Send success message to Slack
            success_message = (
                f"✅ **Stories Created in Jira!**\n\n"
                f"Successfully created {len(created_stories)} user stories in your Jira project. "
                f"You can view them at {self.jira_client.base_url}/browse/{project_key}\n\n"
                f"Next: Assigning tasks to team members... 👥"
            )
            self.slack_client.send_message(success_message)
            
        except Exception as e:
            logger.error(f"Error creating stories in Jira: {e}")
            error_message = (
                f"❌ **Error creating stories in Jira:** {str(e)}\n\n"
                f"I'll continue with task assignment for planning purposes."
            )
            self.slack_client.send_message(error_message)
            
            state["messages"] = add_messages(state["messages"], [
                {"role": "system", "content": f"Error creating stories: {e}"}
            ])
        
        return state
    
    def _assign_tasks(self, state: AgentIanState) -> AgentIanState:
        """Assign tasks to appropriate team members"""
        logger.info("👥 Assigning tasks to team members...")
        
        state["current_state"] = WorkflowState.ASSIGN_TASKS.value
        
        # Assignment summary for Slack
        assignment_summary = "👥 **Task Assignments:**\n\n"
        
        for story in state["stories"]:
            assignment_summary += f"**{story.title}:**\n"
            
            for task in story.tasks:
                # Smart assignment logic based on task type
                task.assigned_to = self._assign_task_to_role(task, state["team_members"])
                assignment_summary += f"  • {task.title} → @{task.assigned_to}\n"
                logger.info(f"📌 Assigned '{task.title}' to {task.assigned_to}")
            
            assignment_summary += "\n"
        
        # Send assignments to Slack
        self.slack_client.send_message(assignment_summary)
        return state
    
    def _assign_task_to_role(self, task, team_members: Dict[str, str]) -> str:
        """Assign task to appropriate team member based on task type"""
        task_type_lower = task.task_type.lower()
        
        assignment_map = {
            "development": "developer",
            "testing": "tester",
            "review": "reviewer",
            "design": "developer",  # Could be specialized designer if available
            "analysis": "product_owner",
            "documentation": "developer"
        }
        
        role = assignment_map.get(task_type_lower, "product_owner")
        return team_members.get(role, team_members["product_owner"])
    
    def _complete_workflow(self, state: AgentIanState) -> AgentIanState:
        """Complete the workflow"""
        logger.info("✅ AgentIan workflow completed successfully!")
        
        state["current_state"] = WorkflowState.COMPLETE.value
        
        # Calculate summary statistics
        total_stories = len(state["stories"])
        total_tasks = sum(len(story.tasks) for story in state["stories"])
        total_points = sum(story.estimated_points for story in state["stories"])
        total_hours = sum(
            task.estimated_hours 
            for story in state["stories"] 
            for task in story.tasks
        )
        
        summary = f"""🎉 **Project Breakdown Complete!**

📊 **Summary:**
• Created {total_stories} user stories
• Planned {total_tasks} tasks  
• Estimated {total_points} story points total
• Estimated {total_hours} development hours

✅ **What's Done:**
• Stories created in Jira
• Tasks assigned to team members
• Ready for development to begin!

🚀 **Next Steps:**
• Review stories in Jira: {self.jira_client.base_url}/browse/{self.project_key}
• AgentPete can start picking up development tasks
• I'll monitor progress and help refine requirements

Thanks for the collaboration! 🤖"""
        
        # Send completion message to Slack
        self.slack_client.send_message(summary)
        
        logger.info("Workflow completed successfully")
        state["messages"] = add_messages(state["messages"], [
            {"role": "assistant", "content": summary}
        ])
        
        return state
    
    def execute_workflow(self, project_goal: str) -> Dict[str, Any]:
        """Execute the complete workflow"""
        logger.info(f"🎯 Processing project goal: {project_goal}")
        
        initial_state = AgentIanState(
            messages=[],
            project_goal=project_goal,
            current_state=WorkflowState.START.value,
            stories=[],
            clarification_needed=False,
            clarification_questions=[],
            clarification_responses=[],
            slack_message_timestamp=None,
            project_key=self.project_key,
            error_message=None,
            team_members=DEFAULT_TEAM_MEMBERS
        )
        
        try:
            # Send initial message to Slack
            self.slack_client.send_message(
                f"🚀 **New Project Analysis Started!**\n\n"
                f"Goal: _{project_goal}_\n\n"
                f"Analyzing requirements and will ask questions if needed..."
            )
            
            # Run the workflow
            final_state = self.workflow.invoke(initial_state)
            
            return {
                "success": final_state["current_state"] == WorkflowState.COMPLETE.value,
                "state": final_state["current_state"],
                "stories_created": len(final_state.get("stories", [])),
                "clarification_needed": final_state.get("clarification_needed", False),
                "clarification_questions": final_state.get("clarification_questions", []),
                "clarification_responses": final_state.get("clarification_responses", []),
                "error": final_state.get("error_message")
            }
            
        except Exception as e:
            logger.error(f"Workflow execution error: {e}")
            self.slack_client.send_message(
                f"❌ **Workflow Error:** {str(e)}\n\n"
                f"Please check the logs for details."
            )
            return {
                "success": False,
                "error": str(e)
            }