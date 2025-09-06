import React, { useState, useEffect } from 'react';
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
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Chip,
  Alert,
  Switch,
  FormControlLabel,
  Slider,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  IconButton,
  Tooltip,
} from '@mui/material';
import {
  ExpandMore as ExpandMoreIcon,
  Add as AddIcon,
  Remove as RemoveIcon,
} from '@mui/icons-material';
import { OrganizationalContext, UpdateContextRequest } from '../../api/contexts';
import { getCategoryColor } from '../../utils/categoryColors';

interface EditContextModalProps {
  open: boolean;
  onClose: () => void;
  onSubmit: (id: number, contextData: UpdateContextRequest) => void;
  context: OrganizationalContext | null;
  loading?: boolean;
}

const EditContextModal: React.FC<EditContextModalProps> = ({
  open,
  onClose,
  onSubmit,
  context,
  loading = false,
}) => {
  const [formData, setFormData] = useState<UpdateContextRequest>({
    name: '',
    description: '',
    content: {},
    applies_to: [],
    priority: 5,
    is_active: true,
  });
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [newTag, setNewTag] = useState('');
  const [tags, setTags] = useState<string[]>([]);

  useEffect(() => {
    if (context && open) {
      setFormData({
        name: context.name || '',
        description: context.description || '',
        content: context.content || {},
        applies_to: context.applies_to || [],
        priority: context.priority || 5,
        is_active: context.is_active ?? true,
      });
      setTags(context.tags || []);
    }
  }, [context, open]);

  // Using centralized color utility function

  const handleSubmit = () => {
    if (!context) return;

    const newErrors: Record<string, string> = {};

    if (!formData.name?.trim()) {
      newErrors.name = 'Context name is required';
    }

    if (!formData.description?.trim()) {
      newErrors.description = 'Description is required';
    }

    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
      return;
    }

    // Include tags in content
    const updatedContent = {
      ...formData.content,
      tags: tags
    };

    onSubmit(context.id, {
      ...formData,
      content: updatedContent
    });
    handleClose();
  };

  const handleClose = () => {
    setFormData({
      name: '',
      description: '',
      content: {},
      applies_to: [],
      priority: 5,
      is_active: true,
    });
    setTags([]);
    setErrors({});
    setNewTag('');
    onClose();
  };

  const handleAddTag = () => {
    if (newTag.trim() && !tags.includes(newTag.trim())) {
      setTags([...tags, newTag.trim()]);
      setNewTag('');
    }
  };

  const handleRemoveTag = (tagToRemove: string) => {
    setTags(tags.filter(tag => tag !== tagToRemove));
  };

  const handleContentChange = (key: string, value: any) => {
    setFormData({
      ...formData,
      content: {
        ...formData.content,
        [key]: value
      }
    });
  };

  const addContentField = () => {
    const newKey = `custom_field_${Object.keys(formData.content || {}).length + 1}`;
    handleContentChange(newKey, '');
  };

  const removeContentField = (keyToRemove: string) => {
    const newContent = { ...formData.content };
    delete newContent[keyToRemove];
    setFormData({ ...formData, content: newContent });
  };

  if (!context) return null;

  return (
    <Dialog open={open} onClose={handleClose} maxWidth="md" fullWidth>
      <DialogTitle>
        <Box display="flex" alignItems="center" gap={1}>
          <Typography variant="h6">Edit Context</Typography>
          <Chip
            label={context.category.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())}
            size="small"
            sx={{
              backgroundColor: getCategoryColor(context.category) + '20',
              color: getCategoryColor(context.category),
              fontWeight: 'medium'
            }}
          />
        </Box>
      </DialogTitle>
      <DialogContent>
        <Grid container spacing={3}>
          <Grid item xs={12} md={6}>
            <TextField
              autoFocus
              label="Context Name"
              fullWidth
              value={formData.name}
              onChange={(e) => {
                setFormData({ ...formData, name: e.target.value });
                if (errors.name) setErrors({ ...errors, name: '' });
              }}
              error={!!errors.name}
              helperText={errors.name}
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
              helperText={errors.description}
              sx={{ mb: 2 }}
            />

            <Box sx={{ mb: 2 }}>
              <Typography variant="subtitle2" gutterBottom>
                Priority Level
              </Typography>
              <Slider
                value={formData.priority || 5}
                onChange={(_, value) => setFormData({ ...formData, priority: value as number })}
                min={1}
                max={10}
                step={1}
                marks
                valueLabelDisplay="auto"
                sx={{ color: getCategoryColor(context.category) }}
              />
              <Typography variant="caption" color="text.secondary">
                Higher priority contexts are shown first
              </Typography>
            </Box>

            <FormControlLabel
              control={
                <Switch
                  checked={formData.is_active ?? true}
                  onChange={(e) => setFormData({ ...formData, is_active: e.target.checked })}
                  color="primary"
                />
              }
              label="Active"
              sx={{ mb: 2 }}
            />
          </Grid>

          <Grid item xs={12} md={6}>
            <Typography variant="subtitle2" gutterBottom>
              Tags
            </Typography>
            <Box display="flex" flexWrap="wrap" gap={1} mb={2}>
              {tags.map((tag, index) => (
                <Chip
                  key={index}
                  label={tag}
                  size="small"
                  variant="outlined"
                  onDelete={() => handleRemoveTag(tag)}
                  sx={{
                    borderColor: getCategoryColor(context.category),
                    color: getCategoryColor(context.category),
                  }}
                />
              ))}
            </Box>
            <Box display="flex" gap={1} mb={3}>
              <TextField
                size="small"
                placeholder="Add tag"
                value={newTag}
                onChange={(e) => setNewTag(e.target.value)}
                onKeyPress={(e) => {
                  if (e.key === 'Enter') {
                    e.preventDefault();
                    handleAddTag();
                  }
                }}
              />
              <Button
                variant="outlined"
                size="small"
                onClick={handleAddTag}
                disabled={!newTag.trim()}
              >
                Add
              </Button>
            </Box>

            <Typography variant="subtitle2" gutterBottom>
              Applies To (Scopes)
            </Typography>
            <TextField
              fullWidth
              size="small"
              placeholder="e.g., frontend, backend, mobile"
              value={formData.applies_to?.join(', ') || ''}
              onChange={(e) => {
                const scopes = e.target.value.split(',').map(s => s.trim()).filter(s => s);
                setFormData({ ...formData, applies_to: scopes });
              }}
              helperText="Comma-separated list of scopes where this context applies"
            />
          </Grid>

          <Grid item xs={12}>
            <Accordion>
              <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                <Typography variant="subtitle2">
                  Content Details
                </Typography>
              </AccordionSummary>
              <AccordionDetails>
                <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
                  <Typography variant="body2" color="text.secondary">
                    Customize the detailed content for this context
                  </Typography>
                  <Button
                    startIcon={<AddIcon />}
                    size="small"
                    onClick={addContentField}
                  >
                    Add Field
                  </Button>
                </Box>
                
                {Object.entries(formData.content || {}).map(([key, value]) => (
                  <Box key={key} display="flex" alignItems="center" gap={1} mb={2}>
                    <TextField
                      size="small"
                      label="Field Name"
                      value={key}
                      onChange={(e) => {
                        const newContent = { ...formData.content };
                        delete newContent[key];
                        newContent[e.target.value] = value;
                        setFormData({ ...formData, content: newContent });
                      }}
                      sx={{ minWidth: 150 }}
                    />
                    <TextField
                      size="small"
                      label="Value"
                      fullWidth
                      multiline
                      value={typeof value === 'string' ? value : JSON.stringify(value)}
                      onChange={(e) => handleContentChange(key, e.target.value)}
                    />
                    <Tooltip title="Remove field">
                      <IconButton
                        size="small"
                        onClick={() => removeContentField(key)}
                        color="error"
                      >
                        <RemoveIcon />
                      </IconButton>
                    </Tooltip>
                  </Box>
                ))}
                
                {Object.keys(formData.content || {}).length === 0 && (
                  <Alert severity="info">
                    No content fields defined. Click "Add Field" to add custom content.
                  </Alert>
                )}
              </AccordionDetails>
            </Accordion>
          </Grid>
        </Grid>
      </DialogContent>
      <DialogActions>
        <Button onClick={handleClose} disabled={loading}>
          Cancel
        </Button>
        <Button onClick={handleSubmit} variant="contained" disabled={loading}>
          {loading ? 'Saving...' : 'Save Changes'}
        </Button>
      </DialogActions>
    </Dialog>
  );
};

export default EditContextModal;