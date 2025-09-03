import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

export interface HealthCheckResult {
  isApiAvailable: boolean;
  isUsingDatabase: boolean;
  dataSource: 'database' | 'mock' | 'unknown';
  apiResponseTime?: number;
  error?: string;
}

export const checkDataSourceHealth = async (): Promise<HealthCheckResult> => {
  const startTime = Date.now();
  
  try {
    // Try to hit the health check endpoint first
    try {
      const healthResponse = await axios.get(`${API_BASE_URL}/health`, { timeout: 5000 });
      const responseTime = Date.now() - startTime;
      
      if (healthResponse.status === 200) {
        return {
          isApiAvailable: true,
          isUsingDatabase: true,
          dataSource: 'database',
          apiResponseTime: responseTime,
        };
      }
    } catch (healthError) {
      // Health endpoint might not exist, try a regular API call
    }

    // Try to call a real API endpoint
    const testResponse = await axios.get(`${API_BASE_URL}/api/v1/projects/`, { timeout: 5000 });
    const responseTime = Date.now() - startTime;
    
    if (testResponse.status === 200) {
      // Check if we got real data or empty array (which might indicate database issue)
      const hasData = testResponse.data && (testResponse.data.length > 0 || testResponse.data.items?.length > 0);
      
      return {
        isApiAvailable: true,
        isUsingDatabase: hasData,
        dataSource: hasData ? 'database' : 'database', // API is working, assume database even if empty
        apiResponseTime: responseTime,
      };
    }
  } catch (error) {
    // API is not available, so we're using mock data
    return {
      isApiAvailable: false,
      isUsingDatabase: false,
      dataSource: 'mock',
      error: error instanceof Error ? error.message : 'Unknown error',
    };
  }

  return {
    isApiAvailable: false,
    isUsingDatabase: false,
    dataSource: 'unknown',
  };
};

export const checkBackendConnection = async (): Promise<{
  isConnected: boolean;
  responseTime?: number;
  error?: string;
}> => {
  const startTime = Date.now();
  
  try {
    const response = await axios.get(`${API_BASE_URL}/health`, { timeout: 3000 });
    const responseTime = Date.now() - startTime;
    
    return {
      isConnected: true,
      responseTime,
    };
  } catch (error) {
    return {
      isConnected: false,
      error: error instanceof Error ? error.message : 'Connection failed',
    };
  }
};