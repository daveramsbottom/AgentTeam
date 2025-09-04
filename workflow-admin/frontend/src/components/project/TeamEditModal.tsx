import React, { useState, useEffect } from 'react';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  Button,
  Box,
  Typography,
  IconButton,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Checkbox,
  FormControlLabel,
  Paper,
  Stack,
  Chip,
  CircularProgress,
} from '@mui/material';
import {
  Close as CloseIcon,
  Save as SaveIcon,
  Edit as EditIcon,
} from '@mui/icons-material';
import { EditTeamModalProps } from './types';

const TeamEditModal: React.FC<EditTeamModalProps> = ({
  open,
  agents,
  team,
  onClose,
  onSubmit,
  loading,
}) => {
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    team_lead_id: null as number | null,
    member_agent_ids: [] as number[],
  });

  // Populate form when team changes
  useEffect(() => {
    if (team && open) {
      setFormData({
        name: team.name,
        description: team.specialization || '',
        team_lead_id: team.members?.find(m => m.role === 'Team Lead')?.id || null,
        member_agent_ids: team.members?.map(m => m.id) || [],
      });
    }
  }, [team, open]);

  const handleSubmit = async () => {
    if (!formData.name.trim()) return;
    
    await onSubmit(formData);
  };

  if (!team) return null;

  return (
    <Dialog open={open} onClose={onClose} maxWidth="md" fullWidth>
      <DialogTitle sx={{ pb: 1 }}>
        <Box display="flex" alignItems="center" gap={1}>
          <EditIcon color="primary" />
          Edit Team: {team.name}
        </Box>
        <IconButton
          onClick={onClose}
          sx={{ position: 'absolute', right: 8, top: 8 }}
        >
          <CloseIcon />
        </IconButton>
      </DialogTitle>
      <DialogContent dividers>
        <Stack spacing={3}>
          <TextField
            fullWidth
            label="Team Name"
            value={formData.name}
            onChange={(e) => setFormData(prev => ({ ...prev, name: e.target.value }))}
            required
          />
          
          <TextField
            fullWidth
            label="Team Description"
            value={formData.description}
            onChange={(e) => setFormData(prev => ({ ...prev, description: e.target.value }))}
            multiline
            rows={3}
            required
          />

          <FormControl fullWidth>
            <InputLabel>Team Lead (Optional)</InputLabel>
            <Select
              value={formData.team_lead_id || ''}
              onChange={(e) => setFormData(prev => ({ 
                ...prev, 
                team_lead_id: e.target.value ? Number(e.target.value) : null 
              }))}
              label="Team Lead (Optional)"
            >
              <MenuItem value="">
                <em>No team lead</em>
              </MenuItem>
              {agents.map((agent) => (
                <MenuItem key={agent.id} value={agent.id}>
                  {agent.name} - {agent.agent_type?.name || 'Unknown Type'}
                </MenuItem>
              ))}
            </Select>
          </FormControl>

          <Box>
            <Typography variant="subtitle1" gutterBottom>
              Team Members *
            </Typography>
            <Typography variant="body2" color="textSecondary" sx={{ mb: 2 }}>
              Select agents to include in this team. The team lead will automatically be included if selected above.
            </Typography>
            
            <Paper variant="outlined" sx={{ p: 2, maxHeight: 300, overflow: 'auto' }}>
              <Stack spacing={1}>
                {agents.map((agent) => (
                  <FormControlLabel
                    key={agent.id}
                    control={
                      <Checkbox
                        checked={formData.member_agent_ids.includes(agent.id)}
                        onChange={(e) => {
                          setFormData(prev => ({
                            ...prev,
                            member_agent_ids: e.target.checked
                              ? [...prev.member_agent_ids, agent.id]
                              : prev.member_agent_ids.filter(id => id !== agent.id)
                          }));
                        }}
                      />
                    }
                    label={
                      <Box>
                        <Typography variant="body2" fontWeight="medium">
                          {agent.name}
                          {agent.id === formData.team_lead_id && (
                            <Chip 
                              label="Team Lead" 
                              size="small" 
                              color="primary" 
                              sx={{ ml: 1, fontSize: '0.7rem' }} 
                            />
                          )}
                        </Typography>
                        <Typography variant="caption" color="textSecondary">
                          {agent.agent_type?.name || 'Unknown Type'} • {agent.status}
                        </Typography>
                        {agent.description && (
                          <Typography variant="caption" display="block" color="text.primary" sx={{ mt: 0.5 }}>
                            {agent.description}
                          </Typography>
                        )}
                      </Box>
                    }
                  />
                ))}
              </Stack>
            </Paper>
            
            <Typography variant="caption" color="textSecondary" sx={{ mt: 1, display: 'block' }}>
              Selected: {formData.member_agent_ids.length} agent{formData.member_agent_ids.length !== 1 ? 's' : ''}
            </Typography>
          </Box>
        </Stack>
      </DialogContent>
      <DialogActions sx={{ p: 2 }}>
        <Button onClick={onClose} disabled={loading}>
          Cancel
        </Button>
        <Button 
          onClick={handleSubmit} 
          variant="contained"
          disabled={loading || !formData.name.trim()}
          startIcon={loading ? <CircularProgress size={16} /> : <SaveIcon />}
        >
          {loading ? 'Updating...' : 'Update Team'}
        </Button>
      </DialogActions>
    </Dialog>
  );
};

export default TeamEditModal;