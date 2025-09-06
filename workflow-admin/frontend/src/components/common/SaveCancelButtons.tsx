import React from 'react';
import { Box, Button, CircularProgress } from '@mui/material';
import { Save as SaveIcon, Cancel as CancelIcon } from '@mui/icons-material';

interface SaveCancelButtonsProps {
  onSave: () => void;
  onCancel: () => void;
  saveText?: string;
  cancelText?: string;
  loading?: boolean;
  saveDisabled?: boolean;
  variant?: 'contained' | 'outlined' | 'text';
  size?: 'small' | 'medium' | 'large';
  direction?: 'row' | 'column';
}

const SaveCancelButtons: React.FC<SaveCancelButtonsProps> = ({
  onSave,
  onCancel,
  saveText = 'Save',
  cancelText = 'Cancel',
  loading = false,
  saveDisabled = false,
  variant = 'contained',
  size = 'small',
  direction = 'row'
}) => {
  return (
    <Box display="flex" flexDirection={direction} gap={1}>
      <Button
        onClick={onSave}
        variant={variant}
        color="primary"
        size={size}
        disabled={loading || saveDisabled}
        startIcon={loading ? <CircularProgress size={16} /> : <SaveIcon />}
      >
        {saveText}
      </Button>
      <Button
        onClick={onCancel}
        variant="outlined"
        color="secondary"
        size={size}
        disabled={loading}
        startIcon={<CancelIcon />}
      >
        {cancelText}
      </Button>
    </Box>
  );
};

export default SaveCancelButtons;