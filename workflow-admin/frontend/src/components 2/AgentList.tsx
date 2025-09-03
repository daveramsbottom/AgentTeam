import React from 'react';
import {
  List,
  Box,
  Typography,
} from '@mui/material';
import { Agent, AgentType } from '../api/agents';
import AgentCard from './AgentCard';

interface AgentListProps {
  agents: Agent[];
  agentTypes: AgentType[];
}

const AgentList: React.FC<AgentListProps> = ({ agents, agentTypes }) => {
  // Create a lookup map for agent types
  const agentTypeMap = agentTypes.reduce((map, type) => {
    map[type.id] = type;
    return map;
  }, {} as { [key: number]: AgentType });

  if (agents.length === 0) {
    return (
      <Box sx={{ p: 2, textAlign: 'center' }}>
        <Typography variant="body2" color="textSecondary">
          No agents found. Create some agents to get started.
        </Typography>
      </Box>
    );
  }

  return (
    <List dense>
      {agents.map((agent) => (
        <AgentCard 
          key={agent.id} 
          agent={agent} 
          agentType={agentTypeMap[agent.agent_type_id]}
        />
      ))}
    </List>
  );
};

export default AgentList;