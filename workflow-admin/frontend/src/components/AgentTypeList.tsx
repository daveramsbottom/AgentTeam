import React from 'react';
import {
  Grid,
  Card,
  CardContent,
  Chip,
  Box,
  Typography,
  Button,
  Divider,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
} from '@mui/material';
import {
  SmartToy as RobotIcon,
  CheckCircle as ActiveIcon,
  Cancel as InactiveIcon,
  AccountTree as WorkflowIcon,
  Build as CapabilityIcon,
  Settings as ConfigIcon,
  Psychology as AIModelIcon,
} from '@mui/icons-material';
import { AgentType } from '../api/agents';
import { AIModel, modelsApi } from '../api/models';
import { useNavigate } from 'react-router-dom';

interface AgentTypeListProps {
  agentTypes: AgentType[];
}

const AgentTypeList: React.FC<AgentTypeListProps> = ({ agentTypes }) => {
  const navigate = useNavigate();
  const [models, setModels] = React.useState<AIModel[]>([]);

  React.useEffect(() => {
    const loadModels = async () => {
      try {
        const modelsData = await modelsApi.getModels();
        setModels(modelsData);
      } catch (error) {
        console.error('Error loading models:', error);
      }
    };
    loadModels();
  }, []);

  const handleWorkflowClick = (agentTypeName: string) => {
    navigate(`/workflows?agentType=${encodeURIComponent(agentTypeName)}`);
  };

  const getAssignedModel = (agentType: AgentType): AIModel | undefined => {
    return agentType.assigned_model_id ? models.find(m => m.id === agentType.assigned_model_id) : undefined;
  };

  if (agentTypes.length === 0) {
    return (
      <Box sx={{ p: 4, textAlign: 'center' }}>
        <Typography variant="h6" color="textSecondary" gutterBottom>
          No Agent Types Defined
        </Typography>
        <Typography variant="body2" color="textSecondary">
          Create agent types to define role-based templates for team building.
        </Typography>
      </Box>
    );
  }

  const getWorkflowName = (agentType: AgentType) => {
    return agentType.workflow_preferences?.default_workflow || 'No workflow assigned';
  };

  const getCapabilitiesCount = (agentType: AgentType) => {
    return agentType.capabilities ? Object.keys(agentType.capabilities).length : 0;
  };

  const getKeyCapabilities = (agentType: AgentType) => {
    if (!agentType.capabilities) return [];
    return Object.entries(agentType.capabilities)
      .filter(([_, value]) => value === true)
      .slice(0, 3)
      .map(([key, _]) => key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase()));
  };

  return (
    <Grid container spacing={3}>
      {agentTypes.map((agentType) => (
        <Grid item xs={12} md={6} lg={4} key={agentType.id}>
          <Card 
            variant="outlined" 
            sx={{ 
              height: '100%',
              display: 'flex',
              flexDirection: 'column',
              '&:hover': { elevation: 2 }
            }}
          >
            <CardContent sx={{ flexGrow: 1 }}>
              {/* Header with Role and Status */}
              <Box display="flex" alignItems="center" gap={1} mb={2}>
                <RobotIcon color="primary" sx={{ fontSize: 28 }} />
                <Box flexGrow={1}>
                  <Typography variant="h6" fontWeight="medium">
                    {agentType.name}
                  </Typography>
                  <Chip
                    icon={agentType.is_active ? <ActiveIcon /> : <InactiveIcon />}
                    label={agentType.is_active ? 'Active' : 'Inactive'}
                    size="small"
                    color={agentType.is_active ? 'success' : 'default'}
                    variant="outlined"
                  />
                </Box>
              </Box>

              {/* Description */}
              {agentType.description && (
                <Typography variant="body2" color="textSecondary" paragraph>
                  {agentType.description}
                </Typography>
              )}

              {/* Workflow Assignment */}
              <Box 
                display="flex" 
                alignItems="center" 
                gap={1} 
                mb={2}
                sx={{ 
                  cursor: 'pointer',
                  p: 1,
                  borderRadius: 1,
                  '&:hover': { backgroundColor: 'action.hover' }
                }}
                onClick={() => handleWorkflowClick(agentType.name)}
              >
                <WorkflowIcon fontSize="small" color="info" />
                <Box flexGrow={1}>
                  <Typography variant="subtitle2" color="primary">
                    Workflow: {getWorkflowName(agentType)}
                  </Typography>
                  <Typography variant="caption" color="textSecondary">
                    Click to view workflow details
                  </Typography>
                </Box>
              </Box>

              <Divider sx={{ my: 2 }} />

              {/* AI Model Assignment */}
              {(() => {
                const assignedModel = getAssignedModel(agentType);
                return (
                  <Box mb={2}>
                    <Box display="flex" alignItems="center" gap={1} mb={1}>
                      <AIModelIcon fontSize="small" color="secondary" />
                      <Typography variant="subtitle2" color="secondary.main">
                        AI Model
                      </Typography>
                    </Box>
                    {assignedModel ? (
                      <Box>
                        <Typography variant="body2" fontWeight="medium">
                          {assignedModel.name}
                        </Typography>
                        <Typography variant="caption" color="textSecondary">
                          {assignedModel.provider} • {assignedModel.context_window.toLocaleString()} tokens
                        </Typography>
                        {agentType.model_config?.temperature !== undefined && (
                          <Typography variant="caption" color="textSecondary" sx={{ display: 'block' }}>
                            Temperature: {agentType.model_config.temperature}
                          </Typography>
                        )}
                      </Box>
                    ) : (
                      <Typography variant="body2" color="textSecondary">
                        No model assigned
                      </Typography>
                    )}
                  </Box>
                );
              })()}

              <Divider sx={{ my: 2 }} />

              {/* Key Capabilities */}
              <Box mb={2}>
                <Box display="flex" alignItems="center" gap={1} mb={1}>
                  <CapabilityIcon fontSize="small" color="secondary" />
                  <Typography variant="subtitle2">
                    Key Capabilities ({getCapabilitiesCount(agentType)})
                  </Typography>
                </Box>
                <Box display="flex" flexWrap="wrap" gap={0.5}>
                  {getKeyCapabilities(agentType).map((capability, index) => (
                    <Chip
                      key={index}
                      label={capability}
                      size="small"
                      variant="outlined"
                      color="secondary"
                      sx={{ fontSize: '0.7rem' }}
                    />
                  ))}
                  {getCapabilitiesCount(agentType) > 3 && (
                    <Chip
                      label={`+${getCapabilitiesCount(agentType) - 3} more`}
                      size="small"
                      variant="outlined"
                      color="default"
                      sx={{ fontSize: '0.7rem' }}
                    />
                  )}
                </Box>
              </Box>

              {/* Configuration Info */}
              {agentType.default_config && (
                <Box>
                  <Box display="flex" alignItems="center" gap={1} mb={1}>
                    <ConfigIcon fontSize="small" color="action" />
                    <Typography variant="subtitle2" color="textSecondary">
                      Default Configuration
                    </Typography>
                  </Box>
                  <Typography variant="caption" color="textSecondary">
                    {Object.keys(agentType.default_config).length} settings configured
                  </Typography>
                </Box>
              )}
            </CardContent>

            {/* Actions */}
            <Box sx={{ p: 2, pt: 0 }}>
              <Button 
                variant="outlined" 
                size="small" 
                fullWidth
                sx={{ mb: 1 }}
                onClick={() => navigate(`/agents/${agentType.id}`)}
              >
                View Details
              </Button>
              <Typography variant="caption" color="textSecondary" align="center" display="block">
                Last updated: {new Date(agentType.updated_at || agentType.created_at).toLocaleDateString()}
              </Typography>
            </Box>
          </Card>
        </Grid>
      ))}
    </Grid>
  );
};

export default AgentTypeList;