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
  Edit as EditIcon,
  Save as SaveIcon,
  Cancel as CancelIcon,
} from '@mui/icons-material';

interface ProjectHeaderProps {
  project: any;
  isEditMode: boolean;
  onBack: () => void;
  onToggleEditMode: () => void;
}

const ProjectHeader: React.FC<ProjectHeaderProps> = ({
  project,
  isEditMode,
  onBack,
  onToggleEditMode,
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
      <Tooltip title={isEditMode ? "Save Changes" : "Edit Project"}>
        <IconButton
          onClick={onToggleEditMode}
          color={isEditMode ? "success" : "primary"}
          size="large"
        >
          {isEditMode ? <SaveIcon /> : <EditIcon />}
        </IconButton>
      </Tooltip>
    </Box>
  );
};

export default ProjectHeader;