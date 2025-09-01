import { ProjectContext } from './projects';
import { TeamContext } from './teams';
import { AgentContext } from './agents';

/**
 * Context inheritance and merging utilities for AI-friendly context management
 */

export interface InheritedContext {
  project: ProjectContext;
  team?: TeamContext;
  agent?: AgentContext;
  merged: any; // Flattened context for AI consumption
}

/**
 * Merges project, team, and agent contexts into a single AI-friendly context
 */
export function mergeContexts(
  projectContext: ProjectContext,
  teamContext?: TeamContext,
  agentContext?: AgentContext
): any {
  const merged: any = {
    // Project-level context (root)
    project: {
      purpose: projectContext.purpose,
      scope: projectContext.scope,
      limitations: projectContext.limitations,
      requirements: projectContext.requirements,
      success_criteria: projectContext.success_criteria,
      stakeholders: projectContext.stakeholders,
      timeline: projectContext.timeline,
      technology_preferences: projectContext.technology_preferences,
      compliance_requirements: projectContext.compliance_requirements,
    },
  };

  // Add team context if available
  if (teamContext) {
    merged.team = {
      type: teamContext.team_type,
      specialization: teamContext.specialization,
      responsibilities: teamContext.responsibilities,
      deliverables: teamContext.deliverables,
      technology_stack: teamContext.technology_stack,
      methodology: teamContext.methodology,
      quality_standards: teamContext.quality_standards,
      dependencies: teamContext.dependencies,
    };

    // Merge technology preferences
    merged.effective_technology_stack = {
      ...merged.project.technology_preferences,
      ...teamContext.technology_stack,
    };
  }

  // Add agent context if available
  if (agentContext) {
    merged.agent = {
      role: agentContext.role,
      responsibilities: agentContext.responsibilities,
      skills_required: agentContext.skills_required,
      experience_level: agentContext.experience_level,
      workflow_template: agentContext.workflow_template,
      collaboration_style: agentContext.collaboration_style,
      decision_authority: agentContext.decision_authority,
      escalation_rules: agentContext.escalation_rules,
    };

    // Create AI-friendly flattened context
    merged.ai_context = {
      // High-level context
      project_purpose: merged.project.purpose,
      project_scope: merged.project.scope,
      team_type: merged.team?.type,
      agent_role: merged.agent.role,
      
      // Combined responsibilities
      all_responsibilities: [
        ...(merged.team?.responsibilities || []),
        ...merged.agent.responsibilities,
      ],
      
      // Technology context
      technology_stack: merged.effective_technology_stack,
      
      // Decision-making context
      can_decide_autonomously: merged.agent.decision_authority.autonomous_decisions,
      must_escalate: merged.agent.decision_authority.requires_approval,
      
      // Performance context
      success_criteria: merged.project.success_criteria,
      quality_standards: merged.team?.quality_standards,
      performance_metrics: agentContext.performance_metrics,
      
      // Workflow context
      workflow_template: merged.agent.workflow_template,
      methodology: merged.team?.methodology,
      
      // Communication context
      stakeholders: merged.project.stakeholders,
      communication_tools: merged.team?.communication_preferences?.tools,
      escalation_paths: merged.agent.escalation_rules,
    };
  }

  return merged;
}

/**
 * Validates context inheritance and identifies missing required fields
 */
export function validateContext(
  projectContext: ProjectContext,
  teamContext?: TeamContext,
  agentContext?: AgentContext
): { valid: boolean; errors: string[] } {
  const errors: string[] = [];

  // Validate project context
  if (!projectContext.purpose) errors.push('Project purpose is required');
  if (!projectContext.scope) errors.push('Project scope is required');
  if (!projectContext.requirements) errors.push('Project requirements are required');

  // Validate team context if provided
  if (teamContext) {
    if (!teamContext.team_type) errors.push('Team type is required');
    if (!teamContext.responsibilities?.length) errors.push('Team responsibilities are required');
    if (!teamContext.technology_stack) errors.push('Team technology stack is required');
  }

  // Validate agent context if provided
  if (agentContext) {
    if (!agentContext.role) errors.push('Agent role is required');
    if (!agentContext.responsibilities?.length) errors.push('Agent responsibilities are required');
    if (!agentContext.workflow_template) errors.push('Agent workflow template is required');
  }

  // Check for conflicts
  if (teamContext && agentContext) {
    // Ensure agent technology skills align with team stack
    const teamTech = teamContext.technology_stack.primary_languages;
    const agentSkills = agentContext.skills_required.technical;
    const hasAlignment = teamTech.some(tech => 
      agentSkills.some(skill => skill.toLowerCase().includes(tech.toLowerCase()))
    );
    
    if (!hasAlignment) {
      errors.push('Agent technical skills should align with team technology stack');
    }
  }

  return {
    valid: errors.length === 0,
    errors,
  };
}

/**
 * Generates context suggestions based on project type and team composition
 */
export function generateContextSuggestions(
  projectType: string,
  teamTypes: string[]
): {
  suggestedTechnologies: string[];
  suggestedRoles: string[];
  suggestedMethodology: string;
} {
  const suggestions: any = {
    web_application: {
      technologies: ['react', 'typescript', 'node.js', 'postgresql', 'docker'],
      roles: ['frontend_developer', 'backend_developer', 'ui_designer', 'devops_engineer'],
      methodology: 'agile',
    },
    mobile_app: {
      technologies: ['react_native', 'swift', 'kotlin', 'firebase', 'rest_api'],
      roles: ['mobile_developer', 'ui_designer', 'backend_developer', 'qa_engineer'],
      methodology: 'scrum',
    },
    data_platform: {
      technologies: ['python', 'spark', 'kafka', 'elasticsearch', 'kubernetes'],
      roles: ['data_engineer', 'ml_engineer', 'backend_developer', 'devops_engineer'],
      methodology: 'kanban',
    },
  };

  const suggestion = suggestions[projectType] || suggestions.web_application;
  
  return {
    suggestedTechnologies: suggestion.technologies,
    suggestedRoles: suggestion.roles,
    suggestedMethodology: suggestion.methodology,
  };
}

export const contextApi = {
  /**
   * Get full inherited context for an entity
   */
  getFullContext: async (entityType: 'project' | 'team' | 'agent', entityId: number) => {
    // This would call the appropriate API endpoints to build the full context
    // For now, return mock structure
    return {
      entity_type: entityType,
      entity_id: entityId,
      inherited_context: {},
      validation: { valid: true, errors: [] },
    };
  },

  /**
   * Validate context inheritance
   */
  validateContextInheritance: async (
    projectId: number,
    teamId?: number,
    agentId?: number
  ) => {
    // Mock validation - in real implementation would fetch contexts and validate
    return {
      valid: true,
      errors: [],
      suggestions: [],
    };
  },
};