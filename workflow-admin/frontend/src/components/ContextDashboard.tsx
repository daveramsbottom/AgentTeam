import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Box,
  Typography,
  Paper,
  Grid,
  Alert,
  CircularProgress,
  Card,
  CardContent,
  Button,
  Chip,
  Stack,
} from '@mui/material';
import {
  Description as ContextIcon,
  Category as CategoryIcon,
  ArrowForward as ArrowForwardIcon,
} from '@mui/icons-material';
import { contextsApi, GroupedContexts } from '../api/contexts';

const ContextDashboard: React.FC = () => {
  const navigate = useNavigate();
  const [groupedContexts, setGroupedContexts] = useState<GroupedContexts>({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      setLoading(true);
      setError(null);
      const contextsData = await contextsApi.getSelectableProjectContexts();
      setGroupedContexts(contextsData);
    } catch (err) {
      console.error('Error loading contexts:', err);
      setError('Failed to load contexts.');
    } finally {
      setLoading(false);
    }
  };

  const getCategoryDisplayName = (category: string) => {
    return category.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase());
  };

  const getCategoryColor = (category: string) => {
    const colors: Record<string, string> = {
      'tech_standards': '#2196F3',
      'security': '#F44336', 
      'compliance': '#FF9800',
      'business_guidelines': '#4CAF50'
    };
    return colors[category] || '#757575';
  };

  const getCategoryDescription = (category: string) => {
    const descriptions: Record<string, string> = {
      'tech_standards': 'Technology stacks, frameworks, and development standards',
      'security': 'Security protocols, authentication, and data protection requirements',
      'compliance': 'Legal, regulatory, and accessibility compliance requirements',
      'business_guidelines': 'Process guidelines, quality standards, and business rules'
    };
    return descriptions[category] || 'Organizational context guidelines';
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="200px">
        <CircularProgress />
        <Typography variant="body2" sx={{ ml: 2 }}>
          Loading organizational contexts...
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
            Organizational Contexts
          </Typography>
          <Typography variant="body1" color="textSecondary">
            Manage organizational guidelines, standards, and contexts used across projects.
          </Typography>
        </Box>
      </Box>

      {/* Category Overview Cards */}
      <Grid container spacing={3} mb={4}>
        {Object.entries(groupedContexts).map(([category, contexts]) => (
          <Grid item xs={12} md={6} lg={3} key={category}>
            <Card 
              variant="outlined" 
              sx={{ 
                cursor: 'pointer',
                transition: 'all 0.2s ease-in-out',
                '&:hover': { 
                  elevation: 4,
                  transform: 'translateY(-2px)',
                  borderColor: getCategoryColor(category)
                },
                borderLeft: `4px solid ${getCategoryColor(category)}`
              }}
              onClick={() => navigate(`/contexts/${category}`)}
            >
              <CardContent>
                <Box display="flex" alignItems="center" gap={1} mb={2}>
                  <CategoryIcon sx={{ color: getCategoryColor(category) }} />
                  <Typography variant="h6" fontWeight="medium">
                    {getCategoryDisplayName(category)}
                  </Typography>
                </Box>
                
                <Typography variant="body2" color="textSecondary" paragraph>
                  {getCategoryDescription(category)}
                </Typography>
                
                <Box display="flex" justifyContent="space-between" alignItems="center">
                  <Chip 
                    label={`${contexts.length} contexts`}
                    size="small"
                    sx={{ 
                      backgroundColor: getCategoryColor(category) + '20',
                      color: getCategoryColor(category),
                      fontWeight: 'medium'
                    }}
                  />
                  <Button 
                    size="small" 
                    endIcon={<ArrowForwardIcon />}
                    onClick={(e) => {
                      e.stopPropagation();
                      navigate(`/contexts/${category}`);
                    }}
                    sx={{ color: getCategoryColor(category) }}
                  >
                    View
                  </Button>
                </Box>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      {/* Summary Statistics */}
      <Paper elevation={1} sx={{ p: 3 }}>
        <Typography variant="h6" gutterBottom>
          Context Overview
        </Typography>
        <Grid container spacing={3}>
          <Grid item xs={12} sm={6} md={3}>
            <Box textAlign="center">
              <Typography variant="h3" color="primary" fontWeight="bold">
                {Object.keys(groupedContexts).length}
              </Typography>
              <Typography variant="body2" color="textSecondary">
                Categories
              </Typography>
            </Box>
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <Box textAlign="center">
              <Typography variant="h3" color="success.main" fontWeight="bold">
                {Object.values(groupedContexts).flat().length}
              </Typography>
              <Typography variant="body2" color="textSecondary">
                Total Contexts
              </Typography>
            </Box>
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <Box textAlign="center">
              <Typography variant="h3" color="info.main" fontWeight="bold">
                {Math.round(Object.values(groupedContexts).flat().length / Math.max(Object.keys(groupedContexts).length, 1))}
              </Typography>
              <Typography variant="body2" color="textSecondary">
                Average per Category
              </Typography>
            </Box>
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <Box textAlign="center">
              <Typography variant="h3" color="warning.main" fontWeight="bold">
                {Object.values(groupedContexts).flat().filter(c => c.tags && c.tags.length > 0).length}
              </Typography>
              <Typography variant="body2" color="textSecondary">
                Tagged Contexts
              </Typography>
            </Box>
          </Grid>
        </Grid>
      </Paper>

      {/* Quick Preview of All Contexts */}
      <Box mt={4}>
        <Typography variant="h6" gutterBottom>
          All Contexts Preview
        </Typography>
        <Stack spacing={2}>
          {Object.entries(groupedContexts).map(([category, contexts]) => (
            <Paper key={category} variant="outlined" sx={{ p: 2 }}>
              <Box display="flex" justifyContent="space-between" alignItems="center" mb={1}>
                <Typography variant="subtitle1" fontWeight="medium" sx={{ color: getCategoryColor(category) }}>
                  {getCategoryDisplayName(category)}
                </Typography>
                <Button 
                  size="small" 
                  onClick={() => navigate(`/contexts/${category}`)}
                  sx={{ color: getCategoryColor(category) }}
                >
                  Manage
                </Button>
              </Box>
              <Box display="flex" flexWrap="wrap" gap={1}>
                {contexts.map((context) => (
                  <Chip
                    key={context.id}
                    label={context.name}
                    size="small"
                    variant="outlined"
                    sx={{ 
                      borderColor: getCategoryColor(category) + '40',
                      color: getCategoryColor(category),
                      '&:hover': {
                        backgroundColor: getCategoryColor(category) + '10'
                      }
                    }}
                  />
                ))}
              </Box>
            </Paper>
          ))}
        </Stack>
      </Box>
    </Box>
  );
};

export default ContextDashboard;