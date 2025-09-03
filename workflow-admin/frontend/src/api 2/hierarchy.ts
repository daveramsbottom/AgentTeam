import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export interface ProjectHierarchy {
  project: {
    id: number;
    name: string;
    description: string;
    context: any;
    status: string;
    team_count: number;
    agent_count: number;
  };
  teams: {
    id: number;
    name: string;
    team_type: string;
    context: any;
    agent_count: number;
    status: string;
    agents: {
      id: number;
      name: string;
      role: string;
      status: string;
    }[];
  }[];
}

export interface TeamHierarchy {
  team: {
    id: number;
    name: string;
    team_type: string;
    context: any;
    project_context: any;
  };
  agents: {
    id: number;
    name: string;
    role: string;
    context: any;
    full_context: any;
    status: string;
  }[];
}

/**
 * API endpoints for hierarchical data management
 */
export const hierarchyApi = {
  /**
   * Get complete project hierarchy with teams and agents
   */
  getProjectHierarchy: async (projectId: number): Promise<ProjectHierarchy> => {
    try {
      const response = await api.get(`/api/v1/projects/${projectId}/hierarchy`);
      return response.data;
    } catch (error) {
      console.warn('Project hierarchy API failed, returning mock data:', error);
      return {
        project: {
          id: projectId,
          name: 'AgentTeam Multi-Agent System',
          description: 'AI-powered development team simulation with workflow orchestration',
          context: {
            purpose: 'Create an AI-powered multi-agent system that simulates professional software development teams',
            scope: 'Full-stack development with AI agents for Product Owner and Developer roles',
          },
          status: 'active',
          team_count: 2,
          agent_count: 3,
        },
        teams: [
          {
            id: 1,
            name: 'Core Development Team',
            team_type: 'full_stack',
            context: {
              specialization: 'AI agent orchestration and workflow management',
              responsibilities: ['Requirements gathering', 'Technical implementation', 'System integration'],
            },
            agent_count: 2,
            status: 'active',
            agents: [
              { id: 1, name: 'AgentIan', role: 'Product Owner', status: 'active' },
              { id: 2, name: 'AgentPete', role: 'Senior Developer', status: 'active' },
            ],
          },
          {
            id: 2,
            name: 'Quality Assurance Team',
            team_type: 'qa',
            context: {
              specialization: 'Testing and quality validation',
              responsibilities: ['Test planning', 'Quality assurance', 'Bug tracking'],
            },
            agent_count: 1,
            status: 'planning',
            agents: [
              { id: 3, name: 'AgentSarah', role: 'QA Engineer', status: 'inactive' },
            ],
          },
        ],
      };
    }
  },

  /**
   * Get team hierarchy with inherited context and agents
   */
  getTeamHierarchy: async (teamId: number): Promise<TeamHierarchy> => {
    try {
      const response = await api.get(`/api/v1/teams/${teamId}/hierarchy`);
      return response.data;
    } catch (error) {
      console.warn('Team hierarchy API failed, returning mock data:', error);
      return {
        team: {
          id: teamId,
          name: 'Core Development Team',
          team_type: 'full_stack',
          context: {
            specialization: 'AI agent orchestration and workflow management',
            responsibilities: ['Requirements gathering', 'Technical implementation'],
            technology_stack: {
              primary_languages: ['typescript', 'python'],
              frameworks: ['react', 'fastapi'],
              tools: ['docker', 'postgresql'],
            },
          },
          project_context: {
            purpose: 'Create an AI-powered multi-agent system',
            requirements: {
              functional: ['AI agent management', 'Workflow orchestration'],
              non_functional: ['Scalability', 'Reliability'],
            },
          },
        },
        agents: [
          {
            id: 1,
            name: 'AgentIan',
            role: 'Product Owner',
            context: {
              responsibilities: ['Requirements analysis', 'Stakeholder communication'],
              workflow_template: 'product_owner_workflow',
            },
            full_context: {
              // Combined project + team + agent context
              effective_responsibilities: ['Requirements analysis', 'Stakeholder communication', 'Story creation'],
              technology_awareness: ['typescript', 'react', 'jira', 'slack'],
              decision_authority: ['story_prioritization', 'requirement_changes'],
            },
            status: 'active',
          },
          {
            id: 2,
            name: 'AgentPete',
            role: 'Senior Developer',
            context: {
              responsibilities: ['Technical implementation', 'Code review'],
              workflow_template: 'developer_workflow',
            },
            full_context: {
              effective_responsibilities: ['Technical implementation', 'Code review', 'Architecture decisions'],
              technology_stack: ['typescript', 'python', 'react', 'fastapi'],
              decision_authority: ['technical_decisions', 'code_quality'],
            },
            status: 'active',
          },
        ],
      };
    }
  },

  /**
   * Create a new team within a project with inherited context
   */
  createTeamInProject: async (projectId: number, teamData: any) => {
    try {
      const response = await api.post(`/api/v1/projects/${projectId}/teams`, teamData);
      return response.data;
    } catch (error) {
      console.warn('Create team API failed:', error);
      throw error;
    }
  },

  /**
   * Create a new agent within a team with inherited context
   */
  createAgentInTeam: async (teamId: number, agentData: any) => {
    try {
      const response = await api.post(`/api/v1/teams/${teamId}/agents`, agentData);
      return response.data;
    } catch (error) {
      console.warn('Create agent API failed:', error);
      throw error;
    }
  },

  /**
   * Get AI-friendly context for an entity
   */
  getAIContext: async (entityType: 'project' | 'team' | 'agent', entityId: number) => {
    try {
      const response = await api.get(`/api/v1/${entityType}s/${entityId}/ai-context`);
      return response.data;
    } catch (error) {
      console.warn('AI context API failed:', error);
      return {
        entity_type: entityType,
        entity_id: entityId,
        context: {},
        metadata: {
          generated_at: new Date().toISOString(),
          version: '1.0',
        },
      };
    }
  },

  /**
   * Generate team suggestions based on project context
   */
  generateTeamSuggestions: async (projectId: number) => {
    try {
      const response = await api.post(`/api/v1/projects/${projectId}/generate-teams`);
      return response.data;
    } catch (error) {
      console.warn('Team generation API failed, returning mock suggestions:', error);
      return {
        suggested_teams: [
          {
            name: 'Frontend Development Team',
            team_type: 'frontend',
            specialization: 'User interface and experience',
            suggested_agents: [
              { role: 'Frontend Developer', agent_type: 'developer' },
              { role: 'UI/UX Designer', agent_type: 'designer' },
            ],
          },
          {
            name: 'Backend Development Team',
            team_type: 'backend',
            specialization: 'API and data management',
            suggested_agents: [
              { role: 'Backend Developer', agent_type: 'developer' },
              { role: 'Database Specialist', agent_type: 'developer' },
            ],
          },
        ],
      };
    }
  },

  /**
   * Generate agent suggestions based on team context
   */
  generateAgentSuggestions: async (teamId: number) => {
    try {
      const response = await api.post(`/api/v1/teams/${teamId}/generate-agents`);
      return response.data;
    } catch (error) {
      console.warn('Agent generation API failed, returning mock suggestions:', error);
      return {
        suggested_agents: [
          {
            name: 'Agent_Frontend_Dev_1',
            role: 'Frontend Developer',
            agent_type_id: 2,
            skills: ['react', 'typescript', 'css'],
            experience_level: 'senior',
          },
          {
            name: 'Agent_UI_Designer_1',
            role: 'UI/UX Designer',
            agent_type_id: 4,
            skills: ['figma', 'user_research', 'design_systems'],
            experience_level: 'mid',
          },
        ],
      };
    }
  },
};