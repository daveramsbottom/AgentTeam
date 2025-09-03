// Get version from package.json
export const APP_VERSION = '1.0.0';
export const BUILD_DATE = new Date().toISOString().split('T')[0];

// API to check backend version
export const getBackendVersion = async (): Promise<{ version: string; buildDate?: string }> => {
  const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';
  try {
    const response = await fetch(`${API_BASE_URL}/api/v1/version`);
    return await response.json();
  } catch (error) {
    console.warn('Could not fetch backend version:', error);
    return { version: 'unknown' };
  }
};

export const getVersionInfo = () => ({
  frontend: {
    version: APP_VERSION,
    buildDate: BUILD_DATE,
  }
});