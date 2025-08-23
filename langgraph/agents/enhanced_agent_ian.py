"""
Enhanced AgentIan - Flexible, Event-Driven Product Owner Agent
Integrates state machine, intelligent context analysis, and event monitoring
"""
import logging
import asyncio
from typing import Dict, Any, List, Optional
from datetime import datetime

from .agent_ian import AgentIan  # Inherit from existing AgentIan
from workflows.agent_state_machine import DynamicStateMachine, Event, EventType, AgentContext, AgentMode
from workflows.event_monitor import EventDrivenMonitor, MonitorConfig
from ai.context_analyzer import IntelligentContextAnalyzer, ProjectContext

logger = logging.getLogger(__name__)


class EnhancedAgentIan(AgentIan):
    """
    Enhanced AgentIan with flexible workflows, intelligent context analysis, and event-driven operation
    """
    
    def __init__(self, jira_base_url: str, jira_username: str, jira_api_token: str,
                 slack_token: str, slack_channel: str, project_key: str):
        
        # Initialize parent AgentIan
        super().__init__(jira_base_url, jira_username, jira_api_token, slack_token, slack_channel, project_key)
        
        # Initialize new flexible systems
        self.state_machine = DynamicStateMachine("enhanced_agent_ian")
        self.context_analyzer = IntelligentContextAnalyzer(self.ai_client)
        
        # Check AI status and warn if there are issues
        if self.ai_client and hasattr(self.ai_client, 'ai_enabled') and not self.ai_client.ai_enabled:
            logger.warning("🔴 AI is disabled due to previous failures - using rule-based fallbacks")
        
        # Initialize event monitoring system
        monitor_config = MonitorConfig(
            slack_poll_interval=30,
            jira_poll_interval=60,
            health_check_interval=300
        )
        self.event_monitor = EventDrivenMonitor(monitor_config)
        
        # Set up monitoring
        self.event_monitor.add_slack_monitor(self.slack_client)
        self.event_monitor.add_jira_monitor(self.jira_client, self.project_key)
        
        # Register event handlers
        self._register_event_handlers()
        
        # Agent context for state machine
        self.agent_context = AgentContext(
            agent_id="enhanced_agent_ian",
            project_key=self.project_key,
            current_stories=[],
            recent_changes=[],
            last_activity=datetime.now(),
            mode=AgentMode.REACTIVE
        )
        
        logger.info(f"🚀 Enhanced AgentIan initialized with flexible architecture")
        
    def _register_event_handlers(self):
        """Register event handlers with the monitoring system"""
        
        # Slack message handler
        self.event_monitor.register_event_handler(
            EventType.SLACK_MESSAGE,
            self._handle_slack_message,
            priority=1
        )
        
        # Backlog change handler
        self.event_monitor.register_event_handler(
            EventType.BACKLOG_CHANGE,
            self._handle_backlog_change,
            priority=2
        )
        
        # Health check handler
        self.event_monitor.register_event_handler(
            EventType.TIME_TRIGGER,
            self._handle_health_check,
            priority=5
        )
        
        logger.info("📝 Event handlers registered")
    
    def start_continuous_monitoring(self):
        """Start continuous event-driven monitoring"""
        logger.info("🔄 Starting continuous monitoring mode...")
        
        # Update agent context
        self.agent_context.mode = AgentMode.MONITORING
        self.agent_context.last_activity = datetime.now()
        
        # Start monitoring system
        self.event_monitor.start_monitoring()
        
        # Send startup notification
        self.slack_client.send_message(
            f"🤖 **Enhanced AgentIan Online**\n\n"
            f"**Mode:** Continuous Monitoring\n"
            f"**Features:** \n"
            f"• 🧠 Intelligent context analysis\n"
            f"• 🔄 Dynamic workflow states\n"
            f"• 📊 Real-time backlog monitoring\n"
            f"• 💬 Event-driven Slack responses\n\n"
            f"I'm now actively monitoring for project changes and ready to respond to your messages!",
            username=self.name
        )
        
        logger.info("✅ Enhanced AgentIan is now monitoring continuously")
    
    def stop_monitoring(self):
        """Stop continuous monitoring"""
        logger.info("🛑 Stopping continuous monitoring...")
        
        self.event_monitor.stop_monitoring()
        self.agent_context.mode = AgentMode.IDLE
        
        # Send shutdown notification
        self.slack_client.send_message(
            f"🤖 **Enhanced AgentIan Standby**\n\n"
            f"Continuous monitoring stopped. I'm now in standby mode.\n"
            f"💡 You can still interact with me directly or restart monitoring anytime!",
            username=self.name
        )
        
        logger.info("✅ Enhanced AgentIan monitoring stopped")
    
    def _handle_slack_message(self, event: Event) -> Dict[str, Any]:
        """Handle incoming Slack messages with intelligent analysis"""
        logger.info(f"💬 Processing Slack message: {event.payload.get('text', '')[:50]}...")
        
        # Update agent context
        self.agent_context.last_activity = datetime.now()
        
        # Process through state machine
        result = self.state_machine.process_event(event, self.agent_context)
        
        # Handle based on current state
        current_state = result.get("current_state")
        
        if current_state == "ANALYZING":
            return self._analyze_user_message(event)
        elif current_state == "CLARIFYING":
            return self._handle_clarification_request(event)
        elif current_state == "CREATING_STORIES":
            return self._create_intelligent_stories(event)
        else:
            return self._provide_contextual_response(event)
    
    def _handle_backlog_change(self, event: Event) -> Dict[str, Any]:
        """Handle backlog changes with intelligent analysis"""
        changes = event.payload.get("changes", [])
        logger.info(f"📊 Processing {len(changes)} backlog changes")
        
        # Update agent context with changes
        self.agent_context.recent_changes = changes
        self.agent_context.last_activity = datetime.now()
        
        # Process through state machine
        result = self.state_machine.process_event(event, self.agent_context)
        
        # Analyze impact of changes
        impact_analysis = self._analyze_change_impact(changes)
        
        # Send intelligent update
        if impact_analysis["requires_attention"]:
            message = f"📊 **Backlog Update - Product Owner Review Required**\n\n"
            message += f"**Changes Detected:** {len(changes)}\n"
            
            for change in changes[:3]:  # Show top 3 changes
                change_type = change.get("type", "unknown")
                story_title = change.get("story_title", "Unknown Story")
                
                if change_type == "status_changed":
                    message += f"• **{story_title}**: {change.get('old_status')} → {change.get('new_status')}\n"
                elif change_type == "story_added":
                    message += f"• **New Story**: {story_title}\n"
                elif change_type == "assignment_changed":
                    message += f"• **{story_title}**: Assigned to {change.get('new_assignee', 'Unassigned')}\n"
            
            if len(changes) > 3:
                message += f"• ...and {len(changes) - 3} more changes\n"
            
            message += f"\n**Impact Analysis:**\n{impact_analysis['summary']}\n\n"
            
            if impact_analysis["recommended_actions"]:
                message += f"**Recommended Actions:**\n"
                for action in impact_analysis["recommended_actions"]:
                    message += f"• {action}\n"
            
            self.slack_client.send_message(message, username=self.name)
        
        return {"changes_processed": len(changes), "attention_required": impact_analysis["requires_attention"]}
    
    def _handle_health_check(self, event: Event) -> Dict[str, Any]:
        """Handle periodic health checks"""
        logger.debug("💓 Performing health check")
        
        # Check if we need to do anything
        time_since_activity = datetime.now() - self.agent_context.last_activity
        
        if time_since_activity.total_seconds() > 3600:  # 1 hour of inactivity
            # Send idle status update
            status_message = f"💤 **Agent Status: Monitoring**\n\n"
            status_message += f"**Last Activity:** {time_since_activity.total_seconds() // 60:.0f} minutes ago\n"
            status_message += f"**Current State:** {self.state_machine.current_state}\n"
            status_message += f"**Queue Size:** {event.payload.get('queue_size', 0)}\n\n"
            status_message += f"✅ All systems operational - standing by for work"
            
            self.slack_client.send_message(status_message, username=self.name)
        
        return {"status": "healthy", "last_activity": self.agent_context.last_activity.isoformat()}
    
    def _analyze_user_message(self, event: Event) -> Dict[str, Any]:
        """Analyze user message with intelligent context awareness"""
        message_text = event.payload.get("text", "")
        
        # Get current project context
        project_context = self._build_project_context()
        
        # Use intelligent context analyzer
        analysis = self.context_analyzer.analyze_project_context(message_text, project_context)
        
        # Send intelligent response based on analysis
        if analysis.needs_clarification:
            response = f"🧠 **Intelligent Analysis Complete**\n\n"
            response += f"**Understanding:** {analysis.reasoning}\n\n"
            response += f"**Smart Questions ({len(analysis.clarification_questions)}):**\n"
            
            for i, question in enumerate(analysis.clarification_questions, 1):
                response += f"{i}. {question}\n"
            
            response += f"\n💡 **Confidence:** {analysis.confidence_score:.1%}\n"
            response += f"**Next Actions:** {', '.join(analysis.suggested_actions)}\n\n"
            response += f"Please provide details so I can create the most relevant user stories!"
            
            # Wait for user response before proceeding
            timestamp = self.slack_client.send_message(response, add_tracking=True, username=self.name)
            if timestamp:
                user_response = self.slack_client.wait_for_response(timestamp, timeout=300)
                if user_response:
                    # Process the clarification response
                    enhanced_response = self._enhance_human_response(user_response)
                    clarification_text = enhanced_response.get('enhanced_text', user_response)
                    
                    # Create stories with clarification
                    asyncio.create_task(self._create_stories_from_analysis(f"{message_text}\n\nClarification: {clarification_text}", analysis))
                    return {"analysis_complete": True, "needs_clarification": True, "clarification_received": True}
            
            return {"analysis_complete": True, "needs_clarification": True, "awaiting_response": True}
            
        else:
            response = f"✅ **Ready to Proceed**\n\n"
            response += f"**Analysis:** {analysis.reasoning}\n"
            response += f"**Confidence:** {analysis.confidence_score:.1%}\n\n"
            response += f"I have enough context to create intelligent user stories. Proceeding now..."
            
            # Trigger story creation
            asyncio.create_task(self._create_stories_from_analysis(message_text, analysis))
        
        self.slack_client.send_message(response, username=self.name)
        
        return {"analysis_complete": True, "needs_clarification": analysis.needs_clarification}
    
    def _analyze_change_impact(self, changes: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze the impact of backlog changes"""
        
        high_impact_changes = []
        recommendations = []
        
        for change in changes:
            change_type = change.get("type")
            
            if change_type == "status_changed":
                new_status = change.get("new_status", "").lower()
                
                if "done" in new_status or "completed" in new_status:
                    high_impact_changes.append(change)
                    recommendations.append(f"Review completed story: {change.get('story_title')}")
                    
                elif "in progress" in new_status:
                    recommendations.append(f"Monitor progress: {change.get('story_title')}")
                    
            elif change_type == "story_added":
                high_impact_changes.append(change)
                recommendations.append(f"Review new story for clarity: {change.get('story_title')}")
        
        requires_attention = len(high_impact_changes) > 0
        
        summary = f"Detected {len(changes)} changes"
        if high_impact_changes:
            summary += f", {len(high_impact_changes)} require product owner attention"
        else:
            summary += ", no immediate action required"
        
        return {
            "requires_attention": requires_attention,
            "high_impact_count": len(high_impact_changes),
            "summary": summary,
            "recommended_actions": recommendations[:3]  # Top 3 recommendations
        }
    
    def _build_project_context(self) -> ProjectContext:
        """Build current project context for analysis"""
        try:
            # Get current stories
            stories = self.jira_client.get_user_stories(self.project_key)
            story_data = []
            
            if stories:
                for story in stories:
                    story_data.append({
                        "title": story.summary,
                        "description": story.description or "",
                        "status": story.status,
                        "key": story.key
                    })
            
            # Get project details
            project = self.jira_client.get_project_details(self.project_key)
            project_name = project.get("name", "Unknown Project") if project else "Unknown Project"
            
            return ProjectContext(
                project_key=self.project_key,
                project_name=project_name,
                existing_stories=story_data,
                recent_changes=self.agent_context.recent_changes,
                last_activity=self.agent_context.last_activity
            )
            
        except Exception as e:
            logger.error(f"Error building project context: {e}")
            return ProjectContext(
                project_key=self.project_key,
                project_name="Unknown Project",
                existing_stories=[],
                recent_changes=[]
            )
    
    async def _create_stories_from_analysis(self, project_goal: str, analysis) -> Dict[str, Any]:
        """Create intelligent user stories based on analysis"""
        try:
            # Use intelligent story generation instead of hardcoded logic
            stories = await self._generate_intelligent_stories(project_goal, analysis)
            
            # Filter out stories that already exist
            filtered_stories = self._filter_existing_stories(stories)
            
            if len(filtered_stories) == 0:
                no_new_message = f"✅ **Project Analysis Complete**\n\n"
                no_new_message += f"**Analysis:** {analysis.reasoning}\n"
                no_new_message += f"**Result:** All necessary stories already exist in your backlog\n"
                no_new_message += f"**Existing Stories:** {len(analysis.project_insights.get('backlog_analysis', {}).get('story_count', 0))}\n\n"
                no_new_message += f"💡 **Recommendation:** Your project backlog is well-defined. Ready for development!"
                
                self.slack_client.send_message(no_new_message, username=self.name)
                return {"stories_created": 0, "success": True, "reason": "no_new_stories_needed"}
            
            # Create in Jira
            created_stories = []
            for story in filtered_stories:
                try:
                    created_story = self.jira_client.create_user_story(
                        project_key=self.project_key,
                        summary=story["title"],
                        description=story["description"]
                    )
                    if created_story:
                        created_stories.append(created_story)
                        logger.info(f"✅ Created intelligent story: {story['title']}")
                except Exception as e:
                    logger.error(f"Error creating story: {e}")
            
            # Send intelligent completion message
            completion_message = f"🧠 **Intelligent Story Creation Complete**\n\n"
            completion_message += f"**Context Analysis:** {analysis.reasoning}\n"
            completion_message += f"**Project Type Detected:** {analysis.project_insights.get('project_type', 'general')}\n"
            completion_message += f"**New Stories Created:** {len(created_stories)}\n"
            completion_message += f"**Existing Stories:** {len(stories) - len(filtered_stories)} (skipped to avoid duplicates)\n\n"
            
            if created_stories:
                completion_message += f"**New Stories:**\n"
                for i, story in enumerate(filtered_stories, 1):
                    completion_message += f"{i}. {story['title']}\n"
            
            completion_message += f"\n✅ All stories are context-aware and optimized for your project!"
            
            self.slack_client.send_message(completion_message, username=self.name)
            
            return {"stories_created": len(created_stories), "success": True, "analysis_used": True}
            
        except Exception as e:
            logger.error(f"Error in intelligent story creation: {e}")
            error_message = f"❌ **Intelligent Story Creation Error**\n\nEncountered an issue: {e}\n\nFalling back to basic story generation."
            self.slack_client.send_message(error_message, username=self.name)
            
            # Fallback to basic generation
            return await self._create_basic_stories_fallback(project_goal)
    
    async def _generate_intelligent_stories(self, project_goal: str, analysis) -> List[Dict[str, Any]]:
        """Generate truly intelligent stories based on context analysis"""
        logger.info("🧠 Generating intelligent stories using context analysis...")
        
        project_insights = analysis.project_insights
        project_type = project_insights.get('project_type', 'general')
        backlog_analysis = project_insights.get('backlog_analysis', {})
        knowledge_gaps = project_insights.get('knowledge_gaps', [])
        
        # Use AI if available for intelligent generation
        if self.ai_client:
            try:
                ai_stories = self.ai_client.generate_user_stories(
                    project_goal, 
                    context_info=f"Project type: {project_type}, Existing stories: {backlog_analysis.get('story_count', 0)}, Gaps: {knowledge_gaps}"
                )
                
                if ai_stories:
                    logger.info(f"✅ Generated {len(ai_stories)} AI-powered intelligent stories")
                    return self._format_ai_stories(ai_stories)
            except Exception as e:
                logger.warning(f"AI story generation failed, using context-aware fallback: {e}")
        
        # Context-aware fallback generation
        return self._generate_context_aware_stories(project_goal, project_type, backlog_analysis, knowledge_gaps)
    
    def _generate_context_aware_stories(self, project_goal: str, project_type: str, backlog_analysis: Dict, knowledge_gaps: List[str]) -> List[Dict[str, Any]]:
        """Generate context-aware stories based on project type and existing backlog"""
        logger.info(f"🎯 Generating context-aware stories for {project_type}")
        
        stories = []
        existing_areas = set(backlog_analysis.get('coverage_areas', []))
        
        # Basic application - minimal stories
        if project_type == "basic_application":
            if "core_features" not in existing_areas:
                stories.append({
                    "title": f"Core Functionality for {project_goal.split()[0] if project_goal else 'Basic'} Application",
                    "description": f"As a user, I want to access the main functionality of this basic application so that I can accomplish my primary tasks.\n\n**Project Context:** {project_goal}\n\n**Acceptance Criteria:**\n- Application loads successfully\n- Core features are accessible\n- Basic user interface is functional"
                })
            
            if "ui_ux" not in existing_areas:
                stories.append({
                    "title": "Simple User Interface",
                    "description": f"As a user, I want a clean, simple interface so that I can easily navigate the application.\n\n**Project Context:** Basic application focused on simplicity\n\n**Acceptance Criteria:**\n- Interface is intuitive and easy to use\n- Navigation is clear and logical\n- Application is responsive on different screen sizes"
                })
        
        # E-commerce application
        elif project_type == "e-commerce_web_app":
            if "core_features" not in existing_areas:
                stories.append({
                    "title": "Product Catalog Management",
                    "description": f"As a customer, I want to browse and search products so that I can find items to purchase.\n\n**Project Context:** {project_goal}\n\n**Acceptance Criteria:**\n- Products are displayed with images and details\n- Search and filter functionality works\n- Product categories are organized logically"
                })
                
                stories.append({
                    "title": "Shopping Cart Functionality",
                    "description": f"As a customer, I want to add items to a cart and manage my selections so that I can purchase multiple items.\n\n**Acceptance Criteria:**\n- Items can be added to cart\n- Cart quantities can be updated\n- Cart persists across sessions"
                })
        
        # API service
        elif project_type == "api_service":
            if "api" not in existing_areas:
                stories.append({
                    "title": "REST API Endpoints",
                    "description": f"As a developer, I want well-defined REST API endpoints so that I can integrate with the service.\n\n**Project Context:** {project_goal}\n\n**Acceptance Criteria:**\n- API follows REST conventions\n- Endpoints are documented\n- Response format is consistent"
                })
            
            if "authentication" not in existing_areas and "missing_authentication" in knowledge_gaps:
                stories.append({
                    "title": "API Authentication",
                    "description": f"As a developer, I want secure API authentication so that only authorized users can access the API.\n\n**Acceptance Criteria:**\n- Authentication mechanism is implemented\n- API keys or tokens are validated\n- Unauthorized access is blocked"
                })
        
        # General web application
        else:
            if "core_features" not in existing_areas:
                stories.append({
                    "title": "Main Application Features",
                    "description": f"As a user, I want access to the main features described in the project requirements so that I can accomplish my goals.\n\n**Project Context:** {project_goal}\n\n**Acceptance Criteria:**\n- Core functionality is implemented\n- Features work as specified\n- User experience is smooth and intuitive"
                })
        
        # Only add authentication if it's missing and needed (not for basic apps)
        if project_type != "basic_application" and "authentication" not in existing_areas and "missing_authentication" in knowledge_gaps:
            stories.append({
                "title": "User Authentication System",
                "description": f"As a user, I want to create an account and log in securely so that I can access personalized features.\n\n**Project Context:** {project_goal}\n\n**Acceptance Criteria:**\n- Users can register new accounts\n- Secure login/logout functionality\n- Password reset capability"
            })
        
        logger.info(f"📝 Generated {len(stories)} context-aware stories (avoided {len(existing_areas)} existing areas)")
        return stories
    
    def _filter_existing_stories(self, new_stories: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Filter out stories that already exist in the backlog"""
        try:
            existing_stories = self.jira_client.get_user_stories(self.project_key) or []
            existing_titles = {story.summary.lower() for story in existing_stories}
            
            filtered_stories = []
            for story in new_stories:
                story_title_lower = story["title"].lower()
                
                # Check for exact matches or very similar titles
                is_duplicate = any(
                    self._is_similar_title(story_title_lower, existing_title)
                    for existing_title in existing_titles
                )
                
                if not is_duplicate:
                    filtered_stories.append(story)
                else:
                    logger.info(f"🔄 Skipping duplicate story: {story['title']}")
            
            logger.info(f"📊 Filtered {len(new_stories)} stories down to {len(filtered_stories)} unique stories")
            return filtered_stories
            
        except Exception as e:
            logger.error(f"Error filtering existing stories: {e}")
            return new_stories  # Return all if filtering fails
    
    def _is_similar_title(self, title1: str, title2: str) -> bool:
        """Check if two story titles are similar enough to be considered duplicates"""
        # Simple similarity check - can be enhanced with fuzzy matching
        title1_words = set(title1.split())
        title2_words = set(title2.split())
        
        # If they share more than 70% of words, consider them similar
        intersection = title1_words.intersection(title2_words)
        union = title1_words.union(title2_words)
        
        if len(union) == 0:
            return False
            
        similarity = len(intersection) / len(union)
        return similarity > 0.7
    
    async def _create_basic_stories_fallback(self, project_goal: str) -> Dict[str, Any]:
        """Fallback to basic story creation if intelligent generation fails"""
        try:
            stories = self._generate_user_stories(project_goal)  # Use parent method
            filtered_stories = self._filter_existing_stories(stories)
            
            created_stories = []
            for story in filtered_stories:
                created_story = self.jira_client.create_user_story(
                    project_key=self.project_key,
                    summary=story["title"],
                    description=story["description"]
                )
                if created_story:
                    created_stories.append(created_story)
            
            return {"stories_created": len(created_stories), "success": True, "fallback_used": True}
            
        except Exception as e:
            logger.error(f"Even fallback story creation failed: {e}")
            return {"success": False, "error": str(e)}
    
    def _format_ai_stories(self, ai_stories: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Format AI-generated stories to the expected format"""
        formatted_stories = []
        
        for story in ai_stories:
            # Build comprehensive description
            description = story.get('user_story', story.get('description', ''))
            
            # Add acceptance criteria if available
            if story.get('acceptance_criteria'):
                description += "\n\n**Acceptance Criteria:**\n"
                for criteria in story['acceptance_criteria']:
                    description += f"- {criteria}\n"
            
            # Add story points and priority info
            if story.get('story_points'):
                description += f"\n**Story Points:** {story['story_points']}"
            if story.get('priority'):
                description += f"\n**Priority:** {story['priority']}"
            
            formatted_stories.append({
                "title": story.get('title', 'AI Generated Story'),
                "description": description
            })
        
        return formatted_stories
    
    def _provide_contextual_response(self, event: Event) -> Dict[str, Any]:
        """Provide contextual response based on current state"""
        message = event.payload.get("text", "").lower()
        
        # Analyze message intent
        if any(word in message for word in ["status", "update", "progress"]):
            return self._provide_status_update()
        elif any(word in message for word in ["help", "what can you do"]):
            return self._provide_capabilities()
        elif any(word in message for word in ["create", "new", "story", "feature"]):
            return self._handle_creation_request(event)
        else:
            return self._provide_general_response(event)
    
    def _provide_status_update(self) -> Dict[str, Any]:
        """Provide intelligent status update"""
        status = self.get_intelligent_project_status()
        
        message = f"📊 **Current Project Status**\n\n"
        
        if status.get("success"):
            message += f"**Project:** {status['project_name']}\n"
            message += f"**Phase:** {status['phase']}\n" 
            message += f"**Summary:** {status['summary']}\n"
            message += f"**Agent State:** {self.state_machine.current_state}\n\n"
            message += f"**Recent Activity:** {len(self.agent_context.recent_changes)} changes in last check\n"
        else:
            message += f"**Status:** Unable to retrieve project details\n"
            message += f"**Agent State:** {self.state_machine.current_state}\n"
        
        message += f"\n💡 **Available:** Ready for new requests or project updates"
        
        self.slack_client.send_message(message, username=self.name)
        return {"status_provided": True}
    
    def get_enhanced_capabilities_summary(self) -> str:
        """Get enhanced capabilities summary"""
        return f"""🤖 **Enhanced AgentIan - Intelligent Product Owner Agent**

**🧠 Intelligent Features:**
• Context-aware project analysis with AI
• Smart question generation (no generic questions!)
• Dynamic workflow states based on project context
• Real-time backlog monitoring and change detection
• Collaborative multi-agent architecture ready

**🔄 Event-Driven Operations:**
• Continuous Slack monitoring for new messages
• Automatic Jira backlog change detection
• Intelligent idle state management
• Priority-based event processing
• Health checks and status reporting

**💬 Human-like Interactions:**
• Contextual responses based on project state
• Intelligent clarification requests
• Progress-aware status updates  
• Proactive change notifications
• Collaborative team communication

**⚙️ Flexible Architecture:**
• Configurable state machine workflows
• Event handler registration system
• Multi-agent collaboration framework
• Extensible monitoring system
• AI-powered decision making

**🎯 Smart Project Management:**
• Project type detection and adaptation
• Context-aware story generation
• Intelligent backlog gap analysis
• Automated priority recommendations
• Continuous improvement suggestions

Ready to transform your project management with intelligent automation!"""

    def get_monitoring_status(self) -> Dict[str, Any]:
        """Get current monitoring system status"""
        base_status = self.event_monitor.get_monitoring_status()
        
        base_status.update({
            "agent_state": self.state_machine.current_state,
            "agent_mode": self.agent_context.mode.value,
            "last_activity": self.agent_context.last_activity.isoformat(),
            "recent_changes": len(self.agent_context.recent_changes)
        })
        
        return base_status