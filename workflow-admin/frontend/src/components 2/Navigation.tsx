import React from 'react';
import { useLocation, Link } from 'react-router-dom';
import {
  Drawer,
  List,
  ListItem,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  Toolbar,
  Box,
  Typography,
} from '@mui/material';
import {
  Dashboard as DashboardIcon,
  SmartToy as AgentsIcon,
  Folder as ProjectsIcon,
  Group as TeamsIcon,
  AccountTree as WorkflowsIcon,
  Settings as SettingsIcon,
} from '@mui/icons-material';

const drawerWidth = 240;

interface NavigationItem {
  path: string;
  label: string;
  icon: React.ReactElement;
}

const navigationItems: NavigationItem[] = [
  { path: '/agents', label: 'Agents', icon: <AgentsIcon /> },
  { path: '/projects', label: 'Projects', icon: <ProjectsIcon /> },
  { path: '/teams', label: 'Teams', icon: <TeamsIcon /> },
  { path: '/workflows', label: 'Workflows', icon: <WorkflowsIcon /> },
];

const Navigation: React.FC = () => {
  const location = useLocation();

  return (
    <Drawer
      variant="permanent"
      sx={{
        width: drawerWidth,
        flexShrink: 0,
        '& .MuiDrawer-paper': {
          width: drawerWidth,
          boxSizing: 'border-box',
        },
      }}
    >
      <Toolbar>
        <Box display="flex" alignItems="center" gap={1}>
          <DashboardIcon color="primary" />
          <Typography variant="h6" component="div">
            Workflow Admin
          </Typography>
        </Box>
      </Toolbar>
      
      <Box sx={{ overflow: 'auto' }}>
        <List>
          {navigationItems.map((item) => (
            <ListItem key={item.path} disablePadding>
              <ListItemButton
                component={Link}
                to={item.path}
                selected={location.pathname === item.path}
                sx={{
                  '&.Mui-selected': {
                    backgroundColor: 'primary.light',
                    color: 'primary.contrastText',
                    '&:hover': {
                      backgroundColor: 'primary.main',
                    },
                    '& .MuiListItemIcon-root': {
                      color: 'primary.contrastText',
                    },
                  },
                }}
              >
                <ListItemIcon>
                  {item.icon}
                </ListItemIcon>
                <ListItemText primary={item.label} />
              </ListItemButton>
            </ListItem>
          ))}
        </List>
      </Box>
    </Drawer>
  );
};

export default Navigation;