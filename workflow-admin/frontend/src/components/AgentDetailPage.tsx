import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  Box,
  Typography,
  Paper,
  Grid,
  Card,
  CardContent,
  Button,
  Chip,
  Alert,
  CircularProgress,
  List,
  ListItem,
  ListItemText,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  IconButton,
  Tooltip,
} from '@mui/material';
import {
  ArrowBack as BackIcon,
  Person as AgentIcon,
  Business as TypeIcon,
  Assessment as MetricsIcon,
  Schedule as StatusIcon,
  Settings as ConfigIcon,
  Description as DescriptionIcon,
  Psychology as ModelIcon,
  Edit as EditIcon,
  AccountTree as WorkflowIcon,
  PlayArrow as ActiveIcon,
  Visibility as PassiveIcon,
  Psychology as CognitiveIcon,
  Group as CollaborativeIcon,
} from '@mui/icons-material';
import { Agent, agentsApi } from '../api/agents';
import { modelsApi, AIModel } from '../api/models';
import { AgentWorkflow, workflowsApi } from '../api/workflows';
import { EditButton } from './common';

const AgentDetailPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [agent, setAgent] = useState<Agent | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [models, setModels] = useState<AIModel[]>([]);
  const [modelAssignDialogOpen, setModelAssignDialogOpen] = useState(false);
  const [selectedModelId, setSelectedModelId] = useState<number | ''>('');
  const [compatibleWorkflows, setCompatibleWorkflows] = useState<AgentWorkflow[]>([]);
  const [workflowAssignDialogOpen, setWorkflowAssignDialogOpen] = useState(false);
  const [selectedWorkflowId, setSelectedWorkflowId] = useState<number | ''>('');

  useEffect(() => {
    const loadAgent = async () => {
      if (!id) return;
      
      try {
        setLoading(true);
        setError(null);
        
        const agentData = await agentsApi.getAgent(parseInt(id));
        setAgent(agentData);
        
        // Load workflows after agent is loaded
        await loadWorkflowsForAgent(agentData);
      } catch (error) {
        console.error('Error loading agent:', error);
        setError('Failed to load agent details');
      } finally {
        setLoading(false);
      }
    };

    loadAgent();
    loadModels();
  }, [id]);

  const loadModels = async () => {
    try {
      const modelsData = await modelsApi.getModels();
      setModels(modelsData);
    } catch (error) {
      console.error('Error loading models:', error);
    }
  };


  const loadWorkflowsForAgent = async (agentData: any) => {
    if (!agentData?.agent_type) return;
    
    try {
      // Load all available workflows
      const allWorkflows = await workflowsApi.getAgentWorkflows();
      
      // Filter workflows that match this agent's type
      const compatibleWorkflows = allWorkflows.filter(w => 
        w.definition.agent_type_category === agentData.agent_type.name
      );
      setCompatibleWorkflows(compatibleWorkflows);
      
      // Note: No "assigned" workflow concept anymore - agent can use any compatible workflow
    } catch (error) {
      console.error('Error loading workflows:', error);
    }
  };

  // This useEffect is no longer needed since we load assigned workflows directly in loadWorkflows

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active': return 'success';
      case 'inactive': return 'default';
      case 'maintenance': return 'warning';
      case 'error': return 'error';
      default: return 'default';
    }
  };

  const getWorkloadColor = (workload: number, capacity: number) => {
    const percentage = (workload / capacity) * 100;
    if (percentage >= 90) return 'error';
    if (percentage >= 70) return 'warning';
    return 'success';
  };

  const handleOpenModelAssignDialog = () => {
    setSelectedModelId(agent?.assigned_model_id || '');
    setModelAssignDialogOpen(true);
  };

  const handleAssignModel = async () => {
    if (!agent || !id) return;

    try {
      setLoading(true);
      await agentsApi.updateAgent(parseInt(id), {
        assigned_model_id: selectedModelId || undefined
      });
      
      // Reload agent to show updated model assignment
      const updatedAgent = await agentsApi.getAgent(parseInt(id));
      setAgent(updatedAgent);
      
      setModelAssignDialogOpen(false);
    } catch (error) {
      console.error('Error assigning model:', error);
      setError('Failed to assign model to agent');
    } finally {
      setLoading(false);
    }
  };

  const getAssignedModelName = () => {
    if (!agent?.assigned_model_id) return null;
    const model = models.find(m => m.id === agent.assigned_model_id);
    return model?.name || `Model ${agent.assigned_model_id}`;
  };

  const handleAssignWorkflow = async () => {
    if (!agent || !id) return;

    try {
      setLoading(true);
      await agentsApi.updateAgent(parseInt(id), {
        assigned_workflow_id: selectedWorkflowId || undefined
      });
      
      // Reload agent to show updated workflow assignment
      const updatedAgent = await agentsApi.getAgent(parseInt(id));
      setAgent(updatedAgent);
      
      setWorkflowAssignDialogOpen(false);
    } catch (error) {
      console.error('Error assigning workflow:', error);
      setError('Failed to assign workflow to agent');
    } finally {
      setLoading(false);
    }
  };

  const getAssignedWorkflowName = () => {
    if (!agent?.assigned_workflow_id) return null;
    const workflow = compatibleWorkflows.find(w => w.id === agent.assigned_workflow_id);
    return workflow?.name || `Workflow ${agent.assigned_workflow_id}`;
  };


  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
        <CircularProgress />
      </Box>
    );
  }

  if (error || !agent) {
    return (
      <Box>
        <Button
          startIcon={<BackIcon />}
          onClick={() => navigate(-1)}
          sx={{ mb: 2 }}
        >
          Back
        </Button>
        <Alert severity="error">
          {error || 'Agent not found'}
        </Alert>
      </Box>
    );
  }

  return (
    <Box>
      {/* Header with back button */}
      <Box display="flex" alignItems="center" gap={2} mb={3}>
        <Button
          startIcon={<BackIcon />}
          onClick={() => navigate(-1)}
        >
          Back
        </Button>
        <Box>
          <Typography variant="h4" component="h1" fontWeight="bold">
            {agent.name}
          </Typography>
          <Typography variant="subtitle1" color="text.secondary">
            {agent.agent_type?.name || 'Unknown Type'}
          </Typography>
        </Box>
      </Box>

      <Grid container spacing={3}>
        {/* Basic Information */}
        <Grid item xs={12} md={8}>
          <Paper sx={{ p: 3, mb: 3 }}>
            <Box display="flex" alignItems="center" gap={1} mb={2}>
              <DescriptionIcon color="primary" />
              <Typography variant="h6" color="primary">
                Basic Information
              </Typography>
            </Box>
            
            <Grid container spacing={2}>
              <Grid item xs={12} sm={6}>
                <Typography variant="body2" color="text.secondary" gutterBottom>
                  Name
                </Typography>
                <Typography variant="body1" fontWeight="medium">
                  {agent.name}
                </Typography>
              </Grid>
              
              <Grid item xs={12} sm={6}>
                <Typography variant="body2" color="text.secondary" gutterBottom>
                  Agent Type
                </Typography>
                <Typography variant="body1" fontWeight="medium">
                  {agent.agent_type?.name || 'Unknown Type'}
                </Typography>
              </Grid>
              
              <Grid item xs={12}>
                <Typography variant="body2" color="text.secondary" gutterBottom>
                  Description
                </Typography>
                <Typography variant="body1">
                  {agent.description || 'No description provided'}
                </Typography>
              </Grid>
            </Grid>
          </Paper>

          {/* Specializations */}
          {agent.specializations && (
            <Paper sx={{ p: 3, mb: 3 }}>
              <Box display="flex" alignItems="center" gap={1} mb={2}>
                <ConfigIcon color="primary" />
                <Typography variant="h6" color="primary">
                  Specializations
                </Typography>
              </Box>
              
              {agent.specializations.skills && (
                <Box mb={2}>
                  <Typography variant="subtitle2" gutterBottom>
                    Skills
                  </Typography>
                  <Box display="flex" flexWrap="wrap" gap={1}>
                    {agent.specializations.skills.map((skill: string, index: number) => (
                      <Chip key={index} label={skill} size="small" variant="outlined" />
                    ))}
                  </Box>
                </Box>
              )}
              
              {agent.specializations.tools && (
                <Box mb={2}>
                  <Typography variant="subtitle2" gutterBottom>
                    Tools
                  </Typography>
                  <Box display="flex" flexWrap="wrap" gap={1}>
                    {agent.specializations.tools.map((tool: string, index: number) => (
                      <Chip key={index} label={tool} size="small" />
                    ))}
                  </Box>
                </Box>
              )}
            </Paper>
          )}
        </Grid>

        {/* Status and Metrics Sidebar */}
        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 3, mb: 3 }}>
            <Box display="flex" alignItems="center" gap={1} mb={2}>
              <StatusIcon color="primary" />
              <Typography variant="h6" color="primary">
                Status & Metrics
              </Typography>
            </Box>
            
            <Box mb={2}>
              <Typography variant="body2" color="text.secondary" gutterBottom>
                Status
              </Typography>
              <Chip
                label={agent.status}
                color={getStatusColor(agent.status) as any}
                size="small"
              />
            </Box>
            
            <Box mb={2}>
              <Typography variant="body2" color="text.secondary" gutterBottom>
                Workload
              </Typography>
              <Box display="flex" alignItems="center" gap={1}>
                <Typography variant="body2">
                  {agent.current_workload} / {agent.workload_capacity}
                </Typography>
                <Chip
                  label={`${Math.round((agent.current_workload / agent.workload_capacity) * 100)}%`}
                  color={getWorkloadColor(agent.current_workload, agent.workload_capacity) as any}
                  size="small"
                />
              </Box>
            </Box>
            
            {agent.last_active && (
              <Box>
                <Typography variant="body2" color="text.secondary" gutterBottom>
                  Last Active
                </Typography>
                <Typography variant="body2">
                  {new Date(agent.last_active).toLocaleString()}
                </Typography>
              </Box>
            )}
          </Paper>

          {/* AI Model & Workflow Assignment */}
          <Paper sx={{ p: 3, mb: 3 }}>
            <Box display="flex" alignItems="center" justifyContent="space-between" mb={2}>
              <Box display="flex" alignItems="center" gap={1}>
                <ModelIcon color="primary" />
                <Typography variant="h6" color="primary">
                  AI Model & Workflow
                </Typography>
              </Box>
              <Box display="flex" gap={1}>
                <EditButton
                  onClick={handleOpenModelAssignDialog}
                  tooltip="Assign AI Model"
                  color="primary"
                />
                <EditButton
                  onClick={() => {
                    setSelectedWorkflowId(agent?.assigned_workflow_id || '');
                    setWorkflowAssignDialogOpen(true);
                  }}
                  tooltip="Assign Workflow"
                  color="secondary"
                />
              </Box>
            </Box>
            
            <Box>
              <Typography variant="body2" color="text.secondary" gutterBottom>
                Assigned Model
              </Typography>
              {getAssignedModelName() ? (
                <Chip
                  label={getAssignedModelName()}
                  color="primary"
                  variant="outlined"
                  icon={<ModelIcon />}
                />
              ) : (
                <Typography variant="body2" color="text.secondary">
                  No model assigned
                </Typography>
              )}
            </Box>

            <Box>
              <Typography variant="body2" color="text.secondary" gutterBottom>
                Assigned Workflow
              </Typography>
              {getAssignedWorkflowName() ? (
                <Chip
                  label={getAssignedWorkflowName()}
                  color="secondary"
                  variant="outlined"
                  icon={<WorkflowIcon />}
                />
              ) : (
                <Typography variant="body2" color="text.secondary">
                  No workflow assigned
                </Typography>
              )}
            </Box>
          </Paper>


          {/* Configuration */}
          {agent.configuration && Object.keys(agent.configuration).length > 0 && (
            <Paper sx={{ p: 3 }}>
              <Box display="flex" alignItems="center" gap={1} mb={2}>
                <ConfigIcon color="primary" />
                <Typography variant="h6" color="primary">
                  Configuration
                </Typography>
              </Box>
              
              <List dense>
                {Object.entries(agent.configuration).map(([key, value]) => (
                  <ListItem key={key} divider>
                    <ListItemText
                      primary={key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}
                      secondary={typeof value === 'object' ? JSON.stringify(value) : String(value)}
                    />
                  </ListItem>
                ))}
              </List>
            </Paper>
          )}
        </Grid>
      </Grid>

      {/* Model Assignment Dialog */}
      <Dialog
        open={modelAssignDialogOpen}
        onClose={() => setModelAssignDialogOpen(false)}
        maxWidth="sm"
        fullWidth
      >
        <DialogTitle>Assign AI Model</DialogTitle>
        <DialogContent>
          <Typography variant="body2" color="text.secondary" gutterBottom>
            Select an AI model to assign to {agent?.name}. The assigned model will be used for this agent's operations.
          </Typography>
          
          <FormControl fullWidth margin="normal">
            <InputLabel>AI Model</InputLabel>
            <Select
              value={selectedModelId}
              onChange={(e) => setSelectedModelId(e.target.value as number | '')}
              label="AI Model"
            >
              <MenuItem value="">
                <em>No model (unassign)</em>
              </MenuItem>
              {models
                .filter(model => model.is_active)
                .map((model) => (
                  <MenuItem key={model.id} value={model.id}>
                    <Box display="flex" alignItems="center" gap={1}>
                      <ModelIcon fontSize="small" />
                      <Box>
                        <Typography variant="body2">{model.name}</Typography>
                        <Typography variant="caption" color="text.secondary">
                          {model.provider} • {model.context_window.toLocaleString()} tokens
                        </Typography>
                      </Box>
                    </Box>
                  </MenuItem>
                ))}
            </Select>
          </FormControl>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setModelAssignDialogOpen(false)}>
            Cancel
          </Button>
          <Button 
            onClick={handleAssignModel} 
            variant="contained"
            disabled={loading}
          >
            Assign Model
          </Button>
        </DialogActions>
      </Dialog>

      {/* Workflow Assignment Dialog */}
      <Dialog
        open={workflowAssignDialogOpen}
        onClose={() => setWorkflowAssignDialogOpen(false)}
        maxWidth="sm"
        fullWidth
      >
        <DialogTitle>Assign Workflow</DialogTitle>
        <DialogContent>
          <Typography variant="body2" color="text.secondary" gutterBottom>
            Select a workflow to assign to {agent?.name}. Only workflows compatible with this agent's type ({agent?.agent_type?.name}) are shown.
          </Typography>
          
          <FormControl fullWidth margin="normal">
            <InputLabel>Workflow</InputLabel>
            <Select
              value={selectedWorkflowId}
              onChange={(e) => setSelectedWorkflowId(e.target.value as number | '')}
              label="Workflow"
            >
              <MenuItem value="">
                <em>No workflow (unassign)</em>
              </MenuItem>
              {compatibleWorkflows.map((workflow) => (
                <MenuItem key={workflow.id} value={workflow.id}>
                  <Box display="flex" alignItems="center" gap={1}>
                    <WorkflowIcon fontSize="small" />
                    <Box>
                      <Typography variant="body2">{workflow.name}</Typography>
                      <Typography variant="caption" color="text.secondary">
                        v{workflow.version} • {workflow.definition.states?.length || 0} states
                      </Typography>
                    </Box>
                  </Box>
                </MenuItem>
              ))}
            </Select>
          </FormControl>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setWorkflowAssignDialogOpen(false)}>
            Cancel
          </Button>
          <Button 
            onClick={handleAssignWorkflow} 
            variant="contained"
            disabled={loading}
          >
            Assign Workflow
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default AgentDetailPage;