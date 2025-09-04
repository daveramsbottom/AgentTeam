import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  Box,
  Alert,
  CircularProgress,
} from '@mui/material';
import { Project, projectsApi } from '../api/projects';
import { teamsApi } from '../api/teams';
import { Agent, agentsApi } from '../api/agents';
import ProjectHeader from './project/ProjectHeader';
import ProjectContextEditor from './project/ProjectContextEditor';
import TeamManager from './project/TeamManager';
import { TeamSummary, ProjectContext } from './project/types';

const ProjectDetailsPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  
  // Core state
  const [project, setProject] = useState<Project | null>(null);
  const [teams, setTeams] = useState<TeamSummary[]>([]);
  const [agents, setAgents] = useState<Agent[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  
  // UI state
  const [isEditMode, setIsEditMode] = useState(false);
  const [expandedTeams, setExpandedTeams] = useState<Set<number>>(new Set());
  
  // Context editing state
  const [editingContext, setEditingContext] = useState(false);
  const [tempContext, setTempContext] = useState('');

  // Get project context from the project's settings field
  const getProjectContext = (): ProjectContext => {
    if (!project?.settings) return {
      tech_stack: [],
      compliance_rules: [],
      security_standards: [],
      business_guidelines: [],
    };
    
    return project.settings as ProjectContext;
  };

  // Load project data
  useEffect(() => {
    if (!id) return;

    const loadProject = async () => {
      setLoading(true);
      setError(null);
      
      try {
        // Load project, teams, and agents concurrently
        const [projects, allTeams, allAgents] = await Promise.all([
          projectsApi.getProjects(),
          teamsApi.getTeams(),
          agentsApi.getAgents(),
        ]);

        const foundProject = projects.find(p => p.id === parseInt(id));
        
        if (foundProject) {
          setProject(foundProject);
          setAgents(allAgents);
          
          // Filter teams for this project and convert to TeamSummary format
          const projectTeams = allTeams.filter(team => team.project_id === foundProject.id);
          
          const getAgentById = (agentId: number): Agent | undefined => 
            allAgents.find(agent => agent.id === agentId);
          
          const teamSummaries: TeamSummary[] = projectTeams.map(team => {
            const leadAgent = team.team_lead_id ? getAgentById(team.team_lead_id) : undefined;
            
            return {
              id: team.id,
              name: team.name,
              agent_count: team.member_agent_ids?.length || 0,
              lead_agent: leadAgent?.name || 'No lead assigned',
              specialization: team.description || 'General purpose team',
              members: team.member_agent_ids?.map(agentId => {
                const agent = getAgentById(agentId);
                return {
                  id: agentId,
                  name: agent?.name || `Agent ${agentId}`,
                  role: agentId === team.team_lead_id ? 'Team Lead' : 'Team Member',
                  status: (agent?.status as 'active' | 'idle' | 'busy') || 'active',
                  specialization: agent?.description || 'Multi-agent system development',
                  workflow_version: 'v1.0.0',
                  workflow_id: 1
                };
              }) || []
            };
          });
          
          setTeams(teamSummaries);
        } else {
          setError('Project not found');
        }
      } catch (error) {
        console.error('Error loading project:', error);
        setError('Failed to load project details');
      } finally {
        setLoading(false);
      }
    };

    loadProject();
  }, [id]);

  // Navigation handlers
  const handleBack = () => {
    navigate('/projects');
  };

  const handleWorkflowNavigation = (workflowId: number, memberName: string, role: string) => {
    navigate(`/workflows/${workflowId}?agent=${encodeURIComponent(memberName)}&role=${encodeURIComponent(role)}&project=${id}`, {
      state: { from: `/projects/${id}` }
    });
  };

  // Team management handlers
  const toggleTeamExpansion = (teamId: number) => {
    setExpandedTeams(prev => {
      const newSet = new Set(prev);
      if (newSet.has(teamId)) {
        newSet.delete(teamId);
      } else {
        newSet.add(teamId);
      }
      return newSet;
    });
  };

  // Edit mode handlers
  const toggleEditMode = () => {
    if (isEditMode) {
      // Exiting edit mode - cancel any ongoing edits
      setEditingContext(false);
      setTempContext('');
    }
    setIsEditMode(!isEditMode);
  };

  // Context editing handlers
  const startEditingContext = () => {
    setTempContext(project?.context || '');
    setEditingContext(true);
  };

  const saveContext = async () => {
    if (!project) return;
    
    try {
      await projectsApi.updateProject(project.id, { context: tempContext });
      setProject({ ...project, context: tempContext });
      setEditingContext(false);
    } catch (error) {
      console.error('Error saving context:', error);
      setError('Failed to save context');
    }
  };

  const cancelEditingContext = () => {
    setTempContext('');
    setEditingContext(false);
  };

  // Loading and error states
  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="200px">
        <CircularProgress />
      </Box>
    );
  }

  if (error || !project) {
    return (
      <Box>
        <ProjectHeader
          project={{ name: 'Error', description: '' }}
          isEditMode={false}
          onBack={handleBack}
          onToggleEditMode={() => {}}
        />
        <Alert severity="error">
          {error || 'Project not found'}
        </Alert>
      </Box>
    );
  }

  return (
    <Box>
      <ProjectHeader
        project={project}
        isEditMode={isEditMode}
        onBack={handleBack}
        onToggleEditMode={toggleEditMode}
      />

      <ProjectContextEditor
        project={project}
        isEditMode={isEditMode}
        editingContext={editingContext}
        tempContext={tempContext}
        onStartEditing={startEditingContext}
        onSaveContext={saveContext}
        onCancelEditing={cancelEditingContext}
        onContextChange={setTempContext}
      />

      <TeamManager
        project={project}
        teams={teams}
        agents={agents}
        isEditMode={isEditMode}
        onTeamsUpdate={setTeams}
        expandedTeams={expandedTeams}
        onToggleTeamExpansion={toggleTeamExpansion}
        onWorkflowNavigation={handleWorkflowNavigation}
      />
    </Box>
  );
};

export default ProjectDetailsPage;