import React from 'react';
import {
  Box,
  Typography,
  Button,
  IconButton,
  Tooltip,
} from '@mui/material';
import {
  ArrowBack as BackIcon,
} from '@mui/icons-material';
import { EditButton, SaveCancelButtons } from '../common';

interface ProjectHeaderProps {
  project: any;
  isEditMode: boolean;
  onBack: () => void;
  onToggleEditMode: () => void;
  onCancelEdit?: () => void;
}

const ProjectHeader: React.FC<ProjectHeaderProps> = ({
  project,
  isEditMode,
  onBack,
  onToggleEditMode,
  onCancelEdit,
}) => {
  return (
    <Box display="flex" alignItems="center" gap={2} mb={3}>
      <Button
        startIcon={<BackIcon />}
        onClick={onBack}
        variant="outlined"
      >
        Back to Projects
      </Button>
      <Box flexGrow={1}>
        <Typography variant="h4" component="h1" gutterBottom>
          {project.name}
        </Typography>
        {project.description && (
          <Typography variant="body1" color="text.secondary">
            {project.description}
          </Typography>
        )}
      </Box>
      {isEditMode ? (
        <SaveCancelButtons
          onSave={onToggleEditMode}
          onCancel={onCancelEdit || onToggleEditMode}
          saveLabel="Save Changes"
          cancelLabel="Cancel Changes"
        />
      ) : (
        <EditButton
          onClick={onToggleEditMode}
          tooltip="Edit Project"
          color="primary"
          placement="header"
        />
      )}
    </Box>
  );
};

export default ProjectHeader;