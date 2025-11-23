
```sql
-- ============================================================================
-- DESIGN CHOICES
-- ============================================================================

CREATE TYPE design_choice_status AS ENUM (
    'considering',
    'researching',
    'specified',
    'approved',
    'ordered',
    'delivered',
    'installed'
);

CREATE TABLE design_choices (
    choice_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_id UUID NOT NULL REFERENCES projects(project_id) ON DELETE CASCADE,
    room_id UUID REFERENCES rooms(room_id) ON DELETE CASCADE,  -- Nullable for project-wide choices
    
    -- What is being chosen
    category TEXT NOT NULL,  -- flooring, wall_finish, lighting, fixtures, etc.
    element TEXT,  -- More specific: "floor_tiles", "pendant_light"
    
    -- The choice
    choice_name TEXT NOT NULL,
    description TEXT,
    
    -- Product details
    manufacturer TEXT,
    product_code TEXT,
    specification TEXT,
    
    -- Sourcing
    supplier_name TEXT,
    supplier_contact TEXT,
    
    -- Cost
    estimated_cost DECIMAL(12,2),
    actual_cost DECIMAL(12,2),
    
    -- Status
    status design_choice_status DEFAULT 'considering',
    
    -- Decision tracking
    decided_date DATE,
    decided_by UUID REFERENCES users(user_id),
    reasoning TEXT,
    alternatives_considered TEXT[],
    confidence_level INTEGER CHECK (confidence_level BETWEEN 1 AND 5),
    
    -- Links to other entities
    linked_material_id UUID,  -- Will reference materials table
    linked_decision_id UUID,  -- Will reference decisions table
    
    -- Compliance
    building_regs_parts TEXT[],  -- e.g., ['Part L', 'Part F']
    
    -- Flexible data
    choice_metadata JSONB DEFAULT '{}'::jsonb,
    
    -- Audit
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_choices_project ON design_choices(project_id);
CREATE INDEX idx_choices_room ON design_choices(room_id);
CREATE INDEX idx_choices_category ON design_choices(category);
CREATE INDEX idx_choices_status ON design_choices(status);
CREATE INDEX idx_choices_metadata ON design_choices USING GIN(choice_metadata);

CREATE TRIGGER update_design_choices_updated_at 
    BEFORE UPDATE ON design_choices 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();
```