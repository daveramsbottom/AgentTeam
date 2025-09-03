# Entity Creation Development Workflow

## Overview
This guide provides a step-by-step workflow for implementing entity creation functionality across Projects, Agents, Teams, and Workflows. It builds on the established patterns from the Project creation implementation.

## Pre-Implementation Checklist

### 1. API Validation ✅ (Complete)
- [x] Run Newman API tests: `./api-tests/scripts/run-tests.sh`
- [x] Verify CRUD endpoints respond correctly
- [x] Confirm database relationships work
- [x] Validate request/response schemas

**Status**: All 15/15 assertions passing for all entity types

### 2. Component Analysis
Before implementing, examine existing dashboard components:
- **Projects**: Complete implementation at `frontend/src/components/ProjectDashboard.tsx`
- **Agents**: Basic dashboard at `frontend/src/components/AgentDashboard.tsx` 
- **Teams**: Basic dashboard at `frontend/src/components/TeamDashboard.tsx`
- **Workflows**: Basic dashboard at `frontend/src/components/WorkflowDashboard.tsx`

## Implementation Workflow

### Step 1: Update API Client
**File**: `frontend/src/api/{entityType}.ts`

Add the create method to the existing API client:

```typescript
// Example for agents.ts
export interface CreateAgentRequest {
  name: string;
  agent_type_id: number;
  project_id?: number;
  team_id?: number;
  description?: string;
  config?: any;
}

export const agentsApi = {
  // ... existing methods ...

  createAgent: async (agentData: CreateAgentRequest): Promise<Agent> => {
    const response = await api.post('/api/v1/agents/', agentData);
    return response.data;
  },
};
```

### Step 2: Define TypeScript Interfaces
**Location**: Top of dashboard component or separate interface file

Define form data and request interfaces:

```typescript
// Form data interface (UI state)
interface Create{EntityType}FormData {
  name: string;
  description: string;
  // Entity-specific fields
  // For agents: agent_type_id, project_id, team_id
  // For teams: project_id, lead_agent_id, description  
  // For workflows: project_id, description, steps
}
```

### Step 3: Add State Management
**Location**: Inside dashboard component

Add creation-related state variables:

```typescript
// Modal and form state
const [createModalOpen, setCreateModalOpen] = useState(false);
const [formData, setFormData] = useState<Create{EntityType}FormData>({
  // Initial values
});
const [formErrors, setFormErrors] = useState<Record<string, string>>({});
const [creating, setCreating] = useState(false);

// Action menu state (if not already present)
const [actionMenuAnchor, setActionMenuAnchor] = useState<null | HTMLElement>(null);
```

### Step 4: Implement Event Handlers
**Location**: Inside dashboard component

Add the standard handler functions:

```typescript
// Modal handlers
const handleCreateEntity = () => {
  setCreateModalOpen(true);
  handleActionMenuClose(); // if opened from menu
};

const handleModalClose = () => {
  setCreateModalOpen(false);
  setFormData({
    // Reset to initial values
  });
  setFormErrors({});
};

// Form change handler (reuse from ProjectDashboard pattern)
const handleFormChange = (field: string, value: any) => {
  // Copy implementation from ProjectDashboard.tsx:126-151
};

// Validation function
const validateForm = (): boolean => {
  const errors: Record<string, string> = {};
  
  // Add entity-specific validation rules
  if (!formData.name.trim()) {
    errors.name = '{EntityType} name is required';
  }
  
  setFormErrors(errors);
  return Object.keys(errors).length === 0;
};

// Submit handler
const handleSubmit = async () => {
  if (!validateForm()) return;
  
  setCreating(true);
  try {
    const newEntity = await {entityType}Api.create{EntityType}({
      // Map form data to API request format
    });
    
    // Update local state
    set{EntityType}s(prev => [newEntity, ...prev]);
    handleModalClose();
  } catch (err) {
    console.error(`Error creating {entityType}:`, err);
    setError(`Failed to create {entityType}. Please try again.`);
  } finally {
    setCreating(false);
  }
};
```

### Step 5: Add Horizontal Action Menu
**Location**: Dashboard component render method

If not already present, add the horizontal action menu:

```typescript
{/* Copy implementation from ProjectDashboard.tsx:253-315 */}
<Paper elevation={1} sx={{ mb: 3, p: 2 }}>
  <Box display="flex" alignItems="center" justifyContent="space-between">
    <Typography variant="h6" sx={{ fontWeight: 500 }}>
      Actions
    </Typography>
    <Box display="flex" gap={1}>
      <Button
        variant="contained"
        startIcon={<AddIcon />}
        onClick={handleCreate{EntityType}}
        sx={{ borderRadius: 2, textTransform: 'none' }}
      >
        Create {EntityType}
      </Button>
      {/* ... other actions ... */}
    </Box>
  </Box>
</Paper>
```

### Step 6: Implement Creation Modal
**Location**: End of dashboard component render method

Add the modal dialog with entity-specific form fields:

```typescript
{/* Creation Modal */}
<Dialog 
  open={createModalOpen} 
  onClose={handleModalClose}
  maxWidth="md"
  fullWidth
>
  <DialogTitle sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
    Create New {EntityType}
    <IconButton onClick={handleModalClose} size="small">
      <CloseIcon />
    </IconButton>
  </DialogTitle>
  <DialogContent dividers>
    <Stack spacing={3}>
      <TextField
        fullWidth
        label="{EntityType} Name"
        value={formData.name}
        onChange={(e) => handleFormChange('name', e.target.value)}
        error={!!formErrors.name}
        helperText={formErrors.name}
        required
      />
      
      {/* Add entity-specific fields */}
      
    </Stack>
  </DialogContent>
  <DialogActions sx={{ p: 2 }}>
    <Button onClick={handleModalClose} disabled={creating}>
      Cancel
    </Button>
    <Button 
      onClick={handleSubmit} 
      variant="contained"
      disabled={creating}
      startIcon={creating ? <CircularProgress size={16} /> : <AddIcon />}
    >
      {creating ? 'Creating...' : 'Create {EntityType}'}
    </Button>
  </DialogActions>
</Dialog>
```

### Step 7: Add Required Imports
**Location**: Top of dashboard component

Ensure all necessary imports are present:

```typescript
import { useState } from 'react';
import {
  Dialog,
  DialogTitle,  
  DialogContent,
  DialogActions,
  TextField,
  Stack,
  CircularProgress,
  IconButton,
  // ... other Material-UI imports
} from '@mui/material';
import {
  Add as AddIcon,
  Close as CloseIcon,
  // ... other icons
} from '@mui/icons-material';
import { {entityType}Api, Create{EntityType}Request } from '../api/{entityType}';
```

## Entity-Specific Implementation Details

### Agents Entity
**Key Considerations**:
- Requires `agent_type_id` - need dropdown populated from AgentTypes
- Optional `project_id` and `team_id` for assignments
- Configuration field for agent-specific settings

**Form Fields**:
```typescript
interface CreateAgentFormData {
  name: string;
  agent_type_id: number;
  project_id?: number;
  team_id?: number;
  description: string;
  config: Record<string, any>;
}
```

**Special UI Elements**:
- AgentType dropdown (populated via API)
- Project assignment dropdown (optional)
- Team assignment dropdown (optional)
- JSON config editor or key-value pairs

### Teams Entity
**Key Considerations**:
- Requires `project_id` for project assignment
- Optional `lead_agent_id` for team lead
- Team description and objectives

**Form Fields**:
```typescript
interface CreateTeamFormData {
  name: string;
  project_id: number;
  lead_agent_id?: number;
  description: string;
  objectives: string[];
}
```

**Special UI Elements**:
- Project dropdown (required)
- Lead Agent dropdown (optional, filtered by project)
- Multi-line objectives field

### Workflows Entity
**Key Considerations**:
- Requires `project_id` for project assignment
- Complex workflow steps definition
- Status and priority settings

**Form Fields**:
```typescript
interface CreateWorkflowFormData {
  name: string;
  project_id: number;
  description: string;
  priority: 'low' | 'medium' | 'high' | 'critical';
  steps: WorkflowStep[];
}
```

**Special UI Elements**:
- Project dropdown (required)
- Priority selector
- Dynamic step creation interface
- Step dependency management

## Testing Workflow

### 1. Component Testing
After implementation, test each component:

```bash
# Start development environment
cd workflow-admin
docker-compose --profile api --profile frontend up -d

# Access frontend at http://localhost:3000
# Test entity creation flow:
# 1. Click Create button
# 2. Fill out form
# 3. Submit and verify creation
# 4. Check entity appears in list
```

### 2. API Integration Testing
Verify API calls work correctly:

```bash
# Monitor backend logs during testing
docker logs workflow-admin-backend -f

# Check database for created entities
# Run Newman tests to ensure API still works
./api-tests/scripts/run-tests.sh
```

### 3. Form Validation Testing
Test validation scenarios:
- Submit empty form (should show required field errors)
- Submit partial form (should show specific field errors)
- Submit valid form (should create entity successfully)
- Test error clearing when typing in fields

## Common Patterns Reference

### Form Field Templates

**Text Input**:
```typescript
<TextField
  fullWidth
  label="Field Label"
  value={formData.fieldName}
  onChange={(e) => handleFormChange('fieldName', e.target.value)}
  error={!!formErrors.fieldName}
  helperText={formErrors.fieldName || "Optional help text"}
  required
/>
```

**Dropdown Selection**:
```typescript
<FormControl fullWidth>
  <InputLabel>Selection Label</InputLabel>
  <Select
    value={formData.selectionField}
    onChange={(e) => handleFormChange('selectionField', e.target.value)}
    label="Selection Label"
  >
    {options.map((option) => (
      <MenuItem key={option.id} value={option.id}>
        {option.name}
      </MenuItem>
    ))}
  </Select>
</FormControl>
```

**Multi-line Text**:
```typescript
<TextField
  fullWidth
  label="Description"
  value={formData.description}
  onChange={(e) => handleFormChange('description', e.target.value)}
  multiline
  rows={3}
/>
```

## Quality Checklist

Before marking entity creation as complete:

- [ ] Newman API tests still pass (15/15 assertions)
- [ ] TypeScript builds without errors
- [ ] Modal opens and closes correctly
- [ ] Form validation works for all fields
- [ ] API integration creates entities successfully
- [ ] Created entities appear in the list immediately
- [ ] Error handling displays user-friendly messages
- [ ] Loading states prevent double-submission
- [ ] UI follows established Material-UI patterns
- [ ] Code follows TypeScript interface patterns established

## Implementation Order Recommendation

1. **Agents** - Moderate complexity, builds on established patterns
2. **Teams** - Simple, similar to Projects but with dropdowns
3. **Workflows** - Most complex, requires step management interface

This order allows incremental learning and pattern refinement while building toward the most complex implementation.

---
*Last Updated: 2025-09-03*
*Ready for: Agent, Team, and Workflow entity creation implementation*