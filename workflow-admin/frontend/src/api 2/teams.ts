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
  project_id: number;
  context: TeamContext;
  // Inherited context from project
  project_context?: any;
  full_context?: any; // Combined project + team context for AI consumption
  lead_agent_id?: number;
  member_agent_ids?: number[];
  status: string;
  capacity: number;
  current_workload: number;
  created_at: string;
  updated_at?: string;
  // Computed fields
  agent_count?: number;
  completion_percentage?: number;
}

export const teamsApi = {
  getTeams: async (): Promise<Team[]> => {
    try {
      const response = await api.get('/api/v1/teams/');
      return response.data.items || response.data || [];
    } catch (error) {
      console.warn('Teams API failed, returning mock data:', error);
      return [
        {
          id: 1,
          name: 'Core AgentTeam Development',
          description: 'Primary AI agent team for multi-agent system development and requirements gathering',
          project_id: 1,
          lead_agent_id: 1, // AgentIan (Product Owner)
          member_agent_ids: [1, 2], // AgentIan + AgentPete
          configuration: {
            collaboration_mode: 'sequential',
            workflow_handoff: {
              product_owner_to_developer: {
                trigger: 'stories_created',
                assignment_field: 'agentpete'
              }
            },
            communication_channels: {
              primary: 'slack',
              coordination: 'jira_comments',
              escalation: 'direct_api'
            },
            performance_tracking: {
              story_completion_rate: true,
              estimation_accuracy: true,
              stakeholder_satisfaction: true
            }
          },
          status: 'active',
          created_at: new Date().toISOString(),
        },
        {
          id: 2,
          name: 'Workflow Admin UI Team',
          description: 'Agent team focused on workflow management interface development',
          project_id: 2,
          lead_agent_id: 2, // AgentPete (Developer lead)
          member_agent_ids: [2], // Just AgentPete for now
          configuration: {
            specialization: 'frontend_development',
            workflow_focus: 'crud_operations',
            tech_stack_alignment: {
              frontend: ['react', 'typescript'],
              integration: 'backend_api',
              testing_approach: 'component_based'
            },
            development_approach: {
              methodology: 'agile',
              iteration_length: 'weekly',
              code_review: 'automated_and_manual'
            }
          },
          status: 'active',
          created_at: new Date().toISOString(),
        },
        {
          id: 3,
          name: 'Future QA Team',
          description: 'Planned testing and quality assurance team with AgentSarah',
          project_id: 3,
          lead_agent_id: 3, // Future AgentSarah
          member_agent_ids: [], // To be populated when AgentSarah is activated
          configuration: {
            testing_philosophy: 'shift_left',
            automation_strategy: 'test_pyramid',
            quality_gates: {
              unit_test_coverage: 85,
              integration_test_coverage: 70,
              e2e_test_coverage: 40
            },
            tool_integration: {
              test_management: 'jira',
              automation: ['cypress', 'jest'],
              performance: 'k6'
            }
          },
          status: 'planning',
          created_at: new Date().toISOString(),
        },
      ];
    }
  },

  getTeam: async (id: number): Promise<Team> => {
    try {
      const response = await api.get(`/api/v1/teams/${id}`);
      return response.data;
    } catch (error) {
      throw new Error(`Failed to fetch team ${id}`);
    }
  },
};