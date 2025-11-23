
```sql
-- ============================================================================
-- VARIATIONS / CHANGE ORDERS
-- ============================================================================

CREATE TYPE variation_status AS ENUM (
    'pending',
    'submitted',
    'approved',
    'rejected',
    'in_progress',
    'completed',
    'disputed',
    'cancelled'
);

CREATE TABLE variations (
    variation_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_id UUID NOT NULL REFERENCES projects(project_id) ON DELETE CASCADE,
    
    -- Variation Details
    variation_number TEXT NOT NULL,  -- VO-001, VO-002
    variation_title TEXT NOT NULL,
    description TEXT NOT NULL,
    
    -- Classification
    change_type TEXT NOT NULL,  -- design_change, spec_upgrade, omission, addition, remedial_work
    reason TEXT,  -- client_request, unforeseen_conditions, regulatory_requirement, error_correction
    
    -- Raised By
    raised_date DATE NOT NULL DEFAULT CURRENT_DATE,
    raised_by TEXT NOT NULL,
    raised_by_user_id UUID REFERENCES users(user_id),
    
    -- Impact Assessment
    cost_impact DECIMAL(15,2),
    programme_impact_days INTEGER,
    critical_path_affected BOOLEAN DEFAULT FALSE,
    
    -- Cost Breakdown
    labour_cost DECIMAL(12,2),
    materials_cost DECIMAL(12,2),
    plant_cost DECIMAL(12,2),
    preliminaries_cost DECIMAL(12,2),
    overheads_profit DECIMAL(12,2),
    
    -- Approval
    submitted_for_approval DATE,
    approver TEXT,
    approver_user_id UUID REFERENCES users(user_id),
    approved BOOLEAN,
    approval_date DATE,
    approval_conditions TEXT[],
    rejection_reason TEXT,
    
    -- Status
    status variation_status DEFAULT 'pending',
    
    -- Implementation
    implementation_start_date DATE,
    implementation_completion_date DATE,
    contractor TEXT,
    
    -- Quality Check
    quality_check_completed BOOLEAN DEFAULT FALSE,
    quality_check_date DATE,
    quality_check_by TEXT,
    
    -- Payment
    invoiced BOOLEAN DEFAULT FALSE,
    invoice_reference TEXT,
    invoice_date DATE,
    paid BOOLEAN DEFAULT FALSE,
    payment_date DATE,
    
    -- Disputes
    disputed BOOLEAN DEFAULT FALSE,
    dispute_reason TEXT,
    dispute_resolution TEXT,
    
    -- Linked Entities
    affects_room_ids UUID[],
    affects_task_ids UUID[],
    linked_decision_id UUID REFERENCES decisions(decision_id),
    linked_risk_id UUID REFERENCES risks(risk_id),
    original_design_choice_ids UUID[],
    original_cost_item_ids UUID[],
    
    -- Documentation
    quotations TEXT[],
    instructions TEXT[],
    drawings_revised TEXT[],
    specifications_updated TEXT[],
    photo_urls TEXT[],
    
    -- Notes
    notes TEXT,
    
    -- Audit
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_variations_project ON variations(project_id);
CREATE INDEX idx_variations_number ON variations(variation_number);
CREATE INDEX idx_variations_status ON variations(status);
CREATE INDEX idx_variations_raised_date ON variations(raised_date);
CREATE INDEX idx_variations_approved ON variations(approved);
CREATE INDEX idx_variations_disputed ON variations(disputed);

CREATE TRIGGER update_variations_updated_at 
    BEFORE UPDATE ON variations 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();
```