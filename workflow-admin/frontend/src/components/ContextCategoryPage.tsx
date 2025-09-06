import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  Box,
  Typography,
  Paper,
  Alert,
  CircularProgress,
  Card,
  CardContent,
  Button,
  Chip,
  Stack,
  Breadcrumbs,
  Link,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  Divider,
  Grid,
} from '@mui/material';
import {
  ArrowBack as ArrowBackIcon,
  Description as ContextIcon,
  ExpandMore as ExpandMoreIcon,
  Edit as EditIcon,
  Add as AddIcon,
} from '@mui/icons-material';
import { contextsApi, OrganizationalContext, UpdateContextRequest } from '../api/contexts';
import { EditContextModal } from './contexts';
import { 
  getCategoryColor, 
  getCategoryDisplayName, 
  updateCategoryColorsFromContexts 
} from '../utils/categoryColors';

const ContextCategoryPage: React.FC = () => {
  const { category } = useParams<{ category: string }>();
  const navigate = useNavigate();
  const [contexts, setContexts] = useState<OrganizationalContext[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [editModalOpen, setEditModalOpen] = useState(false);
  const [editingContext, setEditingContext] = useState<OrganizationalContext | null>(null);
  const [updating, setUpdating] = useState(false);

  useEffect(() => {
    if (category) {
      loadData();
    }
  }, [category]);

  const loadData = async () => {
    if (!category) return;
    
    try {
      setLoading(true);
      setError(null);
      const contextsData = await contextsApi.getContextsByCategory(category);
      
      // Update color cache with any new category colors
      updateCategoryColorsFromContexts(contextsData);
      
      setContexts(contextsData);
    } catch (err) {
      console.error('Error loading contexts:', err);
      setError('Failed to load contexts for this category.');
    } finally {
      setLoading(false);
    }
  };

  // Using centralized color utility functions

  const getCategoryDescription = (category: string) => {
    const descriptions: Record<string, string> = {
      'tech_standards': 'Technology stacks, frameworks, and development standards used across projects',
      'security': 'Security protocols, authentication requirements, and data protection standards',
      'compliance': 'Legal, regulatory, and accessibility compliance requirements and guidelines',
      'business_guidelines': 'Process guidelines, quality standards, and business rules for project execution'
    };
    return descriptions[category] || 'Organizational context guidelines';
  };

  const handleEditContext = (context: OrganizationalContext) => {
    setEditingContext(context);
    setEditModalOpen(true);
  };

  const handleUpdateContext = async (id: number, contextData: UpdateContextRequest) => {
    try {
      setUpdating(true);
      setError(null);
      
      await contextsApi.updateContext(id, contextData);
      
      // Reload contexts to show updated data
      await loadData();
      setEditModalOpen(false);
      setEditingContext(null);
    } catch (err) {
      console.error('Error updating context:', err);
      setError('Failed to update context. Please try again.');
    } finally {
      setUpdating(false);
    }
  };

  const renderContextContent = (content: any) => {
    if (!content) return null;

    const renderValue = (key: string, value: any): React.ReactNode => {
      if (Array.isArray(value)) {
        return (
          <Box key={key} mb={2}>
            <Typography variant="subtitle2" fontWeight="medium" gutterBottom>
              {key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}:
            </Typography>
            <Stack direction="row" spacing={1} flexWrap="wrap" useFlexGap>
              {value.map((item, index) => (
                <Chip key={index} label={item} size="small" variant="outlined" />
              ))}
            </Stack>
          </Box>
        );
      } else if (typeof value === 'object' && value !== null) {
        return (
          <Box key={key} mb={2}>
            <Typography variant="subtitle2" fontWeight="medium" gutterBottom>
              {key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}:
            </Typography>
            <Box pl={2}>
              {Object.entries(value).map(([subKey, subValue]) => 
                renderValue(subKey, subValue)
              )}
            </Box>
          </Box>
        );
      } else {
        return (
          <Box key={key} mb={2}>
            <Typography variant="subtitle2" fontWeight="medium" display="inline">
              {key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}:{' '}
            </Typography>
            <Typography variant="body2" display="inline">
              {String(value)}
            </Typography>
          </Box>
        );
      }
    };

    return (
      <Box>
        {Object.entries(content).map(([key, value]) => 
          renderValue(key, value)
        )}
      </Box>
    );
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="200px">
        <CircularProgress />
        <Typography variant="body2" sx={{ ml: 2 }}>
          Loading contexts...
        </Typography>
      </Box>
    );
  }

  if (error) {
    return (
      <Box>
        <Button
          startIcon={<ArrowBackIcon />}
          onClick={() => navigate('/contexts')}
          sx={{ mb: 2 }}
        >
          Back to Contexts
        </Button>
        <Alert severity="error">
          {error}
        </Alert>
      </Box>
    );
  }

  if (!category) {
    return (
      <Alert severity="error">
        No category specified.
      </Alert>
    );
  }

  return (
    <Box>
      {/* Breadcrumbs */}
      <Breadcrumbs sx={{ mb: 2 }}>
        <Link 
          component="button"
          variant="body2"
          onClick={() => navigate('/contexts')}
          sx={{ textDecoration: 'none' }}
        >
          Contexts
        </Link>
        <Typography variant="body2" color="text.primary">
          {getCategoryDisplayName(category, contexts)}
        </Typography>
      </Breadcrumbs>

      {/* Header */}
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Box>
          <Box display="flex" alignItems="center" gap={1} mb={1}>
            <Button
              startIcon={<ArrowBackIcon />}
              onClick={() => navigate('/contexts')}
              variant="outlined"
              size="small"
            >
              Back
            </Button>
          </Box>
          <Typography variant="h4" gutterBottom sx={{ color: getCategoryColor(category) }}>
            {getCategoryDisplayName(category, contexts)}
          </Typography>
          <Typography variant="body1" color="textSecondary">
            {getCategoryDescription(category)}
          </Typography>
        </Box>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={() => {
            // TODO: Implement add context functionality
            console.log('Add new context for category:', category);
          }}
          sx={{ 
            backgroundColor: getCategoryColor(category),
            '&:hover': {
              backgroundColor: getCategoryColor(category) + 'CC'
            }
          }}
        >
          Add Context
        </Button>
      </Box>

      {/* Statistics */}
      <Paper elevation={1} sx={{ p: 2, mb: 3 }}>
        <Grid container spacing={3}>
          <Grid item xs={6} sm={3}>
            <Box textAlign="center">
              <Typography variant="h4" sx={{ color: getCategoryColor(category) }} fontWeight="bold">
                {contexts.length}
              </Typography>
              <Typography variant="caption" color="textSecondary">
                Total Contexts
              </Typography>
            </Box>
          </Grid>
          <Grid item xs={6} sm={3}>
            <Box textAlign="center">
              <Typography variant="h4" color="success.main" fontWeight="bold">
                {contexts.filter(c => c.tags && c.tags.length > 0).length}
              </Typography>
              <Typography variant="caption" color="textSecondary">
                Tagged
              </Typography>
            </Box>
          </Grid>
          <Grid item xs={6} sm={3}>
            <Box textAlign="center">
              <Typography variant="h4" color="info.main" fontWeight="bold">
                {Math.round(contexts.reduce((sum, c) => sum + (c.tags?.length || 0), 0) / Math.max(contexts.length, 1))}
              </Typography>
              <Typography variant="caption" color="textSecondary">
                Avg Tags
              </Typography>
            </Box>
          </Grid>
          <Grid item xs={6} sm={3}>
            <Box textAlign="center">
              <Typography variant="h4" color="primary.main" fontWeight="bold">
                {contexts.filter(c => c.content_summary).length}
              </Typography>
              <Typography variant="caption" color="textSecondary">
                Documented
              </Typography>
            </Box>
          </Grid>
        </Grid>
      </Paper>

      {/* Contexts List */}
      {contexts.length === 0 ? (
        <Paper elevation={1} sx={{ p: 4, textAlign: 'center' }}>
          <ContextIcon sx={{ fontSize: 48, color: 'grey.400', mb: 2 }} />
          <Typography variant="h6" color="textSecondary" gutterBottom>
            No contexts found
          </Typography>
          <Typography variant="body2" color="textSecondary" mb={3}>
            This category doesn't have any organizational contexts yet.
          </Typography>
          <Button 
            variant="contained" 
            startIcon={<AddIcon />}
            sx={{ 
              backgroundColor: getCategoryColor(category),
              '&:hover': {
                backgroundColor: getCategoryColor(category) + 'CC'
              }
            }}
            onClick={() => {
              // TODO: Implement add context functionality
              console.log('Add first context for category:', category);
            }}
          >
            Add First Context
          </Button>
        </Paper>
      ) : (
        <Stack spacing={2}>
          {contexts.map((context) => (
            <Accordion key={context.id}>
              <AccordionSummary 
                expandIcon={<ExpandMoreIcon />}
                sx={{
                  '&:hover': {
                    backgroundColor: getCategoryColor(category) + '08'
                  }
                }}
              >
                <Box display="flex" alignItems="center" justifyContent="space-between" width="100%">
                  <Box display="flex" alignItems="center" gap={2} flexGrow={1}>
                    <ContextIcon sx={{ color: getCategoryColor(category) }} />
                    <Box>
                      <Typography variant="h6" fontWeight="medium">
                        {context.name}
                      </Typography>
                      {context.description && (
                        <Typography variant="body2" color="textSecondary">
                          {context.description}
                        </Typography>
                      )}
                    </Box>
                  </Box>
                  <Box display="flex" gap={1} onClick={(e) => e.stopPropagation()}>
                    {context.tags && context.tags.map((tag, index) => (
                      <Chip 
                        key={index}
                        label={tag} 
                        size="small" 
                        variant="outlined"
                        sx={{ 
                          borderColor: getCategoryColor(category),
                          color: getCategoryColor(category),
                          fontSize: '0.75rem'
                        }}
                      />
                    ))}
                    <Button
                      size="small"
                      startIcon={<EditIcon />}
                      onClick={(e) => {
                        e.stopPropagation();
                        handleEditContext(context);
                      }}
                      sx={{ 
                        color: getCategoryColor(category),
                        minWidth: 'auto',
                        ml: 1
                      }}
                    >
                      Edit
                    </Button>
                  </Box>
                </Box>
              </AccordionSummary>
              <AccordionDetails>
                <Divider sx={{ mb: 2 }} />
                
                {/* Content Summary */}
                {context.content_summary && (
                  <Box mb={3}>
                    <Typography variant="subtitle1" fontWeight="medium" gutterBottom>
                      Summary
                    </Typography>
                    <Paper variant="outlined" sx={{ p: 2, backgroundColor: 'grey.50' }}>
                      <Typography variant="body2">
                        {context.content_summary}
                      </Typography>
                    </Paper>
                  </Box>
                )}

                {/* Detailed Content */}
                <Typography variant="subtitle1" fontWeight="medium" gutterBottom>
                  Details
                </Typography>
                <Paper variant="outlined" sx={{ p: 2 }}>
                  {renderContextContent((context as any).content)}
                </Paper>
              </AccordionDetails>
            </Accordion>
          ))}
        </Stack>
      )}
      
      {/* Edit Context Modal */}
      <EditContextModal
        open={editModalOpen}
        onClose={() => {
          setEditModalOpen(false);
          setEditingContext(null);
        }}
        onSubmit={handleUpdateContext}
        context={editingContext}
        loading={updating}
      />
    </Box>
  );
};

export default ContextCategoryPage;