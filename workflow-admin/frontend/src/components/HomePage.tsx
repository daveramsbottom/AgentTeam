import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Paper,
  Grid,
  Card,
  CardContent,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Chip,
  Alert,
  CircularProgress,
} from '@mui/material';
import {
  Dashboard as HomeIcon,
  CheckCircle as CompletedIcon,
  RadioButtonUnchecked as PendingIcon,
  Info as InfoIcon,
  Storage as DatabaseIcon,
  CloudOff as OfflineIcon,
} from '@mui/icons-material';
import { APP_VERSION, getBackendVersion } from '../utils/version';
import { checkDataSourceHealth, HealthCheckResult } from '../utils/health';
import { projectsApi, Project } from '../api/projects';
import { agentsApi, Agent } from '../api/agents';
import { teamsApi, Team } from '../api/teams';


const HomePage: React.FC = () => {
  const [backendVersion, setBackendVersion] = useState<{ version: string; buildDate?: string } | null>(null);
  const [healthStatus, setHealthStatus] = useState<HealthCheckResult | null>(null);
  const [projects, setProjects] = useState<Project[]>([]);
  const [agents, setAgents] = useState<Agent[]>([]);
  const [teams, setTeams] = useState<Team[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchSystemInfo = async () => {
      try {
        const [version, health, projectsData, agentsData, teamsData] = await Promise.all([
          getBackendVersion().catch(() => null),
          checkDataSourceHealth(),
          projectsApi.getProjects().catch(() => []),
          agentsApi.getAgents().catch(() => []),
          teamsApi.getTeams().catch(() => [])
        ]);
        setBackendVersion(version);
        setHealthStatus(health);
        setProjects(projectsData);
        setAgents(agentsData);
        setTeams(teamsData);
      } catch (error) {
        console.error('Failed to fetch system info:', error);
      } finally {
        setLoading(false);
      }
    };
    fetchSystemInfo();
  }, []);

  const getActiveAgentsCount = () => {
    return agents.filter(agent => agent.status === 'active').length;
  };

  const getAverageWorkload = () => {
    if (agents.length === 0) return 0;
    const totalWorkload = agents.reduce((sum, agent) => sum + (agent.current_workload || 0), 0);
    const totalCapacity = agents.reduce((sum, agent) => sum + (agent.workload_capacity || 100), 0);
    return Math.round((totalWorkload / totalCapacity) * 100);
  };

  const getActiveTeamsCount = () => {
    return teams.filter(team => team.is_active).length;
  };


  return (
    <Box>
      <Box display="flex" alignItems="center" gap={2} mb={3}>
        <HomeIcon color="primary" sx={{ fontSize: 32 }} />
        <Box>
          <Typography variant="h4" gutterBottom>
            Workflow Admin Portal
          </Typography>
          <Typography variant="body1" color="textSecondary">
            Multi-Agent Workflow Management System
          </Typography>
        </Box>
      </Box>

      <Grid container spacing={3}>
        {/* Version Information */}
        <Grid item xs={12} md={6}>
          <Paper elevation={1} sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              System Information
            </Typography>
            {loading ? (
              <Box display="flex" alignItems="center" gap={2}>
                <CircularProgress size={20} />
                <Typography variant="body2">Loading version info...</Typography>
              </Box>
            ) : (
              <Box>
                <Typography variant="body2" color="textSecondary" gutterBottom>
                  Frontend: v{APP_VERSION}
                </Typography>
                <Typography variant="body2" color="textSecondary" gutterBottom>
                  Backend: {backendVersion ? `v${backendVersion.version}` : 'Unknown'}
                  {backendVersion?.buildDate && ` (${backendVersion.buildDate})`}
                </Typography>
                
                {/* Data Source Status */}
                <Box display="flex" alignItems="center" gap={1} mt={1} mb={1}>
                  {healthStatus?.isApiAvailable ? (
                    <DatabaseIcon color="success" fontSize="small" />
                  ) : (
                    <OfflineIcon color="warning" fontSize="small" />
                  )}
                  <Typography variant="body2" color="textSecondary">
                    Data Source: 
                    <Chip 
                      label={
                        healthStatus?.dataSource === 'database' ? 'Database' : 
                        healthStatus?.dataSource === 'mock' ? 'Mock Data' : 'Unknown'
                      }
                      color={
                        healthStatus?.dataSource === 'database' ? 'success' : 
                        healthStatus?.dataSource === 'mock' ? 'warning' : 'default'
                      }
                      size="small" 
                      sx={{ ml: 1 }}
                    />
                  </Typography>
                </Box>

                {healthStatus?.apiResponseTime && (
                  <Typography variant="body2" color="textSecondary" gutterBottom>
                    API Response: {healthStatus.apiResponseTime}ms
                  </Typography>
                )}

                {healthStatus?.error && (
                  <Typography variant="body2" color="error" gutterBottom>
                    Connection: {healthStatus.error}
                  </Typography>
                )}
                
                <Typography variant="body2" color="textSecondary">
                  Status: <Chip label="Running" color="success" size="small" />
                </Typography>
              </Box>
            )}
          </Paper>
        </Grid>

        {/* System Overview */}
        <Grid item xs={12} md={6}>
          <Paper elevation={1} sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              System Overview
            </Typography>
            {loading ? (
              <Box display="flex" alignItems="center" gap={2}>
                <CircularProgress size={20} />
                <Typography variant="body2">Loading system data...</Typography>
              </Box>
            ) : (
              <Grid container spacing={2}>
                <Grid item xs={6}>
                  <Card variant="outlined" sx={{ p: 2, textAlign: 'center' }}>
                    <Typography variant="h4" color="primary.main">
                      {projects.length}
                    </Typography>
                    <Typography variant="body2" color="textSecondary">
                      Projects
                    </Typography>
                  </Card>
                </Grid>
                <Grid item xs={6}>
                  <Card variant="outlined" sx={{ p: 2, textAlign: 'center' }}>
                    <Typography variant="h4" color="success.main">
                      {getActiveAgentsCount()}
                    </Typography>
                    <Typography variant="body2" color="textSecondary">
                      Active Agents
                    </Typography>
                  </Card>
                </Grid>
                <Grid item xs={6}>
                  <Card variant="outlined" sx={{ p: 2, textAlign: 'center' }}>
                    <Typography variant="h4" color="info.main">
                      {getActiveTeamsCount()}
                    </Typography>
                    <Typography variant="body2" color="textSecondary">
                      Active Teams
                    </Typography>
                  </Card>
                </Grid>
                <Grid item xs={6}>
                  <Card variant="outlined" sx={{ p: 2, textAlign: 'center' }}>
                    <Typography variant="h4" color="warning.main">
                      {getAverageWorkload()}%
                    </Typography>
                    <Typography variant="body2" color="textSecondary">
                      Avg Workload
                    </Typography>
                  </Card>
                </Grid>
              </Grid>
            )}
          </Paper>
        </Grid>

        {/* Recent Activity & Quick Actions */}
        <Grid item xs={12}>
          <Paper elevation={1} sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              System Activity
            </Typography>
            <Typography variant="body2" color="textSecondary" paragraph>
              Current projects, teams, and agents in the system
            </Typography>
            
            <Grid container spacing={3}>
              <Grid item xs={12} md={4}>
                <Typography variant="subtitle1" gutterBottom>
                  Projects
                </Typography>
                <List dense>
                  {projects.slice(0, 3).map((project) => (
                    <ListItem key={project.id} disablePadding>
                      <ListItemIcon>
                        <InfoIcon color="primary" fontSize="small" />
                      </ListItemIcon>
                      <ListItemText 
                        primary={
                          <Typography variant="body2">
                            {project.name}
                          </Typography>
                        }
                        secondary={
                          <Typography variant="caption" color="textSecondary">
                            {project.description || 'No description'}
                          </Typography>
                        }
                      />
                    </ListItem>
                  ))}
                  {projects.length === 0 && (
                    <ListItem disablePadding>
                      <ListItemText 
                        primary={
                          <Typography variant="body2" color="textSecondary">
                            No projects found
                          </Typography>
                        }
                      />
                    </ListItem>
                  )}
                </List>
              </Grid>
              
              <Grid item xs={12} md={4}>
                <Typography variant="subtitle1" gutterBottom>
                  Teams
                </Typography>
                <List dense>
                  {teams.slice(0, 3).map((team) => (
                    <ListItem key={team.id} disablePadding>
                      <ListItemIcon>
                        {team.is_active ? (
                          <CompletedIcon color="success" fontSize="small" />
                        ) : (
                          <PendingIcon color="disabled" fontSize="small" />
                        )}
                      </ListItemIcon>
                      <ListItemText 
                        primary={
                          <Typography variant="body2">
                            {team.name}
                          </Typography>
                        }
                        secondary={
                          <Typography variant="caption" color="textSecondary">
                            {team.is_active ? 'Active' : 'Inactive'}
                          </Typography>
                        }
                      />
                    </ListItem>
                  ))}
                  {teams.length === 0 && (
                    <ListItem disablePadding>
                      <ListItemText 
                        primary={
                          <Typography variant="body2" color="textSecondary">
                            No teams found
                          </Typography>
                        }
                      />
                    </ListItem>
                  )}
                </List>
              </Grid>
              
              <Grid item xs={12} md={4}>
                <Typography variant="subtitle1" gutterBottom>
                  Agents
                </Typography>
                <List dense>
                  {agents.slice(0, 3).map((agent) => (
                    <ListItem key={agent.id} disablePadding>
                      <ListItemIcon>
                        {agent.status === 'active' ? (
                          <CompletedIcon color="success" fontSize="small" />
                        ) : (
                          <PendingIcon color="disabled" fontSize="small" />
                        )}
                      </ListItemIcon>
                      <ListItemText 
                        primary={
                          <Typography variant="body2">
                            {agent.name}
                          </Typography>
                        }
                        secondary={
                          <Typography variant="caption" color="textSecondary">
                            {agent.status} • {agent.current_workload}/{agent.workload_capacity} capacity
                          </Typography>
                        }
                      />
                    </ListItem>
                  ))}
                  {agents.length === 0 && (
                    <ListItem disablePadding>
                      <ListItemText 
                        primary={
                          <Typography variant="body2" color="textSecondary">
                            No agents found
                          </Typography>
                        }
                      />
                    </ListItem>
                  )}
                </List>
              </Grid>
            </Grid>
          </Paper>
        </Grid>

        {/* Quick Links */}
        <Grid item xs={12}>
          <Alert severity="info" sx={{ mt: 2 }}>
            <Typography variant="body2">
              <strong>Getting Started:</strong> Navigate to "Projects" to create and manage your AI agent projects. 
              Each project can contain multiple teams with specialized agents configured for specific workflows.
            </Typography>
          </Alert>
        </Grid>
      </Grid>
    </Box>
  );
};

export default HomePage;