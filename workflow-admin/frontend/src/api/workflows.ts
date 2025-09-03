import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export interface WorkflowTemplate {
  id: number;
  name: string;
  description?: string;
  agent_type: string; // Links to AgentType.name
  version: string;
  is_active: boolean;
  is_default: boolean; // Default version for this agent type
  definition: WorkflowDefinition;
  created_at: string;
  updated_at?: string;
  created_by?: string;
  change_notes?: string;
}

export interface WorkflowDefinition {
  workflow_type: 'agent_workflow';
  agent_type: string;
  stages: WorkflowStage[];
  monitoring?: {
    continuous_monitoring: boolean;
    check_interval: number;
    trigger_conditions: string[];
  };
  automation_support?: boolean;
  total_estimated_time: string;
  success_criteria: string[];
}

export interface ContextReference {
  id: string;
  name: string;
  type: 'project' | 'team' | 'agent' | 'domain' | 'technical';
  description: string;
  content: string;
  tags?: string[];
}

export interface StageContextConfig {
  // Optional: Override the agent's default behavior for this specific stage
  stage_specific_guidance?: string;
  
  // Optional: Which contexts to include/exclude for this decision
  context_selection?: {
    include_references?: string[]; // Context IDs to specifically include
    exclude_references?: string[]; // Context IDs to specifically exclude
    use_project_context?: boolean; // Default: true
    use_team_context?: boolean; // Default: true  
    use_agent_context?: boolean; // Default: true
  };
  
  // Optional: Fine-tune AI behavior for this specific stage
  ai_tuning?: {
    temperature?: number;
    max_tokens?: number;
    response_format?: 'text' | 'json' | 'markdown';
    focus_instruction?: string; // "Focus only on security aspects" or "Ignore UI concerns"
  };
  
  // Optional: Examples specific to this stage's decision
  stage_examples?: {
    description: string;
    input_example: any;
    expected_output: any;
  }[];
}

export interface WorkflowStage {
  name: string;
  description: string;
  inputs: string[];
  outputs: string[];
  ai_prompts?: string[];
  integrations?: string[];
  timeout: number;
  conditions?: {
    required?: string[];
    optional?: string[];
  };
  
  // New hierarchical context system
  context_config?: StageContextConfig;
  
  retry_config?: {
    max_retries: number;
    backoff_strategy: 'linear' | 'exponential';
    retry_conditions: string[];
  };
}

// Legacy Workflow interface for backward compatibility
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

// Mock context references that show the hierarchy
const mockContextReferences: ContextReference[] = [
  {
    id: 'project_ecommerce_tech',
    name: 'E-commerce Tech Stack',
    type: 'project',
    description: 'Technical guidelines specific to our e-commerce platform',
    content: 'Tech Stack: React 18, Node.js 18, PostgreSQL 14, Redis, Docker. APIs: REST with OpenAPI 3.0. Authentication: JWT with refresh tokens. Payment: Stripe integration required.',
    tags: ['tech-stack', 'ecommerce', 'architecture']
  },
  {
    id: 'project_ecommerce_business',
    name: 'E-commerce Business Rules',
    type: 'project',  
    description: 'Business logic and rules for e-commerce decisions',
    content: 'Business Rules: All prices in USD. Tax calculation required for US states. Inventory must be checked before order confirmation. Free shipping over $50. Return window: 30 days.',
    tags: ['business', 'ecommerce', 'pricing']
  },
  {
    id: 'team_backend_focus',
    name: 'Backend Team Context',
    type: 'team',
    description: 'Backend-specific concerns and priorities',
    content: 'Focus Areas: API performance, database optimization, security, scalability. Avoid: UI/UX decisions, frontend styling, client-side validation specifics. Prioritize: Server performance, data integrity, security best practices.',
    tags: ['backend', 'api', 'database', 'security']
  },
  {
    id: 'team_frontend_focus', 
    name: 'Frontend Team Context',
    type: 'team',
    description: 'Frontend-specific concerns and priorities', 
    content: 'Focus Areas: User experience, responsive design, accessibility, client performance. Avoid: Database schema decisions, server architecture, deployment strategies. Prioritize: Component reusability, user workflows, mobile experience.',
    tags: ['frontend', 'ui', 'ux', 'accessibility']
  },
  {
    id: 'domain_security_compliance',
    name: 'Security & Compliance Requirements',
    type: 'domain',
    description: 'Security and compliance guidelines that may apply selectively',
    content: 'Security: All user inputs must be sanitized. PII data encryption at rest. HTTPS only. Password policies: min 8 chars, complexity required. GDPR: User consent tracking, right to deletion. PCI DSS: No card data storage.',
    tags: ['security', 'compliance', 'gdpr', 'pci']
  },
  {
    id: 'domain_performance_guidelines',
    name: 'Performance Guidelines',
    type: 'domain', 
    description: 'Performance targets and optimization guidance',
    content: 'Performance Targets: Page load < 2s, API response < 200ms, Database queries < 50ms. Optimization: Image compression, lazy loading, CDN usage, database indexing, caching strategies.',
    tags: ['performance', 'optimization', 'metrics']
  }
];

export const workflowsApi = {
  getContextReferences: async (): Promise<ContextReference[]> => {
    return mockContextReferences;
  },

  // Workflow Templates API
  getWorkflowTemplates: async (): Promise<WorkflowTemplate[]> => {
    const response = await api.get('/api/v1/workflow-templates/');
    return response.data.items || response.data || [];
  },

  getWorkflowTemplate: async (id: number): Promise<WorkflowTemplate> => {
    const templates = await workflowsApi.getWorkflowTemplates();
    const template = templates.find(t => t.id === id);
    if (!template) {
      throw new Error(`Workflow template ${id} not found`);
    }
    return template;
  },

  getWorkflowsByAgentType: async (agentType: string): Promise<WorkflowTemplate[]> => {
    const templates = await workflowsApi.getWorkflowTemplates();
    return templates.filter(t => t.agent_type === agentType).sort((a, b) => {
      // Sort by default first, then by version descending
      if (a.is_default && !b.is_default) return -1;
      if (!a.is_default && b.is_default) return 1;
      return b.version.localeCompare(a.version);
    });
  },

  // Legacy workflow API
  getWorkflows: async (): Promise<Workflow[]> => {
    const response = await api.get('/api/v1/workflows/');
    return response.data.items || response.data || [];
  },

  getWorkflow: async (id: number): Promise<Workflow> => {
    const response = await api.get(`/api/v1/workflows/${id}`);
    return response.data;
  },
};