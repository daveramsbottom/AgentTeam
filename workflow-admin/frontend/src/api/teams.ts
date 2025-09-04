import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export interface TeamContext {
  team_type: 'frontend' | 'backend' | 'mobile' | 'devops' | 'data' | 'qa' | 'design';
  specialization: string;
  responsibilities: string[];
  deliverables: string[];
  dependencies: {
    internal_teams: string[];
    external_services: string[];
    data_dependencies: string[];
  };
  technology_stack: {
    primary_languages: string[];
    frameworks: string[];
    tools: string[];
    infrastructure: string[];
  };
  methodology: 'agile' | 'scrum' | 'kanban' | 'waterfall' | 'lean';
  communication_preferences: {
    daily_standup: boolean;
    sprint_planning: boolean;
    retrospectives: boolean;
    tools: string[];
  };
  quality_standards: {
    code_coverage_threshold: number;
    testing_requirements: string[];
    review_requirements: string[];
  };
  performance_targets: {
    velocity: number;
    cycle_time: number;
    defect_rate: number;
  };
}

export interface Team {
  id: number;
  name: string;
  description?: string;
  project_id?: number;
  team_lead_id?: number;
  configuration?: any;
  created_at: string;
  updated_at?: string;
  is_active: boolean;
  // Legacy fields for compatibility with mock data
  context?: TeamContext;
  lead_agent_id?: number;
  member_agent_ids?: number[];
  status?: string;
  capacity?: number;
  current_workload?: number;
  agent_count?: number;
  completion_percentage?: number;
}

export interface CreateTeamRequest {
  name: string;
  description?: string;
  project_id: number;
  team_lead_id?: number;
  member_agent_ids?: number[];
  configuration?: any;
}

export interface UpdateTeamRequest {
  name: string;
  description?: string;
  team_lead_id?: number;
  member_agent_ids?: number[];
  configuration?: any;
}

export const teamsApi = {
  createTeam: async (teamData: CreateTeamRequest): Promise<Team> => {
    const response = await api.post('/api/v1/teams/', teamData);
    return response.data;
  },

  updateTeam: async (id: number, teamData: UpdateTeamRequest): Promise<Team> => {
    const response = await api.put(`/api/v1/teams/${id}`, teamData);
    return response.data;
  },

  getTeams: async (): Promise<Team[]> => {
    const response = await api.get('/api/v1/teams/');
    const teams = response.data || [];
    
    // Default context structure for teams without configuration
    const defaultContext = {
      team_type: 'general',
      specialization: 'General purpose team',
      responsibilities: ['Team collaboration', 'Task coordination'],
      deliverables: ['Project deliverables', 'Team outputs'],
      dependencies: {
        internal_teams: [],
        external_services: [],
        data_dependencies: []
      },
      technology_stack: {
        primary_languages: ['JavaScript'],
        frameworks: ['React'],
        tools: ['Git', 'VS Code'],
        infrastructure: ['Docker']
      },
      methodology: 'agile',
      communication_preferences: {
        daily_standup: true,
        sprint_planning: true,
        retrospectives: true,
        tools: ['Slack', 'Email']
      },
      quality_standards: {
        code_coverage_threshold: 80,
        testing_requirements: ['Unit tests'],
        review_requirements: ['Code review']
      },
      performance_targets: {
        velocity: 8,
        cycle_time: 2,
        defect_rate: 0.05
      }
    };

    // Transform database teams to include legacy fields for compatibility
    const transformedTeams = teams.map((team: any) => ({
      ...team,
      lead_agent_id: team.team_lead_id,
      status: team.is_active ? 'active' : 'inactive',
      capacity: 1, // Default capacity
      current_workload: 0.5, // Default workload
      context: team.configuration || defaultContext, // Use configuration or default context
    }));
    
    return transformedTeams;
  },

  getTeam: async (id: number): Promise<Team> => {
    const response = await api.get(`/api/v1/teams/${id}`);
    const team = response.data;
    
    // Default context structure for teams without configuration
    const defaultContext = {
      team_type: 'general',
      specialization: 'General purpose team',
      responsibilities: ['Team collaboration', 'Task coordination'],
      deliverables: ['Project deliverables', 'Team outputs'],
      dependencies: {
        internal_teams: [],
        external_services: [],
        data_dependencies: []
      },
      technology_stack: {
        primary_languages: ['JavaScript'],
        frameworks: ['React'],
        tools: ['Git', 'VS Code'],
        infrastructure: ['Docker']
      },
      methodology: 'agile',
      communication_preferences: {
        daily_standup: true,
        sprint_planning: true,
        retrospectives: true,
        tools: ['Slack', 'Email']
      },
      quality_standards: {
        code_coverage_threshold: 80,
        testing_requirements: ['Unit tests'],
        review_requirements: ['Code review']
      },
      performance_targets: {
        velocity: 8,
        cycle_time: 2,
        defect_rate: 0.05
      }
    };

    // Apply the same transformation as getTeams with default context structure
    const transformedTeam = {
      ...team,
      lead_agent_id: team.team_lead_id,
      status: team.is_active ? 'active' : 'inactive',
      capacity: 1, // Default capacity
      current_workload: 0.5, // Default workload
      context: team.configuration || defaultContext, // Use configuration or default context
    };
    
    return transformedTeam;
  },
};