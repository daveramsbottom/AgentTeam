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
  LinearProgress,
} from '@mui/material';
import {
  ArrowBack as BackIcon,
  Group as TeamIcon,
  Person as LeaderIcon,
  Groups as MembersIcon,
  Folder as ProjectIcon,
  CheckCircle as ActiveIcon,
  Cancel as InactiveIcon,
  Code as TechIcon,
  Assignment as TaskIcon,
  TrendingUp as PerformanceIcon,
  ExpandMore as ExpandMoreIcon,
  Speed as VelocityIcon,
  Timer as CycleTimeIcon,
  BugReport as DefectIcon,
  Settings as ConfigIcon,
  AccountTree as WorkflowIcon,
  SmartToy as AgentIcon,
} from '@mui/icons-material';
import { Team, teamsApi } from '../api/teams';
import { Project, projectsApi } from '../api/projects';
import { AgentType, agentsApi } from '../api/agents';

const TeamDetailPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [team, setTeam] = useState<Team | null>(null);
  const [project, setProject] = useState<Project | null>(null);
  const [agentTypes, setAgentTypes] = useState<AgentType[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const loadTeamDetails = async () => {
      if (!id) {
        setError('No team ID provided');
        setLoading(false);
        return;
      }
      
      try {
        setLoading(true);
        setError(null);
        console.log('TeamDetailPage - Loading team with ID:', id);
        
        // Load team
        const foundTeam = await teamsApi.getTeam(parseInt(id));
        console.log('TeamDetailPage - Loaded team:', foundTeam);
        setTeam(foundTeam);
        
        // Load associated project
        try {
          const projects = await projectsApi.getProjects();
          const teamProject = projects.find(p => p.id === foundTeam.project_id);
          setProject(teamProject || null);
        } catch (projectError) {
          console.warn('Could not load project:', projectError);
        }
        
        // Load agent types for context
        try {
          const allAgentTypes = await agentsApi.getAgentTypes();
          setAgentTypes(allAgentTypes);
        } catch (agentError) {
          console.warn('Could not load agent types:', agentError);
        }
        
      } catch (error) {
        console.error('Error loading team details:', error);
        setError(`Failed to load team details: ${error instanceof Error ? error.message : 'Unknown error'}`);
      } finally {
        setLoading(false);
      }
    };

    loadTeamDetails();
  }, [id]);

  const handleBack = () => {
    navigate('/teams');
  };

  const getStatusColor = (status: string) => {
    switch (status.toLowerCase()) {
      case 'active': return 'success';
      case 'planning': return 'warning';
      case 'inactive': return 'default';
      default: return 'info';
    }
  };

  const getWorkloadPercentage = () => {
    if (!team || !team.capacity || team.capacity === 0) return 0;
    return Math.min((team.current_workload / team.capacity) * 100, 100);
  };

  const getWorkloadColor = () => {
    const percentage = getWorkloadPercentage();
    if (percentage < 70) return 'success';
    if (percentage < 90) return 'warning';
    return 'error';
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="200px">
        <CircularProgress />
        <Typography variant="body2" sx={{ ml: 2 }}>
          Loading team details... (ID: {id})
        </Typography>
      </Box>
    );
  }

  if (error || !team) {
    console.log('TeamDetailPage - Error state:', { error, team, id, loading });
    return (
      <Box>
        <Button
          startIcon={<BackIcon />}
          onClick={handleBack}
          sx={{ mb: 2 }}
        >
          Back to Teams
        </Button>
        <Alert severity="error">
          {error || `Team not found (ID: ${id})`}
        </Alert>
        <Typography variant="caption" sx={{ mt: 2, display: 'block' }}>
          Debug: loading={String(loading)}, team={team ? 'exists' : 'null'}, error={String(error)}
        </Typography>
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
          Back to Teams
        </Button>
        <Box flexGrow={1}>
          <Box display="flex" alignItems="center" gap={2}>
            <TeamIcon color="primary" sx={{ fontSize: 32 }} />
            <Box>
              <Typography variant="h4" gutterBottom>
                {team.name}
              </Typography>
              <Box display="flex" gap={1}>
                <Chip
                  label={team.status}
                  size="small"
                  color={getStatusColor(team.status) as any}
                  variant="filled"
                />
                {project && (
                  <Chip
                    label={`Project: ${project.name}`}
                    size="small"
                    variant="outlined"
                    icon={<ProjectIcon />}
                  />
                )}
                <Chip
                  label={`${team.member_agent_ids?.length || 0} members`}
                  size="small"
                  variant="outlined"
                  icon={<MembersIcon />}
                />
              </Box>
            </Box>
          </Box>
        </Box>
        <Button
          startIcon={<ConfigIcon />}
          variant="contained"
          color="primary"
        >
          Configure Team
        </Button>
      </Box>

      <Grid container spacing={3}>
        {/* Main Content */}
        <Grid item xs={12} md={8}>
          {/* Team Information */}
          <Paper elevation={1} sx={{ p: 3, mb: 3 }}>
            <Typography variant="h6" gutterBottom>
              Team Information
            </Typography>
            
            <Typography variant="body2" color="textSecondary" paragraph>
              <strong>Description:</strong> {team.description || 'No description provided'}
            </Typography>

            {/* Workload Status */}
            <Box sx={{ mt: 2 }}>
              <Box display="flex" justifyContent="between" alignItems="center" mb={1}>
                <Typography variant="body2" fontWeight="medium">
                  Current Workload
                </Typography>
                <Typography variant="body2" color="textSecondary">
                  {team.current_workload} / {team.capacity} capacity
                </Typography>
              </Box>
              <LinearProgress
                variant="determinate"
                value={getWorkloadPercentage()}
                color={getWorkloadColor() as any}
                sx={{ height: 8, borderRadius: 4 }}
              />
              <Typography variant="caption" color="textSecondary" sx={{ mt: 1, display: 'block' }}>
                {getWorkloadPercentage().toFixed(1)}% capacity utilized
              </Typography>
            </Box>

            <Box sx={{ mt: 2 }}>
              <Typography variant="body2" color="textSecondary">
                <strong>Created:</strong> {new Date(team.created_at).toLocaleDateString()}
              </Typography>
              {team.updated_at && (
                <Typography variant="body2" color="textSecondary">
                  <strong>Last Updated:</strong> {new Date(team.updated_at).toLocaleDateString()}
                </Typography>
              )}
            </Box>
          </Paper>

          {/* Team Context */}
          {team.context && (
            <Paper elevation={1} sx={{ p: 3, mb: 3 }}>
              <Typography variant="h6" gutterBottom>
                Team Context & Configuration
              </Typography>
              
              <Grid container spacing={2}>
                <Grid item xs={12} md={6}>
                  <Card variant="outlined" sx={{ height: '100%' }}>
                    <CardContent>
                      <Typography variant="subtitle2" color="primary" gutterBottom>
                        <TechIcon sx={{ verticalAlign: 'middle', mr: 1 }} />
                        Specialization
                      </Typography>
                      <Typography variant="body2" paragraph>
                        {team.context.specialization || 'No specialization defined'}
                      </Typography>
                      <Typography variant="caption" color="textSecondary" display="block">
                        Team Type: {team.context.team_type ? team.context.team_type.replace(/_/g, ' ').toUpperCase() : 'Not specified'}
                      </Typography>
                      <Typography variant="caption" color="textSecondary">
                        Methodology: {team.context.methodology ? team.context.methodology.toUpperCase() : 'Not specified'}
                      </Typography>
                    </CardContent>
                  </Card>
                </Grid>
                
                <Grid item xs={12} md={6}>
                  <Card variant="outlined" sx={{ height: '100%' }}>
                    <CardContent>
                      <Typography variant="subtitle2" color="primary" gutterBottom>
                        <PerformanceIcon sx={{ verticalAlign: 'middle', mr: 1 }} />
                        Performance Targets
                      </Typography>
                      <Box display="flex" flexDirection="column" gap={1}>
                        {team.context.performance_targets ? (
                          <>
                            <Box display="flex" alignItems="center" gap={1}>
                              <VelocityIcon fontSize="small" />
                              <Typography variant="body2">
                                Velocity: {team.context.performance_targets.velocity || 'N/A'} pts/sprint
                              </Typography>
                            </Box>
                            <Box display="flex" alignItems="center" gap={1}>
                              <CycleTimeIcon fontSize="small" />
                              <Typography variant="body2">
                                Cycle Time: {team.context.performance_targets.cycle_time || 'N/A'} days
                              </Typography>
                            </Box>
                            <Box display="flex" alignItems="center" gap={1}>
                              <DefectIcon fontSize="small" />
                              <Typography variant="body2">
                                Defect Rate: {team.context.performance_targets.defect_rate ? (team.context.performance_targets.defect_rate * 100).toFixed(1) + '%' : 'N/A'}
                              </Typography>
                            </Box>
                          </>
                        ) : (
                          <Typography variant="body2" color="textSecondary">
                            No performance targets defined
                          </Typography>
                        )}
                      </Box>
                    </CardContent>
                  </Card>
                </Grid>

                <Grid item xs={12}>
                  <Accordion>
                    <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                      <Typography variant="subtitle2">
                        Responsibilities & Deliverables
                      </Typography>
                    </AccordionSummary>
                    <AccordionDetails>
                      <Grid container spacing={2}>
                        <Grid item xs={12} md={6}>
                          <Typography variant="body2" fontWeight="medium" gutterBottom>
                            Responsibilities:
                          </Typography>
                          <List dense>
                            {team.context.responsibilities.map((responsibility, index) => (
                              <ListItem key={index} disablePadding>
                                <ListItemIcon>
                                  <TaskIcon fontSize="small" />
                                </ListItemIcon>
                                <ListItemText 
                                  primary={responsibility} 
                                  primaryTypographyProps={{ variant: 'body2' }}
                                />
                              </ListItem>
                            ))}
                          </List>
                        </Grid>
                        <Grid item xs={12} md={6}>
                          <Typography variant="body2" fontWeight="medium" gutterBottom>
                            Deliverables:
                          </Typography>
                          <List dense>
                            {team.context.deliverables.map((deliverable, index) => (
                              <ListItem key={index} disablePadding>
                                <ListItemIcon>
                                  <TaskIcon fontSize="small" />
                                </ListItemIcon>
                                <ListItemText 
                                  primary={deliverable}
                                  primaryTypographyProps={{ variant: 'body2' }}
                                />
                              </ListItem>
                            ))}
                          </List>
                        </Grid>
                      </Grid>
                    </AccordionDetails>
                  </Accordion>

                  <Accordion>
                    <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                      <Typography variant="subtitle2">
                        Technology Stack
                      </Typography>
                    </AccordionSummary>
                    <AccordionDetails>
                      <Grid container spacing={2}>
                        <Grid item xs={12} md={6}>
                          <Typography variant="caption" color="textSecondary" display="block" gutterBottom>
                            Primary Languages:
                          </Typography>
                          <Box display="flex" flexWrap="wrap" gap={0.5} mb={2}>
                            {team.context.technology_stack.primary_languages.map((lang, index) => (
                              <Chip key={index} label={lang} size="small" variant="outlined" color="primary" />
                            ))}
                          </Box>
                          
                          <Typography variant="caption" color="textSecondary" display="block" gutterBottom>
                            Frameworks:
                          </Typography>
                          <Box display="flex" flexWrap="wrap" gap={0.5}>
                            {team.context.technology_stack.frameworks.map((framework, index) => (
                              <Chip key={index} label={framework} size="small" variant="outlined" color="secondary" />
                            ))}
                          </Box>
                        </Grid>
                        <Grid item xs={12} md={6}>
                          <Typography variant="caption" color="textSecondary" display="block" gutterBottom>
                            Tools:
                          </Typography>
                          <Box display="flex" flexWrap="wrap" gap={0.5} mb={2}>
                            {team.context.technology_stack.tools.map((tool, index) => (
                              <Chip key={index} label={tool} size="small" variant="outlined" />
                            ))}
                          </Box>
                          
                          <Typography variant="caption" color="textSecondary" display="block" gutterBottom>
                            Infrastructure:
                          </Typography>
                          <Box display="flex" flexWrap="wrap" gap={0.5}>
                            {team.context.technology_stack.infrastructure.map((infra, index) => (
                              <Chip key={index} label={infra} size="small" variant="outlined" color="info" />
                            ))}
                          </Box>
                        </Grid>
                      </Grid>
                    </AccordionDetails>
                  </Accordion>
                </Grid>
              </Grid>
            </Paper>
          )}

          {/* Team Members */}
          <Paper elevation={1} sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              <MembersIcon sx={{ verticalAlign: 'middle', mr: 1 }} />
              Team Members ({team.member_agent_ids?.length || 0})
            </Typography>
            
            {team.member_agent_ids && team.member_agent_ids.length > 0 ? (
              <Grid container spacing={2}>
                {team.member_agent_ids.map((agentId, index) => (
                  <Grid item xs={12} md={6} key={agentId}>
                    <Card variant="outlined">
                      <CardContent>
                        <Box display="flex" alignItems="center" gap={1} mb={1}>
                          <AgentIcon color="primary" />
                          <Typography variant="subtitle2" fontWeight="medium">
                            Agent {agentId}
                          </Typography>
                          {agentId === team.lead_agent_id && (
                            <Chip 
                              label="Team Lead" 
                              size="small" 
                              color="primary"
                              variant="filled"
                              icon={<LeaderIcon />}
                            />
                          )}
                        </Box>
                        <Typography variant="body2" color="textSecondary" paragraph>
                          Active team member specializing in {team.context?.specialization.toLowerCase()}
                        </Typography>
                        <Box display="flex" justifyContent="between" alignItems="center">
                          <Typography variant="caption" color="textSecondary">
                            Member since: {new Date(team.created_at).toLocaleDateString()}
                          </Typography>
                          <Button
                            size="small"
                            variant="outlined"
                            onClick={() => navigate(`/agents/${agentId}`)}
                          >
                            View Agent
                          </Button>
                        </Box>
                      </CardContent>
                    </Card>
                  </Grid>
                ))}
              </Grid>
            ) : (
              <Alert severity="info">
                No members assigned to this team yet.
              </Alert>
            )}
          </Paper>
        </Grid>

        {/* Sidebar */}
        <Grid item xs={12} md={4}>
          {/* Project Information */}
          {project && (
            <Paper elevation={1} sx={{ p: 3, mb: 3 }}>
              <Typography variant="h6" gutterBottom>
                <ProjectIcon sx={{ verticalAlign: 'middle', mr: 1 }} />
                Project Context
              </Typography>
              
              <Typography variant="subtitle2" fontWeight="medium" gutterBottom>
                {project.name}
              </Typography>
              <Typography variant="body2" color="textSecondary" paragraph>
                {project.description}
              </Typography>
              
              {project.context && (
                <Box sx={{ mt: 2 }}>
                  <Typography variant="caption" color="textSecondary" display="block" gutterBottom>
                    Project Context:
                  </Typography>
                  <Typography variant="body2" sx={{ 
                    fontStyle: 'italic',
                    backgroundColor: 'grey.50',
                    p: 1.5,
                    borderRadius: 1,
                    border: '1px solid',
                    borderColor: 'grey.200'
                  }}>
                    {project.context.length > 200 ? `${project.context.substring(0, 200)}...` : project.context}
                  </Typography>
                </Box>
              )}
              
              <Button
                variant="outlined"
                size="small"
                sx={{ mt: 2 }}
                onClick={() => navigate(`/projects/${project.id}`)}
              >
                View Project Details
              </Button>
            </Paper>
          )}

          {/* Quality Standards */}
          {team.context?.quality_standards && (
            <Paper elevation={1} sx={{ p: 3, mb: 3 }}>
              <Typography variant="h6" gutterBottom>
                Quality Standards
              </Typography>
              
              <Box mb={2}>
                <Typography variant="body2" fontWeight="medium">
                  Code Coverage Threshold
                </Typography>
                <Box display="flex" alignItems="center" gap={1}>
                  <LinearProgress
                    variant="determinate"
                    value={team.context.quality_standards.code_coverage_threshold}
                    sx={{ flexGrow: 1, height: 6, borderRadius: 3 }}
                  />
                  <Typography variant="caption">
                    {team.context.quality_standards.code_coverage_threshold}%
                  </Typography>
                </Box>
              </Box>

              <Box mb={2}>
                <Typography variant="body2" fontWeight="medium" gutterBottom>
                  Testing Requirements:
                </Typography>
                {team.context.quality_standards.testing_requirements.map((req, index) => (
                  <Chip
                    key={index}
                    label={req}
                    size="small"
                    variant="outlined"
                    sx={{ mr: 0.5, mb: 0.5, fontSize: '0.7rem' }}
                  />
                ))}
              </Box>

              <Box>
                <Typography variant="body2" fontWeight="medium" gutterBottom>
                  Review Requirements:
                </Typography>
                {team.context.quality_standards.review_requirements.map((req, index) => (
                  <Chip
                    key={index}
                    label={req}
                    size="small"
                    variant="outlined"
                    color="secondary"
                    sx={{ mr: 0.5, mb: 0.5, fontSize: '0.7rem' }}
                  />
                ))}
              </Box>
            </Paper>
          )}

          {/* Communication Preferences */}
          {team.context?.communication_preferences && (
            <Paper elevation={1} sx={{ p: 3 }}>
              <Typography variant="h6" gutterBottom>
                Communication
              </Typography>
              
              <Box mb={2}>
                <Typography variant="body2" fontWeight="medium" gutterBottom>
                  Meeting Preferences:
                </Typography>
                <List dense>
                  <ListItem disablePadding>
                    <ListItemIcon>
                      {team.context.communication_preferences.daily_standup ? <ActiveIcon color="success" /> : <InactiveIcon color="disabled" />}
                    </ListItemIcon>
                    <ListItemText 
                      primary="Daily Standups" 
                      primaryTypographyProps={{ variant: 'body2' }}
                    />
                  </ListItem>
                  <ListItem disablePadding>
                    <ListItemIcon>
                      {team.context.communication_preferences.sprint_planning ? <ActiveIcon color="success" /> : <InactiveIcon color="disabled" />}
                    </ListItemIcon>
                    <ListItemText 
                      primary="Sprint Planning" 
                      primaryTypographyProps={{ variant: 'body2' }}
                    />
                  </ListItem>
                  <ListItem disablePadding>
                    <ListItemIcon>
                      {team.context.communication_preferences.retrospectives ? <ActiveIcon color="success" /> : <InactiveIcon color="disabled" />}
                    </ListItemIcon>
                    <ListItemText 
                      primary="Retrospectives" 
                      primaryTypographyProps={{ variant: 'body2' }}
                    />
                  </ListItem>
                </List>
              </Box>

              <Box>
                <Typography variant="body2" fontWeight="medium" gutterBottom>
                  Communication Tools:
                </Typography>
                <Box display="flex" flexWrap="wrap" gap={0.5}>
                  {team.context.communication_preferences.tools.map((tool, index) => (
                    <Chip
                      key={index}
                      label={tool}
                      size="small"
                      variant="filled"
                      color="info"
                    />
                  ))}
                </Box>
              </Box>
            </Paper>
          )}
        </Grid>
      </Grid>
    </Box>
  );
};

export default TeamDetailPage;