import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export interface AIModel {
  id: number;
  name: string;
  provider: 'openai' | 'anthropic' | 'google' | 'azure' | 'local';
  model_id: string; // e.g., 'gpt-4', 'claude-3-opus', 'gemini-pro'
  description?: string;
  capabilities: {
    text_generation: boolean;
    code_generation: boolean;
    analysis: boolean;
    reasoning: boolean;
    conversation: boolean;
    function_calling: boolean;
  };
  context_window: number; // tokens
  cost_per_1k_tokens?: {
    input: number;
    output: number;
  };
  performance_metrics?: {
    speed: 'slow' | 'medium' | 'fast';
    quality: 'good' | 'excellent' | 'outstanding';
    reliability: 'moderate' | 'high' | 'very_high';
  };
  best_for: string[]; // e.g., ['coding', 'analysis', 'creative_writing']
  is_active: boolean;
  created_at: string;
  updated_at?: string;
}

export const modelsApi = {
  getModels: async (): Promise<AIModel[]> => {
    const response = await api.get('/api/v1/models/');
    return response.data.items || response.data || [];
  },

  getModel: async (id: number): Promise<AIModel> => {
    const response = await api.get(`/api/v1/models/${id}`);
    return response.data;
  },

  getModelsByCapability: async (capability: keyof AIModel['capabilities']): Promise<AIModel[]> => {
    const models = await modelsApi.getModels();
    return models.filter(model => model.capabilities[capability] && model.is_active);
  },

  getRecommendedModelsForAgentType: async (agentType: string): Promise<AIModel[]> => {
    const models = await modelsApi.getModels();
    
    // Define recommendations based on agent type
    const recommendations: Record<string, string[]> = {
      'Product Owner': ['general_purpose', 'requirements', 'product_management'],
      'Developer': ['coding', 'code_review', 'technical_analysis'],
      'Tester': ['analysis', 'reasoning'],
      'DevOps': ['coding', 'technical_analysis'],
    };

    const agentRecommendations = recommendations[agentType] || ['general_purpose'];
    
    return models
      .filter(model => model.is_active)
      .filter(model => 
        agentRecommendations.some(rec => model.best_for.includes(rec))
      )
      .sort((a, b) => {
        // Sort by quality, then by speed
        const qualityOrder = { 'outstanding': 3, 'excellent': 2, 'good': 1 };
        const speedOrder = { 'fast': 3, 'medium': 2, 'slow': 1 };
        
        const aQuality = qualityOrder[a.performance_metrics?.quality || 'good'];
        const bQuality = qualityOrder[b.performance_metrics?.quality || 'good'];
        
        if (aQuality !== bQuality) return bQuality - aQuality;
        
        const aSpeed = speedOrder[a.performance_metrics?.speed || 'medium'];
        const bSpeed = speedOrder[b.performance_metrics?.speed || 'medium'];
        
        return bSpeed - aSpeed;
      });
  },
};