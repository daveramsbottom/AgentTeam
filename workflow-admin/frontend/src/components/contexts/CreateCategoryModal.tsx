import React, { useState } from 'react';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  TextField,
  Box,
  Typography,
  Grid,
  Paper,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Chip,
  Alert,
} from '@mui/material';
import {
  Security as SecurityIcon,
  Code as TechIcon,
  Policy as ComplianceIcon,
  Business as BusinessIcon,
  Category as CategoryIcon,
  Description as ContextIcon,
} from '@mui/icons-material';

interface CreateCategoryModalProps {
  open: boolean;
  onClose: () => void;
  onSubmit: (categoryData: {
    name: string;
    displayName: string;
    description: string;
    color: string;
    icon: string;
  }) => void;
  loading?: boolean;
}

const CreateCategoryModal: React.FC<CreateCategoryModalProps> = ({
  open,
  onClose,
  onSubmit,
  loading = false,
}) => {
  const [formData, setFormData] = useState({
    name: '',
    displayName: '',
    description: '',
    color: '#2196F3',
    icon: 'category',
  });
  const [errors, setErrors] = useState<Record<string, string>>({});

  const colorOptions = [
    { value: '#F44336', label: 'Red', muiColor: 'error' },
    { value: '#2196F3', label: 'Blue', muiColor: 'info' },
    { value: '#FF9800', label: 'Orange', muiColor: 'warning' },
    { value: '#4CAF50', label: 'Green', muiColor: 'success' },
    { value: '#9C27B0', label: 'Purple', muiColor: 'secondary' },
    { value: '#607D8B', label: 'Blue Grey', muiColor: 'default' },
    { value: '#795548', label: 'Brown', muiColor: 'default' },
    { value: '#009688', label: 'Teal', muiColor: 'info' },
  ];

  const iconOptions = [
    { value: 'security', label: 'Security', icon: <SecurityIcon /> },
    { value: 'tech', label: 'Technology', icon: <TechIcon /> },
    { value: 'compliance', label: 'Compliance', icon: <ComplianceIcon /> },
    { value: 'business', label: 'Business', icon: <BusinessIcon /> },
    { value: 'category', label: 'Category', icon: <CategoryIcon /> },
    { value: 'context', label: 'Context', icon: <ContextIcon /> },
  ];

  const handleSubmit = () => {
    const newErrors: Record<string, string> = {};

    if (!formData.name.trim()) {
      newErrors.name = 'Category name is required';
    } else if (!/^[a-z_]+$/.test(formData.name)) {
      newErrors.name = 'Category name must be lowercase with underscores only';
    }

    if (!formData.displayName.trim()) {
      newErrors.displayName = 'Display name is required';
    }

    if (!formData.description.trim()) {
      newErrors.description = 'Description is required';
    }

    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
      return;
    }

    onSubmit(formData);
    handleClose();
  };

  const handleClose = () => {
    setFormData({
      name: '',
      displayName: '',
      description: '',
      color: '#2196F3',
      icon: 'category',
    });
    setErrors({});
    onClose();
  };

  const selectedIconComponent = iconOptions.find(icon => icon.value === formData.icon)?.icon || <CategoryIcon />;

  return (
    <Dialog open={open} onClose={handleClose} maxWidth="md" fullWidth>
      <DialogTitle>Create New Context Category</DialogTitle>
      <DialogContent>
        <Typography variant="body2" color="text.secondary" gutterBottom sx={{ mb: 3 }}>
          Create a new category for organizing contexts. This will define how contexts are grouped and displayed throughout the system.
        </Typography>

        <Grid container spacing={3}>
          <Grid item xs={12} md={6}>
            <TextField
              autoFocus
              label="Category Name"
              fullWidth
              value={formData.name}
              onChange={(e) => {
                const value = e.target.value.toLowerCase().replace(/[^a-z_]/g, '');
                setFormData({ ...formData, name: value });
                if (errors.name) setErrors({ ...errors, name: '' });
              }}
              error={!!errors.name}
              helperText={errors.name || 'Lowercase with underscores only (e.g., "data_governance")'}
              sx={{ mb: 2 }}
            />

            <TextField
              label="Display Name"
              fullWidth
              value={formData.displayName}
              onChange={(e) => {
                setFormData({ ...formData, displayName: e.target.value });
                if (errors.displayName) setErrors({ ...errors, displayName: '' });
              }}
              error={!!errors.displayName}
              helperText={errors.displayName || 'Human-readable name (e.g., "Data Governance")'}
              sx={{ mb: 2 }}
            />

            <TextField
              label="Description"
              fullWidth
              multiline
              rows={3}
              value={formData.description}
              onChange={(e) => {
                setFormData({ ...formData, description: e.target.value });
                if (errors.description) setErrors({ ...errors, description: '' });
              }}
              error={!!errors.description}
              helperText={errors.description || 'Brief description of what this category contains'}
              sx={{ mb: 2 }}
            />

            <FormControl fullWidth>
              <InputLabel>Icon</InputLabel>
              <Select
                value={formData.icon}
                onChange={(e) => setFormData({ ...formData, icon: e.target.value })}
                label="Icon"
              >
                {iconOptions.map((option) => (
                  <MenuItem key={option.value} value={option.value}>
                    <Box display="flex" alignItems="center" gap={1}>
                      {option.icon}
                      {option.label}
                    </Box>
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
          </Grid>

          <Grid item xs={12} md={6}>
            <Typography variant="subtitle2" gutterBottom>
              Category Color
            </Typography>
            <Grid container spacing={1} sx={{ mb: 3 }}>
              {colorOptions.map((option) => (
                <Grid item xs={3} key={option.value}>
                  <Paper
                    elevation={formData.color === option.value ? 4 : 1}
                    sx={{
                      p: 2,
                      textAlign: 'center',
                      cursor: 'pointer',
                      backgroundColor: option.value + '20',
                      border: formData.color === option.value ? `2px solid ${option.value}` : '1px solid transparent',
                      transition: 'all 0.2s ease-in-out',
                      '&:hover': {
                        elevation: 3,
                        transform: 'scale(1.05)',
                      }
                    }}
                    onClick={() => setFormData({ ...formData, color: option.value })}
                  >
                    <Box
                      sx={{
                        width: 24,
                        height: 24,
                        backgroundColor: option.value,
                        borderRadius: '50%',
                        mx: 'auto',
                        mb: 1,
                      }}
                    />
                    <Typography variant="caption" display="block">
                      {option.label}
                    </Typography>
                  </Paper>
                </Grid>
              ))}
            </Grid>

            <Typography variant="subtitle2" gutterBottom>
              Preview
            </Typography>
            <Paper variant="outlined" sx={{ p: 2, textAlign: 'center' }}>
              <Box display="flex" alignItems="center" justifyContent="center" gap={1} mb={1}>
                <Box sx={{ color: formData.color }}>
                  {selectedIconComponent}
                </Box>
                <Typography variant="h6" sx={{ color: formData.color }}>
                  {formData.displayName || 'Category Name'}
                </Typography>
              </Box>
              <Typography variant="body2" color="text.secondary" gutterBottom>
                {formData.description || 'Category description will appear here'}
              </Typography>
              <Chip
                label={`Example Context`}
                size="small"
                variant="outlined"
                sx={{
                  borderColor: formData.color,
                  color: formData.color,
                }}
              />
            </Paper>
          </Grid>
        </Grid>

        <Alert severity="info" sx={{ mt: 2 }}>
          <Typography variant="body2">
            <strong>Note:</strong> Once created, the category name cannot be changed, but display name, description, color, and icon can be updated later.
          </Typography>
        </Alert>
      </DialogContent>
      <DialogActions>
        <Button onClick={handleClose} disabled={loading}>
          Cancel
        </Button>
        <Button onClick={handleSubmit} variant="contained" disabled={loading}>
          {loading ? 'Creating...' : 'Create Category'}
        </Button>
      </DialogActions>
    </Dialog>
  );
};

export default CreateCategoryModal;