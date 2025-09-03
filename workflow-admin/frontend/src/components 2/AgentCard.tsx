import React from 'react';
import {
  ListItem,
  ListItemText,
  ListItemIcon,
  Box,
  Typography,
  Chip,
  LinearProgress,
} from '@mui/material';
import {
  Person as PersonIcon,
  Circle as StatusIcon,
} from '@mui/icons-material';
import { Agent, AgentType } from '../api/agents';

interface AgentCardProps {
  agent: Agent;
  agentType?: AgentType;
}

const AgentCard: React.FC<AgentCardProps> = ({ agent, agentType }) => {
  // Calculate workload percentage
  const workloadPercentage = agent.workload_capacity > 0 
    ? (agent.current_workload / agent.workload_capacity) * 100 
    : 0;

  // Determine status color
  const getStatusColor = (status: string) => {
    switch (status.toLowerCase()) {
      case 'active':
        return 'success';
      case 'inactive':
        return 'default';
      case 'maintenance':
        return 'warning';
      case 'error':
        return 'error';
      default:
        return 'default';
    }
  };

  const formatLastActive = (lastActive?: string) => {
    if (!lastActive) return 'Never';
    const date = new Date(lastActive);
    return date.toLocaleDateString();
  };

  return (
    <ListItem divider sx={{ py: 2 }}>
      <ListItemIcon>
        <PersonIcon color="primary" />
      </ListItemIcon>
      <ListItemText
        primary={
          <Box display="flex" alignItems="center" gap={1}>
            <Typography variant="subtitle1" fontWeight="medium">
              {agent.name}
            </Typography>
            <Chip
              icon={<StatusIcon />}
              label={agent.status}
              size="small"
              color={getStatusColor(agent.status) as any}
              variant="outlined"
            />
          </Box>
        }
        secondary={
          <Box sx={{ mt: 1 }}>
            {/* Agent Type */}
            <Typography variant="body2" color="textSecondary">
              Type: {agentType?.name || 'Unknown'}
            </Typography>
            
            {/* Description */}
            {agent.description && (
              <Typography variant="body2" color="textSecondary">
                {agent.description}
              </Typography>
            )}
            
            {/* Workload */}
            <Box sx={{ mt: 1 }}>
              <Box display="flex" alignItems="center" justifyContent="space-between">
                <Typography variant="caption" color="textSecondary">
                  Workload: {agent.current_workload}/{agent.workload_capacity}
                </Typography>
                <Typography variant="caption" color="textSecondary">
                  {workloadPercentage.toFixed(0)}%
                </Typography>
              </Box>
              <LinearProgress 
                variant="determinate" 
                value={workloadPercentage} 
                sx={{ mt: 0.5, height: 4, borderRadius: 2 }}
                color={workloadPercentage > 80 ? 'warning' : 'primary'}
              />
            </Box>
            
            {/* Last Active */}
            <Typography variant="caption" color="textSecondary" sx={{ mt: 1, display: 'block' }}>
              Last active: {formatLastActive(agent.last_active)}
            </Typography>
            
            {/* Specializations */}
            {agent.specializations && Object.keys(agent.specializations).length > 0 && (
              <Typography variant="caption" color="textSecondary" sx={{ display: 'block' }}>
                Specializations: {Object.keys(agent.specializations).length} defined
              </Typography>
            )}
          </Box>
        }
      />
    </ListItem>
  );
};

export default AgentCard;