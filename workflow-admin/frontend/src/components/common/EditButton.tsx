import React from 'react';
import { IconButton, Tooltip } from '@mui/material';
import { Edit as EditIcon } from '@mui/icons-material';

interface EditButtonProps {
  onClick: () => void;
  tooltip?: string;
  size?: 'small' | 'medium' | 'large';
  color?: 'primary' | 'secondary' | 'default';
  disabled?: boolean;
  placement?: 'header' | 'inline';
}

const EditButton: React.FC<EditButtonProps> = ({
  onClick,
  tooltip = 'Edit',
  size = 'small',
  color = 'primary',
  disabled = false,
  placement = 'inline'
}) => {
  const buttonStyle = placement === 'header' 
    ? { border: 1, borderColor: `${color}.main` }
    : {};

  return (
    <Tooltip title={tooltip}>
      <IconButton
        onClick={onClick}
        color={color}
        size={size}
        disabled={disabled}
        sx={buttonStyle}
      >
        <EditIcon />
      </IconButton>
    </Tooltip>
  );
};

export default EditButton;