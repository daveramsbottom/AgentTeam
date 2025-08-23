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
        logger.info("🤖 AgentIan AI initialized with OpenAI integration")
    
    def improve_text_with_ai(self, text: str) -> Dict[str, Any]:
        """
        Use OpenAI to improve spelling, grammar, and clarity of human input
        
        Returns:
            Dict with improved text and analysis
        """
        try:
            prompt = f"""
            Please review the following text for spelling, grammar, and clarity improvements:

            "{text}"

            Please provide:
            1. Corrected text with proper spelling and grammar
            2. List any significant changes made
            3. Whether any improvements were needed

            Format as JSON:
            {{
                "original_text": "{text}",
                "improved_text": "corrected version",
                "changes_made": ["list of changes"],
                "has_improvements": true/false,
                "notes": "brief explanation if needed"
            }}
            """

            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that improves text quality by fixing spelling, grammar, and clarity issues."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=500
            )
            
            import json
            result = json.loads(response.choices[0].message.content)
            
            return {
                'original_text': text,
                'corrected_text': result.get('improved_text', text),
                'changes_made': result.get('changes_made', []),
                'has_corrections': result.get('has_improvements', False),
                'notes': result.get('notes', '')
            }
            
        except Exception as e:
            logger.warning(f"AI text improvement failed: {e}")
            return {
                'original_text': text,
                'corrected_text': text,
                'changes_made': [],
                'has_corrections': False,
                'notes': 'Text improvement unavailable'
            }
    
    def analyze_project_goal(self, project_goal: str) -> Dict[str, Any]:
        """
        Use AI to analyze a project goal and generate intelligent clarification questions
        """
        try:
            prompt = f"""
            As AgentIan, a Product Owner AI, analyze this project goal and generate intelligent clarification questions.

            Project Goal: "{project_goal}"

            Please provide:
            1. A brief analysis of the project complexity and scope
            2. 3-4 specific, insightful clarification questions that would help create better user stories
            3. Identify any potential technical challenges or considerations
            4. Suggest the project type (web app, mobile app, API, etc.)

            Format your response as JSON with these keys:
            - "analysis": string with project analysis
            - "questions": array of clarification questions
            - "technical_considerations": array of technical points to consider
            - "suggested_project_type": string
            - "estimated_complexity": "low" | "medium" | "high"
            """

            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are AgentIan, an expert Product Owner AI specializing in software project analysis and user story creation."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1000
            )
            
            # Parse the JSON response
            import json
            ai_analysis = json.loads(response.choices[0].message.content)
            
            logger.info("✅ AI project analysis completed")
            return {
                'success': True,
                'analysis': ai_analysis
            }
            
        except Exception as e:
            logger.error(f"AI project analysis failed: {e}")
            # Fallback to basic analysis
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