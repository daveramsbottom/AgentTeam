"""
Story Breakdown Logic for AgentTeam
Handles project goal analysis and story creation
"""
import logging
from typing import List, Dict, Any
from .states import StoryBreakdown, TaskBreakdown, Priority, TaskType

logger = logging.getLogger(__name__)


class StoryBreakdownEngine:
    """Handles breaking down project goals into user stories and tasks"""
    
    def __init__(self):
        self.vague_indicators = [
            "simple", "basic", "user-friendly", "intuitive", 
            "scalable", "robust", "modern", "clean", "nice"
        ]
    
    def analyze_project_goal(self, project_goal: str) -> Dict[str, Any]:
        """Analyze project goal and determine if clarification is needed"""
        logger.info("🔍 Analyzing project goal for clarity and completeness...")
        
        analysis_questions = []
        
        # Check for vague terms
        found_vague = [term for term in self.vague_indicators 
                      if term.lower() in project_goal.lower()]
        
        if found_vague:
            analysis_questions.append(
                f"The goal mentions '{', '.join(found_vague)}' - can you provide "
                f"more specific requirements for these aspects?"
            )
        
        # Check for missing technical details
        if "web" in project_goal.lower() and "api" not in project_goal.lower():
            analysis_questions.append(
                "Will this web application need API integration or backend services?"
            )
        
        if "user" in project_goal.lower() and "authentication" not in project_goal.lower():
            analysis_questions.append(
                "What type of user authentication/authorization is needed?"
            )
        
        # Check for scope clarity
        if len(project_goal.split()) < 10:
            analysis_questions.append(
                "The project goal seems quite brief - can you provide more details "
                "about the expected features and functionality?"
            )
        
        # Check for data requirements
        if any(word in project_goal.lower() for word in ["manage", "store", "save", "data"]):
            if "database" not in project_goal.lower():
                analysis_questions.append(
                    "What type of data storage/database requirements do you have?"
                )
        
        clarification_needed = len(analysis_questions) > 0
        
        logger.info(f"Analysis complete. Clarification needed: {clarification_needed}")
        if clarification_needed:
            logger.info(f"Questions to ask: {len(analysis_questions)}")
        
        return {
            "clarification_needed": clarification_needed,
            "questions": analysis_questions,
            "goal_length": len(project_goal.split()),
            "complexity_indicators": found_vague
        }
    
    def create_stories_for_project(self, project_goal: str) -> List[StoryBreakdown]:
        """Create user stories based on project goal"""
        logger.info("📝 Creating user stories based on project goal...")
        
        goal_lower = project_goal.lower()
        stories = []
        
        # Determine project type and create appropriate stories
        if self._is_web_app_project(goal_lower):
            stories.extend(self._create_web_app_stories(project_goal))
        elif self._is_api_project(goal_lower):
            stories.extend(self._create_api_stories(project_goal))
        elif self._is_mobile_project(goal_lower):
            stories.extend(self._create_mobile_stories(project_goal))
        else:
            stories.extend(self._create_generic_stories(project_goal))
        
        # Always add infrastructure and testing stories
        stories.extend(self._create_common_stories(project_goal))
        
        logger.info(f"Created {len(stories)} user stories")
        return stories
    
    def _is_web_app_project(self, goal: str) -> bool:
        """Check if project is a web application"""
        web_indicators = ["web app", "website", "web application", "frontend", "dashboard"]
        return any(indicator in goal for indicator in web_indicators)
    
    def _is_api_project(self, goal: str) -> bool:
        """Check if project is an API"""
        api_indicators = ["api", "rest", "backend", "service", "microservice"]
        return any(indicator in goal for indicator in api_indicators)
    
    def _is_mobile_project(self, goal: str) -> bool:
        """Check if project is mobile"""
        mobile_indicators = ["mobile", "app", "ios", "android", "react native"]
        return any(indicator in goal for indicator in mobile_indicators)
    
    def _create_web_app_stories(self, goal: str) -> List[StoryBreakdown]:
        """Create stories for web applications"""
        return [
            StoryBreakdown(
                title="Design User Interface and Experience",
                description="As a product owner, I need UI/UX designs to guide development and ensure a great user experience",
                acceptance_criteria=[
                    "User flow diagrams are created",
                    "Wireframes for main pages are designed",
                    "Design system (colors, fonts, components) is defined",
                    "Responsive design considerations are documented",
                    "Designs are reviewed and approved by stakeholders"
                ],
                priority=Priority.HIGH.value,
                estimated_points=5,
                tasks=[
                    TaskBreakdown("Create user flow diagrams", "Map out user journeys", TaskType.DESIGN.value, 4),
                    TaskBreakdown("Design wireframes", "Create page layouts and structure", TaskType.DESIGN.value, 6),
                    TaskBreakdown("Define design system", "Create consistent styling guide", TaskType.DESIGN.value, 4),
                    TaskBreakdown("Review and refine designs", "Stakeholder review and approval", TaskType.REVIEW.value, 2)
                ]
            ),
            StoryBreakdown(
                title="Implement Core Web Application Features",
                description=f"As a user, I need the main functionality described in: {goal}",
                acceptance_criteria=[
                    "Core features are fully implemented",
                    "User interface is responsive and functional",
                    "Navigation between pages works correctly",
                    "Basic error handling is implemented",
                    "Performance is acceptable on target browsers"
                ],
                priority=Priority.HIGH.value,
                estimated_points=8,
                tasks=[
                    TaskBreakdown("Set up frontend framework", "Initialize React/Vue/Angular project", TaskType.DEVELOPMENT.value, 4),
                    TaskBreakdown("Implement core components", "Build reusable UI components", TaskType.DEVELOPMENT.value, 8),
                    TaskBreakdown("Add routing and navigation", "Implement page routing", TaskType.DEVELOPMENT.value, 3),
                    TaskBreakdown("Implement main features", "Code the core functionality", TaskType.DEVELOPMENT.value, 12),
                    TaskBreakdown("Add error handling", "Implement user-friendly error states", TaskType.DEVELOPMENT.value, 3)
                ]
            )
        ]
    
    def _create_api_stories(self, goal: str) -> List[StoryBreakdown]:
        """Create stories for API projects"""
        return [
            StoryBreakdown(
                title="Design API Architecture",
                description="As a developer, I need a well-designed API architecture to ensure scalability and maintainability",
                acceptance_criteria=[
                    "API endpoints and methods are defined",
                    "Data models and database schema are designed",
                    "Authentication and authorization strategy is planned",
                    "API documentation structure is outlined",
                    "Error handling strategy is defined"
                ],
                priority=Priority.HIGH.value,
                estimated_points=5,
                tasks=[
                    TaskBreakdown("Design API endpoints", "Define REST endpoints, methods, and parameters", TaskType.DEVELOPMENT.value, 4),
                    TaskBreakdown("Design data models", "Create database schema and data relationships", TaskType.DEVELOPMENT.value, 4),
                    TaskBreakdown("Plan authentication", "Design JWT/OAuth authentication strategy", TaskType.DEVELOPMENT.value, 3),
                    TaskBreakdown("Create API documentation", "Set up OpenAPI/Swagger documentation", TaskType.DOCUMENTATION.value, 2)
                ]
            ),
            StoryBreakdown(
                title="Implement API Endpoints",
                description=f"As a client application, I need API endpoints that provide: {goal}",
                acceptance_criteria=[
                    "All planned endpoints are implemented and functional",
                    "Proper HTTP status codes are returned",
                    "Request and response validation is in place",
                    "Authentication middleware is working",
                    "API returns consistent JSON responses"
                ],
                priority=Priority.HIGH.value,
                estimated_points=8,
                tasks=[
                    TaskBreakdown("Set up API framework", "Initialize FastAPI/Express/Django project", TaskType.DEVELOPMENT.value, 3),
                    TaskBreakdown("Implement CRUD operations", "Create basic Create, Read, Update, Delete endpoints", TaskType.DEVELOPMENT.value, 8),
                    TaskBreakdown("Add input validation", "Implement request validation and sanitization", TaskType.DEVELOPMENT.value, 4),
                    TaskBreakdown("Implement authentication", "Add JWT/session authentication", TaskType.DEVELOPMENT.value, 5),
                    TaskBreakdown("Add error handling", "Implement consistent error responses", TaskType.DEVELOPMENT.value, 3)
                ]
            )
        ]
    
    def _create_mobile_stories(self, goal: str) -> List[StoryBreakdown]:
        """Create stories for mobile projects"""
        return [
            StoryBreakdown(
                title="Design Mobile User Interface",
                description="As a product owner, I need mobile-optimized designs that work well on various screen sizes",
                acceptance_criteria=[
                    "Mobile wireframes are created for key screens",
                    "Touch interactions and gestures are designed",
                    "Navigation patterns are mobile-friendly",
                    "Designs work on both iOS and Android",
                    "Accessibility considerations are included"
                ],
                priority=Priority.HIGH.value,
                estimated_points=5,
                tasks=[
                    TaskBreakdown("Create mobile wireframes", "Design mobile-specific layouts", TaskType.DESIGN.value, 5),
                    TaskBreakdown("Design interaction patterns", "Define touch gestures and animations", TaskType.DESIGN.value, 3),
                    TaskBreakdown("Test on different devices", "Validate designs on various screen sizes", TaskType.TESTING.value, 2)
                ]
            ),
            StoryBreakdown(
                title="Implement Mobile Application",
                description=f"As a mobile user, I need an app that provides: {goal}",
                acceptance_criteria=[
                    "Core mobile features are implemented",
                    "App works on both iOS and Android (if React Native)",
                    "Touch interactions are responsive",
                    "App follows platform design guidelines",
                    "Performance is optimized for mobile devices"
                ],
                priority=Priority.HIGH.value,
                estimated_points=8,
                tasks=[
                    TaskBreakdown("Set up mobile development environment", "Configure React Native/Flutter/native setup", TaskType.DEVELOPMENT.value, 4),
                    TaskBreakdown("Implement core screens", "Build main application screens", TaskType.DEVELOPMENT.value, 10),
                    TaskBreakdown("Add navigation", "Implement mobile navigation patterns", TaskType.DEVELOPMENT.value, 3),
                    TaskBreakdown("Optimize performance", "Improve loading times and responsiveness", TaskType.DEVELOPMENT.value, 4)
                ]
            )
        ]
    
    def _create_generic_stories(self, goal: str) -> List[StoryBreakdown]:
        """Create generic stories for any project type"""
        return [
            StoryBreakdown(
                title="Project Planning and Requirements Analysis",
                description="As a team, we need clear requirements and technical planning to build the right solution",
                acceptance_criteria=[
                    "Functional requirements are documented",
                    "Non-functional requirements are defined",
                    "Technical architecture is decided",
                    "Development timeline is estimated",
                    "Risk assessment is completed"
                ],
                priority=Priority.HIGH.value,
                estimated_points=3,
                tasks=[
                    TaskBreakdown("Document requirements", "Gather and document detailed requirements", TaskType.ANALYSIS.value, 4),
                    TaskBreakdown("Technical architecture planning", "Design system architecture and tech stack", TaskType.DEVELOPMENT.value, 4),
                    TaskBreakdown("Create project timeline", "Estimate tasks and create development schedule", TaskType.ANALYSIS.value, 2),
                    TaskBreakdown("Risk assessment", "Identify and plan for potential risks", TaskType.ANALYSIS.value, 2)
                ]
            ),
            StoryBreakdown(
                title="Core Implementation",
                description=f"As a user, I need the main functionality described in: {goal}",
                acceptance_criteria=[
                    "Core features are implemented according to requirements",
                    "Code follows established quality standards",
                    "Basic documentation is created",
                    "Performance meets acceptable standards",
                    "Security considerations are addressed"
                ],
                priority=Priority.HIGH.value,
                estimated_points=8,
                tasks=[
                    TaskBreakdown("Set up development environment", "Configure development tools and environment", TaskType.DEVELOPMENT.value, 2),
                    TaskBreakdown("Implement core functionality", "Build the main features and logic", TaskType.DEVELOPMENT.value, 10),
                    TaskBreakdown("Add security measures", "Implement basic security practices", TaskType.DEVELOPMENT.value, 3),
                    TaskBreakdown("Create documentation", "Document code and functionality", TaskType.DOCUMENTATION.value, 3)
                ]
            )
        ]
    
    def _create_common_stories(self, goal: str) -> List[StoryBreakdown]:
        """Create common stories that apply to most projects"""
        return [
            StoryBreakdown(
                title="Set Up Development Infrastructure",
                description="As a development team, we need proper infrastructure and tools to work efficiently",
                acceptance_criteria=[
                    "Version control repository is set up",
                    "CI/CD pipeline is configured",
                    "Development environment is documented",
                    "Code quality tools are integrated",
                    "Deployment process is automated"
                ],
                priority=Priority.MEDIUM.value,
                estimated_points=3,
                tasks=[
                    TaskBreakdown("Set up Git repository", "Initialize repo with proper structure", TaskType.DEVELOPMENT.value, 1),
                    TaskBreakdown("Configure CI/CD", "Set up automated testing and deployment", TaskType.DEVELOPMENT.value, 4),
                    TaskBreakdown("Set up code quality tools", "Configure linting, formatting, and code analysis", TaskType.DEVELOPMENT.value, 2),
                    TaskBreakdown("Document setup process", "Create setup and deployment documentation", TaskType.DOCUMENTATION.value, 1)
                ]
            ),
            StoryBreakdown(
                title="Comprehensive Testing and Quality Assurance",
                description="As a team, we need thorough testing to ensure the solution is reliable and bug-free",
                acceptance_criteria=[
                    "Unit tests cover core functionality",
                    "Integration tests validate complete workflows",
                    "Manual testing is completed for user scenarios",
                    "Performance testing meets requirements",
                    "Security testing is performed",
                    "All critical bugs are fixed"
                ],
                priority=Priority.MEDIUM.value,
                estimated_points=5,
                tasks=[
                    TaskBreakdown("Write unit tests", "Create comprehensive unit test suite", TaskType.TESTING.value, 6),
                    TaskBreakdown("Integration testing", "Test complete user workflows and API integrations", TaskType.TESTING.value, 4),
                    TaskBreakdown("Manual testing", "Perform manual QA testing of user scenarios", TaskType.TESTING.value, 3),
                    TaskBreakdown("Performance testing", "Test application performance and scalability", TaskType.TESTING.value, 2),
                    TaskBreakdown("Security testing", "Basic security vulnerability testing", TaskType.TESTING.value, 2),
                    TaskBreakdown("Bug fixes", "Address issues found during testing", TaskType.DEVELOPMENT.value, 4)
                ]
            )
        ]
