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

export interface CreateProjectRequest {
  name: string;
  description?: string;
  context?: string;
  settings?: any;
  selected_contexts?: number[];
}

export const projectsApi = {
  getProjects: async (): Promise<Project[]> => {
    const response = await api.get('/api/v1/projects/');
    return response.data || [];
  },

  getProject: async (id: number): Promise<Project> => {
    try {
      const response = await api.get(`/api/v1/projects/${id}`);
      return response.data;
    } catch (error) {
      throw new Error(`Failed to fetch project ${id}`);
    }
  },

  createProject: async (projectData: CreateProjectRequest): Promise<Project> => {
    const response = await api.post('/api/v1/projects/', projectData);
    return response.data;
  },
};