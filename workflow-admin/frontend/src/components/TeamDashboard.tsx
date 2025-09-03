import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Box,
  Typography,
  Paper,
  Grid,
  Alert,
  CircularProgress,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  Chip,
  Avatar,
  AvatarGroup,
  Card,
  CardContent,
  Button,
  Divider,
  Collapse,
} from '@mui/material';
import {
  Group as TeamIcon,
  Person as LeaderIcon,
  Groups as MembersIcon,
  ExpandMore as ExpandMoreIcon,
  ExpandLess as ExpandLessIcon,
  SmartToy as AgentIcon,
  Circle as StatusIcon,
} from '@mui/icons-material';
import { Team, teamsApi } from '../api/teams';

const TeamDashboard: React.FC = () => {
  const navigate = useNavigate();
  const [teams, setTeams] = useState<Team[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [expandedTeams, setExpandedTeams] = useState<Set<number>>(new Set());

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      setLoading(true);
      setError(null);
      const teamsData = await teamsApi.getTeams();
      console.log('TeamDashboard - Loaded teams data:', teamsData);
      setTeams(teamsData);
    } catch (err) {
      console.error('Error loading team data:', err);
      setError('Failed to load team data.');
    } finally {
      setLoading(false);
    }
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

  const getStatusColor = (status: string | undefined) => {
    if (!status) return 'default';
    switch (status.toLowerCase()) {
      case 'active':
        return 'success';
      case 'planning':
        return 'warning';
      case 'inactive':
        return 'default';
      default:
        return 'info';
    }
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="200px">
        <CircularProgress />
        <Typography variant="body2" sx={{ ml: 2 }}>
          Loading team data...
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
      <Typography variant="h4" gutterBottom>
        Team Dashboard
      </Typography>
      <Typography variant="body1" color="textSecondary" paragraph>
        Manage and monitor teams and their members in the workflow system.
      </Typography>

      <Paper elevation={1} sx={{ p: 3 }}>
        <Typography variant="h6" gutterBottom>
          Teams ({teams.length})
        </Typography>
        
        {teams.length === 0 ? (
          <Alert severity="info">
            No teams found. Create some teams to get started.
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
                        <Chip
                          label={team.status || 'Unknown'}
                          size="small"
                          color={getStatusColor(team.status) as any}
                          variant="outlined"
                        />
                      </Box>
                      <Button size="small" endIcon={expandedTeams.has(team.id) ? <ExpandLessIcon /> : <ExpandMoreIcon />}>
                        {expandedTeams.has(team.id) ? 'Hide Details' : 'Show Details'}
                      </Button>
                    </Box>
                    
                    {team.description && (
                      <Typography variant="body2" color="textSecondary" paragraph>
                        {team.description}
                      </Typography>
                    )}
                    
                    <Box display="flex" justifyContent="space-between" alignItems="center" mb={expandedTeams.has(team.id) ? 2 : 0}>
                      <Box display="flex" gap={2}>
                        {team.lead_agent_id && (
                          <Typography variant="caption" color="textSecondary">
                            <LeaderIcon fontSize="small" sx={{ verticalAlign: 'middle', mr: 0.5 }} />
                            Lead: Agent {team.lead_agent_id}
                          </Typography>
                        )}
                        <Typography variant="caption" color="textSecondary">
                          <MembersIcon fontSize="small" sx={{ verticalAlign: 'middle', mr: 0.5 }} />
                          {team.member_agent_ids?.length || 0} members
                        </Typography>
                      </Box>
                      {team.project_id && (
                        <Typography variant="caption" color="textSecondary">
                          Project: {team.project_id}
                        </Typography>
                      )}
                    </Box>

                    <Collapse in={expandedTeams.has(team.id)} timeout="auto" unmountOnExit>
                      <Box>
                        <Divider sx={{ mb: 2 }} />
                        <Typography variant="subtitle2" gutterBottom color="primary">
                          Team Members
                        </Typography>
                        {team.member_agent_ids && team.member_agent_ids.length > 0 ? (
                          <List dense>
                            {team.member_agent_ids.map((agentId, index) => (
                              <ListItem key={agentId} disablePadding>
                                <ListItemIcon>
                                  <StatusIcon fontSize="small" color="success" />
                                </ListItemIcon>
                                <ListItemText
                                  primary={
                                    <Box display="flex" alignItems="center" gap={1}>
                                      <Typography variant="body2" fontWeight="medium">
                                        Agent {agentId}
                                      </Typography>
                                      {agentId === team.lead_agent_id && (
                                        <Chip 
                                          label="Team Lead" 
                                          size="small" 
                                          color="primary"
                                          variant="outlined"
                                          sx={{ fontSize: '0.7rem' }}
                                        />
                                      )}
                                    </Box>
                                  }
                                  secondary={`Active team member • Added ${new Date(team.created_at).toLocaleDateString()}`}
                                />
                              </ListItem>
                            ))}
                          </List>
                        ) : (
                          <Typography variant="body2" color="textSecondary">
                            No members assigned to this team yet.
                          </Typography>
                        )}
                      </Box>
                    </Collapse>
                    
                    {/* Quick action to view full details */}
                    <Box sx={{ p: 2, pt: 0 }}>
                      <Button
                        variant="outlined"
                        size="small"
                        fullWidth
                        onClick={(e) => {
                          e.stopPropagation();
                          navigate(`/teams/${team.id}`);
                        }}
                      >
                        View Full Details
                      </Button>
                    </Box>
                  </CardContent>
                </Card>
              </Grid>
            ))}
          </Grid>
        )}
      </Paper>
    </Box>
  );
};

export default TeamDashboard;