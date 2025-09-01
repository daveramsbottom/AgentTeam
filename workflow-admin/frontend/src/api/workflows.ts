import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export interface Workflow {
  id: number;
  name: string;
  description?: string;
  project_id: number;
  assigned_team_id?: number;
  primary_agent_id?: number;
  definition: any;
  status: string;
  priority: string;
  created_at: string;
  updated_at?: string;
}

export const workflowsApi = {
  getWorkflows: async (): Promise<Workflow[]> => {
    try {
      const response = await api.get('/api/v1/workflows/');
      return response.data.items || response.data || [];
    } catch (error) {
      console.warn('Workflows API failed, returning mock data:', error);
      return [
        {
          id: 1,
          name: 'Product Owner Workflow Template',
          description: 'Core workflow for AI Product Owner agents (AgentIan pattern)',
          project_id: 1,
          assigned_team_id: 1,
          primary_agent_id: 1,
          definition: {
            workflow_type: 'agent_workflow',
            agent_type: 'product_owner',
            stages: [
              {
                name: 'analyze_goal',
                description: 'Analyze project goal and assess complexity',
                inputs: ['project_description', 'stakeholder_input'],
                outputs: ['complexity_assessment', 'project_type_suggestion'],
                ai_prompts: ['project_analysis_prompt'],
                timeout: 30
              },
              {
                name: 'seek_clarification', 
                description: 'Generate and ask clarification questions via Slack',
                inputs: ['complexity_assessment'],
                outputs: ['clarification_responses', 'enhanced_requirements'],
                integrations: ['slack', 'ai_text_improvement'],
                timeout: 300
              },
              {
                name: 'break_down_stories',
                description: 'Break down requirements into user stories',
                inputs: ['enhanced_requirements'],
                outputs: ['user_stories_list'],
                ai_prompts: ['story_breakdown_prompt'],
                timeout: 60
              },
              {
                name: 'create_stories',
                description: 'Create formatted user stories in Jira',
                inputs: ['user_stories_list'],
                outputs: ['jira_story_ids'],
                integrations: ['jira', 'atlassian_adf'],
                timeout: 120
              },
              {
                name: 'assign_tasks',
                description: 'Assign created stories to appropriate developers',
                inputs: ['jira_story_ids', 'team_members'],
                outputs: ['assignment_confirmations'],
                integrations: ['jira'],
                timeout: 30
              }
            ],
            total_estimated_time: '8-15 minutes',
            success_criteria: ['stories_created', 'tasks_assigned', 'stakeholder_approved']
          },
          status: 'active',
          priority: 'high',
          created_at: new Date().toISOString(),
        },
        {
          id: 2,
          name: 'Developer Workflow Template',
          description: 'Core workflow for AI Developer agents (AgentPete pattern)',
          project_id: 1,
          assigned_team_id: 1,
          primary_agent_id: 2,
          definition: {
            workflow_type: 'agent_workflow',
            agent_type: 'developer',
            stages: [
              {
                name: 'analyze_task',
                description: 'Analyze assigned Jira task for technical requirements',
                inputs: ['jira_task_id', 'task_description'],
                outputs: ['technical_analysis', 'requirement_extraction'],
                integrations: ['jira'],
                timeout: 45
              },
              {
                name: 'extract_requirements',
                description: 'Extract detailed technical requirements using AI',
                inputs: ['technical_analysis'],
                outputs: ['detailed_requirements', 'acceptance_criteria'],
                ai_prompts: ['requirement_extraction_prompt'],
                timeout: 60
              },
              {
                name: 'assess_complexity',
                description: 'Assess technical complexity and identify risks',
                inputs: ['detailed_requirements'],
                outputs: ['complexity_score', 'risk_factors'],
                ai_prompts: ['complexity_assessment_prompt'],
                timeout: 30
              },
              {
                name: 'estimate_effort',
                description: 'Provide effort estimation with confidence scoring',
                inputs: ['complexity_score', 'risk_factors'],
                outputs: ['effort_estimate', 'confidence_score'],
                ai_prompts: ['estimation_prompt'],
                timeout: 30
              },
              {
                name: 'plan_implementation',
                description: 'Create detailed implementation plan and tech recommendations',
                inputs: ['effort_estimate', 'detailed_requirements'],
                outputs: ['implementation_plan', 'tech_stack_recommendations'],
                ai_prompts: ['implementation_planning_prompt'],
                timeout: 90
              },
              {
                name: 'update_task',
                description: 'Update Jira task with analysis results and estimates',
                inputs: ['implementation_plan', 'effort_estimate'],
                outputs: ['jira_update_confirmation'],
                integrations: ['jira'],
                timeout: 30
              }
            ],
            monitoring: {
              continuous_monitoring: true,
              check_interval: 60,
              trigger_conditions: ['task_assigned_to_agent']
            },
            total_estimated_time: '5-8 minutes per task',
            success_criteria: ['task_analyzed', 'estimates_provided', 'jira_updated']
          },
          status: 'active',
          priority: 'critical',
          created_at: new Date().toISOString(),
        },
        {
          id: 3,
          name: 'Tester Workflow Template',
          description: 'Core workflow for AI Testing agents (future AgentSarah)',
          project_id: 2,
          assigned_team_id: 2,
          definition: {
            workflow_type: 'agent_workflow',
            agent_type: 'tester',
            stages: [
              {
                name: 'analyze_requirements',
                description: 'Analyze user stories and acceptance criteria for testing',
                inputs: ['user_story', 'acceptance_criteria'],
                outputs: ['test_requirements', 'risk_analysis'],
                timeout: 45
              },
              {
                name: 'create_test_plan',
                description: 'Generate comprehensive test plan with coverage analysis',
                inputs: ['test_requirements'],
                outputs: ['test_plan', 'coverage_matrix'],
                ai_prompts: ['test_planning_prompt'],
                timeout: 60
              },
              {
                name: 'design_test_cases',
                description: 'Design detailed test cases including automation candidates',
                inputs: ['test_plan'],
                outputs: ['test_cases', 'automation_candidates'],
                ai_prompts: ['test_case_generation_prompt'],
                timeout: 90
              },
              {
                name: 'track_defects',
                description: 'Monitor and track defects throughout testing lifecycle',
                inputs: ['test_execution_results'],
                outputs: ['defect_reports', 'quality_metrics'],
                integrations: ['jira', 'test_management_tools'],
                timeout: 30
              },
              {
                name: 'validate_fixes',
                description: 'Validate bug fixes and regression testing',
                inputs: ['fixed_defects'],
                outputs: ['validation_results', 'regression_test_results'],
                timeout: 45
              }
            ],
            automation_support: true,
            total_estimated_time: '4-6 minutes per story',
            success_criteria: ['test_plan_created', 'test_cases_designed', 'quality_validated']
          },
          status: 'draft',
          priority: 'medium',
          created_at: new Date().toISOString(),
        },
      ];
    }
  },

  getWorkflow: async (id: number): Promise<Workflow> => {
    try {
      const response = await api.get(`/api/v1/workflows/${id}`);
      return response.data;
    } catch (error) {
      throw new Error(`Failed to fetch workflow ${id}`);
    }
  },
};