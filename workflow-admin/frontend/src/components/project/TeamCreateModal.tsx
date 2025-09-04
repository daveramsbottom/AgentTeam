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
  Alert,
  Chip,
  CircularProgress,
} from '@mui/material';
import {
  Close as CloseIcon,
  PersonAdd as PersonAddIcon,
} from '@mui/icons-material';
import { TeamModalProps } from './types';

const TeamCreateModal: React.FC<TeamModalProps> = ({
  open,
  agents,
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
  const [formErrors, setFormErrors] = useState<Record<string, string>>({});

  // Reset form when modal opens/closes
  useEffect(() => {
    if (open) {
      setFormData({
        name: '',
        description: '',
        team_lead_id: null,
        member_agent_ids: [],
      });
      setFormErrors({});
    }
  }, [open]);

  const handleFormChange = (field: string, value: any) => {
    setFormData(prev => ({ ...prev, [field]: value }));
    
    // Clear error when user starts typing
    if (formErrors[field]) {
      setFormErrors(prev => ({ ...prev, [field]: '' }));
    }

    // Auto-include team lead in members if selected
    if (field === 'team_lead_id' && value && !formData.member_agent_ids.includes(value)) {
      setFormData(prev => ({
        ...prev,
        [field]: value,
        member_agent_ids: [...prev.member_agent_ids, value]
      }));
    }
  };

  const handleAgentSelection = (agentId: number, checked: boolean) => {
    setFormData(prev => ({
      ...prev,
      member_agent_ids: checked
        ? [...prev.member_agent_ids, agentId]
        : prev.member_agent_ids.filter(id => id !== agentId)
    }));
  };

  const validateForm = (): boolean => {
    const errors: Record<string, string> = {};
    
    if (!formData.name.trim()) {
      errors.name = 'Team name is required';
    }
    if (!formData.description.trim()) {
      errors.description = 'Team description is required';
    }
    if (formData.member_agent_ids.length === 0) {
      errors.members = 'At least one team member must be selected';
    }
    
    setFormErrors(errors);
    return Object.keys(errors).length === 0;
  };

  const handleSubmit = async () => {
    if (!validateForm()) return;
    
    await onSubmit(formData);
  };

  return (
    <Dialog open={open} onClose={onClose} maxWidth="md" fullWidth>
      <DialogTitle sx={{ pb: 1 }}>
        <Box display="flex" alignItems="center" gap={1}>
          <PersonAddIcon color="primary" />
          Create New Team
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
            onChange={(e) => handleFormChange('name', e.target.value)}
            error={!!formErrors.name}
            helperText={formErrors.name}
            required
          />
          
          <TextField
            fullWidth
            label="Team Description"
            value={formData.description}
            onChange={(e) => handleFormChange('description', e.target.value)}
            error={!!formErrors.description}
            helperText={formErrors.description}
            multiline
            rows={3}
            required
          />

          <FormControl fullWidth>
            <InputLabel>Team Lead (Optional)</InputLabel>
            <Select
              value={formData.team_lead_id || ''}
              onChange={(e) => handleFormChange('team_lead_id', e.target.value ? Number(e.target.value) : null)}
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
            
            {formErrors.members && (
              <Alert severity="error" sx={{ mb: 2 }}>
                {formErrors.members}
              </Alert>
            )}
            
            <Paper variant="outlined" sx={{ p: 2, maxHeight: 300, overflow: 'auto' }}>
              <Stack spacing={1}>
                {agents.map((agent) => (
                  <FormControlLabel
                    key={agent.id}
                    control={
                      <Checkbox
                        checked={formData.member_agent_ids.includes(agent.id)}
                        onChange={(e) => handleAgentSelection(agent.id, e.target.checked)}
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
          disabled={loading}
          startIcon={loading ? <CircularProgress size={16} /> : <PersonAddIcon />}
        >
          {loading ? 'Creating...' : 'Create Team'}
        </Button>
      </DialogActions>
    </Dialog>
  );
};

export default TeamCreateModal;