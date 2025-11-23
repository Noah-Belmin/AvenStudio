

```sql
-- ============================================================================
-- ROOMS & SPACES
-- ============================================================================

CREATE TYPE room_type AS ENUM (
    'kitchen',
    'living_room',
    'dining_room',
    'bedroom',
    'bathroom',
    'ensuite',
    'wc',
    'utility',
    'hallway',
    'landing',
    'study',
    'garage',
    'workshop',
    'storage',
    'other'
);

CREATE TABLE rooms (
    room_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_id UUID NOT NULL REFERENCES projects(project_id) ON DELETE CASCADE,
    
    -- Basic Info
    room_name TEXT NOT NULL,
    room_type room_type NOT NULL,
    room_reference TEXT,  -- User reference like "BR1", "Kitchen"
    
    -- Location
    floor INTEGER,  -- 0 = ground, 1 = first, -1 = basement
    zone TEXT,  -- e.g., "North Wing", "Main House"
    
    -- Dimensions
    area_sqm DECIMAL(10,2),
    ceiling_height_m DECIMAL(4,2),
    volume_m3 DECIMAL(10,2) GENERATED ALWAYS AS (area_sqm * ceiling_height_m) STORED,
    
    -- Status
    design_locked BOOLEAN DEFAULT FALSE,
    design_locked_date DATE,
    construction_status TEXT DEFAULT 'not_started',  -- not_started, in_progress, completed
    completion_percentage INTEGER DEFAULT 0 CHECK (completion_percentage BETWEEN 0 AND 100),
    
    -- Flexible attributes (finishes, features, etc.)
    custom_attributes JSONB DEFAULT '{}'::jsonb,
    
    -- Notes
    notes TEXT,
    
    -- Ordering (for display)
    display_order INTEGER,
    
    -- Audit
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    
    -- Full-text search
    search_vector tsvector GENERATED ALWAYS AS (
        to_tsvector('english', 
            coalesce(room_name, '') || ' ' || 
            coalesce(room_reference, '') || ' ' ||
            coalesce(notes, '')
        )
    ) STORED
);

CREATE INDEX idx_rooms_project ON rooms(project_id);
CREATE INDEX idx_rooms_type ON rooms(room_type);
CREATE INDEX idx_rooms_floor ON rooms(floor);
CREATE INDEX idx_rooms_search ON rooms USING GIN(search_vector);
CREATE INDEX idx_rooms_attributes ON rooms USING GIN(custom_attributes);
CREATE INDEX idx_rooms_project_display ON rooms(project_id, display_order);

CREATE TRIGGER update_rooms_updated_at 
    BEFORE UPDATE ON rooms 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();
```