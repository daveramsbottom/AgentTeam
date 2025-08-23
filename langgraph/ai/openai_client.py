"""
OpenAI Integration for AgentTeam
Provides AI-powered analysis, spell checking, and content generation
"""
import os
import logging
from typing import Dict, List, Any, Optional
from openai import OpenAI

logger = logging.getLogger(__name__)

class AgentIanAI:
    """OpenAI integration for AgentIan with spell checking capabilities"""
    
    def __init__(self, api_key: str):
        """Initialize OpenAI client"""
        self.client = OpenAI(api_key=api_key)
        self.ai_enabled = True
        self.consecutive_failures = 0
        self.max_failures_before_disable = 3
        logger.info("🤖 AgentIan AI initialized with OpenAI integration")
    
    def _handle_ai_failure(self, operation: str):
        """Handle AI operation failure and disable if too many failures"""
        self.consecutive_failures += 1
        if self.consecutive_failures >= self.max_failures_before_disable:
            self.ai_enabled = False
            logger.warning(f"🔴 AI disabled after {self.consecutive_failures} consecutive failures in {operation}")
            logger.info("💡 Enhanced AgentIan will continue using rule-based fallbacks")
    
    def _handle_ai_success(self):
        """Handle successful AI operation"""
        if self.consecutive_failures > 0:
            logger.info(f"🟢 AI recovered after {self.consecutive_failures} failures")
        self.consecutive_failures = 0
        self.ai_enabled = True
    
    def improve_text_with_ai(self, text: str) -> Dict[str, Any]:
        """
        Use OpenAI to improve spelling, grammar, and clarity of human input
        
        Returns:
            Dict with improved text and analysis
        """
        # Skip AI improvement for very short text or if AI is disabled
        if len(text.strip()) < 10 or not self.ai_enabled:
            return {
                'original_text': text,
                'corrected_text': text,
                'changes_made': [],
                'has_corrections': False,
                'notes': 'Text too short for AI improvement' if len(text.strip()) < 10 else 'AI temporarily disabled'
            }
        
        try:
            prompt = f"""Review this text and improve spelling, grammar, and clarity. Respond ONLY with valid JSON in this exact format:

{{"original_text": "{text}", "improved_text": "your improved version", "changes_made": ["list any significant changes"], "has_improvements": false, "notes": "brief explanation"}}

Text to review: "{text}"

Remember: Respond only with the JSON object, no other text."""

            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a text improvement assistant. Always respond with valid JSON only, no other text or formatting."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,
                max_tokens=300
            )
            
            response_text = response.choices[0].message.content.strip()
            logger.debug(f"AI text improvement response: {response_text[:100]}...")
            
            # Handle cases where response might have markdown formatting
            if response_text.startswith('```json'):
                response_text = response_text.replace('```json', '').replace('```', '').strip()
            elif response_text.startswith('```'):
                response_text = response_text.replace('```', '').strip()
            
            import json
            result = json.loads(response_text)
            
            # Success - reset failure counter
            self._handle_ai_success()
            
            return {
                'original_text': text,
                'corrected_text': result.get('improved_text', text),
                'changes_made': result.get('changes_made', []),
                'has_corrections': result.get('has_improvements', False),
                'notes': result.get('notes', '')
            }
            
        except json.JSONDecodeError as e:
            self._handle_ai_failure("text_improvement")
            logger.warning(f"AI text improvement failed - invalid JSON: {e}")
            logger.debug(f"Response was: {response.choices[0].message.content if 'response' in locals() else 'No response'}")
            return {
                'original_text': text,
                'corrected_text': text,
                'changes_made': [],
                'has_corrections': False,
                'notes': 'AI improvement unavailable - JSON parse error'
            }
        except Exception as e:
            self._handle_ai_failure("text_improvement") 
            logger.warning(f"AI text improvement failed: {e}")
            return {
                'original_text': text,
                'corrected_text': text,
                'changes_made': [],
                'has_corrections': False,
                'notes': 'AI improvement unavailable'
            }
    
    def analyze_project_goal(self, project_goal: str) -> Dict[str, Any]:
        """
        Use AI to analyze a project goal and generate intelligent clarification questions
        """
        if not self.ai_enabled:
            logger.info("AI disabled, using fallback questions")
            return {
                'success': False,
                'error': 'AI temporarily disabled',
                'fallback_questions': self._generate_fallback_questions(project_goal)
            }
        
        try:
            prompt = f"""Analyze this project goal and respond ONLY with valid JSON in this exact format:

{{"analysis": "brief project analysis", "questions": ["question 1", "question 2", "question 3"], "technical_considerations": ["consideration 1", "consideration 2"], "suggested_project_type": "web app", "estimated_complexity": "medium"}}

Project Goal: "{project_goal}"

Provide 3-4 insightful questions that would help create better user stories. Focus on what's most important to understand about this specific project.

Remember: Respond only with the JSON object, no other text."""

            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are AgentIan, a Product Owner AI. Always respond with valid JSON only, no other text."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5,
                max_tokens=800
            )
            
            response_text = response.choices[0].message.content.strip()
            logger.debug(f"AI project analysis response: {response_text[:100]}...")
            
            # Handle markdown formatting
            if response_text.startswith('```json'):
                response_text = response_text.replace('```json', '').replace('```', '').strip()
            elif response_text.startswith('```'):
                response_text = response_text.replace('```', '').strip()
            
            import json
            ai_analysis = json.loads(response_text)
            
            # Success - reset failure counter
            self._handle_ai_success()
            
            logger.info("✅ AI project analysis completed")
            return {
                'success': True,
                'analysis': ai_analysis
            }
            
        except json.JSONDecodeError as e:
            self._handle_ai_failure("project_analysis")
            logger.warning(f"AI project analysis failed - invalid JSON: {e}")
            logger.debug(f"Response was: {response.choices[0].message.content if 'response' in locals() else 'No response'}")
            return {
                'success': False,
                'error': f'JSON parse error: {e}',
                'fallback_questions': self._generate_fallback_questions(project_goal)
            }
        except Exception as e:
            self._handle_ai_failure("project_analysis")
            logger.error(f"AI project analysis failed: {e}")
            return {
                'success': False,
                'error': str(e),
                'fallback_questions': self._generate_fallback_questions(project_goal)
            }
    
    def generate_user_stories(self, project_goal: str, clarification_response: str = "") -> List[Dict[str, Any]]:
        """
        Use AI to generate comprehensive user stories with acceptance criteria
        """
        try:
            context = f"Project Goal: {project_goal}"
            if clarification_response:
                context += f"\n\nAdditional Requirements from Human: {clarification_response}"
            
            prompt = f"""
            As AgentIan, create detailed user stories for this project:

            {context}

            Generate 4-6 user stories that cover the core functionality. For each story, provide:
            - A clear title
            - User story in "As a [user], I want [goal] so that [benefit]" format
            - Detailed description with context
            - 3-5 specific acceptance criteria
            - Estimated story points (1, 2, 3, 5, 8, 13)
            - Priority level (High, Medium, Low)

            Format as JSON array with objects containing:
            - "title": string
            - "user_story": string
            - "description": string  
            - "acceptance_criteria": array of strings
            - "story_points": number
            - "priority": string
            """

            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are AgentIan, an expert Product Owner AI creating professional user stories for software development teams."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.6,
                max_tokens=2000
            )
            
            # Parse the JSON response
            import json
            ai_stories = json.loads(response.choices[0].message.content)
            
            logger.info(f"✅ Generated {len(ai_stories)} AI-powered user stories")
            return ai_stories
            
        except Exception as e:
            logger.error(f"AI story generation failed: {e}")
            # Fallback to basic story generation
            return self._generate_fallback_stories(project_goal, clarification_response)
    
    def enhance_clarification_response(self, human_response: str) -> Dict[str, Any]:
        """
        Process and enhance human clarification responses with AI text improvement and analysis
        """
        # First, improve the text with AI
        text_improvement = self.improve_text_with_ai(human_response)
        
        try:
            # Use AI to analyze and enhance the response
            prompt = f"""
            As AgentIan, analyze this human response to clarification questions:

            Original Response: "{human_response}"
            Improved Text: "{text_improvement['corrected_text']}"

            Please:
            1. Extract key requirements and features mentioned
            2. Identify any ambiguities that might need further clarification
            3. Suggest additional considerations the human might not have mentioned
            4. Format the response in a clear, structured way

            Provide JSON response with:
            - "key_requirements": array of extracted requirements
            - "ambiguities": array of things that need clarification
            - "suggestions": array of additional considerations
            - "structured_response": cleaned up version of the human response
            """

            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are AgentIan, analyzing human requirements to improve user story creation."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5,
                max_tokens=800
            )
            
            import json
            ai_enhancement = json.loads(response.choices[0].message.content)
            
            return {
                'text_improvement': text_improvement,
                'ai_enhancement': ai_enhancement,
                'enhanced_text': ai_enhancement.get('structured_response', text_improvement['corrected_text'])
            }
            
        except Exception as e:
            logger.error(f"AI response enhancement failed: {e}")
            return {
                'text_improvement': text_improvement,
                'ai_enhancement': None,
                'enhanced_text': text_improvement['corrected_text']
            }
    
    def _generate_fallback_questions(self, project_goal: str) -> List[str]:
        """Fallback question generation if AI fails"""
        basic_questions = [
            "What are the main features you want users to be able to do?",
            "Who is the primary target audience for this project?",
            "Are there any specific technical requirements or constraints?",
            "What is the most important functionality to implement first?"
        ]
        
        goal_lower = project_goal.lower()
        
        if "web" in goal_lower:
            basic_questions.append("Should this work on both desktop and mobile browsers?")
        if "mobile" in goal_lower:
            basic_questions.append("Do you need native mobile apps or is mobile web sufficient?")
        if "user" in goal_lower:
            basic_questions.append("What types of user accounts or roles do you need?")
        
        return basic_questions[:4]
    
    def _generate_fallback_stories(self, project_goal: str, clarification: str) -> List[Dict[str, Any]]:
        """Fallback story generation if AI fails"""
        stories = []
        
        # Basic user registration story
        stories.append({
            "title": "User Registration and Login",
            "user_story": "As a user, I want to create an account and log in so that I can access the application features.",
            "description": f"Enable user registration and authentication for the project: {project_goal}",
            "acceptance_criteria": [
                "User can register with email and password",
                "User can log in with valid credentials",
                "User receives appropriate error messages for invalid inputs",
                "User session is maintained during browsing"
            ],
            "story_points": 5,
            "priority": "High"
        })
        
        # Project-specific story based on keywords
        goal_lower = project_goal.lower()
        if "task" in goal_lower or "manage" in goal_lower:
            stories.append({
                "title": "Task Management",
                "user_story": "As a user, I want to create and manage tasks so that I can track my work progress.",
                "description": f"Core task management functionality for: {project_goal}",
                "acceptance_criteria": [
                    "User can create new tasks",
                    "User can edit existing tasks", 
                    "User can mark tasks as complete",
                    "User can view list of all tasks"
                ],
                "story_points": 8,
                "priority": "High"
            })
        
        return stories

# Configuration helper
def get_openai_client() -> Optional[AgentIanAI]:
    """Get configured OpenAI client if API key is available"""
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key or api_key == 'your_openai_key_here':
        logger.warning("⚠️ OpenAI API key not configured, using fallback methods")
        return None
    
    try:
        return AgentIanAI(api_key)
    except Exception as e:
        logger.error(f"Failed to initialize OpenAI client: {e}")
        return None