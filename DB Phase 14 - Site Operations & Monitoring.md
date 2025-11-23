
```sql
-- ============================================================================
-- SITE DIARY / DAILY LOG
-- ============================================================================

CREATE TABLE site_diary (
    diary_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_id UUID NOT NULL REFERENCES projects(project_id) ON DELETE CASCADE,
    
    -- Date
    log_date DATE NOT NULL DEFAULT CURRENT_DATE,
    
    -- Weather
    weather_conditions TEXT,  -- dry, light_rain, heavy_rain, snow, frost, wind
    temperature_celsius INTEGER,
    weather_impact TEXT,  -- none, slowed, stopped, damage_risk
    
    -- Ground Conditions
    ground_conditions TEXT,  -- dry, damp, wet, waterlogged, frozen
    
    -- Labour On Site
    workers_on_site JSONB DEFAULT '[]'::jsonb,  -- Array of {name, trade, company, hours}
    total_workers INTEGER,
    
    -- Activities
    activities_completed TEXT[],
    activities_in_progress TEXT[],
    activities_planned_next TEXT[],
    
    -- Materials
    materials_delivered JSONB DEFAULT '[]'::jsonb,  -- Array of {material, quantity, supplier}
    materials_used JSONB DEFAULT '[]'::jsonb,
    
    -- Plant & Equipment
    plant_on_site TEXT[],
    
    -- Inspections
    inspections_today UUID[],  -- Links to inspections table
    
    -- Issues
    issues_encountered TEXT[],
    delays TEXT[],
    safety_incidents TEXT[],
    
    -- Visitors
    visitors JSONB DEFAULT '[]'::jsonb,  -- Array of {name, company, purpose, time}
    
    -- Progress
    progress_notes TEXT,
    
    -- Photos
    photo_ids UUID[],
    
    -- Next Day Plan
    next_day_plan TEXT,
    
    -- Notes
    notes TEXT,
    
    -- Logged By
    logged_by TEXT,
    logged_by_user_id UUID REFERENCES users(user_id),
    
    -- Audit
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    
    UNIQUE(project_id, log_date)
);

CREATE INDEX idx_site_diary_project ON site_diary(project_id);
CREATE INDEX idx_site_diary_date ON site_diary(log_date);
CREATE INDEX idx_site_diary_weather ON site_diary(weather_conditions);

CREATE TRIGGER update_site_diary_updated_at 
    BEFORE UPDATE ON site_diary 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();


-- ============================================================================
-- WEATHER LOG (Detailed Time Series)
-- ============================================================================

CREATE TABLE weather_log (
    weather_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_id UUID NOT NULL REFERENCES projects(project_id) ON DELETE CASCADE,
    
    -- Timestamp
    log_date DATE NOT NULL,
    log_time TIME,
    
    -- Temperature
    temperature_celsius DECIMAL(4,1),
    feels_like_celsius DECIMAL(4,1),
    
    -- Conditions
    conditions TEXT,  -- clear, cloudy, rain, heavy_rain, snow, fog, ice
    precipitation_mm DECIMAL(5,1),
    wind_speed_mph INTEGER,
    wind_direction TEXT,  -- N, NE, E, SE, S, SW, W, NW
    
    -- Ground
    ground_frozen BOOLEAN DEFAULT FALSE,
    ground_waterlogged BOOLEAN DEFAULT FALSE,
    
    -- Work Impact
    work_stopped BOOLEAN DEFAULT FALSE,
    activities_affected TEXT[],
    
    -- Notes
    notes TEXT,
    
    -- Audit
    created_at TIMESTAMPTZ DEFAULT NOW(),
    
    UNIQUE(project_id, log_date, log_time)
);

CREATE INDEX idx_weather_project ON weather_log(project_id);
CREATE INDEX idx_weather_date ON weather_log(log_date);
CREATE INDEX idx_weather_conditions ON weather_log(conditions);
CREATE INDEX idx_weather_impact ON weather_log(work_stopped);

-- For time-series analysis, consider adding TimescaleDB extension:
-- SELECT create_hypertable('weather_log', 'log_date');
```