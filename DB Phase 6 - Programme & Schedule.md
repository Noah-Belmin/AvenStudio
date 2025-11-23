
```sql
-- ============================================================================
-- PROGRAMME STAGES (RIBA-Aligned)
-- ============================================================================

CREATE TYPE riba_stage AS ENUM (
    'stage_0',  -- Strategic Definition
    'stage_1',  -- Preparation and Briefing
    'stage_2',  -- Concept Design
    'stage_3',  -- Spatial Coordination
    'stage_4',  -- Technical Design
    'stage_5',  -- Manufacturing and Construction
    'stage_6',  -- Handover
    'stage_7'   -- Use
);

CREATE TABLE programme_stages (
    stage_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_id UUID NOT NULL REFERENCES projects(project_id) ON DELETE CASCADE,
    
    -- Stage Info
    stage_name TEXT NOT NULL,
    stage_code riba_stage,
    parent_stage_id UUID REFERENCES programme_stages(stage_id),  -- For sub-stages
    
    -- Timeline
    planned_start_date DATE,
    planned_end_date DATE,
    actual_start_date DATE,
    actual_end_date DATE,
    
    -- Duration
    planned_duration_days INTEGER GENERATED ALWAYS AS (
        planned_end_date - planned_start_date
    ) STORED,
    actual_duration_days INTEGER GENERATED ALWAYS AS (
        actual_end_date - actual_start_date
    ) STORED,
    
    -- Status
    status TEXT DEFAULT 'not_started',  -- not_started, in_progress, completed, on_hold
    completion_percentage INTEGER DEFAULT 0 CHECK (completion_percentage BETWEEN 0 AND 100),
    
    -- Critical Path
    on_critical_path BOOLEAN DEFAULT FALSE,
    float_days INTEGER,  -- Slack time available
    
    -- Display
    display_order INTEGER,
    
    -- Notes
    notes TEXT,
    
    -- Audit
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_programme_stages_project ON programme_stages(project_id);
CREATE INDEX idx_programme_stages_parent ON programme_stages(parent_stage_id);
CREATE INDEX idx_programme_stages_dates ON programme_stages(planned_start_date, planned_end_date);
CREATE INDEX idx_programme_stages_critical ON programme_stages(on_critical_path);

CREATE TRIGGER update_programme_stages_updated_at 
    BEFORE UPDATE ON programme_stages 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();


-- ============================================================================
-- TASKS / ACTIVITIES
-- ============================================================================

CREATE TABLE tasks (
    task_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_id UUID NOT NULL REFERENCES projects(project_id) ON DELETE CASCADE,
    stage_id UUID REFERENCES programme_stages(stage_id) ON DELETE SET NULL,
    
    -- Task Info
    task_name TEXT NOT NULL,
    task_reference TEXT,
    description TEXT,
    
    -- Classification
    trade TEXT,  -- groundworks, brickwork, carpentry, etc.
    category TEXT,
    
    -- Timeline
    planned_start_date DATE,
    planned_end_date DATE,
    actual_start_date DATE,
    actual_end_date DATE,
    planned_duration_days INTEGER,
    
    -- Status
    status TEXT DEFAULT 'not_started',  -- not_started, in_progress, on_hold, completed, cancelled
    completion_percentage INTEGER DEFAULT 0 CHECK (completion_percentage BETWEEN 0 AND 100),
    
    -- Assignment
    assigned_to TEXT,  -- Contractor/subcontractor name
    assigned_contact TEXT,
    
    -- Dependencies
    predecessor_task_ids UUID[],  -- Tasks that must complete before this one
    lag_days INTEGER DEFAULT 0,  -- Gap between predecessor completion and this start
    
    -- Critical Path
    on_critical_path BOOLEAN DEFAULT FALSE,
    
    -- Resources
    labour_required TEXT[],
    plant_equipment_required TEXT[],
    materials_required UUID[],  -- Array of material_ids
    
    -- Weather
    weather_dependent BOOLEAN DEFAULT FALSE,
    
    -- Inspections
    inspection_required BOOLEAN DEFAULT FALSE,
    inspection_type TEXT,
    
    -- Relationships
    linked_room_ids UUID[],
    
    -- Notes
    notes TEXT,
    
    -- Metadata
    task_metadata JSONB DEFAULT '{}'::jsonb,
    
    -- Audit
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_tasks_project ON tasks(project_id);
CREATE INDEX idx_tasks_stage ON tasks(stage_id);
CREATE INDEX idx_tasks_status ON tasks(status);
CREATE INDEX idx_tasks_dates ON tasks(planned_start_date, planned_end_date);
CREATE INDEX idx_tasks_trade ON tasks(trade);
CREATE INDEX idx_tasks_assigned ON tasks(assigned_to);
CREATE INDEX idx_tasks_predecessors ON tasks USING GIN(predecessor_task_ids);
CREATE INDEX idx_tasks_linked_rooms ON tasks USING GIN(linked_room_ids);
CREATE INDEX idx_tasks_materials ON tasks USING GIN(materials_required);

CREATE TRIGGER update_tasks_updated_at 
    BEFORE UPDATE ON tasks 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();
```