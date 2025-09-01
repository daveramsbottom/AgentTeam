import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Paper,
  Grid,
  Alert,
  CircularProgress,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  Chip,
  Card,
  CardContent,
  Button,
  Tabs,
  Tab,
} from '@mui/material';
import {
  Folder as ProjectIcon,
  Star as HighPriorityIcon,
  Remove as MediumPriorityIcon,
  KeyboardArrowDown as LowPriorityIcon,
  AccountTree as HierarchyIcon,
  List as ListIcon,
} from '@mui/icons-material';
import { Project, projectsApi } from '../api/projects';
import ProjectHierarchyView from './ProjectHierarchyView';

const ProjectDashboard: React.FC = () => {
  const [projects, setProjects] = useState<Project[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [viewMode, setViewMode] = useState<'list' | 'hierarchy'>('list');
  const [selectedProject, setSelectedProject] = useState<number | null>(null);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      setLoading(true);
      setError(null);
      const projectsData = await projectsApi.getProjects();
      setProjects(projectsData);
      if (projectsData.length > 0 && !selectedProject) {
        setSelectedProject(projectsData[0].id);
      }
    } catch (err) {
      console.error('Error loading project data:', err);
      setError('Failed to load project data.');
    } finally {
      setLoading(false);
    }
  };

  const handleViewModeChange = (_: React.SyntheticEvent, newValue: 'list' | 'hierarchy') => {
    setViewMode(newValue);
  };

  const getPriorityIcon = (priority: string) => {
    switch (priority?.toLowerCase()) {
      case 'high':
        return <HighPriorityIcon color="error" />;
      case 'medium':
        return <MediumPriorityIcon color="warning" />;
      case 'low':
        return <LowPriorityIcon color="info" />;
      default:
        return <MediumPriorityIcon />;
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
            Manage AI agent projects with hierarchical team and context structure.
          </Typography>
        </Box>
        
        <Tabs value={viewMode} onChange={handleViewModeChange}>
          <Tab 
            value="list" 
            label="List View" 
            icon={<ListIcon />} 
            iconPosition="start"
          />
          <Tab 
            value="hierarchy" 
            label="Hierarchy View" 
            icon={<HierarchyIcon />} 
            iconPosition="start"
          />
        </Tabs>
      </Box>

      {viewMode === 'list' ? (
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
                          border: selectedProject === project.id ? '2px solid' : '1px solid',
                          borderColor: selectedProject === project.id ? 'primary.main' : 'grey.300',
                        }}
                        onClick={() => setSelectedProject(project.id)}
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
                                setSelectedProject(project.id);
                                setViewMode('hierarchy');
                              }}
                            >
                              View Hierarchy
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
      ) : (
        <Box>
          {selectedProject && (
            <ProjectHierarchyView projectId={selectedProject} />
          )}
          {!selectedProject && (
            <Paper elevation={1} sx={{ p: 4, textAlign: 'center' }}>
              <Typography variant="h6" color="textSecondary">
                Select a project to view its hierarchy
              </Typography>
            </Paper>
          )}
        </Box>
      )}
    </Box>
  );
};

export default ProjectDashboard;