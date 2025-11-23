

```sql
-- ============================================================================
-- DOCUMENTS
-- ============================================================================

CREATE TYPE document_type AS ENUM (
    'drawing',
    'specification',
    'report',
    'certificate',
    'contract',
    'correspondence',
    'quote',
    'invoice',
    'photo',
    'video',
    'other'
);

CREATE TABLE documents (
    document_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_id UUID NOT NULL REFERENCES projects(project_id) ON DELETE CASCADE,
    
    -- Document Info
    document_name TEXT NOT NULL,
    document_number TEXT,  -- e.g., "DRG-001", "SPEC-012"
    document_type document_type NOT NULL,
    
    -- Classification
    discipline TEXT,  -- architectural, structural, mep, landscape, planning
    category TEXT,  -- design, construction, compliance, commercial, admin
    
    -- Version Control
    version_number TEXT DEFAULT '1.0',
    revision_code TEXT,
    is_current_version BOOLEAN DEFAULT TRUE,
    supersedes_document_id UUID REFERENCES documents(document_id),
    
    -- File Details
    file_name TEXT NOT NULL,
    file_path TEXT,  -- S3 path, filesystem path, or URL
    file_url TEXT,
    file_size_bytes BIGINT,
    file_format TEXT,  -- pdf, dwg, xlsx, docx, jpg
    mime_type TEXT,
    
    -- Metadata
    title TEXT,
    description TEXT,
    author TEXT,
    issued_by TEXT,
    issued_for TEXT,  -- information, tender, construction, record
    
    -- Dates
    issue_date DATE,
    received_date DATE,
    expiry_date DATE,
    
    -- Approval
    requires_approval BOOLEAN DEFAULT FALSE,
    approved BOOLEAN DEFAULT FALSE,
    approved_by UUID REFERENCES users(user_id),
    approved_date DATE,
    
    -- Status
    status TEXT DEFAULT 'active',  -- draft, issued, approved, superseded, archived
    
    -- Linked Entities
    linked_room_ids UUID[],
    linked_material_ids UUID[],
    linked_task_ids UUID[],
    linked_inspection_ids UUID[],
    linked_snag_ids UUID[],
    
    -- Tags & Search
    tags TEXT[],
    search_vector tsvector GENERATED ALWAYS AS (
        to_tsvector('english', 
            coalesce(document_name, '') || ' ' || 
            coalesce(document_number, '') || ' ' ||
            coalesce(title, '') || ' ' ||
            coalesce(description, '') || ' ' ||
            coalesce(array_to_string(tags, ' '), '')
        )
    ) STORED,
    
    -- Access Control
    confidentiality TEXT DEFAULT 'private',  -- public, private, restricted, confidential
    
    -- Notes
    notes TEXT,
    
    -- Audit
    uploaded_by UUID REFERENCES users(user_id),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_documents_project ON documents(project_id);
CREATE INDEX idx_documents_type ON documents(document_type);
CREATE INDEX idx_documents_status ON documents(status);
CREATE INDEX idx_documents_issue_date ON documents(issue_date);
CREATE INDEX idx_documents_current ON documents(is_current_version);
CREATE INDEX idx_documents_tags ON documents USING GIN(tags);
CREATE INDEX idx_documents_search ON documents USING GIN(search_vector);
CREATE INDEX idx_documents_linked_rooms ON documents USING GIN(linked_room_ids);

CREATE TRIGGER update_documents_updated_at 
    BEFORE UPDATE ON documents 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();


-- ============================================================================
-- PHOTOS (Special Document Type with Geo/Context)
-- ============================================================================

CREATE TABLE photos (
    photo_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_id UUID NOT NULL REFERENCES projects(project_id) ON DELETE CASCADE,
    
    -- File Details
    file_name TEXT NOT NULL,
    file_path TEXT NOT NULL,
    file_url TEXT,
    file_size_bytes BIGINT,
    thumbnail_url TEXT,
    
    -- Photo Metadata
    caption TEXT,
    taken_date TIMESTAMPTZ DEFAULT NOW(),
    taken_by TEXT,
    
    -- Location
    room_id UUID REFERENCES rooms(room_id),
    location_description TEXT,
    gps_latitude DECIMAL(10, 8),
    gps_longitude DECIMAL(11, 8),
    
    -- Context
    photo_category TEXT,  -- progress, site_conditions, quality_issue, completion, marketing
    before_during_after TEXT,  -- before, during, after, comparison
    
    -- Camera Metadata (from EXIF)
    camera_make TEXT,
    camera_model TEXT,
    camera_settings JSONB,
    
    -- Linked Entities
    linked_task_id UUID REFERENCES tasks(task_id),
    linked_inspection_id UUID REFERENCES inspections(inspection_id),
    linked_snag_id UUID REFERENCES snagging_items(snag_id),
    linked_material_id UUID REFERENCES materials(material_id),
    
    -- Tags
    tags TEXT[],
    
    -- Visibility
    featured BOOLEAN DEFAULT FALSE,
    usage_rights TEXT DEFAULT 'private',  -- private, shareable, publishable
    
    -- Notes
    notes TEXT,
    
    -- Audit
    uploaded_by UUID REFERENCES users(user_id),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_photos_project ON photos(project_id);
CREATE INDEX idx_photos_room ON photos(room_id);
CREATE INDEX idx_photos_date ON photos(taken_date);
CREATE INDEX idx_photos_category ON photos(photo_category);
CREATE INDEX idx_photos_tags ON photos USING GIN(tags);
CREATE INDEX idx_photos_featured ON photos(featured);
CREATE INDEX idx_photos_gps ON photos(gps_latitude, gps_longitude) WHERE gps_latitude IS NOT NULL;

CREATE TRIGGER update_photos_updated_at 
    BEFORE UPDATE ON photos 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();
```