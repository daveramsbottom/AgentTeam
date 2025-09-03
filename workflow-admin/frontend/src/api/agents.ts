import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export interface AgentContext {
  specialization: string;
  responsibilities: string[];
  deliverables: string[];
  key_skills: string[];
  tools: string[];
  preferred_languages: string[];
  work_style: {
    communication_frequency: 'high' | 'medium' | 'low';
    collaboration_preference: 'independent' | 'collaborative';
    feedback_style: 'detailed' | 'concise';
    documentation_level: 'minimal' | 'standard' | 'comprehensive';
  };
  expertise_areas: string[];
  learning_preferences: {
    new_technologies: boolean;
    domain_expansion: boolean;
    skill_depth_vs_breadth: 'depth' | 'breadth' | 'balanced';
  };
}

export interface AgentType {
  id: number;
  name: string;
  description?: string;
  capabilities?: any;
  workflow_preferences?: any;
  default_config?: any;
  assigned_model_id?: number;
  model_config?: any;
  is_active: boolean;
  created_at: string;
  updated_at?: string;
}

export interface Agent {
  id: number;
  name: string;
  agent_type_id: number;
  description?: string;
  context: AgentContext;
  configuration?: any;
  credentials?: any;
  status: string;
  workload_capacity: number;
  current_workload: number;
  specializations?: any;
  performance_metrics?: any;
  last_active?: string;
  created_at: string;
  updated_at?: string;
  agent_type?: AgentType;
  team?: any;
}

export const agentsApi = {
  getAgents: async (): Promise<Agent[]> => {
    const response = await api.get('/api/v1/agents/');
    return response.data.items || response.data || [];
  },

  getAgent: async (id: number): Promise<Agent> => {
    const response = await api.get(`/api/v1/agents/${id}`);
    return response.data;
  },

  getAgentTypes: async (): Promise<AgentType[]> => {
    const response = await api.get('/api/v1/agents/types/');
    return response.data.items || response.data || [];
  },

  getAgentType: async (id: number): Promise<AgentType> => {
    const response = await api.get(`/api/v1/agents/types/${id}`);
    return response.data;
  },
};