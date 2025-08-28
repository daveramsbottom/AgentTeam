"""
AgentPete - Senior Developer Agent
AI-powered development agent that monitors assigned tasks, analyzes requirements, 
provides estimates, and creates implementation plans
"""
import logging
import time
from typing import Dict, Any, Optional, List
from datetime import datetime

from communication.slack_client import SlackClient
from workflows.developer_workflow import DeveloperWorkflowEngine
from jira.client import JiraClient
from ai.openai_client import get_openai_client
from ai.technical_analyzer import TechnicalAnalyzer

logger = logging.getLogger(__name__)


class AgentPete:
    """
    AgentPete - Senior Developer Agent
    Handles task analysis, estimation, implementation planning, and development coordination
    """
    
    def __init__(self, jira_base_url: str, jira_username: str, jira_api_token: str, 
                 slack_token: str, slack_channel: str, project_key: str):
        """Initialize AgentPete with all necessary clients"""
        
        # Initialize clients
        self.jira_client = JiraClient(jira_base_url, jira_username, jira_api_token)
        self.slack_client = SlackClient(slack_token, slack_channel)
        self.project_key = project_key
        
        # Initialize AI capabilities
        self.ai_client = get_openai_client()
        self.technical_analyzer = TechnicalAnalyzer(self.ai_client)
        
        # Initialize workflow engine
        self.workflow_engine = DeveloperWorkflowEngine(
            self.jira_client, 
            self.slack_client, 
            self.technical_analyzer,
            project_key
        )
        
        # Agent metadata
        self.name = "AgentPete"
        self.role = "Senior Developer"
        self.agent_username = "agentpete"  # Jira assignee name
        self.capabilities = [
            "Task analysis and requirement extraction",
            "Technical complexity assessment", 
            "Development effort estimation",
            "Implementation planning and architecture design",
            "Technology stack recommendations",
            "Code structure and component planning",
            "Technical clarification requests",
            "Cross-agent coordination with AgentIan",
            "Jira task management and progress tracking"
        ]
        
        # Task monitoring configuration
        self.monitoring_enabled = False
        self.assigned_tasks = {}  # Cache of currently assigned tasks
        self.completed_tasks = {}  # History of completed tasks
        
        if self.ai_client:
            logger.info("🤖 AgentPete initialized with AI capabilities")
        else:
            logger.info("🤖 AgentPete initialized without AI (using fallback methods)")
        
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
    
    def start_task_monitoring(self) -> bool:
        """Start monitoring for assigned development tasks"""
        logger.info("👀 Starting task monitoring...")
        
        if not self.authenticate():
            return False
        
        self.monitoring_enabled = True
        
        # Send startup message to Slack
        startup_message = f"""🚀 **{self.name} Online - Ready for Development**

👨‍💻 **Role**: {self.role}
🎯 **Project**: {self.project_key}
📋 **Monitoring**: Tasks assigned to '{self.agent_username}'

**Capabilities**:
• 🔍 Analyze user stories and extract technical requirements
• 📊 Provide accurate effort estimates with risk assessment  
• 🏗️ Create detailed implementation plans and architecture
• ⚙️ Recommend optimal technology stacks and patterns
• 💬 Request clarifications for ambiguous requirements
• 🤝 Coordinate with AgentIan on requirement changes

Ready to pick up development tasks! 💪"""
        
        self.slack_client.send_message(startup_message)
        return True
    
    def check_for_assigned_tasks(self) -> List[Dict[str, Any]]:
        """Check Jira for tasks assigned to this agent"""
        logger.info(f"🔍 Checking for tasks assigned to {self.agent_username}...")
        
        try:
            # Get all issues assigned to AgentPete
            issues = self.jira_client.get_issues(
                project_key=self.project_key,
                issue_types=['Story', 'Task', 'Sub-task']
            )
            
            # Filter for tasks assigned to this agent
            assigned_issues = [
                issue for issue in issues 
                if issue.assigned_to and self.agent_username.lower() in issue.assigned_to.lower()
            ]
            
            # Filter for new tasks (not already processed)
            new_tasks = []
            for issue in assigned_issues:
                if issue.key not in self.assigned_tasks:
                    new_tasks.append({
                        'issue': issue,
                        'assigned_date': datetime.now(),
                        'status': 'new'
                    })
                    self.assigned_tasks[issue.key] = {
                        'issue': issue,
                        'assigned_date': datetime.now(),
                        'status': 'new',
                        'analysis': None,
                        'estimate': None,
                        'implementation_plan': None
                    }
            
            if new_tasks:
                logger.info(f"📋 Found {len(new_tasks)} new assigned tasks")
                for task in new_tasks:
                    logger.info(f"   • {task['issue'].key}: {task['issue'].summary}")
            else:
                logger.debug(f"No new tasks found (monitoring {len(self.assigned_tasks)} existing tasks)")
            
            return new_tasks
            
        except Exception as e:
            logger.error(f"Error checking for assigned tasks: {e}")
            return []
    
    def process_assigned_task(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process a newly assigned task with analysis, estimation, and planning"""
        issue = task_data['issue']
        logger.info(f"⚙️ Processing assigned task: {issue.key}")
        
        try:
            # Send initial processing message
            processing_message = f"""🔧 **Processing Development Task**

📋 **Task**: {issue.key} - {issue.summary}
🏷️ **Type**: {issue.issue_type}
⭐ **Priority**: {issue.priority}
📅 **Status**: {issue.status}

🤖 Analyzing requirements and creating implementation plan...
This may take a few moments for complex tasks."""
            
            self.slack_client.send_message(processing_message)
            
            # Execute the developer workflow
            workflow_result = self.workflow_engine.execute_task_analysis_workflow(
                issue_key=issue.key,
                issue_summary=issue.summary,
                issue_description=issue.description,
                issue_type=issue.issue_type,
                current_status=issue.status
            )
            
            # Update task cache with results
            self.assigned_tasks[issue.key].update({
                'status': 'processed',
                'analysis': workflow_result.get('analysis'),
                'estimate': workflow_result.get('estimate'), 
                'implementation_plan': workflow_result.get('implementation_plan'),
                'processed_date': datetime.now(),
                'workflow_result': workflow_result
            })
            
            logger.info(f"✅ Successfully processed task {issue.key}")
            return workflow_result
            
        except Exception as e:
            logger.error(f"❌ Error processing task {issue.key}: {e}")
            
            # Update task with error status
            self.assigned_tasks[issue.key].update({
                'status': 'error',
                'error': str(e),
                'error_date': datetime.now()
            })
            
            # Send error message to Slack
            error_message = f"""❌ **Task Processing Error**

📋 **Task**: {issue.key} - {issue.summary}
🚨 **Error**: {str(e)}

I'll retry processing this task on the next monitoring cycle.
If this error persists, please check the task requirements or contact support."""
            
            self.slack_client.send_message(error_message)
            return {'success': False, 'error': str(e)}
    
    def run_monitoring_cycle(self) -> Dict[str, Any]:
        """Run a single monitoring cycle to check and process tasks"""
        cycle_start = datetime.now()
        logger.info("🔄 Running task monitoring cycle...")
        
        # Check for new assigned tasks
        new_tasks = self.check_for_assigned_tasks()
        
        results = {
            'cycle_start': cycle_start,
            'new_tasks_found': len(new_tasks),
            'processed_tasks': [],
            'errors': []
        }
        
        # Process each new task
        for task_data in new_tasks:
            try:
                result = self.process_assigned_task(task_data)
                results['processed_tasks'].append({
                    'issue_key': task_data['issue'].key,
                    'result': result
                })
            except Exception as e:
                error_info = {
                    'issue_key': task_data['issue'].key,
                    'error': str(e)
                }
                results['errors'].append(error_info)
                logger.error(f"Error in monitoring cycle for {task_data['issue'].key}: {e}")
        
        cycle_end = datetime.now()
        cycle_duration = (cycle_end - cycle_start).total_seconds()
        
        results.update({
            'cycle_end': cycle_end,
            'duration_seconds': cycle_duration,
            'total_monitored_tasks': len(self.assigned_tasks),
            'success': len(results['errors']) == 0
        })
        
        if results['new_tasks_found'] > 0:
            logger.info(f"✅ Monitoring cycle completed: {results['new_tasks_found']} new tasks processed in {cycle_duration:.1f}s")
        else:
            logger.debug(f"🔄 Monitoring cycle completed: no new tasks ({cycle_duration:.1f}s)")
        
        return results
    
    def run_continuous_monitoring(self, check_interval: int = 60) -> None:
        """Run continuous task monitoring loop"""
        logger.info(f"🔄 Starting continuous monitoring (check every {check_interval}s)")
        
        if not self.start_task_monitoring():
            logger.error("❌ Failed to start task monitoring")
            return
        
        try:
            while self.monitoring_enabled:
                # Run monitoring cycle
                cycle_result = self.run_monitoring_cycle()
                
                # Sleep until next check
                logger.debug(f"😴 Sleeping {check_interval}s until next monitoring cycle...")
                time.sleep(check_interval)
                
        except KeyboardInterrupt:
            logger.info("⏹️ Monitoring stopped by user")
        except Exception as e:
            logger.error(f"❌ Error in continuous monitoring: {e}")
        finally:
            self.stop_monitoring()
    
    def stop_monitoring(self) -> None:
        """Stop task monitoring and cleanup"""
        logger.info("⏹️ Stopping task monitoring...")
        self.monitoring_enabled = False
        
        # Send shutdown message
        shutdown_message = f"""⏹️ **{self.name} Going Offline**

📊 **Session Summary**:
• Monitored tasks: {len(self.assigned_tasks)}
• Completed tasks: {len([t for t in self.assigned_tasks.values() if t['status'] == 'processed'])}
• Tasks with errors: {len([t for t in self.assigned_tasks.values() if t['status'] == 'error'])}

Thank you for the development session! 👨‍💻"""
        
        self.slack_client.send_message(shutdown_message)
    
    def get_task_summary(self) -> Dict[str, Any]:
        """Get summary of current task status"""
        total_tasks = len(self.assigned_tasks)
        processed_tasks = len([t for t in self.assigned_tasks.values() if t['status'] == 'processed'])
        error_tasks = len([t for t in self.assigned_tasks.values() if t['status'] == 'error'])
        new_tasks = len([t for t in self.assigned_tasks.values() if t['status'] == 'new'])
        
        return {
            'total_assigned_tasks': total_tasks,
            'processed_tasks': processed_tasks,
            'error_tasks': error_tasks,
            'new_tasks': new_tasks,
            'monitoring_enabled': self.monitoring_enabled,
            'agent_name': self.name,
            'agent_username': self.agent_username,
            'project_key': self.project_key
        }
    
    def send_status_update(self) -> None:
        """Send current status update to Slack"""
        summary = self.get_task_summary()
        
        status_message = f"""📊 **{self.name} Status Update**

🎯 **Project**: {self.project_key}
👤 **Monitoring**: Tasks assigned to '{self.agent_username}'

📋 **Task Summary**:
• Total assigned: {summary['total_assigned_tasks']}
• ✅ Processed: {summary['processed_tasks']}
• 🔄 New/In Progress: {summary['new_tasks']}
• ❌ Errors: {summary['error_tasks']}

🤖 **Status**: {'🟢 Monitoring Active' if self.monitoring_enabled else '🔴 Monitoring Stopped'}

Ready to analyze and estimate your development tasks! 🚀"""
        
        self.slack_client.send_message(status_message)