import { OrganizationalContext } from '../api/contexts';

// Default colors for built-in categories
const DEFAULT_CATEGORY_COLORS: Record<string, string> = {
  'tech_standards': '#2196F3',
  'security': '#F44336', 
  'compliance': '#FF9800',
  'business_guidelines': '#9C27B0'
};

// Default Material-UI theme colors mapping
const DEFAULT_MUI_COLORS: Record<string, string> = {
  'tech_standards': 'info',
  'security': 'error', 
  'compliance': 'warning',
  'business_guidelines': 'secondary'
};

// Cache for dynamic colors extracted from contexts
let dynamicColorCache: Record<string, string> = {};
let dynamicMuiColorCache: Record<string, string> = {};

// Helper function to convert hex color to Material-UI theme color
const hexToMuiColor = (hexColor: string): string => {
  const colorMap: Record<string, string> = {
    '#F44336': 'error',    // Red
    '#2196F3': 'info',     // Blue
    '#FF9800': 'warning',  // Orange
    '#4CAF50': 'success',  // Green
    '#9C27B0': 'secondary', // Purple
    '#607D8B': 'default',  // Blue Grey
    '#795548': 'default',  // Brown
    '#009688': 'info',     // Teal
  };
  return colorMap[hexColor] || 'default';
};

// Extract colors from context data and update cache
export const updateCategoryColorsFromContexts = (contexts: OrganizationalContext[]) => {
  contexts.forEach(context => {
    if (context.content?.ui_settings?.color) {
      const category = context.category;
      const color = context.content.ui_settings.color;
      
      // Update both hex and MUI color caches
      dynamicColorCache[category] = color;
      dynamicMuiColorCache[category] = hexToMuiColor(color);
    }
  });
};

// Get hex color for a category (for styling)
export const getCategoryColor = (category: string): string => {
  // First check dynamic cache
  if (dynamicColorCache[category]) {
    return dynamicColorCache[category];
  }
  
  // Fall back to defaults
  return DEFAULT_CATEGORY_COLORS[category] || '#757575';
};

// Get Material-UI color for a category (for chips, buttons, etc.)
export const getCategoryMuiColor = (category: string): string => {
  // First check dynamic cache
  if (dynamicMuiColorCache[category]) {
    return dynamicMuiColorCache[category];
  }
  
  // Fall back to defaults
  return DEFAULT_MUI_COLORS[category] || 'default';
};

// Get display name for a category
export const getCategoryDisplayName = (category: string, contexts?: OrganizationalContext[]): string => {
  // Try to get display name from context data
  if (contexts) {
    const contextWithDisplayName = contexts.find(c => 
      c.category === category && c.content?.ui_settings?.display_name
    );
    if (contextWithDisplayName) {
      return contextWithDisplayName.content.ui_settings.display_name;
    }
  }
  
  // Fall back to formatted category name
  return category.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase());
};

// Get icon name for a category  
export const getCategoryIcon = (category: string, contexts?: OrganizationalContext[]): string => {
  // Try to get icon from context data
  if (contexts) {
    const contextWithIcon = contexts.find(c => 
      c.category === category && c.content?.ui_settings?.icon
    );
    if (contextWithIcon) {
      return contextWithIcon.content.ui_settings.icon;
    }
  }
  
  // Fall back to default icons
  const defaultIcons: Record<string, string> = {
    'tech_standards': 'tech',
    'security': 'security', 
    'compliance': 'compliance',
    'business_guidelines': 'business'
  };
  
  return defaultIcons[category] || 'category';
};

// Clear caches (useful when contexts are reloaded)
export const clearCategoryColorCache = () => {
  dynamicColorCache = {};
  dynamicMuiColorCache = {};
};

// Initialize colors from a full context list
export const initializeCategoryColors = (contexts: OrganizationalContext[]) => {
  clearCategoryColorCache();
  updateCategoryColorsFromContexts(contexts);
};