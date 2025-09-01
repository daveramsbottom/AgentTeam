import React, { useState, useEffect } from 'react'
import {
  Card,
  CardContent,
  Typography,
  Chip,
  Box,
  CircularProgress,
  Alert,
} from '@mui/material'
import { 
  CheckCircle as CheckCircleIcon,
  Error as ErrorIcon,
  Info as InfoIcon,
} from '@mui/icons-material'
import { healthApi, HealthStatus, ApiInfo } from '../api/client'

const HealthCheck: React.FC = () => {
  const [health, setHealth] = useState<HealthStatus | null>(null)
  const [apiInfo, setApiInfo] = useState<ApiInfo | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true)
        setError(null)
        
        // Fetch health status and API info in parallel
        const [healthData, infoData] = await Promise.all([
          healthApi.getHealth(),
          healthApi.getInfo(),
        ])
        
        setHealth(healthData)
        setApiInfo(infoData)
      } catch (err: any) {
        setError(err.message || 'Failed to connect to backend API')
        console.error('API connection error:', err)
      } finally {
        setLoading(false)
      }
    }

    fetchData()
  }, [])

  if (loading) {
    return (
      <Card>
        <CardContent>
          <Box display="flex" alignItems="center" gap={2}>
            <CircularProgress size={24} />
            <Typography variant="h6">Connecting to Backend...</Typography>
          </Box>
        </CardContent>
      </Card>
    )
  }

  if (error) {
    return (
      <Alert severity="error" icon={<ErrorIcon />}>
        <Typography variant="h6">Backend Connection Failed</Typography>
        <Typography variant="body2">{error}</Typography>
      </Alert>
    )
  }

  const isHealthy = health?.status === 'healthy'
  const isDatabaseConnected = health?.database?.local_connection_ok === true

  return (
    <Box display="flex" gap={2} flexDirection="column">
      {/* Backend Health Status */}
      <Card>
        <CardContent>
          <Box display="flex" alignItems="center" justifyContent="space-between" mb={2}>
            <Typography variant="h6" display="flex" alignItems="center" gap={1}>
              <CheckCircleIcon color={isHealthy ? 'success' : 'error'} />
              Backend API Status
            </Typography>
            <Chip
              label={health?.status || 'Unknown'}
              color={isHealthy ? 'success' : 'error'}
              variant="filled"
            />
          </Box>
          
          <Box display="flex" gap={2} mb={2}>
            <Typography variant="body2" color="textSecondary">
              <strong>Service:</strong> {health?.service || 'N/A'}
            </Typography>
            <Typography variant="body2" color="textSecondary">
              <strong>Version:</strong> {health?.version || 'N/A'}
            </Typography>
          </Box>

          <Box display="flex" alignItems="center" gap={1}>
            <Typography variant="body2">Database:</Typography>
            <Chip
              size="small"
              label={isDatabaseConnected ? 'Connected' : 'Disconnected'}
              color={isDatabaseConnected ? 'success' : 'error'}
              variant="outlined"
            />
          </Box>
        </CardContent>
      </Card>

      {/* API Information */}
      {apiInfo && (
        <Card>
          <CardContent>
            <Box display="flex" alignItems="center" gap={1} mb={2}>
              <InfoIcon color="primary" />
              <Typography variant="h6">{apiInfo.name}</Typography>
            </Box>
            
            <Typography variant="body2" color="textSecondary" paragraph>
              {apiInfo.description}
            </Typography>

            <Typography variant="subtitle2" gutterBottom>
              Available Features:
            </Typography>
            <Box display="flex" flexWrap="wrap" gap={1} mb={2}>
              {apiInfo.features.map((feature) => (
                <Chip
                  key={feature}
                  label={feature}
                  size="small"
                  variant="outlined"
                  color="primary"
                />
              ))}
            </Box>

            <Typography variant="body2" color="textSecondary">
              <strong>Endpoints:</strong> {Object.keys(apiInfo.endpoints).length} available
            </Typography>
          </CardContent>
        </Card>
      )}
    </Box>
  )
}

export default HealthCheck