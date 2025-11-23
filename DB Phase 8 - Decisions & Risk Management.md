
```sql
-- ============================================================================
-- DECISIONS LOG
-- ============================================================================

CREATE TABLE decisions (
    decision_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_id UUID NOT NULL REFERENCES projects(project_id) ON DELETE CASCADE,
    
    -- Decision Details
    decision_topic TEXT NOT NULL,
    decision_question TEXT,
    decision_made TEXT NOT NULL,
    
    -- Context
    decision_category TEXT,  -- design, procurement, programme, budget, compliance
    decision_date DATE NOT NULL DEFAULT CURRENT_DATE,
    
    -- Decision Process
    alternatives_considered TEXT[],
    reasoning TEXT,
    
    -- Confidence & Reversibility
    confidence_level INTEGER CHECK (confidence_level BETWEEN 1 AND 5),
    reversible BOOLEAN,
    reversal_cost_estimate DECIMAL(12,2),
    
    -- Impact Analysis
    cost_impact DECIMAL(12,2),
    programme_impact_days INTEGER,
    quality_impact TEXT,
    
    -- Dependencies
    dependent_decision_ids UUID[],  -- Other decisions that depend on this
    blocks_decisions UUID[],  -- Decisions waiting on this one
    
    -- Decision Makers
    decided_by UUID REFERENCES users(user_id),
    consulted_parties TEXT[],
    approval_required BOOLEAN DEFAULT FALSE,
    approved_by UUID REFERENCES users(user_id),
    approval_date DATE,
    
    -- Status
    status TEXT DEFAULT 'final',  -- proposed, under_review, final, reversed, superseded
    
    -- If Reversed
    reversed BOOLEAN DEFAULT FALSE,
    reversal_date DATE,
    reversal_reason TEXT,
    superseded_by_decision_id UUID REFERENCES decisions(decision_id),
    
    -- Linked Entities
    linked_room_ids UUID[],
    linked_material_ids UUID[],
    linked_cost_ids UUID[],
    linked_task_ids UUID[],
    linked_choice_id UUID REFERENCES design_choices(choice_id),
    
    -- Documentation
    supporting_documents TEXT[],
    
    -- Notes
    notes TEXT,
    
    -- Search
    search_vector tsvector GENERATED ALWAYS AS (
        to_tsvector('english', 
            coalesce(decision_topic, '') || ' ' || 
            coalesce(decision_question, '') || ' ' ||
            coalesce(decision_made, '') || ' ' ||
            coalesce(reasoning, '')
        )
    ) STORED,
    
    -- Audit
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_decisions_project ON decisions(project_id);
CREATE INDEX idx_decisions_date ON decisions(decision_date);
CREATE INDEX idx_decisions_category ON decisions(decision_category);
CREATE INDEX idx_decisions_status ON decisions(status);
CREATE INDEX idx_decisions_decided_by ON decisions(decided_by);
CREATE INDEX idx_decisions_search ON decisions USING GIN(search_vector);
CREATE INDEX idx_decisions_linked_rooms ON decisions USING GIN(linked_room_ids);

CREATE TRIGGER update_decisions_updated_at 
    BEFORE UPDATE ON decisions 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();


-- ============================================================================
-- RISKS REGISTER
-- ============================================================================

CREATE TYPE risk_category AS ENUM (
    'planning',
    'structural',
    'budget',
    'programme',
    'regulatory',
    'quality',
    'health_and_safety',
    'environmental',
    'stakeholder',
    'supply_chain'
);

CREATE TYPE risk_severity AS ENUM (
    'low',
    'medium',
    'high',
    'critical'
);

CREATE TYPE risk_status AS ENUM (
    'identified',
    'assessing',
    'monitoring',
    'mitigating',
    'realized',
    'resolved',
    'accepted'
);

CREATE TABLE risks (
    risk_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_id UUID NOT NULL REFERENCES projects(project_id) ON DELETE CASCADE,
    
    -- Risk Details
    risk_title TEXT NOT NULL,
    risk_description TEXT NOT NULL,
    category risk_category NOT NULL,
    
    -- Assessment
    likelihood risk_severity NOT NULL,  -- Probability of occurrence
    impact risk_severity NOT NULL,      -- Severity if it happens
    
    -- Overall Risk Score (calculated)
    risk_score INTEGER GENERATED ALWAYS AS (
        CASE likelihood
            WHEN 'low' THEN 1
            WHEN 'medium' THEN 2
            WHEN 'high' THEN 3
            WHEN 'critical' THEN 4
        END *
        CASE impact
            WHEN 'low' THEN 1
            WHEN 'medium' THEN 2
            WHEN 'high' THEN 3
            WHEN 'critical' THEN 4
        END
    ) STORED,
    
    -- Mitigation
    mitigation_strategy TEXT,
    mitigation_actions TEXT[],
    mitigation_cost DECIMAL(12,2),
    
    -- Ownership
    risk_owner TEXT,  -- Person responsible for monitoring
    risk_owner_user_id UUID REFERENCES users(user_id),
    
    -- Status
    status risk_status DEFAULT 'identified',
    
    -- Timeline
    identified_date DATE NOT NULL DEFAULT CURRENT_DATE,
    review_date DATE,
    last_reviewed DATE,
    
    -- If Realized
    realized BOOLEAN DEFAULT FALSE,
    realization_date DATE,
    actual_impact TEXT,
    actual_cost DECIMAL(12,2),
    
    -- Resolution
    resolved BOOLEAN DEFAULT FALSE,
    resolution_date DATE,
    resolution_description TEXT,
    
    -- Linked Entities
    linked_task_ids UUID[],
    linked_decision_ids UUID[],
    
    -- Notes
    notes TEXT,
    
    -- Audit
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_risks_project ON risks(project_id);
CREATE INDEX idx_risks_category ON risks(category);
CREATE INDEX idx_risks_severity ON risks(likelihood, impact);
CREATE INDEX idx_risks_score ON risks(risk_score);
CREATE INDEX idx_risks_status ON risks(status);
CREATE INDEX idx_risks_owner ON risks(risk_owner_user_id);
CREATE INDEX idx_risks_realized ON risks(realized);

CREATE TRIGGER update_risks_updated_at 
    BEFORE UPDATE ON risks 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();
```