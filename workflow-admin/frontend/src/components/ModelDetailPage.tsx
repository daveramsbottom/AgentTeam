import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  Box,
  Typography,
  Paper,
  Grid,
  Alert,
  CircularProgress,
  Button,
  Chip,
  Card,
  CardContent,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  IconButton,
  Tooltip,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  FormControlLabel,
  Switch,
  MenuItem,
} from '@mui/material';
import {
  Psychology as ModelIcon,
  ArrowBack as ArrowBackIcon,
} from '@mui/icons-material';
import { modelsApi, AIModel } from '../api/models';
import { EditButton, DeleteButton, SaveCancelButtons, ConfirmDialog } from './common';

const ModelDetailPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [model, setModel] = useState<AIModel | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isEditing, setIsEditing] = useState(false);
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);
  const [editedModel, setEditedModel] = useState<Partial<AIModel>>({});

  useEffect(() => {
    if (id) {
      loadModel();
    }
  }, [id]);

  const loadModel = async () => {
    if (!id || isNaN(Number(id))) {
      setError('Invalid model ID');
      setLoading(false);
      return;
    }

    try {
      setLoading(true);
      setError(null);
      const modelData = await modelsApi.getModel(Number(id));
      setModel(modelData);
      setEditedModel(modelData);
    } catch (err) {
      console.error('Error loading model:', err);
      setError('Failed to load model details.');
    } finally {
      setLoading(false);
    }
  };

  const handleEdit = () => {
    setIsEditing(true);
  };

  const handleCancelEdit = () => {
    setIsEditing(false);
    setEditedModel(model || {});
  };

  const handleSave = async () => {
    if (!model || !id) return;

    try {
      setLoading(true);
      const updatedModel = await modelsApi.updateModel(Number(id), {
        name: editedModel.name,
        description: editedModel.description,
        is_active: editedModel.is_active,
        // Add other updatable fields as needed
      });
      setModel(updatedModel);
      setIsEditing(false);
    } catch (err) {
      console.error('Error updating model:', err);
      setError('Failed to update model.');
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async () => {
    if (!id) return;

    try {
      await modelsApi.deleteModel(Number(id));
      navigate('/models');
    } catch (err) {
      console.error('Error deleting model:', err);
      setError('Failed to delete model.');
    }
    setDeleteDialogOpen(false);
  };

  const getProviderColor = (provider: string) => {
    const colors: Record<string, string> = {
      'openai': '#10A37F',
      'anthropic': '#D97757',
      'google': '#4285F4',
      'azure': '#0078D4',
      'local': '#6C757D'
    };
    return colors[provider] || '#757575';
  };

  const formatContextWindow = (tokens: number) => {
    if (tokens >= 1000000) {
      return `${(tokens / 1000000).toFixed(1)}M tokens`;
    } else if (tokens >= 1000) {
      return `${(tokens / 1000).toFixed(0)}K tokens`;
    }
    return `${tokens} tokens`;
  };

  const getCapabilityIcon = (capability: string, enabled: boolean) => {
    if (!enabled) return '❌';
    switch (capability) {
      case 'text_generation': return '📝';
      case 'code_generation': return '💻';
      case 'analysis': return '🔍';
      case 'reasoning': return '🧠';
      case 'conversation': return '💬';
      case 'function_calling': return '⚙️';
      default: return '✅';
    }
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
        <CircularProgress />
        <Typography variant="body2" sx={{ ml: 2 }}>
          Loading model details...
        </Typography>
      </Box>
    );
  }

  if (error || !model) {
    return (
      <Box>
        <Button
          startIcon={<ArrowBackIcon />}
          onClick={() => navigate('/models')}
          sx={{ mb: 2 }}
        >
          Back to Models
        </Button>
        <Alert severity="error">
          {error || 'Model not found'}
        </Alert>
      </Box>
    );
  }

  return (
    <Box>
      {/* Header */}
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Box display="flex" alignItems="center" gap={2}>
          <Button
            startIcon={<ArrowBackIcon />}
            onClick={() => navigate('/models')}
          >
            Back to Models
          </Button>
          <Box>
            <Typography variant="h4" gutterBottom>
              {isEditing ? (
                <TextField
                  value={editedModel.name || ''}
                  onChange={(e) => setEditedModel({...editedModel, name: e.target.value})}
                  variant="outlined"
                  size="small"
                  sx={{ fontSize: '2rem' }}
                />
              ) : (
                model.name
              )}
            </Typography>
            <Box display="flex" alignItems="center" gap={1}>
              <Chip 
                label={model.provider}
                sx={{ 
                  backgroundColor: getProviderColor(model.provider) + '20',
                  color: getProviderColor(model.provider),
                  fontWeight: 'medium',
                  textTransform: 'capitalize'
                }}
              />
              {isEditing ? (
                <FormControlLabel
                  control={
                    <Switch
                      checked={editedModel.is_active ?? model.is_active}
                      onChange={(e) => setEditedModel({...editedModel, is_active: e.target.checked})}
                    />
                  }
                  label="Active"
                />
              ) : (
                <Chip 
                  label={model.is_active ? 'Active' : 'Inactive'}
                  color={model.is_active ? 'success' : 'default'}
                  size="small"
                />
              )}
            </Box>
          </Box>
        </Box>
        <Box display="flex" gap={1}>
          {isEditing ? (
            <SaveCancelButtons
              onSave={handleSave}
              onCancel={handleCancelEdit}
              loading={loading}
            />
          ) : (
            <>
              <EditButton
                onClick={handleEdit}
                tooltip="Edit Model"
                color="primary"
                placement="header"
              />
              <DeleteButton
                onClick={() => setDeleteDialogOpen(true)}
                tooltip="Delete Model"
                size="medium"
              />
            </>
          )}
        </Box>
      </Box>

      <Grid container spacing={3}>
        {/* Basic Information */}
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3, height: 'fit-content' }}>
            <Typography variant="h6" gutterBottom color="primary">
              Basic Information
            </Typography>
            
            <Table size="small">
              <TableBody>
                <TableRow>
                  <TableCell><strong>Model ID</strong></TableCell>
                  <TableCell>{model.model_id}</TableCell>
                </TableRow>
                <TableRow>
                  <TableCell><strong>Provider</strong></TableCell>
                  <TableCell sx={{ textTransform: 'capitalize' }}>{model.provider}</TableCell>
                </TableRow>
                <TableRow>
                  <TableCell><strong>Description</strong></TableCell>
                  <TableCell>
                    {isEditing ? (
                      <TextField
                        value={editedModel.description || ''}
                        onChange={(e) => setEditedModel({...editedModel, description: e.target.value})}
                        multiline
                        rows={2}
                        fullWidth
                        variant="outlined"
                        size="small"
                      />
                    ) : (
                      model.description || 'No description provided'
                    )}
                  </TableCell>
                </TableRow>
                <TableRow>
                  <TableCell><strong>Context Window</strong></TableCell>
                  <TableCell>{formatContextWindow(model.context_window)}</TableCell>
                </TableRow>
                <TableRow>
                  <TableCell><strong>Created</strong></TableCell>
                  <TableCell>{new Date(model.created_at).toLocaleDateString()}</TableCell>
                </TableRow>
                {model.updated_at && (
                  <TableRow>
                    <TableCell><strong>Last Updated</strong></TableCell>
                    <TableCell>{new Date(model.updated_at).toLocaleDateString()}</TableCell>
                  </TableRow>
                )}
              </TableBody>
            </Table>
          </Paper>
        </Grid>

        {/* Capabilities */}
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3, height: 'fit-content' }}>
            <Typography variant="h6" gutterBottom color="primary">
              Capabilities
            </Typography>
            
            <Grid container spacing={2}>
              {Object.entries(model.capabilities).map(([capability, enabled]) => (
                <Grid item xs={6} key={capability}>
                  <Box display="flex" alignItems="center" gap={1}>
                    <Typography variant="body2">
                      {getCapabilityIcon(capability, enabled)}
                    </Typography>
                    <Typography 
                      variant="body2" 
                      color={enabled ? 'text.primary' : 'text.secondary'}
                    >
                      {capability.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())}
                    </Typography>
                  </Box>
                </Grid>
              ))}
            </Grid>
          </Paper>
        </Grid>

        {/* Performance Metrics */}
        {model.performance_metrics && (
          <Grid item xs={12} md={6}>
            <Paper sx={{ p: 3 }}>
              <Typography variant="h6" gutterBottom color="primary">
                Performance Metrics
              </Typography>
              
              <Grid container spacing={2}>
                <Grid item xs={4}>
                  <Box textAlign="center">
                    <Typography variant="h4">
                      {model.performance_metrics.quality === 'outstanding' ? '⭐⭐⭐' :
                       model.performance_metrics.quality === 'excellent' ? '⭐⭐' : '⭐'}
                    </Typography>
                    <Typography variant="body2" color="textSecondary">
                      Quality
                    </Typography>
                    <Typography variant="caption" sx={{ textTransform: 'capitalize' }}>
                      {model.performance_metrics.quality}
                    </Typography>
                  </Box>
                </Grid>
                <Grid item xs={4}>
                  <Box textAlign="center">
                    <Typography variant="h4">
                      {model.performance_metrics.speed === 'fast' ? '🚀' :
                       model.performance_metrics.speed === 'medium' ? '⚡' : '🐌'}
                    </Typography>
                    <Typography variant="body2" color="textSecondary">
                      Speed
                    </Typography>
                    <Typography variant="caption" sx={{ textTransform: 'capitalize' }}>
                      {model.performance_metrics.speed}
                    </Typography>
                  </Box>
                </Grid>
                <Grid item xs={4}>
                  <Box textAlign="center">
                    <Typography variant="h4">🛡️</Typography>
                    <Typography variant="body2" color="textSecondary">
                      Reliability
                    </Typography>
                    <Typography variant="caption" sx={{ textTransform: 'capitalize' }}>
                      {model.performance_metrics.reliability}
                    </Typography>
                  </Box>
                </Grid>
              </Grid>
            </Paper>
          </Grid>
        )}

        {/* Cost Information */}
        {model.cost_per_1k_tokens && (
          <Grid item xs={12} md={6}>
            <Paper sx={{ p: 3 }}>
              <Typography variant="h6" gutterBottom color="primary">
                Cost Information
              </Typography>
              
              <Grid container spacing={2}>
                <Grid item xs={6}>
                  <Box textAlign="center">
                    <Typography variant="h4" color="info.main">
                      ${model.cost_per_1k_tokens.input.toFixed(4)}
                    </Typography>
                    <Typography variant="body2" color="textSecondary">
                      Input / 1K tokens
                    </Typography>
                  </Box>
                </Grid>
                <Grid item xs={6}>
                  <Box textAlign="center">
                    <Typography variant="h4" color="warning.main">
                      ${model.cost_per_1k_tokens.output.toFixed(4)}
                    </Typography>
                    <Typography variant="body2" color="textSecondary">
                      Output / 1K tokens
                    </Typography>
                  </Box>
                </Grid>
              </Grid>
            </Paper>
          </Grid>
        )}

        {/* Best For */}
        <Grid item xs={12}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom color="primary">
              Best For
            </Typography>
            
            <Box display="flex" flexWrap="wrap" gap={1}>
              {model.best_for.map((tag) => (
                <Chip
                  key={tag}
                  label={tag.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())}
                  sx={{ 
                    backgroundColor: getProviderColor(model.provider) + '20',
                    color: getProviderColor(model.provider),
                    fontWeight: 'medium'
                  }}
                />
              ))}
            </Box>
          </Paper>
        </Grid>
      </Grid>

      {/* Delete Confirmation Dialog */}
      <ConfirmDialog
        open={deleteDialogOpen}
        onClose={() => setDeleteDialogOpen(false)}
        onConfirm={handleDelete}
        title="Delete AI Model"
        content={`Are you sure you want to delete the model "${model.name}"? This action cannot be undone and may affect agents currently using this model.`}
        confirmText="Delete"
        confirmColor="error"
      />
    </Box>
  );
};

export default ModelDetailPage;