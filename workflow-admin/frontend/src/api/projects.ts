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
  context?: string;  // Simple text description of what the project will achieve
  status?: string;
  priority?: string;
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
          context: 'Create an AI-powered multi-agent system that simulates professional software development teams with intelligent workflow orchestration and context-aware agent management. This system will automate story creation, technical analysis, and provide intelligent agent coordination.',
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
          context: 'Build a scalable, enterprise-grade e-commerce platform supporting multi-tenant operations with advanced analytics and AI-powered recommendations. The platform will handle high-volume transactions, integrate with legacy ERP systems, and provide comprehensive analytics dashboards.',
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
          context: 'Develop a cutting-edge mobile banking application that provides secure, intuitive financial services with AI-powered insights and personalized recommendations. The app will feature biometric authentication, real-time transaction processing, and comprehensive budgeting tools.',
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