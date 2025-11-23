
```YAML
# Aven Memory Store - Expanded Schema
# Last updated: 2025-10-23 00:00:00
# Version: 2.0

# ============================================================================

# USER PROFILE

# ============================================================================

user_profile:

  experience_level: "unknown"  # first-time, some_experience, experienced, professional

  project_stage: "unknown"      # pre-planning, planning, design, pre-construction, construction, completion

  learning_style: "unknown"     # detail-oriented, big-picture, visual, step-by-step

  communication_preference:     # How they prefer information

    detail_level: "medium"      # brief, medium, detailed

    technical_language: false   # Use jargon or explain everything?

    wants_examples: true

  confidence_level: "unknown"   # anxious, cautious, confident, very_confident

# ============================================================================

# PROJECT CONTEXT

# ============================================================================

project_context:

  # Location and Planning Authority

  location:

    country: null               # england, scotland, wales, northern_ireland

    region: null                # south_west, london, yorkshire, etc.

    local_authority: null       # Specific council name

    postcode_area: null         # First part only (e.g., BS for Bristol)

    rural_or_urban: null        # rural, suburban, urban, city_centre

  # Site Characteristics

  site:

    type: null                  # greenfield, brownfield, garden, infill, agricultural, conversion

    size_sqm: null

    size_acres: null

    dimensions: null            # e.g., "20m x 15m"

    shape: null                 # regular, irregular, awkward, ideal

    # Boundaries

    boundaries:

      north: null               # e.g., "neighbouring property", "road", "field"

      south: null

      east: null

      west: null

      boundary_treatments: []   # fence, hedge, wall, shared, none

    # Physical Characteristics

    topography: null            # flat, gentle_slope, moderate_slope, steep, terraced

    slope_direction: null       # n, ne, e, se, s, sw, w, nw

    orientation: null           # Which way does the site face?

    soil_type: null             # clay, sand, chalk, rock, peat

    ground_conditions: null     # stable, problematic, requires_investigation

    drainage: null              # good, poor, waterlogged, unknown

    # Access

    access:

      quality: null             # good, adequate, limited, challenging, none

      type: null                # road, track, shared, right_of_way

      vehicle_access: false

      construction_access: null # separate, same, requires_improvement

      parking_available: false

    # Existing Features

    existing_structures:

      - type: null              # dwelling, outbuilding, barn, wall, hardstanding

        condition: null         # good, fair, poor, derelict

        to_demolish: false

        listed: false

    existing_trees:

      - location: null

        species: null

        size: null

        tpo: false              # Tree Preservation Order

        impact: null            # none, minor, major

    utilities:

      water_main: null          # connected, nearby, distant, none

      sewerage: null            # mains, septic, treatment_plant, none

      electricity: null         # connected, nearby, distant, none

      gas: null                 # connected, nearby, not_available

      broadband: null           # fibre, standard, poor, none

  # Planning Constraints

  constraints:

    statutory:

      conservation_area: false

      listed_building: false

      listed_grade: null        # I, II*, II

      green_belt: false

      aonb: false               # Area of Outstanding Natural Beauty

      national_park: false

      world_heritage_site: false

      sssi: false               # Site of Special Scientific Interest

      flood_zone: null          # 1, 2, 3a, 3b

      coastal_zone: false

      article_4_direction: false

    environmental:

      tree_preservation_orders: []

      protected_species: []     # bats, newts, badgers, birds, etc.

      ecological_survey_required: false

      contaminated_land: false

      archaeological_interest: false

      noise_constraints: []     # airport, railway, road, industrial

      air_quality_concerns: false

    infrastructure:

      highways_constraints: []  # visibility, access, parking requirements

      drainage_restrictions: []

      utility_constraints: []

    neighbouring:

      overlooking_issues: false

      privacy_concerns: false

      party_wall_matters: []

      shared_access: false

      boundary_disputes: false

      neighbour_objections: []  # documented concerns

  # Build Specifications

  build:

    project_type: null          # new_build, extension, conversion, renovation, demolition_rebuild

    project_scale: null         # small, medium, large, very_large

    # For new builds

    build_method: null          # traditional_masonry, timber_frame, sips, icf, modular, hybrid

    foundation_type: null       # strip, trench_fill, raft, piled, unknown

    # Size

    stories: null               # 1, 1.5, 2, 2.5, 3, split_level

    approx_floor_area_sqm: null

    approx_floor_area_sqft: null

    # For extensions/conversions

    existing_building:

      type: null

      age: null                 # pre_1900, 1900-1945, 1945-1980, post_1980

      construction: null        # solid_wall, cavity_wall, timber_frame, etc.

      condition: null           # excellent, good, fair, poor

# ============================================================================

# DESIGN INTENT

# ============================================================================

design_intent:

  # Aesthetic Preferences

  style:

    primary: null               # modern, contemporary, traditional, vernacular, eco, industrial

    secondary: []               # Can have multiple influences

    reference_images: []        # Paths to images in vault or URLs

    pinterest_boards: []

    architect_influences: []    # Names of architects they admire

  # Spatial Requirements

  accommodation:

    bedrooms: null

    bathrooms: null

    ensuites: null

    reception_rooms: null

    kitchen_type: null          # open_plan, separate, kitchen_diner

    utility_room: false

    study_office: false

    workshop: false

    gym: false

    cinema_room: false

    guest_suite: false

    annexe: false

    garage: null                # none, single, double, triple, carport

    storage: []                 # types of storage needed

    special_requirements:

      accessibility: false      # Part M compliant or beyond

      wheelchair_access: false

      level_access: false

      elderly_relatives: false

      young_children: false

      pets: []                  # impacts design (dog shower, cattery, etc.)

  # Priorities (ranked)

  priorities:

    - priority: null            # e.g., "natural_light"

      importance: null          # critical, high, medium, low

      notes: null

  must_haves: []                # Non-negotiable requirements

  nice_to_haves: []             # Aspirational features

  definitely_not: []            # Things to avoid

  # Performance Targets

  performance:

    energy_standard: null       # building_regs, better_than_regs, passivhaus, net_zero

    airtightness_target: null   # e.g., "3 m³/h/m² @ 50Pa"

    u_values:

      walls: null

      roof: null

      floor: null

      windows: null

    heating_system: null        # ashp, gshp, biomass, solar_thermal, gas, oil, electric

    renewable_energy: []        # pv, solar_thermal, wind, none

    water_efficiency: null      # standard, enhanced, rainwater_harvesting, greywater

    sustainability_goals:

      - goal: null

        target: null

        importance: null        # critical, high, medium, low

  # Spatial Character

  spatial_preferences:

    ceiling_heights: null       # standard, high, very_high, varied

    openness: null              # open_plan, semi_open, cellular

    light_quality: null         # bright, balanced, cosy, dramatic

    connection_to_outside: null # strong, moderate, minimal

    views_priority: []          # which views to prioritise

    privacy_level: null         # private, balanced, open

# ============================================================================

# PROJECT MANAGEMENT

# ============================================================================

project_management:

  # Timeline

  timeline:

    project_start: null

    planning_submission_target: null

    planning_decision_received: null

    construction_start_target: null

    construction_completion_target: null

    move_in_target: null

    milestones:

      - name: null

        target_date: null

        actual_date: null

        status: null            # pending, in_progress, completed, delayed

        notes: null

  # Budget

  budget:

    total_budget: null

    land_cost: null

    build_cost_budget: null

    professional_fees_budget: null

    contingency_percentage: null

    funding_secured: false

    funding_type: null          # savings, mortgage, self_build_mortgage, loan, mixed

    breakdown:

      - category: null          # e.g., "groundworks", "structure", "finishes"

        estimated: null

        actual: null

        variance: null

    cost_tracking:

      spent_to_date: null

      committed: null

      remaining: null

      forecast_final_cost: null

  # Procurement Route

  procurement:

    route: null                 # architect_led, main_contractor, design_and_build, self_manage

    contracts: []               # List of contracts in place

    insurances: []              # Required insurances

  # Professional Team

  professional_team:

    architect:

      hired: false

      name: null

      practice: null

      riba_stages: []           # Which stages are they doing?

      contact: null

      fee: null

    structural_engineer:

      hired: false

      name: null

      company: null

      contact: null

      fee: null

    planning_consultant:

      hired: false

      name: null

      company: null

      contact: null

      fee: null

    quantity_surveyor:

      hired: false

      name: null

      company: null

      contact: null

      fee: null

    building_control:

      provider: null            # local_authority, approved_inspector

      name: null

      contact: null

    party_wall_surveyor:

      required: false

      hired: false

      name: null

    ecological_consultant:

      required: false

      hired: false

      name: null

    principal_designer:        # CDM Regulations

      required: false

      hired: false

      name: null

    other_consultants: []      # acoustics, energy, landscape, etc.

  

# ============================================================================

# DECISIONS LOG

# ============================================================================

decisions_made:

  - date: null

    topic: null

    decision: null

    reasoning: null

    alternatives_considered: []

    confidence: null            # low, medium, high

    reversible: null            # true, false

    dependencies: []            # what else depends on this?

    cost_impact: null

    programme_impact: null

  

# ============================================================================

# RISKS AND CONCERNS

# ============================================================================

risks:

  - id: null

    category: null              # planning, structural, budget, programme, regulatory

    description: null

    severity: null              # low, medium, high, critical

    likelihood: null            # low, medium, high

    impact: null                # low, medium, high, critical

    mitigation: null

    owner: null                 # who's responsible?

    status: null                # identified, monitoring, mitigating, resolved

    identified_date: null

    review_date: null

  

concerns:

  - topic: null

    severity: null              # low, medium, high

    notes: null

    raised_date: null

    status: null                # open, investigating, resolved

    resolution: null

  

# ============================================================================

# CONVERSATION TRACKING

# ============================================================================

conversations:

  total_sessions: 0

  first_conversation: null

  last_conversation: null

  topics_discussed:

    - topic: null

      frequency: null

      last_discussed: null

      depth: null               # surface, moderate, detailed

  common_questions: []

  knowledge_gaps_identified: []  # Areas where user needs more info

  user_preferences:

    prefers_options_vs_recommendations: null  # present choices or give direct advice?

    wants_proactive_suggestions: null         # or waits for questions?

    risk_tolerance: null                       # risk-averse, balanced, adventurous

  

# ============================================================================

# OBSIDIAN VAULT INTEGRATION

# ============================================================================

vault_context:

  obsidian_vault_path: null

  vault_last_scanned: null

  vault_note_count: null

  # Key project notes identified

  key_notes:

    - path: null

      title: null

      type: null                # project_brief, site_analysis, budget, schedule, etc.

      last_modified: null

      relevance: null           # high, medium, low

  # Obsidian templates being used

  templates_used: []

  # Vault organization

  vault_structure:

    has_project_folder: false

    has_daily_notes: false

    has_meeting_notes: false

    has_decision_log: false

    organization_style: null    # structured, organic, minimal

  # Data extracted from vault

  extracted_context:

    location_mentions: []

    budget_mentions: []

    deadline_mentions: []

    concern_mentions: []

    decision_mentions: []

  # Vault health

  documentation_gaps: []        # Suggested notes/docs user should create

  last_backup_reminder: null

  

# ============================================================================

# PLANNING APPLICATION TRACKING

# ============================================================================

planning:

  pre_application:

    pre_app_meeting_held: false

    pre_app_date: null

    pre_app_feedback: null

    pre_app_concerns: []

    pre_app_recommendations: []

  application:

    application_type: null      # full, outline, reserved_matters, listed_building

    reference_number: null

    submission_date: null

    validation_date: null

    target_decision_date: null

    actual_decision_date: null

    status: null                # not_submitted, submitted, validated, under_review, 

                                # approved, refused, withdrawn, appealed

    case_officer:

      name: null

      contact: null

      last_contact: null

    consultations:

      - consultee: null         # highways, conservation, environmental_health, etc.

        response_due: null

        response_received: null

        comments: null

        objection: false

    neighbour_consultation:

      letters_sent: null

      responses_received: null

      objections: []

      support: []

    conditions:

      - condition_number: null

        description: null

        category: null          # pre_commencement, pre_occupation, ongoing

        status: null            # pending, submitted, discharged

        discharge_date: null

  appeals:

    appeal_lodged: false

    appeal_reference: null

    appeal_type: null           # written_reps, hearing, inquiry

    appeal_date: null

    appeal_decision: null

    appeal_notes: null

  

# ============================================================================

# BUILDING REGULATIONS

# ============================================================================

building_regulations:

  application:

    route: null                 # full_plans, building_notice, regularisation

    reference_number: null

    submission_date: null

    approval_date: null

    status: null                # not_submitted, submitted, approved, conditional

  inspections:

    - stage: null               # foundations, dpc, drains, structure, completion

      scheduled_date: null

      completed_date: null

      passed: null

      notes: null

      remedial_work_required: []

  compliance_strategy:

    - regulation: null          # Part A, Part L, Part M, etc.

      approach: null

      specialist_required: null

      status: null              # compliant, needs_work, unknown

  

# ============================================================================

# DESIGN DEVELOPMENT

# ============================================================================

design_development:

  riba_stage: null              # 0, 1, 2, 3, 4, 5, 6, 7

  iterations:

    - version: null

      date: null

      description: null

      changes_from_previous: []

      reason_for_change: null

      drawings: []              # Paths to drawings in vault

  key_design_elements:

    - element: null             # e.g., "entrance", "living space", "roof form"

      description: null

      status: null              # concept, developed, finalised

      constraints: []

      opportunities: []

  materials_palette:

    - element: null             # walls, roof, windows, doors, etc.

      material: null

      specification: null

      supplier: null

      cost_estimate: null

      sustainability_rating: null

      status: null              # considering, specified, procured

  

# ============================================================================

# LEARNING JOURNEY

# ============================================================================

learning_journey:

  topics_mastered: []           # Things user now understands well

  current_learning_focus: []    # What they're trying to understand now

  concepts_explained:

    - concept: null             # e.g., "permitted development", "u-values"

      first_explained: null

      times_referenced: null

      understood: null          # true, false, partially

  resources_recommended: []     # External resources shared with user

  confidence_progression:

    - date: null

      topic: null

      confidence_level: null

      notes: null

  

# ============================================================================

# PROGRESS TRACKING

# ============================================================================

project_progress:

  overall_percentage: null

  phase_completion:

    land_acquisition: null      # percentage complete

    planning: null

    design: null

    pre_construction: null

    construction: null

    completion: null

  current_focus: null           # What's happening right now

  next_major_milestone: null

  blockers: []                  # Current obstacles

  recent_wins: []               # Achievements to celebrate

  

# ============================================================================

# AVEN INTERACTION PATTERNS

# ============================================================================

aven_notes:

  # Internal notes for Aven to track patterns

  user_engagement_style: null   # how user interacts with Aven

  effective_strategies: []      # What communication approaches work well

  topics_requiring_sensitivity: [] # Areas where user is anxious/stressed

  recurring_concerns: []        # Issues that keep coming up

  user_strengths: []            # What user is good at / confident with

  areas_needing_support: []     # Where user needs most help

  personality_notes: null       # Observations about working style, preferences

  custom_templates: []          # Any custom response patterns for this user

  

# ============================================================================

# COLLABORATION & SHARING

# ============================================================================

collaboration:

  shared_with: []               # Family members, partners involved

  stakeholders:

    - name: null

      role: null                # partner, parent, investor, etc.

      involvement_level: null   # decision_maker, consultant, informed

      priorities: []

      concerns: []

  communication_log:

    - date: null

      stakeholder: null

      topic: null

      outcome: null

  

# ============================================================================

# METADATA

# ============================================================================

metadata:

  schema_version: "2.0"

  created_date: null

  last_updated: null

  last_backup: null

  # Data quality

  completeness_score: null      # How much of the schema is populated

  confidence_score: null        # How confident are we in the data

  # Privacy

  data_retention_consent: true

  anonymisation_required: false

  # System

  aven_version: null

  last_rag_sync: null           # Last time vault was scanned

  memory_optimization_due: null # Periodic cleanup date

  

# ============================================================================

# NOTES

# ============================================================================

notes: |

  General observations, context, and freeform notes about this user's project.

  Use this space for:

  - Project narrative and backstory

  - Unique circumstances or context

  - Relationship dynamics affecting decisions

  - Emotional journey observations

  - Anything that doesn't fit structured fields above

  - Resources: https://www.gov.uk/housing-local-and-community/building-regulation

```


