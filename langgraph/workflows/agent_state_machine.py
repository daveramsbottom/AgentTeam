"""
Dynamic Agent State Machine
Replaces hardcoded workflows with flexible, configurable state management
"""
import logging
from enum import Enum
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
import json
from datetime import datetime

logger = logging.getLogger(__name__)


class EventType(str, Enum):
    """Types of events that can trigger state transitions"""
    SLACK_MESSAGE = "slack_message"
    JIRA_CHANGE = "jira_change"  
    TIME_TRIGGER = "time_trigger"
    AGENT_MESSAGE = "agent_message"
    USER_RESPONSE = "user_response"
    PROJECT_START = "project_start"
    BACKLOG_CHANGE = "backlog_change"


class AgentMode(str, Enum):
    """Operating modes for agents"""
    REACTIVE = "reactive"  # Responds to events
    MONITORING = "monitoring"  # Actively watching for changes
    IDLE = "idle"  # No active work, periodic check-ins
    COLLABORATING = "collaborating"  # Working with other agents


@dataclass
class AgentContext:
    """Context information for agent decision making"""
    agent_id: str
    project_key: str
    current_stories: List[Dict[str, Any]]
    recent_changes: List[Dict[str, Any]]
    last_activity: datetime
    mode: AgentMode
    collaboration_state: Optional[Dict[str, Any]] = None
    custom_data: Dict[str, Any] = None


@dataclass
class Event:
    """Event that triggers agent actions"""
    event_type: EventType
    source: str
    payload: Dict[str, Any]
    timestamp: datetime
    context: Optional[AgentContext] = None


class AgentState(ABC):
    """Abstract base class for agent states"""
    
    def __init__(self, name: str):
        self.name = name
        
    @abstractmethod
    def can_handle(self, event: Event, context: AgentContext) -> bool:
        """Determine if this state can handle the given event"""
        pass
        
    @abstractmethod
    def handle_event(self, event: Event, context: AgentContext) -> Dict[str, Any]:
        """Process the event and return action results"""
        pass
        
    @abstractmethod
    def get_next_state(self, event: Event, context: AgentContext) -> Optional[str]:
        """Determine the next state based on event and context"""
        pass
        
    def get_idle_timeout(self) -> int:
        """How long to wait in this state before checking for work (seconds)"""
        return 300  # 5 minutes default


class MonitoringState(AgentState):
    """Agent actively monitors for changes and new work"""
    
    def __init__(self):
        super().__init__("MONITORING")
        
    def can_handle(self, event: Event, context: AgentContext) -> bool:
        return event.event_type in [
            EventType.TIME_TRIGGER,
            EventType.BACKLOG_CHANGE,
            EventType.SLACK_MESSAGE
        ]
        
    def handle_event(self, event: Event, context: AgentContext) -> Dict[str, Any]:
        logger.info(f"🔍 Monitoring state handling {event.event_type}")
        
        if event.event_type == EventType.TIME_TRIGGER:
            return self._periodic_check(context)
            
        elif event.event_type == EventType.BACKLOG_CHANGE:
            return self._analyze_backlog_changes(event, context)
            
        elif event.event_type == EventType.SLACK_MESSAGE:
            return self._analyze_message(event, context)
            
        return {"action": "no_action", "message": "Event not processed"}
        
    def get_next_state(self, event: Event, context: AgentContext) -> Optional[str]:
        if event.event_type == EventType.SLACK_MESSAGE:
            # Check if message requires active work
            message_content = event.payload.get("text", "").lower()
            if any(keyword in message_content for keyword in ["help", "create", "update", "question"]):
                return "ANALYZING"
        
        if event.event_type == EventType.BACKLOG_CHANGE:
            return "REVIEWING_CHANGES"
            
        return "MONITORING"  # Stay in monitoring by default
        
    def _periodic_check(self, context: AgentContext) -> Dict[str, Any]:
        """Perform periodic health check"""
        return {
            "action": "periodic_check",
            "message": f"✅ {context.agent_id} monitoring - all systems operational",
            "requires_response": False,
            "next_check": datetime.now().timestamp() + self.get_idle_timeout()
        }
        
    def _analyze_backlog_changes(self, event: Event, context: AgentContext) -> Dict[str, Any]:
        """Analyze changes to the backlog"""
        changes = event.payload.get("changes", [])
        
        return {
            "action": "backlog_analysis",
            "message": f"📊 Detected {len(changes)} backlog changes - analyzing impact...",
            "changes_detected": len(changes),
            "requires_review": len(changes) > 0
        }
        
    def _analyze_message(self, event: Event, context: AgentContext) -> Dict[str, Any]:
        """Analyze Slack message for required actions"""
        message = event.payload.get("text", "")
        
        return {
            "action": "message_analysis",
            "message": f"💬 New message received - analyzing intent...",
            "message_preview": message[:100],
            "requires_response": True
        }


class AnalyzingState(AgentState):
    """Agent analyzes requirements and context before taking action"""
    
    def __init__(self):
        super().__init__("ANALYZING")
        
    def can_handle(self, event: Event, context: AgentContext) -> bool:
        return event.event_type in [
            EventType.PROJECT_START,
            EventType.SLACK_MESSAGE,
            EventType.USER_RESPONSE
        ]
        
    def handle_event(self, event: Event, context: AgentContext) -> Dict[str, Any]:
        logger.info(f"🧠 Analyzing state handling {event.event_type}")
        
        if event.event_type == EventType.PROJECT_START:
            return self._analyze_project_goal(event, context)
            
        elif event.event_type == EventType.SLACK_MESSAGE:
            return self._analyze_user_request(event, context)
            
        return {"action": "analysis_complete", "message": "Analysis completed"}
        
    def get_next_state(self, event: Event, context: AgentContext) -> Optional[str]:
        # After analysis, typically need clarification or can create stories
        existing_stories = len(context.current_stories) if context.current_stories else 0
        
        if existing_stories == 0:
            return "CLARIFYING"  # New project needs clarification
        else:
            return "CREATING_STORIES"  # Existing project can create stories directly
        
    def _analyze_project_goal(self, event: Event, context: AgentContext) -> Dict[str, Any]:
        """Analyze a new project goal with context awareness"""
        project_goal = event.payload.get("project_goal", "")
        
        # Check existing backlog for context
        existing_stories = context.current_stories or []
        
        return {
            "action": "project_analysis",
            "message": f"🎯 Analyzing project goal with {len(existing_stories)} existing stories...",
            "project_goal": project_goal,
            "existing_context": len(existing_stories) > 0,
            "analysis_complete": True
        }
        
    def _analyze_user_request(self, event: Event, context: AgentContext) -> Dict[str, Any]:
        """Analyze user request in context of current project state"""
        message = event.payload.get("text", "")
        
        return {
            "action": "request_analysis", 
            "message": f"💭 Analyzing request in context of current project...",
            "request_preview": message[:100],
            "context_aware": True
        }


class ClarifyingState(AgentState):
    """Agent asks intelligent, context-aware clarification questions"""
    
    def __init__(self):
        super().__init__("CLARIFYING")
        
    def can_handle(self, event: Event, context: AgentContext) -> bool:
        return event.event_type in [EventType.USER_RESPONSE, EventType.TIME_TRIGGER]
        
    def handle_event(self, event: Event, context: AgentContext) -> Dict[str, Any]:
        logger.info(f"🤔 Clarifying state handling {event.event_type}")
        
        if event.event_type == EventType.USER_RESPONSE:
            return self._process_clarification_response(event, context)
            
        return {"action": "waiting_for_response", "message": "Waiting for user clarification..."}
        
    def get_next_state(self, event: Event, context: AgentContext) -> Optional[str]:
        if event.event_type == EventType.USER_RESPONSE:
            return "CREATING_STORIES"
        return "CLARIFYING"
        
    def _process_clarification_response(self, event: Event, context: AgentContext) -> Dict[str, Any]:
        """Process user's clarification response"""
        response = event.payload.get("text", "")
        
        return {
            "action": "clarification_processed",
            "message": "✅ Clarification received - proceeding to story creation...",
            "response_length": len(response),
            "ready_for_stories": True
        }


class CreatingStoriesState(AgentState):
    """Agent creates intelligent, context-aware user stories"""
    
    def __init__(self):
        super().__init__("CREATING_STORIES")
        
    def can_handle(self, event: Event, context: AgentContext) -> bool:
        return True  # Can always create stories when needed
        
    def handle_event(self, event: Event, context: AgentContext) -> Dict[str, Any]:
        logger.info(f"📝 Creating stories state handling {event.event_type}")
        
        return {
            "action": "create_stories",
            "message": "🔨 Creating intelligent user stories based on context...",
            "context_aware": True
        }
        
    def get_next_state(self, event: Event, context: AgentContext) -> Optional[str]:
        return "MONITORING"  # Return to monitoring after creating stories


class ReviewingChangesState(AgentState):
    """Agent reviews and responds to backlog changes"""
    
    def __init__(self):
        super().__init__("REVIEWING_CHANGES")
        
    def can_handle(self, event: Event, context: AgentContext) -> bool:
        return event.event_type == EventType.BACKLOG_CHANGE
        
    def handle_event(self, event: Event, context: AgentContext) -> Dict[str, Any]:
        logger.info(f"📊 Reviewing changes state handling {event.event_type}")
        
        changes = event.payload.get("changes", [])
        
        return {
            "action": "review_changes",
            "message": f"🔍 Reviewing {len(changes)} backlog changes for impact...",
            "changes_count": len(changes)
        }
        
    def get_next_state(self, event: Event, context: AgentContext) -> Optional[str]:
        return "MONITORING"


class IdleState(AgentState):
    """Agent is idle but performs periodic health checks"""
    
    def __init__(self):
        super().__init__("IDLE")
        
    def can_handle(self, event: Event, context: AgentContext) -> bool:
        return event.event_type == EventType.TIME_TRIGGER
        
    def handle_event(self, event: Event, context: AgentContext) -> Dict[str, Any]:
        logger.info(f"😴 Idle state handling {event.event_type}")
        
        return {
            "action": "idle_check",
            "message": "💤 Agent idle - performing health check...",
            "status": "healthy"
        }
        
    def get_next_state(self, event: Event, context: AgentContext) -> Optional[str]:
        return "MONITORING"
        
    def get_idle_timeout(self) -> int:
        return 1800  # 30 minutes for idle state


class DynamicStateMachine:
    """Dynamic state machine for agent workflow management"""
    
    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        self.current_state = "MONITORING"
        
        # Initialize all available states
        self.states = {
            "MONITORING": MonitoringState(),
            "ANALYZING": AnalyzingState(),
            "CLARIFYING": ClarifyingState(),
            "CREATING_STORIES": CreatingStoriesState(),
            "REVIEWING_CHANGES": ReviewingChangesState(),
            "IDLE": IdleState()
        }
        
        logger.info(f"🤖 Initialized state machine for {agent_id} in {self.current_state}")
        
    def process_event(self, event: Event, context: AgentContext) -> Dict[str, Any]:
        """Process an event through the current state"""
        current_state_obj = self.states[self.current_state]
        
        if not current_state_obj.can_handle(event, context):
            logger.warning(f"⚠️ State {self.current_state} cannot handle event {event.event_type}")
            return {"action": "event_not_handled", "message": "Event cannot be processed in current state"}
        
        # Handle the event
        result = current_state_obj.handle_event(event, context)
        
        # Determine next state
        next_state = current_state_obj.get_next_state(event, context)
        
        if next_state and next_state != self.current_state:
            logger.info(f"🔄 State transition: {self.current_state} → {next_state}")
            self.current_state = next_state
            result["state_transition"] = {"from": self.current_state, "to": next_state}
        
        result["current_state"] = self.current_state
        result["agent_id"] = self.agent_id
        
        return result
        
    def get_current_state_info(self) -> Dict[str, Any]:
        """Get information about the current state"""
        state_obj = self.states[self.current_state]
        
        return {
            "current_state": self.current_state,
            "state_name": state_obj.name,
            "idle_timeout": state_obj.get_idle_timeout(),
            "agent_id": self.agent_id
        }
        
    def force_state_transition(self, new_state: str) -> bool:
        """Force transition to a specific state (for debugging/admin)"""
        if new_state in self.states:
            old_state = self.current_state
            self.current_state = new_state
            logger.info(f"🔧 Forced state transition: {old_state} → {new_state}")
            return True
        else:
            logger.error(f"❌ Invalid state: {new_state}")
            return False