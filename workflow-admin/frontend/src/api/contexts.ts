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
  tags: string[];
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
};