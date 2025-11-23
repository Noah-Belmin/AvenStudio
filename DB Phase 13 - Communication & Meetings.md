
```sql
-- ============================================================================
-- MEETINGS
-- ============================================================================

CREATE TYPE meeting_type AS ENUM (
    'site_meeting',
    'design_review',
    'progress_meeting',
    'client_decision',
    'planning_officer',
    'inspection',
    'coordination',
    'other'
);

CREATE TABLE meetings (
    meeting_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_id UUID NOT NULL REFERENCES projects(project_id) ON DELETE CASCADE,
    
    -- Meeting Details
    meeting_title TEXT NOT NULL,
    meeting_type meeting_type NOT NULL,
    
    -- When & Where
    meeting_date DATE NOT NULL,
    meeting_time TIME,
    duration_minutes INTEGER,
    location TEXT,  -- on_site, office, video_call
    
    -- Attendees
    attendees JSONB DEFAULT '[]'::jsonb,  -- Array of {name, role, organization}
    
    -- Agenda
    agenda_items TEXT[],
    
    -- Discussion
    discussion_points JSONB DEFAULT '[]'::jsonb,  -- Array of {topic, summary}
    
    -- Outcomes
    decisions_made_ids UUID[],  -- Links to decisions table
    action_items JSONB DEFAULT '[]'::jsonb,  -- Array of {action, responsible, due_date, status}
    risks_identified UUID[],  -- Links to risks table
    issues_raised TEXT[],
    
    -- Next Meeting
    next_meeting_scheduled BOOLEAN DEFAULT FALSE,
    next_meeting_date DATE,
    next_meeting_purpose TEXT,
    
    -- Documentation
    minutes_document_id UUID REFERENCES documents(document_id),
    photo_ids UUID[],
    
    -- Notes
    notes TEXT,
    
    -- Satisfaction
    attendee_satisfaction TEXT,  -- productive, mixed, frustrating
    
    -- Audit
    created_by UUID REFERENCES users(user_id),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_meetings_project ON meetings(project_id);
CREATE INDEX idx_meetings_date ON meetings(meeting_date);
CREATE INDEX idx_meetings_type ON meetings(meeting_type);
CREATE INDEX idx_meetings_decisions ON meetings USING GIN(decisions_made_ids);
CREATE INDEX idx_meetings_attendees ON meetings USING GIN(attendees);

CREATE TRIGGER update_meetings_updated_at 
    BEFORE UPDATE ON meetings 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();


-- ============================================================================
-- COMMUNICATIONS / CORRESPONDENCE
-- ============================================================================

CREATE TYPE communication_direction AS ENUM (
    'sent',
    'received'
);

CREATE TYPE communication_method AS ENUM (
    'email',
    'letter',
    'phone',
    'text',
    'meeting',
    'site_visit',
    'other'
);

CREATE TABLE communications (
    communication_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_id UUID NOT NULL REFERENCES projects(project_id) ON DELETE CASCADE,
    
    -- Communication Details
    date DATE NOT NULL DEFAULT CURRENT_DATE,
    direction communication_direction NOT NULL,
    method communication_method NOT NULL,
    
    -- Parties
    from_party TEXT NOT NULL,
    to_parties TEXT[] NOT NULL,
    cc_parties TEXT[],
    
    -- Content
    subject TEXT NOT NULL,
    summary TEXT,
    reference TEXT,  -- Email subject, letter reference
    
    -- Classification
    category TEXT,  -- instruction, information, query, approval, complaint
    priority TEXT DEFAULT 'normal',  -- low, normal, high, urgent
    
    -- Response
    response_required BOOLEAN DEFAULT FALSE,
    response_deadline DATE,
    response_received BOOLEAN DEFAULT FALSE,
    response_date DATE,
    
    -- Linked Entities
    linked_decision_ids UUID[],
    linked_task_ids UUID[],
    linked_risk_ids UUID[],
    linked_variation_ids UUID[],
    linked_snag_ids UUID[],
    
    -- Attachments
    attachment_document_ids UUID[],
    
    -- Status
    status TEXT DEFAULT 'filed',  -- pending, actioned, filed, archived
    
    -- Notes
    notes TEXT,
    
    -- Search
    search_vector tsvector GENERATED ALWAYS AS (
        to_tsvector('english', 
            coalesce(subject, '') || ' ' || 
            coalesce(summary, '') || ' ' ||
            coalesce(from_party, '') || ' ' ||
            coalesce(array_to_string(to_parties, ' '), '')
        )
    ) STORED,
    
    -- Audit
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_communications_project ON communications(project_id);
CREATE INDEX idx_communications_date ON communications(date);
CREATE INDEX idx_communications_direction ON communications(direction);
CREATE INDEX idx_communications_category ON communications(category);
CREATE INDEX idx_communications_response ON communications(response_required, response_received);
CREATE INDEX idx_communications_search ON communications USING GIN(search_vector);

CREATE TRIGGER update_communications_updated_at 
    BEFORE UPDATE ON communications 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();
```