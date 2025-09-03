import React, { useState, useEffect } from 'react';
import { useParams, useNavigate, useSearchParams, useLocation } from 'react-router-dom';
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
  Divider,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  Stepper,
  Step,
  StepLabel,
  StepContent,
} from '@mui/material';
import {
  ArrowBack as BackIcon,
  AccountTree as WorkflowIcon,
  Schedule as TimeIcon,
  Assignment as StepsIcon,
  CheckCircle as ActiveIcon,
  Cancel as InactiveIcon,
  Star as DefaultIcon,
  Input as InputIcon,
  Output as OutputIcon,
  SmartToy as AIIcon,
  Link as IntegrationIcon,
  Timer as TimerIcon,
  PlayArrow as PlayIcon,
  Psychology as AIModelIcon,
  Tune as ConfigIcon,
  Code as CodeIcon,
  Description as TemplateIcon,
  AutoAwesome as ExampleIcon,
  Warning as ImportantIcon,
} from '@mui/icons-material';
import { WorkflowTemplate, workflowsApi } from '../api/workflows';
import { AIModel, modelsApi } from '../api/models';
import { agentsApi } from '../api/agents';

const WorkflowDetailPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const location = useLocation();
  const [workflow, setWorkflow] = useState<WorkflowTemplate | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [activeStep, setActiveStep] = useState(0);
  const [assignedModel, setAssignedModel] = useState<AIModel | null>(null);

  // Extract navigation context from URL params or state
  const fromAgent = searchParams.get('agent');
  const fromRole = searchParams.get('role');
  const fromProject = searchParams.get('project');
  const referrer = location.state?.from;

  useEffect(() => {
    const loadWorkflow = async () => {
      if (!id) return;
      
      try {
        setLoading(true);
        setError(null);
        
        const workflowData = await workflowsApi.getWorkflowTemplate(parseInt(id));
        setWorkflow(workflowData);
        
        // Load the associated agent type and its assigned model
        try {
          const agentTypes = await agentsApi.getAgentTypes();
          const agentType = agentTypes.find(at => at.name === workflowData.agent_type);
          
          if (agentType?.assigned_model_id) {
            const models = await modelsApi.getModels();
            const model = models.find(m => m.id === agentType.assigned_model_id);
            setAssignedModel(model || null);
          }
        } catch (modelError) {
          console.warn('Could not load model information:', modelError);
        }
      } catch (error) {
        console.error('Error loading workflow:', error);
        setError('Failed to load workflow details');
      } finally {
        setLoading(false);
      }
    };

    loadWorkflow();
  }, [id]);

  const handleBack = () => {
    // Smart back navigation based on context
    if (referrer) {
      // If we have a specific referrer from navigation state, use it
      navigate(referrer);
    } else if (fromProject) {
      // If we came from a specific project, go back to that project's detail page
      navigate(`/projects/${fromProject}`);
    } else if (fromAgent || fromRole) {
      // If we came from a team member, go back to workflows filtered by agent type
      navigate(`/workflows?agentType=${encodeURIComponent(workflow?.agent_type || '')}`);
    } else {
      // Default fallback to workflows list
      navigate('/workflows');
    }
  };

  const getBackButtonText = () => {
    if (fromProject) {
      return 'Back to Project';
    } else if (fromAgent) {
      return `Back to ${fromAgent}`;
    } else if (fromRole) {
      return `Back to ${fromRole} Workflows`;
    } else {
      return 'Back to Workflows';
    }
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="200px">
        <CircularProgress />
        <Typography variant="body2" sx={{ ml: 2 }}>
          Loading workflow details...
        </Typography>
      </Box>
    );
  }

  if (error || !workflow) {
    return (
      <Box>
        <Button
          startIcon={<BackIcon />}
          onClick={handleBack}
          sx={{ mb: 2 }}
        >
          {getBackButtonText()}
        </Button>
        <Alert severity="error">
          {error || 'Workflow not found'}
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
          {getBackButtonText()}
        </Button>
        <Box flexGrow={1}>
          <Box display="flex" alignItems="center" gap={2}>
            <WorkflowIcon color="primary" sx={{ fontSize: 32 }} />
            <Box>
              <Typography variant="h4" gutterBottom>
                {workflow.name} {workflow.version}
              </Typography>
              <Box display="flex" gap={1}>
                {workflow.is_default && (
                  <Chip
                    icon={<DefaultIcon />}
                    label="Default Version"
                    size="small"
                    color="primary"
                    variant="filled"
                  />
                )}
                <Chip
                  icon={workflow.is_active ? <ActiveIcon /> : <InactiveIcon />}
                  label={workflow.is_active ? 'Active' : 'Inactive'}
                  size="small"
                  color={workflow.is_active ? 'success' : 'default'}
                  variant="outlined"
                />
                <Chip
                  label={workflow.agent_type}
                  size="small"
                  variant="outlined"
                  color="secondary"
                />
              </Box>
            </Box>
          </Box>
        </Box>
      </Box>

      <Grid container spacing={3}>
        {/* Workflow Information */}
        <Grid item xs={12} md={8}>
          <Paper elevation={1} sx={{ p: 3, mb: 3 }}>
            <Typography variant="h6" gutterBottom>
              Workflow Information
            </Typography>
            
            <Typography variant="body2" color="textSecondary" paragraph>
              <strong>Description:</strong> {workflow.description || 'No description provided'}
            </Typography>

            <Grid container spacing={2} sx={{ mb: 2 }}>
              <Grid item xs={12} md={4}>
                <Box display="flex" alignItems="center" gap={1}>
                  <StepsIcon fontSize="small" color="action" />
                  <Typography variant="body2" color="textSecondary">
                    <strong>Stages:</strong> {workflow.definition.stages.length}
                  </Typography>
                </Box>
              </Grid>
              <Grid item xs={12} md={4}>
                <Box display="flex" alignItems="center" gap={1}>
                  <TimeIcon fontSize="small" color="action" />
                  <Typography variant="body2" color="textSecondary">
                    <strong>Duration:</strong> {workflow.definition.total_estimated_time}
                  </Typography>
                </Box>
              </Grid>
              <Grid item xs={12} md={4}>
                <Typography variant="body2" color="textSecondary">
                  <strong>Created:</strong> {new Date(workflow.created_at).toLocaleDateString()}
                </Typography>
              </Grid>
            </Grid>

            {workflow.change_notes && (
              <Box sx={{ p: 2, backgroundColor: 'grey.50', borderRadius: 1, mb: 2 }}>
                <Typography variant="body2" color="text.primary">
                  <strong>Change Notes:</strong> {workflow.change_notes}
                </Typography>
              </Box>
            )}

            {/* Context Configuration Summary */}
            <Box sx={{ mt: 2 }}>
              <Typography variant="subtitle2" gutterBottom color="secondary">
                Stage Context Configuration
              </Typography>
              <Box display="flex" flexWrap="wrap" gap={1} mb={2}>
                {workflow.definition.stages.map((stage, index) => (
                  <Chip
                    key={index}
                    label={stage.name.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}
                    size="small"
                    icon={stage.context_config ? <ConfigIcon /> : undefined}
                    color={stage.context_config ? 'secondary' : 'default'}
                    variant={stage.context_config ? 'filled' : 'outlined'}
                  />
                ))}
              </Box>
              <Typography variant="caption" color="textSecondary">
                {workflow.definition.stages.filter(s => s.context_config).length} of {workflow.definition.stages.length} stages have custom AI context configuration
              </Typography>
            </Box>

            {/* Success Criteria */}
            <Box sx={{ mt: 2 }}>
              <Typography variant="subtitle2" gutterBottom color="primary">
                Success Criteria
              </Typography>
              <Box display="flex" flexWrap="wrap" gap={0.5}>
                {workflow.definition.success_criteria.map((criterion, index) => (
                  <Chip
                    key={index}
                    label={criterion}
                    size="small"
                    variant="outlined"
                    color="success"
                  />
                ))}
              </Box>
            </Box>
          </Paper>

          {/* Visual Workflow Flow */}
          <Paper elevation={1} sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Workflow Stages
            </Typography>
            
            <Stepper 
              activeStep={activeStep} 
              orientation="vertical"
              sx={{ mt: 2 }}
            >
              {workflow.definition.stages.map((stage, index) => (
                <Step key={stage.name}>
                  <StepLabel
                    onClick={() => setActiveStep(index)}
                    sx={{ cursor: 'pointer' }}
                  >
                    <Box display="flex" alignItems="center" gap={1}>
                      <Typography variant="subtitle1" fontWeight="medium">
                        {stage.name.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}
                      </Typography>
                      {stage.context_config && (
                        <Chip
                          icon={<ConfigIcon />}
                          label="Custom Context"
                          size="small"
                          color="secondary"
                          variant="filled"
                          sx={{ fontSize: '0.7rem', height: '20px' }}
                        />
                      )}
                    </Box>
                  </StepLabel>
                  <StepContent>
                    <Grid container spacing={2}>
                      {/* Stage Context Configuration - Now First and Most Prominent */}
                      {stage.context_config && (
                        <Grid item xs={12}>
                          <Card 
                            sx={{ 
                              mb: 2,
                              border: '2px solid',
                              borderColor: 'secondary.main',
                              backgroundColor: 'secondary.light',
                              backgroundImage: 'linear-gradient(45deg, transparent 25%, rgba(255,255,255,0.1) 25%, rgba(255,255,255,0.1) 50%, transparent 50%, transparent 75%, rgba(255,255,255,0.1) 75%)',
                              backgroundSize: '20px 20px'
                            }}
                          >
                            <CardContent>
                              <Box display="flex" alignItems="center" gap={1} mb={3}>
                                <ImportantIcon fontSize="small" color="secondary" />
                                <Typography variant="h6" color="secondary.main" fontWeight="bold">
                                  🎯 Custom AI Context Configuration
                                </Typography>
                                <Chip 
                                  label="Critical for Performance" 
                                  size="small" 
                                  color="warning" 
                                  variant="filled"
                                />
                              </Box>
                              
                              {stage.context_config.system_prompt && (
                                <Card variant="outlined" sx={{ mb: 3, backgroundColor: 'background.paper' }}>
                                  <CardContent>
                                    <Box display="flex" alignItems="center" gap={1} mb={2}>
                                      <CodeIcon fontSize="small" color="primary" />
                                      <Typography variant="subtitle1" color="primary" fontWeight="bold">
                                        System Prompt
                                      </Typography>
                                    </Box>
                                    <Paper 
                                      sx={{ 
                                        p: 2, 
                                        backgroundColor: '#f8f9fa',
                                        border: '1px solid #dee2e6',
                                        fontFamily: 'monospace'
                                      }}
                                    >
                                      <Typography 
                                        variant="body2" 
                                        sx={{ 
                                          fontFamily: 'Consolas, "Courier New", monospace',
                                          fontSize: '0.9rem',
                                          lineHeight: 1.6,
                                          whiteSpace: 'pre-wrap'
                                        }}
                                      >
                                        {stage.context_config.system_prompt}
                                      </Typography>
                                    </Paper>
                                  </CardContent>
                                </Card>
                              )}

                              {stage.context_config.user_prompt_template && (
                                <Card variant="outlined" sx={{ mb: 3, backgroundColor: 'background.paper' }}>
                                  <CardContent>
                                    <Box display="flex" alignItems="center" gap={1} mb={2}>
                                      <TemplateIcon fontSize="small" color="info" />
                                      <Typography variant="subtitle1" color="info.main" fontWeight="bold">
                                        User Prompt Template
                                      </Typography>
                                    </Box>
                                    <Paper 
                                      sx={{ 
                                        p: 2, 
                                        backgroundColor: '#f0f8ff',
                                        border: '1px solid #b6d7ff',
                                        fontFamily: 'monospace'
                                      }}
                                    >
                                      <Typography 
                                        variant="body2" 
                                        sx={{ 
                                          fontFamily: 'Consolas, "Courier New", monospace',
                                          fontSize: '0.9rem',
                                          lineHeight: 1.6,
                                          whiteSpace: 'pre-wrap'
                                        }}
                                      >
                                        {stage.context_config.user_prompt_template}
                                      </Typography>
                                    </Paper>
                                  </CardContent>
                                </Card>
                              )}

                              <Grid container spacing={2} sx={{ mb: 2 }}>
                                {stage.context_config.temperature !== undefined && (
                                  <Grid item xs={12} sm={6} md={3}>
                                    <Card variant="outlined" sx={{ textAlign: 'center', p: 1 }}>
                                      <Typography variant="caption" color="textSecondary">Temperature</Typography>
                                      <Typography variant="h6" color="primary">{stage.context_config.temperature}</Typography>
                                    </Card>
                                  </Grid>
                                )}
                                {stage.context_config.max_tokens !== undefined && (
                                  <Grid item xs={12} sm={6} md={3}>
                                    <Card variant="outlined" sx={{ textAlign: 'center', p: 1 }}>
                                      <Typography variant="caption" color="textSecondary">Max Tokens</Typography>
                                      <Typography variant="h6" color="primary">{stage.context_config.max_tokens}</Typography>
                                    </Card>
                                  </Grid>
                                )}
                                {stage.context_config.response_format && (
                                  <Grid item xs={12} sm={6} md={3}>
                                    <Card variant="outlined" sx={{ textAlign: 'center', p: 1 }}>
                                      <Typography variant="caption" color="textSecondary">Response Format</Typography>
                                      <Typography variant="h6" color="primary">{stage.context_config.response_format}</Typography>
                                    </Card>
                                  </Grid>
                                )}
                              </Grid>

                              {stage.context_config.examples && stage.context_config.examples.length > 0 && (
                                <Card variant="outlined" sx={{ backgroundColor: 'background.paper' }}>
                                  <CardContent>
                                    <Box display="flex" alignItems="center" gap={1} mb={2}>
                                      <ExampleIcon fontSize="small" color="success" />
                                      <Typography variant="subtitle1" color="success.main" fontWeight="bold">
                                        Examples for Few-Shot Learning
                                      </Typography>
                                    </Box>
                                    {stage.context_config.examples.map((example, idx) => (
                                      <Paper 
                                        key={idx}
                                        sx={{ 
                                          p: 2, 
                                          mb: idx < stage.context_config.examples.length - 1 ? 2 : 0,
                                          backgroundColor: '#f0fff0',
                                          border: '1px solid #90ee90',
                                          fontStyle: 'italic'
                                        }}
                                      >
                                        <Typography variant="body2">
                                          "{example}"
                                        </Typography>
                                      </Paper>
                                    ))}
                                  </CardContent>
                                </Card>
                              )}
                            </CardContent>
                          </Card>
                        </Grid>
                      )}

                      {/* Basic Stage Information - Now Secondary */}
                      <Grid item xs={12}>
                        <Card variant="outlined" sx={{ mb: 2 }}>
                          <CardContent>
                            <Typography variant="h6" gutterBottom color="primary">
                              Stage Overview
                            </Typography>
                            <Typography variant="body2" color="textSecondary" paragraph>
                              {stage.description}
                            </Typography>

                            <Grid container spacing={3}>
                              {/* Inputs */}
                              <Grid item xs={12} md={6}>
                                <Box display="flex" alignItems="center" gap={1} mb={1}>
                                  <InputIcon fontSize="small" color="info" />
                                  <Typography variant="subtitle2" color="info.main">
                                    Inputs ({stage.inputs.length})
                                  </Typography>
                                </Box>
                                <List dense>
                                  {stage.inputs.map((input, idx) => (
                                    <ListItem key={idx} disablePadding>
                                      <ListItemText 
                                        primary={
                                          <Typography variant="body2">
                                            {input.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}
                                          </Typography>
                                        }
                                      />
                                    </ListItem>
                                  ))}
                                </List>
                              </Grid>

                              {/* Outputs */}
                              <Grid item xs={12} md={6}>
                                <Box display="flex" alignItems="center" gap={1} mb={1}>
                                  <OutputIcon fontSize="small" color="success" />
                                  <Typography variant="subtitle2" color="success.main">
                                    Outputs ({stage.outputs.length})
                                  </Typography>
                                </Box>
                                <List dense>
                                  {stage.outputs.map((output, idx) => (
                                    <ListItem key={idx} disablePadding>
                                      <ListItemText 
                                        primary={
                                          <Typography variant="body2">
                                            {output.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}
                                          </Typography>
                                        }
                                      />
                                    </ListItem>
                                  ))}
                                </List>
                              </Grid>
                            </Grid>

                            <Divider sx={{ my: 2 }} />

                            {/* Technical Details */}
                            <Grid container spacing={2}>
                              <Grid item xs={12} md={4}>
                                <Box display="flex" alignItems="center" gap={1}>
                                  <TimerIcon fontSize="small" color="warning" />
                                  <Typography variant="body2" color="textSecondary">
                                    <strong>Timeout:</strong> {stage.timeout}s
                                  </Typography>
                                </Box>
                              </Grid>

                              {stage.ai_prompts && stage.ai_prompts.length > 0 && (
                                <Grid item xs={12} md={4}>
                                  <Box display="flex" alignItems="center" gap={1}>
                                    <AIIcon fontSize="small" color="secondary" />
                                    <Typography variant="body2" color="textSecondary">
                                      <strong>AI Prompts:</strong> {stage.ai_prompts.length}
                                    </Typography>
                                  </Box>
                                </Grid>
                              )}

                              {stage.integrations && stage.integrations.length > 0 && (
                                <Grid item xs={12} md={4}>
                                  <Box display="flex" alignItems="center" gap={1}>
                                    <IntegrationIcon fontSize="small" color="primary" />
                                    <Typography variant="body2" color="textSecondary">
                                      <strong>Integrations:</strong> {stage.integrations.join(', ')}
                                    </Typography>
                                  </Box>
                                </Grid>
                              )}
                            </Grid>
                          </CardContent>
                        </Card>
                      </Grid>
                    </Grid>

                    <Box sx={{ mb: 1 }}>
                      <Button
                        variant="contained"
                        size="small"
                        onClick={() => setActiveStep(index + 1)}
                        disabled={index === workflow.definition.stages.length - 1}
                        startIcon={<PlayIcon />}
                      >
                        {index === workflow.definition.stages.length - 1 ? 'Final Stage' : 'Next Stage'}
                      </Button>
                    </Box>
                  </StepContent>
                </Step>
              ))}
            </Stepper>
          </Paper>
        </Grid>

        {/* Sidebar - Additional Information */}
        <Grid item xs={12} md={4}>
          <Paper elevation={1} sx={{ p: 3, mb: 3 }}>
            <Typography variant="h6" gutterBottom>
              Workflow Configuration
            </Typography>

            {/* AI Model Information */}
            {assignedModel && (
              <Box sx={{ mb: 3 }}>
                <Typography variant="subtitle2" gutterBottom color="primary">
                  <Box display="flex" alignItems="center" gap={1}>
                    <AIModelIcon fontSize="small" />
                    AI Model
                  </Box>
                </Typography>
                <Typography variant="body2" fontWeight="medium" paragraph>
                  {assignedModel.name}
                </Typography>
                <Typography variant="body2" color="textSecondary" paragraph>
                  <strong>Provider:</strong> {assignedModel.provider}
                </Typography>
                <Typography variant="body2" color="textSecondary" paragraph>
                  <strong>Context Window:</strong> {assignedModel.context_window.toLocaleString()} tokens
                </Typography>
                {assignedModel.performance_metrics && (
                  <Box display="flex" gap={1} mb={1}>
                    <Chip 
                      label={`Quality: ${assignedModel.performance_metrics.quality}`} 
                      size="small" 
                      color="success"
                      variant="outlined"
                    />
                    <Chip 
                      label={`Speed: ${assignedModel.performance_metrics.speed}`} 
                      size="small" 
                      color="info"
                      variant="outlined"
                    />
                  </Box>
                )}
                <Typography variant="caption" color="textSecondary">
                  Best for: {assignedModel.best_for.join(', ')}
                </Typography>
              </Box>
            )}

            {/* Monitoring Settings */}
            {workflow.definition.monitoring && (
              <Box sx={{ mb: 3 }}>
                <Typography variant="subtitle2" gutterBottom color="primary">
                  Monitoring
                </Typography>
                <Typography variant="body2" color="textSecondary" paragraph>
                  <strong>Continuous:</strong> {workflow.definition.monitoring.continuous_monitoring ? 'Yes' : 'No'}
                </Typography>
                {workflow.definition.monitoring.check_interval && (
                  <Typography variant="body2" color="textSecondary" paragraph>
                    <strong>Check Interval:</strong> {workflow.definition.monitoring.check_interval}s
                  </Typography>
                )}
                {workflow.definition.monitoring.trigger_conditions && (
                  <Box>
                    <Typography variant="caption" color="textSecondary" gutterBottom display="block">
                      <strong>Trigger Conditions:</strong>
                    </Typography>
                    {workflow.definition.monitoring.trigger_conditions.map((condition, index) => (
                      <Chip
                        key={index}
                        label={condition}
                        size="small"
                        variant="outlined"
                        sx={{ mr: 0.5, mb: 0.5, fontSize: '0.7rem' }}
                      />
                    ))}
                  </Box>
                )}
              </Box>
            )}

            {/* Automation Support */}
            {workflow.definition.automation_support && (
              <Box sx={{ mb: 3 }}>
                <Typography variant="subtitle2" gutterBottom color="primary">
                  Automation Support
                </Typography>
                <Typography variant="body2" color="textSecondary">
                  This workflow supports automation features
                </Typography>
              </Box>
            )}

            {/* Version History */}
            <Box>
              <Typography variant="subtitle2" gutterBottom color="primary">
                Version Information
              </Typography>
              <Typography variant="body2" color="textSecondary" paragraph>
                <strong>Current Version:</strong> {workflow.version}
              </Typography>
              <Typography variant="body2" color="textSecondary" paragraph>
                <strong>Agent Type:</strong> {workflow.agent_type}
              </Typography>
              <Button
                variant="outlined"
                size="small"
                fullWidth
                onClick={() => navigate(`/workflows?agentType=${encodeURIComponent(workflow.agent_type)}`)}
              >
                View All Versions
              </Button>
            </Box>
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
};

export default WorkflowDetailPage;