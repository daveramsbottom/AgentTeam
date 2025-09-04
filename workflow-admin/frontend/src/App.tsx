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
import HomePage from './components/HomePage'
import ProjectDashboard from './components/ProjectDashboard'
import ProjectDetailsPage from './components/ProjectDetailsPage'
import AgentDashboard from './components/AgentDashboard'
import AgentTypeDetailPage from './components/AgentTypeDetailPage'
import AgentListPage from './components/AgentListPage'
import TeamDashboard from './components/TeamDashboard'
import TeamDetailPage from './components/TeamDetailPage'
import WorkflowDashboard from './components/WorkflowDashboard'
import WorkflowDetailPage from './components/WorkflowDetailPage'
import ContextDashboard from './components/ContextDashboard'
import ContextCategoryPage from './components/ContextCategoryPage'

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
                <Route path="/" element={<HomePage />} />
                <Route path="/projects" element={<ProjectDashboard />} />
                <Route path="/projects/:id" element={<ProjectDetailsPage />} />
                <Route path="/agents" element={<AgentDashboard />} />
                <Route path="/agents/:id" element={<AgentTypeDetailPage />} />
                <Route path="/agents-list" element={<AgentListPage />} />
                <Route path="/agents-list/:id" element={<AgentTypeDetailPage />} />
                <Route path="/teams" element={<TeamDashboard />} />
                <Route path="/teams/:id" element={<TeamDetailPage />} />
                <Route path="/workflows" element={<WorkflowDashboard />} />
                <Route path="/workflows/:id" element={<WorkflowDetailPage />} />
                <Route path="/contexts" element={<ContextDashboard />} />
                <Route path="/contexts/:category" element={<ContextCategoryPage />} />
              </Routes>

              {/* System Status Section - Only show on agents page */}
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
            </Container>
          </Box>
        </Box>
      </Router>
    </ThemeProvider>
  )
}

export default App