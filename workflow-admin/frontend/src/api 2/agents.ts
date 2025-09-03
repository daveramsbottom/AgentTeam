import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Types for Agent entities
export interface AgentType {
  id: number;
  name: string;
  description?: string;
  capabilities: any;
  workflow_preferences?: any;
  default_config?: any;
  is_active: boolean;
  created_at: string;
  updated_at?: string;
}

export interface AgentContext {
  role: string;
  responsibilities: string[];
  skills_required: {
    technical: string[];
    soft_skills: string[];
    domain_knowledge: string[];
  };
  experience_level: 'junior' | 'mid' | 'senior' | 'lead' | 'principal';
  workflow_template: string;
  performance_metrics: {
    individual_kpis: Record<string, any>;
    success_measures: string[];
  };
  collaboration_style: {
    communication_preference: string;
    meeting_frequency: string;
    review_participation: boolean;
  };
  decision_authority: {
    autonomous_decisions: string[];
    requires_approval: string[];
  };
  escalation_rules: {
    technical_issues: string;
    timeline_concerns: string;
    quality_concerns: string;
  };
  learning_objectives?: string[];
}

export interface Agent {
  id: number;
  name: string;
  agent_type_id: number;
  team_id?: number;
  description?: string;
  context: AgentContext;
  // Inherited contexts
  project_context?: any;
  team_context?: any;
  full_context?: any; // Combined project + team + agent context for AI consumption
  configuration?: any;
  credentials?: any;
  status: string;
  workload_capacity: number;
  current_workload: number;
  specializations?: any;
  performance_metrics?: any;
  last_active?: string;
  created_at: string;
  updated_at?: string;
  // Populated from relationships
  agent_type?: AgentType;
  team?: any;
}

// API functions with mock data fallbacks
export const agentsApi = {
  // Get all agents
  getAgents: async (): Promise<Agent[]> => {
    try {
      const response = await api.get('/api/v1/agents/');
      return response.data.items || response.data || [];
    } catch (error) {
      // Return mock data if API fails
      console.warn('API failed, returning mock data:', error);
      return [
        {
          id: 1,
          name: 'AgentIan',
          agent_type_id: 1,
          description: 'Product Owner agent specialized in e-commerce and fintech requirements',
          configuration: {
            communication_style: 'business_focused',
            domain_expertise: ['e-commerce', 'fintech', 'user_experience'],
            clarification_depth: 'thorough',
            story_complexity_preference: 'detailed'
          },
          specializations: {
            industry_knowledge: ['retail', 'banking', 'payments'],
            stakeholder_types: ['business_users', 'product_managers', 'executives'],
            project_scales: ['enterprise', 'mid-market']
          },
          status: 'active',
          workload_capacity: 5,
          current_workload: 2,
          performance_metrics: {
            avg_stories_per_session: 8,
            clarification_efficiency: 85,
            stakeholder_satisfaction: 4.2
          },
          last_active: new Date(Date.now() - 1000 * 60 * 30).toISOString(), // 30 minutes ago
          created_at: new Date().toISOString(),
        },
        {
          id: 2,
          name: 'AgentPete',
          agent_type_id: 2,
          description: 'Senior Developer agent with full-stack web development expertise',
          configuration: {
            tech_stack_preference: ['javascript', 'typescript', 'react', 'node', 'python'],
            estimation_approach: 'fibonacci_story_points',
            architecture_style: 'microservices_preferred',
            code_review_strictness: 'high'
          },
          specializations: {
            technologies: ['react', 'node.js', 'postgresql', 'redis', 'docker'],
            patterns: ['clean_architecture', 'domain_driven_design', 'tdd'],
            project_types: ['web_applications', 'apis', 'data_processing']
          },
          status: 'active',
          workload_capacity: 3,
          current_workload: 1,
          performance_metrics: {
            avg_estimation_accuracy: 92,
            technical_debt_score: 15,
            implementation_success_rate: 94
          },
          last_active: new Date(Date.now() - 1000 * 60 * 5).toISOString(), // 5 minutes ago
          created_at: new Date().toISOString(),
        },
        {
          id: 3,
          name: 'AgentSarah',
          agent_type_id: 3,
          description: 'QA agent specialized in automated testing and quality assurance',
          configuration: {
            testing_philosophy: 'shift_left',
            automation_coverage_target: 85,
            test_pyramid_approach: true,
            performance_testing: true
          },
          specializations: {
            testing_types: ['unit', 'integration', 'e2e', 'performance', 'security'],
            tools: ['jest', 'cypress', 'selenium', 'k6', 'sonarqube'],
            methodologies: ['bdd', 'tdd', 'risk_based_testing']
          },
          status: 'inactive',
          workload_capacity: 4,
          current_workload: 0,
          performance_metrics: {
            bug_detection_rate: 87,
            test_coverage_achieved: 88,
            automation_efficiency: 76
          },
          last_active: new Date(Date.now() - 1000 * 60 * 60 * 24 * 3).toISOString(), // 3 days ago
          created_at: new Date().toISOString(),
        },
      ];
    }
  },

  // Get agent by ID
  getAgent: async (id: number): Promise<Agent> => {
    try {
      const response = await api.get(`/api/v1/agents/${id}`);
      return response.data;
    } catch (error) {
      throw new Error(`Failed to fetch agent ${id}`);
    }
  },

  // Get all agent types
  getAgentTypes: async (): Promise<AgentType[]> => {
    try {
      const response = await api.get('/api/v1/agents/types/');
      return response.data.items || response.data || [];
    } catch (error) {
      // Return mock data if API fails
      console.warn('API failed, returning mock data:', error);
      return [
        {
          id: 1,
          name: 'Product Owner',
          description: 'AI Product Owner with requirements gathering workflow',
          capabilities: { 
            slack_communication: true, 
            jira_integration: true, 
            project_analysis: true,
            stakeholder_interaction: true,
            story_creation: true
          },
          workflow_preferences: {
            default_workflow: 'product_owner_workflow',
            stages: ['analyze_goal', 'seek_clarification', 'break_down_stories', 'create_stories', 'assign_tasks'],
            timeout_settings: { clarification_wait: 300, max_iterations: 5 }
          },
          default_config: {
            communication_style: 'professional',
            clarification_depth: 'detailed',
            story_format: 'atlassian_adf'
          },
          is_active: true,
          created_at: new Date().toISOString(),
        },
        {
          id: 2,
          name: 'Developer',
          description: 'AI Senior Developer with technical analysis workflow',
          capabilities: { 
            code_analysis: true, 
            technical_estimation: true, 
            architecture_planning: true,
            technology_recommendations: true,
            implementation_planning: true
          },
          workflow_preferences: {
            default_workflow: 'developer_workflow',
            stages: ['analyze_task', 'extract_requirements', 'assess_complexity', 'estimate_effort', 'plan_implementation', 'update_task'],
            monitoring_interval: 60
          },
          default_config: {
            estimation_approach: 'story_points',
            risk_assessment: true,
            tech_stack_recommendations: true
          },
          is_active: true,
          created_at: new Date().toISOString(),
        },
        {
          id: 3,
          name: 'Tester',
          description: 'AI Quality Assurance with testing workflow',
          capabilities: { 
            test_planning: true, 
            quality_assurance: true,
            bug_tracking: true,
            test_automation_planning: true
          },
          workflow_preferences: {
            default_workflow: 'tester_workflow',
            stages: ['analyze_requirements', 'create_test_plan', 'design_test_cases', 'track_defects', 'validate_fixes'],
            automation_preference: true
          },
          default_config: {
            testing_approach: 'bdd',
            coverage_requirements: 80,
            automation_frameworks: ['selenium', 'jest', 'cypress']
          },
          is_active: false,
          created_at: new Date().toISOString(),
        },
        {
          id: 4,
          name: 'DevOps',
          description: 'AI DevOps Engineer with deployment workflow',
          capabilities: { 
            infrastructure_management: true, 
            ci_cd_pipeline: true,
            monitoring_setup: true,
            security_scanning: true
          },
          workflow_preferences: {
            default_workflow: 'devops_workflow',
            stages: ['assess_infrastructure', 'design_pipeline', 'configure_deployment', 'setup_monitoring', 'security_review'],
            cloud_providers: ['aws', 'azure', 'gcp']
          },
          default_config: {
            deployment_strategy: 'blue_green',
            monitoring_tools: ['prometheus', 'grafana'],
            security_scanning: true
          },
          is_active: false,
          created_at: new Date().toISOString(),
        },
      ];
    }
  },

  // Get agent type by ID
  getAgentType: async (id: number): Promise<AgentType> => {
    try {
      const response = await api.get(`/api/v1/agents/types/${id}`);
      return response.data;
    } catch (error) {
      throw new Error(`Failed to fetch agent type ${id}`);
    }
  },
};