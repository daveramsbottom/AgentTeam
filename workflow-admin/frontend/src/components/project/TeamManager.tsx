import React, { useState } from 'react';
import {
  Box,
  Typography,
  Paper,
  Grid,
  Card,
  CardContent,
  Button,
  Alert,
  IconButton,
  Chip,
  Tooltip,
  CircularProgress,
  Collapse,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
} from '@mui/material';
import {
  Add as AddIcon,
  Group as TeamIcon,
  Edit as EditIcon,
  SmartToy as AgentIcon,
  Circle as StatusIcon,
  AccountTree as WorkflowIcon,
  Launch as LaunchIcon,
  ExpandLess as ExpandLessIcon,
  ExpandMore as ExpandMoreIcon,
} from '@mui/icons-material';
import { TeamManagementProps, TeamSummary } from './types';
import { teamsApi, CreateTeamRequest, UpdateTeamRequest } from '../../api/teams';
import TeamCreateModal from './TeamCreateModal';
import TeamEditModal from './TeamEditModal';

const TeamManager: React.FC<TeamManagementProps> = ({
  project,
  teams,
  agents,
  isEditMode,
  onTeamsUpdate,
  expandedTeams,
  onToggleTeamExpansion,
  onWorkflowNavigation,
}) => {
  const [createModalOpen, setCreateModalOpen] = useState(false);
  const [editModalOpen, setEditModalOpen] = useState(false);
  const [editingTeam, setEditingTeam] = useState<TeamSummary | null>(null);
  const [creatingTeam, setCreatingTeam] = useState(false);
  const [updatingTeam, setUpdatingTeam] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const getStatusColor = (status: 'active' | 'idle' | 'busy') => {
    switch (status) {
      case 'active': return 'success';
      case 'busy': return 'warning';
      case 'idle': return 'info';
      default: return 'default';
    }
  };

  const refreshTeams = async () => {
    try {
      const projectTeams = await teamsApi.getTeams();
      const filteredTeams = projectTeams.filter(team => team.project_id === project.id);
      
      const getAgentById = (agentId: number) => agents.find(agent => agent.id === agentId);
      
      const teamSummaries = filteredTeams.map(team => {
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
              workflow_version: 'v1.0.0',
              workflow_id: 1
            };
          }) || []
        };
      });
      
      onTeamsUpdate(teamSummaries);
    } catch (err) {
      console.error('Error refreshing teams:', err);
      setError('Failed to refresh teams');
    }
  };

  const handleCreateTeam = async (teamData: any) => {
    setCreatingTeam(true);
    setError(null);
    
    try {
      const newTeamData: CreateTeamRequest = {
        name: teamData.name,
        description: teamData.description,
        project_id: project.id,
        team_lead_id: teamData.team_lead_id || undefined,
        member_agent_ids: teamData.member_agent_ids,
      };
      
      await teamsApi.createTeam(newTeamData);
      await refreshTeams();
      setCreateModalOpen(false);
    } catch (err) {
      console.error('Error creating team:', err);
      setError('Failed to create team. Please try again.');
    } finally {
      setCreatingTeam(false);
    }
  };

  const handleEditTeam = (team: TeamSummary) => {
    setEditingTeam(team);
    setEditModalOpen(true);
  };

  const handleUpdateTeam = async (teamData: any) => {
    if (!editingTeam) return;
    
    setUpdatingTeam(true);
    setError(null);
    
    try {
      const updateTeamData: UpdateTeamRequest = {
        name: teamData.name,
        description: teamData.description,
        team_lead_id: teamData.team_lead_id || undefined,
        member_agent_ids: teamData.member_agent_ids,
      };
      
      await teamsApi.updateTeam(editingTeam.id, updateTeamData);
      await refreshTeams();
      setEditModalOpen(false);
      setEditingTeam(null);
    } catch (err) {
      console.error('Error updating team:', err);
      setError('Failed to update team. Please try again.');
    } finally {
      setUpdatingTeam(false);
    }
  };

  return (
    <Paper elevation={1} sx={{ p: 3 }}>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
        <Typography variant="h6">
          Project Teams ({teams.length})
        </Typography>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={() => setCreateModalOpen(true)}
          size="small"
        >
          Add Team
        </Button>
      </Box>
      
      {error && (
        <Alert severity="error" sx={{ mb: 2 }} onClose={() => setError(null)}>
          {error}
        </Alert>
      )}
      
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
                  >
                    <Box 
                      display="flex" 
                      alignItems="center" 
                      gap={1}
                      sx={{ cursor: 'pointer', flexGrow: 1 }}
                      onClick={() => onToggleTeamExpansion(team.id)}
                    >
                      <TeamIcon color="primary" />
                      <Typography variant="subtitle1" fontWeight="medium">
                        {team.name}
                      </Typography>
                    </Box>
                    <Box display="flex" alignItems="center" gap={1}>
                      {isEditMode && (
                        <IconButton
                          size="small"
                          onClick={(e) => {
                            e.stopPropagation();
                            handleEditTeam(team);
                          }}
                          sx={{
                            color: 'warning.main',
                            '&:hover': { backgroundColor: 'warning.light' }
                          }}
                        >
                          <EditIcon fontSize="small" />
                        </IconButton>
                      )}
                      <IconButton
                        size="small"
                        onClick={() => onToggleTeamExpansion(team.id)}
                      >
                        {expandedTeams.has(team.id) ? <ExpandLessIcon /> : <ExpandMoreIcon />}
                      </IconButton>
                    </Box>
                  </Box>
                  
                  <Typography variant="body2" color="text.secondary" gutterBottom>
                    {team.specialization}
                  </Typography>
                  
                  <Box display="flex" gap={1} mb={2}>
                    <Chip size="small" label={`${team.agent_count} members`} />
                    <Chip size="small" label={`Lead: ${team.lead_agent}`} variant="outlined" />
                  </Box>
                  
                  <Collapse in={expandedTeams.has(team.id)} timeout="auto" unmountOnExit>
                    <List dense>
                      {team.members?.map((member) => (
                        <ListItem
                          key={member.id}
                          sx={{
                            cursor: 'pointer',
                            '&:hover': {
                              backgroundColor: 'action.hover'
                            }
                          }}
                          onClick={() => onWorkflowNavigation(
                            member.workflow_id || 1, 
                            member.name, 
                            member.role
                          )}
                        >
                          <ListItemIcon>
                            <AgentIcon color="action" />
                          </ListItemIcon>
                          <ListItemText
                            primary={
                              <Box display="flex" alignItems="center" gap={1}>
                                <Typography variant="body2" fontWeight="medium">
                                  {member.name}
                                </Typography>
                                <Chip 
                                  size="small" 
                                  label={member.role} 
                                  color={member.role === 'Team Lead' ? 'primary' : 'default'} 
                                  variant="outlined"
                                />
                              </Box>
                            }
                            secondary={
                              <Box display="flex" alignItems="center" gap={1} mt={0.5}>
                                <StatusIcon 
                                  sx={{ 
                                    fontSize: 12, 
                                    color: `${getStatusColor(member.status)}.main` 
                                  }} 
                                />
                                <Typography variant="caption">
                                  {member.status.charAt(0).toUpperCase() + member.status.slice(1)}
                                </Typography>
                                <Typography variant="caption" color="text.secondary">
                                  • {member.specialization}
                                </Typography>
                              </Box>
                            }
                          />
                          <Tooltip title="View workflow details">
                            <IconButton size="small">
                              <LaunchIcon fontSize="small" />
                            </IconButton>
                          </Tooltip>
                        </ListItem>
                      ))}
                    </List>
                  </Collapse>
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>
      )}

      <TeamCreateModal
        open={createModalOpen}
        agents={agents}
        onClose={() => setCreateModalOpen(false)}
        onSubmit={handleCreateTeam}
        loading={creatingTeam}
      />

      <TeamEditModal
        open={editModalOpen}
        agents={agents}
        team={editingTeam}
        onClose={() => {
          setEditModalOpen(false);
          setEditingTeam(null);
        }}
        onSubmit={handleUpdateTeam}
        loading={updatingTeam}
      />
    </Paper>
  );
};

export default TeamManager;