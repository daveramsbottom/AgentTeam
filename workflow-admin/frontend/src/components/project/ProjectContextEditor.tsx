import React from 'react';
import {
  Box,
  Typography,
  Paper,
  IconButton,
  TextField,
  Button,
  Tooltip,
} from '@mui/material';
import {
  EditNote as EditNoteIcon,
  Save as SaveIcon,
  Cancel as CancelIcon,
} from '@mui/icons-material';
import { ProjectContextEditorProps } from './types';

const ProjectContextEditor: React.FC<ProjectContextEditorProps> = ({
  project,
  isEditMode,
  editingContext,
  tempContext,
  onStartEditing,
  onSaveContext,
  onCancelEditing,
  onContextChange,
}) => {
  return (
    <Paper elevation={1} sx={{ p: 3, mb: 3 }}>
      <Box display="flex" justifyContent="space-between" alignItems="flex-start" mb={2}>
        <Typography variant="h6">Project Context</Typography>
        {isEditMode && !editingContext && (
          <Tooltip title="Edit context">
            <IconButton
              size="small"
              onClick={onStartEditing}
              sx={{
                color: 'primary.main',
                '&:hover': { backgroundColor: 'primary.light' }
              }}
            >
              <EditNoteIcon />
            </IconButton>
          </Tooltip>
        )}
      </Box>

      <Box sx={{ position: 'relative' }}>
        {editingContext ? (
          <Box>
            <TextField
              fullWidth
              multiline
              rows={8}
              value={tempContext}
              onChange={(e) => onContextChange(e.target.value)}
              placeholder="Enter project context, guidelines, requirements..."
              variant="outlined"
              sx={{ mb: 2 }}
            />
            <Box display="flex" gap={1} justifyContent="flex-end">
              <Button
                startIcon={<SaveIcon />}
                variant="contained"
                size="small"
                onClick={onSaveContext}
              >
                Save
              </Button>
              <Button
                startIcon={<CancelIcon />}
                variant="outlined"
                size="small"
                onClick={onCancelEditing}
              >
                Cancel
              </Button>
            </Box>
          </Box>
        ) : (
          <Typography variant="body2" color="text.primary" sx={{ 
            fontStyle: 'italic', 
            backgroundColor: project.context ? 'grey.50' : 'grey.100', 
            p: 2, 
            borderRadius: 1,
            border: '1px solid',
            borderColor: project.context ? 'grey.200' : 'grey.300',
            ...(isEditMode && {
              backgroundColor: 'warning.light',
              borderColor: 'warning.main',
            })
          }}>
            {project.context || 'No project context set. Click the edit icon to add context.'}
          </Typography>
        )}
      </Box>

      <Box sx={{ mt: 2 }}>
        <Typography variant="body2" color="textSecondary">
          <strong>Created:</strong> {new Date(project.created_at).toLocaleDateString()}
        </Typography>
        {project.updated_at && (
          <Typography variant="body2" color="textSecondary">
            <strong>Last Updated:</strong> {new Date(project.updated_at).toLocaleDateString()}
          </Typography>
        )}
      </Box>
    </Paper>
  );
};

export default ProjectContextEditor;