import React from 'react'
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import {
  ThemeProvider,
  CssBaseline,
  Container,
  Typography,
  Box,
  AppBar,
  Toolbar,
  Paper,
} from '@mui/material'
import {
  Dashboard as DashboardIcon,
} from '@mui/icons-material'
import { theme } from './theme'
import Navigation from './components/Navigation'
import HealthCheck from './components/HealthCheck'
import AgentDashboard from './components/AgentDashboard'
import ProjectDashboard from './components/ProjectDashboard'
import TeamDashboard from './components/TeamDashboard'
import WorkflowDashboard from './components/WorkflowDashboard'

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Router>
        <Box sx={{ display: 'flex' }}>
          {/* Navigation Sidebar */}
          <Navigation />
          
          {/* Main Content Area */}
          <Box
            component="main"
            sx={{
              flexGrow: 1,
              bgcolor: 'background.default',
              minHeight: '100vh',
            }}
          >
            {/* App Bar */}
            <AppBar 
              position="static" 
              sx={{ 
                zIndex: (theme) => theme.zIndex.drawer - 1,
                ml: '240px',
                width: 'calc(100% - 240px)',
              }}
            >
              <Toolbar>
                <DashboardIcon sx={{ mr: 2 }} />
                <Typography variant="h6" component="div">
                  Workflow Admin
                </Typography>
                <Typography variant="subtitle2" sx={{ ml: 2, opacity: 0.8 }}>
                  Multi-Agent Management System
                </Typography>
              </Toolbar>
            </AppBar>

            {/* Page Content */}
            <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
              <Routes>
                <Route path="/" element={<Navigate to="/agents" replace />} />
                <Route path="/agents" element={<AgentDashboard />} />
                <Route path="/projects" element={<ProjectDashboard />} />
                <Route path="/teams" element={<TeamDashboard />} />
                <Route path="/workflows" element={<WorkflowDashboard />} />
              </Routes>

              {/* System Status Section - Only show on agents page for now */}
              <Routes>
                <Route path="/agents" element={
                  <Box sx={{ mt: 4 }}>
                    <Typography variant="h5" gutterBottom>
                      System Status
                    </Typography>
                    <HealthCheck />
                  </Box>
                } />
              </Routes>

              {/* Development Info */}
              <Paper elevation={1} sx={{ p: 2, mt: 3, bgcolor: 'grey.50' }}>
                <Typography variant="subtitle2" gutterBottom>
                  Development Stage 2 Status:
                </Typography>
                <Box component="ul" sx={{ m: 0, pl: 2 }}>
                  <Typography component="li" variant="body2">
                    ✅ React Router navigation system
                  </Typography>
                  <Typography component="li" variant="body2">
                    ✅ Multi-page dashboard with sidebar navigation
                  </Typography>
                  <Typography component="li" variant="body2">
                    ✅ Agents, Projects, Teams, and Workflows views
                  </Typography>
                  <Typography component="li" variant="body2">
                    ✅ Mock data integration for all entities
                  </Typography>
                  <Typography component="li" variant="body2">
                    ⏳ Next: CRUD operations and detailed views
                  </Typography>
                </Box>
              </Paper>
            </Container>
          </Box>
        </Box>
      </Router>
    </ThemeProvider>
  )
}

export default App