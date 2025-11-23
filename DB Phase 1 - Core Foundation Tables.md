

```sql
-- ============================================================================
-- USERS & AUTHENTICATION
-- ============================================================================

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";  -- For fuzzy text search
CREATE EXTENSION IF NOT EXISTS "btree_gin";  -- For multi-column indexes

-- Users table (if not using Supabase Auth)
CREATE TABLE users (
    user_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email TEXT UNIQUE NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    last_login TIMESTAMPTZ,
    
    -- Profile
    full_name TEXT,
    phone TEXT,
    avatar_url TEXT,
    
    -- Preferences stored as JSONB for flexibility
    preferences JSONB DEFAULT '{}'::jsonb,
    
    -- Metadata
    metadata JSONB DEFAULT '{}'::jsonb,
    
    -- Audit
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    
    -- Constraints
    CONSTRAINT valid_email CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$')
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_created_at ON users(created_at);

-- Auto-update timestamp trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_users_updated_at 
    BEFORE UPDATE ON users 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();


-- ============================================================================
-- PROJECTS (Core Entity)
-- ============================================================================

CREATE TYPE project_stage AS ENUM (
    'pre_planning',
    'planning',
    'design',
    'pre_construction',
    'construction',
    'completion',
    'post_occupancy'
);

CREATE TYPE build_method AS ENUM (
    'traditional_masonry',
    'timber_frame',
    'sips',
    'icf',
    'modular',
    'hybrid',
    'other'
);

CREATE TABLE projects (
    project_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    
    -- Ownership
    owner_user_id UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    
    -- Basic Info
    project_name TEXT NOT NULL,
    project_reference TEXT UNIQUE,  -- User-friendly reference (e.g., "OAK-2025-001")
    
    -- Location
    site_address TEXT,
    postcode TEXT,
    country TEXT DEFAULT 'england',
    region TEXT,
    local_authority TEXT,
    
    -- Project Type
    project_type TEXT DEFAULT 'new_build',  -- new_build, extension, conversion, etc.
    build_method build_method,
    
    -- Status
    current_stage project_stage DEFAULT 'pre_planning',
    completion_percentage INTEGER DEFAULT 0 CHECK (completion_percentage BETWEEN 0 AND 100),
    
    -- Timeline
    project_start_date DATE,
    planned_completion_date DATE,
    actual_completion_date DATE,
    
    -- Budget
    total_budget_amount DECIMAL(15,2),
    currency TEXT DEFAULT 'GBP',
    
    -- Size
    approx_floor_area_sqm DECIMAL(10,2),
    stories INTEGER,
    
    -- Flexible fields for additional data
    project_metadata JSONB DEFAULT '{}'::jsonb,
    
    -- Full-text search
    search_vector tsvector GENERATED ALWAYS AS (
        to_tsvector('english', 
            coalesce(project_name, '') || ' ' || 
            coalesce(site_address, '') || ' ' ||
            coalesce(project_reference, '')
        )
    ) STORED,
    
    -- Audit
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    archived BOOLEAN DEFAULT FALSE,
    archived_at TIMESTAMPTZ
);

CREATE INDEX idx_projects_owner ON projects(owner_user_id);
CREATE INDEX idx_projects_stage ON projects(current_stage);
CREATE INDEX idx_projects_reference ON projects(project_reference);
CREATE INDEX idx_projects_search ON projects USING GIN(search_vector);
CREATE INDEX idx_projects_metadata ON projects USING GIN(project_metadata);

CREATE TRIGGER update_projects_updated_at 
    BEFORE UPDATE ON projects 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();


-- ============================================================================
-- PROJECT COLLABORATORS (Multi-User Access)
-- ============================================================================

CREATE TYPE collaborator_role AS ENUM (
    'owner',
    'partner',
    'architect',
    'contractor',
    'engineer',
    'viewer'
);

CREATE TABLE project_collaborators (
    collaboration_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_id UUID NOT NULL REFERENCES projects(project_id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    
    role collaborator_role NOT NULL,
    
    -- Permissions
    can_edit BOOLEAN DEFAULT FALSE,
    can_view_costs BOOLEAN DEFAULT TRUE,
    can_manage_team BOOLEAN DEFAULT FALSE,
    
    -- Status
    invited_at TIMESTAMPTZ DEFAULT NOW(),
    accepted_at TIMESTAMPTZ,
    status TEXT DEFAULT 'pending',  -- pending, active, removed
    
    -- Audit
    invited_by UUID REFERENCES users(user_id),
    removed_at TIMESTAMPTZ,
    removed_by UUID REFERENCES users(user_id),
    
    UNIQUE(project_id, user_id)
);

CREATE INDEX idx_collaborators_project ON project_collaborators(project_id);
CREATE INDEX idx_collaborators_user ON project_collaborators(user_id);
CREATE INDEX idx_collaborators_role ON project_collaborators(role);
```