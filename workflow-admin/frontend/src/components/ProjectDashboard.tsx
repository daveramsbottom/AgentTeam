import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Box,
  Typography,
  Paper,
  Grid,
  Alert,
  CircularProgress,
  Chip,
  Card,
  CardContent,
  Button,
  IconButton,
  Menu,
  MenuItem,
  Divider,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  FormControl,
  InputLabel,
  Select,
  Stack,
  FormControlLabel,
  Checkbox,
  Accordion,
  AccordionSummary,
  AccordionDetails,
} from '@mui/material';
import {
  Folder as ProjectIcon,
  Add as AddIcon,
  Settings as SettingsIcon,
  MoreVert as MoreVertIcon,
  Close as CloseIcon,
  ExpandMore as ExpandMoreIcon,
} from '@mui/icons-material';
import { Project, CreateProjectRequest, projectsApi } from '../api/projects';
import { contextsApi, GroupedContexts, OrganizationalContext } from '../api/contexts';

interface CreateProjectFormData {
  name: string;
  description: string;
  context: string;
  priority: 'low' | 'medium' | 'high' | 'critical';
  settings: {
    tech_stack: string[];
    timeline: string;
  };
  selected_contexts: number[]; // Array of context IDs
}

const ProjectDashboard: React.FC = () => {
  const navigate = useNavigate();
  const [projects, setProjects] = useState<Project[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  
  // Contexts state
  const [availableContexts, setAvailableContexts] = useState<GroupedContexts>({});
  const [contextsLoading, setContextsLoading] = useState(false);
  const [contextLookup, setContextLookup] = useState<Map<number, OrganizationalContext>>(new Map());
  
  // Action menu state
  const [actionMenuAnchor, setActionMenuAnchor] = useState<null | HTMLElement>(null);
  
  // Create project modal state
  const [createModalOpen, setCreateModalOpen] = useState(false);
  const [formData, setFormData] = useState<CreateProjectFormData>({
    name: '',
    description: '',
    context: '',
    priority: 'medium',
    settings: {
      tech_stack: [],
      timeline: '',
    },
    selected_contexts: [],
  });
  const [formErrors, setFormErrors] = useState<Record<string, string>>({});
  const [creating, setCreating] = useState(false);

  useEffect(() => {
    loadData();
    loadContexts(); // Load contexts for project display
  }, []);

  const loadData = async () => {
    try {
      setLoading(true);
      setError(null);
      const projectsData = await projectsApi.getProjects();
      setProjects(projectsData);
    } catch (err) {
      console.error('Error loading project data:', err);
      setError('Failed to load project data.');
    } finally {
      setLoading(false);
    }
  };

  const loadContexts = async () => {
    try {
      setContextsLoading(true);
      const contextsData = await contextsApi.getSelectableProjectContexts();
      setAvailableContexts(contextsData);
      
      // Create lookup map for easy access
      const lookup = new Map<number, OrganizationalContext>();
      Object.values(contextsData).flat().forEach(context => {
        lookup.set(context.id, context);
      });
      setContextLookup(lookup);
    } catch (err) {
      console.error('Error loading contexts:', err);
      // Don't set error state as contexts are not critical
    } finally {
      setContextsLoading(false);
    }
  };

  // Action menu handlers
  const handleActionMenuOpen = (event: React.MouseEvent<HTMLButtonElement>) => {
    setActionMenuAnchor(event.currentTarget);
  };

  const handleActionMenuClose = () => {
    setActionMenuAnchor(null);
  };

  const handleCreateProject = () => {
    setCreateModalOpen(true);
    handleActionMenuClose();
    loadContexts(); // Load contexts when modal opens
  };

  const handleConfigure = () => {
    // TODO: Implement configure functionality
    console.log('Configure clicked - to be implemented later');
    handleActionMenuClose();
  };

  // Create project modal handlers
  const handleModalClose = () => {
    setCreateModalOpen(false);
    setFormData({
      name: '',
      description: '',
      context: '',
      priority: 'medium',
      settings: {
        tech_stack: [],
        timeline: '',
      },
      selected_contexts: [],
    });
    setFormErrors({});
  };

  const handleFormChange = (field: string, value: any) => {
    if (field.includes('.')) {
      const [parent, child] = field.split('.');
      setFormData(prev => ({
        ...prev,
        [parent]: {
          ...(prev[parent as keyof typeof prev] as object),
          [child]: value,
        },
      }));
    } else {
      setFormData(prev => ({
        ...prev,
        [field]: value,
      }));
    }
    
    // Clear error for this field
    if (formErrors[field]) {
      setFormErrors(prev => {
        const newErrors = { ...prev };
        delete newErrors[field];
        return newErrors;
      });
    }
  };

  const handleContextToggle = (contextId: number, checked: boolean) => {
    setFormData(prev => ({
      ...prev,
      selected_contexts: checked 
        ? [...prev.selected_contexts, contextId]
        : prev.selected_contexts.filter(id => id !== contextId)
    }));
  };

  const validateForm = (): boolean => {
    const errors: Record<string, string> = {};
    
    if (!formData.name.trim()) {
      errors.name = 'Project name is required';
    } else if (formData.name.length < 3) {
      errors.name = 'Project name must be at least 3 characters';
    }
    
    if (!formData.description.trim()) {
      errors.description = 'Project description is required';
    }
    
    if (!formData.context.trim()) {
      errors.context = 'Project context is required';
    }
    
    if (!formData.settings.timeline.trim()) {
      errors['settings.timeline'] = 'Timeline is required';
    }
    
    setFormErrors(errors);
    return Object.keys(errors).length === 0;
  };

  const handleSubmit = async () => {
    if (!validateForm()) {
      return;
    }
    
    setCreating(true);
    try {
      const newProject = await projectsApi.createProject({
        name: formData.name,
        description: formData.description,
        context: formData.context,
        settings: {
          priority: formData.priority,
          tech_stack: formData.settings.tech_stack,
          timeline: formData.settings.timeline,
        },
        selected_contexts: formData.selected_contexts,
      });
      
      // Add the new project to the list
      setProjects(prev => [newProject, ...prev]);
      handleModalClose();
    } catch (err) {
      console.error('Error creating project:', err);
      setError('Failed to create project. Please try again.');
    } finally {
      setCreating(false);
    }
  };

  const getPriorityColor = (priority: string) => {
    switch (priority?.toLowerCase()) {
      case 'high':
        return 'error';
      case 'medium':
        return 'warning';
      case 'low':
        return 'info';
      default:
        return 'default';
    }
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="200px">
        <CircularProgress />
        <Typography variant="body2" sx={{ ml: 2 }}>
          Loading project data...
        </Typography>
      </Box>
    );
  }

  if (error) {
    return (
      <Alert severity="error" sx={{ mb: 2 }}>
        {error}
      </Alert>
    );
  }

  return (
    <Box>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Box>
          <Typography variant="h4" gutterBottom>
            Project Management
          </Typography>
          <Typography variant="body1" color="textSecondary">
            Manage AI agent projects with team structure and context guidelines.
          </Typography>
        </Box>
      </Box>

      {/* Horizontal Action Menu */}
      <Paper elevation={1} sx={{ mb: 3, p: 2 }}>
        <Box display="flex" alignItems="center" justifyContent="space-between">
          <Typography variant="h6" sx={{ fontWeight: 500 }}>
            Actions
          </Typography>
          <Box display="flex" gap={1}>
            <Button
              variant="contained"
              startIcon={<AddIcon />}
              onClick={handleCreateProject}
              sx={{ 
                borderRadius: 2,
                textTransform: 'none',
              }}
            >
              Create Project
            </Button>
            <Button
              variant="outlined"
              startIcon={<SettingsIcon />}
              onClick={handleConfigure}
              sx={{ 
                borderRadius: 2,
                textTransform: 'none',
              }}
              disabled
            >
              Configure
            </Button>
            <IconButton
              onClick={handleActionMenuOpen}
              size="small"
              sx={{ ml: 1 }}
            >
              <MoreVertIcon />
            </IconButton>
            <Menu
              anchorEl={actionMenuAnchor}
              open={Boolean(actionMenuAnchor)}
              onClose={handleActionMenuClose}
              anchorOrigin={{
                vertical: 'bottom',
                horizontal: 'right',
              }}
              transformOrigin={{
                vertical: 'top',
                horizontal: 'right',
              }}
            >
              <MenuItem onClick={() => loadData()}>
                Refresh
              </MenuItem>
              <Divider />
              <MenuItem onClick={() => console.log('Export clicked')}>
                Export Projects
              </MenuItem>
              <MenuItem onClick={() => console.log('Import clicked')}>
                Import Projects
              </MenuItem>
            </Menu>
          </Box>
        </Box>
      </Paper>

      <Grid container spacing={3}>
        <Grid item xs={12}>
          <Paper elevation={1} sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Projects ({projects.length})
            </Typography>
            
            {projects.length === 0 ? (
              <Box sx={{ p: 2, textAlign: 'center' }}>
                <Typography variant="body2" color="textSecondary">
                  No projects found. Create some projects to get started.
                </Typography>
              </Box>
            ) : (
              <Grid container spacing={2}>
                {projects.map((project) => (
                  <Grid item xs={12} md={6} lg={4} key={project.id}>
                    <Card 
                      variant="outlined" 
                      sx={{ 
                        cursor: 'pointer',
                        '&:hover': { elevation: 2 },
                      }}
                      onClick={() => navigate(`/projects/${project.id}`)}
                    >
                      <CardContent>
                          <Box display="flex" alignItems="center" gap={1} mb={2}>
                            <ProjectIcon color="primary" />
                            <Typography variant="h6" fontWeight="medium">
                              {project.name}
                            </Typography>
                          </Box>
                          
                          <Typography variant="body2" color="textSecondary" paragraph>
                            {project.description}
                          </Typography>
                          
                          {project.context && (
                            <Typography variant="body2" color="text.primary" sx={{ 
                              fontStyle: 'italic', 
                              backgroundColor: 'grey.50', 
                              p: 1, 
                              borderRadius: 1,
                              mb: 2,
                              border: '1px solid',
                              borderColor: 'grey.200'
                            }}>
                              <strong>Context:</strong> {project.context}
                            </Typography>
                          )}

                          {/* Selected Organizational Contexts */}
                          {project.settings?.selected_contexts && project.settings.selected_contexts.length > 0 && (
                            <Box mb={2}>
                              <Typography variant="caption" color="textSecondary" display="block" sx={{ mb: 1 }}>
                                <strong>Applied Guidelines:</strong>
                              </Typography>
                              <Box display="flex" flexWrap="wrap" gap={0.5}>
                                {project.settings.selected_contexts.map((contextId: number) => {
                                  const context = contextLookup.get(contextId);
                                  return context ? (
                                    <Chip
                                      key={contextId}
                                      label={context.name}
                                      size="small"
                                      variant="outlined"
                                      color="secondary"
                                      sx={{ 
                                        fontSize: '0.75rem',
                                        height: '24px',
                                        backgroundColor: 'rgba(156, 39, 176, 0.04)'
                                      }}
                                    />
                                  ) : (
                                    <Chip
                                      key={contextId}
                                      label={`Context ${contextId}`}
                                      size="small"
                                      variant="outlined"
                                      color="default"
                                      sx={{ fontSize: '0.75rem', height: '24px' }}
                                    />
                                  );
                                })}
                              </Box>
                            </Box>
                          )}
                          
                          <Box display="flex" gap={1} mb={2}>
                            {project.priority && (
                              <Chip
                                label={project.priority}
                                size="small"
                                color={getPriorityColor(project.priority) as any}
                                variant="outlined"
                              />
                            )}
                            <Chip
                              label={project.status}
                              size="small"
                              variant="filled"
                              sx={{ backgroundColor: 'grey.200' }}
                            />
                          </Box>
                          
                          <Box display="flex" justifyContent="space-between" alignItems="center">
                            <Typography variant="caption" color="textSecondary">
                              {project.team_count || 0} teams • {project.agent_count || 0} agents
                            </Typography>
                            <Button 
                              size="small" 
                              onClick={(e) => {
                                e.stopPropagation();
                                navigate(`/projects/${project.id}`);
                              }}
                            >
                              View Details
                            </Button>
                          </Box>
                        </CardContent>
                      </Card>
                    </Grid>
                  ))}
                </Grid>
              )}
            </Paper>
          </Grid>
        </Grid>

        {/* Create Project Modal */}
        <Dialog 
          open={createModalOpen} 
          onClose={handleModalClose}
          maxWidth="md"
          fullWidth
        >
          <DialogTitle sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            Create New Project
            <IconButton onClick={handleModalClose} size="small">
              <CloseIcon />
            </IconButton>
          </DialogTitle>
          <DialogContent dividers>
            <Stack spacing={3}>
              <TextField
                fullWidth
                label="Project Name"
                value={formData.name}
                onChange={(e) => handleFormChange('name', e.target.value)}
                error={!!formErrors.name}
                helperText={formErrors.name}
                required
              />
              
              <TextField
                fullWidth
                label="Description"
                value={formData.description}
                onChange={(e) => handleFormChange('description', e.target.value)}
                error={!!formErrors.description}
                helperText={formErrors.description}
                multiline
                rows={3}
                required
              />
              
              <TextField
                fullWidth
                label="Project Context"
                value={formData.context}
                onChange={(e) => handleFormChange('context', e.target.value)}
                error={!!formErrors.context}
                helperText={formErrors.context || "Describe what this project will achieve and its key objectives"}
                multiline
                rows={4}
                required
              />
              
              <Box display="flex" gap={2}>
                <FormControl sx={{ minWidth: 150 }}>
                  <InputLabel>Priority</InputLabel>
                  <Select
                    value={formData.priority}
                    onChange={(e) => handleFormChange('priority', e.target.value)}
                    label="Priority"
                  >
                    <MenuItem value="low">Low</MenuItem>
                    <MenuItem value="medium">Medium</MenuItem>
                    <MenuItem value="high">High</MenuItem>
                    <MenuItem value="critical">Critical</MenuItem>
                  </Select>
                </FormControl>
                
                <TextField
                  fullWidth
                  label="Timeline"
                  value={formData.settings.timeline}
                  onChange={(e) => handleFormChange('settings.timeline', e.target.value)}
                  error={!!formErrors['settings.timeline']}
                  helperText={formErrors['settings.timeline'] || "e.g., '6 months', 'Q1 2024', '12 weeks'"}
                  required
                />
              </Box>
              
              <TextField
                fullWidth
                label="Technology Stack (optional)"
                value={formData.settings.tech_stack.join(', ')}
                onChange={(e) => handleFormChange('settings.tech_stack', 
                  e.target.value.split(',').map(s => s.trim()).filter(Boolean)
                )}
                helperText="Enter technologies separated by commas (e.g., React, Node.js, PostgreSQL)"
              />

              {/* Organizational Contexts Selection */}
              <Box>
                <Typography variant="h6" gutterBottom>
                  Organizational Contexts
                </Typography>
                <Typography variant="body2" color="textSecondary" sx={{ mb: 2 }}>
                  Select applicable contexts for this project. These provide guidelines and standards that will be used during project execution.
                </Typography>
                
                {contextsLoading ? (
                  <Box display="flex" justifyContent="center" alignItems="center" py={2}>
                    <CircularProgress size={20} sx={{ mr: 1 }} />
                    <Typography variant="body2">Loading contexts...</Typography>
                  </Box>
                ) : (
                  Object.entries(availableContexts).map(([category, contexts]) => (
                    <Accordion key={category} sx={{ mb: 1 }}>
                      <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                        <Typography variant="subtitle1" sx={{ textTransform: 'capitalize' }}>
                          {category.replace('_', ' ')} ({contexts.length})
                        </Typography>
                      </AccordionSummary>
                      <AccordionDetails>
                        <Stack spacing={1}>
                          {contexts.map((context) => (
                            <FormControlLabel
                              key={context.id}
                              control={
                                <Checkbox
                                  checked={formData.selected_contexts.includes(context.id)}
                                  onChange={(e) => handleContextToggle(context.id, e.target.checked)}
                                />
                              }
                              label={
                                <Box>
                                  <Typography variant="body2" fontWeight="medium">
                                    {context.name}
                                  </Typography>
                                  <Typography variant="caption" color="textSecondary">
                                    {context.description}
                                  </Typography>
                                  {context.content_summary && (
                                    <Typography variant="caption" display="block" color="text.primary" sx={{ mt: 0.5 }}>
                                      {context.content_summary}
                                    </Typography>
                                  )}
                                </Box>
                              }
                            />
                          ))}
                        </Stack>
                      </AccordionDetails>
                    </Accordion>
                  ))
                )}
              </Box>
            </Stack>
          </DialogContent>
          <DialogActions sx={{ p: 2 }}>
            <Button onClick={handleModalClose} disabled={creating}>
              Cancel
            </Button>
            <Button 
              onClick={handleSubmit} 
              variant="contained"
              disabled={creating}
              startIcon={creating ? <CircularProgress size={16} /> : <AddIcon />}
            >
              {creating ? 'Creating...' : 'Create Project'}
            </Button>
          </DialogActions>
        </Dialog>
    </Box>
  );
};

export default ProjectDashboard;