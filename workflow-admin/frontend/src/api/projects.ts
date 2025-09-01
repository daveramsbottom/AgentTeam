import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export interface ProjectContext {
  purpose: string;
  scope: string;
  limitations?: string;
  requirements: {
    functional: string[];
    non_functional: string[];
    business: string[];
  };
  success_criteria: string[];
  stakeholders: {
    name: string;
    role: string;
    contact: string;
  }[];
  timeline: {
    start_date: string;
    target_completion: string;
    milestones: {
      name: string;
      date: string;
      deliverables: string[];
    }[];
  };
  budget?: {
    total_budget: number;
    currency: string;
    allocation: Record<string, number>;
  };
  technology_preferences: {
    preferred_stack: string[];
    avoided_technologies: string[];
    infrastructure: string[];
  };
  compliance_requirements?: {
    security: string[];
    regulatory: string[];
    accessibility: string[];
  };
  integration_requirements?: {
    external_apis: string[];
    data_sources: string[];
    third_party_tools: string[];
  };
}

export interface Project {
  id: number;
  name: string;
  description?: string;
  context: ProjectContext;
  status: string;
  priority: string;
  settings?: any;
  created_at: string;
  updated_at?: string;
  // Computed fields
  team_count?: number;
  agent_count?: number;
  progress?: number;
}

export const projectsApi = {
  getProjects: async (): Promise<Project[]> => {
    try {
      const response = await api.get('/api/v1/projects/');
      return response.data.items || response.data || [];
    } catch (error) {
      console.warn('Projects API failed, returning mock data:', error);
      return [
        {
          id: 1,
          name: 'AgentTeam Multi-Agent System',
          description: 'AI-powered development team simulation with workflow orchestration',
          context: {
            purpose: 'Create an AI-powered multi-agent system that simulates professional software development teams with intelligent workflow orchestration and context-aware agent management.',
            scope: 'Full-stack development including AI agent creation, workflow management, real-time communication integration (Slack, Jira), and database-driven configuration system.',
            limitations: 'Limited to development environment initially, requires OpenAI API access, depends on external integrations (Slack/Jira availability)',
            requirements: {
              functional: [
                'AI agent creation and management',
                'Workflow orchestration and execution',
                'Real-time Slack communication',
                'Jira integration for project management',
                'Context inheritance system',
                'Performance monitoring and analytics'
              ],
              non_functional: [
                'Sub-second response times for agent interactions',
                '99.9% uptime for core services',
                'Scalable to 100+ concurrent agents',
                'Secure handling of API credentials'
              ],
              business: [
                'Reduce manual project setup time by 80%',
                'Improve story creation consistency',
                'Enable rapid team scaling'
              ]
            },
            success_criteria: [
              'AgentIan creates coherent user stories within 5 minutes',
              'AgentPete provides accurate technical estimates within 3 minutes',
              'End-to-end project setup automated in under 15 minutes',
              'User satisfaction rating above 4.5/5'
            ],
            stakeholders: [
              { name: 'Development Team', role: 'Primary Users', contact: 'dev-team@company.com' },
              { name: 'Product Management', role: 'Requirements Source', contact: 'pm@company.com' },
              { name: 'Engineering Leadership', role: 'Strategic Oversight', contact: 'eng-lead@company.com' }
            ],
            timeline: {
              start_date: '2024-08-01',
              target_completion: '2024-12-31',
              milestones: [
                { name: 'MVP Release', date: '2024-09-30', deliverables: ['Core agent workflows', 'Basic UI'] },
                { name: 'Beta Release', date: '2024-11-15', deliverables: ['Full feature set', 'Performance optimization'] },
                { name: 'Production Release', date: '2024-12-31', deliverables: ['Scale testing', 'Documentation'] }
              ]
            },
            budget: {
              total_budget: 150000,
              currency: 'USD',
              allocation: {
                'development': 80000,
                'infrastructure': 30000,
                'external_services': 25000,
                'testing_qa': 15000
              }
            },
            technology_preferences: {
              preferred_stack: ['python', 'typescript', 'react', 'fastapi', 'postgresql', 'docker'],
              avoided_technologies: ['php', 'legacy_frameworks'],
              infrastructure: ['docker_compose', 'cloud_native_ready', 'microservices_architecture']
            },
            compliance_requirements: {
              security: ['API_key_encryption', 'secure_communication', 'audit_logging'],
              regulatory: ['GDPR_compliance', 'data_retention_policies'],
              accessibility: ['WCAG_2.1_AA', 'keyboard_navigation']
            },
            integration_requirements: {
              external_apis: ['OpenAI_GPT4', 'Slack_API', 'Jira_REST_API'],
              data_sources: ['project_databases', 'user_configurations'],
              third_party_tools: ['Docker', 'Postman', 'Newman']
            }
          },
          status: 'active',
          priority: 'high',
          team_count: 2,
          agent_count: 3,
          progress: 65,
          created_at: new Date().toISOString(),
        },
        {
          id: 2,
          name: 'Enterprise E-commerce Platform',
          description: 'Large-scale e-commerce platform with microservices architecture',
          context: {
            purpose: 'Build a scalable, enterprise-grade e-commerce platform supporting multi-tenant operations with advanced analytics and AI-powered recommendations.',
            scope: 'Full e-commerce ecosystem including user management, product catalog, payment processing, order fulfillment, analytics dashboard, and mobile applications.',
            limitations: 'Must integrate with legacy ERP systems, limited to specific payment gateways, 18-month delivery timeline',
            requirements: {
              functional: [
                'User registration and authentication',
                'Product catalog management',
                'Shopping cart and checkout',
                'Payment processing integration',
                'Order management system',
                'Inventory tracking',
                'Customer support portal',
                'Analytics and reporting'
              ],
              non_functional: [
                'Handle 10,000 concurrent users',
                '99.99% uptime requirement',
                'Sub-200ms page load times',
                'PCI DSS compliance',
                'Mobile-first responsive design'
              ],
              business: [
                'Support $50M annual revenue',
                'Reduce operational costs by 30%',
                'Improve customer satisfaction to 4.8/5'
              ]
            },
            success_criteria: [
              'Successfully process 1000+ orders per day',
              'Achieve 99.99% payment success rate',
              'Mobile app rating above 4.5 stars',
              'Page load times under 200ms'
            ],
            stakeholders: [
              { name: 'Business Owner', role: 'Executive Sponsor', contact: 'ceo@ecommerce.com' },
              { name: 'Product Team', role: 'Requirements Owner', contact: 'product@ecommerce.com' },
              { name: 'Customer Success', role: 'User Advocate', contact: 'success@ecommerce.com' }
            ],
            timeline: {
              start_date: '2024-09-01',
              target_completion: '2026-03-01',
              milestones: [
                { name: 'Foundation Phase', date: '2024-12-31', deliverables: ['Core services', 'User management'] },
                { name: 'Commerce Phase', date: '2025-06-30', deliverables: ['Product catalog', 'Payment system'] },
                { name: 'Advanced Phase', date: '2025-12-31', deliverables: ['Analytics', 'Mobile apps'] },
                { name: 'Launch Phase', date: '2026-03-01', deliverables: ['Production deployment', 'User training'] }
              ]
            },
            technology_preferences: {
              preferred_stack: ['java', 'spring_boot', 'react', 'kotlin', 'postgresql', 'redis', 'elasticsearch'],
              avoided_technologies: ['monolithic_architecture', 'legacy_databases'],
              infrastructure: ['kubernetes', 'aws', 'microservices', 'event_driven_architecture']
            },
            compliance_requirements: {
              security: ['PCI_DSS', 'data_encryption', 'secure_authentication', 'vulnerability_scanning'],
              regulatory: ['GDPR', 'CCPA', 'PSD2_compliance'],
              accessibility: ['WCAG_2.1_AA', 'screen_reader_support']
            }
          },
          status: 'planning',
          priority: 'high',
          team_count: 4,
          agent_count: 12,
          progress: 15,
          created_at: new Date().toISOString(),
        },
        {
          id: 3,
          name: 'Mobile Banking Application',
          description: 'Secure mobile banking app with biometric authentication and AI-powered insights',
          context: {
            purpose: 'Develop a cutting-edge mobile banking application that provides secure, intuitive financial services with AI-powered insights and personalized recommendations.',
            scope: 'Native iOS and Android applications with core banking features, biometric security, budgeting tools, and integration with existing banking infrastructure.',
            limitations: 'Strict regulatory compliance requirements, must work with legacy banking systems, limited to specific regions initially',
            requirements: {
              functional: [
                'Account balance and transaction history',
                'Money transfers and payments',
                'Bill payment and scheduling',
                'Biometric authentication (fingerprint, face)',
                'AI-powered spending insights',
                'Budgeting and savings goals',
                'Customer support chat',
                'Security alerts and controls'
              ],
              non_functional: [
                'Bank-grade security standards',
                '99.999% uptime requirement',
                'Real-time transaction processing',
                'Offline mode for basic features',
                'Support for accessibility features'
              ],
              business: [
                'Increase mobile adoption to 80%',
                'Reduce support call volume by 40%',
                'Improve customer engagement by 60%'
              ]
            },
            success_criteria: [
              'App store rating above 4.7 stars',
              'Transaction success rate 99.99%',
              'Biometric authentication adoption >90%',
              'Customer satisfaction score >4.8/5'
            ],
            stakeholders: [
              { name: 'Bank Leadership', role: 'Executive Sponsor', contact: 'exec@bank.com' },
              { name: 'Compliance Team', role: 'Regulatory Oversight', contact: 'compliance@bank.com' },
              { name: 'Customer Experience', role: 'User Advocate', contact: 'cx@bank.com' }
            ],
            timeline: {
              start_date: '2024-10-01',
              target_completion: '2025-08-31',
              milestones: [
                { name: 'Security Foundation', date: '2024-12-31', deliverables: ['Security architecture', 'Authentication system'] },
                { name: 'Core Banking Features', date: '2025-03-31', deliverables: ['Account management', 'Transfers'] },
                { name: 'AI Features', date: '2025-06-30', deliverables: ['Spending insights', 'Recommendations'] },
                { name: 'Market Launch', date: '2025-08-31', deliverables: ['App store release', 'Marketing campaign'] }
              ]
            },
            technology_preferences: {
              preferred_stack: ['swift', 'kotlin', 'react_native', 'node_js', 'java', 'postgresql', 'redis'],
              avoided_technologies: ['hybrid_frameworks', 'unsecured_protocols'],
              infrastructure: ['aws', 'kubernetes', 'secure_cloud', 'cdn']
            },
            compliance_requirements: {
              security: ['SOX_compliance', 'PCI_DSS', 'multi_factor_auth', 'encryption_at_rest'],
              regulatory: ['FFIEC', 'GLBA', 'state_banking_regulations'],
              accessibility: ['ADA_compliance', 'screen_reader_support', 'voice_control']
            }
          },
          status: 'active',
          priority: 'critical',
          team_count: 3,
          agent_count: 8,
          progress: 35,
          created_at: new Date().toISOString(),
        },
      ];
    }
  },

  getProject: async (id: number): Promise<Project> => {
    try {
      const response = await api.get(`/api/v1/projects/${id}`);
      return response.data;
    } catch (error) {
      throw new Error(`Failed to fetch project ${id}`);
    }
  },
};