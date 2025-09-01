import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Paper,
  Grid,
  Alert,
  CircularProgress,
} from '@mui/material';
import { Agent, AgentType, agentsApi } from '../api/agents';
import AgentTypeList from './AgentTypeList';
import AgentList from './AgentList';

const AgentDashboard: React.FC = () => {
  const [agents, setAgents] = useState<Agent[]>([]);
  const [agentTypes, setAgentTypes] = useState<AgentType[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      setLoading(true);
      setError(null);
      
      const [agentsData, agentTypesData] = await Promise.all([
        agentsApi.getAgents(),
        agentsApi.getAgentTypes(),
      ]);
      
      setAgents(agentsData);
      setAgentTypes(agentTypesData);
    } catch (err) {
      console.error('Error loading agent data:', err);
      setError('Failed to load agent data. Please check if the backend is running.');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="200px">
        <CircularProgress />
        <Typography variant="body2" sx={{ ml: 2 }}>
          Loading agent data...
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
        Agent Dashboard
      </Typography>
      <Typography variant="body1" color="textSecondary" paragraph>
        Manage and monitor AI agents and their types in the workflow system.
      </Typography>

      <Grid container spacing={3}>
        {/* Agent Types Section */}
        <Grid item xs={12} md={6}>
          <Paper elevation={1} sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Agent Types ({agentTypes.length})
            </Typography>
            <AgentTypeList agentTypes={agentTypes} />
          </Paper>
        </Grid>

        {/* Individual Agents Section */}
        <Grid item xs={12} md={6}>
          <Paper elevation={1} sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Individual Agents ({agents.length})
            </Typography>
            <AgentList agents={agents} agentTypes={agentTypes} />
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
};

export default AgentDashboard;