import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    host: '0.0.0.0',  // Allow external connections in Docker
    port: 3000,
    proxy: {
      // Proxy API calls to backend during development
      '/api': {
        target: 'http://backend:8000',
        changeOrigin: true,
        secure: false,
      },
    },
  },
  preview: {
    host: '0.0.0.0',
    port: 3000,
  },
})