import React from 'react';
import { IconButton, Tooltip } from '@mui/material';
import { Delete as DeleteIcon } from '@mui/icons-material';

interface DeleteButtonProps {
  onClick: () => void;
  tooltip?: string;
  size?: 'small' | 'medium' | 'large';
  color?: 'error' | 'default' | 'secondary';
  disabled?: boolean;
}

const DeleteButton: React.FC<DeleteButtonProps> = ({
  onClick,
  tooltip = 'Delete',
  size = 'small',
  color = 'error',
  disabled = false
}) => {
  return (
    <Tooltip title={tooltip}>
      <IconButton
        onClick={onClick}
        color={color}
        size={size}
        disabled={disabled}
      >
        <DeleteIcon />
      </IconButton>
    </Tooltip>
  );
};

export default DeleteButton;