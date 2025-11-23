

```sql
-- ============================================================================
-- BUDGET CATEGORIES
-- ============================================================================

CREATE TABLE budget_categories (
    category_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_id UUID NOT NULL REFERENCES projects(project_id) ON DELETE CASCADE,
    
    -- Category Info
    category_name TEXT NOT NULL,
    category_code TEXT,  -- e.g., "GW" for groundworks, "STR" for structure
    parent_category_id UUID REFERENCES budget_categories(category_id),  -- For hierarchical categories
    
    -- Budget Allocation
    budgeted_amount DECIMAL(15,2) NOT NULL DEFAULT 0,
    
    -- Display
    display_order INTEGER,
    color_hex TEXT,  -- For visualizations
    
    -- Audit
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_budget_categories_project ON budget_categories(project_id);
CREATE INDEX idx_budget_categories_parent ON budget_categories(parent_category_id);

CREATE TRIGGER update_budget_categories_updated_at 
    BEFORE UPDATE ON budget_categories 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();


-- ============================================================================
-- COSTS (Actual Spending)
-- ============================================================================

CREATE TYPE cost_status AS ENUM (
    'estimated',
    'quoted',
    'committed',
    'invoiced',
    'paid'
);

CREATE TABLE costs (
    cost_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_id UUID NOT NULL REFERENCES projects(project_id) ON DELETE CASCADE,
    
    -- Classification
    budget_category_id UUID REFERENCES budget_categories(category_id),
    cost_type TEXT,  -- labour, materials, professional_fees, plant, other
    
    -- Description
    description TEXT NOT NULL,
    reference TEXT,  -- Invoice number, quote reference
    
    -- Amounts
    estimated_amount DECIMAL(15,2),
    quoted_amount DECIMAL(15,2),
    actual_amount DECIMAL(15,2),
    vat_amount DECIMAL(15,2),
    total_including_vat DECIMAL(15,2) GENERATED ALWAYS AS (
        COALESCE(actual_amount, quoted_amount, estimated_amount) + COALESCE(vat_amount, 0)
    ) STORED,
    
    -- Status
    status cost_status DEFAULT 'estimated',
    
    -- Dates
    cost_date DATE NOT NULL,
    due_date DATE,
    paid_date DATE,
    
    -- Payment
    payment_method TEXT,  -- bank_transfer, card, cash, cheque
    payment_reference TEXT,
    
    -- Relationships
    linked_room_id UUID REFERENCES rooms(room_id),
    linked_material_id UUID REFERENCES materials(material_id),
    linked_supplier_id UUID REFERENCES suppliers(supplier_id),
    linked_order_id UUID REFERENCES material_orders(order_id),
    
    -- Responsibility
    responsible_party TEXT,  -- client, contractor, subcontractor
    
    -- Notes
    notes TEXT,
    
    -- Metadata
    cost_metadata JSONB DEFAULT '{}'::jsonb,
    
    -- Audit
    created_by UUID REFERENCES users(user_id),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    
    -- Constraints
    CONSTRAINT positive_amounts CHECK (
        (estimated_amount IS NULL OR estimated_amount >= 0) AND
        (quoted_amount IS NULL OR quoted_amount >= 0) AND
        (actual_amount IS NULL OR actual_amount >= 0)
    )
);

CREATE INDEX idx_costs_project ON costs(project_id);
CREATE INDEX idx_costs_category ON costs(budget_category_id);
CREATE INDEX idx_costs_status ON costs(status);
CREATE INDEX idx_costs_date ON costs(cost_date);
CREATE INDEX idx_costs_room ON costs(linked_room_id);
CREATE INDEX idx_costs_material ON costs(linked_material_id);
CREATE INDEX idx_costs_supplier ON costs(linked_supplier_id);

CREATE TRIGGER update_costs_updated_at 
    BEFORE UPDATE ON costs 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();


-- ============================================================================
-- BUDGET SUMMARY VIEW (Materialized for Performance)
-- ============================================================================

CREATE MATERIALIZED VIEW budget_summary AS
SELECT 
    bc.project_id,
    bc.category_id,
    bc.category_name,
    bc.budgeted_amount,
    COALESCE(SUM(c.actual_amount), 0) AS spent_amount,
    bc.budgeted_amount - COALESCE(SUM(c.actual_amount), 0) AS remaining_amount,
    CASE 
        WHEN bc.budgeted_amount > 0 THEN 
            (COALESCE(SUM(c.actual_amount), 0) / bc.budgeted_amount * 100)
        ELSE 0 
    END AS percentage_spent
FROM budget_categories bc
LEFT JOIN costs c ON bc.category_id = c.budget_category_id 
    AND c.status IN ('invoiced', 'paid')
GROUP BY bc.project_id, bc.category_id, bc.category_name, bc.budgeted_amount;

CREATE INDEX idx_budget_summary_project ON budget_summary(project_id);

-- Refresh function
CREATE OR REPLACE FUNCTION refresh_budget_summary()
RETURNS TRIGGER AS $$
BEGIN
    REFRESH MATERIALIZED VIEW CONCURRENTLY budget_summary;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

-- Auto-refresh when costs change
CREATE TRIGGER refresh_budget_on_cost_change
AFTER INSERT OR UPDATE OR DELETE ON costs
FOR EACH STATEMENT
EXECUTE FUNCTION refresh_budget_summary();
```