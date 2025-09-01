import React, { useState, useEffect } from 'react';
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
} from '@mui/material';
import {
  Group as TeamIcon,
  Person as LeaderIcon,
  Groups as MembersIcon,
} from '@mui/icons-material';
import { Team, teamsApi } from '../api/teams';

const TeamDashboard: React.FC = () => {
  const [teams, setTeams] = useState<Team[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      setLoading(true);
      setError(null);
      const teamsData = await teamsApi.getTeams();
      setTeams(teamsData);
    } catch (err) {
      console.error('Error loading team data:', err);
      setError('Failed to load team data.');
    } finally {
      setLoading(false);
    }
  };

  const getStatusColor = (status: string) => {
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

      <Grid container spacing={3}>
        <Grid item xs={12}>
          <Paper elevation={1} sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Teams ({teams.length})
            </Typography>
            
            {teams.length === 0 ? (
              <Box sx={{ p: 2, textAlign: 'center' }}>
                <Typography variant="body2" color="textSecondary">
                  No teams found. Create some teams to get started.
                </Typography>
              </Box>
            ) : (
              <List>
                {teams.map((team) => (
                  <ListItem key={team.id} divider>
                    <ListItemIcon>
                      <TeamIcon color="primary" />
                    </ListItemIcon>
                    <ListItemText
                      primary={
                        <Box display="flex" alignItems="center" gap={1}>
                          <Typography variant="subtitle1" fontWeight="medium">
                            {team.name}
                          </Typography>
                          <Chip
                            label={team.status}
                            size="small"
                            color={getStatusColor(team.status) as any}
                            variant="outlined"
                          />
                        </Box>
                      }
                      secondary={
                        <Box sx={{ mt: 1 }}>
                          {team.description && (
                            <Typography variant="body2" color="textSecondary" paragraph>
                              {team.description}
                            </Typography>
                          )}
                          
                          <Box display="flex" alignItems="center" gap={2} sx={{ mt: 1 }}>
                            {team.lead_agent_id && (
                              <Box display="flex" alignItems="center" gap={0.5}>
                                <LeaderIcon fontSize="small" color="action" />
                                <Typography variant="caption" color="textSecondary">
                                  Lead: Agent {team.lead_agent_id}
                                </Typography>
                              </Box>
                            )}
                            
                            {team.member_agent_ids && team.member_agent_ids.length > 0 && (
                              <Box display="flex" alignItems="center" gap={0.5}>
                                <MembersIcon fontSize="small" color="action" />
                                <Typography variant="caption" color="textSecondary">
                                  Members: {team.member_agent_ids.length}
                                </Typography>
                                <AvatarGroup max={3} sx={{ '& .MuiAvatar-root': { width: 20, height: 20, fontSize: '0.75rem' } }}>
                                  {team.member_agent_ids.map((agentId) => (
                                    <Avatar key={agentId} sx={{ bgcolor: 'primary.main' }}>
                                      {agentId}
                                    </Avatar>
                                  ))}
                                </AvatarGroup>
                              </Box>
                            )}
                            
                            {team.project_id && (
                              <Typography variant="caption" color="textSecondary">
                                Project: {team.project_id}
                              </Typography>
                            )}
                          </Box>
                          
                          <Typography variant="caption" color="textSecondary" sx={{ mt: 1, display: 'block' }}>
                            Created: {new Date(team.created_at).toLocaleDateString()}
                          </Typography>
                        </Box>
                      }
                    />
                  </ListItem>
                ))}
              </List>
            )}
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
};

export default TeamDashboard;