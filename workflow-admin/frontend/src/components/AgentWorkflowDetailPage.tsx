import React, { useState, useEffect } from 'react';
import { useParams, useNavigate, useSearchParams } from 'react-router-dom';
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
  Accordion,
  AccordionSummary,
  AccordionDetails,
  IconButton,
} from '@mui/material';
import {
  ArrowBack as BackIcon,
  AccountTree as WorkflowIcon,
  Person as AgentIcon,
  Group as TeamIcon,
  PlayArrow as StateIcon,
  Schedule as TimeIcon,
  Psychology as ContextIcon,
  Assignment as TaskIcon,
  CheckCircle as ActiveIcon,
  Cancel as InactiveIcon,
  Edit as EditIcon,
  ExpandMore as ExpandMoreIcon,
  FolderOpen as ProjectIcon,
  Star as VersionIcon,
} from '@mui/icons-material';
import { AgentWorkflow, workflowsApi } from '../api/workflows';
import { Agent, agentsApi } from '../api/agents';
import { Team, teamsApi } from '../api/teams';
import { Project, projectsApi } from '../api/projects';
import { EditButton } from './common';

const AgentWorkflowDetailPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const [workflow, setWorkflow] = useState<AgentWorkflow | null>(null);
  const [assignedAgents, setAssignedAgents] = useState<Agent[]>([]);
  const [team, setTeam] = useState<Team | null>(null);
  const [project, setProject] = useState<Project | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [expandedState, setExpandedState] = useState<string | false>(false);

  // Extract navigation context from URL params
  const fromAgentType = searchParams.get('agentType');

  useEffect(() => {
    const loadWorkflowDetails = async () => {
      if (!id) return;
      
      try {
        setLoading(true);
        setError(null);
        
        // Load workflow details
        const workflowData = await workflowsApi.getAgentWorkflow(parseInt(id));
        setWorkflow(workflowData);
        
        // Load related data in parallel
        const promises = [];
        
        // Load all agents that are compatible with this workflow
        promises.push(
          agentsApi.getAgents()
            .then(allAgents => {
              // Filter agents that match this workflow's agent type
              const compatibleAgents = allAgents.filter(agent => 
                agent.agent_type?.name === workflowData.definition.agent_type_category
              );
              setAssignedAgents(compatibleAgents);
            })
            .catch(err => console.warn('Could not load compatible agents:', err))
        );
        
        // Load team details if assigned
        if (workflowData.assigned_team_id) {
          promises.push(
            teamsApi.getTeam(workflowData.assigned_team_id)
              .then(teamData => setTeam(teamData))
              .catch(err => console.warn('Could not load team:', err))
          );
        }
        
        // Load project details
        if (workflowData.project_id) {
          promises.push(
            projectsApi.getProject(workflowData.project_id)
              .then(projectData => setProject(projectData))
              .catch(err => console.warn('Could not load project:', err))
          );
        }
        
        await Promise.all(promises);
      } catch (error) {
        console.error('Error loading workflow:', error);
        setError('Failed to load workflow details');
      } finally {
        setLoading(false);
      }
    };

    loadWorkflowDetails();
  }, [id]);

  const handleBack = () => {
    if (fromAgentType) {
      navigate(`/workflows?agentType=${encodeURIComponent(fromAgentType)}`);
    } else {
      navigate('/workflows');
    }
  };

  const handleStateAccordionChange = (stateId: string) => (_event: React.SyntheticEvent, isExpanded: boolean) => {
    setExpandedState(isExpanded ? stateId : false);
  };

  const handleEditWorkflow = () => {
    // Navigate to edit mode (we'll implement this later)
    navigate(`/workflows/${id}/edit`);
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
          Back to Workflows
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
          {fromAgentType ? `Back to ${fromAgentType} Workflows` : 'Back to Workflows'}
        </Button>
        <Box flexGrow={1}>
          <Box display="flex" alignItems="center" gap={2}>
            <WorkflowIcon color="primary" sx={{ fontSize: 32 }} />
            <Box>
              <Typography variant="h4" gutterBottom>
                {workflow.name}
              </Typography>
              <Box display="flex" gap={1}>
                <Chip
                  label={`v${workflow.version}`}
                  size="small"
                  color="primary"
                  variant="outlined"
                  icon={<VersionIcon />}
                />
                <Chip
                  icon={workflow.status === 'active' ? <ActiveIcon /> : <InactiveIcon />}
                  label={workflow.status === 'active' ? 'Active' : workflow.status}
                  size="small"
                  color={workflow.status === 'active' ? 'success' : 'default'}
                  variant="outlined"
                />
                <Chip
                  label={workflow.definition.agent_type_category}
                  size="small"
                  variant="outlined"
                  color="secondary"
                />
              </Box>
            </Box>
          </Box>
        </Box>
        <EditButton
          onClick={handleEditWorkflow}
          tooltip="Edit Workflow"
          placement="header"
        />
      </Box>

      <Grid container spacing={3}>
        {/* Main Content */}
        <Grid item xs={12} md={8}>
          {/* Workflow Information */}
          <Paper elevation={1} sx={{ p: 3, mb: 3 }}>
            <Typography variant="h6" gutterBottom>
              Workflow Overview
            </Typography>
            
            <Typography variant="body2" color="textSecondary" paragraph>
              {workflow.description || 'No description provided'}
            </Typography>

            <Grid container spacing={2} sx={{ mb: 2 }}>
              <Grid item xs={12} md={4}>
                <Box display="flex" alignItems="center" gap={1}>
                  <StateIcon fontSize="small" color="action" />
                  <Typography variant="body2" color="textSecondary">
                    <strong>States:</strong> {workflow.definition.states.length}
                  </Typography>
                </Box>
              </Grid>
              <Grid item xs={12} md={4}>
                <Box display="flex" alignItems="center" gap={1}>
                  <TimeIcon fontSize="small" color="action" />
                  <Typography variant="body2" color="textSecondary">
                    <strong>Version:</strong> {workflow.definition.workflow_version}
                  </Typography>
                </Box>
              </Grid>
              <Grid item xs={12} md={4}>
                <Typography variant="body2" color="textSecondary">
                  <strong>Created:</strong> {new Date(workflow.created_at).toLocaleDateString()}
                </Typography>
              </Grid>
            </Grid>

            {/* Context Summary */}
            {workflow.definition.context && (
              <Box sx={{ mt: 2 }}>
                <Typography variant="subtitle2" gutterBottom color="secondary">
                  Workflow Context
                </Typography>
                <Grid container spacing={2}>
                  {workflow.definition.context.project_focus && (
                    <Grid item xs={12} md={6}>
                      <Typography variant="body2" color="textSecondary">
                        <strong>Project Focus:</strong> {workflow.definition.context.project_focus}
                      </Typography>
                    </Grid>
                  )}
                  {workflow.definition.context.tech_stack && (
                    <Grid item xs={12} md={6}>
                      <Typography variant="body2" color="textSecondary">
                        <strong>Tech Stack:</strong> {workflow.definition.context.tech_stack.join(', ')}
                      </Typography>
                    </Grid>
                  )}
                </Grid>
              </Box>
            )}

            {/* Success Metrics */}
            {workflow.definition.success_metrics && (
              <Box sx={{ mt: 2 }}>
                <Typography variant="subtitle2" gutterBottom color="primary">
                  Success Metrics
                </Typography>
                <Box display="flex" flexWrap="wrap" gap={0.5}>
                  {workflow.definition.success_metrics.map((metric, index) => (
                    <Chip
                      key={index}
                      label={metric}
                      size="small"
                      variant="outlined"
                      color="success"
                    />
                  ))}
                </Box>
              </Box>
            )}
          </Paper>

          {/* Workflow States */}
          <Paper elevation={1} sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Workflow States ({workflow.definition.states.length})
            </Typography>
            
            <Box sx={{ mt: 2 }}>
              {workflow.definition.states.map((state, index) => (
                <Accordion
                  key={state.id}
                  expanded={expandedState === state.id}
                  onChange={handleStateAccordionChange(state.id)}
                  sx={{ mb: 1 }}
                >
                  <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                    <Box display="flex" alignItems="center" gap={2} width="100%">
                      <Chip
                        label={index + 1}
                        size="small"
                        color="primary"
                        variant="filled"
                      />
                      <Typography variant="subtitle1" fontWeight="medium" sx={{ flexGrow: 1 }}>
                        {state.name}
                      </Typography>
                      <Box display="flex" gap={1}>
                        <Chip
                          label={state.type}
                          size="small"
                          color="info"
                          variant="outlined"
                        />
                        <Chip
                          label={`${state.duration_minutes}min`}
                          size="small"
                          color="default"
                          variant="outlined"
                        />
                        <Chip
                          label={`${state.attention_level}% focus`}
                          size="small"
                          color="warning"
                          variant="outlined"
                        />
                      </Box>
                    </Box>
                  </AccordionSummary>
                  <AccordionDetails>
                    <Grid container spacing={3}>
                      {/* Context Information */}
                      {state.context && (
                        <Grid item xs={12}>
                          <Card variant="outlined" sx={{ mb: 2 }}>
                            <CardContent>
                              <Box display="flex" alignItems="center" gap={1} mb={2}>
                                <ContextIcon fontSize="small" color="secondary" />
                                <Typography variant="subtitle2" color="secondary.main">
                                  State Context
                                </Typography>
                              </Box>
                              <Grid container spacing={2}>
                                {Object.entries(state.context).map(([key, value]) => (
                                  <Grid item xs={12} md={6} key={key}>
                                    <Typography variant="body2" color="textSecondary">
                                      <strong>{key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}:</strong>
                                    </Typography>
                                    <Typography variant="body2">
                                      {Array.isArray(value) ? value.join(', ') : String(value)}
                                    </Typography>
                                  </Grid>
                                ))}
                              </Grid>
                            </CardContent>
                          </Card>
                        </Grid>
                      )}

                      {/* Prompts */}
                      <Grid item xs={12}>
                        <Card variant="outlined">
                          <CardContent>
                            <Box display="flex" alignItems="center" gap={1} mb={2}>
                              <TaskIcon fontSize="small" color="primary" />
                              <Typography variant="subtitle2" color="primary.main">
                                Task Prompts ({state.prompts.length})
                              </Typography>
                            </Box>
                            <List dense>
                              {state.prompts.map((prompt, idx) => (
                                <ListItem key={idx} sx={{ pl: 0 }}>
                                  <ListItemText
                                    primary={`${idx + 1}. ${prompt}`}
                                    primaryTypographyProps={{ variant: 'body2' }}
                                  />
                                </ListItem>
                              ))}
                            </List>
                          </CardContent>
                        </Card>
                      </Grid>

                      {/* Success Criteria */}
                      {state.success_criteria && state.success_criteria.length > 0 && (
                        <Grid item xs={12}>
                          <Card variant="outlined" sx={{ backgroundColor: 'rgba(76, 175, 80, 0.08)' }}>
                            <CardContent>
                              <Typography variant="subtitle2" color="success.main" gutterBottom>
                                Success Criteria
                              </Typography>
                              <List dense>
                                {state.success_criteria.map((criterion, idx) => (
                                  <ListItem key={idx} sx={{ pl: 0 }}>
                                    <ListItemText
                                      primary={`✓ ${criterion}`}
                                      primaryTypographyProps={{ variant: 'body2', color: 'success.main' }}
                                    />
                                  </ListItem>
                                ))}
                              </List>
                            </CardContent>
                          </Card>
                        </Grid>
                      )}
                    </Grid>
                  </AccordionDetails>
                </Accordion>
              ))}
            </Box>
          </Paper>
        </Grid>

        {/* Sidebar */}
        <Grid item xs={12} md={4}>
          {/* Assignment Information */}
          <Paper elevation={1} sx={{ p: 3, mb: 3 }}>
            <Typography variant="h6" gutterBottom>
              Compatibility Details
            </Typography>
            

            {/* Compatible Agents */}
            {assignedAgents.length > 0 && (
              <Box sx={{ mb: 3 }}>
                <Box display="flex" alignItems="center" gap={1} mb={1}>
                  <AgentIcon fontSize="small" color="primary" />
                  <Typography variant="subtitle2" color="primary.main">
                    Compatible Agents ({assignedAgents.length})
                  </Typography>
                </Box>
                {assignedAgents.map((agent, index) => (
                  <Box key={agent.id} sx={{ mb: index < assignedAgents.length - 1 ? 2 : 0 }}>
                    <Typography variant="body2" fontWeight="medium">
                      {agent.name}
                    </Typography>
                    <Typography variant="body2" color="textSecondary">
                      {agent.agent_type?.name || 'Unknown Type'}
                    </Typography>
                    {index < assignedAgents.length - 1 && <Divider sx={{ mt: 1 }} />}
                  </Box>
                ))}
              </Box>
            )}

            {/* Assigned Team */}
            {team && (
              <Box sx={{ mb: 3 }}>
                <Box display="flex" alignItems="center" gap={1} mb={1}>
                  <TeamIcon fontSize="small" color="secondary" />
                  <Typography variant="subtitle2" color="secondary.main">
                    Team Assignment
                  </Typography>
                </Box>
                <Typography variant="body2" fontWeight="medium">
                  {team.name}
                </Typography>
                <Typography variant="body2" color="textSecondary">
                  {team.description}
                </Typography>
              </Box>
            )}

            {/* Project */}
            {project && (
              <Box sx={{ mb: 3 }}>
                <Box display="flex" alignItems="center" gap={1} mb={1}>
                  <ProjectIcon fontSize="small" color="info" />
                  <Typography variant="subtitle2" color="info.main">
                    Project
                  </Typography>
                </Box>
                <Typography variant="body2" fontWeight="medium">
                  {project.name}
                </Typography>
                <Typography variant="body2" color="textSecondary">
                  {project.description}
                </Typography>
              </Box>
            )}
          </Paper>

          {/* Quick Actions */}
          <Paper elevation={1} sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Actions
            </Typography>
            
            <Box display="flex" flexDirection="column" gap={2}>
              <Button
                variant="contained"
                startIcon={<EditIcon />}
                onClick={handleEditWorkflow}
                fullWidth
              >
                Edit Workflow
              </Button>
              
              <Button
                variant="outlined"
                onClick={() => navigate(`/workflows?agentType=${encodeURIComponent(workflow.definition.agent_type_category)}`)}
                fullWidth
              >
                View Similar Workflows
              </Button>
              
              {assignedAgents.length > 0 && (
                <Box>
                  <Typography variant="subtitle2" gutterBottom>
                    View Compatible Agents
                  </Typography>
                  {assignedAgents.map((agent) => (
                    <Button
                      key={agent.id}
                      variant="outlined"
                      onClick={() => navigate(`/agents-list/${agent.id}`)}
                      fullWidth
                      sx={{ mb: 1 }}
                    >
                      {agent.name}
                    </Button>
                  ))}
                </Box>
              )}
            </Box>
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
};

export default AgentWorkflowDetailPage;