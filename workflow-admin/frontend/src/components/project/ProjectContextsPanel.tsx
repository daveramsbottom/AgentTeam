import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Paper,
  Card,
  CardContent,
  Chip,
  Button,
  IconButton,
  Divider,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  ListItemSecondaryAction,
  Collapse,
  Alert,
  CircularProgress,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Checkbox,
  FormControlLabel,
} from '@mui/material';
import {
  Description as ContextIcon,
  Add as AddIcon,
  Remove as RemoveIcon,
  ExpandLess as ExpandLessIcon,
  ExpandMore as ExpandMoreIcon,
  Security as SecurityIcon,
  Code as TechIcon,
  Policy as ComplianceIcon,
  Business as BusinessIcon,
} from '@mui/icons-material';
import { contextsApi } from '../../api/contexts';
import { 
  getCategoryColor, 
  getCategoryMuiColor, 
  getCategoryDisplayName, 
  updateCategoryColorsFromContexts 
} from '../../utils/categoryColors';

interface ProjectContextsPanelProps {
  project: any;
  isEditMode: boolean;
  onContextsUpdate?: (contexts: any[]) => void;
}

interface OrganizationalContext {
  id: number;
  category: string;
  name: string;
  description?: string;
  content: any;
  applies_to?: string[];
  priority: number;
  is_active: boolean;
}

const ProjectContextsPanel: React.FC<ProjectContextsPanelProps> = ({
  project,
  isEditMode,
  onContextsUpdate,
}) => {
  const [availableContexts, setAvailableContexts] = useState<OrganizationalContext[]>([]);
  const [selectedContexts, setSelectedContexts] = useState<OrganizationalContext[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [addModalOpen, setAddModalOpen] = useState(false);
  const [expandedCategories, setExpandedCategories] = useState<Set<string>>(new Set(['tech_standards']));

  useEffect(() => {
    loadAvailableContexts();
  }, []);

  const loadAvailableContexts = async () => {
    try {
      setLoading(true);
      // Use regular contexts endpoint since the selectable one has issues
      const response = await fetch(`${import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'}/api/v1/contexts/`);
      const contexts = await response.json();
      
      // Update color cache with context UI settings
      updateCategoryColorsFromContexts(contexts);
      
      setAvailableContexts(contexts);
    } catch (err) {
      console.error('Error loading contexts:', err);
      setError('Failed to load available contexts');
    } finally {
      setLoading(false);
    }
  };

  const getCategoryIcon = (category: string) => {
    switch (category) {
      case 'security': return <SecurityIcon fontSize="small" />;
      case 'tech_standards': return <TechIcon fontSize="small" />;
      case 'compliance': return <ComplianceIcon fontSize="small" />;
      case 'business_guidelines': return <BusinessIcon fontSize="small" />;
      default: return <ContextIcon fontSize="small" />;
    }
  };

  // Using centralized color utility functions

  const toggleCategory = (category: string) => {
    setExpandedCategories(prev => {
      const newSet = new Set(prev);
      if (newSet.has(category)) {
        newSet.delete(category);
      } else {
        newSet.add(category);
      }
      return newSet;
    });
  };

  const addContext = (context: OrganizationalContext) => {
    if (!selectedContexts.find(c => c.id === context.id)) {
      const updated = [...selectedContexts, context];
      setSelectedContexts(updated);
      onContextsUpdate?.(updated);
    }
    setAddModalOpen(false);
  };

  const removeContext = (contextId: number) => {
    const updated = selectedContexts.filter(c => c.id !== contextId);
    setSelectedContexts(updated);
    onContextsUpdate?.(updated);
  };

  const groupedAvailableContexts = availableContexts.reduce((acc, context) => {
    if (!acc[context.category]) {
      acc[context.category] = [];
    }
    acc[context.category].push(context);
    return acc;
  }, {} as Record<string, OrganizationalContext[]>);

  // Using centralized display name function

  if (loading && availableContexts.length === 0) {
    return (
      <Paper sx={{ p: 3 }}>
        <Box display="flex" alignItems="center" gap={1} mb={2}>
          <ContextIcon color="primary" />
          <Typography variant="h6" color="primary">
            Project Contexts
          </Typography>
        </Box>
        <Box display="flex" justifyContent="center" p={3}>
          <CircularProgress size={40} />
        </Box>
      </Paper>
    );
  }

  return (
    <Paper sx={{ p: 3, height: 'fit-content', minHeight: '400px' }}>
      <Box display="flex" alignItems="center" justifyContent="space-between" mb={2}>
        <Box display="flex" alignItems="center" gap={1}>
          <ContextIcon color="primary" />
          <Typography variant="h6" color="primary">
            Project Contexts
          </Typography>
        </Box>
        {isEditMode && (
          <Button
            startIcon={<AddIcon />}
            onClick={() => setAddModalOpen(true)}
            size="small"
            variant="contained"
            sx={{
              backgroundColor: '#1976d2',
              color: 'white',
              boxShadow: 3,
              '&:hover': {
                backgroundColor: '#1565c0',
                boxShadow: 6
              }
            }}
          >
            Add Context
          </Button>
        )}
      </Box>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}

      <Typography variant="body2" color="text.secondary" gutterBottom>
        Organizational contexts define standards, guidelines, and requirements that apply to this project.
      </Typography>

      <Divider sx={{ my: 2 }} />

      {selectedContexts.length === 0 ? (
        <Box textAlign="center" py={3}>
          <Typography variant="body2" color="text.secondary">
            No contexts selected for this project
          </Typography>
          {isEditMode && (
            <Button
              startIcon={<AddIcon />}
              onClick={() => setAddModalOpen(true)}
              sx={{ 
                mt: 1,
                backgroundColor: '#1976d2',
                color: 'white',
                boxShadow: 3,
                '&:hover': {
                  backgroundColor: '#1565c0',
                  boxShadow: 6
                }
              }}
              size="small"
              variant="contained"
            >
              Add First Context
            </Button>
          )}
        </Box>
      ) : (
        <List dense>
          {selectedContexts.map((context) => (
            <ListItem key={context.id} divider>
              <ListItemIcon>
                {getCategoryIcon(context.category)}
              </ListItemIcon>
              <ListItemText
                primary={context.name}
                secondary={
                  <Box display="flex" alignItems="center" gap={1} mt={0.5}>
                    <Chip
                      label={getCategoryDisplayName(context.category, availableContexts)}
                      size="small"
                      color={getCategoryMuiColor(context.category) as any}
                      variant="outlined"
                    />
                    {context.description && (
                      <Typography variant="caption" color="text.secondary">
                        {context.description.substring(0, 80)}...
                      </Typography>
                    )}
                  </Box>
                }
              />
              {isEditMode && (
                <ListItemSecondaryAction>
                  <IconButton
                    edge="end"
                    onClick={() => removeContext(context.id)}
                    size="small"
                    color="error"
                  >
                    <RemoveIcon />
                  </IconButton>
                </ListItemSecondaryAction>
              )}
            </ListItem>
          ))}
        </List>
      )}

      {/* Add Context Dialog */}
      <Dialog
        open={addModalOpen}
        onClose={() => setAddModalOpen(false)}
        maxWidth="md"
        fullWidth
      >
        <DialogTitle>Add Organizational Context</DialogTitle>
        <DialogContent>
          <Typography variant="body2" color="text.secondary" gutterBottom>
            Select contexts that should apply to this project. These define standards, guidelines, and requirements for the project team.
          </Typography>
          
          <Box mt={2}>
            {Object.entries(groupedAvailableContexts).map(([category, contexts]) => (
              <Card key={category} sx={{ mb: 2 }} variant="outlined">
                <CardContent sx={{ pb: 1 }}>
                  <Box
                    display="flex"
                    alignItems="center"
                    sx={{ cursor: 'pointer' }}
                    onClick={() => toggleCategory(category)}
                  >
                    {getCategoryIcon(category)}
                    <Typography variant="subtitle1" sx={{ ml: 1, flexGrow: 1 }}>
                      {getCategoryDisplayName(category, availableContexts)} ({contexts.length})
                    </Typography>
                    {expandedCategories.has(category) ? <ExpandLessIcon /> : <ExpandMoreIcon />}
                  </Box>
                  
                  <Collapse in={expandedCategories.has(category)}>
                    <List dense>
                      {contexts.map((context) => {
                        const isSelected = selectedContexts.find(c => c.id === context.id);
                        return (
                          <ListItem
                            key={context.id}
                            button
                            onClick={() => !isSelected && addContext(context)}
                            disabled={!!isSelected}
                          >
                            <ListItemIcon>
                              <FormControlLabel
                                control={
                                  <Checkbox
                                    checked={!!isSelected}
                                    disabled={!!isSelected}
                                  />
                                }
                                label=""
                              />
                            </ListItemIcon>
                            <ListItemText
                              primary={context.name}
                              secondary={context.description}
                            />
                          </ListItem>
                        );
                      })}
                    </List>
                  </Collapse>
                </CardContent>
              </Card>
            ))}
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setAddModalOpen(false)}>
            Done
          </Button>
        </DialogActions>
      </Dialog>
    </Paper>
  );
};

export default ProjectContextsPanel;