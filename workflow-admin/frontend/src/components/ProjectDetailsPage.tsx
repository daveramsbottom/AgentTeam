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
  TextField,
  IconButton,
  Tooltip,
} from '@mui/material';
import {
  ArrowBack as BackIcon,
  Folder as ProjectIcon,
  Group as TeamIcon,
  SmartToy as AgentIcon,
  Edit as EditIcon,
  ExpandMore as ExpandMoreIcon,
  Info as InfoIcon,
  Security as SecurityIcon,
  Code as TechIcon,
  Gavel as ComplianceIcon,
  ExpandLess as ExpandLessIcon,
  Circle as StatusIcon,
  AccountTree as WorkflowIcon,
  Launch as LaunchIcon,
  Save as SaveIcon,
  Cancel as CancelIcon,
  EditNote as EditNoteIcon,
} from '@mui/icons-material';
import { Project, projectsApi } from '../api/projects';
import { Team, teamsApi } from '../api/teams';
import { Agent, agentsApi } from '../api/agents';

interface TeamMember {
  id: number;
  name: string;
  role: string;
  status: 'active' | 'idle' | 'busy';
  specialization: string;
  workflow_version?: string;
  workflow_id?: number;
}

interface TeamSummary {
  id: number;
  name: string;
  agent_count: number;
  lead_agent?: string;
  specialization?: string;
  members?: TeamMember[];
}

interface ProjectContext {
  tech_stack?: string[];
  compliance_rules?: string[];
  security_standards?: string[];
  business_guidelines?: string[];
  version?: string;
  last_updated?: string;
}

const ProjectDetailsPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [project, setProject] = useState<Project | null>(null);
  const [teams, setTeams] = useState<TeamSummary[]>([]);
  const [agents, setAgents] = useState<Agent[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [expandedTeams, setExpandedTeams] = useState<Set<number>>(new Set());
  const [isEditMode, setIsEditMode] = useState(false);
  const [editingContext, setEditingContext] = useState(false);
  const [tempContext, setTempContext] = useState('');

  // Get project context from the project's settings field
  const getProjectContext = (): ProjectContext => {
    if (!project?.settings) return {
      tech_stack: [],
      compliance_rules: [],
      security_standards: [],
      business_guidelines: [],
      version: '1.0.0',
      last_updated: new Date().toISOString().split('T')[0],
    };

    const settings = project.settings;
    return {
      tech_stack: settings.tech_stack || [],
      compliance_rules: settings.compliance_rules || ['GDPR compliance', 'Data retention policies'],
      security_standards: settings.security_standards || ['Authentication required', 'Data encryption'],
      business_guidelines: settings.business_guidelines || ['Code review required', 'Testing mandatory'],
      version: settings.version || '1.0.0',
      last_updated: project.updated_at?.split('T')[0] || project.created_at.split('T')[0],
    };
  };

  // Teams are now loaded dynamically from the API based on project_id

  useEffect(() => {
    const loadProject = async () => {
      if (!id) return;
      
      try {
        setLoading(true);
        setError(null);
        
        // Load project, teams, and agents in parallel
        const [projects, allTeams, allAgents] = await Promise.all([
          projectsApi.getProjects(),
          teamsApi.getTeams(),
          agentsApi.getAgents()
        ]);
        
        const foundProject = projects.find(p => p.id === parseInt(id));
        
        if (foundProject) {
          setProject(foundProject);
          setAgents(allAgents);
          
          // Load teams for this specific project
          const projectTeams = allTeams.filter(team => team.project_id === foundProject.id);
          
          // Helper function to get agent by ID
          const getAgentById = (agentId: number): Agent | undefined => 
            allAgents.find(agent => agent.id === agentId);
          
          // Convert Team objects to TeamSummary format for display
          const teamSummaries: TeamSummary[] = projectTeams.map(team => {
            const leadAgent = team.lead_agent_id ? getAgentById(team.lead_agent_id) : undefined;
            
            return {
              id: team.id,
              name: team.name,
              agent_count: team.member_agent_ids?.length || 0,
              lead_agent: leadAgent?.name || 'No lead assigned',
              specialization: team.description || 'General purpose team',
              members: team.member_agent_ids?.map(agentId => {
                const agent = getAgentById(agentId);
                return {
                  id: agentId,
                  name: agent?.name || `Agent ${agentId}`,
                  role: agentId === team.lead_agent_id ? 'Team Lead' : 'Team Member',
                  status: (agent?.status as 'active' | 'idle' | 'busy') || 'active',
                  specialization: agent?.description || 'Multi-agent system development',
                  workflow_version: 'v1.0.0', // TODO: Get from agent workflow mapping
                  workflow_id: 1 // TODO: Get from agent workflow mapping
                };
              }) || [
                // Show lead agent as a member if no member_agent_ids are available but lead exists
                ...(leadAgent ? [{
                  id: leadAgent.id,
                  name: leadAgent.name,
                  role: 'Team Lead',
                  status: (leadAgent.status as 'active' | 'idle' | 'busy') || 'active',
                  specialization: leadAgent.description || 'Team leadership',
                  workflow_version: 'v1.0.0',
                  workflow_id: 1
                }] : [])
              ]
            };
          });
          
          setTeams(teamSummaries);
        } else {
          setError('Project not found');
        }
      } catch (error) {
        console.error('Error loading project:', error);
        setError('Failed to load project details');
      } finally {
        setLoading(false);
      }
    };

    loadProject();
  }, [id]);

  const handleBack = () => {
    navigate('/projects');
  };

  const handleWorkflowNavigation = (workflowId: number, memberName: string, role: string) => {
    navigate(`/workflows/${workflowId}?agent=${encodeURIComponent(memberName)}&role=${encodeURIComponent(role)}&project=${id}`, {
      state: { from: `/projects/${id}` }
    });
  };

  const toggleTeamExpansion = (teamId: number) => {
    setExpandedTeams(prev => {
      const newSet = new Set(prev);
      if (newSet.has(teamId)) {
        newSet.delete(teamId);
      } else {
        newSet.add(teamId);
      }
      return newSet;
    });
  };

  const toggleEditMode = () => {
    if (isEditMode) {
      // Exiting edit mode - cancel any ongoing edits
      setEditingContext(false);
      setTempContext('');
    }
    setIsEditMode(!isEditMode);
  };

  const startEditingContext = () => {
    setEditingContext(true);
    setTempContext(project?.context || '');
  };

  const saveContext = async () => {
    // In real implementation, this would call an API to save the context
    if (project) {
      setProject({ ...project, context: tempContext });
      setEditingContext(false);
      setTempContext('');
      // TODO: Call API to persist changes
      console.log('Saving context:', tempContext);
    }
  };

  const cancelEditingContext = () => {
    setEditingContext(false);
    setTempContext('');
  };

  const getStatusColor = (status: TeamMember['status']) => {
    switch (status) {
      case 'active': return 'success';
      case 'busy': return 'warning';
      case 'idle': return 'info';
      default: return 'default';
    }
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="200px">
        <CircularProgress />
        <Typography variant="body2" sx={{ ml: 2 }}>
          Loading project details...
        </Typography>
      </Box>
    );
  }

  if (error || !project) {
    return (
      <Box>
        <Button
          startIcon={<BackIcon />}
          onClick={handleBack}
          sx={{ mb: 2 }}
        >
          Back to Projects
        </Button>
        <Alert severity="error">
          {error || 'Project not found'}
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
          Back to Projects
        </Button>
        <Box flexGrow={1}>
          <Box display="flex" alignItems="center" gap={2}>
            <ProjectIcon color="primary" sx={{ fontSize: 32 }} />
            <Box>
              <Typography variant="h4" gutterBottom>
                {project.name}
              </Typography>
              <Box display="flex" gap={1}>
                {project.priority && (
                  <Chip
                    label={project.priority}
                    size="small"
                    color={project.priority === 'high' ? 'warning' : 'default'}
                    variant="outlined"
                  />
                )}
                <Chip
                  label={project.status || 'active'}
                  size="small"
                  variant="filled"
                  sx={{ backgroundColor: 'grey.200' }}
                />
              </Box>
            </Box>
          </Box>
        </Box>
        <Button
          startIcon={isEditMode ? <SaveIcon /> : <EditIcon />}
          variant="contained"
          color={isEditMode ? "secondary" : "primary"}
          onClick={toggleEditMode}
          sx={{
            ...(isEditMode && {
              backgroundColor: 'warning.main',
              '&:hover': {
                backgroundColor: 'warning.dark',
              },
            })
          }}
        >
          {isEditMode ? 'Exit Edit Mode' : 'Edit Project'}
        </Button>
      </Box>

      <Grid container spacing={3}>
        {/* Project Information */}
        <Grid item xs={12} md={8}>
          <Paper 
            elevation={1} 
            sx={{ 
              p: 3, 
              mb: 3,
              ...(isEditMode && {
                border: '2px solid',
                borderColor: 'warning.main',
                backgroundColor: 'warning.light',
                backgroundImage: 'linear-gradient(45deg, transparent 25%, rgba(255,255,255,0.1) 25%)',
              })
            }}
          >
            <Box display="flex" alignItems="center" justifyContent="between" mb={2}>
              <Typography variant="h6">
                Project Information
              </Typography>
              {isEditMode && (
                <Chip 
                  label="✏️ Edit Mode Active" 
                  size="small" 
                  color="warning" 
                  variant="filled" 
                  sx={{ ml: 2 }}
                />
              )}
            </Box>
            
            <Typography variant="body2" color="textSecondary" paragraph>
              <strong>Description:</strong> {project.description || 'No description provided'}
            </Typography>
            
            {(project.context || isEditMode) && (
              <Box sx={{ mt: 2 }}>
                <Box display="flex" alignItems="center" gap={1} mb={1}>
                  <Typography variant="body2" fontWeight="bold" color="text.primary">
                    Project Context:
                  </Typography>
                  {isEditMode && !editingContext && (
                    <Tooltip title="Edit project context">
                      <IconButton 
                        size="small" 
                        onClick={startEditingContext}
                        sx={{ 
                          color: 'warning.main',
                          '&:hover': { backgroundColor: 'warning.light' }
                        }}
                      >
                        <EditNoteIcon fontSize="small" />
                      </IconButton>
                    </Tooltip>
                  )}
                </Box>
                
                {editingContext ? (
                  <Box sx={{ mt: 1 }}>
                    <TextField
                      fullWidth
                      multiline
                      rows={4}
                      value={tempContext}
                      onChange={(e) => setTempContext(e.target.value)}
                      placeholder="Enter project context description..."
                      variant="outlined"
                      sx={{ 
                        mb: 1,
                        '& .MuiOutlinedInput-root': {
                          backgroundColor: 'background.paper'
                        }
                      }}
                    />
                    <Box display="flex" gap={1}>
                      <Button
                        startIcon={<SaveIcon />}
                        variant="contained"
                        size="small"
                        color="success"
                        onClick={saveContext}
                      >
                        Save
                      </Button>
                      <Button
                        startIcon={<CancelIcon />}
                        variant="outlined"
                        size="small"
                        onClick={cancelEditingContext}
                      >
                        Cancel
                      </Button>
                    </Box>
                  </Box>
                ) : (
                  <Typography variant="body2" color="text.primary" sx={{ 
                    fontStyle: 'italic', 
                    backgroundColor: project.context ? 'grey.50' : 'grey.100', 
                    p: 2, 
                    borderRadius: 1,
                    border: '1px solid',
                    borderColor: project.context ? 'grey.200' : 'grey.300',
                    ...(isEditMode && {
                      backgroundColor: 'warning.light',
                      borderColor: 'warning.main',
                    })
                  }}>
                    {project.context || 'No project context set. Click the edit icon to add context.'}
                  </Typography>
                )}
              </Box>
            )}

            <Box sx={{ mt: 2 }}>
              <Typography variant="body2" color="textSecondary">
                <strong>Created:</strong> {new Date(project.created_at).toLocaleDateString()}
              </Typography>
              {project.updated_at && (
                <Typography variant="body2" color="textSecondary">
                  <strong>Last Updated:</strong> {new Date(project.updated_at).toLocaleDateString()}
                </Typography>
              )}
            </Box>
          </Paper>

          {/* Teams */}
          <Paper elevation={1} sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Project Teams ({teams.length})
            </Typography>
            
            {teams.length === 0 ? (
              <Alert severity="info">
                No teams assigned to this project yet.
              </Alert>
            ) : (
              <Grid container spacing={2}>
                {teams.map((team) => (
                  <Grid item xs={12} key={team.id}>
                    <Card variant="outlined">
                      <CardContent>
                        <Box 
                          display="flex" 
                          alignItems="center" 
                          justifyContent="space-between" 
                          mb={1}
                          sx={{ cursor: 'pointer' }}
                          onClick={() => toggleTeamExpansion(team.id)}
                        >
                          <Box display="flex" alignItems="center" gap={1}>
                            <TeamIcon color="primary" />
                            <Typography variant="subtitle1" fontWeight="medium">
                              {team.name}
                            </Typography>
                          </Box>
                          <Button size="small" endIcon={expandedTeams.has(team.id) ? <ExpandLessIcon /> : <ExpandMoreIcon />}>
                            {expandedTeams.has(team.id) ? 'Hide Members' : 'Show Members'}
                          </Button>
                        </Box>
                        
                        <Typography variant="body2" color="textSecondary" paragraph>
                          {team.specialization}
                        </Typography>
                        
                        <Box display="flex" justifyContent="space-between" alignItems="center" mb={expandedTeams.has(team.id) ? 2 : 0}>
                          <Typography variant="caption" color="textSecondary">
                            <AgentIcon fontSize="small" sx={{ verticalAlign: 'middle', mr: 0.5 }} />
                            {team.agent_count} agents
                          </Typography>
                          <Typography variant="caption" color="textSecondary">
                            Lead: {team.lead_agent}
                          </Typography>
                        </Box>

                        {expandedTeams.has(team.id) && team.members && (
                          <Box>
                            <Divider sx={{ mb: 2 }} />
                            <Typography variant="subtitle2" gutterBottom color="primary">
                              Team Members
                            </Typography>
                            <List dense>
                              {team.members.map((member) => (
                                <ListItem key={member.id} disablePadding>
                                  <ListItemIcon>
                                    <StatusIcon 
                                      fontSize="small" 
                                      color={getStatusColor(member.status) as any}
                                    />
                                  </ListItemIcon>
                                  <ListItemText
                                    primary={
                                      <Box display="flex" alignItems="center" gap={1}>
                                        <Typography variant="body2" fontWeight="medium">
                                          {member.name}
                                        </Typography>
                                        <Chip 
                                          label={member.role} 
                                          size="small" 
                                          variant="outlined"
                                          sx={{ fontSize: '0.7rem' }}
                                        />
                                        <Chip 
                                          label={member.status} 
                                          size="small" 
                                          color={getStatusColor(member.status) as any}
                                          sx={{ fontSize: '0.7rem' }}
                                        />
                                      </Box>
                                    }
                                    secondary={
                                      <Box>
                                        <Typography variant="body2" color="textSecondary" sx={{ mb: 0.5 }}>
                                          {member.specialization}
                                        </Typography>
                                        {member.workflow_version && member.workflow_id && (
                                          <Box 
                                            display="flex" 
                                            alignItems="center" 
                                            gap={1}
                                            sx={{
                                              cursor: 'pointer',
                                              padding: '4px 8px',
                                              borderRadius: 1,
                                              backgroundColor: 'action.hover',
                                              '&:hover': {
                                                backgroundColor: 'primary.light',
                                                '& .workflow-text': { color: 'primary.contrastText' }
                                              },
                                              transition: 'all 0.2s ease'
                                            }}
                                            onClick={(e) => {
                                              e.stopPropagation();
                                              handleWorkflowNavigation(member.workflow_id!, member.name, member.role);
                                            }}
                                          >
                                            <WorkflowIcon fontSize="small" color="primary" />
                                            <Typography 
                                              variant="caption" 
                                              className="workflow-text"
                                              sx={{ fontWeight: 'medium' }}
                                            >
                                              Workflow {member.workflow_version}
                                            </Typography>
                                            <LaunchIcon fontSize="small" color="action" />
                                          </Box>
                                        )}
                                      </Box>
                                    }
                                  />
                                </ListItem>
                              ))}
                            </List>
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

        {/* Sidebar - Project Context Guidelines */}
        <Grid item xs={12} md={4}>
          <Paper elevation={1} sx={{ p: 3 }}>
            <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
              <Box>
                <Typography variant="h6" gutterBottom>
                  Project Guidelines
                </Typography>
                <Typography variant="body2" color="textSecondary">
                  Context and standards that inform all team members
                </Typography>
              </Box>
              <Box textAlign="right">
                <Chip 
                  label={`Version ${getProjectContext().version}`} 
                  size="small" 
                  color="primary" 
                  variant="outlined"
                />
                <Typography variant="caption" color="textSecondary" sx={{ display: 'block', mt: 0.5 }}>
                  Updated: {new Date(getProjectContext().last_updated || '').toLocaleDateString()}
                </Typography>
              </Box>
            </Box>

            <Box>
              {/* Tech Stack */}
              <Accordion defaultExpanded>
                <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                  <Box display="flex" alignItems="center" gap={1}>
                    <TechIcon color="primary" fontSize="small" />
                    <Typography variant="subtitle2">Tech Stack</Typography>
                  </Box>
                </AccordionSummary>
                <AccordionDetails>
                  <List dense>
                    {getProjectContext().tech_stack?.map((tech, index) => (
                      <ListItem key={index} disablePadding>
                        <ListItemText 
                          primary={
                            <Typography variant="body2">{tech}</Typography>
                          }
                        />
                      </ListItem>
                    ))}
                  </List>
                </AccordionDetails>
              </Accordion>

              {/* Security Standards */}
              <Accordion>
                <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                  <Box display="flex" alignItems="center" gap={1}>
                    <SecurityIcon color="error" fontSize="small" />
                    <Typography variant="subtitle2">Security Standards</Typography>
                  </Box>
                </AccordionSummary>
                <AccordionDetails>
                  <List dense>
                    {getProjectContext().security_standards?.map((standard, index) => (
                      <ListItem key={index} disablePadding>
                        <ListItemText 
                          primary={
                            <Typography variant="body2">{standard}</Typography>
                          }
                        />
                      </ListItem>
                    ))}
                  </List>
                </AccordionDetails>
              </Accordion>

              {/* Compliance Rules */}
              <Accordion>
                <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                  <Box display="flex" alignItems="center" gap={1}>
                    <ComplianceIcon color="info" fontSize="small" />
                    <Typography variant="subtitle2">Compliance</Typography>
                  </Box>
                </AccordionSummary>
                <AccordionDetails>
                  <List dense>
                    {getProjectContext().compliance_rules?.map((rule, index) => (
                      <ListItem key={index} disablePadding>
                        <ListItemText 
                          primary={
                            <Typography variant="body2">{rule}</Typography>
                          }
                        />
                      </ListItem>
                    ))}
                  </List>
                </AccordionDetails>
              </Accordion>

              {/* Business Guidelines */}
              <Accordion>
                <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                  <Box display="flex" alignItems="center" gap={1}>
                    <InfoIcon color="warning" fontSize="small" />
                    <Typography variant="subtitle2">Business Guidelines</Typography>
                  </Box>
                </AccordionSummary>
                <AccordionDetails>
                  <List dense>
                    {getProjectContext().business_guidelines?.map((guideline, index) => (
                      <ListItem key={index} disablePadding>
                        <ListItemText 
                          primary={
                            <Typography variant="body2">{guideline}</Typography>
                          }
                        />
                      </ListItem>
                    ))}
                  </List>
                </AccordionDetails>
              </Accordion>
            </Box>
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
};

export default ProjectDetailsPage;