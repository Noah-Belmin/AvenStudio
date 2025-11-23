

```sql

-- ============================================================================
-- MATERIALS INVENTORY
-- ============================================================================

CREATE TYPE procurement_status AS ENUM (
    'researching',
    'quoted',
    'approved',
    'ordered',
    'in_transit',
    'delivered',
    'installed',
    'returned',
    'cancelled'
);

CREATE TABLE materials (
    material_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_id UUID NOT NULL REFERENCES projects(project_id) ON DELETE CASCADE,
    
    -- Classification
    category TEXT NOT NULL,  -- structural, envelope, finishes, services
    subcategory TEXT,
    trade TEXT,  -- groundworker, bricklayer, carpenter, etc.
    
    -- Product Info
    product_name TEXT NOT NULL,
    manufacturer TEXT,
    manufacturer_part_number TEXT,
    description TEXT,
    
    -- Technical Specification
    technical_spec JSONB DEFAULT '{}'::jsonb,  -- dimensions, grade, performance
    data_sheet_url TEXT,
    
    -- Quantities
    unit_of_measure TEXT NOT NULL,  -- m2, linear_m, nr, kg, litres
    estimated_quantity DECIMAL(12,3),
    ordered_quantity DECIMAL(12,3),
    delivered_quantity DECIMAL(12,3),
    installed_quantity DECIMAL(12,3),
    wastage_allowance_percentage DECIMAL(5,2) DEFAULT 10.00,
    actual_wastage_percentage DECIMAL(5,2),
    
    -- Costs
    unit_price DECIMAL(12,2),
    total_cost DECIMAL(12,2) GENERATED ALWAYS AS (
        ordered_quantity * unit_price
    ) STORED,
    
    -- Sourcing
    supplier_name TEXT,
    supplier_contact TEXT,
    lead_time_weeks INTEGER,
    
    -- Status
    procurement_status procurement_status DEFAULT 'researching',
    
    -- Storage
    storage_location TEXT,
    storage_requirements TEXT[],  -- keep_dry, secure, temperature_controlled
    
    -- Compliance
    ce_marking BOOLEAN DEFAULT FALSE,
    ukca_marking BOOLEAN DEFAULT FALSE,
    fire_rating TEXT,
    sustainability_rating TEXT,
    certifications TEXT[],
    
    -- Relationships
    linked_room_ids UUID[],  -- Array of room IDs where this material is used
    linked_choice_id UUID REFERENCES design_choices(choice_id),
    
    -- Flexible data
    material_metadata JSONB DEFAULT '{}'::jsonb,
    
    -- Search
    search_vector tsvector GENERATED ALWAYS AS (
        to_tsvector('english', 
            coalesce(product_name, '') || ' ' || 
            coalesce(manufacturer, '') || ' ' ||
            coalesce(description, '') || ' ' ||
            coalesce(category, '')
        )
    ) STORED,
    
    -- Audit
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_materials_project ON materials(project_id);
CREATE INDEX idx_materials_category ON materials(category);
CREATE INDEX idx_materials_status ON materials(procurement_status);
CREATE INDEX idx_materials_supplier ON materials(supplier_name);
CREATE INDEX idx_materials_search ON materials USING GIN(search_vector);
CREATE INDEX idx_materials_metadata ON materials USING GIN(material_metadata);
CREATE INDEX idx_materials_linked_rooms ON materials USING GIN(linked_room_ids);

CREATE TRIGGER update_materials_updated_at 
    BEFORE UPDATE ON materials 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();


-- ============================================================================
-- MATERIAL ORDERS
-- ============================================================================

CREATE TYPE order_status AS ENUM (
    'pending',
    'confirmed',
    'dispatched',
    'delivered',
    'cancelled',
    'returned'
);

CREATE TABLE material_orders (
    order_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_id UUID NOT NULL REFERENCES projects(project_id) ON DELETE CASCADE,
    material_id UUID NOT NULL REFERENCES materials(material_id) ON DELETE CASCADE,
    
    -- Order Details
    order_reference TEXT,  -- Supplier's PO number
    order_date DATE NOT NULL,
    ordered_by UUID REFERENCES users(user_id),
    
    -- Quantities & Pricing
    quantity_ordered DECIMAL(12,3) NOT NULL,
    unit_price DECIMAL(12,2) NOT NULL,
    subtotal DECIMAL(12,2) GENERATED ALWAYS AS (quantity_ordered * unit_price) STORED,
    delivery_charge DECIMAL(12,2) DEFAULT 0,
    total_amount DECIMAL(12,2) GENERATED ALWAYS AS (
        (quantity_ordered * unit_price) + delivery_charge
    ) STORED,
    
    -- Delivery
    requested_delivery_date DATE,
    confirmed_delivery_date DATE,
    actual_delivery_date DATE,
    delivery_address TEXT,
    
    -- Status
    status order_status DEFAULT 'pending',
    
    -- Tracking
    tracking_reference TEXT,
    
    -- Order metadata
    order_notes TEXT,
    special_instructions TEXT,
    
    -- Audit
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_orders_project ON material_orders(project_id);
CREATE INDEX idx_orders_material ON material_orders(material_id);
CREATE INDEX idx_orders_status ON material_orders(status);
CREATE INDEX idx_orders_delivery_date ON material_orders(actual_delivery_date);

CREATE TRIGGER update_material_orders_updated_at 
    BEFORE UPDATE ON material_orders 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();


-- ============================================================================
-- SUPPLIERS
-- ============================================================================

CREATE TABLE suppliers (
    supplier_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_id UUID NOT NULL REFERENCES projects(project_id) ON DELETE CASCADE,
    
    -- Basic Info
    supplier_name TEXT NOT NULL,
    supplier_type TEXT,  -- merchant, specialist, manufacturer, trade_counter
    
    -- Contact
    contact_name TEXT,
    phone TEXT,
    email TEXT,
    website TEXT,
    address TEXT,
    
    -- Account
    account_number TEXT,
    account_status TEXT,  -- cash, trade_account, credit_terms
    payment_terms TEXT,
    discount_percentage DECIMAL(5,2),
    
    -- Performance Tracking
    orders_placed INTEGER DEFAULT 0,
    on_time_deliveries INTEGER DEFAULT 0,
    quality_issues INTEGER DEFAULT 0,
    overall_rating INTEGER CHECK (overall_rating BETWEEN 1 AND 10),
    
    -- Preferences
    preferred BOOLEAN DEFAULT FALSE,
    would_use_again BOOLEAN,
    
    -- Notes
    notes TEXT,
    
    -- Metadata
    supplier_metadata JSONB DEFAULT '{}'::jsonb,
    
    -- Audit
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_suppliers_project ON suppliers(project_id);
CREATE INDEX idx_suppliers_name ON suppliers(supplier_name);
CREATE INDEX idx_suppliers_preferred ON suppliers(preferred);

CREATE TRIGGER update_suppliers_updated_at 
    BEFORE UPDATE ON suppliers 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();
```