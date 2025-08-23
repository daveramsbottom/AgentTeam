"""
Intelligent Context Analyzer
Replaces generic question generation with smart, context-aware analysis
"""
import logging
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta
import json

logger = logging.getLogger(__name__)


@dataclass
class ProjectContext:
    """Rich context information about a project"""
    project_key: str
    project_name: str
    existing_stories: List[Dict[str, Any]]
    recent_changes: List[Dict[str, Any]]
    project_type: Optional[str] = None
    complexity_level: Optional[str] = None
    team_members: List[str] = None
    last_activity: Optional[datetime] = None


@dataclass
class AnalysisResult:
    """Result of intelligent context analysis"""
    needs_clarification: bool
    clarification_questions: List[str]
    suggested_actions: List[str]
    project_insights: Dict[str, Any]
    confidence_score: float
    reasoning: str


class IntelligentContextAnalyzer:
    """Analyzes project context to make intelligent decisions about next actions"""
    
    def __init__(self, ai_client=None):
        self.ai_client = ai_client
        self.question_templates = self._load_question_templates()
        
    def analyze_project_context(self, project_goal: str, context: ProjectContext) -> AnalysisResult:
        """
        Perform comprehensive analysis of project context to determine intelligent next actions
        """
        logger.info(f"🧠 Analyzing project context for {context.project_key}")
        
        # Step 1: Analyze existing backlog
        backlog_analysis = self._analyze_existing_backlog(context.existing_stories)
        
        # Step 2: Detect project type and complexity
        project_type = self._detect_project_type(project_goal, context.existing_stories)
        
        # Step 3: Identify knowledge gaps
        knowledge_gaps = self._identify_knowledge_gaps(project_goal, backlog_analysis, project_type)
        
        # Step 4: Generate context-aware questions (only if needed)
        questions = self._generate_smart_questions(project_goal, knowledge_gaps, backlog_analysis, project_type)
        
        # Step 5: Suggest intelligent actions
        actions = self._suggest_next_actions(backlog_analysis, knowledge_gaps, project_type)
        
        # Step 6: Calculate confidence and provide reasoning
        confidence = self._calculate_confidence(backlog_analysis, knowledge_gaps, questions)
        reasoning = self._generate_reasoning(backlog_analysis, knowledge_gaps, questions, actions)
        
        return AnalysisResult(
            needs_clarification=len(questions) > 0,
            clarification_questions=questions,
            suggested_actions=actions,
            project_insights={
                "project_type": project_type,
                "backlog_analysis": backlog_analysis,
                "knowledge_gaps": knowledge_gaps
            },
            confidence_score=confidence,
            reasoning=reasoning
        )
    
    def _analyze_existing_backlog(self, stories: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze existing backlog to understand what's already covered"""
        if not stories:
            return {
                "story_count": 0,
                "coverage_areas": [],
                "gaps": ["No existing stories found"],
                "recommendations": ["Start with core user stories"],
                "status": "empty_backlog"
            }
        
        # Categorize existing stories
        categories = {
            "authentication": [],
            "user_management": [],
            "core_features": [],
            "ui_ux": [],
            "api": [],
            "testing": [],
            "deployment": []
        }
        
        coverage_areas = set()
        
        for story in stories:
            title = story.get("title", "").lower()
            description = story.get("description", "").lower()
            story_text = f"{title} {description}"
            
            # Categorize story
            if any(keyword in story_text for keyword in ["login", "register", "auth", "password"]):
                categories["authentication"].append(story)
                coverage_areas.add("authentication")
                
            elif any(keyword in story_text for keyword in ["user", "profile", "account"]):
                categories["user_management"].append(story)
                coverage_areas.add("user_management")
                
            elif any(keyword in story_text for keyword in ["dashboard", "home", "main"]):
                categories["ui_ux"].append(story)
                coverage_areas.add("ui_ux")
                
            elif any(keyword in story_text for keyword in ["api", "endpoint", "rest"]):
                categories["api"].append(story)
                coverage_areas.add("api")
                
            else:
                categories["core_features"].append(story)
                coverage_areas.add("core_features")
        
        # Identify what's missing
        all_areas = set(categories.keys())
        gaps = list(all_areas - coverage_areas)
        
        return {
            "story_count": len(stories),
            "coverage_areas": list(coverage_areas),
            "gaps": gaps,
            "categories": {k: len(v) for k, v in categories.items() if v},
            "recommendations": self._get_backlog_recommendations(coverage_areas, gaps),
            "status": "has_stories"
        }
    
    def _detect_project_type(self, project_goal: str, stories: List[Dict[str, Any]]) -> str:
        """Detect the type of project based on goal and existing stories"""
        goal_lower = project_goal.lower()
        
        # Check for explicit project type mentions
        if "web application" in goal_lower or "website" in goal_lower:
            if "e-commerce" in goal_lower or "shop" in goal_lower:
                return "e-commerce_web_app"
            elif "blog" in goal_lower or "cms" in goal_lower:
                return "blog_cms"
            elif "task" in goal_lower or "management" in goal_lower:
                return "task_management_app" 
            else:
                return "general_web_app"
                
        elif "api" in goal_lower or "rest" in goal_lower:
            return "api_service"
            
        elif "mobile" in goal_lower:
            return "mobile_app"
            
        elif "basic" in goal_lower or "simple" in goal_lower:
            return "basic_application"
            
        else:
            # Infer from existing stories
            if stories:
                story_text = " ".join([f"{s.get('title', '')} {s.get('description', '')}" for s in stories]).lower()
                
                if "api" in story_text:
                    return "api_service"
                elif "mobile" in story_text:
                    return "mobile_app"
                elif "e-commerce" in story_text or "cart" in story_text:
                    return "e-commerce_web_app"
                    
            return "general_application"
    
    def _identify_knowledge_gaps(self, project_goal: str, backlog_analysis: Dict[str, Any], project_type: str) -> List[str]:
        """Identify what information is still needed"""
        gaps = []
        
        # Check if we have enough detail in the project goal
        goal_words = len(project_goal.split())
        if goal_words < 10:
            gaps.append("project_goal_too_vague")
        
        # Check for missing coverage areas based on project type
        coverage_areas = set(backlog_analysis.get("coverage_areas", []))
        
        if project_type in ["e-commerce_web_app", "general_web_app", "task_management_app"]:
            required_areas = {"authentication", "core_features", "ui_ux"}
            missing = required_areas - coverage_areas
            gaps.extend([f"missing_{area}" for area in missing])
            
        elif project_type == "basic_application":
            # For basic apps, we need very few areas
            if "core_features" not in coverage_areas and backlog_analysis["story_count"] == 0:
                gaps.append("missing_core_features")
                
        elif project_type == "api_service":
            required_areas = {"api", "authentication"}
            missing = required_areas - coverage_areas
            gaps.extend([f"missing_{area}" for area in missing])
        
        # Check if goal conflicts with existing stories
        if backlog_analysis["story_count"] > 0:
            if "basic" in project_goal.lower() and "authentication" in coverage_areas:
                gaps.append("goal_story_mismatch")
        
        return gaps
    
    def _generate_smart_questions(self, project_goal: str, gaps: List[str], backlog_analysis: Dict[str, Any], project_type: str) -> List[str]:
        """Generate intelligent, context-aware questions only when truly needed"""
        questions = []
        
        # For basic applications, don't ask complex questions
        if project_type == "basic_application":
            if backlog_analysis["story_count"] == 0:
                questions.append("What core functionality should this basic application provide? (please be specific about the main features)")
            return questions[:1]  # Only ask 1 question for basic apps
        
        # Handle goal/story mismatches
        if "goal_story_mismatch" in gaps:
            questions.append(f"I notice you mentioned a 'basic' app, but there are existing authentication stories. Should I focus on simple functionality or include user management?")
        
        # Ask about missing core features only if truly needed
        if "missing_core_features" in gaps and backlog_analysis["story_count"] == 0:
            if project_type == "e-commerce_web_app":
                questions.append("What products will be sold and what payment methods should be supported?")
            elif project_type == "task_management_app":
                questions.append("What types of tasks will users manage and how should they be organized?")
            elif project_type == "blog_cms":
                questions.append("What content types will be managed and who can create/edit content?")
            else:
                questions.append("What are the core features users need to accomplish their main goals?")
        
        # Ask about user types only for complex applications
        if project_type not in ["basic_application"] and backlog_analysis["story_count"] == 0:
            questions.append("Who are the main types of users and what are their different needs?")
        
        # Ask about technical preferences only if relevant
        if "missing_api" in gaps and project_type in ["api_service", "e-commerce_web_app"]:
            questions.append("What external systems need to integrate with this application?")
        
        # Prioritization question for existing backlogs
        if backlog_analysis["story_count"] > 0:
            questions.append("Looking at the existing stories, which features are most important to implement first?")
        
        # Use AI to refine questions if available
        if self.ai_client and len(questions) > 0:
            try:
                refined_questions = self.ai_client.refine_questions(
                    questions=questions,
                    project_goal=project_goal,
                    project_type=project_type,
                    existing_stories_count=backlog_analysis["story_count"]
                )
                if refined_questions:
                    questions = refined_questions
            except Exception as e:
                logger.warning(f"AI question refinement failed: {e}")
        
        # Limit questions based on project complexity
        max_questions = 2 if project_type == "basic_application" else 4
        return questions[:max_questions]
    
    def _suggest_next_actions(self, backlog_analysis: Dict[str, Any], gaps: List[str], project_type: str) -> List[str]:
        """Suggest intelligent next actions based on context"""
        actions = []
        
        if backlog_analysis["story_count"] == 0:
            if project_type == "basic_application":
                actions.append("Create minimal set of user stories focusing on core functionality")
            else:
                actions.append("Create comprehensive user stories with acceptance criteria")
        else:
            actions.append("Review and refine existing stories based on current project understanding")
            
        if gaps:
            actions.append(f"Address {len(gaps)} identified knowledge gaps through clarification")
            
        if backlog_analysis["story_count"] > 0:
            actions.append("Prioritize existing stories for development planning")
            
        return actions
    
    def _calculate_confidence(self, backlog_analysis: Dict[str, Any], gaps: List[str], questions: List[str]) -> float:
        """Calculate confidence score for proceeding without clarification"""
        base_confidence = 0.5
        
        # Higher confidence with existing stories
        if backlog_analysis["story_count"] > 0:
            base_confidence += 0.2
            
        # Lower confidence with many gaps
        gap_penalty = min(len(gaps) * 0.1, 0.3)
        base_confidence -= gap_penalty
        
        # Higher confidence with fewer questions needed
        question_penalty = min(len(questions) * 0.1, 0.2)
        base_confidence -= question_penalty
        
        return max(0.1, min(1.0, base_confidence))
    
    def _generate_reasoning(self, backlog_analysis: Dict[str, Any], gaps: List[str], questions: List[str], actions: List[str]) -> str:
        """Generate human-readable reasoning for the analysis"""
        reasoning_parts = []
        
        # Backlog context
        if backlog_analysis["story_count"] == 0:
            reasoning_parts.append("No existing stories found - starting fresh")
        else:
            reasoning_parts.append(f"Found {backlog_analysis['story_count']} existing stories covering {', '.join(backlog_analysis['coverage_areas'])}")
        
        # Gaps identified
        if gaps:
            gap_descriptions = {
                "project_goal_too_vague": "project goal needs more detail",
                "missing_core_features": "core features not defined",
                "missing_authentication": "authentication approach unclear", 
                "goal_story_mismatch": "project goal conflicts with existing stories"
            }
            
            gap_texts = [gap_descriptions.get(gap, gap) for gap in gaps[:3]]
            reasoning_parts.append(f"Identified issues: {', '.join(gap_texts)}")
        
        # Question necessity
        if len(questions) == 0:
            reasoning_parts.append("No clarification needed - can proceed directly")
        elif len(questions) <= 2:
            reasoning_parts.append(f"Asking {len(questions)} focused questions to fill key gaps")
        else:
            reasoning_parts.append(f"Need {len(questions)} clarifications for comprehensive understanding")
        
        return ". ".join(reasoning_parts)
    
    def _get_backlog_recommendations(self, coverage_areas: List[str], gaps: List[str]) -> List[str]:
        """Get recommendations based on backlog analysis"""
        recommendations = []
        
        if not coverage_areas:
            recommendations.append("Start with user authentication and core features")
        elif "core_features" not in coverage_areas:
            recommendations.append("Define core business functionality stories")
        elif "testing" in gaps:
            recommendations.append("Add testing and quality assurance stories")
            
        return recommendations
    
    def _load_question_templates(self) -> Dict[str, List[str]]:
        """Load question templates for different project types"""
        return {
            "basic_application": [
                "What is the main purpose of this application?",
                "What core features do users need?"
            ],
            "web_application": [
                "What types of users will use this application?",
                "What are the main workflows users need to complete?",
                "Do you need user registration and authentication?"
            ],
            "api_service": [
                "What data will this API manage?",
                "What external systems need to integrate?", 
                "What authentication method should be used?"
            ],
            "e-commerce": [
                "What types of products will be sold?",
                "What payment methods should be supported?",
                "Do you need inventory management?"
            ]
        }