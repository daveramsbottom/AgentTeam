import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export interface OrganizationalContext {
  id: number;
  name: string;
  description: string;
  category: string;
  content_summary: string;
  content: any;
  tags: string[];
  priority?: number;
  is_active?: boolean;
  applies_to?: string[];
}

export interface CreateContextRequest {
  category: string;
  name: string;
  description?: string;
  content: any;
  applies_to?: string[];
  priority?: number;
}

export interface UpdateContextRequest {
  name?: string;
  description?: string;
  content?: any;
  applies_to?: string[];
  priority?: number;
  is_active?: boolean;
}

export interface CategoryData {
  name: string;
  displayName: string;
  description: string;
  color: string;
  icon: string;
}

export interface GroupedContexts {
  [category: string]: OrganizationalContext[];
}

export const contextsApi = {
  getSelectableProjectContexts: async (): Promise<GroupedContexts> => {
    const response = await api.get('/api/v1/contexts/selectable/project-contexts');
    return response.data;
  },

  getContextsByCategory: async (category: string): Promise<OrganizationalContext[]> => {
    const response = await api.get(`/api/v1/contexts/?category=${category}`);
    return response.data;
  },

  getContextCategories: async (): Promise<string[]> => {
    const response = await api.get('/api/v1/contexts/categories');
    return response.data;
  },

  getAllContexts: async (): Promise<OrganizationalContext[]> => {
    const response = await api.get('/api/v1/contexts/?active_only=false');
    return response.data;
  },

  getContext: async (id: number): Promise<OrganizationalContext> => {
    const response = await api.get(`/api/v1/contexts/${id}`);
    return response.data;
  },

  createContext: async (contextData: CreateContextRequest): Promise<OrganizationalContext> => {
    const response = await api.post('/api/v1/contexts/', contextData);
    return response.data;
  },

  updateContext: async (id: number, contextData: UpdateContextRequest): Promise<OrganizationalContext> => {
    const response = await api.put(`/api/v1/contexts/${id}`, contextData);
    return response.data;
  },

  deleteContext: async (id: number): Promise<void> => {
    await api.delete(`/api/v1/contexts/${id}`);
  },

  // Create category with UI settings
  createCategory: async (categoryData: CategoryData): Promise<OrganizationalContext> => {
    // Create a placeholder context to establish the category with UI settings
    const placeholderContent = {
      summary: categoryData.description,
      ui_settings: {
        color: categoryData.color,
        icon: categoryData.icon,
        display_name: categoryData.displayName
      }
    };
    
    const response = await api.post('/api/v1/contexts/', {
      category: categoryData.name,
      name: `${categoryData.displayName} Guidelines`,
      description: `Default context for ${categoryData.displayName} category`,
      content: placeholderContent,
      priority: 10 // High priority so it appears first
    });
    
    return response.data;
  }
};