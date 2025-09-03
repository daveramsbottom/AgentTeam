import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Paper,
  Grid,
  Card,
  CardContent,
  Chip,
  Alert,
  CircularProgress,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Button,
} from '@mui/material';
import {
  Psychology as AIModelIcon,
  CheckCircle as ActiveIcon,
  Cancel as InactiveIcon,
  Speed as SpeedIcon,
  Star as QualityIcon,
  Security as ReliabilityIcon,
} from '@mui/icons-material';
import { AIModel, modelsApi } from '../api/models';

const ModelManagement: React.FC = () => {
  const [models, setModels] = useState<AIModel[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadModels();
  }, []);

  const loadModels = async () => {
    try {
      setLoading(true);
      setError(null);
      const modelsData = await modelsApi.getModels();
      setModels(modelsData);
    } catch (err) {
      console.error('Error loading models:', err);
      setError('Failed to load AI models.');
    } finally {
      setLoading(false);
    }
  };

  const getProviderColor = (provider: AIModel['provider']) => {
    switch (provider) {
      case 'openai': return 'primary';
      case 'anthropic': return 'secondary';
      case 'google': return 'success';
      case 'azure': return 'info';
      case 'local': return 'warning';
      default: return 'default';
    }
  };

  const getPerformanceIcon = (metric: string, value: string) => {
    switch (metric) {
      case 'speed':
        return <SpeedIcon fontSize="small" />;
      case 'quality':
        return <QualityIcon fontSize="small" />;
      case 'reliability':
        return <ReliabilityIcon fontSize="small" />;
      default:
        return null;
    }
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="200px">
        <CircularProgress />
        <Typography variant="body2" sx={{ ml: 2 }}>
          Loading AI models...
        </Typography>
      </Box>
    );
  }

  if (error) {
    return (
      <Alert severity="error" sx={{ mb: 2 }}>
        {error}
      </Alert>
    );
  }

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        AI Model Management
      </Typography>
      <Typography variant="body1" color="textSecondary" paragraph>
        Manage available AI models and their configurations for agent types.
      </Typography>

      {/* Summary Cards */}
      <Grid container spacing={2} sx={{ mb: 4 }}>
        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center" gap={1}>
                <AIModelIcon color="primary" />
                <Box>
                  <Typography variant="h6">{models.length}</Typography>
                  <Typography variant="caption" color="textSecondary">
                    Total Models
                  </Typography>
                </Box>
              </Box>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center" gap={1}>
                <ActiveIcon color="success" />
                <Box>
                  <Typography variant="h6">{models.filter(m => m.is_active).length}</Typography>
                  <Typography variant="caption" color="textSecondary">
                    Active Models
                  </Typography>
                </Box>
              </Box>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center" gap={1}>
                <Typography variant="h6">{new Set(models.map(m => m.provider)).size}</Typography>
                <Typography variant="caption" color="textSecondary">
                  Providers
                </Typography>
              </Box>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center" gap={1}>
                <Typography variant="h6">
                  {models.filter(m => m.capabilities.code_generation).length}
                </Typography>
                <Typography variant="caption" color="textSecondary">
                  Code Capable
                </Typography>
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Models Table */}
      <Paper elevation={1}>
        <TableContainer>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>Model</TableCell>
                <TableCell>Provider</TableCell>
                <TableCell>Capabilities</TableCell>
                <TableCell>Performance</TableCell>
                <TableCell>Context</TableCell>
                <TableCell>Cost</TableCell>
                <TableCell>Status</TableCell>
                <TableCell>Actions</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {models.map((model) => (
                <TableRow key={model.id} hover>
                  <TableCell>
                    <Box>
                      <Typography variant="subtitle2" fontWeight="medium">
                        {model.name}
                      </Typography>
                      <Typography variant="caption" color="textSecondary">
                        {model.model_id}
                      </Typography>
                      {model.description && (
                        <Typography variant="body2" color="textSecondary" sx={{ mt: 0.5 }}>
                          {model.description}
                        </Typography>
                      )}
                    </Box>
                  </TableCell>
                  <TableCell>
                    <Chip 
                      label={model.provider} 
                      size="small" 
                      color={getProviderColor(model.provider) as any}
                      variant="outlined"
                    />
                  </TableCell>
                  <TableCell>
                    <Box display="flex" flexDirection="column" gap={0.5}>
                      {Object.entries(model.capabilities)
                        .filter(([_, enabled]) => enabled)
                        .map(([capability, _]) => (
                          <Chip
                            key={capability}
                            label={capability.replace(/_/g, ' ')}
                            size="small"
                            variant="outlined"
                            sx={{ fontSize: '0.7rem', height: '20px' }}
                          />
                        ))
                      }
                    </Box>
                  </TableCell>
                  <TableCell>
                    {model.performance_metrics && (
                      <Box display="flex" flexDirection="column" gap={0.5}>
                        {Object.entries(model.performance_metrics).map(([metric, value]) => (
                          <Box key={metric} display="flex" alignItems="center" gap={0.5}>
                            {getPerformanceIcon(metric, value)}
                            <Typography variant="caption">
                              {metric}: {value}
                            </Typography>
                          </Box>
                        ))}
                      </Box>
                    )}
                  </TableCell>
                  <TableCell>
                    <Typography variant="body2">
                      {model.context_window.toLocaleString()}
                    </Typography>
                    <Typography variant="caption" color="textSecondary">
                      tokens
                    </Typography>
                  </TableCell>
                  <TableCell>
                    {model.cost_per_1k_tokens ? (
                      <Box>
                        <Typography variant="caption">
                          In: ${model.cost_per_1k_tokens.input}
                        </Typography>
                        <Typography variant="caption" display="block">
                          Out: ${model.cost_per_1k_tokens.output}
                        </Typography>
                      </Box>
                    ) : (
                      <Typography variant="caption" color="textSecondary">
                        N/A
                      </Typography>
                    )}
                  </TableCell>
                  <TableCell>
                    <Chip
                      icon={model.is_active ? <ActiveIcon /> : <InactiveIcon />}
                      label={model.is_active ? 'Active' : 'Inactive'}
                      size="small"
                      color={model.is_active ? 'success' : 'default'}
                      variant="outlined"
                    />
                  </TableCell>
                  <TableCell>
                    <Button 
                      size="small" 
                      variant="outlined"
                      disabled={!model.is_active}
                    >
                      Configure
                    </Button>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      </Paper>

      {/* Best For Section */}
      <Paper elevation={1} sx={{ mt: 3, p: 3 }}>
        <Typography variant="h6" gutterBottom>
          Model Recommendations
        </Typography>
        <Grid container spacing={2}>
          {['coding', 'analysis', 'general_purpose', 'reasoning'].map((category) => {
            const recommendedModels = models.filter(m => 
              m.is_active && m.best_for.includes(category)
            );
            
            return (
              <Grid item xs={12} md={6} key={category}>
                <Card variant="outlined">
                  <CardContent>
                    <Typography variant="subtitle2" gutterBottom color="primary">
                      Best for {category.replace(/_/g, ' ')}
                    </Typography>
                    {recommendedModels.length > 0 ? (
                      <Box display="flex" flexDirection="column" gap={1}>
                        {recommendedModels.slice(0, 3).map((model) => (
                          <Box key={model.id} display="flex" alignItems="center" gap={1}>
                            <Chip 
                              label={model.provider} 
                              size="small" 
                              color={getProviderColor(model.provider) as any}
                              variant="filled"
                              sx={{ minWidth: '60px', fontSize: '0.7rem' }}
                            />
                            <Typography variant="body2">
                              {model.name}
                            </Typography>
                          </Box>
                        ))}
                      </Box>
                    ) : (
                      <Typography variant="body2" color="textSecondary">
                        No models available for this category
                      </Typography>
                    )}
                  </CardContent>
                </Card>
              </Grid>
            );
          })}
        </Grid>
      </Paper>
    </Box>
  );
};

export default ModelManagement;