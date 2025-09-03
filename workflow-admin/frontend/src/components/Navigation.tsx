import React, { useState, useEffect } from 'react';
import { useLocation, Link } from 'react-router-dom';
import {
  Drawer,
  List,
  ListItem,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  Toolbar,
  Box,
  Typography,
  Collapse,
  Divider,
} from '@mui/material';
import {
  Home as HomeIcon,
  Folder as ProjectsIcon,
  SmartToy as AgentsIcon,
  Group as TeamsIcon,
  AccountTree as WorkflowsIcon,
  Settings as SettingsIcon,
  Build as ConfigIcon,
  ExpandLess as ExpandLessIcon,
  ExpandMore as ExpandMoreIcon,
  FolderOpen as OpenProjectIcon,
} from '@mui/icons-material';
import { Project, projectsApi } from '../api/projects';
import { AgentType, Agent, agentsApi } from '../api/agents';
import { Team, teamsApi } from '../api/teams';

const drawerWidth = 240;

interface NavigationItem {
  path: string;
  label: string;
  icon: React.ReactElement;
}

interface NavigationSection {
  title: string;
  items: NavigationItem[];
}

const navigationSections: NavigationSection[] = [
  {
    title: 'Operations',
    items: [
      { path: '/', label: 'Home', icon: <HomeIcon /> },
    ],
  },
  {
    title: 'Configuration',
    items: [
      { path: '/workflows', label: 'Workflows', icon: <WorkflowsIcon /> },
    ],
  },
];

const Navigation: React.FC = () => {
  const location = useLocation();
  const [projectsOpen, setProjectsOpen] = useState(false);
  const [projects, setProjects] = useState<Project[]>([]);
  const [loadingProjects, setLoadingProjects] = useState(false);
  const [agentTypesOpen, setAgentTypesOpen] = useState(false);
  const [agentTypes, setAgentTypes] = useState<AgentType[]>([]);
  const [loadingAgentTypes, setLoadingAgentTypes] = useState(false);
  const [teamsOpen, setTeamsOpen] = useState(false);
  const [teams, setTeams] = useState<Team[]>([]);
  const [loadingTeams, setLoadingTeams] = useState(false);
  const [agentsOpen, setAgentsOpen] = useState(false);
  const [agents, setAgents] = useState<Agent[]>([]);
  const [loadingAgents, setLoadingAgents] = useState(false);

  const toggleProjects = async () => {
    if (!projectsOpen && projects.length === 0 && !loadingProjects) {
      // Load projects when first expanding
      setLoadingProjects(true);
      try {
        const projectData = await projectsApi.getProjects();
        setProjects(projectData);
      } catch (error) {
        console.error('Error loading projects:', error);
      } finally {
        setLoadingProjects(false);
      }
    }
    setProjectsOpen(!projectsOpen);
  };

  const toggleAgentTypes = async () => {
    if (!agentTypesOpen && agentTypes.length === 0 && !loadingAgentTypes) {
      // Load agent types when first expanding
      setLoadingAgentTypes(true);
      try {
        const agentTypeData = await agentsApi.getAgentTypes();
        setAgentTypes(agentTypeData);
      } catch (error) {
        console.error('Error loading agent types:', error);
      } finally {
        setLoadingAgentTypes(false);
      }
    }
    setAgentTypesOpen(!agentTypesOpen);
  };

  const toggleTeams = async () => {
    if (!teamsOpen && teams.length === 0 && !loadingTeams) {
      // Load teams when first expanding
      setLoadingTeams(true);
      try {
        const teamData = await teamsApi.getTeams();
        setTeams(teamData);
      } catch (error) {
        console.error('Error loading teams:', error);
      } finally {
        setLoadingTeams(false);
      }
    }
    setTeamsOpen(!teamsOpen);
  };

  const toggleAgents = async () => {
    if (!agentsOpen && agents.length === 0 && !loadingAgents) {
      // Load agents when first expanding
      setLoadingAgents(true);
      try {
        const agentData = await agentsApi.getAgents();
        setAgents(agentData);
      } catch (error) {
        console.error('Error loading agents:', error);
      } finally {
        setLoadingAgents(false);
      }
    }
    setAgentsOpen(!agentsOpen);
  };

  return (
    <Drawer
      variant="permanent"
      sx={{
        width: drawerWidth,
        flexShrink: 0,
        '& .MuiDrawer-paper': {
          width: drawerWidth,
          boxSizing: 'border-box',
        },
      }}
    >
      <Toolbar>
        <Box display="flex" alignItems="center" gap={1}>
          <ProjectsIcon color="primary" />
          <Typography variant="h6" component="div">
            Workflow Admin
          </Typography>
        </Box>
      </Toolbar>
      
      <Box sx={{ overflow: 'auto' }}>
        {navigationSections.map((section, sectionIndex) => (
          <Box key={section.title}>
            <Typography 
              variant="overline" 
              sx={{ 
                px: 2, 
                py: 1, 
                display: 'block',
                color: 'text.secondary',
                fontSize: '0.75rem',
                fontWeight: 'medium',
                letterSpacing: '0.1em'
              }}
            >
              {section.title}
            </Typography>
            <List dense sx={{ pt: 0 }}>
              {section.items.map((item) => (
                <ListItem key={item.path} disablePadding>
                  <ListItemButton
                    component={Link}
                    to={item.path}
                    selected={location.pathname === item.path}
                    sx={{
                      '&.Mui-selected': {
                        backgroundColor: 'primary.light',
                        color: 'primary.contrastText',
                        '&:hover': {
                          backgroundColor: 'primary.main',
                        },
                        '& .MuiListItemIcon-root': {
                          color: 'primary.contrastText',
                        },
                      },
                    }}
                  >
                    <ListItemIcon>
                      {item.icon}
                    </ListItemIcon>
                    <ListItemText primary={item.label} />
                  </ListItemButton>
                </ListItem>
              ))}
              
              {/* Agent Types dropdown - add at start of Configuration section */}
              {section.title === 'Configuration' && (
                <>
                  <ListItem disablePadding>
                    <ListItemButton 
                      onClick={toggleAgentTypes}
                      selected={location.pathname.startsWith('/agents')}
                      sx={{
                        '&.Mui-selected': {
                          backgroundColor: 'primary.light',
                          color: 'primary.contrastText',
                          '&:hover': {
                            backgroundColor: 'primary.main',
                          },
                          '& .MuiListItemIcon-root': {
                            color: 'primary.contrastText',
                          },
                        },
                      }}
                    >
                      <ListItemIcon>
                        <AgentsIcon />
                      </ListItemIcon>
                      <ListItemText primary="Agent Types" />
                      {loadingAgentTypes ? (
                        <Box sx={{ width: 16, height: 16, mx: 1 }}>
                          <Typography variant="caption">...</Typography>
                        </Box>
                      ) : (
                        agentTypesOpen ? <ExpandLessIcon /> : <ExpandMoreIcon />
                      )}
                    </ListItemButton>
                  </ListItem>
                  
                  <Collapse in={agentTypesOpen} timeout="auto" unmountOnExit>
                    <List dense sx={{ pl: 2 }}>
                      <ListItem disablePadding>
                        <ListItemButton
                          component={Link}
                          to="/agents"
                          selected={location.pathname === '/agents'}
                          sx={{
                            '&.Mui-selected': {
                              backgroundColor: 'primary.light',
                              color: 'primary.contrastText',
                            },
                          }}
                        >
                          <ListItemIcon>
                            <AgentsIcon fontSize="small" />
                          </ListItemIcon>
                          <ListItemText 
                            primary="All Agent Types" 
                            primaryTypographyProps={{ variant: 'body2' }}
                          />
                        </ListItemButton>
                      </ListItem>
                      <Divider sx={{ my: 0.5 }} />
                      {agentTypes.map((agentType) => (
                        <ListItem key={agentType.id} disablePadding>
                          <ListItemButton
                            component={Link}
                            to={`/agents/${agentType.id}`}
                            selected={location.pathname === `/agents/${agentType.id}`}
                            sx={{
                              '&.Mui-selected': {
                                backgroundColor: 'primary.light',
                                color: 'primary.contrastText',
                              },
                            }}
                          >
                            <ListItemIcon>
                              <AgentsIcon fontSize="small" />
                            </ListItemIcon>
                            <ListItemText 
                              primary={agentType.name}
                              primaryTypographyProps={{ 
                                variant: 'body2',
                                sx: { 
                                  overflow: 'hidden', 
                                  textOverflow: 'ellipsis',
                                  whiteSpace: 'nowrap'
                                }
                              }}
                            />
                          </ListItemButton>
                        </ListItem>
                      ))}
                    </List>
                  </Collapse>
                  
                  {/* Teams dropdown - add after Agent Types */}
                  <ListItem disablePadding>
                    <ListItemButton 
                      onClick={toggleTeams}
                      selected={location.pathname.startsWith('/teams')}
                      sx={{
                        '&.Mui-selected': {
                          backgroundColor: 'primary.light',
                          color: 'primary.contrastText',
                          '&:hover': {
                            backgroundColor: 'primary.main',
                          },
                          '& .MuiListItemIcon-root': {
                            color: 'primary.contrastText',
                          },
                        },
                      }}
                    >
                      <ListItemIcon>
                        <TeamsIcon />
                      </ListItemIcon>
                      <ListItemText primary="Teams" />
                      {loadingTeams ? (
                        <Box sx={{ width: 16, height: 16, mx: 1 }}>
                          <Typography variant="caption">...</Typography>
                        </Box>
                      ) : (
                        teamsOpen ? <ExpandLessIcon /> : <ExpandMoreIcon />
                      )}
                    </ListItemButton>
                  </ListItem>
                  
                  <Collapse in={teamsOpen} timeout="auto" unmountOnExit>
                    <List dense sx={{ pl: 2 }}>
                      <ListItem disablePadding>
                        <ListItemButton
                          component={Link}
                          to="/teams"
                          selected={location.pathname === '/teams'}
                          sx={{
                            '&.Mui-selected': {
                              backgroundColor: 'primary.light',
                              color: 'primary.contrastText',
                            },
                          }}
                        >
                          <ListItemIcon>
                            <TeamsIcon fontSize="small" />
                          </ListItemIcon>
                          <ListItemText 
                            primary="All Teams" 
                            primaryTypographyProps={{ variant: 'body2' }}
                          />
                        </ListItemButton>
                      </ListItem>
                      <Divider sx={{ my: 0.5 }} />
                      {teams.map((team) => (
                        <ListItem key={team.id} disablePadding>
                          <ListItemButton
                            component={Link}
                            to={`/teams/${team.id}`}
                            selected={location.pathname === `/teams/${team.id}`}
                            sx={{
                              '&.Mui-selected': {
                                backgroundColor: 'primary.light',
                                color: 'primary.contrastText',
                              },
                            }}
                          >
                            <ListItemIcon>
                              <TeamsIcon fontSize="small" />
                            </ListItemIcon>
                            <ListItemText 
                              primary={team.name}
                              secondary={`Project: ${team.project_id}`}
                              primaryTypographyProps={{ 
                                variant: 'body2',
                                sx: { 
                                  overflow: 'hidden', 
                                  textOverflow: 'ellipsis',
                                  whiteSpace: 'nowrap'
                                }
                              }}
                              secondaryTypographyProps={{
                                variant: 'caption',
                                sx: { fontSize: '0.6rem' }
                              }}
                            />
                          </ListItemButton>
                        </ListItem>
                      ))}
                    </List>
                  </Collapse>
                  
                  {/* Individual Agents dropdown - add after Teams */}
                  <ListItem disablePadding>
                    <ListItemButton 
                      onClick={toggleAgents}
                      selected={location.pathname.startsWith('/agents-list')}
                      sx={{
                        '&.Mui-selected': {
                          backgroundColor: 'primary.light',
                          color: 'primary.contrastText',
                          '&:hover': {
                            backgroundColor: 'primary.main',
                          },
                          '& .MuiListItemIcon-root': {
                            color: 'primary.contrastText',
                          },
                        },
                      }}
                    >
                      <ListItemIcon>
                        <AgentsIcon />
                      </ListItemIcon>
                      <ListItemText primary="Agents" />
                      {loadingAgents ? (
                        <Box sx={{ width: 16, height: 16, mx: 1 }}>
                          <Typography variant="caption">...</Typography>
                        </Box>
                      ) : (
                        agentsOpen ? <ExpandLessIcon /> : <ExpandMoreIcon />
                      )}
                    </ListItemButton>
                  </ListItem>
                  
                  <Collapse in={agentsOpen} timeout="auto" unmountOnExit>
                    <List dense sx={{ pl: 2 }}>
                      <ListItem disablePadding>
                        <ListItemButton
                          component={Link}
                          to="/agents-list"
                          selected={location.pathname === '/agents-list'}
                          sx={{
                            '&.Mui-selected': {
                              backgroundColor: 'primary.light',
                              color: 'primary.contrastText',
                            },
                          }}
                        >
                          <ListItemIcon>
                            <AgentsIcon fontSize="small" />
                          </ListItemIcon>
                          <ListItemText 
                            primary="All Agents" 
                            primaryTypographyProps={{ variant: 'body2' }}
                          />
                        </ListItemButton>
                      </ListItem>
                      <Divider sx={{ my: 0.5 }} />
                      {agents.map((agent) => (
                        <ListItem key={agent.id} disablePadding>
                          <ListItemButton
                            component={Link}
                            to={`/agents-list/${agent.id}`}
                            selected={location.pathname === `/agents-list/${agent.id}`}
                            sx={{
                              '&.Mui-selected': {
                                backgroundColor: 'primary.light',
                                color: 'primary.contrastText',
                              },
                            }}
                          >
                            <ListItemIcon>
                              <AgentsIcon fontSize="small" />
                            </ListItemIcon>
                            <ListItemText 
                              primary={agent.name}
                              secondary={agent.agent_type?.name || 'Unknown Type'}
                              primaryTypographyProps={{ 
                                variant: 'body2',
                                sx: { 
                                  overflow: 'hidden', 
                                  textOverflow: 'ellipsis',
                                  whiteSpace: 'nowrap'
                                }
                              }}
                              secondaryTypographyProps={{
                                variant: 'caption',
                                sx: { fontSize: '0.6rem' }
                              }}
                            />
                          </ListItemButton>
                        </ListItem>
                      ))}
                    </List>
                  </Collapse>
                </>
              )}

              {/* Projects dropdown - add after Home in Operations section */}
              {section.title === 'Operations' && (
                <>
                  <ListItem disablePadding>
                    <ListItemButton 
                      onClick={toggleProjects}
                      selected={location.pathname.startsWith('/projects')}
                      sx={{
                        '&.Mui-selected': {
                          backgroundColor: 'primary.light',
                          color: 'primary.contrastText',
                          '&:hover': {
                            backgroundColor: 'primary.main',
                          },
                          '& .MuiListItemIcon-root': {
                            color: 'primary.contrastText',
                          },
                        },
                      }}
                    >
                      <ListItemIcon>
                        <ProjectsIcon />
                      </ListItemIcon>
                      <ListItemText primary="Projects" />
                      {loadingProjects ? (
                        <Box sx={{ width: 16, height: 16, mx: 1 }}>
                          <Typography variant="caption">...</Typography>
                        </Box>
                      ) : (
                        projectsOpen ? <ExpandLessIcon /> : <ExpandMoreIcon />
                      )}
                    </ListItemButton>
                  </ListItem>
                  
                  <Collapse in={projectsOpen} timeout="auto" unmountOnExit>
                    <List dense sx={{ pl: 2 }}>
                      <ListItem disablePadding>
                        <ListItemButton
                          component={Link}
                          to="/projects"
                          selected={location.pathname === '/projects'}
                          sx={{
                            '&.Mui-selected': {
                              backgroundColor: 'primary.light',
                              color: 'primary.contrastText',
                            },
                          }}
                        >
                          <ListItemIcon>
                            <ProjectsIcon fontSize="small" />
                          </ListItemIcon>
                          <ListItemText 
                            primary="All Projects" 
                            primaryTypographyProps={{ variant: 'body2' }}
                          />
                        </ListItemButton>
                      </ListItem>
                      <Divider sx={{ my: 0.5 }} />
                      {projects.map((project) => (
                        <ListItem key={project.id} disablePadding>
                          <ListItemButton
                            component={Link}
                            to={`/projects/${project.id}`}
                            selected={location.pathname === `/projects/${project.id}`}
                            sx={{
                              '&.Mui-selected': {
                                backgroundColor: 'primary.light',
                                color: 'primary.contrastText',
                              },
                            }}
                          >
                            <ListItemIcon>
                              <OpenProjectIcon fontSize="small" />
                            </ListItemIcon>
                            <ListItemText 
                              primary={project.name}
                              primaryTypographyProps={{ 
                                variant: 'body2',
                                sx: { 
                                  overflow: 'hidden', 
                                  textOverflow: 'ellipsis',
                                  whiteSpace: 'nowrap'
                                }
                              }}
                            />
                          </ListItemButton>
                        </ListItem>
                      ))}
                    </List>
                  </Collapse>
                </>
              )}
            </List>
          </Box>
        ))}
      </Box>
    </Drawer>
  );
};

export default Navigation;