
```sql
-- ============================================================================
-- KNOWLEDGE GAPS
-- ============================================================================

CREATE TABLE knowledge_gaps (
    gap_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_id UUID NOT NULL REFERENCES projects(project_id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    
    -- Gap Details
    topic TEXT NOT NULL,
    description TEXT,
    category TEXT,  -- planning, design, construction, costs, regulations
    
    -- Severity
    importance TEXT,  -- critical, high, medium, low
    urgency TEXT,  -- immediate, soon, eventually
    
    -- Status
    identified_date DATE NOT NULL DEFAULT CURRENT_DATE,
    status TEXT DEFAULT 'open',  -- open, learning, resolved
    
    -- Learning
    resources_recommended TEXT[],
    resources_used TEXT[],
    
    -- Resolution
    resolved BOOLEAN DEFAULT FALSE,
    resolution_date DATE,
    how_resolved TEXT,
    
    -- Confidence
    confidence_before INTEGER CHECK (confidence_before BETWEEN 1 AND 5),
    confidence_after INTEGER CHECK (confidence_after BETWEEN 1 AND 5),
    
    -- Notes
    notes TEXT,
    
    -- Audit
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_knowledge_gaps_project ON knowledge_gaps(project_id);
CREATE INDEX idx_knowledge_gaps_user ON knowledge_gaps(user_id);
CREATE INDEX idx_knowledge_gaps_topic ON knowledge_gaps(topic);
CREATE INDEX idx_knowledge_gaps_status ON knowledge_gaps(status);

CREATE TRIGGER update_knowledge_gaps_updated_at 
    BEFORE UPDATE ON knowledge_gaps 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();


-- ============================================================================
-- LESSONS LEARNED
-- ============================================================================

CREATE TABLE lessons_learned (
    lesson_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_id UUID NOT NULL REFERENCES projects(project_id) ON DELETE CASCADE,
    
    -- Lesson Details
    date_captured DATE NOT NULL DEFAULT CURRENT_DATE,
    phase TEXT,  -- planning, design, procurement, construction
    category TEXT,  -- what_went_well, challenge_overcome, mistake_made, near_miss
    
    -- Description
    description TEXT NOT NULL,
    root_cause TEXT,
    
    -- Impact
    cost_impact DECIMAL(12,2),
    time_impact_days INTEGER,
    quality_impact TEXT,
    stress_impact INTEGER CHECK (stress_impact BETWEEN 1 AND 10),
    
    -- Learning
    what_would_do_differently TEXT,
    advice_for_others TEXT,
    key_learning TEXT,
    
    -- Prevention
    preventable BOOLEAN,
    prevention_strategy TEXT,
    
    -- Linked Entities
    linked_decision_id UUID REFERENCES decisions(decision_id),
    linked_risk_id UUID REFERENCES risks(risk_id),
    linked_variation_id UUID REFERENCES variations(variation_id),
    
    -- Visibility
    share_publicly BOOLEAN DEFAULT FALSE,
    
    -- Notes
    notes TEXT,
    
    -- Audit
    captured_by UUID REFERENCES users(user_id),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_lessons_project ON lessons_learned(project_id);
CREATE INDEX idx_lessons_date ON lessons_learned(date_captured);
CREATE INDEX idx_lessons_phase ON lessons_learned(phase);
CREATE INDEX idx_lessons_category ON lessons_learned(category);

CREATE TRIGGER update_lessons_learned_updated_at 
    BEFORE UPDATE ON lessons_learned 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();
```