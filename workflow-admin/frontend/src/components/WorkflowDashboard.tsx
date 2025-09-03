import React, { useState, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import {
  Box,
  Typography,
  Paper,
  Grid,
  Alert,
  CircularProgress,
  Card,
  CardContent,
  Chip,
  Button,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  Divider,
} from '@mui/material';
import {
  AccountTree as WorkflowIcon,
  Schedule as TimeIcon,
  Assignment as StepsIcon,
  CheckCircle as ActiveIcon,
  Cancel as InactiveIcon,
  ExpandMore as ExpandMoreIcon,
  Visibility as ViewIcon,
  Star as DefaultIcon,
} from '@mui/icons-material';
import { WorkflowTemplate, workflowsApi } from '../api/workflows';

const WorkflowDashboard: React.FC = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const [workflowTemplates, setWorkflowTemplates] = useState<WorkflowTemplate[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedAgentType, setSelectedAgentType] = useState<string | null>(null);

  useEffect(() => {
    // Check for agentType query parameter
    const params = new URLSearchParams(location.search);
    const agentType = params.get('agentType');
    setSelectedAgentType(agentType);
    
    loadData();
  }, [location]);

  const loadData = async () => {
    try {
      setLoading(true);
      setError(null);
      const templates = await workflowsApi.getWorkflowTemplates();
      setWorkflowTemplates(templates);
    } catch (err) {
      console.error('Error loading workflow templates:', err);
      setError('Failed to load workflow templates.');
    } finally {
      setLoading(false);
    }
  };

  // Group workflows by agent type
  const workflowsByAgentType = workflowTemplates.reduce((acc, template) => {
    if (!acc[template.agent_type]) {
      acc[template.agent_type] = [];
    }
    acc[template.agent_type].push(template);
    return acc;
  }, {} as Record<string, WorkflowTemplate[]>);

  const handleViewWorkflow = (templateId: number) => {
    navigate(`/workflows/${templateId}`);
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="200px">
        <CircularProgress />
        <Typography variant="body2" sx={{ ml: 2 }}>
          Loading workflow templates...
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
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Box>
          <Typography variant="h4" gutterBottom>
            Workflow Templates
          </Typography>
          <Typography variant="body1" color="textSecondary">
            {selectedAgentType 
              ? `Workflow versions for ${selectedAgentType} agent type`
              : 'Manage workflow templates organized by agent types with version control'
            }
          </Typography>
        </Box>
        {selectedAgentType && (
          <Button 
            variant="outlined" 
            onClick={() => {
              navigate('/workflows');
              setSelectedAgentType(null);
            }}
          >
            View All Agent Types
          </Button>
        )}
      </Box>

      <Grid container spacing={3}>
        {selectedAgentType ? (
          // Show specific agent type workflows
          <Grid item xs={12}>
            <Paper elevation={1} sx={{ p: 3 }}>
              <Typography variant="h6" gutterBottom>
                {selectedAgentType} Workflows ({workflowsByAgentType[selectedAgentType]?.length || 0} versions)
              </Typography>
              
              {workflowsByAgentType[selectedAgentType]?.length === 0 ? (
                <Box sx={{ p: 4, textAlign: 'center' }}>
                  <Typography variant="body2" color="textSecondary">
                    No workflow versions found for {selectedAgentType}
                  </Typography>
                </Box>
              ) : (
                <Grid container spacing={2}>
                  {workflowsByAgentType[selectedAgentType]?.map((template) => (
                    <Grid item xs={12} key={template.id}>
                      <Card variant="outlined">
                        <CardContent>
                          <Box display="flex" alignItems="center" gap={2} mb={2}>
                            <WorkflowIcon color="primary" sx={{ fontSize: 28 }} />
                            <Box flexGrow={1}>
                              <Box display="flex" alignItems="center" gap={1}>
                                <Typography variant="h6" fontWeight="medium">
                                  {template.name} {template.version}
                                </Typography>
                                {template.is_default && (
                                  <Chip
                                    icon={<DefaultIcon />}
                                    label="Default"
                                    size="small"
                                    color="primary"
                                    variant="filled"
                                  />
                                )}
                                <Chip
                                  icon={template.is_active ? <ActiveIcon /> : <InactiveIcon />}
                                  label={template.is_active ? 'Active' : 'Inactive'}
                                  size="small"
                                  color={template.is_active ? 'success' : 'default'}
                                  variant="outlined"
                                />
                              </Box>
                              <Typography variant="body2" color="textSecondary">
                                {template.description}
                              </Typography>
                            </Box>
                            <Button
                              variant="contained"
                              startIcon={<ViewIcon />}
                              onClick={() => handleViewWorkflow(template.id)}
                            >
                              View Workflow
                            </Button>
                          </Box>

                          <Divider sx={{ mb: 2 }} />

                          <Grid container spacing={2}>
                            <Grid item xs={12} md={4}>
                              <Box display="flex" alignItems="center" gap={1}>
                                <StepsIcon fontSize="small" color="action" />
                                <Typography variant="body2" color="textSecondary">
                                  {template.definition.stages.length} stages
                                </Typography>
                              </Box>
                            </Grid>
                            <Grid item xs={12} md={4}>
                              <Box display="flex" alignItems="center" gap={1}>
                                <TimeIcon fontSize="small" color="action" />
                                <Typography variant="body2" color="textSecondary">
                                  {template.definition.total_estimated_time}
                                </Typography>
                              </Box>
                            </Grid>
                            <Grid item xs={12} md={4}>
                              <Typography variant="caption" color="textSecondary">
                                Created: {new Date(template.created_at).toLocaleDateString()}
                              </Typography>
                            </Grid>
                          </Grid>

                          {template.change_notes && (
                            <Box sx={{ mt: 2, p: 1, backgroundColor: 'grey.50', borderRadius: 1 }}>
                              <Typography variant="caption" color="textSecondary">
                                <strong>Change Notes:</strong> {template.change_notes}
                              </Typography>
                            </Box>
                          )}
                        </CardContent>
                      </Card>
                    </Grid>
                  ))}
                </Grid>
              )}
            </Paper>
          </Grid>
        ) : (
          // Show all agent types with their workflows
          <Grid item xs={12}>
            {Object.keys(workflowsByAgentType).length === 0 ? (
              <Paper elevation={1} sx={{ p: 4, textAlign: 'center' }}>
                <Typography variant="h6" color="textSecondary" gutterBottom>
                  No Workflow Templates Found
                </Typography>
                <Typography variant="body2" color="textSecondary">
                  Create workflow templates to define agent behaviors.
                </Typography>
              </Paper>
            ) : (
              Object.entries(workflowsByAgentType).map(([agentType, templates]) => (
                <Accordion key={agentType} defaultExpanded>
                  <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                    <Box display="flex" alignItems="center" gap={2}>
                      <WorkflowIcon color="primary" />
                      <Box>
                        <Typography variant="h6">
                          {agentType} Workflows
                        </Typography>
                        <Typography variant="body2" color="textSecondary">
                          {templates.length} version{templates.length !== 1 ? 's' : ''} • 
                          {templates.filter(t => t.is_active).length} active
                        </Typography>
                      </Box>
                    </Box>
                  </AccordionSummary>
                  <AccordionDetails>
                    <Grid container spacing={2}>
                      {templates.map((template) => (
                        <Grid item xs={12} md={6} key={template.id}>
                          <Card variant="outlined" sx={{ height: '100%' }}>
                            <CardContent>
                              <Box display="flex" alignItems="center" gap={1} mb={1}>
                                <Typography variant="subtitle1" fontWeight="medium">
                                  {template.version}
                                </Typography>
                                {template.is_default && (
                                  <Chip
                                    icon={<DefaultIcon />}
                                    label="Default"
                                    size="small"
                                    color="primary"
                                    variant="filled"
                                  />
                                )}
                                <Chip
                                  icon={template.is_active ? <ActiveIcon /> : <InactiveIcon />}
                                  label={template.is_active ? 'Active' : 'Inactive'}
                                  size="small"
                                  color={template.is_active ? 'success' : 'default'}
                                  variant="outlined"
                                />
                              </Box>

                              <Typography variant="body2" color="textSecondary" paragraph>
                                {template.description}
                              </Typography>

                              <Box display="flex" alignItems="center" gap={2} mb={2}>
                                <Box display="flex" alignItems="center" gap={0.5}>
                                  <StepsIcon fontSize="small" color="action" />
                                  <Typography variant="caption" color="textSecondary">
                                    {template.definition.stages.length} stages
                                  </Typography>
                                </Box>
                                <Box display="flex" alignItems="center" gap={0.5}>
                                  <TimeIcon fontSize="small" color="action" />
                                  <Typography variant="caption" color="textSecondary">
                                    {template.definition.total_estimated_time}
                                  </Typography>
                                </Box>
                              </Box>

                              <Button
                                variant="outlined"
                                size="small"
                                fullWidth
                                startIcon={<ViewIcon />}
                                onClick={() => handleViewWorkflow(template.id)}
                              >
                                View Details
                              </Button>

                              {template.change_notes && (
                                <Box sx={{ mt: 1 }}>
                                  <Typography variant="caption" color="textSecondary">
                                    {template.change_notes}
                                  </Typography>
                                </Box>
                              )}
                            </CardContent>
                          </Card>
                        </Grid>
                      ))}
                    </Grid>
                  </AccordionDetails>
                </Accordion>
              ))
            )}
          </Grid>
        )}
      </Grid>
    </Box>
  );
};

export default WorkflowDashboard;