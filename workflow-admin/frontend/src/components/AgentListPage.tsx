import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Paper,
  Grid,
  Card,
  CardContent,
  Chip,
  Button,
  CircularProgress,
  Alert,
} from '@mui/material';
import {
  SmartToy as AgentIcon,
  CheckCircle as ActiveIcon,
  Pause as InactiveIcon,
  Build as ConfigIcon,
} from '@mui/icons-material';
import { Link } from 'react-router-dom';
import { Agent, agentsApi } from '../api/agents';

const AgentListPage: React.FC = () => {
  const [agents, setAgents] = useState<Agent[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchAgents = async () => {
      try {
        const agentData = await agentsApi.getAgents();
        setAgents(agentData);
      } catch (err) {
        setError('Failed to load agents');
        console.error('Error loading agents:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchAgents();
  }, []);

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active':
        return 'success';
      case 'inactive':
        return 'default';
      case 'busy':
        return 'warning';
      default:
        return 'default';
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'active':
        return <ActiveIcon fontSize="small" />;
      default:
        return <InactiveIcon fontSize="small" />;
    }
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Alert severity="error" sx={{ mt: 2 }}>
        {error}
      </Alert>
    );
  }

  return (
    <Box>
      <Box display="flex" alignItems="center" gap={2} mb={3}>
        <AgentIcon color="primary" sx={{ fontSize: 32 }} />
        <Box>
          <Typography variant="h4" gutterBottom>
            All Agents
          </Typography>
          <Typography variant="body1" color="textSecondary">
            Individual AI agents configured across all projects and teams
          </Typography>
        </Box>
      </Box>

      <Grid container spacing={3}>
        {agents.map((agent) => (
          <Grid item xs={12} md={6} lg={4} key={agent.id}>
            <Card variant="outlined" sx={{ height: '100%' }}>
              <CardContent>
                <Box display="flex" alignItems="center" gap={1} mb={2}>
                  <AgentIcon color="primary" />
                  <Typography variant="h6" component="div">
                    {agent.name}
                  </Typography>
                  <Box ml="auto">
                    {getStatusIcon(agent.status)}
                  </Box>
                </Box>

                <Typography variant="body2" color="textSecondary" paragraph>
                  {agent.description}
                </Typography>

                <Box display="flex" flexWrap="wrap" gap={1} mb={2}>
                  <Chip
                    label={agent.status}
                    color={getStatusColor(agent.status) as any}
                    size="small"
                  />
                  {agent.agent_type && (
                    <Chip
                      label={agent.agent_type.name}
                      variant="outlined"
                      size="small"
                    />
                  )}
                </Box>

                {agent.workload_capacity && (
                  <Typography variant="caption" color="textSecondary" paragraph>
                    Workload: {agent.current_workload || 0} / {agent.workload_capacity}
                    {' '}({Math.round(((agent.current_workload || 0) / agent.workload_capacity) * 100)}% capacity)
                  </Typography>
                )}

                <Box display="flex" justifyContent="space-between" alignItems="center" mt={2}>
                  <Button
                    variant="outlined"
                    size="small"
                    component={Link}
                    to={`/agents-list/${agent.id}`}
                  >
                    View Details
                  </Button>
                  
                  {agent.configuration && (
                    <Chip
                      icon={<ConfigIcon fontSize="small" />}
                      label="Configured"
                      size="small"
                      variant="filled"
                      sx={{ backgroundColor: 'grey.200' }}
                    />
                  )}
                </Box>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      {agents.length === 0 && (
        <Paper sx={{ p: 4, textAlign: 'center', mt: 4 }}>
          <AgentIcon sx={{ fontSize: 48, color: 'text.secondary', mb: 2 }} />
          <Typography variant="h6" color="textSecondary" gutterBottom>
            No agents found
          </Typography>
          <Typography variant="body2" color="textSecondary">
            Create your first agent to get started with AI-powered workflows.
          </Typography>
        </Paper>
      )}
    </Box>
  );
};

export default AgentListPage;