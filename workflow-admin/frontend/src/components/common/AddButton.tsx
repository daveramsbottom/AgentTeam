import React from 'react';
import { IconButton, Tooltip, Button } from '@mui/material';
import { Add as AddIcon } from '@mui/icons-material';

interface AddButtonProps {
  onClick: () => void;
  tooltip?: string;
  text?: string;
  variant?: 'icon' | 'button';
  size?: 'small' | 'medium' | 'large';
  color?: 'primary' | 'secondary' | 'default';
  disabled?: boolean;
  fullWidth?: boolean;
}

const AddButton: React.FC<AddButtonProps> = ({
  onClick,
  tooltip = 'Add',
  text = 'Add',
  variant = 'icon',
  size = 'small',
  color = 'primary',
  disabled = false,
  fullWidth = false
}) => {
  if (variant === 'button') {
    return (
      <Button
        onClick={onClick}
        color={color}
        size={size}
        disabled={disabled}
        fullWidth={fullWidth}
        startIcon={<AddIcon />}
        variant="outlined"
      >
        {text}
      </Button>
    );
  }

  return (
    <Tooltip title={tooltip}>
      <IconButton
        onClick={onClick}
        color={color}
        size={size}
        disabled={disabled}
      >
        <AddIcon />
      </IconButton>
    </Tooltip>
  );
};

export default AddButton;