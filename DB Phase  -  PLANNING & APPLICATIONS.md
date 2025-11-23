
```sql
-- ============================================================================
-- PLANNING APPLICATIONS
-- ============================================================================

CREATE TYPE application_status AS ENUM (
    'not_submitted',
    'submitted',
    'validated',
    'under_review',
    'approved',
    'refused',
    'withdrawn',
    'appealed'
);

CREATE TABLE planning_applications (
    application_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_id UUID NOT NULL REFERENCES projects(project_id) ON DELETE CASCADE,
    
    -- Application Details
    application_type TEXT NOT NULL,  -- full, outline, reserved_matters, listed_building
    application_reference TEXT UNIQUE,
    
    -- Dates
    submission_date DATE,
    validation_date DATE,
    target_decision_date DATE,
    actual_decision_date DATE,
    
    -- Status
    status application_status DEFAULT 'not_submitted',
    
    -- Case Officer
    case_officer_name TEXT,
    case_officer_contact TEXT,
    last_contact_date DATE,
    
    -- Outcome
    decision TEXT,  -- approved, refused, etc.
    decision_notes TEXT,
    
    -- Conditions
    conditions_count INTEGER DEFAULT 0,
    
    -- Consultations
    neighbour_letters_sent INTEGER,
    objections_received INTEGER,
    support_received INTEGER,
    
    -- Appeal
    appeal_lodged BOOLEAN DEFAULT FALSE,
    appeal_reference TEXT,
    appeal_date DATE,
    appeal_decision TEXT,
    
    -- Documents
    document_ids UUID[],
    
    -- Notes
    notes TEXT,
    
    -- Audit
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_planning_project ON planning_applications(project_id);
CREATE INDEX idx_planning_reference ON planning_applications(application_reference);
CREATE INDEX idx_planning_status ON planning_applications(status);

CREATE TRIGGER update_planning_applications_updated_at 
    BEFORE UPDATE ON planning_applications 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();


-- ============================================================================
-- PLANNING CONDITIONS
-- ============================================================================

CREATE TABLE planning_conditions (
    condition_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    application_id UUID NOT NULL REFERENCES planning_applications(application_id) ON DELETE CASCADE,
    
    -- Condition Details
    condition_number TEXT NOT NULL,
    condition_text TEXT NOT NULL,
    category TEXT NOT NULL,  -- pre_commencement, pre_occupation, ongoing
    
    -- Requirements
    submission_requirements TEXT[],
    
    -- Discharge
    submission_date DATE,
    documents_submitted TEXT[],
    
    -- Review
    reviewed BOOLEAN DEFAULT FALSE,
    review_date DATE,
    outcome TEXT,  -- approved, further_info_required, rejected
    officer_comments TEXT,
    
    -- Status
    status TEXT DEFAULT 'pending',  -- pending, submitted, approved, ongoing
    
    -- Evidence
    compliance_evidence TEXT[],
    
    -- Audit
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_conditions_application ON planning_conditions(application_id);
CREATE INDEX idx_conditions_category ON planning_conditions(category);
CREATE INDEX idx_conditions_status ON planning_conditions(status);

CREATE TRIGGER update_planning_conditions_updated_at 
    BEFORE UPDATE ON planning_conditions 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();


-- ============================================================================
-- CERTIFICATES
-- ============================================================================

CREATE TABLE certificates (
    certificate_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_id UUID NOT NULL REFERENCES projects(project_id) ON DELETE CASCADE,
    
    -- Certificate Details
    certificate_type TEXT NOT NULL,  -- building_control, electrical, gas, energy, structural
    certificate_name TEXT NOT NULL,
    certificate_number TEXT,
    
    -- Issuer
    issued_by TEXT NOT NULL,
    issuing_organization TEXT,
    issuer_contact TEXT,
    
    -- Dates
    issue_date DATE NOT NULL,
    expiry_date DATE,
    renewal_required BOOLEAN DEFAULT FALSE,
    renewal_date DATE,
    
    -- Scope
    scope_description TEXT,
    conditions TEXT[],
    
    -- Verification
    verified BOOLEAN DEFAULT FALSE,
    verified_by TEXT,
    verification_date DATE,
    
    -- Insurance
    insurance_required BOOLEAN DEFAULT FALSE,
    
    -- Linked Entities
    linked_inspection_id UUID REFERENCES inspections(inspection_id),
    linked_task_id UUID REFERENCES tasks(task_id),
    
    -- File
    certificate_file_url TEXT,
    document_id UUID REFERENCES documents(document_id),
    
    -- Notes
    notes TEXT,
    
    -- Audit
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_certificates_project ON certificates(project_id);
CREATE INDEX idx_certificates_type ON certificates(certificate_type);
CREATE INDEX idx_certificates_issue_date ON certificates(issue_date);
CREATE INDEX idx_certificates_expiry ON certificates(expiry_date);

CREATE TRIGGER update_certificates_updated_at 
    BEFORE UPDATE ON certificates 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();
```