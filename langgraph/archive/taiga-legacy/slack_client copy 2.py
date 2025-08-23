"""
Enhanced Slack Client for AgentTeam Communication
Handles all Slack API interactions with improved message detection
"""
import time
import random
import logging
import requests
from typing import Dict, List, Any, Optional

logger = logging.getLogger(__name__)


class SlackClient:
    """Slack client for agent communication with humans"""
    
    def __init__(self, bot_token: str, channel_id: str):
        self.bot_token = bot_token
        self.channel_id = channel_id
        self.base_url = "https://slack.com/api"
        self.headers = {
            "Authorization": f"Bearer {bot_token}",
            "Content-Type": "application/json"
        }
        self.current_tracking_code = None
        self.bot_user_id = None
        self._session = requests.Session()
        self._session.headers.update(self.headers)
    
    def _get_bot_user_id(self) -> Optional[str]:
        """Get the bot's user ID for filtering messages"""
        if self.bot_user_id:
            return self.bot_user_id
        
        url = f"{self.base_url}/auth.test"
        try:
            response = self._session.get(url)
            data = response.json()
            
            if data.get("ok"):
                self.bot_user_id = data.get("user_id")
                logger.info(f"🤖 Bot user ID: {self.bot_user_id}")
                return self.bot_user_id
            else:
                logger.error(f"❌ Failed to get bot user ID: {data.get('error')}")
                return None
        except Exception as e:
            logger.error(f"❌ Error getting bot user ID: {e}")
            return None
    
    def _generate_tracking_code(self) -> str:
        """Generate a 4-digit tracking code for message identification"""
        code = f"{random.randint(1000, 9999)}"
        self.current_tracking_code = code
        logger.debug(f"🎯 Generated tracking code: {code}")
        return code
    
    def send_message(self, text: str, add_tracking: bool = False, username: str = "AgentIan") -> Optional[str]:
        """Send a message to the channel and return the timestamp"""
        url = f"{self.base_url}/chat.postMessage"
        
        # Add tracking code if requested
        if add_tracking:
            tracking_code = self._generate_tracking_code()
            text = f"{text}\n\n*[Tracking: {tracking_code}] - Just reply with a new message in this channel, I'll detect it!* 🎯"
        
        payload = {
            "channel": self.channel_id,
            "text": text,
            "username": username,
            "icon_emoji": ":robot_face:"
        }
        
        try:
            response = self._session.post(url, json=payload)
            data = response.json()
            
            if data.get("ok"):
                timestamp = data.get("ts")
                if add_tracking:
                    logger.info(f"✅ Sent Slack message with tracking code {self.current_tracking_code}")
                else:
                    logger.info(f"✅ Sent Slack message to channel")
                return timestamp
            else:
                logger.error(f"❌ Slack API error: {data.get('error')}")
                return None
                
        except Exception as e:
            logger.error(f"❌ Error sending Slack message: {e}")
            return None
    
    def get_recent_messages(self, limit: int = 20) -> List[Dict[str, Any]]:
        """
        Get recent messages from the channel
        
        Args:
            limit: Number of messages to retrieve
            
        Returns:
            List of message dictionaries
        """
        url = f"{self.base_url}/conversations.history"
        params = {
            "channel": self.channel_id,
            "limit": limit
        }
        
        try:
            response = self._session.get(url, params=params)
            data = response.json()
            
            if data.get("ok"):
                messages = data.get("messages", [])
                logger.debug(f"Retrieved {len(messages)} recent messages")
                return messages
            else:
                logger.error(f"Failed to get messages: {data.get('error', 'Unknown error')}")
                return []
                
        except Exception as e:
            logger.error(f"Error getting messages: {e}")
            return []
    
    def get_messages_since(self, timestamp: str) -> List[Dict]:
        """Get messages from the channel since a specific timestamp with improved filtering"""
        url = f"{self.base_url}/conversations.history"
        
        # Get bot user ID for filtering
        bot_user_id = self._get_bot_user_id()
        
        params = {
            "channel": self.channel_id,
            "oldest": timestamp,
            "inclusive": False,
            "limit": 50
        }
        
        try:
            response = self._session.get(url, params=params)
            data = response.json()
            
            if data.get("ok"):
                messages = data.get("messages", [])
                logger.debug(f"📥 Retrieved {len(messages)} total messages since {timestamp}")
                
                # Enhanced filtering logic
                human_messages = []
                for msg in messages:
                    if self._is_human_message(msg, bot_user_id):
                        human_messages.append(msg)
                        logger.debug(f"💬 Human message: {msg.get('text', '')[:50]}...")
                
                if human_messages:
                    logger.info(f"📨 Found {len(human_messages)} human message(s)")
                else:
                    logger.debug(f"🔭 No human messages found since tracking code {self.current_tracking_code}")
                
                return human_messages
            else:
                logger.error(f"❌ Slack API error getting messages: {data.get('error')}")
                return []
                
        except Exception as e:
            logger.error(f"❌ Error getting Slack messages: {e}")
            return []
    
    def _is_human_message(self, msg: Dict, bot_user_id: str = None) -> bool:
        """Determine if a message is from a human user"""
        # Skip messages that are:
        # 1. From bots (has bot_id)
        # 2. From our own bot user
        # 3. Bot message subtype
        # 4. Have no text content
        # 5. Are system messages
        
        excluded_subtypes = [
            "bot_message", "channel_join", "channel_leave", 
            "message_changed", "message_deleted", "thread_broadcast"
        ]
        
        # Get bot user ID if not provided
        if bot_user_id is None:
            bot_user_id = self._get_bot_user_id()
        
        if (msg.get("bot_id") or 
            msg.get("user") == bot_user_id or 
            msg.get("subtype") in excluded_subtypes or
            not msg.get("text") or 
            not msg.get("user")):
            return False
        
        return True
    
    def wait_for_response(self, original_timestamp: str, timeout: int = 300, poll_interval: int = 2) -> Optional[str]:
        """
        Enhanced wait for response with better debugging and detection
        
        Args:
            original_timestamp: Timestamp of the original message
            timeout: Maximum time to wait in seconds
            poll_interval: How often to check for new messages
            
        Returns:
            Response text if found, None otherwise
        """
        start_time = time.time()
        
        logger.info(f"⏳ Waiting for response to message {original_timestamp} (timeout: {timeout}s)")
        logger.info(f"🎯 Tracking code: {self.current_tracking_code}")
        
        while time.time() - start_time < timeout:
            try:
                messages = self.get_recent_messages(limit=10)
                
                # Look for messages after our timestamp from human users
                for message in messages:
                    msg_timestamp = message.get('ts', '')
                    msg_text = message.get('text', '')
                    msg_user = message.get('user', '')
                    
                    logger.debug(f"Checking message: ts={msg_timestamp}, user={msg_user}, text={msg_text[:50]}...")
                    
                    # Check if this message is newer and not from a bot
                    if (msg_timestamp > original_timestamp and 
                        msg_text and 
                        self._is_human_message(message)):
                        
                        logger.info(f"🎉 Found response from user {msg_user}: {msg_text[:100]}...")
                        return msg_text
                
                elapsed = time.time() - start_time
                if elapsed % 30 < poll_interval:  # Log progress every 30 seconds
                    remaining = int(timeout - elapsed)
                    logger.info(f"⏱️ Still waiting for response to {self.current_tracking_code}... ({remaining}s remaining)")
                
                time.sleep(poll_interval)
                
            except Exception as e:
                logger.error(f"❌ Error while waiting for response: {e}")
                time.sleep(poll_interval)
        
        logger.warning(f"⏰ Timeout reached after {timeout} seconds")
        return None
    
    def wait_for_response_legacy(self, question_timestamp: str, timeout: int = 300) -> Optional[str]:
        """Legacy wait for response method (keeping for compatibility)"""
        logger.info(f"⏳ Waiting for human response to tracking code {self.current_tracking_code} (timeout: {timeout}s)...")
        
        start_time = time.time()
        poll_interval = 5  # Check every 5 seconds
        last_progress_time = start_time
        
        while time.time() - start_time < timeout:
            messages = self.get_messages_since(question_timestamp)
            
            if messages:
                # Get the most recent human message
                latest_message = messages[-1]
                response_text = latest_message.get("text", "").strip()
                
                if response_text:
                    logger.info(f"💬 Received human response for tracking {self.current_tracking_code}")
                    return response_text
            
            # Show progress every 30 seconds
            elapsed = time.time() - start_time
            if elapsed - (last_progress_time - start_time) >= 30:
                remaining = int(timeout - elapsed)
                logger.info(f"⌛ Still waiting for response to {self.current_tracking_code}... ({remaining}s remaining)")
                last_progress_time = time.time()
            
            time.sleep(poll_interval)
        
        logger.warning(f"⏰ Timeout waiting for human response to tracking code {self.current_tracking_code} after {timeout}s")
        return None
    
    def test_response_waiting(self) -> Dict[str, Any]:
        """
        Test method to verify response waiting functionality
        """
        logger.info("🧪 Testing Slack response waiting...")
        
        test_message = "🧪 **Test Message - Please Reply!**\n\nThis is a test to verify that I can detect your responses. Please reply with anything!"
        
        timestamp = self.send_message(test_message, add_tracking=True)
        
        if not timestamp:
            return {"success": False, "error": "Failed to send test message"}
        
        logger.info(f"📤 Test message sent with timestamp: {timestamp}")
        logger.info("⏳ Waiting 30 seconds for a response...")
        
        response = self.wait_for_response(timestamp, timeout=30)
        
        result = {
            "success": True,
            "timestamp": timestamp,
            "tracking_code": self.current_tracking_code,
            "response_received": response is not None,
            "response_text": response if response else "No response received"
        }
        
        status_msg = "✅ Response detection working!" if response else "❌ No response detected"
        self.send_message(f"🧪 Test complete: {status_msg}")
        
        return result
    
    def test_connection(self) -> Dict[str, Any]:
        """Test Slack connection and bot permissions"""
        try:
            # Test auth
            auth_response = self._session.get(f"{self.base_url}/auth.test")
            auth_data = auth_response.json()
            
            if not auth_data.get("ok"):
                return {"success": False, "error": f"Auth failed: {auth_data.get('error')}"}
            
            # Test channel access
            channel_response = self._session.get(
                f"{self.base_url}/conversations.info",
                params={"channel": self.channel_id}
            )
            channel_data = channel_response.json()
            
            if not channel_data.get("ok"):
                return {"success": False, "error": f"Channel access failed: {channel_data.get('error')}"}
            
            return {
                "success": True,
                "bot_user_id": auth_data.get("user_id"),
                "channel_name": channel_data.get("channel", {}).get("name"),
                "permissions": "OK"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def debug_message_detection(self) -> Dict[str, Any]:
        """Enhanced debug method for message detection testing"""
        logger.info("🔍 Testing enhanced message detection...")
        
        # Send a test message
        test_timestamp = self.send_message(
            "🧪 **Enhanced Message Detection Test**\n\n"
            "This is an improved test message. Please reply to test message detection!\n"
            "The enhanced filtering should now work better.",
            add_tracking=True
        )
        
        if not test_timestamp:
            return {"success": False, "error": "Failed to send test message"}
        
        # Wait a moment and check for messages
        time.sleep(2)
        messages = self.get_messages_since(test_timestamp)
        
        # Also get recent messages for debugging
        recent_messages = self.get_recent_messages(limit=10)
        
        return {
            "success": True,
            "test_timestamp": test_timestamp,
            "tracking_code": self.current_tracking_code,
            "bot_user_id": self.bot_user_id,
            "filtered_messages": len(messages),
            "total_recent_messages": len(recent_messages),
            "recent_message_details": [
                {
                    "user": msg.get("user"),
                    "bot_id": msg.get("bot_id"),
                    "subtype": msg.get("subtype"),
                    "text": msg.get("text", "")[:50] + "..." if len(msg.get("text", "")) > 50 else msg.get("text", ""),
                    "is_human": self._is_human_message(msg, self.bot_user_id),
                    "timestamp": msg.get("ts")
                } for msg in recent_messages[:5]
            ]
        }
    
    def send_debug_info(self, info: Dict[str, Any]) -> None:
        """Send debug information to Slack for troubleshooting"""
        debug_text = f"""🔧 **Debug Information**

**Bot User ID:** {info.get('bot_user_id', 'Unknown')}
**Tracking Code:** {info.get('tracking_code', 'None')}
**Recent Messages:** {info.get('total_recent_messages', 0)}
**Human Messages Found:** {info.get('filtered_messages', 0)}

**Recent Message Analysis:**
"""
        
        for i, msg in enumerate(info.get('recent_message_details', []), 1):
            debug_text += f"\n{i}. User: {msg.get('user', 'Unknown')}, Human: {msg.get('is_human', False)}, Text: {msg.get('text', 'No text')}"
        
        self.send_message(debug_text)