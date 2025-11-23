
```sql
-- ============================================================================
-- NOTIFICATIONS / ALERTS
-- ============================================================================

CREATE TYPE notification_type AS ENUM (
    'task_due',
    'inspection_scheduled',
    'payment_due',
    'delivery_scheduled',
    'decision_required',
    'risk_escalated',
    'budget_alert',
    'milestone_approaching',
    'certificate_expiring',
    'information_request',
    'system_update'
);

CREATE TYPE notification_priority AS ENUM (
    'low',
    'normal',
    'high',
    'urgent'
);

CREATE TABLE notifications (
    notification_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    
    -- Target
    user_id UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    project_id UUID REFERENCES projects(project_id) ON DELETE CASCADE,
    
    -- Notification Details
    notification_type notification_type NOT NULL,
    priority notification_priority DEFAULT 'normal',
    
    -- Content
    title TEXT NOT NULL,
    message TEXT NOT NULL,
    
    -- Action
    action_url TEXT,  -- Deep link to relevant page
    action_label TEXT,  -- e.g., "View Task", "Approve Decision"
    
    -- Linked Entity
    linked_entity_type TEXT,  -- task, inspection, cost, decision, etc.
    linked_entity_id UUID,
    
    -- Status
    read BOOLEAN DEFAULT FALSE,
    read_at TIMESTAMPTZ,
    
    dismissed BOOLEAN DEFAULT FALSE,
    dismissed_at TIMESTAMPTZ,
    
    actioned BOOLEAN DEFAULT FALSE,
    actioned_at TIMESTAMPTZ,
    
    -- Delivery
    delivery_method TEXT DEFAULT 'in_app',  -- in_app, email, sms, push
    sent BOOLEAN DEFAULT FALSE,
    sent_at TIMESTAMPTZ,
    
    -- Expiry
    expires_at TIMESTAMPTZ,
    
    -- Audit
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_notifications_user ON notifications(user_id);
CREATE INDEX idx_notifications_project ON notifications(project_id);
CREATE INDEX idx_notifications_type ON notifications(notification_type);
CREATE INDEX idx_notifications_read ON notifications(read);
CREATE INDEX idx_notifications_priority ON notifications(priority);
CREATE INDEX idx_notifications_created ON notifications(created_at);
CREATE INDEX idx_notifications_unread_user ON notifications(user_id, read) WHERE read = FALSE;
```