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
  ListItemIcon,
  Divider,
  Accordion,
  AccordionSummary,
  AccordionDetails,
} from '@mui/material';
import {
  ArrowBack as BackIcon,
  SmartToy as AgentIcon,
  Psychology as AIModelIcon,
  CheckCircle as ActiveIcon,
  Cancel as InactiveIcon,
  Build as CapabilityIcon,
  Settings as ConfigIcon,
  AccountTree as WorkflowIcon,
  Tune as TuneIcon,
  Code as CodeIcon,
  Speed as SpeedIcon,
  Star as QualityIcon,
  Security as ReliabilityIcon,
  ExpandMore as ExpandMoreIcon,
  Group as TeamIcon,
  Assignment as TaskIcon,
} from '@mui/icons-material';
import { AgentType, agentsApi } from '../api/agents';
import { AIModel, modelsApi } from '../api/models';
import { WorkflowTemplate, workflowsApi } from '../api/workflows';
import { Team, teamsApi } from '../api/teams';

const AgentTypeDetailPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [agentType, setAgentType] = useState<AgentType | null>(null);
  const [assignedModel, setAssignedModel] = useState<AIModel | null>(null);
  const [workflows, setWorkflows] = useState<WorkflowTemplate[]>([]);
  const [teams, setTeams] = useState<Team[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const loadAgentTypeDetails = async () => {
      if (!id) return;
      
      try {
        setLoading(true);
        setError(null);
        
        // Load agent type
        const agentTypes = await agentsApi.getAgentTypes();
        const foundAgentType = agentTypes.find(at => at.id === parseInt(id));
        
        if (!foundAgentType) {
          setError('Agent type not found');
          return;
        }
        
        setAgentType(foundAgentType);
        
        // Load assigned AI model
        if (foundAgentType.assigned_model_id) {
          try {
            const models = await modelsApi.getModels();
            const model = models.find(m => m.id === foundAgentType.assigned_model_id);
            setAssignedModel(model || null);
          } catch (modelError) {
            console.warn('Could not load assigned model:', modelError);
          }
        }
        
        // Load workflows for this agent type
        try {
          const agentWorkflows = await workflowsApi.getWorkflowsByAgentType(foundAgentType.name);
          setWorkflows(agentWorkflows);
        } catch (workflowError) {
          console.warn('Could not load workflows:', workflowError);
        }
        
        // Load teams that include this agent type (by checking member_agent_ids)
        try {
          const allTeams = await teamsApi.getTeams();
          // This is simplified - in real implementation, you'd have agent instances mapped to agent types
          const relevantTeams = allTeams.filter(team => 
            team.member_agent_ids && team.member_agent_ids.length > 0
          );
          setTeams(relevantTeams);
        } catch (teamError) {
          console.warn('Could not load teams:', teamError);
        }
        
      } catch (error) {
        console.error('Error loading agent type details:', error);
        setError('Failed to load agent type details');
      } finally {
        setLoading(false);
      }
    };

    loadAgentTypeDetails();
  }, [id]);

  const handleBack = () => {
    navigate('/agents');
  };

  const getCapabilitiesArray = () => {
    if (!agentType?.capabilities) return [];
    return Object.entries(agentType.capabilities)
      .filter(([_, enabled]) => enabled)
      .map(([capability, _]) => capability.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase()));
  };

  const getPerformanceIcon = (metric: string) => {
    switch (metric) {
      case 'speed': return <SpeedIcon fontSize="small" />;
      case 'quality': return <QualityIcon fontSize="small" />;  
      case 'reliability': return <ReliabilityIcon fontSize="small" />;
      default: return null;
    }
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="200px">
        <CircularProgress />
        <Typography variant="body2" sx={{ ml: 2 }}>
          Loading agent type details...
        </Typography>
      </Box>
    );
  }

  if (error || !agentType) {
    return (
      <Box>
        <Button
          startIcon={<BackIcon />}
          onClick={handleBack}
          sx={{ mb: 2 }}
        >
          Back to Agent Types
        </Button>
        <Alert severity="error">
          {error || 'Agent type not found'}
        </Alert>
      </Box>
    );
  }

  return (
    <Box>
      {/* Header */}
      <Box display="flex" alignItems="center" gap={2} mb={3}>
        <Button
          startIcon={<BackIcon />}
          onClick={handleBack}
          variant="outlined"
        >
          Back to Agent Types
        </Button>
        <Box flexGrow={1}>
          <Box display="flex" alignItems="center" gap={2}>
            <AgentIcon color="primary" sx={{ fontSize: 32 }} />
            <Box>
              <Typography variant="h4" gutterBottom>
                {agentType.name}
              </Typography>
              <Box display="flex" gap={1}>
                <Chip
                  icon={agentType.is_active ? <ActiveIcon /> : <InactiveIcon />}
                  label={agentType.is_active ? 'Active' : 'Inactive'}
                  size="small"
                  color={agentType.is_active ? 'success' : 'default'}
                  variant="filled"
                />
                {agentType.workflow_preferences?.default_workflow && (
                  <Chip
                    label={`Default Workflow: ${agentType.workflow_preferences.default_workflow}`}
                    size="small"
                    variant="outlined"
                  />
                )}
              </Box>
            </Box>
          </Box>
        </Box>
        <Button
          startIcon={<ConfigIcon />}
          variant="contained"
          color="primary"
        >
          Configure Agent Type
        </Button>
      </Box>

      <Grid container spacing={3}>
        {/* Main Content */}
        <Grid item xs={12} md={8}>
          {/* Description */}
          <Paper elevation={1} sx={{ p: 3, mb: 3 }}>
            <Typography variant="h6" gutterBottom>
              Agent Type Information
            </Typography>
            
            <Typography variant="body2" color="textSecondary" paragraph>
              <strong>Description:</strong> {agentType.description || 'No description provided'}
            </Typography>

            <Box sx={{ mt: 2 }}>
              <Typography variant="body2" color="textSecondary">
                <strong>Created:</strong> {new Date(agentType.created_at).toLocaleDateString()}
              </Typography>
              {agentType.updated_at && (
                <Typography variant="body2" color="textSecondary">
                  <strong>Last Updated:</strong> {new Date(agentType.updated_at).toLocaleDateString()}
                </Typography>
              )}
            </Box>
          </Paper>

          {/* Capabilities */}
          <Paper elevation={1} sx={{ p: 3, mb: 3 }}>
            <Typography variant="h6" gutterBottom>
              <CapabilityIcon sx={{ verticalAlign: 'middle', mr: 1 }} />
              Capabilities ({getCapabilitiesArray().length})
            </Typography>
            
            {getCapabilitiesArray().length > 0 ? (
              <Box display="flex" flexWrap="wrap" gap={1}>
                {getCapabilitiesArray().map((capability, index) => (
                  <Chip
                    key={index}
                    label={capability}
                    variant="outlined"
                    color="primary"
                  />
                ))}
              </Box>
            ) : (
              <Typography variant="body2" color="textSecondary">
                No capabilities defined for this agent type.
              </Typography>
            )}
          </Paper>

          {/* Workflows */}
          <Paper elevation={1} sx={{ p: 3, mb: 3 }}>
            <Typography variant="h6" gutterBottom>
              <WorkflowIcon sx={{ verticalAlign: 'middle', mr: 1 }} />
              Associated Workflows ({workflows.length})
            </Typography>
            
            {workflows.length > 0 ? (
              <List>
                {workflows.map((workflow) => (
                  <ListItem key={workflow.id} divider>
                    <ListItemIcon>
                      <WorkflowIcon color={workflow.is_active ? 'primary' : 'disabled'} />
                    </ListItemIcon>
                    <ListItemText
                      primary={
                        <Box display="flex" alignItems="center" gap={1}>
                          <Typography variant="subtitle2" fontWeight="medium">
                            {workflow.name}
                          </Typography>
                          <Chip label={workflow.version} size="small" variant="outlined" />
                          {workflow.is_default && (
                            <Chip label="Default" size="small" color="primary" variant="filled" />
                          )}
                        </Box>
                      }
                      secondary={
                        <Box>
                          <Typography variant="body2" color="textSecondary">
                            {workflow.description}
                          </Typography>
                          <Typography variant="caption" color="textSecondary">
                            {workflow.definition.stages.length} stages • Est. {workflow.definition.total_estimated_time}
                          </Typography>
                        </Box>
                      }
                    />
                    <Button
                      size="small"
                      variant="outlined"
                      onClick={() => navigate(`/workflows/${workflow.id}`)}
                    >
                      View Details
                    </Button>
                  </ListItem>
                ))}
              </List>
            ) : (
              <Alert severity="info">
                No workflows found for this agent type.
              </Alert>
            )}
          </Paper>

          {/* Teams */}
          <Paper elevation={1} sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              <TeamIcon sx={{ verticalAlign: 'middle', mr: 1 }} />
              Team Assignments ({teams.length})
            </Typography>
            
            {teams.length > 0 ? (
              <Grid container spacing={2}>
                {teams.map((team) => (
                  <Grid item xs={12} md={6} key={team.id}>
                    <Card variant="outlined">
                      <CardContent>
                        <Typography variant="subtitle2" fontWeight="medium" gutterBottom>
                          {team.name}
                        </Typography>
                        <Typography variant="body2" color="textSecondary" paragraph>
                          {team.description}
                        </Typography>
                        <Box display="flex" justifyContent="space-between" alignItems="center">
                          <Typography variant="caption" color="textSecondary">
                            Project: {team.project_id} • {team.member_agent_ids?.length || 0} members
                          </Typography>
                          <Button
                            size="small"
                            variant="outlined"
                            onClick={() => navigate(`/teams/${team.id}`)}
                          >
                            View Team
                          </Button>
                        </Box>
                      </CardContent>
                    </Card>
                  </Grid>
                ))}
              </Grid>
            ) : (
              <Alert severity="info">
                No team assignments found for this agent type.
              </Alert>
            )}
          </Paper>
        </Grid>

        {/* Sidebar */}
        <Grid item xs={12} md={4}>
          {/* AI Model Assignment */}
          <Paper elevation={1} sx={{ p: 3, mb: 3 }}>
            <Typography variant="h6" gutterBottom>
              <AIModelIcon sx={{ verticalAlign: 'middle', mr: 1 }} />
              AI Model Configuration
            </Typography>
            
            {assignedModel ? (
              <Box>
                <Box mb={2}>
                  <Typography variant="subtitle2" fontWeight="medium">
                    {assignedModel.name}
                  </Typography>
                  <Typography variant="body2" color="textSecondary">
                    {assignedModel.provider} • {assignedModel.context_window.toLocaleString()} tokens
                  </Typography>
                </Box>
                
                {assignedModel.capabilities && (
                  <Box mb={2}>
                    <Typography variant="caption" color="textSecondary" display="block" gutterBottom>
                      Model Capabilities:
                    </Typography>
                    <Box display="flex" flexWrap="wrap" gap={0.5}>
                      {Object.entries(assignedModel.capabilities)
                        .filter(([_, enabled]) => enabled)
                        .map(([capability, _]) => (
                          <Chip
                            key={capability}
                            label={capability.replace(/_/g, ' ')}
                            size="small"
                            variant="outlined"
                            sx={{ fontSize: '0.65rem' }}
                          />
                        ))
                      }
                    </Box>
                  </Box>
                )}

                {assignedModel.performance_metrics && (
                  <Box mb={2}>
                    <Typography variant="caption" color="textSecondary" display="block" gutterBottom>
                      Performance Metrics:
                    </Typography>
                    {Object.entries(assignedModel.performance_metrics).map(([metric, value]) => (
                      <Box key={metric} display="flex" alignItems="center" gap={0.5} mb={0.5}>
                        {getPerformanceIcon(metric)}
                        <Typography variant="caption">
                          {metric}: {value}
                        </Typography>
                      </Box>
                    ))}
                  </Box>
                )}

                {agentType.model_config && (
                  <Box>
                    <Typography variant="caption" color="textSecondary" display="block" gutterBottom>
                      Agent-Specific Configuration:
                    </Typography>
                    {agentType.model_config.temperature !== undefined && (
                      <Typography variant="caption" display="block">
                        Temperature: {agentType.model_config.temperature}
                      </Typography>
                    )}
                    {agentType.model_config.max_tokens && (
                      <Typography variant="caption" display="block">
                        Max Tokens: {agentType.model_config.max_tokens}
                      </Typography>
                    )}
                  </Box>
                )}
              </Box>
            ) : (
              <Alert severity="warning">
                No AI model assigned to this agent type.
              </Alert>
            )}
          </Paper>

          {/* Default Configuration */}
          {agentType.default_config && (
            <Paper elevation={1} sx={{ p: 3 }}>
              <Typography variant="h6" gutterBottom>
                <TuneIcon sx={{ verticalAlign: 'middle', mr: 1 }} />
                Default Configuration
              </Typography>
              
              <Accordion>
                <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                  <Typography variant="subtitle2">
                    Configuration Settings ({Object.keys(agentType.default_config).length})
                  </Typography>
                </AccordionSummary>
                <AccordionDetails>
                  <Box>
                    {Object.entries(agentType.default_config).map(([key, value]) => (
                      <Box key={key} mb={1}>
                        <Typography variant="caption" color="textSecondary" display="block">
                          {key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}:
                        </Typography>
                        <Typography variant="body2">
                          {typeof value === 'object' ? JSON.stringify(value, null, 2) : String(value)}
                        </Typography>
                      </Box>
                    ))}
                  </Box>
                </AccordionDetails>
              </Accordion>
            </Paper>
          )}
        </Grid>
      </Grid>
    </Box>
  );
};

export default AgentTypeDetailPage;