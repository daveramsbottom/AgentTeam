"""
Developer Workflow Engine for AgentPete
LangGraph-based workflow for analyzing development tasks, creating estimates,
and generating implementation plans
"""
import logging
from typing import Dict, Any
from datetime import datetime
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages

from .states import (
    DeveloperWorkflowState, AgentPeteState, DevelopmentTask, 
    TechnicalRequirement, TechnicalEstimate, ImplementationPlan
)
from ai.technical_analyzer import TechnicalAnalyzer

logger = logging.getLogger(__name__)


class DeveloperWorkflowEngine:
    """LangGraph workflow engine for AgentPete's development task analysis"""
    
    def __init__(self, jira_client, slack_client, technical_analyzer: TechnicalAnalyzer, project_key: str):
        self.jira_client = jira_client
        self.slack_client = slack_client
        self.technical_analyzer = technical_analyzer
        self.project_key = project_key
        self.workflow = self._build_workflow()
    
    def _build_workflow(self) -> StateGraph:
        """Build the LangGraph workflow for development task analysis"""
        workflow = StateGraph(AgentPeteState)
        
        # Add nodes for each workflow step
        workflow.add_node("start", self._start_analysis)
        workflow.add_node("analyze_task", self._analyze_task)
        workflow.add_node("extract_requirements", self._extract_requirements)
        workflow.add_node("assess_complexity", self._assess_complexity)
        workflow.add_node("estimate_effort", self._estimate_effort)
        workflow.add_node("plan_implementation", self._plan_implementation)
        workflow.add_node("recommend_tech_stack", self._recommend_tech_stack)
        workflow.add_node("seek_clarification", self._seek_clarification)
        workflow.add_node("process_clarification", self._process_clarification)
        workflow.add_node("update_task", self._update_task)
        workflow.add_node("complete", self._complete_workflow)
        
        # Define workflow edges
        workflow.set_entry_point("start")
        workflow.add_edge("start", "analyze_task")
        workflow.add_edge("analyze_task", "extract_requirements")
        
        # Conditional path: check if clarification is needed after requirements extraction
        workflow.add_conditional_edges(
            "extract_requirements",
            self._should_seek_clarification,
            {
                "clarification": "seek_clarification",
                "continue": "assess_complexity"
            }
        )
        
        workflow.add_edge("seek_clarification", "process_clarification")
        workflow.add_edge("process_clarification", "assess_complexity")
        workflow.add_edge("assess_complexity", "estimate_effort")
        workflow.add_edge("estimate_effort", "recommend_tech_stack")
        workflow.add_edge("recommend_tech_stack", "plan_implementation")
        workflow.add_edge("plan_implementation", "update_task")
        workflow.add_edge("update_task", "complete")
        workflow.add_edge("complete", END)
        
        return workflow.compile()
    
    def _start_analysis(self, state: AgentPeteState) -> AgentPeteState:
        """Initialize the developer workflow"""
        task = state["current_task"]
        logger.info(f"🚀 AgentPete starting analysis of task: {task.issue_key}")
        
        state["current_state"] = DeveloperWorkflowState.START.value
        state["clarification_needed"] = False
        state["clarification_questions"] = []
        state["clarification_responses"] = []
        state["slack_message_timestamp"] = None
        state["messages"] = add_messages(state["messages"], [
            {"role": "system", "content": f"Starting analysis of development task: {task.title}"}
        ])
        
        # Update task metadata
        task.processing_notes.append(f"Started analysis at {datetime.now().isoformat()}")
        
        return state
    
    def _analyze_task(self, state: AgentPeteState) -> AgentPeteState:
        """Analyze the development task for initial understanding"""
        logger.info("🔍 Analyzing development task...")
        
        state["current_state"] = DeveloperWorkflowState.ANALYZE_TASK.value
        task = state["current_task"]
        
        # Basic task analysis - this is mostly logging and metadata
        logger.info(f"Task Type: {task.issue_type}")
        logger.info(f"Priority: {task.priority}")
        logger.info(f"Status: {task.status}")
        
        # Log to processing notes
        task.processing_notes.append(f"Task analysis completed: {task.issue_type} with {task.priority} priority")
        
        state["messages"] = add_messages(state["messages"], [
            {"role": "assistant", "content": f"Analyzed task {task.issue_key}: {task.issue_type} with {task.priority} priority"}
        ])
        
        return state
    
    def _extract_requirements(self, state: AgentPeteState) -> AgentPeteState:
        """Extract technical requirements from the task description"""
        logger.info("📋 Extracting technical requirements...")
        
        state["current_state"] = DeveloperWorkflowState.EXTRACT_REQUIREMENTS.value
        task = state["current_task"]
        
        # Use technical analyzer to extract requirements
        requirements = self.technical_analyzer.analyze_task_requirements(
            task.issue_key,
            task.title,
            task.description,
            task.issue_type
        )
        
        task.technical_requirements = requirements
        
        logger.info(f"Extracted {len(requirements)} technical requirements")
        for req in requirements:
            logger.info(f"  • {req.requirement_type}: {req.description} ({req.priority})")
        
        task.processing_notes.append(f"Extracted {len(requirements)} technical requirements")
        
        state["messages"] = add_messages(state["messages"], [
            {"role": "assistant", "content": f"Extracted {len(requirements)} technical requirements from task description"}
        ])
        
        return state
    
    def _should_seek_clarification(self, state: AgentPeteState) -> str:
        """Decide whether to seek clarification based on requirements analysis"""
        task = state["current_task"]
        
        # Check for indicators that clarification might be needed
        vague_requirements = len([r for r in task.technical_requirements if "unclear" in r.description.lower()])
        high_complexity_reqs = len([r for r in task.technical_requirements if r.complexity in ["high", "very-high"]])
        missing_details = len(task.technical_requirements) < 2 and len(task.description) < 100
        
        if vague_requirements > 0 or (high_complexity_reqs > 1 and missing_details):
            state["clarification_needed"] = True
            return "clarification"
        else:
            return "continue"
    
    def _seek_clarification(self, state: AgentPeteState) -> AgentPeteState:
        """Seek clarification on ambiguous requirements via Slack"""
        logger.info("❓ Seeking clarification on task requirements...")
        
        state["current_state"] = DeveloperWorkflowState.SEEK_CLARIFICATION.value
        task = state["current_task"]
        
        # Generate clarification questions based on analysis
        questions = self._generate_clarification_questions(task)
        state["clarification_questions"] = questions
        
        # Format questions for Slack
        questions_text = f"""🤔 **Technical Clarification Needed - {task.issue_key}**

**Task**: {task.title}

I need some clarification to provide accurate estimates and implementation plans:

"""
        for i, question in enumerate(questions, 1):
            questions_text += f"{i}. {question}\n"
        
        questions_text += f"""
**Context**: {task.description[:200]}{'...' if len(task.description) > 200 else ''}

Please provide clarification so I can create a detailed technical analysis and accurate estimate! 🚀"""
        
        # Send to Slack WITH tracking code
        timestamp = self.slack_client.send_message(questions_text, add_tracking=True)
        
        if timestamp:
            state["slack_message_timestamp"] = timestamp
            logger.info("✅ Clarification questions sent to Slack with tracking")
        else:
            logger.error("❌ Failed to send clarification to Slack")
            state["clarification_needed"] = False
        
        state["messages"] = add_messages(state["messages"], [
            {"role": "assistant", "content": f"Sent {len(questions)} clarification questions to Slack"}
        ])
        
        return state
    
    def _process_clarification(self, state: AgentPeteState) -> AgentPeteState:
        """Wait for and process clarification response from Slack"""
        logger.info("⏳ Waiting for clarification response from Slack...")
        
        state["current_state"] = DeveloperWorkflowState.PROCESS_CLARIFICATION.value
        task = state["current_task"]
        
        if state["slack_message_timestamp"]:
            # Wait for human response (3 minutes timeout for technical questions)
            response = self.slack_client.wait_for_response(
                state["slack_message_timestamp"],
                timeout=180
            )
            
            if response:
                # Send acknowledgment
                ack_message = (
                    f"✅ **Clarification Received - {task.issue_key}**\n\n"
                    f"Thanks for the technical details! Processing your response:\n\n"
                    f"_{response[:200]}{'...' if len(response) > 200 else ''}_\n\n"
                    f"Creating updated technical analysis and implementation plan... ⚙️"
                )
                self.slack_client.send_message(ack_message)
                
                state["clarification_responses"] = [response]
                logger.info("✅ Received and acknowledged clarification")
                
                # Update task description with clarification
                task.description = f"{task.description}\n\n**Additional Technical Details:**\n{response}"
                task.clarification_responses = [response]
                task.processing_notes.append(f"Received clarification: {len(response)} characters")
                
            else:
                logger.warning("⏰ No response received, proceeding with original requirements")
                timeout_message = (
                    f"⏰ **No Response Received - {task.issue_key}**\n\n"
                    f"I didn't receive clarification within the timeout, so I'll proceed with "
                    f"my best interpretation of the requirements.\n\n"
                    f"You can always provide additional details later if needed!"
                )
                self.slack_client.send_message(timeout_message)
        
        state["messages"] = add_messages(state["messages"], [
            {"role": "system", "content": f"Processed clarification for task {task.issue_key}"}
        ])
        
        return state
    
    def _assess_complexity(self, state: AgentPeteState) -> AgentPeteState:
        """Assess the technical complexity of the task"""
        logger.info("📊 Assessing technical complexity...")
        
        state["current_state"] = DeveloperWorkflowState.ASSESS_COMPLEXITY.value
        task = state["current_task"]
        
        # Use technical analyzer to assess complexity
        complexity, complexity_factor = self.technical_analyzer.assess_complexity(
            task.title,
            task.description,
            task.technical_requirements
        )
        
        task.complexity_assessment = complexity
        
        logger.info(f"Assessed complexity: {complexity} (factor: {complexity_factor})")
        task.processing_notes.append(f"Complexity assessment: {complexity} (factor: {complexity_factor})")
        
        state["messages"] = add_messages(state["messages"], [
            {"role": "assistant", "content": f"Assessed task complexity as: {complexity}"}
        ])
        
        return state
    
    def _estimate_effort(self, state: AgentPeteState) -> AgentPeteState:
        """Estimate development effort for the task"""
        logger.info("⏱️ Estimating development effort...")
        
        state["current_state"] = DeveloperWorkflowState.ESTIMATE_EFFORT.value
        task = state["current_task"]
        
        # Get story points from Jira if available
        story_points = None
        try:
            jira_issue = self.jira_client.get_issue(task.issue_key)
            story_points = jira_issue.story_points if jira_issue else None
        except Exception as e:
            logger.warning(f"Could not retrieve story points from Jira: {e}")
        
        # Use technical analyzer to estimate effort
        estimate = self.technical_analyzer.estimate_effort(
            task.title,
            task.description,
            task.complexity_assessment,
            task.technical_requirements,
            story_points
        )
        
        task.estimate = estimate
        
        logger.info(f"Estimated effort: {estimate.estimated_hours} hours (confidence: {estimate.confidence_level})")
        logger.info(f"Breakdown: {estimate.breakdown}")
        
        task.processing_notes.append(f"Effort estimate: {estimate.estimated_hours}h ({estimate.confidence_level} confidence)")
        
        state["messages"] = add_messages(state["messages"], [
            {"role": "assistant", "content": f"Estimated {estimate.estimated_hours} development hours"}
        ])
        
        return state
    
    def _recommend_tech_stack(self, state: AgentPeteState) -> AgentPeteState:
        """Recommend appropriate technology stack"""
        logger.info("⚙️ Recommending technology stack...")
        
        state["current_state"] = DeveloperWorkflowState.RECOMMEND_TECH_STACK.value
        task = state["current_task"]
        
        # Use technical analyzer to recommend tech stack
        tech_recommendations = self.technical_analyzer.recommend_tech_stack(
            task.title,
            task.description,
            task.technical_requirements
        )
        
        logger.info(f"Generated {len(tech_recommendations)} technology recommendations")
        for tech in tech_recommendations:
            logger.info(f"  • {tech.category}: {tech.recommended_tech}")
        
        task.processing_notes.append(f"Tech stack recommendations: {len(tech_recommendations)} categories")
        
        state["messages"] = add_messages(state["messages"], [
            {"role": "assistant", "content": f"Recommended technology stack with {len(tech_recommendations)} categories"}
        ])
        
        # Store tech recommendations for implementation planning
        state["tech_recommendations"] = tech_recommendations
        
        return state
    
    def _plan_implementation(self, state: AgentPeteState) -> AgentPeteState:
        """Create detailed implementation plan"""
        logger.info("📋 Creating implementation plan...")
        
        state["current_state"] = DeveloperWorkflowState.PLAN_IMPLEMENTATION.value
        task = state["current_task"]
        
        # Get tech recommendations from previous step
        tech_recommendations = state.get("tech_recommendations", [])
        
        # Use technical analyzer to create implementation plan
        implementation_plan = self.technical_analyzer.create_implementation_plan(
            task.title,
            task.description,
            task.technical_requirements,
            tech_recommendations
        )
        
        task.implementation_plan = implementation_plan
        
        logger.info(f"Created implementation plan with {len(implementation_plan.implementation_steps)} steps")
        logger.info(f"Architecture: {implementation_plan.architecture_approach}")
        
        task.processing_notes.append(f"Implementation plan: {len(implementation_plan.implementation_steps)} steps")
        
        state["messages"] = add_messages(state["messages"], [
            {"role": "assistant", "content": f"Created detailed implementation plan with {len(implementation_plan.implementation_steps)} steps"}
        ])
        
        return state
    
    def _update_task(self, state: AgentPeteState) -> AgentPeteState:
        """Update the Jira task with analysis results"""
        logger.info("📝 Updating Jira task with analysis results...")
        
        state["current_state"] = DeveloperWorkflowState.UPDATE_TASK.value
        task = state["current_task"]
        
        try:
            # Create comprehensive update comment for Jira
            update_comment = self._generate_jira_update_comment(task)
            
            # Add comment to Jira issue
            success = self.jira_client.add_issue_comment(task.issue_key, update_comment)
            
            if success:
                logger.info(f"✅ Successfully updated Jira task {task.issue_key}")
                task.updated_in_jira = True
                task.processing_notes.append("Successfully updated in Jira")
                
                # Send success message to Slack
                success_message = f"""✅ **Task Analysis Complete - {task.issue_key}**

📋 **Task**: {task.title}
⏱️ **Estimate**: {task.estimate.estimated_hours if task.estimate else 'N/A'} hours
📊 **Complexity**: {task.complexity_assessment}
🔧 **Tech Stack**: {len(task.implementation_plan.tech_stack) if task.implementation_plan else 0} recommendations

**Updated in Jira** with detailed technical analysis, effort estimates, and implementation plan!

Ready for development! 🚀"""
                
                self.slack_client.send_message(success_message)
                
            else:
                logger.error(f"❌ Failed to update Jira task {task.issue_key}")
                task.processing_notes.append("Failed to update in Jira")
                
                # Send error message to Slack
                error_message = f"""⚠️ **Jira Update Failed - {task.issue_key}**

Analysis completed successfully, but I couldn't update the Jira task.
Please check Jira permissions or try again later.

Analysis results are still available and valid! 📊"""
                
                self.slack_client.send_message(error_message)
                
        except Exception as e:
            logger.error(f"Error updating Jira task {task.issue_key}: {e}")
            task.processing_notes.append(f"Error updating Jira: {str(e)}")
        
        state["messages"] = add_messages(state["messages"], [
            {"role": "assistant", "content": f"Updated Jira task {task.issue_key} with analysis results"}
        ])
        
        return state
    
    def _complete_workflow(self, state: AgentPeteState) -> AgentPeteState:
        """Complete the developer workflow"""
        logger.info("✅ AgentPete workflow completed successfully!")
        
        state["current_state"] = DeveloperWorkflowState.COMPLETE.value
        task = state["current_task"]
        
        task.analysis_complete = True
        task.processing_notes.append(f"Workflow completed at {datetime.now().isoformat()}")
        
        # Generate summary statistics
        total_requirements = len(task.technical_requirements)
        estimated_hours = task.estimate.estimated_hours if task.estimate else 0
        implementation_steps = len(task.implementation_plan.implementation_steps) if task.implementation_plan else 0
        tech_recommendations = len(task.implementation_plan.tech_stack) if task.implementation_plan else 0
        
        summary = f"""🎉 **Development Analysis Complete - {task.issue_key}**

📊 **Analysis Summary:**
• Task: {task.title}
• Type: {task.issue_type} 
• Priority: {task.priority}
• Complexity: {task.complexity_assessment}

🔍 **Technical Analysis:**
• Requirements extracted: {total_requirements}
• Estimated effort: {estimated_hours} hours
• Implementation steps: {implementation_steps}
• Technology recommendations: {tech_recommendations}

✅ **Status:**
• Analysis complete and stored in Jira
• Ready for development implementation
• All technical questions resolved

**Next Steps**: Review the analysis in Jira and begin implementation when ready! 🚀"""
        
        # Send completion summary to Slack
        self.slack_client.send_message(summary)
        
        logger.info("Developer workflow completed successfully")
        state["messages"] = add_messages(state["messages"], [
            {"role": "assistant", "content": summary}
        ])
        
        return state
    
    def _generate_clarification_questions(self, task: DevelopmentTask) -> List[str]:
        """Generate intelligent clarification questions for ambiguous requirements"""
        questions = []
        
        # Check for common ambiguity patterns
        desc_lower = task.description.lower()
        
        if "user" in desc_lower and "interface" in desc_lower:
            questions.append("What specific user roles or types need to interact with this feature?")
            questions.append("Are there any specific UI/UX requirements or design constraints?")
        
        if "data" in desc_lower or "save" in desc_lower:
            questions.append("What data needs to be stored and what's the expected data structure?")
            questions.append("Are there any data validation or security requirements?")
        
        if "integration" in desc_lower or "api" in desc_lower:
            questions.append("Which external systems or APIs need to be integrated?")
            questions.append("What authentication or rate limiting considerations are there?")
        
        if len(task.description) < 50:
            questions.append("Could you provide more detailed requirements and acceptance criteria?")
        
        # Check for high complexity requirements that might need clarification
        high_complexity_reqs = [r for r in task.technical_requirements if r.complexity in ["high", "very-high"]]
        if high_complexity_reqs:
            questions.append("For the complex requirements identified, are there any specific technical constraints or preferences?")
        
        # Default technical questions if nothing specific identified
        if not questions:
            questions.extend([
                "Are there any specific technology stack preferences or constraints?",
                "What are the performance and scalability requirements?",
                "Are there any integration requirements with existing systems?"
            ])
        
        return questions[:4]  # Limit to 4 questions to avoid overwhelming
    
    def _generate_jira_update_comment(self, task: DevelopmentTask) -> str:
        """Generate comprehensive Jira comment with analysis results"""
        comment_parts = [
            f"*AgentPete Development Analysis - {datetime.now().strftime('%Y-%m-%d %H:%M')}*",
            "",
            "h3. 📊 Technical Analysis Summary",
            f"*Complexity Assessment:* {task.complexity_assessment.title()}",
            f"*Requirements Identified:* {len(task.technical_requirements)}",
        ]
        
        # Add effort estimate if available
        if task.estimate:
            comment_parts.extend([
                "",
                "h3. ⏱️ Effort Estimate",
                f"*Total Development Hours:* {task.estimate.estimated_hours}",
                f"*Confidence Level:* {task.estimate.confidence_level.title()}",
                f"*Risk Buffer:* +{task.estimate.risk_buffer_hours} hours",
                "",
                "*Breakdown:*"
            ])
            
            for activity, hours in task.estimate.breakdown.items():
                comment_parts.append(f"• {activity.title()}: {hours} hours")
        
        # Add technical requirements
        if task.technical_requirements:
            comment_parts.extend([
                "",
                "h3. 📋 Technical Requirements"
            ])
            
            for i, req in enumerate(task.technical_requirements, 1):
                comment_parts.extend([
                    f"*{i}. {req.requirement_type.title()} Requirement* ({req.priority}, {req.complexity} complexity)",
                    req.description
                ])
                if req.acceptance_criteria:
                    comment_parts.extend([
                        "*Acceptance Criteria:*",
                        *[f"• {criteria}" for criteria in req.acceptance_criteria]
                    ])
                comment_parts.append("")
        
        # Add technology recommendations
        if task.implementation_plan and task.implementation_plan.tech_stack:
            comment_parts.extend([
                "h3. ⚙️ Technology Stack Recommendations"
            ])
            
            for tech in task.implementation_plan.tech_stack:
                comment_parts.extend([
                    f"*{tech.category.title()}:* {tech.recommended_tech}",
                    f"• Reasoning: {tech.reasoning}",
                    f"• Alternatives: {', '.join(tech.alternatives)}",
                    ""
                ])
        
        # Add implementation plan
        if task.implementation_plan:
            comment_parts.extend([
                "h3. 🏗️ Implementation Plan",
                f"*Architecture Approach:* {task.implementation_plan.architecture_approach}",
                ""
            ])
            
            if task.implementation_plan.implementation_steps:
                comment_parts.extend([
                    "*Implementation Steps:*",
                    *[f"{i}. {step}" for i, step in enumerate(task.implementation_plan.implementation_steps, 1)],
                    ""
                ])
            
            if task.implementation_plan.api_endpoints:
                comment_parts.extend([
                    "*API Endpoints:*",
                    *[f"• {endpoint['method']} {endpoint['path']} - {endpoint['purpose']}" 
                      for endpoint in task.implementation_plan.api_endpoints],
                    ""
                ])
        
        # Add assumptions and risks if available
        if task.estimate and (task.estimate.assumptions or task.estimate.risks):
            comment_parts.extend([
                "h3. ⚠️ Assumptions & Risks"
            ])
            
            if task.estimate.assumptions:
                comment_parts.extend([
                    "*Assumptions:*",
                    *[f"• {assumption}" for assumption in task.estimate.assumptions],
                    ""
                ])
            
            if task.estimate.risks:
                comment_parts.extend([
                    "*Risks:*", 
                    *[f"• {risk}" for risk in task.estimate.risks],
                    ""
                ])
        
        comment_parts.extend([
            "---",
            f"_Analysis completed by AgentPete at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}_"
        ])
        
        return "\n".join(comment_parts)
    
    def execute_task_analysis_workflow(self, issue_key: str, issue_summary: str,
                                     issue_description: str, issue_type: str,
                                     current_status: str) -> Dict[str, Any]:
        """Execute the complete task analysis workflow"""
        logger.info(f"🎯 Starting task analysis workflow for: {issue_key}")
        
        # Create development task object
        development_task = DevelopmentTask(
            issue_key=issue_key,
            title=issue_summary,
            description=issue_description,
            issue_type=issue_type,
            priority="Medium",  # Default, will be updated from Jira if available
            status=current_status,
            assigned_date=datetime.now()
        )
        
        # Create initial state
        initial_state = AgentPeteState(
            messages=[],
            current_task=development_task,
            current_state=DeveloperWorkflowState.START.value,
            clarification_needed=False,
            clarification_questions=[],
            clarification_responses=[],
            slack_message_timestamp=None,
            error_message=None,
            project_key=self.project_key
        )
        
        try:
            # Run the workflow
            final_state = self.workflow.invoke(initial_state)
            
            completed_task = final_state["current_task"]
            
            return {
                "success": final_state["current_state"] == DeveloperWorkflowState.COMPLETE.value,
                "issue_key": issue_key,
                "analysis": {
                    "requirements_count": len(completed_task.technical_requirements),
                    "complexity": completed_task.complexity_assessment,
                    "requirements": [req.__dict__ for req in completed_task.technical_requirements]
                },
                "estimate": completed_task.estimate.__dict__ if completed_task.estimate else None,
                "implementation_plan": {
                    "architecture": completed_task.implementation_plan.architecture_approach,
                    "steps_count": len(completed_task.implementation_plan.implementation_steps),
                    "tech_stack_count": len(completed_task.implementation_plan.tech_stack)
                } if completed_task.implementation_plan else None,
                "updated_in_jira": completed_task.updated_in_jira,
                "clarification_needed": final_state.get("clarification_needed", False),
                "processing_notes": completed_task.processing_notes,
                "error": final_state.get("error_message")
            }
            
        except Exception as e:
            logger.error(f"Workflow execution error: {e}")
            
            # Send error message to Slack
            error_message = f"""❌ **Workflow Error - {issue_key}**

Task: {issue_summary}
Error: {str(e)}

Please check the logs and try again. If the error persists, contact support."""
            
            self.slack_client.send_message(error_message)
            
            return {
                "success": False,
                "issue_key": issue_key,
                "error": str(e),
                "analysis": None,
                "estimate": None,
                "implementation_plan": None,
                "updated_in_jira": False
            }