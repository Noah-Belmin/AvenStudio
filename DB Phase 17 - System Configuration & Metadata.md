
```sql
-- ============================================================================
-- PROJECT TEMPLATES
-- ============================================================================

CREATE TABLE project_templates (
    template_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    
    -- Template Info
    template_name TEXT NOT NULL,
    description TEXT,
    category TEXT,  -- residential_new_build, extension, conversion
    
    -- Template Content (JSONB structure)
    template_structure JSONB NOT NULL,  -- Rooms, stages, budget categories, etc.
    
    -- Usage
    usage_count INTEGER DEFAULT 0,
    
    -- Visibility
    public BOOLEAN DEFAULT FALSE,
    created_by UUID REFERENCES users(user_id),
    
    -- Audit
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_templates_category ON project_templates(category);
CREATE INDEX idx_templates_public ON project_templates(public);


-- ============================================================================
-- TAGS (Global Tagging System)
-- ============================================================================

CREATE TABLE tags (
    tag_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    
    -- Tag Details
    tag_name TEXT NOT NULL UNIQUE,
    tag_category TEXT,  -- user_defined, system, material_type, trade, etc.
    
    -- Color for UI
    color_hex TEXT,
    
    -- Usage
    usage_count INTEGER DEFAULT 0,
    
    -- Audit
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_tags_name ON tags(tag_name);
CREATE INDEX idx_tags_category ON tags(tag_category);


-- ============================================================================
-- ENTITY TAGS (Polymorphic Tagging)
-- ============================================================================

CREATE TABLE entity_tags (
    entity_tag_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    
    -- Tagged Entity
    entity_type TEXT NOT NULL,  -- room, material, task, document, etc.
    entity_id UUID NOT NULL,
    
    -- Tag
    tag_id UUID NOT NULL REFERENCES tags(tag_id) ON DELETE CASCADE,
    
    -- Project Context
    project_id UUID REFERENCES projects(project_id) ON DELETE CASCADE,
    
    -- Audit
    tagged_by UUID REFERENCES users(user_id),
    tagged_at TIMESTAMPTZ DEFAULT NOW(),
    
    UNIQUE(entity_type, entity_id, tag_id)
);

CREATE INDEX idx_entity_tags_entity ON entity_tags(entity_type, entity_id);
CREATE INDEX idx_entity_tags_tag ON entity_tags(tag_id);
CREATE INDEX idx_entity_tags_project ON entity_tags(project_id);


-- ============================================================================
-- ACTIVITY LOG (Audit Trail)
-- ============================================================================

CREATE TABLE activity_log (
    activity_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    
    -- Context
    project_id UUID REFERENCES projects(project_id) ON DELETE CASCADE,
    user_id UUID REFERENCES users(user_id) ON DELETE SET NULL,
    
    -- Action
    action_type TEXT NOT NULL,  -- created, updated, deleted, viewed, exported
    entity_type TEXT NOT NULL,  -- room, task, cost, document, etc.
    entity_id UUID NOT NULL,
    
    -- Changes (JSONB for flexibility)
    changes JSONB,  -- {field: {old: value, new: value}}
    
    -- Context
    ip_address INET,
    user_agent TEXT,
    
    -- Timestamp
    occurred_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_activity_project ON activity_log(project_id);
CREATE INDEX idx_activity_user ON activity_log(user_id);
CREATE INDEX idx_activity_entity ON activity_log(entity_type, entity_id);
CREATE INDEX idx_activity_time ON activity_log(occurred_at);

-- For time-series, consider:
-- SELECT create_hypertable('activity_log', 'occurred_at');
```