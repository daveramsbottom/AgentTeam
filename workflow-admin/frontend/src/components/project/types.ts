/**
 * Shared types and interfaces for project-related components
 */

export interface TeamMember {
  id: number;
  name: string;
  role: string;
  status: 'active' | 'idle' | 'busy';
  specialization: string;
  workflow_version?: string;
  workflow_id?: number;
}

export interface TeamSummary {
  id: number;
  name: string;
  agent_count: number;
  lead_agent?: string;
  specialization?: string;
  members?: TeamMember[];
}

export interface ProjectContext {
  tech_stack?: string[];
  compliance_rules?: string[];
  security_standards?: string[];
  business_guidelines?: string[];
  version?: string;
  last_updated?: string;
}

export interface ProjectDetailsProps {
  project: any; // Use the actual Project type from API
  teams: TeamSummary[];
  agents: any[]; // Use the actual Agent type from API
  isEditMode: boolean;
  onEditModeToggle: () => void;
  onBack: () => void;
  onWorkflowNavigation: (workflowId: number, memberName: string, role: string) => void;
}

export interface TeamManagementProps {
  project: any;
  teams: TeamSummary[];
  agents: any[];
  isEditMode: boolean;
  onTeamsUpdate: (teams: TeamSummary[]) => void;
  expandedTeams: Set<number>;
  onToggleTeamExpansion: (teamId: number) => void;
  onWorkflowNavigation: (workflowId: number, memberName: string, role: string) => void;
}

export interface TeamModalProps {
  open: boolean;
  agents: any[];
  onClose: () => void;
  onSubmit: (teamData: any) => Promise<void>;
  loading: boolean;
}

export interface EditTeamModalProps extends TeamModalProps {
  team: TeamSummary | null;
}

export interface ProjectContextEditorProps {
  project: any;
  isEditMode: boolean;
  editingContext: boolean;
  tempContext: string;
  onStartEditing: () => void;
  onSaveContext: () => Promise<void>;
  onCancelEditing: () => void;
  onContextChange: (value: string) => void;
}