```SQL
-- ============================================================================
-- PROJECT DASHBOARD VIEW (Materialized for Performance)
-- ============================================================================

CREATE MATERIALIZED VIEW project_dashboard AS
SELECT 
    p.project_id,
    p.project_name,
    p.current_stage,
    p.completion_percentage,
    
    -- Timeline
    p.project_start_date,
    p.planned_completion_date,
    CURRENT_DATE - p.project_start_date AS days_elapsed,
    p.planned_completion_date - CURRENT_DATE AS days_remaining,
    
    -- Budget
    p.total_budget_amount,
    COALESCE(SUM(c.actual_amount), 0) AS total_spent,
    p.total_budget_amount - COALESCE(SUM(c.actual_amount), 0) AS budget_remaining,
    CASE 
        WHEN p.total_budget_amount > 0 THEN 
            (COALESCE(SUM(c.actual_amount), 0) / p.total_budget_amount * 100)
        ELSE 0 
    END AS budget_percentage_spent,
    
    -- Tasks
    COUNT(DISTINCT t.task_id) AS total_tasks,
    COUNT(DISTINCT t.task_id) FILTER (WHERE t.status = 'completed') AS completed_tasks,
    COUNT(DISTINCT t.task_id) FILTER (WHERE t.status = 'in_progress') AS in_progress_tasks,
    COUNT(DISTINCT t.task_id) FILTER (WHERE t.status = 'not_started') AS pending_tasks,
    
    -- Snagging
    COUNT(DISTINCT s.snag_id) AS total_snags,
    COUNT(DISTINCT s.snag_id) FILTER (WHERE s.severity = 'critical') AS critical_snags,
    COUNT(DISTINCT s.snag_id) FILTER (WHERE s.status IN ('identified', 'allocated', 'in_progress')) AS open_snags,
    
    -- Inspections
    COUNT(DISTINCT i.inspection_id) AS total_inspections,
    COUNT(DISTINCT i.inspection_id) FILTER (WHERE i.result = 'pass') AS inspections_passed,
    COUNT(DISTINCT i.inspection_id) FILTER (WHERE i.result = 'fail') AS inspections_failed,
    
    -- Rooms
    COUNT(DISTINCT r.room_id) AS total_rooms,
    AVG(r.completion_percentage) AS avg_room_completion,
    
    -- Last Activity
    MAX(GREATEST(
        p.updated_at,
        c.updated_at,
        t.updated_at,
        s.updated_at
    )) AS last_activity
    
FROM projects p
LEFT JOIN costs c ON p.project_id = c.project_id AND c.status IN ('invoiced', 'paid')
LEFT JOIN tasks t ON p.project_id = t.project_id
LEFT JOIN snagging_items s ON p.project_id = s.project_id
LEFT JOIN inspections i ON p.project_id = i.project_id
LEFT JOIN rooms r ON p.project_id = r.project_id
GROUP BY p.project_id, p.project_name, p.current_stage, p.completion_percentage,
         p.project_start_date, p.planned_completion_date, p.total_budget_amount;

CREATE UNIQUE INDEX idx_project_dashboard_project ON project_dashboard(project_id);


-- ============================================================================
-- ROOM SUMMARY VIEW
-- ============================================================================

CREATE MATERIALIZED VIEW room_summary AS
SELECT 
    r.room_id,
    r.project_id,
    r.room_name,
    r.room_type,
    r.area_sqm,
    r.completion_percentage,
    
    -- Design Choices
    COUNT(DISTINCT dc.choice_id) AS design_choices_count,
    COUNT(DISTINCT dc.choice_id) FILTER (WHERE dc.status = 'installed') AS design_choices_complete,
    
    -- Costs
    COALESCE(SUM(c.actual_amount), 0) AS total_cost,
    
    -- Tasks
    COUNT(DISTINCT t.task_id) AS tasks_count,
    COUNT(DISTINCT t.task_id) FILTER (WHERE t.status = 'completed') AS tasks_completed,
    
    -- Snagging
    COUNT(DISTINCT s.snag_id) AS snags_count,
    COUNT(DISTINCT s.snag_id) FILTER (WHERE s.status NOT IN ('closed', 'verified')) AS snags_open,
    
    -- Cost per sqm
    CASE 
        WHEN r.area_sqm > 0 THEN COALESCE(SUM(c.actual_amount), 0) / r.area_sqm
        ELSE 0
    END AS cost_per_sqm
    
FROM rooms r
LEFT JOIN design_choices dc ON r.room_id = dc.room_id
LEFT JOIN costs c ON r.room_id = c.linked_room_id AND c.status IN ('invoiced', 'paid')
LEFT JOIN tasks t ON r.room_id = ANY(t.linked_room_ids)
LEFT JOIN snagging_items s ON r.room_id = s.room_id
GROUP BY r.room_id, r.project_id, r.room_name, r.room_type, r.area_sqm, r.completion_percentage;

CREATE UNIQUE INDEX idx_room_summary_room ON room_summary(room_id);
CREATE INDEX idx_room_summary_project ON room_summary(project_id);


-- ============================================================================
-- REFRESH FUNCTIONS
-- ============================================================================

CREATE OR REPLACE FUNCTION refresh_all_materialized_views()
RETURNS void AS $$
BEGIN
    REFRESH MATERIALIZED VIEW CONCURRENTLY budget_summary;
    REFRESH MATERIALIZED VIEW CONCURRENTLY project_dashboard;
    REFRESH MATERIALIZED VIEW CONCURRENTLY room_summary;
END;
$$ LANGUAGE plpgsql;

-- Schedule automatic refresh (requires pg_cron extension)
-- SELECT cron.schedule('refresh-views', '0 * * * *', 'SELECT refresh_all_materialized_views()');
```