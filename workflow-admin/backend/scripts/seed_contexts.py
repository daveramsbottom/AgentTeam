#!/usr/bin/env python3
"""
Seed script for organizational contexts
Creates sample tech stack, security, compliance, and business guideline contexts
"""

import sys
import os
from sqlalchemy.orm import Session

# Add the parent directory to Python path to import our modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database.database import get_db, engine
from sqlalchemy.orm import sessionmaker
from app.database.models import OrganizationalContext

def create_sample_contexts(db: Session):
    """Create sample organizational contexts for project selection"""
    
    # Tech Stack contexts
    tech_contexts = [
        {
            'context_category': 'tech_standards',
            'context_name': 'React TypeScript Stack',
            'description': 'Modern React web application with TypeScript',
            'content': {
                'summary': 'React + TypeScript + Material-UI frontend stack',
                'technologies': ['React', 'TypeScript', 'Material-UI', 'Vite', 'ESLint'],
                'requirements': [
                    'Use functional components with hooks',
                    'Implement strict TypeScript types',
                    'Follow Material-UI design patterns',
                    'Use Vite for build tooling'
                ],
                'best_practices': [
                    'Component composition over inheritance',
                    'Proper error boundaries',
                    'Consistent state management patterns'
                ]
            },
            'applicable_agent_types': ['frontend_developer', 'full_stack_developer'],
            'priority': 8,
            'tags': ['frontend', 'react', 'typescript', 'web']
        },
        {
            'context_category': 'tech_standards',
            'context_name': 'FastAPI Python Backend',
            'description': 'Python FastAPI backend with SQLAlchemy',
            'content': {
                'summary': 'FastAPI + SQLAlchemy + PostgreSQL backend stack',
                'technologies': ['FastAPI', 'SQLAlchemy', 'PostgreSQL', 'Pydantic', 'Alembic'],
                'requirements': [
                    'Use FastAPI for API framework',
                    'SQLAlchemy ORM for database operations',
                    'Pydantic models for data validation',
                    'Alembic for database migrations'
                ],
                'best_practices': [
                    'Async/await for database operations',
                    'Proper dependency injection',
                    'Comprehensive API documentation'
                ]
            },
            'applicable_agent_types': ['backend_developer', 'full_stack_developer'],
            'priority': 8,
            'tags': ['backend', 'python', 'fastapi', 'api']
        },
        {
            'context_category': 'tech_standards',
            'context_name': 'Docker Containerization',
            'description': 'Docker containerization standards',
            'content': {
                'summary': 'Docker containers with Docker Compose orchestration',
                'technologies': ['Docker', 'Docker Compose', 'Multi-stage builds'],
                'requirements': [
                    'All services must be containerized',
                    'Use multi-stage builds for optimization',
                    'Docker Compose for local development',
                    'Environment-based configuration'
                ],
                'best_practices': [
                    'Minimal base images (Alpine when possible)',
                    'Non-root user execution',
                    'Proper health checks',
                    'Layer caching optimization'
                ]
            },
            'applicable_agent_types': ['devops_engineer', 'backend_developer'],
            'priority': 7,
            'tags': ['devops', 'docker', 'containers', 'deployment']
        }
    ]
    
    # Security contexts
    security_contexts = [
        {
            'context_category': 'security',
            'context_name': 'API Security Standards',
            'description': 'Security requirements for API development',
            'content': {
                'summary': 'Comprehensive API security guidelines',
                'requirements': [
                    'All endpoints must be authenticated',
                    'Use HTTPS/TLS encryption',
                    'Implement rate limiting',
                    'Input validation and sanitization',
                    'SQL injection prevention',
                    'CORS configuration'
                ],
                'authentication': {
                    'method': 'JWT tokens',
                    'expiration': '24 hours',
                    'refresh_mechanism': 'Required'
                },
                'validation': [
                    'Pydantic models for request validation',
                    'Size limits on file uploads',
                    'Whitelist allowed file types'
                ]
            },
            'applicable_agent_types': ['backend_developer', 'security_engineer'],
            'priority': 9,
            'tags': ['security', 'api', 'authentication', 'validation']
        },
        {
            'context_category': 'security',
            'context_name': 'Data Protection',
            'description': 'Data handling and protection standards',
            'content': {
                'summary': 'Data encryption and privacy protection requirements',
                'requirements': [
                    'Encrypt sensitive data at rest',
                    'Use parameterized queries',
                    'No plaintext password storage',
                    'Regular security audits',
                    'Access logging and monitoring'
                ],
                'encryption': {
                    'at_rest': 'AES-256',
                    'in_transit': 'TLS 1.3',
                    'keys_management': 'Environment variables'
                },
                'privacy': [
                    'Data minimization principles',
                    'User consent tracking',
                    'Right to deletion support'
                ]
            },
            'applicable_agent_types': ['backend_developer', 'security_engineer', 'dba'],
            'priority': 10,
            'tags': ['security', 'data', 'encryption', 'privacy']
        }
    ]
    
    # Compliance contexts
    compliance_contexts = [
        {
            'context_category': 'compliance',
            'context_name': 'GDPR Compliance',
            'description': 'General Data Protection Regulation requirements',
            'content': {
                'summary': 'GDPR compliance for EU data processing',
                'requirements': [
                    'Explicit user consent for data collection',
                    'Data portability features',
                    'Right to erasure implementation',
                    'Privacy by design principles',
                    'Data breach notification procedures'
                ],
                'data_handling': {
                    'legal_basis': 'Consent or legitimate interest',
                    'retention_policy': 'Define clear retention periods',
                    'cross_border': 'Adequacy decisions required'
                },
                'user_rights': [
                    'Access to personal data',
                    'Data rectification',
                    'Data erasure',
                    'Data portability',
                    'Processing restriction'
                ]
            },
            'applicable_agent_types': ['backend_developer', 'product_manager', 'legal'],
            'priority': 9,
            'tags': ['compliance', 'gdpr', 'privacy', 'data-protection']
        },
        {
            'context_category': 'compliance',
            'context_name': 'Accessibility Standards',
            'description': 'WCAG 2.1 AA accessibility compliance',
            'content': {
                'summary': 'Web accessibility guidelines compliance',
                'requirements': [
                    'WCAG 2.1 Level AA compliance',
                    'Keyboard navigation support',
                    'Screen reader compatibility',
                    'Color contrast ratios (4.5:1 minimum)',
                    'Alternative text for images'
                ],
                'testing': {
                    'tools': ['axe-core', 'WAVE', 'Screen readers'],
                    'frequency': 'Every sprint',
                    'coverage': 'All user-facing features'
                },
                'implementation': [
                    'Semantic HTML structure',
                    'ARIA labels where needed',
                    'Focus management',
                    'Responsive design principles'
                ]
            },
            'applicable_agent_types': ['frontend_developer', 'ui_designer', 'qa_engineer'],
            'priority': 8,
            'tags': ['compliance', 'accessibility', 'wcag', 'ui']
        }
    ]
    
    # Business Guidelines contexts
    business_contexts = [
        {
            'context_category': 'business_guidelines',
            'context_name': 'Agile Development Process',
            'description': 'Agile methodology and sprint planning guidelines',
            'content': {
                'summary': 'Scrum-based agile development process',
                'methodology': 'Scrum',
                'sprint_length': '2 weeks',
                'ceremonies': [
                    'Daily standups (15 min)',
                    'Sprint planning (2 hours)',
                    'Sprint review (1 hour)',
                    'Sprint retrospective (1 hour)'
                ],
                'requirements': [
                    'User stories with acceptance criteria',
                    'Story point estimation',
                    'Definition of Done compliance',
                    'Regular backlog grooming'
                ],
                'tools': {
                    'project_management': 'Jira',
                    'communication': 'Slack',
                    'documentation': 'Confluence',
                    'version_control': 'Git'
                }
            },
            'applicable_agent_types': ['product_manager', 'scrum_master', 'developer'],
            'priority': 7,
            'tags': ['business', 'agile', 'scrum', 'process']
        },
        {
            'context_category': 'business_guidelines',
            'context_name': 'Code Quality Standards',
            'description': 'Code review and quality assurance guidelines',
            'content': {
                'summary': 'Code quality and review process standards',
                'requirements': [
                    'All code must be peer reviewed',
                    'Unit test coverage > 80%',
                    'Integration tests for critical paths',
                    'Automated linting and formatting',
                    'Documentation for public APIs'
                ],
                'review_process': {
                    'reviewers_required': 2,
                    'approval_threshold': '100%',
                    'blocked_merge': 'Until all issues resolved'
                },
                'testing': {
                    'unit_coverage': '80% minimum',
                    'integration_tests': 'Required for API changes',
                    'e2e_tests': 'Critical user journeys'
                },
                'documentation': [
                    'README for all repositories',
                    'API documentation (OpenAPI)',
                    'Architecture decision records',
                    'Deployment guides'
                ]
            },
            'applicable_agent_types': ['developer', 'tech_lead', 'qa_engineer'],
            'priority': 8,
            'tags': ['business', 'quality', 'code-review', 'testing']
        }
    ]
    
    # Combine all contexts
    all_contexts = tech_contexts + security_contexts + compliance_contexts + business_contexts
    
    # Insert contexts into database
    for context_data in all_contexts:
        # Check if context already exists
        existing = db.query(OrganizationalContext).filter(
            OrganizationalContext.context_category == context_data['context_category'],
            OrganizationalContext.context_name == context_data['context_name']
        ).first()
        
        if not existing:
            context = OrganizationalContext(**context_data)
            db.add(context)
            print(f"Created context: {context_data['context_category']} - {context_data['context_name']}")
        else:
            print(f"Context already exists: {context_data['context_category']} - {context_data['context_name']}")
    
    db.commit()
    print(f"\n✅ Successfully processed {len(all_contexts)} organizational contexts")

def main():
    """Main function to seed contexts"""
    print("🌱 Seeding organizational contexts...")
    
    # Create database session
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        create_sample_contexts(db)
        print("🎉 Context seeding completed successfully!")
    except Exception as e:
        print(f"❌ Error seeding contexts: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    main()