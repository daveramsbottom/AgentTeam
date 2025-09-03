# UI Architecture & Component Patterns

## Overview
This document describes the established UI patterns and component architecture for the workflow-admin frontend, focusing on the entity creation system that scales across Projects, Agents, Teams, and Workflows.

## Design Philosophy

### Consistency First
All entity management follows the same interaction patterns:
- Horizontal action menus for primary actions
- Modal dialogs for entity creation
- Consistent form validation and error handling
- Unified loading states and API integration

### Material-UI Foundation
Built on Material-UI components for:
- Professional appearance suitable for admin interfaces  
- Accessibility built-in
- Responsive design patterns
- Consistent theming and spacing

## Core UI Patterns

### 1. Horizontal Action Menu Pattern

**Purpose**: Provide consistent, scannable actions at the top of entity list pages

**Implementation**:
```typescript
// Located at top of each entity dashboard component
<Paper elevation={1} sx={{ mb: 3, p: 2 }}>
  <Box display="flex" alignItems="center" justifyContent="space-between">
    <Typography variant="h6" sx={{ fontWeight: 500 }}>
      Actions
    </Typography>
    <Box display="flex" gap={1}>
      <Button
        variant="contained"
        startIcon={<AddIcon />}
        onClick={handleCreateEntity}
        sx={{ borderRadius: 2, textTransform: 'none' }}
      >
        Create {EntityType}
      </Button>
      <Button
        variant="outlined"
        startIcon={<SettingsIcon />}
        onClick={handleConfigure}
        disabled  // Future functionality
        sx={{ borderRadius: 2, textTransform: 'none' }}
      >
        Configure
      </Button>
      <IconButton onClick={handleActionMenuOpen} size="small" sx={{ ml: 1 }}>
        <MoreVertIcon />
      </IconButton>
    </Box>
  </Box>
</Paper>
```

**Features**:
- **Primary Actions**: Create and Configure (future) prominently displayed
- **Secondary Actions**: Dropdown menu for Refresh, Export, Import operations
- **Consistent Styling**: Rounded corners, proper spacing, disabled states
- **Accessibility**: Proper button labeling and keyboard navigation

### 2. Modal Creation Dialog Pattern

**Purpose**: Focused entity creation without losing list page context

**Implementation**:
```typescript
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
      {/* Form fields with validation */}
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
      {creating ? 'Creating...' : `Create ${EntityType}`}
    </Button>
  </DialogActions>
</Dialog>
```

**Features**:
- **Full Width**: Utilizes available screen space for complex forms
- **Divided Content**: Clear separation between title, form, and actions
- **Loading States**: Visual feedback during API calls
- **Keyboard Support**: ESC to close, proper focus management

### 3. Form Validation Pattern

**Purpose**: Consistent field validation with user-friendly error messages

**Implementation**:
```typescript
// Validation function pattern
const validateForm = (): boolean => {
  const errors: Record<string, string> = {};
  
  if (!formData.name.trim()) {
    errors.name = 'Name is required';
  } else if (formData.name.length < 3) {
    errors.name = 'Name must be at least 3 characters';
  }
  
  if (!formData.description.trim()) {
    errors.description = 'Description is required';
  }
  
  // Nested field validation
  if (!formData.settings.timeline.trim()) {
    errors['settings.timeline'] = 'Timeline is required';
  }
  
  setFormErrors(errors);
  return Object.keys(errors).length === 0;
};

// Form field with error display
<TextField
  fullWidth
  label="Project Name"
  value={formData.name}
  onChange={(e) => handleFormChange('name', e.target.value)}
  error={!!formErrors.name}
  helperText={formErrors.name}
  required
/>
```

**Features**:
- **Real-time Clearing**: Errors clear when user starts typing
- **Field-specific Messages**: Targeted validation feedback
- **Required Field Indicators**: Visual cues for mandatory fields
- **Nested Field Support**: Validation for complex object structures

### 4. State Management Pattern

**Purpose**: Consistent state handling across all entity creation components

**State Structure**:
```typescript
// Modal and menu state
const [createModalOpen, setCreateModalOpen] = useState(false);
const [actionMenuAnchor, setActionMenuAnchor] = useState<null | HTMLElement>(null);

// Form data with TypeScript interfaces
const [formData, setFormData] = useState<Create{EntityType}FormData>({
  // Form-specific initial values
});

// Error handling
const [formErrors, setFormErrors] = useState<Record<string, string>>({});
const [creating, setCreating] = useState(false);
const [error, setError] = useState<string | null>(null);
```

**State Management Functions**:
```typescript
// Generic form change handler
const handleFormChange = (field: string, value: any) => {
  if (field.includes('.')) {
    // Handle nested fields (e.g., 'settings.timeline')
    const [parent, child] = field.split('.');
    setFormData(prev => ({
      ...prev,
      [parent]: {
        ...(prev[parent as keyof typeof prev] as object),
        [child]: value,
      },
    }));
  } else {
    setFormData(prev => ({ ...prev, [field]: value }));
  }
  
  // Clear field error when user types
  if (formErrors[field]) {
    setFormErrors(prev => {
      const newErrors = { ...prev };
      delete newErrors[field];
      return newErrors;
    });
  }
};
```

## Component Architecture

### Dashboard Components Structure

```
{EntityType}Dashboard.tsx
├── State Management
│   ├── Entity list state (projects, agents, teams, workflows)
│   ├── Loading and error states
│   ├── Modal and form states
│   └── Action menu state
├── Data Loading
│   ├── useEffect hook for initial load
│   ├── Error handling and retry logic
│   └── Loading state management
├── Event Handlers
│   ├── Modal open/close handlers
│   ├── Form change and validation handlers
│   ├── Submit handler with API integration
│   └── Action menu handlers
├── UI Rendering
│   ├── Loading and error state displays
│   ├── Horizontal action menu
│   ├── Entity list/grid display
│   └── Creation modal dialog
└── API Integration
    ├── List fetching on component mount
    ├── Create API calls with error handling
    └── Live list updates after creation
```

### TypeScript Interface Patterns

```typescript
// Form data interface - UI-specific
interface Create{EntityType}FormData {
  name: string;
  description: string;
  // Additional form-specific fields
  priority: 'low' | 'medium' | 'high' | 'critical';
  settings: {
    // Nested settings object
    tech_stack: string[];
    timeline: string;
  };
}

// API request interface - backend-specific
interface Create{EntityType}Request {
  name: string;
  description?: string;
  context?: string;
  settings?: {
    priority: string;
    tech_stack: string[];
    timeline: string;
  };
}

// Entity interface - full data model
interface {EntityType} {
  id: number;
  name: string;
  description?: string;
  status?: string;
  created_at: string;
  updated_at?: string;
  // Computed fields from relationships
  related_count?: number;
}
```

## API Integration Patterns

### API Client Structure

```typescript
// api/{entityType}.ts
export const {entityType}Api = {
  get{EntityType}s: async (): Promise<{EntityType}[]> => {
    const response = await api.get('/api/v1/{entityType}s/');
    return response.data || [];
  },

  get{EntityType}: async (id: number): Promise<{EntityType}> => {
    const response = await api.get(`/api/v1/{entityType}s/${id}`);
    return response.data;
  },

  create{EntityType}: async (data: Create{EntityType}Request): Promise<{EntityType}> => {
    const response = await api.post('/api/v1/{entityType}s/', data);
    return response.data;
  },
};
```

### Error Handling Pattern

```typescript
const handleSubmit = async () => {
  if (!validateForm()) return;
  
  setCreating(true);
  try {
    const newEntity = await {entityType}Api.create{EntityType}({
      name: formData.name,
      description: formData.description,
      // Map form data to API request format
    });
    
    // Update local state immediately
    setEntities(prev => [newEntity, ...prev]);
    handleModalClose();
  } catch (err) {
    console.error(`Error creating {entityType}:`, err);
    setError(`Failed to create {entityType}. Please try again.`);
  } finally {
    setCreating(false);
  }
};
```

## Styling Patterns

### Consistent Component Styling

```typescript
// Action menu styling
sx={{ 
  borderRadius: 2,          // Rounded corners
  textTransform: 'none',    // Natural text case
  mb: 3,                    // Consistent margins
  p: 2                      // Consistent padding
}}

// Modal styling
sx={{
  display: 'flex',
  justifyContent: 'space-between',
  alignItems: 'center'
}}

// Form field spacing
<Stack spacing={3}>         // Consistent form field spacing
```

### Color and Status Patterns

```typescript
const getPriorityColor = (priority: string) => {
  switch (priority?.toLowerCase()) {
    case 'critical': return 'error';
    case 'high': return 'error';
    case 'medium': return 'warning';  
    case 'low': return 'info';
    default: return 'default';
  }
};
```

## Accessibility Features

- **Keyboard Navigation**: All interactive elements are keyboard accessible
- **Screen Reader Support**: Proper ARIA labels and semantic HTML
- **Focus Management**: Logical focus order in modals and forms
- **Color Contrast**: Material-UI ensures adequate color contrast
- **Error Messaging**: Clear, descriptive error messages

## Performance Considerations

- **State Updates**: Minimal re-renders with targeted state updates
- **API Calls**: Proper loading states prevent double-submissions
- **Memory Management**: Cleanup of event listeners and timeouts
- **Bundle Size**: Material-UI tree shaking for optimal builds

---
*Last Updated: 2025-09-03*
*Status: Core patterns established and documented for scaling*