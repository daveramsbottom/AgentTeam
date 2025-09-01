import React from 'react';
import {
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  Chip,
  Box,
  Typography,
} from '@mui/material';
import {
  SmartToy as RobotIcon,
  CheckCircle as ActiveIcon,
  Cancel as InactiveIcon,
} from '@mui/icons-material';
import { AgentType } from '../api/agents';

interface AgentTypeListProps {
  agentTypes: AgentType[];
}

const AgentTypeList: React.FC<AgentTypeListProps> = ({ agentTypes }) => {
  if (agentTypes.length === 0) {
    return (
      <Box sx={{ p: 2, textAlign: 'center' }}>
        <Typography variant="body2" color="textSecondary">
          No agent types found. Add some agent types to get started.
        </Typography>
      </Box>
    );
  }

  return (
    <List dense>
      {agentTypes.map((agentType) => (
        <ListItem key={agentType.id} divider>
          <ListItemIcon>
            <RobotIcon color="primary" />
          </ListItemIcon>
          <ListItemText
            primary={
              <Box display="flex" alignItems="center" gap={1}>
                <Typography variant="subtitle2">{agentType.name}</Typography>
                <Chip
                  icon={agentType.is_active ? <ActiveIcon /> : <InactiveIcon />}
                  label={agentType.is_active ? 'Active' : 'Inactive'}
                  size="small"
                  color={agentType.is_active ? 'success' : 'default'}
                  variant="outlined"
                />
              </Box>
            }
            secondary={
              <Box>
                {agentType.description && (
                  <Typography variant="body2" color="textSecondary">
                    {agentType.description}
                  </Typography>
                )}
                {agentType.capabilities && (
                  <Typography variant="caption" color="textSecondary">
                    Capabilities: {Object.keys(agentType.capabilities).length} defined
                  </Typography>
                )}
              </Box>
            }
          />
        </ListItem>
      ))}
    </List>
  );
};

export default AgentTypeList;