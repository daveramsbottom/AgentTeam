import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Card,
  CardContent,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  Chip,
  Avatar,
  AvatarGroup,
  IconButton,
  Tooltip,
  Badge,
} from '@mui/material';
import {
  ExpandMore as ExpandMoreIcon,
  Folder as ProjectIcon,
  Group as TeamIcon,
  Person as AgentIcon,
  Add as AddIcon,
  Info as InfoIcon,
} from '@mui/icons-material';
import { ProjectHierarchy, hierarchyApi } from '../api/hierarchy';

interface ProjectHierarchyViewProps {
  projectId: number;
}

const ProjectHierarchyView: React.FC<ProjectHierarchyViewProps> = ({ projectId }) => {
  const [hierarchy, setHierarchy] = useState<ProjectHierarchy | null>(null);
  const [loading, setLoading] = useState(true);
  const [expandedTeam, setExpandedTeam] = useState<string | false>(false);

  useEffect(() => {
    loadHierarchy();
  }, [projectId]);

  const loadHierarchy = async () => {
    try {
      setLoading(true);
      const data = await hierarchyApi.getProjectHierarchy(projectId);
      setHierarchy(data);
    } catch (error) {
      console.error('Error loading project hierarchy:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleTeamExpand = (panel: string) => (_: React.SyntheticEvent, isExpanded: boolean) => {
    setExpandedTeam(isExpanded ? panel : false);
  };

  const getStatusColor = (status: string) => {
    switch (status.toLowerCase()) {
      case 'active': return 'success';
      case 'planning': return 'warning';
      case 'inactive': return 'default';
      default: return 'info';
    }
  };

  const getTeamTypeIcon = (teamType: string) => {
    // You can customize icons based on team type
    return <TeamIcon />;
  };

  if (loading || !hierarchy) {
    return (
      <Box display="flex" justifyContent="center" p={4}>
        <Typography>Loading project hierarchy...</Typography>
      </Box>
    );
  }

  return (
    <Box>
      {/* Project Header */}
      <Card elevation={2} sx={{ mb: 3 }}>
        <CardContent>
          <Box display="flex" alignItems="center" gap={2} mb={2}>
            <ProjectIcon color="primary" fontSize="large" />
            <Box flexGrow={1}>
              <Typography variant="h5" fontWeight="bold">
                {hierarchy.project.name}
              </Typography>
              <Typography variant="body2" color="textSecondary">
                {hierarchy.project.description}
              </Typography>
            </Box>
            <Box textAlign="right">
              <Chip
                label={hierarchy.project.status}
                color={getStatusColor(hierarchy.project.status) as any}
                variant="outlined"
              />
            </Box>
          </Box>

          {/* Project Stats */}
          <Box display="flex" gap={3}>
            <Box textAlign="center">
              <Typography variant="h6" color="primary">
                {hierarchy.project.team_count}
              </Typography>
              <Typography variant="caption" color="textSecondary">
                Teams
              </Typography>
            </Box>
            <Box textAlign="center">
              <Typography variant="h6" color="primary">
                {hierarchy.project.agent_count}
              </Typography>
              <Typography variant="caption" color="textSecondary">
                Agents
              </Typography>
            </Box>
          </Box>

          {/* Project Context Preview */}
          <Box mt={2} p={2} bgcolor="grey.50" borderRadius={1}>
            <Typography variant="subtitle2" gutterBottom>
              Project Context:
            </Typography>
            <Typography variant="body2" color="textSecondary">
              <strong>Purpose:</strong> {hierarchy.project.context?.purpose}
            </Typography>
            <Typography variant="body2" color="textSecondary">
              <strong>Scope:</strong> {hierarchy.project.context?.scope}
            </Typography>
          </Box>
        </CardContent>
      </Card>

      {/* Teams Hierarchy */}
      <Typography variant="h6" gutterBottom sx={{ mt: 3, mb: 2 }}>
        Team Structure
      </Typography>

      {hierarchy.teams.map((team) => (
        <Accordion
          key={team.id}
          expanded={expandedTeam === `team-${team.id}`}
          onChange={handleTeamExpand(`team-${team.id}`)}
          sx={{ mb: 2 }}
        >
          <AccordionSummary expandIcon={<ExpandMoreIcon />}>
            <Box display="flex" alignItems="center" gap={2} width="100%">
              <Badge badgeContent={team.agent_count} color="primary">
                {getTeamTypeIcon(team.team_type)}
              </Badge>
              <Box flexGrow={1}>
                <Typography variant="subtitle1" fontWeight="medium">
                  {team.name}
                </Typography>
                <Typography variant="body2" color="textSecondary">
                  {team.team_type} • {team.agent_count} agents
                </Typography>
              </Box>
              <Chip
                label={team.status}
                size="small"
                color={getStatusColor(team.status) as any}
                variant="outlined"
              />
              <Tooltip title="View team context">
                <IconButton size="small">
                  <InfoIcon fontSize="small" />
                </IconButton>
              </Tooltip>
            </Box>
          </AccordionSummary>
          
          <AccordionDetails>
            <Box>
              {/* Team Context */}
              <Box mb={3} p={2} bgcolor="blue.50" borderRadius={1}>
                <Typography variant="subtitle2" gutterBottom>
                  Team Context (Inherited + Specialized):
                </Typography>
                <Typography variant="body2" color="textSecondary" paragraph>
                  <strong>Specialization:</strong> {team.context?.specialization}
                </Typography>
                <Typography variant="body2" color="textSecondary">
                  <strong>Responsibilities:</strong> {team.context?.responsibilities?.join(', ')}
                </Typography>
              </Box>

              {/* Team Agents */}
              <Typography variant="subtitle2" gutterBottom>
                Team Members:
              </Typography>
              
              <Box display="flex" flexWrap="wrap" gap={2} mb={2}>
                {team.agents.map((agent) => (
                  <Card key={agent.id} variant="outlined" sx={{ minWidth: 200 }}>
                    <CardContent sx={{ p: 2, '&:last-child': { pb: 2 } }}>
                      <Box display="flex" alignItems="center" gap={1} mb={1}>
                        <Avatar sx={{ width: 32, height: 32, bgcolor: 'primary.main' }}>
                          <AgentIcon fontSize="small" />
                        </Avatar>
                        <Box>
                          <Typography variant="subtitle2">
                            {agent.name}
                          </Typography>
                          <Typography variant="caption" color="textSecondary">
                            {agent.role}
                          </Typography>
                        </Box>
                        <Chip
                          label={agent.status}
                          size="small"
                          color={getStatusColor(agent.status) as any}
                          variant="filled"
                        />
                      </Box>
                    </CardContent>
                  </Card>
                ))}
                
                {/* Add Agent Button */}
                <Card variant="outlined" sx={{ minWidth: 200, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                  <CardContent sx={{ p: 2 }}>
                    <IconButton color="primary">
                      <AddIcon />
                    </IconButton>
                    <Typography variant="body2" color="textSecondary" textAlign="center">
                      Add Agent
                    </Typography>
                  </CardContent>
                </Card>
              </Box>
            </Box>
          </AccordionDetails>
        </Accordion>
      ))}

      {/* Add Team Button */}
      <Card variant="outlined" sx={{ mt: 2, cursor: 'pointer' }}>
        <CardContent sx={{ textAlign: 'center', py: 3 }}>
          <IconButton color="primary" size="large">
            <AddIcon fontSize="large" />
          </IconButton>
          <Typography variant="h6" color="primary" gutterBottom>
            Add New Team
          </Typography>
          <Typography variant="body2" color="textSecondary">
            Create a new team with inherited project context
          </Typography>
        </CardContent>
      </Card>
    </Box>
  );
};

export default ProjectHierarchyView;