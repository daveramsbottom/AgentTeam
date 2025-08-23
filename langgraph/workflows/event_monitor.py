"""
Event-Driven Monitoring System
Enables continuous agent operation with intelligent event detection and processing
"""
import logging
import asyncio
import threading
from typing import Dict, Any, List, Callable, Optional
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import json
from queue import Queue, Empty
from enum import Enum

from .agent_state_machine import Event, EventType, AgentContext, AgentMode

logger = logging.getLogger(__name__)


@dataclass
class MonitorConfig:
    """Configuration for different monitoring activities"""
    slack_poll_interval: int = 30  # seconds
    jira_poll_interval: int = 60   # seconds  
    health_check_interval: int = 300  # 5 minutes
    idle_timeout: int = 1800  # 30 minutes
    max_events_per_cycle: int = 10


@dataclass
class EventHandler:
    """Event handler registration"""
    event_type: EventType
    handler_function: Callable
    priority: int = 1  # Lower number = higher priority
    conditions: Dict[str, Any] = field(default_factory=dict)


class EventQueue:
    """Thread-safe event queue with priority handling"""
    
    def __init__(self, max_size: int = 1000):
        self._queue = Queue(maxsize=max_size)
        self._priority_queue = []
        self._lock = threading.Lock()
        
    def add_event(self, event: Event, priority: int = 1):
        """Add event to queue with priority"""
        with self._lock:
            # Add to priority queue for sorting
            self._priority_queue.append((priority, datetime.now(), event))
            self._priority_queue.sort(key=lambda x: (x[0], x[1]))  # Sort by priority, then time
            
            # Move to main queue
            if not self._queue.full():
                # Get highest priority event
                if self._priority_queue:
                    _, _, priority_event = self._priority_queue.pop(0)
                    self._queue.put(priority_event, block=False)
            else:
                logger.warning("Event queue is full - dropping event")
    
    def get_event(self, timeout: float = 1.0) -> Optional[Event]:
        """Get next event from queue"""
        try:
            return self._queue.get(timeout=timeout)
        except Empty:
            return None
    
    def size(self) -> int:
        """Get current queue size"""
        return self._queue.qsize()


class SlackMonitor:
    """Monitors Slack for new messages and events"""
    
    def __init__(self, slack_client, event_queue: EventQueue):
        self.slack_client = slack_client
        self.event_queue = event_queue
        self.last_check = datetime.now()
        self.is_monitoring = False
        
    def start_monitoring(self, poll_interval: int = 30):
        """Start monitoring Slack messages"""
        self.is_monitoring = True
        logger.info(f"🔍 Starting Slack monitoring (poll interval: {poll_interval}s)")
        
        def monitor_loop():
            while self.is_monitoring:
                try:
                    self._check_for_messages()
                    asyncio.sleep(poll_interval)
                except Exception as e:
                    logger.error(f"Slack monitoring error: {e}")
                    asyncio.sleep(poll_interval)
        
        # Run in separate thread
        monitor_thread = threading.Thread(target=monitor_loop, daemon=True)
        monitor_thread.start()
    
    def stop_monitoring(self):
        """Stop monitoring Slack"""
        self.is_monitoring = False
        logger.info("🔍 Stopped Slack monitoring")
    
    def _check_for_messages(self):
        """Check for new Slack messages since last check"""
        try:
            # Get messages since last check
            messages = self.slack_client.get_messages_since(self.last_check)
            
            for message in messages:
                # Filter out bot messages
                if not self._is_human_message(message):
                    continue
                
                # Create event
                event = Event(
                    event_type=EventType.SLACK_MESSAGE,
                    source="slack_monitor",
                    payload={
                        "text": message.get("text", ""),
                        "user": message.get("user", ""),
                        "timestamp": message.get("ts", ""),
                        "channel": message.get("channel", "")
                    },
                    timestamp=datetime.now()
                )
                
                # Add to event queue with high priority
                self.event_queue.add_event(event, priority=1)
                logger.info(f"💬 New Slack message event queued from user {message.get('user', 'unknown')}")
            
            self.last_check = datetime.now()
            
        except Exception as e:
            logger.error(f"Error checking Slack messages: {e}")
    
    def _is_human_message(self, message: Dict[str, Any]) -> bool:
        """Check if message is from a human (not bot)"""
        # Skip bot messages
        if message.get("bot_id") or message.get("subtype") == "bot_message":
            return False
        
        # Skip messages without text
        if not message.get("text"):
            return False
        
        return True


class JiraMonitor:
    """Monitors Jira for backlog changes and updates"""
    
    def __init__(self, jira_client, event_queue: EventQueue, project_key: str):
        self.jira_client = jira_client
        self.event_queue = event_queue
        self.project_key = project_key
        self.last_check = datetime.now()
        self.is_monitoring = False
        self.known_stories = {}  # Cache of known stories
        
    def start_monitoring(self, poll_interval: int = 60):
        """Start monitoring Jira backlog"""
        self.is_monitoring = True
        logger.info(f"📋 Starting Jira monitoring (poll interval: {poll_interval}s)")
        
        # Initialize known stories
        self._update_known_stories()
        
        def monitor_loop():
            while self.is_monitoring:
                try:
                    self._check_for_changes()
                    asyncio.sleep(poll_interval)
                except Exception as e:
                    logger.error(f"Jira monitoring error: {e}")
                    asyncio.sleep(poll_interval)
        
        # Run in separate thread
        monitor_thread = threading.Thread(target=monitor_loop, daemon=True)
        monitor_thread.start()
    
    def stop_monitoring(self):
        """Stop monitoring Jira"""
        self.is_monitoring = False
        logger.info("📋 Stopped Jira monitoring")
    
    def _check_for_changes(self):
        """Check for changes in Jira backlog"""
        try:
            current_stories = self.jira_client.get_user_stories(self.project_key)
            current_story_map = {story.key: story for story in (current_stories or [])}
            
            changes = []
            
            # Check for new stories
            for story_key, story in current_story_map.items():
                if story_key not in self.known_stories:
                    changes.append({
                        "type": "story_added",
                        "story_key": story_key,
                        "story_title": story.summary,
                        "story": story
                    })
            
            # Check for updated stories
            for story_key, story in current_story_map.items():
                if story_key in self.known_stories:
                    old_story = self.known_stories[story_key]
                    
                    # Check for status changes
                    if story.status != old_story.get("status"):
                        changes.append({
                            "type": "status_changed",
                            "story_key": story_key,
                            "story_title": story.summary,
                            "old_status": old_story.get("status"),
                            "new_status": story.status
                        })
                    
                    # Check for assignment changes
                    if story.assigned_to != old_story.get("assigned_to"):
                        changes.append({
                            "type": "assignment_changed", 
                            "story_key": story_key,
                            "story_title": story.summary,
                            "old_assignee": old_story.get("assigned_to"),
                            "new_assignee": story.assigned_to
                        })
            
            # Check for deleted stories
            for story_key in self.known_stories:
                if story_key not in current_story_map:
                    changes.append({
                        "type": "story_deleted",
                        "story_key": story_key,
                        "story_title": self.known_stories[story_key].get("title", "Unknown")
                    })
            
            # Create event if changes detected
            if changes:
                event = Event(
                    event_type=EventType.BACKLOG_CHANGE,
                    source="jira_monitor",
                    payload={
                        "project_key": self.project_key,
                        "changes": changes,
                        "total_stories": len(current_story_map)
                    },
                    timestamp=datetime.now()
                )
                
                self.event_queue.add_event(event, priority=2)
                logger.info(f"📊 Backlog change event queued: {len(changes)} changes detected")
            
            # Update known stories
            self._update_known_stories(current_story_map)
            
        except Exception as e:
            logger.error(f"Error checking Jira changes: {e}")
    
    def _update_known_stories(self, story_map: Optional[Dict[str, Any]] = None):
        """Update the cache of known stories"""
        if story_map is None:
            try:
                stories = self.jira_client.get_user_stories(self.project_key)
                story_map = {story.key: story for story in (stories or [])}
            except Exception as e:
                logger.error(f"Error updating known stories: {e}")
                return
        
        # Convert to simple dict for comparison
        self.known_stories = {
            key: {
                "title": story.summary,
                "status": story.status,
                "assigned_to": story.assigned_to,
                "updated": datetime.now()
            }
            for key, story in story_map.items()
        }


class HealthMonitor:
    """Monitors agent health and triggers periodic checks"""
    
    def __init__(self, event_queue: EventQueue):
        self.event_queue = event_queue
        self.is_monitoring = False
        self.last_health_check = datetime.now()
        
    def start_monitoring(self, check_interval: int = 300):
        """Start health monitoring"""
        self.is_monitoring = True
        logger.info(f"💓 Starting health monitoring (check interval: {check_interval}s)")
        
        def monitor_loop():
            while self.is_monitoring:
                try:
                    self._perform_health_check()
                    asyncio.sleep(check_interval)
                except Exception as e:
                    logger.error(f"Health monitoring error: {e}")
                    asyncio.sleep(check_interval)
        
        # Run in separate thread
        monitor_thread = threading.Thread(target=monitor_loop, daemon=True)
        monitor_thread.start()
    
    def stop_monitoring(self):
        """Stop health monitoring"""
        self.is_monitoring = False
        logger.info("💓 Stopped health monitoring")
    
    def _perform_health_check(self):
        """Perform periodic health check"""
        event = Event(
            event_type=EventType.TIME_TRIGGER,
            source="health_monitor",
            payload={
                "check_type": "health_check",
                "last_check": self.last_health_check.isoformat(),
                "queue_size": self.event_queue.size()
            },
            timestamp=datetime.now()
        )
        
        self.event_queue.add_event(event, priority=5)  # Low priority
        self.last_health_check = datetime.now()
        
        logger.debug("💓 Health check event queued")


class EventDrivenMonitor:
    """Main event-driven monitoring system that coordinates all monitors"""
    
    def __init__(self, config: MonitorConfig):
        self.config = config
        self.event_queue = EventQueue()
        self.event_handlers: List[EventHandler] = []
        self.monitors = {}
        self.is_running = False
        
        # Initialize health monitor
        self.health_monitor = HealthMonitor(self.event_queue)
        
    def add_slack_monitor(self, slack_client):
        """Add Slack monitoring"""
        self.monitors["slack"] = SlackMonitor(slack_client, self.event_queue)
        
    def add_jira_monitor(self, jira_client, project_key: str):
        """Add Jira monitoring"""
        self.monitors["jira"] = JiraMonitor(jira_client, self.event_queue, project_key)
        
    def register_event_handler(self, event_type: EventType, handler_function: Callable, priority: int = 1):
        """Register an event handler"""
        handler = EventHandler(
            event_type=event_type,
            handler_function=handler_function,
            priority=priority
        )
        
        self.event_handlers.append(handler)
        self.event_handlers.sort(key=lambda h: h.priority)  # Sort by priority
        
        logger.info(f"📝 Registered event handler for {event_type} with priority {priority}")
    
    def start_monitoring(self):
        """Start all monitoring systems"""
        if self.is_running:
            logger.warning("Monitoring system already running")
            return
            
        self.is_running = True
        logger.info("🚀 Starting event-driven monitoring system")
        
        # Start all monitors
        if "slack" in self.monitors:
            self.monitors["slack"].start_monitoring(self.config.slack_poll_interval)
            
        if "jira" in self.monitors:
            self.monitors["jira"].start_monitoring(self.config.jira_poll_interval)
            
        self.health_monitor.start_monitoring(self.config.health_check_interval)
        
        # Start event processing loop
        self._start_event_processing()
        
    def stop_monitoring(self):
        """Stop all monitoring systems"""
        if not self.is_running:
            return
            
        self.is_running = False
        logger.info("🛑 Stopping event-driven monitoring system")
        
        # Stop all monitors
        for monitor in self.monitors.values():
            monitor.stop_monitoring()
            
        self.health_monitor.stop_monitoring()
        
    def _start_event_processing(self):
        """Start the main event processing loop"""
        def process_events():
            while self.is_running:
                try:
                    event = self.event_queue.get_event(timeout=1.0)
                    
                    if event:
                        self._process_event(event)
                        
                except Exception as e:
                    logger.error(f"Event processing error: {e}")
        
        # Run event processing in separate thread
        processing_thread = threading.Thread(target=process_events, daemon=True)
        processing_thread.start()
        
        logger.info("🔄 Started event processing loop")
    
    def _process_event(self, event: Event):
        """Process a single event through registered handlers"""
        logger.debug(f"🎯 Processing event: {event.event_type} from {event.source}")
        
        # Find matching handlers
        matching_handlers = [h for h in self.event_handlers if h.event_type == event.event_type]
        
        if not matching_handlers:
            logger.debug(f"No handlers found for event type: {event.event_type}")
            return
        
        # Execute handlers in priority order
        for handler in matching_handlers:
            try:
                result = handler.handler_function(event)
                logger.debug(f"Handler executed successfully: {handler.handler_function.__name__}")
                
                # Log result if provided
                if result:
                    logger.info(f"Handler result: {result}")
                    
            except Exception as e:
                logger.error(f"Handler execution failed: {handler.handler_function.__name__} - {e}")
    
    def get_monitoring_status(self) -> Dict[str, Any]:
        """Get current monitoring system status"""
        return {
            "is_running": self.is_running,
            "event_queue_size": self.event_queue.size(),
            "active_monitors": list(self.monitors.keys()),
            "registered_handlers": len(self.event_handlers),
            "config": {
                "slack_poll_interval": self.config.slack_poll_interval,
                "jira_poll_interval": self.config.jira_poll_interval,
                "health_check_interval": self.config.health_check_interval
            }
        }
    
    def inject_test_event(self, event_type: EventType, payload: Dict[str, Any]):
        """Inject a test event for debugging/testing"""
        test_event = Event(
            event_type=event_type,
            source="test_injection",
            payload=payload,
            timestamp=datetime.now()
        )
        
        self.event_queue.add_event(test_event, priority=0)  # Highest priority
        logger.info(f"🧪 Test event injected: {event_type}")