"""
Technical Analysis Module for AgentPete
AI-powered analysis of user stories and tasks to extract technical requirements,
assess complexity, and provide implementation recommendations
"""
import logging
import json
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime

from workflows.states import (
    TechnicalRequirement, TechnicalEstimate, TechStackRecommendation, 
    ImplementationPlan, DevelopmentTask
)

logger = logging.getLogger(__name__)


class TechnicalAnalyzer:
    """
    AI-powered technical analyzer for development tasks
    Provides requirement extraction, complexity assessment, and implementation planning
    """
    
    def __init__(self, ai_client=None):
        """Initialize the technical analyzer with AI capabilities"""
        self.ai_client = ai_client
        self.ai_enabled = ai_client is not None and hasattr(ai_client, 'ai_enabled') and ai_client.ai_enabled
        
        # Fallback patterns for rule-based analysis when AI is not available
        self.complexity_indicators = {
            'high': ['integration', 'api', 'database', 'authentication', 'security', 'performance', 'migration', 'complex'],
            'medium': ['form', 'validation', 'ui', 'frontend', 'backend', 'service', 'component'],
            'low': ['text', 'button', 'style', 'layout', 'simple', 'basic', 'display']
        }
        
        self.tech_stack_defaults = {
            'frontend': {'tech': 'React', 'alternatives': ['Vue.js', 'Angular'], 'reasoning': 'Popular, well-supported framework'},
            'backend': {'tech': 'FastAPI', 'alternatives': ['Django', 'Flask'], 'reasoning': 'Fast, modern Python framework'},
            'database': {'tech': 'PostgreSQL', 'alternatives': ['MySQL', 'SQLite'], 'reasoning': 'Reliable, feature-rich relational database'},
            'testing': {'tech': 'pytest', 'alternatives': ['unittest', 'Jest'], 'reasoning': 'Comprehensive testing framework'}
        }
        
        if self.ai_enabled:
            logger.info("🤖 TechnicalAnalyzer initialized with AI capabilities")
        else:
            logger.info("🤖 TechnicalAnalyzer initialized with rule-based fallbacks")
    
    def analyze_task_requirements(self, issue_key: str, title: str, description: str, 
                                issue_type: str) -> List[TechnicalRequirement]:
        """Extract technical requirements from a user story or task"""
        logger.info(f"🔍 Analyzing technical requirements for {issue_key}")
        
        if self.ai_enabled:
            return self._ai_analyze_requirements(title, description, issue_type)
        else:
            return self._rule_based_analyze_requirements(title, description, issue_type)
    
    def assess_complexity(self, title: str, description: str, 
                         requirements: List[TechnicalRequirement]) -> Tuple[str, float]:
        """Assess the complexity of a development task"""
        logger.info("📊 Assessing task complexity...")
        
        if self.ai_enabled:
            return self._ai_assess_complexity(title, description, requirements)
        else:
            return self._rule_based_assess_complexity(title, description, requirements)
    
    def estimate_effort(self, title: str, description: str, complexity: str, 
                       requirements: List[TechnicalRequirement], 
                       story_points: Optional[int] = None) -> TechnicalEstimate:
        """Estimate development effort for the task"""
        logger.info("⏱️ Estimating development effort...")
        
        if self.ai_enabled:
            return self._ai_estimate_effort(title, description, complexity, requirements, story_points)
        else:
            return self._rule_based_estimate_effort(title, description, complexity, requirements, story_points)
    
    def recommend_tech_stack(self, title: str, description: str, 
                            requirements: List[TechnicalRequirement]) -> List[TechStackRecommendation]:
        """Recommend appropriate technology stack for the task"""
        logger.info("⚙️ Recommending technology stack...")
        
        if self.ai_enabled:
            return self._ai_recommend_tech_stack(title, description, requirements)
        else:
            return self._rule_based_recommend_tech_stack(title, description, requirements)
    
    def create_implementation_plan(self, title: str, description: str, 
                                  requirements: List[TechnicalRequirement],
                                  tech_stack: List[TechStackRecommendation]) -> ImplementationPlan:
        """Create detailed implementation plan for the task"""
        logger.info("📋 Creating implementation plan...")
        
        if self.ai_enabled:
            return self._ai_create_implementation_plan(title, description, requirements, tech_stack)
        else:
            return self._rule_based_create_implementation_plan(title, description, requirements, tech_stack)
    
    # AI-Powered Analysis Methods
    def _ai_analyze_requirements(self, title: str, description: str, issue_type: str) -> List[TechnicalRequirement]:
        """Use AI to extract technical requirements"""
        try:
            prompt = f"""
Analyze this {issue_type.lower()} and extract technical requirements:

Title: {title}
Description: {description}

Extract technical requirements in the following categories:
1. Functional requirements (what the system should do)
2. Non-functional requirements (performance, security, usability)
3. Technical constraints (technology, integration, compatibility)

For each requirement, determine:
- Priority: must-have, should-have, or could-have
- Complexity: low, medium, high, or very-high
- Dependencies on other components
- Acceptance criteria

Return as JSON array with this structure:
[
  {{
    "requirement_type": "functional|non-functional|constraint",
    "description": "Clear description of the requirement",
    "priority": "must-have|should-have|could-have", 
    "complexity": "low|medium|high|very-high",
    "dependencies": ["list of dependencies"],
    "acceptance_criteria": ["list of criteria"]
  }}
]
"""
            
            result = self.ai_client.analyze_project_goal(prompt)
            if result['success'] and 'analysis' in result:
                # Try to parse AI response as JSON
                try:
                    requirements_data = json.loads(result['analysis'].get('technical_analysis', '[]'))
                    requirements = []
                    for req_data in requirements_data:
                        requirements.append(TechnicalRequirement(
                            requirement_type=req_data.get('requirement_type', 'functional'),
                            description=req_data.get('description', ''),
                            priority=req_data.get('priority', 'should-have'),
                            complexity=req_data.get('complexity', 'medium'),
                            dependencies=req_data.get('dependencies', []),
                            acceptance_criteria=req_data.get('acceptance_criteria', [])
                        ))
                    return requirements
                except json.JSONDecodeError:
                    logger.warning("Failed to parse AI requirements response as JSON, using fallback")
                    
        except Exception as e:
            logger.error(f"Error in AI requirements analysis: {e}")
        
        # Fallback to rule-based analysis
        return self._rule_based_analyze_requirements(title, description, issue_type)
    
    def _ai_assess_complexity(self, title: str, description: str, 
                             requirements: List[TechnicalRequirement]) -> Tuple[str, float]:
        """Use AI to assess task complexity"""
        try:
            req_summary = "\n".join([f"- {req.description} ({req.complexity})" for req in requirements])
            
            prompt = f"""
Assess the complexity of this development task:

Title: {title}
Description: {description}

Technical Requirements:
{req_summary}

Consider:
- Number and complexity of requirements
- Integration complexity
- Technical challenges
- Risk factors
- Development experience needed

Return complexity as one of: low, medium, high, very-high
Also provide a complexity factor (multiplier) between 0.5 and 3.0

Format: {{"complexity": "medium", "factor": 1.2}}
"""
            
            result = self.ai_client.analyze_project_goal(prompt)
            if result['success'] and 'analysis' in result:
                try:
                    analysis_data = json.loads(result['analysis'].get('complexity_assessment', '{}'))
                    complexity = analysis_data.get('complexity', 'medium')
                    factor = float(analysis_data.get('factor', 1.0))
                    return complexity, factor
                except (json.JSONDecodeError, ValueError):
                    logger.warning("Failed to parse AI complexity response, using fallback")
                    
        except Exception as e:
            logger.error(f"Error in AI complexity assessment: {e}")
        
        # Fallback to rule-based assessment
        return self._rule_based_assess_complexity(title, description, requirements)
    
    def _ai_estimate_effort(self, title: str, description: str, complexity: str,
                           requirements: List[TechnicalRequirement],
                           story_points: Optional[int] = None) -> TechnicalEstimate:
        """Use AI to estimate development effort"""
        try:
            req_summary = "\n".join([f"- {req.description} ({req.complexity})" for req in requirements])
            
            prompt = f"""
Estimate development effort for this task:

Title: {title}
Description: {description}
Complexity: {complexity}
Story Points: {story_points if story_points else "Not specified"}

Technical Requirements:
{req_summary}

Provide estimation including:
- Total development hours
- Breakdown by activity (analysis, design, coding, testing, review)
- Risk factors and buffer hours
- Confidence level (low, medium, high)
- Key assumptions
- Potential risks

Return as JSON:
{{
  "estimated_hours": 8.0,
  "complexity_factor": 1.2,
  "risk_buffer_hours": 2.0,
  "confidence_level": "medium",
  "breakdown": {{
    "analysis": 1.0,
    "design": 1.5,
    "coding": 4.0,
    "testing": 1.0,
    "review": 0.5
  }},
  "assumptions": ["list of assumptions"],
  "risks": ["list of risks"]
}}
"""
            
            result = self.ai_client.analyze_project_goal(prompt)
            if result['success'] and 'analysis' in result:
                try:
                    estimation_data = json.loads(result['analysis'].get('effort_estimation', '{}'))
                    return TechnicalEstimate(
                        story_points=story_points or 0,
                        estimated_hours=estimation_data.get('estimated_hours', 8.0),
                        complexity_factor=estimation_data.get('complexity_factor', 1.0),
                        risk_buffer_hours=estimation_data.get('risk_buffer_hours', 2.0),
                        confidence_level=estimation_data.get('confidence_level', 'medium'),
                        breakdown=estimation_data.get('breakdown', {}),
                        assumptions=estimation_data.get('assumptions', []),
                        risks=estimation_data.get('risks', [])
                    )
                except json.JSONDecodeError:
                    logger.warning("Failed to parse AI estimation response, using fallback")
                    
        except Exception as e:
            logger.error(f"Error in AI effort estimation: {e}")
        
        # Fallback to rule-based estimation
        return self._rule_based_estimate_effort(title, description, complexity, requirements, story_points)
    
    def _ai_recommend_tech_stack(self, title: str, description: str,
                                requirements: List[TechnicalRequirement]) -> List[TechStackRecommendation]:
        """Use AI to recommend technology stack"""
        try:
            req_summary = "\n".join([f"- {req.description}" for req in requirements])
            
            prompt = f"""
Recommend technology stack for this development task:

Title: {title}
Description: {description}

Requirements:
{req_summary}

Recommend technologies for relevant categories:
- Frontend (if UI/web application)
- Backend (if server-side logic needed)
- Database (if data storage needed)
- Testing frameworks
- Deployment tools

For each recommendation, provide:
- Primary recommendation
- Alternative options
- Reasoning for the choice
- Pros and cons
- Required experience level

Return as JSON array:
[
  {{
    "category": "frontend|backend|database|testing|deployment",
    "recommended_tech": "Technology Name",
    "alternatives": ["alt1", "alt2"],
    "reasoning": "Why this technology",
    "pros": ["advantage1", "advantage2"],
    "cons": ["limitation1", "limitation2"], 
    "experience_required": "beginner|intermediate|advanced"
  }}
]
"""
            
            result = self.ai_client.analyze_project_goal(prompt)
            if result['success'] and 'analysis' in result:
                try:
                    tech_data = json.loads(result['analysis'].get('tech_recommendations', '[]'))
                    recommendations = []
                    for tech in tech_data:
                        recommendations.append(TechStackRecommendation(
                            category=tech.get('category', 'general'),
                            recommended_tech=tech.get('recommended_tech', ''),
                            alternatives=tech.get('alternatives', []),
                            reasoning=tech.get('reasoning', ''),
                            pros=tech.get('pros', []),
                            cons=tech.get('cons', []),
                            experience_required=tech.get('experience_required', 'intermediate')
                        ))
                    return recommendations
                except json.JSONDecodeError:
                    logger.warning("Failed to parse AI tech stack response, using fallback")
                    
        except Exception as e:
            logger.error(f"Error in AI tech stack recommendation: {e}")
        
        # Fallback to rule-based recommendations
        return self._rule_based_recommend_tech_stack(title, description, requirements)
    
    def _ai_create_implementation_plan(self, title: str, description: str,
                                      requirements: List[TechnicalRequirement],
                                      tech_stack: List[TechStackRecommendation]) -> ImplementationPlan:
        """Use AI to create implementation plan"""
        try:
            req_summary = "\n".join([f"- {req.description}" for req in requirements])
            tech_summary = "\n".join([f"- {tech.category}: {tech.recommended_tech}" for tech in tech_stack])
            
            prompt = f"""
Create detailed implementation plan for this task:

Title: {title}
Description: {description}

Requirements:
{req_summary}

Technology Stack:
{tech_summary}

Create a comprehensive plan including:
- Architecture approach
- Component breakdown
- Suggested file/folder structure
- Database schema changes (if applicable)
- API endpoints (if applicable)
- Step-by-step implementation order
- Testing strategy
- Deployment considerations

Return as JSON:
{{
  "architecture_approach": "Description of overall architecture",
  "component_breakdown": [
    {{"name": "ComponentName", "purpose": "What it does", "dependencies": ["dep1"]}}
  ],
  "file_structure": {{
    "src/": ["components/", "services/", "utils/"],
    "components/": ["Component1.tsx", "Component2.tsx"]
  }},
  "database_changes": ["table additions", "schema updates"],
  "api_endpoints": [
    {{"method": "GET", "path": "/api/items", "purpose": "Retrieve items"}}
  ],
  "implementation_steps": ["step 1", "step 2", "step 3"],
  "testing_approach": ["unit tests", "integration tests"],
  "deployment_considerations": ["environment setup", "configuration"]
}}
"""
            
            result = self.ai_client.analyze_project_goal(prompt)
            if result['success'] and 'analysis' in result:
                try:
                    plan_data = json.loads(result['analysis'].get('implementation_plan', '{}'))
                    return ImplementationPlan(
                        architecture_approach=plan_data.get('architecture_approach', ''),
                        component_breakdown=plan_data.get('component_breakdown', []),
                        file_structure=plan_data.get('file_structure', {}),
                        database_changes=plan_data.get('database_changes', []),
                        api_endpoints=plan_data.get('api_endpoints', []),
                        tech_stack=tech_stack,
                        implementation_steps=plan_data.get('implementation_steps', []),
                        testing_approach=plan_data.get('testing_approach', []),
                        deployment_considerations=plan_data.get('deployment_considerations', [])
                    )
                except json.JSONDecodeError:
                    logger.warning("Failed to parse AI implementation plan response, using fallback")
                    
        except Exception as e:
            logger.error(f"Error in AI implementation planning: {e}")
        
        # Fallback to rule-based planning
        return self._rule_based_create_implementation_plan(title, description, requirements, tech_stack)
    
    # Rule-Based Fallback Methods
    def _rule_based_analyze_requirements(self, title: str, description: str, issue_type: str) -> List[TechnicalRequirement]:
        """Rule-based requirement extraction as fallback"""
        requirements = []
        
        # Basic functional requirement
        requirements.append(TechnicalRequirement(
            requirement_type="functional",
            description=f"Implement {title.lower()} according to specifications",
            priority="must-have",
            complexity=self._determine_text_complexity(title + " " + description),
            acceptance_criteria=[
                "Feature works as described",
                "Code follows team standards",
                "All edge cases are handled"
            ]
        ))
        
        # Check for common patterns that indicate additional requirements
        text_lower = (title + " " + description).lower()
        
        if any(word in text_lower for word in ['user', 'login', 'auth']):
            requirements.append(TechnicalRequirement(
                requirement_type="non-functional",
                description="Implement secure user authentication",
                priority="must-have", 
                complexity="high",
                acceptance_criteria=["Passwords are encrypted", "Session management is secure"]
            ))
        
        if any(word in text_lower for word in ['data', 'save', 'store', 'database']):
            requirements.append(TechnicalRequirement(
                requirement_type="functional",
                description="Implement data persistence",
                priority="must-have",
                complexity="medium",
                acceptance_criteria=["Data is saved correctly", "Data can be retrieved", "Data integrity is maintained"]
            ))
        
        if any(word in text_lower for word in ['api', 'integration', 'external']):
            requirements.append(TechnicalRequirement(
                requirement_type="functional",
                description="Implement API integration",
                priority="should-have",
                complexity="high",
                acceptance_criteria=["API calls are handled correctly", "Error handling for API failures"]
            ))
        
        return requirements
    
    def _rule_based_assess_complexity(self, title: str, description: str, 
                                     requirements: List[TechnicalRequirement]) -> Tuple[str, float]:
        """Rule-based complexity assessment"""
        text_lower = (title + " " + description).lower()
        
        # Count complexity indicators
        high_indicators = sum(1 for word in self.complexity_indicators['high'] if word in text_lower)
        medium_indicators = sum(1 for word in self.complexity_indicators['medium'] if word in text_lower)
        low_indicators = sum(1 for word in self.complexity_indicators['low'] if word in text_lower)
        
        # Factor in number of requirements
        req_complexity_score = len([r for r in requirements if r.complexity in ['high', 'very-high']])
        
        total_score = (high_indicators * 3) + (medium_indicators * 2) + (low_indicators * 1) + req_complexity_score
        
        if total_score >= 8:
            return "very-high", 2.0
        elif total_score >= 5:
            return "high", 1.5
        elif total_score >= 2:
            return "medium", 1.0
        else:
            return "low", 0.7
    
    def _rule_based_estimate_effort(self, title: str, description: str, complexity: str,
                                   requirements: List[TechnicalRequirement],
                                   story_points: Optional[int] = None) -> TechnicalEstimate:
        """Rule-based effort estimation"""
        # Base hours by complexity
        base_hours = {
            'low': 4,
            'medium': 8, 
            'high': 16,
            'very-high': 32
        }
        
        hours = base_hours.get(complexity, 8)
        
        # Adjust based on story points if provided
        if story_points:
            hours = max(hours, story_points * 2)  # Rough conversion: 1 SP = 2 hours minimum
        
        # Add buffer based on complexity
        risk_buffer = hours * 0.25 if complexity in ['high', 'very-high'] else hours * 0.15
        
        return TechnicalEstimate(
            story_points=story_points or 0,
            estimated_hours=hours,
            complexity_factor=1.0,
            risk_buffer_hours=risk_buffer,
            confidence_level="medium",
            breakdown={
                "analysis": hours * 0.15,
                "design": hours * 0.20,
                "coding": hours * 0.50,
                "testing": hours * 0.10,
                "review": hours * 0.05
            },
            assumptions=[
                "Requirements are clearly defined",
                "No major technical blockers",
                "Standard development environment"
            ],
            risks=[
                "Requirements may need clarification",
                "Integration complexity may be higher than expected"
            ]
        )
    
    def _rule_based_recommend_tech_stack(self, title: str, description: str,
                                        requirements: List[TechnicalRequirement]) -> List[TechStackRecommendation]:
        """Rule-based tech stack recommendations"""
        recommendations = []
        text_lower = (title + " " + description).lower()
        
        # Frontend recommendation
        if any(word in text_lower for word in ['ui', 'interface', 'web', 'frontend', 'form', 'page']):
            recommendations.append(TechStackRecommendation(
                category="frontend",
                recommended_tech=self.tech_stack_defaults['frontend']['tech'],
                alternatives=self.tech_stack_defaults['frontend']['alternatives'],
                reasoning=self.tech_stack_defaults['frontend']['reasoning'],
                pros=["Large ecosystem", "Good documentation", "Active community"],
                cons=["Learning curve", "Frequent updates"],
                experience_required="intermediate"
            ))
        
        # Backend recommendation
        if any(word in text_lower for word in ['api', 'backend', 'service', 'server', 'endpoint']):
            recommendations.append(TechStackRecommendation(
                category="backend", 
                recommended_tech=self.tech_stack_defaults['backend']['tech'],
                alternatives=self.tech_stack_defaults['backend']['alternatives'],
                reasoning=self.tech_stack_defaults['backend']['reasoning'],
                pros=["Fast performance", "Modern async support", "Good documentation"],
                cons=["Newer framework", "Smaller ecosystem than Django"],
                experience_required="intermediate"
            ))
        
        # Database recommendation
        if any(word in text_lower for word in ['data', 'database', 'store', 'persist', 'save']):
            recommendations.append(TechStackRecommendation(
                category="database",
                recommended_tech=self.tech_stack_defaults['database']['tech'],
                alternatives=self.tech_stack_defaults['database']['alternatives'],
                reasoning=self.tech_stack_defaults['database']['reasoning'],
                pros=["ACID compliance", "Rich feature set", "Good performance"],
                cons=["Setup complexity", "Memory usage"],
                experience_required="intermediate"
            ))
        
        # Always recommend testing
        recommendations.append(TechStackRecommendation(
            category="testing",
            recommended_tech=self.tech_stack_defaults['testing']['tech'],
            alternatives=self.tech_stack_defaults['testing']['alternatives'],
            reasoning=self.tech_stack_defaults['testing']['reasoning'],
            pros=["Comprehensive testing features", "Good Python integration"],
            cons=["Learning curve for advanced features"],
            experience_required="beginner"
        ))
        
        return recommendations
    
    def _rule_based_create_implementation_plan(self, title: str, description: str,
                                              requirements: List[TechnicalRequirement],
                                              tech_stack: List[TechStackRecommendation]) -> ImplementationPlan:
        """Rule-based implementation planning"""
        # Determine if this is frontend, backend, or full-stack
        has_frontend = any(tech.category == 'frontend' for tech in tech_stack)
        has_backend = any(tech.category == 'backend' for tech in tech_stack)
        has_database = any(tech.category == 'database' for tech in tech_stack)
        
        # Basic architecture approach
        if has_frontend and has_backend:
            arch_approach = "Full-stack application with separate frontend and backend components"
        elif has_frontend:
            arch_approach = "Frontend-focused application with client-side logic"
        elif has_backend:
            arch_approach = "Backend service with API endpoints"
        else:
            arch_approach = "Component-based development approach"
        
        # Basic file structure
        file_structure = {}
        if has_frontend:
            file_structure.update({
                "src/": ["components/", "services/", "utils/", "styles/"],
                "components/": [f"{title.replace(' ', '')}Component.tsx"],
                "services/": ["api.ts", "types.ts"],
                "utils/": ["helpers.ts"]
            })
        
        if has_backend:
            file_structure.update({
                "app/": ["main.py", "models/", "routes/", "services/"],
                "models/": ["models.py"],
                "routes/": ["api.py"],
                "services/": ["business_logic.py"]
            })
        
        # Basic implementation steps
        steps = [
            "Set up project structure and dependencies",
            "Implement core data models and types",
            "Create basic functionality without UI",
            "Add user interface components",
            "Implement business logic and validations", 
            "Add error handling and edge cases",
            "Write unit tests for core functionality",
            "Integration testing and bug fixes",
            "Documentation and deployment preparation"
        ]
        
        # Basic API endpoints if backend
        api_endpoints = []
        if has_backend:
            entity_name = title.lower().replace(' ', '_')
            api_endpoints = [
                {"method": "GET", "path": f"/api/{entity_name}", "purpose": f"Retrieve {title.lower()} data"},
                {"method": "POST", "path": f"/api/{entity_name}", "purpose": f"Create new {title.lower()}"},
                {"method": "PUT", "path": f"/api/{entity_name}/{{id}}", "purpose": f"Update {title.lower()}"},
                {"method": "DELETE", "path": f"/api/{entity_name}/{{id}}", "purpose": f"Delete {title.lower()}"}
            ]
        
        # Database changes if needed
        db_changes = []
        if has_database:
            db_changes = [
                f"Create table for {title.lower()} data",
                "Add necessary indexes for performance",
                "Set up relationships with existing tables"
            ]
        
        return ImplementationPlan(
            architecture_approach=arch_approach,
            component_breakdown=[
                {"name": f"{title}Component", "purpose": "Main functionality component", "dependencies": []},
                {"name": f"{title}Service", "purpose": "Business logic and data handling", "dependencies": ["database"]}
            ],
            file_structure=file_structure,
            database_changes=db_changes,
            api_endpoints=api_endpoints,
            tech_stack=tech_stack,
            implementation_steps=steps,
            testing_approach=[
                "Unit tests for individual functions",
                "Integration tests for component interaction",
                "End-to-end tests for user workflows"
            ],
            deployment_considerations=[
                "Environment configuration setup",
                "Database migration scripts",
                "Build and deployment pipeline"
            ]
        )
    
    def _determine_text_complexity(self, text: str) -> str:
        """Simple rule-based complexity determination from text"""
        text_lower = text.lower()
        
        high_count = sum(1 for word in self.complexity_indicators['high'] if word in text_lower)
        medium_count = sum(1 for word in self.complexity_indicators['medium'] if word in text_lower)
        
        if high_count >= 2:
            return "high"
        elif high_count >= 1 or medium_count >= 2:
            return "medium"
        else:
            return "low"