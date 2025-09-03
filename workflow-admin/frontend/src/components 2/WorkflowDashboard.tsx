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
  LinearProgress,
} from '@mui/material';
import {
  AccountTree as WorkflowIcon,
  Flag as PriorityIcon,
  Schedule as TimeIcon,
  Assignment as StepsIcon,
} from '@mui/icons-material';
import { Workflow, workflowsApi } from '../api/workflows';

const WorkflowDashboard: React.FC = () => {
  const [workflows, setWorkflows] = useState<Workflow[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      setLoading(true);
      setError(null);
      const workflowsData = await workflowsApi.getWorkflows();
      setWorkflows(workflowsData);
    } catch (err) {
      console.error('Error loading workflow data:', err);
      setError('Failed to load workflow data.');
    } finally {
      setLoading(false);
    }
  };

  const getStatusColor = (status: string) => {
    switch (status.toLowerCase()) {
      case 'active':
        return 'success';
      case 'in_progress':
        return 'info';
      case 'draft':
        return 'warning';
      case 'completed':
        return 'success';
      case 'paused':
        return 'default';
      default:
        return 'default';
    }
  };

  const getPriorityColor = (priority: string) => {
    switch (priority?.toLowerCase()) {
      case 'critical':
        return 'error';
      case 'high':
        return 'warning';
      case 'medium':
        return 'info';
      case 'low':
        return 'default';
      default:
        return 'default';
    }
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="200px">
        <CircularProgress />
        <Typography variant="body2" sx={{ ml: 2 }}>
          Loading workflow data...
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
        Workflow Dashboard
      </Typography>
      <Typography variant="body1" color="textSecondary" paragraph>
        Manage and monitor workflows and their execution status.
      </Typography>

      <Grid container spacing={3}>
        <Grid item xs={12}>
          <Paper elevation={1} sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Workflows ({workflows.length})
            </Typography>
            
            {workflows.length === 0 ? (
              <Box sx={{ p: 2, textAlign: 'center' }}>
                <Typography variant="body2" color="textSecondary">
                  No workflows found. Create some workflows to get started.
                </Typography>
              </Box>
            ) : (
              <List>
                {workflows.map((workflow) => (
                  <ListItem key={workflow.id} divider>
                    <ListItemIcon>
                      <WorkflowIcon color="primary" />
                    </ListItemIcon>
                    <ListItemText
                      primary={
                        <Box display="flex" alignItems="center" gap={1}>
                          <Typography variant="subtitle1" fontWeight="medium">
                            {workflow.name}
                          </Typography>
                          <Chip
                            label={workflow.status}
                            size="small"
                            color={getStatusColor(workflow.status) as any}
                            variant="outlined"
                          />
                          <Chip
                            icon={<PriorityIcon />}
                            label={workflow.priority}
                            size="small"
                            color={getPriorityColor(workflow.priority) as any}
                            variant="filled"
                          />
                        </Box>
                      }
                      secondary={
                        <Box sx={{ mt: 1 }}>
                          {workflow.description && (
                            <Typography variant="body2" color="textSecondary" paragraph>
                              {workflow.description}
                            </Typography>
                          )}
                          
                          <Box display="flex" alignItems="center" gap={2} sx={{ mt: 1 }}>
                            {workflow.definition?.steps && (
                              <Box display="flex" alignItems="center" gap={0.5}>
                                <StepsIcon fontSize="small" color="action" />
                                <Typography variant="caption" color="textSecondary">
                                  {workflow.definition.steps} steps
                                </Typography>
                              </Box>
                            )}
                            
                            {workflow.definition?.estimated_time && (
                              <Box display="flex" alignItems="center" gap={0.5}>
                                <TimeIcon fontSize="small" color="action" />
                                <Typography variant="caption" color="textSecondary">
                                  Est: {workflow.definition.estimated_time}
                                </Typography>
                              </Box>
                            )}
                            
                            <Typography variant="caption" color="textSecondary">
                              Project: {workflow.project_id}
                            </Typography>
                            
                            {workflow.assigned_team_id && (
                              <Typography variant="caption" color="textSecondary">
                                Team: {workflow.assigned_team_id}
                              </Typography>
                            )}
                            
                            {workflow.primary_agent_id && (
                              <Typography variant="caption" color="textSecondary">
                                Agent: {workflow.primary_agent_id}
                              </Typography>
                            )}
                          </Box>
                          
                          {workflow.status === 'in_progress' && (
                            <Box sx={{ mt: 1 }}>
                              <Typography variant="caption" color="textSecondary">
                                Progress
                              </Typography>
                              <LinearProgress 
                                variant="determinate" 
                                value={65} // Mock progress
                                sx={{ mt: 0.5, height: 4, borderRadius: 2 }}
                                color="info"
                              />
                            </Box>
                          )}
                          
                          <Typography variant="caption" color="textSecondary" sx={{ mt: 1, display: 'block' }}>
                            Created: {new Date(workflow.created_at).toLocaleDateString()}
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

export default WorkflowDashboard;