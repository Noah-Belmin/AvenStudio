
Currently Incomplete

```SQL
-- ==================================================
-- AVEN KNOWLEDGE ENGINE - COMPLETE DATABASE SCHEMA
-- ==================================================
-- Purpose: Comprehensive relational schema for residential design risk management
-- Supports: Design Risk Map + Building Regulations + Standards + Project tracking
-- Version: 1.0
-- ============================================

-- ============================================
-- CORE REFERENCE TABLES
-- ============================================

-- RIBA Stages / Project Phases
CREATE TABLE phases (
    phase_id VARCHAR(50) PRIMARY KEY,
    riba_stage VARCHAR(10) NOT NULL,
    phase_name VARCHAR(100) NOT NULL,
    description TEXT,
    typical_duration_weeks INT,
    sequence_order INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE INDEX idx_phases_sequence ON phases(sequence_order);

-- Impact Domains (Cost, Thermal, Acoustic, etc.)
CREATE TABLE impact_domains (
    domain_id VARCHAR(50) PRIMARY KEY,
    domain_name VARCHAR(100) NOT NULL,
    color_hex VARCHAR(7),
    description TEXT,
    icon_name VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Severity Levels
CREATE TABLE severity_levels (
    severity_id VARCHAR(20) PRIMARY KEY,
    level_number INT NOT NULL,
    level_name VARCHAR(50) NOT NULL,
    description TEXT,
    typical_cost_min DECIMAL(10,2),
    typical_cost_max DECIMAL(10,2),
    color_hex VARCHAR(7),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_severity_level ON severity_levels(level_number);

-- Probability Levels
CREATE TABLE probability_levels (
    probability_id VARCHAR(20) PRIMARY KEY,
    level_number INT NOT NULL,
    level_name VARCHAR(50) NOT NULL,
    percentage_range VARCHAR(20),
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- UK Building Regulations & Standards
CREATE TABLE standards (
    standard_id VARCHAR(50) PRIMARY KEY,
    standard_code VARCHAR(50) NOT NULL, -- e.g., "BS_5250", "PART_L", "TM59"
    standard_type ENUM('Building_Regulation', 'British_Standard', 'CIBSE_Guide', 'Other') NOT NULL,
    full_title TEXT NOT NULL,
    version VARCHAR(20),
    publication_year INT,
    authority VARCHAR(100), -- e.g., "MHCLG", "BSI", "CIBSE"
    status ENUM('Current', 'Superseded', 'Withdrawn') DEFAULT 'Current',
    summary TEXT,
    official_url VARCHAR(500),
    pdf_url VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE INDEX idx_standards_code ON standards(standard_code);
CREATE INDEX idx_standards_type ON standards(standard_type);

-- Risk Categories
CREATE TABLE risk_categories (
    category_id VARCHAR(50) PRIMARY KEY,
    category_name VARCHAR(100) NOT NULL,
    description TEXT,
    parent_category_id VARCHAR(50),
    sequence_order INT,
    icon_name VARCHAR(50),
    FOREIGN KEY (parent_category_id) REFERENCES risk_categories(category_id) ON DELETE SET NULL
);

-- ============================================
-- DESIGN RISKS - MAIN TABLES
-- ============================================

-- Main Risks Table
CREATE TABLE design_risks (
    risk_id VARCHAR(20) PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    category_id VARCHAR(50) NOT NULL,
    severity_id VARCHAR(20) NOT NULL,
    probability_id VARCHAR(20) NOT NULL,
    description TEXT NOT NULL,
    triggers TEXT, -- JSON array or delimited list
    consequences TEXT, -- JSON array or delimited list
    
    -- Metadata
    is_active BOOLEAN DEFAULT TRUE,
    version_number DECIMAL(3,1) DEFAULT 1.0,
    last_reviewed_date DATE,
    created_by VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (category_id) REFERENCES risk_categories(category_id),
    FOREIGN KEY (severity_id) REFERENCES severity_levels(severity_id),
    FOREIGN KEY (probability_id) REFERENCES probability_levels(probability_id)
);

CREATE INDEX idx_risks_category ON design_risks(category_id);
CREATE INDEX idx_risks_severity ON design_risks(severity_id);
CREATE INDEX idx_risks_active ON design_risks(is_active);

-- Risks to Phases (Many-to-Many)
CREATE TABLE risk_phases (
    risk_phase_id INT AUTO_INCREMENT PRIMARY KEY,
    risk_id VARCHAR(20) NOT NULL,
    phase_id VARCHAR(50) NOT NULL,
    is_primary_phase BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (risk_id) REFERENCES design_risks(risk_id) ON DELETE CASCADE,
    FOREIGN KEY (phase_id) REFERENCES phases(phase_id) ON DELETE CASCADE,
    UNIQUE KEY unique_risk_phase (risk_id, phase_id)
);

CREATE INDEX idx_risk_phases_risk ON risk_phases(risk_id);
CREATE INDEX idx_risk_phases_phase ON risk_phases(phase_id);

-- Risks to Impact Domains (Many-to-Many)
CREATE TABLE risk_impact_domains (
    risk_impact_id INT AUTO_INCREMENT PRIMARY KEY,
    risk_id VARCHAR(20) NOT NULL,
    domain_id VARCHAR(50) NOT NULL,
    impact_level ENUM('Primary', 'Secondary', 'Tertiary') DEFAULT 'Primary',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (risk_id) REFERENCES design_risks(risk_id) ON DELETE CASCADE,
    FOREIGN KEY (domain_id) REFERENCES impact_domains(domain_id) ON DELETE CASCADE,
    UNIQUE KEY unique_risk_domain (risk_id, domain_id)
);

CREATE INDEX idx_risk_domains_risk ON risk_impact_domains(risk_id);
CREATE INDEX idx_risk_domains_domain ON risk_impact_domains(domain_id);

-- Risk Relationships (Cascades, Dependencies)
CREATE TABLE risk_relationships (
    relationship_id INT AUTO_INCREMENT PRIMARY KEY,
    primary_risk_id VARCHAR(20) NOT NULL,
    related_risk_id VARCHAR(20) NOT NULL,
    relationship_type ENUM(
        'causes', 'blocks_resolution_of', 'compounds', 
        'creates_pressure_on', 'exacerbates', 'limits', 
        'undermines', 'interacts_with', 'depends_on', 'enables'
    ) NOT NULL,
    strength ENUM('Strong', 'Medium', 'Weak') DEFAULT 'Medium',
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (primary_risk_id) REFERENCES design_risks(risk_id) ON DELETE CASCADE,
    FOREIGN KEY (related_risk_id) REFERENCES design_risks(risk_id) ON DELETE CASCADE,
    UNIQUE KEY unique_risk_relationship (primary_risk_id, related_risk_id, relationship_type)
);

CREATE INDEX idx_relationships_primary ON risk_relationships(primary_risk_id);
CREATE INDEX idx_relationships_related ON risk_relationships(related_risk_id);
CREATE INDEX idx_relationships_type ON risk_relationships(relationship_type);

-- Risks to Standards (Many-to-Many)
CREATE TABLE risk_standards (
    risk_standard_id INT AUTO_INCREMENT PRIMARY KEY,
    risk_id VARCHAR(20) NOT NULL,
    standard_id VARCHAR(50) NOT NULL,
    relevance ENUM('Mandatory', 'Best_Practice', 'Reference') DEFAULT 'Reference',
    section_reference VARCHAR(100), -- e.g., "Section 4.2", "Appendix A"
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (risk_id) REFERENCES design_risks(risk_id) ON DELETE CASCADE,
    FOREIGN KEY (standard_id) REFERENCES standards(standard_id) ON DELETE CASCADE,
    UNIQUE KEY unique_risk_standard (risk_id, standard_id)
);

CREATE INDEX idx_risk_standards_risk ON risk_standards(risk_id);
CREATE INDEX idx_risk_standards_standard ON risk_standards(standard_id);

-- ============================================
-- MITIGATION STRATEGIES
-- ============================================

-- Mitigation Strategies (One per Risk)
CREATE TABLE mitigation_strategies (
    strategy_id INT AUTO_INCREMENT PRIMARY KEY,
    risk_id VARCHAR(20) NOT NULL,
    primary_action TEXT NOT NULL,
    approach_type ENUM(
        'Early_Assessment', 'Coordination_Workshop', 
        'Testing_Validation', 'Future_Proofing', 
        'Client_Decision', 'Design_Review', 'Other'
    ),
    estimated_cost_min DECIMAL(10,2),
    estimated_cost_max DECIMAL(10,2),
    time_investment_hours INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (risk_id) REFERENCES design_risks(risk_id) ON DELETE CASCADE,
    UNIQUE KEY unique_strategy_per_risk (risk_id)
);

-- Mitigation Checkpoints (Stage-by-Stage Actions)
CREATE TABLE mitigation_checkpoints (
    checkpoint_id INT AUTO_INCREMENT PRIMARY KEY,
    strategy_id INT NOT NULL,
    phase_id VARCHAR(50) NOT NULL,
    checkpoint_name VARCHAR(200) NOT NULL,
    deliverable TEXT NOT NULL,
    sequence_order INT,
    is_mandatory BOOLEAN DEFAULT TRUE,
    typical_cost DECIMAL(10,2),
    typical_duration_days INT,
    responsibility ENUM('Architect', 'Structural_Engineer', 'MEP_Engineer', 'QS', 'Contractor', 'Specialist', 'Client') DEFAULT 'Architect',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (strategy_id) REFERENCES mitigation_strategies(strategy_id) ON DELETE CASCADE,
    FOREIGN KEY (phase_id) REFERENCES phases(phase_id)
);

CREATE INDEX idx_checkpoints_strategy ON mitigation_checkpoints(strategy_id);
CREATE INDEX idx_checkpoints_phase ON mitigation_checkpoints(phase_id);
CREATE INDEX idx_checkpoints_sequence ON mitigation_checkpoints(strategy_id, sequence_order);

-- Mitigation Tactics (Specific Actions)
CREATE TABLE mitigation_tactics (
    tactic_id INT AUTO_INCREMENT PRIMARY KEY,
    strategy_id INT NOT NULL,
    tactic_description TEXT NOT NULL,
    tactic_type ENUM('Design', 'Specification', 'Process', 'Testing', 'Documentation') DEFAULT 'Design',
    sequence_order INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (strategy_id) REFERENCES mitigation_strategies(strategy_id) ON DELETE CASCADE
);

CREATE INDEX idx_tactics_strategy ON mitigation_tactics(strategy_id);

-- ============================================
-- PROJECT-SPECIFIC TRACKING
-- ============================================

-- Projects Table
CREATE TABLE projects (
    project_id INT AUTO_INCREMENT PRIMARY KEY,
    project_name VARCHAR(200) NOT NULL,
    project_code VARCHAR(50) UNIQUE,
    client_name VARCHAR(200),
    
    -- Location
    site_address TEXT,
    postcode VARCHAR(10),
    latitude DECIMAL(10, 7),
    longitude DECIMAL(11, 7),
    local_authority VARCHAR(100),
    
    -- Project Details
    project_type ENUM('New_Build', 'Extension', 'Renovation', 'Mixed') DEFAULT 'New_Build',
    gross_internal_area DECIMAL(10,2),
    number_of_storeys INT,
    number_of_dwellings INT DEFAULT 1,
    
    -- Budget & Timeline
    budget_total DECIMAL(12,2),
    budget_currency VARCHAR(3) DEFAULT 'GBP',
    start_date DATE,
    target_completion_date DATE,
    current_phase_id VARCHAR(50),
    
    -- Status
    status ENUM('Feasibility', 'Design', 'Planning', 'Construction', 'Handover', 'Complete', 'On_Hold') DEFAULT 'Feasibility',
    
    -- Metadata
    created_by VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (current_phase_id) REFERENCES phases(phase_id)
);

CREATE INDEX idx_projects_status ON projects(status);
CREATE INDEX idx_projects_phase ON projects(current_phase_id);
CREATE INDEX idx_projects_postcode ON projects(postcode);

-- Project Team
CREATE TABLE project_team (
    team_id INT AUTO_INCREMENT PRIMARY KEY,
    project_id INT NOT NULL,
    role ENUM('Architect', 'Structural_Engineer', 'MEP_Engineer', 'QS', 'Main_Contractor', 'PM', 'Client', 'Specialist') NOT NULL,
    company_name VARCHAR(200),
    contact_name VARCHAR(200),
    email VARCHAR(200),
    phone VARCHAR(50),
    is_lead BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (project_id) REFERENCES projects(project_id) ON DELETE CASCADE
);

CREATE INDEX idx_team_project ON project_team(project_id);

-- Project Risk Assessment (Which risks apply to this project)
CREATE TABLE project_risks (
    project_risk_id INT AUTO_INCREMENT PRIMARY KEY,
    project_id INT NOT NULL,
    risk_id VARCHAR(20) NOT NULL,
    
    -- Assessment
    assessed_probability_id VARCHAR(20), -- May differ from default
    assessed_severity_id VARCHAR(20), -- May differ from default
    risk_score DECIMAL(4,2), -- Calculated: probability x severity
    
    -- Status
    status ENUM('Identified', 'Assessed', 'Mitigating', 'Monitoring', 'Resolved', 'Accepted') DEFAULT 'Identified',
    priority ENUM('Critical', 'High', 'Medium', 'Low') DEFAULT 'Medium',
    
    -- Tracking
    identified_date DATE,
    identified_by VARCHAR(100),
    target_resolution_date DATE,
    actual_resolution_date DATE,
    notes TEXT,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (project_id) REFERENCES projects(project_id) ON DELETE CASCADE,
    FOREIGN KEY (risk_id) REFERENCES design_risks(risk_id),
    FOREIGN KEY (assessed_probability_id) REFERENCES probability_levels(probability_id),
    FOREIGN KEY (assessed_severity_id) REFERENCES severity_levels(severity_id),
    UNIQUE KEY unique_project_risk (project_id, risk_id)
);

CREATE INDEX idx_project_risks_project ON project_risks(project_id);
CREATE INDEX idx_project_risks_risk ON project_risks(risk_id);
CREATE INDEX idx_project_risks_status ON project_risks(status);
CREATE INDEX idx_project_risks_priority ON project_risks(priority);

-- Project Checkpoint Tracking
CREATE TABLE project_checkpoints (
    project_checkpoint_id INT AUTO_INCREMENT PRIMARY KEY,
    project_id INT NOT NULL,
    checkpoint_id INT NOT NULL,
    
    -- Status
    status ENUM('Not_Started', 'In_Progress', 'Complete', 'Deferred', 'Not_Applicable') DEFAULT 'Not_Started',
    completion_percentage INT DEFAULT 0,
    
    -- Tracking
    assigned_to VARCHAR(100),
    due_date DATE,
    completion_date DATE,
    actual_cost DECIMAL(10,2),
    notes TEXT,
    evidence_url VARCHAR(500), -- Link to deliverable/document
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (project_id) REFERENCES projects(project_id) ON DELETE CASCADE,
    FOREIGN KEY (checkpoint_id) REFERENCES mitigation_checkpoints(checkpoint_id),
    UNIQUE KEY unique_project_checkpoint (project_id, checkpoint_id)
);

CREATE INDEX idx_project_checkpoints_project ON project_checkpoints(project_id);
CREATE INDEX idx_project_checkpoints_status ON project_checkpoints(status);
CREATE INDEX idx_project_checkpoints_due ON project_checkpoints(due_date);

-- ============================================
-- KNOWLEDGE BASE & CONTENT
-- ============================================

-- Best Practice Guidance
CREATE TABLE guidance_articles (
    article_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    category VARCHAR(100),
    content TEXT NOT NULL,
    summary TEXT,
    
    -- Metadata
    author VARCHAR(100),
    source VARCHAR(200),
    source_url VARCHAR(500),
    publication_date DATE,
    last_reviewed_date DATE,
    
    -- Search & Tagging
    tags TEXT, -- JSON array or delimited
    keywords TEXT,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE FULLTEXT INDEX idx_guidance_content ON guidance_articles(title, content, keywords);
CREATE INDEX idx_guidance_category ON guidance_articles(category);

-- Link Guidance to Risks
CREATE TABLE risk_guidance (
    risk_guidance_id INT AUTO_INCREMENT PRIMARY KEY,
    risk_id VARCHAR(20) NOT NULL,
    article_id INT NOT NULL,
    relevance_score DECIMAL(3,2), -- 0.00 to 1.00
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (risk_id) REFERENCES design_risks(risk_id) ON DELETE CASCADE,
    FOREIGN KEY (article_id) REFERENCES guidance_articles(article_id) ON DELETE CASCADE,
    UNIQUE KEY unique_risk_guidance (risk_id, article_id)
);

-- Case Studies / Lessons Learned
CREATE TABLE case_studies (
    case_study_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    project_type VARCHAR(100),
    location VARCHAR(200),
    
    -- Content
    problem_description TEXT,
    solution_description TEXT,
    outcome_description TEXT,
    lessons_learned TEXT,
    
    -- Costs
    problem_cost DECIMAL(10,2),
    solution_cost DECIMAL(10,2),
    
    -- Media
    image_urls TEXT, -- JSON array
    document_urls TEXT, -- JSON array
    
    -- Metadata
    date_occurred DATE,
    submitted_by VARCHAR(100),
    is_verified BOOLEAN DEFAULT FALSE,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Link Case Studies to Risks
CREATE TABLE risk_case_studies (
    risk_case_study_id INT AUTO_INCREMENT PRIMARY KEY,
    risk_id VARCHAR(20) NOT NULL,
    case_study_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (risk_id) REFERENCES design_risks(risk_id) ON DELETE CASCADE,
    FOREIGN KEY (case_study_id) REFERENCES case_studies(case_study_id) ON DELETE CASCADE,
    UNIQUE KEY unique_risk_case_study (risk_id, case_study_id)
);

-- ============================================
-- SITE-SPECIFIC DATA
-- ============================================

-- Site Constraints (Auto-populated from APIs/databases)
CREATE TABLE site_constraints (
    constraint_id INT AUTO_INCREMENT PRIMARY KEY,
    project_id INT NOT NULL,
    constraint_type ENUM(
        'Flood_Zone', 'Radon_Zone', 'Conservation_Area', 
        'Article_4_Direction', 'TPO', 'Contaminated_Land',
        'Archaeology', 'Protected_Species', 'Listed_Building',
        'Green_Belt', 'AONB', 'Other'
    ) NOT NULL,
    severity ENUM('High', 'Medium', 'Low') DEFAULT 'Medium',
    description TEXT,
    source VARCHAR(200), -- e.g., "Environment Agency", "Local Authority"
    source_url VARCHAR(500),
    identified_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (project_id) REFERENCES projects(project_id) ON DELETE CASCADE
);

CREATE INDEX idx_constraints_project ON site_constraints(project_id);
CREATE INDEX idx_constraints_type ON site_constraints(constraint_type);

-- Link Site Constraints to Risks
CREATE TABLE constraint_risk_triggers (
    trigger_id INT AUTO_INCREMENT PRIMARY KEY,
    constraint_id INT NOT NULL,
    risk_id VARCHAR(20) NOT NULL,
    auto_triggered BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (constraint_id) REFERENCES site_constraints(constraint_id) ON DELETE CASCADE,
    FOREIGN KEY (risk_id) REFERENCES design_risks(risk_id) ON DELETE CASCADE
);

-- ============================================
-- MATERIALS & PRODUCTS DATABASE
-- ============================================

-- Materials Library
CREATE TABLE materials (
    material_id INT AUTO_INCREMENT PRIMARY KEY,
    material_name VARCHAR(200) NOT NULL,
    material_category ENUM(
        'Structural', 'Insulation', 'Cladding', 'Roofing', 
        'Windows_Doors', 'Internal_Finishes', 'MEP', 'Other'
    ) NOT NULL,
    
    -- Performance Data
    u_value DECIMAL(4,3),
    r_value DECIMAL(4,2),
    thermal_mass ENUM('High', 'Medium', 'Low'),
    embodied_carbon_kgco2_per_unit DECIMAL(10,2),
    cost_per_unit DECIMAL(10,2),
    unit_of_measure VARCHAR(20), -- e.g., "m²", "m³", "each"
    
    -- Lifecycle
    expected_lifespan_years INT,
    maintenance_frequency_years INT,
    recyclability ENUM('Fully_Recyclable', 'Partially_Recyclable', 'Not_Recyclable'),
    
    -- Standards
    fire_rating VARCHAR(50),
    acoustic_rating_db INT,
    
    -- Supplier
    manufacturer VARCHAR(200),
    supplier VARCHAR(200),
    product_code VARCHAR(100),
    lead_time_weeks INT,
    
    -- Metadata
    epd_url VARCHAR(500), -- Environmental Product Declaration
    datasheet_url VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE INDEX idx_materials_category ON materials(material_category);
CREATE INDEX idx_materials_manufacturer ON materials(manufacturer);

-- Material Alternatives (Substitutions)
CREATE TABLE material_alternatives (
    alternative_id INT AUTO_INCREMENT PRIMARY KEY,
    original_material_id INT NOT NULL,
    alternative_material_id INT NOT NULL,
    substitution_notes TEXT,
    cost_difference_percentage DECIMAL(5,2),
    performance_comparison TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (original_material_id) REFERENCES materials(material_id) ON DELETE CASCADE,
    FOREIGN KEY (alternative_material_id) REFERENCES materials(material_id) ON DELETE CASCADE
);

-- Project Material Selections
CREATE TABLE project_materials (
    project_material_id INT AUTO_INCREMENT PRIMARY KEY,
    project_id INT NOT NULL,
    material_id INT NOT NULL,
    application VARCHAR(200), -- e.g., "External wall insulation", "Main roof covering"
    quantity DECIMAL(10,2),
    unit_of_measure VARCHAR(20),
    specified_date DATE,
    ordered_date DATE,
    delivery_date DATE,
    actual_cost DECIMAL(10,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (project_id) REFERENCES projects(project_id) ON DELETE CASCADE,
    FOREIGN KEY (material_id) REFERENCES materials(material_id)
);

CREATE INDEX idx_project_materials_project ON project_materials(project_id);

-- ============================================
-- CHANGE MANAGEMENT
-- ============================================

-- Design Changes / Architect's Instructions
CREATE TABLE design_changes (
    change_id INT AUTO_INCREMENT PRIMARY KEY,
    project_id INT NOT NULL,
    change_number VARCHAR(50) NOT NULL, -- e.g., "AI-001"
    change_type ENUM('Design_Change', 'Variation', 'Clarification', 'Substitution') DEFAULT 'Design_Change',
    
    -- Description
    title VARCHAR(200) NOT NULL,
    description TEXT NOT NULL,
    reason TEXT,
    
    -- Impact
    cost_impact DECIMAL(10,2),
    time_impact_days INT,
    affected_risks TEXT, -- JSON array of risk_ids
    
    -- Approval
    status ENUM('Draft', 'Issued', 'Approved', 'Rejected', 'Implemented') DEFAULT 'Draft',
    issued_by VARCHAR(100),
    issued_date DATE,
    approved_by VARCHAR(100),
    approval_date DATE,
    
    -- Documentation
    drawing_references TEXT, -- JSON array
    document_urls TEXT, -- JSON array
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (project_id) REFERENCES projects(project_id) ON DELETE CASCADE
);

CREATE INDEX idx_changes_project ON design_changes(project_id);
CREATE INDEX idx_changes_status ON design_changes(status);
CREATE INDEX idx_changes_number ON design_changes(project_id, change_number);

-- ============================================
-- DOCUMENT MANAGEMENT
-- ============================================

-- Project Documents
CREATE TABLE project_documents (
    document_id INT AUTO_INCREMENT PRIMARY KEY,
    project_id INT NOT NULL,
    document_type ENUM(
        'Drawing', 'Specification', 'Schedule', 'Report', 
        'Certificate', 'Contract', 'Invoice', 'Correspondence', 'Other'
    ) NOT NULL,
    
    -- Document Details
    document_name VARCHAR(200) NOT NULL,
    document_number VARCHAR(100), -- e.g., "A-100", "SK-01"
    revision VARCHAR(10),
    phase_id VARCHAR(50),
    
    -- File
    file_url VARCHAR(500) NOT NULL,
    file_size_kb INT,
    file_type VARCHAR(10), -- e.g., "PDF", "DWG", "DOCX"
    
    -- Status
    status ENUM('Draft', 'For_Review', 'For_Approval', 'Approved', 'Issued', 'Superseded', 'Archived') DEFAULT 'Draft',
    is_current BOOLEAN DEFAULT TRUE,
    
    -- Metadata
    uploaded_by VARCHAR(100),
    upload_date DATETIME,
    approved_by VARCHAR(100),
    approval_date DATE,
    supersedes_document_id INT,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (project_id) REFERENCES projects(project_id) ON DELETE CASCADE,
    FOREIGN KEY (phase_id) REFERENCES phases(phase_id),
    FOREIGN KEY (supersedes_document_id) REFERENCES project_documents(document_id) ON DELETE SET NULL
);

CREATE INDEX idx_documents_project ON project_documents(project_id);
CREATE INDEX idx_documents_type ON project_documents(document_type);
CREATE INDEX idx_documents_status ON project_documents(status);
CREATE INDEX idx_documents_current ON project_documents(is_current);

-- ============================================
-- AUDIT & ACTIVITY LOG
-- ============================================

-- Activity Log (Audit Trail)
CREATE TABLE activity_log (
    log_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    project_id INT,
    user_id VARCHAR(100) NOT NULL,
    action_type ENUM(
        'Created', 'Updated', 'Deleted', 'Viewed', 
        'Approved', 'Rejected', 'Uploaded', 'Downloaded', 'Exported'
    ) NOT NULL,
    entity_type VARCHAR(50) NOT NULL, -- e.g., "project_risks", "design_changes"
    entity_id INT,
    description TEXT,
    ip_address VARCHAR(45),
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (project_id) REFERENCES projects(project_id) ON DELETE CASCADE
);

CREATE INDEX idx_log_project ON activity_log(project_id);
CREATE INDEX idx_log_user ON activity_log(user_id);
CREATE INDEX idx_log_entity ON activity_log(entity_type, entity_id);
CREATE INDEX idx_log_created ON activity_log(created_at);

-- ============================================
-- VIEWS FOR COMMON QUERIES
-- ============================================

-- View: Risk Overview with Counts
CREATE VIEW v_risk_overview AS
SELECT 
    dr.risk_id,
    dr.title,
    dr.category_id,
    rc.category_name,
    dr.severity_id,
    sl.level_name AS severity_name,
    sl.level_number AS severity_level,
    dr.probability_id,
    pl.level_name AS probability_name,
    pl.level_number AS probability_level,
    (sl.level_number * pl.level_number) AS risk_score,
    COUNT(DISTINCT rp.phase_id) AS phase_count,
    COUNT(DISTINCT rid.domain_id) AS domain_count,
    COUNT(DISTINCT rr.related_risk_id) AS related_risk_count,
    COUNT(DISTINCT rs.standard_id) AS standard_count,
    dr.is_active
FROM design_risks dr
LEFT JOIN risk_categories rc ON dr.category_id = rc.category_id
LEFT JOIN severity_levels sl ON dr.severity_id = sl.severity_id
LEFT JOIN probability_levels pl ON dr.probability_id = pl.probability_id
LEFT JOIN risk_phases rp ON dr.risk_id = rp.risk_id
LEFT JOIN risk_impact_domains rid ON dr.risk_id = rid.risk_id
LEFT JOIN risk_relationships rr ON dr.risk_id = rr.primary_risk_id
LEFT JOIN risk_standards rs ON dr.risk_id = rs.risk_id
WHERE dr.is_active = TRUE
GROUP BY dr.risk_id, dr.title, dr.category_id, rc.category_name, 
         dr.severity_id, sl.level_name, sl.level_number,
         dr.probability_id, pl.level_name, pl.level_number, dr.is_active;

-- View: Project Risk Dashboard
CREATE VIEW v_project_risk_dashboard AS
SELECT 
    p.project_id,
    p.project_name,
    p.current_phase_id,
    ph.phase_name,
    pr.risk_id,
    dr.title AS risk_title,
    pr.status AS risk_status,
    pr.priority,
    pr.risk_score,
    sl.level_name AS severity_name,
    pl.level_name AS probability_name,
    COUNT(pc.project_checkpoint_id) AS total_checkpoints,
    SUM(CASE WHEN pc.status = 'Complete' THEN 1 ELSE 0 END) AS completed_checkpoints,
    ROUND(
        (SUM(CASE WHEN pc.status = 'Complete' THEN 1 ELSE 0 END) / 
         COUNT(pc.project_checkpoint_id)) * 100, 2
    ) AS completion_percentage
FROM projects p
LEFT JOIN phases ph ON p.
```