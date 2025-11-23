
```sql
-- ============================================================================
-- INSPECTIONS
-- ============================================================================

CREATE TYPE inspection_type AS ENUM (
    'building_control',
    'warranty_provider',
    'self_inspection',
    'architect',
    'engineer',
    'specialist'
);

CREATE TYPE inspection_result AS ENUM (
    'pass',
    'pass_with_advisories',
    'conditional_pass',
    'fail',
    'deferred',
    'not_inspected'
);

CREATE TABLE inspections (
    inspection_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_id UUID NOT NULL REFERENCES projects(project_id) ON DELETE CASCADE,
    
    -- Inspection Details
    inspection_name TEXT NOT NULL,
    inspection_type inspection_type NOT NULL,
    inspection_stage TEXT,  -- foundations, dpc, drains, etc.
    
    -- Inspector
    inspector_name TEXT,
    inspector_organization TEXT,
    inspector_contact TEXT,
    
    -- Scheduling
    scheduled_date DATE,
    actual_date DATE,
    
    -- Prerequisites
    prerequisites_met BOOLEAN DEFAULT FALSE,
    prerequisite_notes TEXT,
    
    -- Outcome
    result inspection_result,
    result_notes TEXT,
    
    -- Non-Compliances
    non_compliances_count INTEGER DEFAULT 0,
    critical_issues_count INTEGER DEFAULT 0,
    
    -- Certificates
    certificate_issued BOOLEAN DEFAULT FALSE,
    certificate_reference TEXT,
    certificate_url TEXT,
    
    -- Follow-up
    re_inspection_required BOOLEAN DEFAULT FALSE,
    re_inspection_date DATE,
    
    -- Linked Entities
    linked_stage_id UUID REFERENCES programme_stages(stage_id),
    linked_task_ids UUID[],
    linked_room_ids UUID[],
    
    -- Documents
    report_url TEXT,
    photo_urls TEXT[],
    
    -- Notes
    notes TEXT,
    
    -- Audit
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_inspections_project ON inspections(project_id);
CREATE INDEX idx_inspections_type ON inspections(inspection_type);
CREATE INDEX idx_inspections_date ON inspections(actual_date);
CREATE INDEX idx_inspections_result ON inspections(result);
CREATE INDEX idx_inspections_result ON inspections(result);
CREATE INDEX idx_inspections_stage ON inspections(linked_stage_id);
CREATE INDEX idx_inspections_tasks ON inspections USING GIN(linked_task_ids);

CREATE TRIGGER update_inspections_updated_at 
    BEFORE UPDATE ON inspections 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();


-- ============================================================================
-- SNAGGING / DEFECTS
-- ============================================================================

CREATE TYPE snag_severity AS ENUM (
    'critical',
    'major',
    'minor',
    'cosmetic'
);

CREATE TYPE snag_status AS ENUM (
    'identified',
    'allocated',
    'in_progress',
    'completed',
    'verified',
    'closed',
    'disputed',
    'deferred'
);

CREATE TABLE snagging_items (
    snag_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_id UUID NOT NULL REFERENCES projects(project_id) ON DELETE CASCADE,
    
    -- Reference
    snag_reference TEXT,  -- e.g., "SNH-001" (Snag High priority)
    
    -- Discovery
    discovered_date DATE NOT NULL DEFAULT CURRENT_DATE,
    discovered_by TEXT,
    discovery_method TEXT,  -- routine_inspection, client_walkthrough, commissioning_test
    
    -- Location
    room_id UUID REFERENCES rooms(room_id),
    specific_location TEXT,  -- "Northeast corner", "Window 3"
    floor INTEGER,
    
    -- Classification
    trade TEXT NOT NULL,  -- brickwork, carpentry, electrical, plumbing, decorating
    category TEXT,  -- dimensional, finish, performance, safety, damage, omission
    element TEXT,  -- door, window, floor, wall, ceiling, fixture
    
    -- Description
    short_description TEXT NOT NULL,
    detailed_description TEXT,
    defect_type TEXT[],  -- alignment, level, plumb, finish, leak, crack, stain, damage
    
    -- Severity
    severity snag_severity NOT NULL,
    severity_justification TEXT,
    
    -- Flags
    health_and_safety_issue BOOLEAN DEFAULT FALSE,
    building_regulation_breach BOOLEAN DEFAULT FALSE,
    warranty_claim_risk BOOLEAN DEFAULT FALSE,
    blocks_occupation BOOLEAN DEFAULT FALSE,
    
    -- Specification
    specification_reference TEXT,
    drawing_reference TEXT,
    original_specification TEXT,
    actual_condition TEXT,
    required_standard TEXT,
    
    -- Responsibility
    responsible_party TEXT NOT NULL,  -- contractor, subcontractor, supplier
    responsible_company TEXT,
    responsible_contact TEXT,
    liability_accepted BOOLEAN,
    liability_disputed BOOLEAN DEFAULT FALSE,
    
    -- Rectification
    rectification_method TEXT,
    estimated_cost DECIMAL(10,2),
    actual_cost DECIMAL(10,2),
    
    -- Timeline
    target_fix_date DATE,
    actual_start_date DATE,
    actual_completion_date DATE,
    
    -- Status
    status snag_status DEFAULT 'identified',
    
    -- Verification
    reinspection_required BOOLEAN DEFAULT TRUE,
    reinspected_by TEXT,
    reinspection_date DATE,
    verification_result TEXT,  -- satisfactory, unsatisfactory, requires_further_work
    
    -- Client Sign-off
    client_signed_off BOOLEAN DEFAULT FALSE,
    client_sign_off_date DATE,
    client_sign_off_by TEXT,
    
    -- Linked Entities
    linked_inspection_id UUID REFERENCES inspections(inspection_id),
    linked_material_id UUID REFERENCES materials(material_id),
    linked_task_id UUID REFERENCES tasks(task_id),
    related_snag_ids UUID[],  -- Similar defects elsewhere
    
    -- Evidence
    photo_urls TEXT[],
    
    -- Notes
    notes TEXT,
    client_visible_notes TEXT,
    internal_notes TEXT,
    
    -- Metadata
    snag_metadata JSONB DEFAULT '{}'::jsonb,
    
    -- Audit
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_snagging_project ON snagging_items(project_id);
CREATE INDEX idx_snagging_room ON snagging_items(room_id);
CREATE INDEX idx_snagging_severity ON snagging_items(severity);
CREATE INDEX idx_snagging_status ON snagging_items(status);
CREATE INDEX idx_snagging_trade ON snagging_items(trade);
CREATE INDEX idx_snagging_responsible ON snagging_items(responsible_party);
CREATE INDEX idx_snagging_dates ON snagging_items(discovered_date, target_fix_date);
CREATE INDEX idx_snagging_flags ON snagging_items(health_and_safety_issue, blocks_occupation);
CREATE INDEX idx_snagging_related ON snagging_items USING GIN(related_snag_ids);

CREATE TRIGGER update_snagging_items_updated_at 
    BEFORE UPDATE ON snagging_items 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();


-- ============================================================================
-- INSPECTION CHECKS (Checklist Items)
-- ============================================================================

CREATE TABLE inspection_checks (
    check_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    inspection_id UUID NOT NULL REFERENCES inspections(inspection_id) ON DELETE CASCADE,
    
    -- Check Details
    check_reference TEXT,  -- e.g., "GF01", "FF02"
    category TEXT NOT NULL,
    item_description TEXT NOT NULL,
    acceptance_criteria TEXT,
    
    -- Standards
    regulatory_requirement TEXT,  -- Part A, BS 8000, etc.
    inspection_method TEXT,  -- visual, measured, tested, witnessed
    
    -- Measurement
    tolerance TEXT,  -- ±5mm, ±2mm
    measurement_taken TEXT,
    within_tolerance BOOLEAN,
    
    -- Result
    pass_fail BOOLEAN,
    result_notes TEXT,
    
    -- Issues
    issues_identified TEXT[],
    remedial_action_required TEXT,
    
    -- Evidence
    photo_urls TEXT[],
    
    -- Metadata
    check_metadata JSONB DEFAULT '{}'::jsonb,
    
    -- Audit
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_checks_inspection ON inspection_checks(inspection_id);
CREATE INDEX idx_checks_category ON inspection_checks(category);
CREATE INDEX idx_checks_pass_fail ON inspection_checks(pass_fail);

CREATE TRIGGER update_inspection_checks_updated_at 
    BEFORE UPDATE ON inspection_checks 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();

```