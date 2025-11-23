
```sql
-- ============================================================================
-- PROFESSIONALS (Architects, Engineers, etc.)
-- ============================================================================

CREATE TYPE professional_type AS ENUM (
    'architect',
    'structural_engineer',
    'mep_engineer',
    'quantity_surveyor',
    'planning_consultant',
    'building_control',
    'party_wall_surveyor',
    'ecological_consultant',
    'principal_designer',
    'other'
);

CREATE TABLE professionals (
    professional_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_id UUID NOT NULL REFERENCES projects(project_id) ON DELETE CASCADE,
    
    -- Basic Info
    professional_type professional_type NOT NULL,
    name TEXT NOT NULL,
    practice_name TEXT,
    
    -- Contact
    email TEXT,
    phone TEXT,
    address TEXT,
    website TEXT,
    
    -- Engagement
    hired BOOLEAN DEFAULT FALSE,
    contract_date DATE,
    contract_reference TEXT,
    
    -- Scope
    riba_stages_responsible TEXT[],  -- Which stages they're covering
    scope_of_works TEXT,
    
    -- Fees
    fee_structure TEXT,  -- fixed, percentage, hourly, stage_based
    agreed_fee DECIMAL(12,2),
    actual_fee DECIMAL(12,2),
    
    -- Performance
    performance_rating INTEGER CHECK (performance_rating BETWEEN 1 AND 10),
    strengths TEXT[],
    weaknesses TEXT[],
    would_use_again BOOLEAN,
    would_recommend BOOLEAN,
    
    -- Status
    status TEXT DEFAULT 'active',  -- active, completed, terminated
    
    -- Notes
    notes TEXT,
    
    -- Audit
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_professionals_project ON professionals(project_id);
CREATE INDEX idx_professionals_type ON professionals(professional_type);
CREATE INDEX idx_professionals_hired ON professionals(hired);

CREATE TRIGGER update_professionals_updated_at 
    BEFORE UPDATE ON professionals 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();


-- ============================================================================
-- CONTRACTORS & SUBCONTRACTORS
-- ============================================================================

CREATE TABLE contractors (
    contractor_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_id UUID NOT NULL REFERENCES projects(project_id) ON DELETE CASCADE,
    
    -- Basic Info
    contractor_type TEXT,  -- main_contractor, subcontractor
    company_name TEXT NOT NULL,
    contact_name TEXT,
    
    -- Contact
    email TEXT,
    phone TEXT,
    address TEXT,
    
    -- Trade/Specialty
    trade TEXT,  -- groundworker, bricklayer, roofer, electrician, plumber, etc.
    specialties TEXT[],
    
    -- Engagement
    contract_type TEXT,  -- fixed_price, day_rate, cost_plus
    contract_value DECIMAL(15,2),
    payment_terms TEXT,
    
    -- Dates
    start_date DATE,
    completion_date DATE,
    
    -- Insurance & Compliance
    insurance_verified BOOLEAN DEFAULT FALSE,
    insurance_expiry_date DATE,
    qualifications TEXT[],  -- Gas Safe, NICEIC, etc.
    
    -- Performance Tracking
    tasks_assigned INTEGER DEFAULT 0,
    tasks_completed INTEGER DEFAULT 0,
    
    quality_rating INTEGER CHECK (quality_rating BETWEEN 1 AND 10),
    snagging_items_attributed INTEGER DEFAULT 0,
    
    on_time_performance INTEGER CHECK (on_time_performance BETWEEN 1 AND 10),
    
    would_use_again BOOLEAN,
    would_recommend BOOLEAN,
    
    -- Notes
    notes TEXT,
    performance_notes TEXT,
    
    -- Status
    status TEXT DEFAULT 'active',  -- active, completed, terminate
    
    -- Audit
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_contractors_project ON contractors(project_id);
CREATE INDEX idx_contractors_trade ON contractors(trade);
CREATE INDEX idx_contractors_status ON contractors(status);
CREATE INDEX idx_contractors_rating ON contractors(quality_rating);

CREATE TRIGGER update_contractors_updated_at 
    BEFORE UPDATE ON contractors 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();
    
```