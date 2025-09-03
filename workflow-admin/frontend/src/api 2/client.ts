import axios from 'axios'

// Create axios instance with base configuration
const api = axios.create({
  baseURL: '/api',  // Proxied through Vite dev server or nginx
  timeout: 5000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// API response types
export interface HealthStatus {
  status: string
  database: {
    local_connection_ok: boolean
  }
  service: string
  version: string
}

export interface ApiInfo {
  name: string
  version: string
  description: string
  features: string[]
  database_connected: boolean
  endpoints: Record<string, string>
}

// API methods
export const healthApi = {
  // Get health status
  getHealth: async (): Promise<HealthStatus> => {
    const response = await api.get('/health')
    return response.data
  },

  // Get API information
  getInfo: async (): Promise<ApiInfo> => {
    const response = await api.get('/v1/info')
    return response.data
  },
}

export default api