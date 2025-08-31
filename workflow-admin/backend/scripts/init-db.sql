-- Initialize PostgreSQL database for workflow-admin cloud sync
-- This script runs when the PostgreSQL container first starts

-- Create extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Set timezone
SET timezone = 'UTC';

-- Create additional users if needed (optional)
-- CREATE USER workflow_admin_readonly WITH PASSWORD 'readonly_password';

-- Grant permissions
GRANT ALL PRIVILEGES ON DATABASE workflow_admin TO workflow_admin;

-- Create schema if needed
-- CREATE SCHEMA IF NOT EXISTS workflow_admin;

-- Log initialization
DO $$
BEGIN
    RAISE NOTICE 'Workflow-Admin database initialized successfully';
    RAISE NOTICE 'Database: workflow_admin';
    RAISE NOTICE 'User: workflow_admin';
    RAISE NOTICE 'Timezone: %', current_setting('timezone');
END $$;