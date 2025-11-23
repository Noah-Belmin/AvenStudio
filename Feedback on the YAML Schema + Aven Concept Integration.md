

The YAML schema shows you've done deep domain research—it captures the **reality** of self-build project data in a way that most project management tools completely miss. Let me give you structured feedback on how this fits into the Aven concept, and where to refine it.

---

## What This YAML Gets Right

### 1. **Captures the "Whole Project Context"**

You're not just tracking tasks—you're modelling the **complete project state**:

- Physical constraints (soil, topography, trees)
- Legal constraints (TPOs, conservation areas, party walls)
- Stakeholder dynamics (neighbour objections, shared access)
- Emotional state (confidence levels, learning journey)

This is **exactly** what self-builders need but can never articulate when starting out.

### 2. **Balances Structure with Flexibility**

The mix of:

- **Controlled vocabularies** (`experience_level: first-time | some_experience | experienced`)
- **Free-text fields** (`notes`, `reasoning`)
- **Nested structures** (site → access → quality, type, construction_access)

...creates a system that can be both **queryable** (for smart prompts) and **human** (for nuanced capture).

### 3. **Anticipates Real-World Complexity**

Things like:

- `existing_trees` with TPO flags
- `neighbour_consultation` tracking objections vs support
- `building_regulations.inspections` with remedial work tracking
- `procurement.route` acknowledging different management approaches

These show you understand self-build as a **negotiated, iterative process**, not a linear checklist.

### 4. **The Learning Journey Section is Gold**

```yaml
learning_journey:
  topics_mastered: []
  concepts_explained:
    - concept: "u-values"
      understood: partially
  confidence_progression:
    - date: 2025-03-15
      topic: "heating_systems"
      confidence_level: medium
```

This turns Aven into a **reflective learning companion**, not just a project tracker. Brilliant.

---

## Critical Issues to Address

### **A. Onboarding Cognitive Load**

**Problem**: This schema contains **~200+ fields**. If onboarding tries to capture even 30% of this upfront, users will **abandon immediately**.

**Solution**: **Progressive disclosure with smart defaults**

#### Onboarding Should Be a Conversation, Not a Form

Break it into **emotional phases**:

1. **Phase 1: "Tell me about your dream"** (2 minutes)
    
    - `project_type`, `accommodation.bedrooms`, `style.primary`, `must_haves`
    - **Goal**: Get them excited, not interrogated
2. **Phase 2: "Where is this happening?"** (3 minutes)
    
    - `location.region`, `site.type`, `site.size_sqm`, `rural_or_urban`
    - **Goal**: Establish basic feasibility context
3. **Phase 3: "Who's involved and what's your timeline?"** (2 minutes)
    
    - `project_stage`, `timeline.planning_submission_target`, `budget.total_budget`
     `professional_team.architect.hired`, `procurement.route`
      
    - **Goal**: Understand resources and urgency
4. **Phase 4: "What do you need help with?"** (2 minutes)
    
    - `experience_level`, `confidence_level`, `learning_style`
    - `user_preferences.wants_proactive_suggestions`
    - **Goal**: Calibrate Aven's guidance style

**Total onboarding time: 10-12 minutes max**

Everything else should be:

- **Auto-discovered** (from uploaded documents, vault scanning)
- **Prompted contextually** ("You're in a conservation area—let's capture some details about that")
- **Deferred** until relevant ("You'll need drainage info before groundworks—let's tackle that when you're ready")

---

### **B. Data Capture Should Be Invisible**

Most users won't "fill in" a schema—they'll **talk to Aven**. The YAML should be a **backend memory store**, not a user-facing form.

#### Example: Capturing `site.soil_type`

**Bad UX** (form-based):

```
Site Details
Soil Type: [dropdown: clay, sand, chalk, rock, peat, unknown]
```

**Good UX** (conversational):

```
Aven: "Have you had a soil investigation done yet?"
User: "No, but the neighbours say it's heavy clay."
Aven: [stores soil_type: clay, confidence: low, source: anecdotal]
      "Clay can affect drainage and foundation design—I'll remind you 
      to get a geotechnical survey before finalizing foundations."
```

**The YAML gets populated through**:

- Natural language capture
- Document parsing (planning applications, surveys)
- Contextual prompts ("You mentioned trees—any TPOs?")
- Background inference (postcode → likely constraints)

---

### **C. Field Granularity vs Usability**

Some sections are **over-specified** for a self-builder's needs:

#### Example: `site.boundaries`

```yaml
boundaries:
  north: "neighbouring property"
  south: "road"
  east: "field"
  west: "shared fence"
  boundary_treatments: [fence, hedge, wall]
```

**Question**: Will a self-builder **ever** need to filter projects by "western boundary type"?

**Suggestion**: Simplify to what **drives decisions**:

```yaml
site:
  boundaries:
    - direction: north
      type: neighbouring_property
      issues: [overlooking, party_wall, privacy_concerns]
      notes: "3-storey house, need to manage overlooking"
```

Only capture **actionable detail**—things that affect design, planning, or cost.

---

### **D. Missing: The "Why" Behind Data**

The schema captures **what** but not always **why it matters**. Aven should help users understand the **purpose** of each data point.

#### Add a `relevance` layer:

```yaml
site:
  soil_type: clay
  soil_type_relevance:
    - affects: foundations
      consideration: "Clay expansion can cause movement—may need deeper foundations"
    - affects: drainage
      consideration: "Poor drainage—surface water management critical"
    - triggers: [geotechnical_survey, building_regs_part_c]
```

This turns data collection into **decision support**.

---

## Recommended Schema Refinements

### **1. Simplify Site Section**

**Current** (too granular):

```yaml
site:
  boundaries:
    north: null
    south: null
    east: null
    west: null
```

**Better** (issue-focused):

```yaml
site:
  boundary_issues: []  # List only if problematic
    - direction: north
      issue_type: overlooking
      description: "3-storey neighbour, first floor windows face our garden"
      mitigation: "Consider screening, window placement"
```

**Principle**: Only capture boundaries if they **constrain design**.

---

### **2. Collapse Constraints into a Unified Model**

**Current** (scattered):

```yaml
constraints:
  statutory:
    conservation_area: false
    green_belt: false
    flood_zone: null
  environmental:
    tree_preservation_orders: []
  neighbouring:
    overlooking_issues: false
```

**Better** (unified risk/constraint register):

```yaml
constraints:
  - id: C001
    type: statutory
    category: conservation_area
    applies: true
    severity: high
    impact: "All materials and design must respect local character"
    action_required: "Submit Heritage Statement with planning"
    status: identified
    
  - id: C002
    type: environmental
    category: tree_preservation_order
    applies: true
    details: "Oak tree on eastern boundary, TPO ref: TPO/2023/456"
    impact: "Root protection zone restricts foundation placement"
    action_required: "Arboricultural Impact Assessment needed"
    status: survey_commissioned
```

**Why better**:

- Each constraint becomes a **trackable item**
- Can show as cards in UI ("3 active constraints")
- Links to decisions, budget, schedule
- Status tracking (identified → mitigated → resolved)

---

### **3. Strengthen Decision Logging**

**Current**:

```yaml
decisions_made:
  - date: null
    topic: null
    decision: null
    reasoning: null
```

**Better** (adds traceability):

```yaml
decisions:
  - id: D001
    date: 2025-03-20
    category: design
    topic: "Bathroom floor finish"
    decision: "Porcelain tiles, 600x600mm, slip-resistant"
    reasoning: "Durable, low-maintenance, Part M compliant"
    
    alternatives_considered:
      - option: "LVT"
        rejected_because: "Concerned about water damage"
      - option: "Natural stone"
        rejected_because: "Over budget"
    
    confidence: high
    reversible: true
    dependencies:
      - decision_id: D042  # (heating system - affects floor buildup)
      - room_id: R003      # (Bathroom 1)
    
    impacts:
      budget: +450
      schedule: null
      building_regs: [Part_M]
    
    linked_to:
      supplier_id: S012
      room_id: R003
      stage_id: ST07  # Second Fix
      cost_item_id: C089
    
    status: confirmed
    
    review_dates:
      - 2025-06-01: "Confirm delivery lead time"
```

**Why better**:

- **Every decision becomes an object** that links across the system
- Can generate views like:
    - "Show all decisions affecting budget"
    - "Which decisions depend on the architect's approval?"
    - "What decisions are reversible if we overspend?"
- Supports the **ripple effect** you described in the concept doc

---

### **4. Add "Project Health" Dashboard Data**

Missing from schema: **aggregate metrics** that power the dashboard.

Add a computed section:

```yaml
project_health:  # Auto-calculated, not user-entered
  overall_score: 67  # 0-100
  
  dimensions:
    planning_risk: medium      # Based on constraints, objections
    budget_health: good         # Spend vs forecast
    schedule_confidence: low    # Dependencies, blockers
    design_maturity: high       # % decisions finalized
    team_readiness: medium      # Key professionals hired?
    knowledge_confidence: 45    # User's understanding level
  
  alerts:
    - severity: high
      message: "Planning decision overdue by 3 weeks"
      action: "Contact case officer"
    
    - severity: medium
      message: "Budget contingency depleted to 3%"
      action: "Review finishes specification"
  
  next_critical_actions:
    - "Book Building Control foundation inspection"
    - "Finalize window supplier (affects lead time)"
    - "Submit Part M compliance details"
```

This powers the "Your project at a glance" dashboard.

---

### **5. Make Learning Journey More Actionable**

**Current**:

```yaml
learning_journey:
  topics_mastered: []
  current_learning_focus: []
```

**Better** (with learning paths):

```yaml
learning_journey:
  knowledge_gaps:
    - topic: "heating_systems"
      severity: high  # Blocks design decisions
      confidence: low
      identified_date: 2025-03-10
      
      learning_resources_suggested:
        - type: article
          title: "ASHP vs GSHP: A Self-Builder's Guide"
          url: "..."
          status: read
        - type: video
          title: "Heat pump sizing basics"
          status: not_started
      
      milestones:
        - 2025-03-15: "Understood CoP concept"
        - 2025-03-20: "Compared 3 systems"
        - 2025-03-25: "Decision made (ASHP)"
      
      current_confidence: medium
      resolved: false
  
  mastered_topics:
    - topic: "planning_process"
      mastered_date: 2025-02-28
      evidence: "Successfully submitted and navigated full application"
      confidence_progression: [anxious → cautious → confident]
```

This allows Aven to:

- Show "You've grown from 'anxious' to 'confident' on planning—well done!"
- Recommend next learning priorities
- Celebrate progress

---

## How Onboarding Should Use This Schema

### **The Conversational Onboarding Flow**

```
┌─────────────────────────────────────────────────────────┐
│ Welcome to Aven                                         │
│ Let's understand your self-build project together.      │
│ This'll take about 10 minutes.                          │
└─────────────────────────────────────────────────────────┘

┌─ Step 1: The Dream (2 min) ─────────────────────────────┐
│ "What kind of home are you imagining?"                  │
│                                                         │
│ [Visual choice cards:]                                  │
│ ○ Modern & minimal   ○ Traditional cottage              │
│ ○ Contemporary eco   ○ Industrial warehouse             │
│                                                         │
│ "How many bedrooms?"  [2 ▼]                             │
│ "Any must-haves?"    [text: "Home office, lots of       │
│                              natural light"]            │
└─────────────────────────────────────────────────────────┘
↓ Populates: design_intent.style, accommodation, must_haves

┌─ Step 2: The Site (3 min) ───────────────────────────────┐
│ "Where is this happening?"                               │
│                                                          │
│ Region:     [South West ▼]                               │
│ Site type:  ○ Garden  ○ Field  ○ Brownfield  ○ Other     │
│ Size:       [Approx 0.5 acres]                           │
│                                                          │
│ "Do you know about any planning constraints?"            │
│ ☐ Conservation area                                      │
│ ☐ Tree preservation orders                               │
│ ☐ I'm not sure yet                                       │
│                                                          │
│ [If "not sure":]                                         │
│ "No worries—we'll help you find out. I'll remind         │
│  you to check with your local planning authority."       │
└──────────────────────────────────────────────────────────┘
↓ Populates: location, site basics, flags knowledge_gaps

┌─ Step 3: The Team & Timeline (2 min) ────────────────────┐
│ "Where are you in the journey?"                          │
│ ○ Just dreaming                                          │
│ ○ Have land, starting planning                           │
│ ○ Planning approved, ready to build                      │
│ ○ Already building                                       │
│                                                          │
│ "Have you hired an architect yet?"                       │
│ ○ Yes [expand: name, practice, stages]                   │
│ ○ Not yet                                                │
│ ○ Doing it myself                                        │
│                                                          │
│ "When do you hope to move in?"  [Month/Year picker].     │
└──────────────────────────────────────────────────────────┘
↓ Populates: project_stage, timeline, professional_team

┌─ Step 4: How Can Aven Help? (2 min) ─────────────────────┐
│ "How would you describe your self-build experience?"     │
│ ○ Total beginner—explain everything                      │
│ ○ Some knowledge—guide me through gaps                   │
│ ○ Experienced—just help me organize                      │
│                                                          │
│ "How do you prefer to learn?"                            │
│ ○ Show me examples and images                            │
│ ○ Explain step-by-step                                   │
│ ○ Give me resources to read myself                       │
│                                                          │
│ "How are you feeling about this project?"                │
│ ○ Excited but overwhelmed                                │
│ ○ Cautiously optimistic                                  │
│ ○ Confident and ready                                    │
│ ○ Stressed and uncertain                                 │
└──────────────────────────────────────────────────────────┘
↓ Populates: experience_level, learning_style, 
             confidence_level, communication_preference

┌─ Final Step: Your Workspace is Ready ────────────────────┐
│ "Thanks! I've created a workspace for your project."     │
│                                                          │
│ Based on what you've told me, here's what I've set up:   │
│                                                          │
│ ✓ Design brief started (2-bed modern eco home)           │
│ ✓ Site context captured (rural, South West)              │
│ ✓ Planning checklist tailored to your location           │
│ ✓ Budget framework (ready when you are)                  │
│ ✓ Learning resources suggested for beginners             │
│                                                          │
│ Your next steps:                                         │
│ 1. Add more detail about your site constraints           │
│ 2. Explore room-by-room design ideas                     │
│ 3. Understand your planning requirements                 │
│                                                          │
│ [Start Exploring] [Take a Tour]                          │
└──────────────────────────────────────────────────────────┘
```

---

### **Post-Onboarding: Progressive Data Capture**

After onboarding, Aven **prompts contextually**:

```
┌─ Dashboard: Active Prompts ──────────────────────────────┐
│ 📍 You mentioned your site is rural—have you checked     │
│    if it's in an AONB or National Park?                  │
│    [Yes, it is] [No, it's not] [I'll check later]        │
│                                                          │
│ 💷 Ready to think about budget? I can help you build     │
│    a realistic cost breakdown.                           │
│    [Start Budget] [Not yet]                              │
│                                                          │
│ 🏗️ You're at concept stage—typical next step is          │
│    hiring an architect. Want guidance on that?           │
│    [Show me] [Already sorted]                            │
└──────────────────────────────────────────────────────────┘
```

**The schema fills in gradually, invisibly, through:**

- User responses to prompts
- Documents uploaded (planning apps, surveys)
- Vault scanning (extracting mentions, dates, decisions)
- Inferred data (postcode → likely planning authority)

---

## Integration with the Concept Document

### **How YAML + UX Concept Work Together**

|Concept Document Says|YAML Schema Enables|
|---|---|
|"Every design choice ripples across the system"|`decisions` with `linked_to: {room_id, cost_item_id, stage_id}`|
|"Context-aware guidance engine"|`constraints`, `knowledge_gaps`, `confidence_level` trigger prompts|
|"Living project narrative"|`conversations`, `learning_journey`, `progress_tracking` tell the story|
|"Budget as living system"|`budget.breakdown` with `linked_to` relationships across entities|
|"Dashboard shows project health"|`project_health` (computed) surfaces alerts and scores|

The YAML is the **data backbone**—but it should be **invisible** to users. They experience it as:

- Smart prompts
- Auto-populated pages
- Connected insights
- Progress celebration

---

## Recommended Next Steps

### **1. Trim the Schema for MVP**

Create a "Core MVP Schema" with just:

- User profile (experience, stage, confidence)
- Project basics (type, location, size, budget)
- Design intent (style, rooms, must-haves)
- Key constraints (planning, site)
- Decisions log
- Learning journey

**Defer to v2**:

- Detailed building regs tracking
- Inspection scheduling
- Material specifications
- Detailed budget variance tracking

### **2. Build the Conversational Onboarding Flow**

Prototype the 4-phase onboarding as:

- A Typeform/Tally survey (quick test)
- A Streamlit interactive prototype
- A Figma clickable mockup

Test with 5 real self-builders—time how long it takes, where they hesitate, what they skip.

### **3. Create "Schema Population Rules"**

Document how each field gets filled:

```yaml
site.soil_type:
  population_methods:
    - user_input: "Direct question during onboarding"
    - document_extraction: "Parse geotechnical survey PDF"
    - inference: "If site.drainage = waterlogged, likely clay"
    - prompt: "When user enters foundations stage"
  
  relevance:
    - stage: design
      importance: low
    - stage: foundations
      importance: critical
      prompt: "We need to know soil type before designing foundations"
```

### **4. Map YAML to UI Pages**

For each major section, sketch:

- **Where** the data appears in the UI
- **When** it gets captured
- **Why** it matters (user benefit)

Example:

```
site.topography → [Site Context page]
                → [Foundation Design considerations]
                → [Cost estimator] (slopes increase costs)
                → [Schedule] (slopes slow groundworks)
```

### **5. Build One Complete Vertical Slice**

Prove the full loop:

```
Onboarding (capture bedrooms: 2)
  ↓
Dashboard (shows "Design Brief: 2 bedrooms")
  ↓
Design Brief page (auto-creates Bedroom 1, Bedroom 2)
  ↓
Bedroom 1 page (add design choice: carpet)
  ↓
Budget (auto-adds: Finishes → Bedroom 1 Flooring → £800)
  ↓
Dashboard (updates: "Budget 12% spent, Design 40% complete")
```

---

## Final Thought

Your YAML schema is **comprehensive and thoughtful**—it shows you've done the research. But remember:

> **The best data model is the one users never see.**

Aven's job is to:

1. **Capture** data invisibly through conversation
2. **Connect** it behind the scenes
3. **Surface** insights at the right moment
4. **Guide** without lecturing

The schema is your **backend engine**—but the user experiences it as a **calm, knowledgeable companion** that just seems to know what they need, when they need it.

**You're building the right thing. Now focus on making it feel effortless.**

# Aven Memory Store YAML Schema considerations

This is an **exceptionally comprehensive** data model. You've clearly thought deeply about what information matters across the entire self-build lifecycle. Let me give you structured feedback on what's working, what's missing, and how to enrich it further.

---

## What's Working Really Well

### 1. **Holistic Coverage**

You've mapped the full spectrum: user psychology → site constraints → design intent → project execution → reflection. This breadth is rare and valuable.

### 2. **Contextual Intelligence Foundations**

Fields like `knowledge_gaps_identified`, `confidence_progression`, and `topics_requiring_sensitivity` show you understand Aven needs to **adapt** to the user, not just store their data.

### 3. **Relationship Mapping**

The implicit connections are strong:

- Site constraints → planning constraints → design decisions
- Budget → procurement → materials palette
- Risks → mitigation → professional team

### 4. **Temporal Awareness**

You're tracking **change over time** (design iterations, confidence progression, decision logs), which is critical for a living project system.

---

## What's Missing or Needs Strengthening

### **A. Pre-Project Feasibility & Discovery**

Your schema jumps into site analysis assuming land is acquired. Add:

#### **Land Search & Acquisition Phase**

```yaml
land_acquisition:
  status: null  # searching, offer_made, under_offer, completed, not_applicable
  
  search_criteria:
    budget_max: null
    location_preferences: []  # regions, proximity to work/family/schools
    site_size_min: null
    site_size_max: null
    deal_breakers: []  # e.g., "no conservation areas", "must have mains sewerage"
  
  plots_considered:
    - plot_id: null
      location: null
      size: null
      price: null
      status: null  # viewing_arranged, dismissed, offer_made, lost
      pros: []
      cons: []
      why_dismissed: null
      feasibility_score: null  # 1-10
  
  acquisition_details:
    purchase_date: null
    purchase_price: null
    legal_fees: null
    stamp_duty: null
    surveys_commissioned:
      - type: null  # boundary, topographic, ground_investigation, arboricultural
        cost: null
        completed: false
        key_findings: []
```

**Why**: Many self-builders are in "plot hunting" mode long before they have a site. Aven should help them **evaluate options** and **track near-misses** (learning from rejected plots).

---

### **B. Financial Complexity & Cash Flow**

Your budget section is good but needs **temporal granularity**:

#### **Enhanced Budget Tracking**

```yaml
budget:
  # Add these sections:
  
  cash_flow:
    monthly_projections:
      - month: null  # YYYY-MM
        planned_spend: null
        actual_spend: null
        variance: null
        cumulative_spend: null
    
    payment_schedule:
      - payee: null  # architect, contractor, supplier
        description: null  # stage payment, materials delivery
        due_date: null
        amount: null
        paid_date: null
        paid_amount: null
        payment_method: null  # bank_transfer, cheque, cash, credit_card
        retention_held: null  # for contractors
        invoice_reference: null
  
  funding_drawdowns:  # For self-build mortgages
    - stage: null  # land, foundations, watertight, first_fix, completion
      approved_amount: null
      inspection_date: null
      inspection_passed: null
      funds_released_date: null
      actual_amount: null
  
  value_engineering_log:
    - item: null
      original_spec: null
      revised_spec: null
      saving: null
      quality_impact: null  # none, minor, moderate, significant
      reversible: null
      decision_date: null
  
  contingency_usage:
    - date: null
      reason: null
      amount: null
      category: null  # unforeseen_ground_conditions, design_change, price_increase
      remaining_contingency: null
```

**Why**: Cash flow kills self-builds. Users need to see **when** money goes out, not just totals. Self-build mortgage drawdown tracking is especially critical.

---

### **C. Contractor & Labour Management**

You have professional team tracking, but site-level labour needs more detail:

#### **Construction Team & Labour**

```yaml
construction_team:
  main_contractor:
    hired: false
    company: null
    contact: null
    contract_type: null  # JCT, bespoke, verbal
    start_date: null
    completion_date: null
    payment_terms: null
    insurance_verified: null
    performance_notes: null
  
  subcontractors:
    - trade: null  # groundworker, bricklayer, roofer, plasterer, electrician, plumber
      company: null
      name: null
      contact: null
      scope: null
      start_date: null
      completion_date: null
      day_rate_or_price: null
      payment_terms: null
      performance_rating: null  # 1-5
      would_use_again: null
      notes: null
      insurance_verified: null
      qualifications: []  # Gas Safe, NICEIC, etc.
  
  labour_diary:
    - date: null
      trade: null
      workers: null  # number on site
      hours_worked: null
      tasks_completed: []
      materials_used: []
      next_day_plan: null
      issues: []
      photos: []
```

**Why**: Self-builders managing their own build need **daily accountability**. This helps with payment tracking, programme monitoring, and quality control.

---

### **D. Site Logistics & Safety**

Construction sites have practical operational needs:

#### **Site Operations**

```yaml
site_operations:
  site_setup:
    site_office_hoarding: false
    welfare_facilities: null  # toilet, water, first_aid
    security: []  # fence, camera, site_manager_presence
    waste_management: null  # skip_hire, segregated_waste
    deliveries_access: null
  
  utilities_during_construction:
    temporary_power:
      provider: null
      meter_location: null
      cost_per_week: null
    temporary_water:
      provider: null
      meter_location: null
    site_phone_signal: null  # good, poor, none
  
  health_and_safety:
    cdm_regulations_apply: null
    principal_designer_appointed: false
    principal_contractor_appointed: false
    construction_phase_plan: null  # filepath
    site_safety_file: null  # filepath
    
    risk_assessments:
      - activity: null  # excavation, working_at_height, lifting_operations
        risk_level: null
        mitigation: null
        responsible_person: null
        date: null
    
    incidents_log:
      - date: null
        type: null  # near_miss, injury, damage
        description: null
        injured_party: null
        actions_taken: []
        reportable_to_hse: null
  
  weather_log:
    - date: null
      conditions: null  # dry, rain, heavy_rain, snow, frost, wind
      temp_celsius: null
      impact_on_work: null  # none, delayed, stopped
```

**Why**: CDM regulations require health & safety management. Weather tracking is **crucial** for programme extensions and insurance claims (frost damage, waterlogged ground).

---

### **E. Design Specification Detail**

Your materials palette is good, but needs more **room-level granularity**:

#### **Room-by-Room Specifications**

```yaml
rooms:  # New top-level section
  - room_id: null
    name: null  # "Kitchen", "Bedroom 1", "En-suite"
    type: null  # kitchen, bedroom, bathroom, living, utility, hallway, wc
    floor: null  # ground, first, second, basement, loft
    area_sqm: null
    
    design_choices:
      flooring:
        material: null  # tiles, engineered_wood, carpet, vinyl, polished_concrete
        product: null
        supplier: null
        colour_finish: null
        cost_per_sqm: null
        total_cost: null
        underfloor_heating: null
        status: null  # considering, specified, ordered, installed
      
      walls:
        finish: null  # plaster_and_paint, tiles, panelling, wallpaper
        paint_colour: null
        paint_brand: null
        feature_wall: null
        status: null
      
      ceiling:
        height: null
        finish: null  # plaster_and_paint, exposed_beams, coffered
        lighting_type: []  # recessed, pendant, track, wall_lights
        status: null
      
      windows:
        quantity: null
        type: null  # casement, sash, fixed, sliding
        material: null  # upvc, timber, aluminium
        glazing: null  # double, triple
        u_value: null
        supplier: null
        cost_per_unit: null
        status: null
      
      doors:
        quantity: null
        type: null  # solid, glazed, sliding, bifold
        material: null
        finish: null
        supplier: null
        cost: null
        status: null
      
      fixtures_and_fittings:  # Bathroom/kitchen specific
        - item: null  # basin, toilet, shower, bath, kitchen_units, worktop
          product: null
          supplier: null
          cost: null
          status: null
      
      electrical:
        socket_outlets: null  # quantity
        light_switches: null
        data_points: null  # ethernet, TV aerial
        special_requirements: []  # USB sockets, smart_switches, dimmer
      
      heating:
        type: null  # radiator, ufh, both
        emitter_size: null
        thermostat_location: null
      
      ventilation:
        type: null  # natural, mechanical, mvhr
        extract_points: null
    
    linked_building_regs: []  # Part F, Part L, Part M, etc.
    linked_budget_categories: []
    linked_tasks: []
    completion_percentage: null
    notes: null
```

**Why**: This is where **design intent meets physical reality**. Every design choice has cost, regulatory, and schedule implications. Room-level tracking makes these connections explicit.

---

### **F. Warranty & Defects Management**

Your schema ends at completion, but the journey continues:

#### **Post-Completion & Defects**

```yaml
completion:
  practical_completion:
    date: null
    certificate_received: false
    snag_list: []  # See below
    outstanding_works: []
  
  final_completion:
    date: null
    final_certificate_received: false
    retention_released: false
  
  warranties:
    - type: null  # structural_warranty, workmanship, product
      provider: null  # NHBC, LABC, Premier, manufacturer
      reference: null
      coverage: null
      start_date: null
      expiry_date: null
      claim_process: null
      cost: null
      documentation: null  # filepath
  
  snagging:
    - item_id: null
      room: null
      description: null
      severity: null  # critical, major, minor, cosmetic
      responsible_party: null  # contractor, subcontractor, supplier
      reported_date: null
      target_fix_date: null
      actual_fix_date: null
      status: null  # open, in_progress, fixed, verified
      photos: []
      reinspection_required: null
  
  defects_liability_period:
    duration_months: null  # typically 6-12
    start_date: null
    end_date: null
    
    defects_reported:
      - defect_id: null
        description: null
        reported_date: null
        severity: null
        responsible_party: null
        warranty_claim: null
        resolution: null
        cost: null
  
  handover_documentation:
    as_built_drawings: false
    operation_and_maintenance_manuals: false
    building_log_book: false
    warranties_and_guarantees: false
    energy_performance_certificate: false
    building_control_completion_certificate: false
    planning_compliance_certificate: false
    electrical_installation_certificate: false
    gas_safety_certificate: false
    water_regulations_certificate: false
```

**Why**: The defects period is when hidden issues emerge. Tracking warranty expiry dates prevents missed claims. Handover documentation is **essential** for future sales or insurance claims.

---

### **G. Sustainability & Performance Monitoring**

You capture intent, but not **actual performance**:

#### **Performance Monitoring (Post-Occupancy)**

```yaml
performance_monitoring:
  energy:
    predicted_epc_rating: null
    actual_epc_rating: null
    predicted_annual_energy_use_kwh: null
    
    actual_energy_use:
      - period: null  # YYYY-MM
        electricity_kwh: null
        gas_kwh: null  # if applicable
        cost: null
        degree_days: null  # weather correction
    
    heating_system_performance:
      - date: null
        cop_or_efficiency: null  # coefficient of performance for heat pumps
        notes: null
  
  airtightness:
    predicted: null
    actual_test_result: null  # m³/h/m² @ 50Pa
    test_date: null
    test_company: null
    pass_or_fail: null
  
  thermal_imaging:
    test_date: null
    test_company: null
    issues_identified: []
    remedial_work: []
  
  indoor_environment:
    temperature_comfort: null  # user satisfaction rating
    humidity_issues: null
    condensation_problems: []
    ventilation_adequacy: null
  
  water_use:
    predicted_litres_per_person_per_day: null
    actual_usage_tracked: null
  
  renewable_generation:
    - system: null  # pv, solar_thermal
      predicted_annual_kwh: null
      actual_annual_kwh: null
      export_vs_self_consumption: null
```

**Why**: The "performance gap" between design intent and reality is a huge issue. Post-occupancy monitoring helps users (and future Aven AI) learn what actually works.

---

### **H. Emotional & Psychological Journey**

You track confidence and learning, but miss the **emotional reality**:

#### **Wellbeing & Stress Management**

```yaml
personal_journey:
  stress_levels:
    - date: null
      level: null  # 1-10
      triggers: []  # budget_overrun, contractor_dispute, planning_delay
      coping_strategies: []
      support_needed: null
  
  relationship_impact:
    partner_alignment: null  # aligned, some_tension, significant_strain
    decision_making_process: null  # collaborative, one_lead, conflict
    areas_of_disagreement: []
    resolution_strategies: []
  
  lifestyle_disruption:
    current_living_situation: null  # staying_on_site, renting, with_family
    commute_to_site: null
    work_life_balance: null
    childcare_eldercare_impacts: []
  
  support_network:
    - person: null
      relationship: null  # family, friend, mentor, professional
      type_of_support: null  # emotional, practical, financial, technical
      availability: null
  
  milestone_celebrations:
    - milestone: null
      date: null
      how_celebrated: null
      reflection: null
  
  lessons_learned_reflections:
    what_went_well: []
    what_was_challenging: []
    what_would_do_differently: []
    advice_for_others: []
```

**Why**: Self-build is **emotionally grueling**. Tracking wellbeing helps Aven recognize when to ease off vs. push forward. It also creates a valuable **emotional archive** for later reflection.

---

### **I. Communications & Correspondence**

You have meeting logs but need **full audit trails**:

#### **Communications Hub**

```yaml
communications:
  correspondence_log:
    - date: null
      direction: null  # sent, received
      party: null  # architect, planner, contractor, neighbour
      method: null  # email, letter, phone, meeting, site_visit
      subject: null
      summary: null
      action_items: []
      follow_up_required: null
      follow_up_date: null
      linked_documents: []
      linked_decisions: []
      sentiment: null  # positive, neutral, concerning, conflict
  
  key_agreements:
    - party: null
      agreement_type: null  # contract, variation, approval, waiver
      date: null
      summary: null
      legal_implications: null
      documentation: null
  
  disputes_and_resolutions:
    - issue: null
      parties: []
      raised_date: null
      severity: null  # minor, moderate, major, legal_action
      resolution_attempted: []
      outcome: null
      lessons_learned: null
  
  planning_officer_interactions:
    - date: null
      officer_name: null
      topic: null
      guidance_given: null
      follow_up_actions: []
```

**Why**: Construction disputes often hinge on **who said what when**. A clear communication log is both project management and legal protection.

---

### **J. Local Knowledge & Relationships**

#### **Community & Local Context**

```yaml
local_context:
  neighbours:
    - address: null
      relationship: null  # supportive, neutral, concerned, hostile
      concerns_raised: []
      engagement_attempts: []
      consultation_response: null  # planning objection, support, neutral
  
  local_resources:
    builders_merchants: []  # names, distances, account_status
    tool_hire: []
    skip_hire: []
    nearest_dump: null
    local_trades_directory: []
  
  local_authority_contacts:
    - department: null  # planning, building_control, highways, environmental_health
      contact_name: null
      direct_line: null
      email: null
      responsiveness: null  # excellent, good, slow, poor
      notes: null
  
  community_resources:
    self_build_group: null
    local_forums: []
    recommended_professionals: []  # word-of-mouth recommendations
```

**Why**: Local relationships matter. A supportive neighbor can ease planning; a hostile one can derail it. Tracking local resources saves **hours of googling**.

---

### **K. Insurance & Legal**

#### **Insurance & Legal Protection**

```yaml
insurance:
  site_insurance:
    provider: null
    policy_number: null
    coverage: null  # public_liability, employer_liability, contract_works
    start_date: null
    expiry_date: null
    premium: null
    excess: null
    claims_made: []
  
  professional_indemnity:  # for self-builders acting as clients
    required: null
    provider: null
    coverage_level: null
  
  latent_defects_insurance:  # structural warranty
    provider: null
    coverage: null
    start_date: null
    duration: null  # typically 10 years
    policy_number: null

legal:
  land_registry:
    title_number: null
    ownership_type: null  # freehold, leasehold
    restrictions: []
    covenants: []
  
  easements_and_rights:
    - type: null  # right_of_way, drainage, light
      benefiting_or_burdening: null
      description: null
      impact_on_build: null
  
  party_wall_agreements:
    - neighbour: null
      agreement_date: null
      scope: null
      surveyor: null
      documentation: null
  
  solicitor:
    firm: null
    contact: null
    matters_handled: []
```

**Why**: Legal and insurance gaps cause **catastrophic failures**. Tracking these proactively prevents nasty surprises.

---

## Structural Improvements to the Schema

### **1. Add Explicit Relationships**

Your schema is flat. Add relationship mappings:

```yaml
relationships:
  design_choices_to_costs:
    - design_choice_id: null
      cost_item_id: null
  
  decisions_to_risks:
    - decision_id: null
      risk_ids: []
  
  rooms_to_tasks:
    - room_id: null
      task_ids: []
  
  professionals_to_stages:
    - professional: null
      riba_stages: []
```

**Why**: This makes the **interconnected nature** of the project explicit for both humans and machines.

---

### **2. Add Status Enums Consistently**

Throughout the schema, add standardized status fields:

```yaml
# Example pattern:
item:
  status: null  # not_started, in_progress, on_hold, completed, cancelled
  status_updated: null  # date
  status_reason: null  # why on_hold or cancelled
  blocking_issues: []
```

---

### **3. Add Confidence & Quality Scores**

For every major data point:

```yaml
item:
  value: null
  confidence: null  # low, medium, high, verified
  source: null  # user_estimate, professional_quote, actual_invoice
  last_verified: null
  verification_method: null
```

**Why**: Distinguishes **rough guesses** from **verified facts**. Critical for AI reasoning.

---

### **4. Add Change History**

For mutable fields (budget, timeline, design specs):

```yaml
item:
  current_value: null
  history:
    - date: null
      previous_value: null
      new_value: null
      reason: null
      changed_by: null
```

**Why**: Tracks **why** things changed. Essential for learning and dispute resolution.

---

### **5. Add Attachment Management**

Throughout:

```yaml
attachments:
  - filename: null
    filepath: null
    type: null  # pdf, image, spreadsheet, cad_drawing
    category: null  # quote, invoice, drawing, certificate, photo
    uploaded_date: null
    uploaded_by: null
    linked_to: []  # room_id, decision_id, task_id
    tags: []
    description: null
```

**Why**: Documents **are** the project. They need first-class status in the schema.

---

## What to Capture During Onboarding vs. Later

**Don't try to capture everything upfront.** The YAML is a target state, not an onboarding questionnaire.

### **Onboarding (First 30 Minutes)**

Capture only:

- User profile (experience, confidence, stage)
- Project basics (type, location, rough scale)
- Design intent (style, must-haves, priorities)
- Current biggest concern
- One key milestone date (planning submission or construction start)

**Progressive Disclosure**: Build the rest **as needed**:

- Site details → when planning application starts
- Budget breakdown → when costing begins
- Room specifications → when designing spaces
- Contractor details → when procurement starts

---

## Final Recommendations

### **Schema Management**

1. **Version the schema**: This is v2.0—plan for v3.0 when you learn what actually matters
2. **Mark required vs. optional**: Not everything needs to be filled in
3. **Add data validation rules**: Dates, enums, number ranges
4. **Create a "minimal viable project" subset**: What's the absolute minimum to make Aven useful?

### **User Experience**

5. **Don't expose the YAML**: This is the **data model**, not the UI
6. **Infer what you can**: If user says "timber frame", auto-suggest relevant building regs
7. **Offer templates**: "First-time self-builder in rural England" pre-populates sensible defaults

### **AI Integration**

8. **Add semantic tags**: Help AI understand what fields mean
9. **Flag uncertainty**: Track what's estimated vs. known
10. **Enable natural language input**: User types "met with planner yesterday, they were concerned about roof height" → Aven extracts structured data

---

## Summary

Your schema is **excellent** as a foundation. The additions I've suggested focus on:

1. **Earlier stages** (land search, feasibility)
2. **Operational detail** (daily site work, cash flow, labour)
3. **Later stages** (defects, performance, reflection)
4. **Relationships** (making connections explicit)
5. **Human factors** (stress, emotions, communications)
6. **Legal/insurance** (often forgotten until too late)

The result will be a schema that **captures the full lived experience** of self-building, not just the technical project data.

**One caveat**: This is now a **very large** schema. You'll need smart UI patterns to avoid overwhelming users. Think: progressive disclosure, contextual prompts, smart defaults, and natural language input.

# Continuing Schema Development - Additional Fields & Sections

Excellent—let's keep building this out systematically. You mentioned post-build snagging (which I added in the previous response), so let me expand that and add other critical missing sections.

---

## **Additional Major Sections Needed**

### **L. Programme & Schedule Management**

This is more granular than your current `timeline` section:

```yaml
programme:
  baseline_programme:
    created_date: null
    created_by: null  # architect, contractor, user
    total_duration_weeks: null
    planned_start: null
    planned_completion: null
    methodology: null  # critical_path, agile, phased
  
  current_programme:
    revised_date: null
    current_completion_forecast: null
    delay_weeks: null
    reasons_for_delay: []
  
  critical_path_activities: []  # Activities that must stay on track
  
  programme_versions:
    - version: null
      date: null
      reason_for_revision: null
      key_changes: []
      filepath: null  # Link to Gantt chart/PDF
  
  activities:
    - activity_id: null
      activity_name: null
      description: null
      trade: null  # groundworks, brickwork, roofing, etc.
      stage: null  # Link to RIBA stage or build phase
      
      dates:
        planned_start: null
        planned_finish: null
        actual_start: null
        actual_finish: null
        forecast_finish: null  # If running late
      
      duration:
        planned_days: null
        actual_days: null
      
      dependencies:
        predecessors: []  # activity_ids that must finish first
        successors: []    # activities waiting on this one
        lag_days: null    # Gap between activities
      
      resources:
        labour_required: []  # trades needed
        plant_equipment: []  # scaffolding, excavator, crane
        materials_required: []
      
      status: null  # not_started, in_progress, on_hold, completed, cancelled
      percent_complete: null
      
      critical_path: false  # Is this on the critical path?
      float_days: null  # How much slack time exists
      
      weather_dependent: false
      inspection_required: false
      
      issues:
        - issue: null
          impact: null  # days_delay, cost_increase, quality_concern
          resolution: null
      
      linked_to:
        rooms: []
        design_choices: []
        cost_items: []
        inspections: []
        supplier_deliveries: []
```

**Why**: Programme management is where self-builds fall apart. This creates a **living schedule** that shows dependencies, delays, and impacts.

---

### **M. Materials & Procurement Management**

More detailed than your current `materials_palette`:

```yaml
materials:
  - material_id: null
    category: null  # structural, external_envelope, internal_finishes, services, landscaping
    element: null  # foundations, walls, roof, windows, flooring, etc.
    
    specification:
      product_name: null
      manufacturer: null
      product_code: null
      technical_spec: null
      colour_finish: null
      dimensions: null
      units: null  # m², linear_m, nr (number), tonnes
      
    quantity:
      estimated: null
      ordered: null
      delivered: null
      used: null
      wastage: null
      remaining: null
    
    sourcing:
      supplier: null
      supplier_contact: null
      quote_reference: null
      lead_time_weeks: null
      alternatives_considered: []
      
    costs:
      quoted_unit_price: null
      quoted_total: null
      actual_unit_price: null
      actual_total: null
      delivery_charge: null
      variance: null
    
    procurement_status: null  # researching, quoted, ordered, delivered, installed
    
    orders:
      - order_reference: null
        order_date: null
        expected_delivery: null
        actual_delivery: null
        quantity_ordered: null
        quantity_delivered: null
        delivery_notes: []
        issues: []  # damaged, incorrect, short_delivery
    
    storage:
      storage_location: null  # on_site, off_site, supplier_holding
      storage_requirements: []  # keep_dry, ventilated, secure, temperature_controlled
      condition_checks: []
    
    installation:
      installer: null  # contractor, subcontractor, self
      install_date: null
      install_notes: null
      wastage_actual: null
      quality_issues: []
    
    compliance:
      ce_marking: false
      ukca_marking: false
      fire_rating: null
      sustainability_certification: []  # FSC, BBA, EPD
      warranty_duration: null
      warranty_documentation: null
    
    linked_to:
      rooms: []
      design_choices: []
      building_reg_requirements: []
      programme_activities: []
    
    technical_documentation:
      data_sheets: []
      installation_guides: []
      maintenance_requirements: []
      certificates: []

procurement_strategy:
  approach: null  # package_deals, individual_suppliers, hybrid
  payment_terms_preference: null  # upfront, on_delivery, credit_account, stage_payments
  bulk_order_opportunities: []
  long_lead_items_identified: []  # Items to order early (windows, kitchen, etc.)
  
  preferred_suppliers:
    - supplier: null
      categories: []  # What they supply
      account_status: null  # trade_account, cash, credit_terms
      discount_available: null
      reliability_rating: null  # 1-5
      notes: null
```

**Why**: Material procurement is **complex logistics**. This tracks the full journey from specification → quote → order → delivery → installation, with all the associated decisions and costs.

---

### **N. Quality Control & Testing**

```yaml
quality_control:
  quality_plan:
    created_date: null
    responsible_person: null  # main_contractor, self, architect
    inspection_schedule: []
    testing_requirements: []
  
  inspections:
    - inspection_id: null
      inspection_type: null  # building_control, warranty_provider, self_inspection, professional
      stage: null  # foundations, dpc, drains, structure, services, completion
      inspector: null
      inspector_organization: null
      
      scheduled_date: null
      actual_date: null
      
      checklist_items:
        - item: null
          requirement: null
          actual: null
          pass_fail: null  # pass, fail, advisory
          notes: null
          photo_reference: null
      
      overall_outcome: null  # passed, passed_with_advisories, failed, partial
      
      non_compliances:
        - issue: null
          severity: null  # critical, major, minor
          regulation_breached: null  # Part A, Part L, etc.
          remedial_action_required: null
          responsible_party: null
          target_resolution_date: null
          actual_resolution_date: null
          re_inspection_required: false
      
      inspection_report: null  # filepath
      photos: []
      
      follow_up_actions:
        - action: null
          responsible: null
          due_date: null
          status: null
  
  testing_regime:
    - test_id: null
      test_type: null  # airtightness, drainage, electrical, sound, thermal_imaging
      required_by: null  # building_regs, warranty, client_spec
      
      test_date: null
      test_company: null
      test_engineer: null
      
      specification_requirement: null
      test_result: null
      pass_fail: null
      
      certification:
        certificate_reference: null
        certificate_date: null
        valid_until: null
        filepath: null
      
      notes: null
      cost: null
  
  site_audits:
    - audit_date: null
      auditor: null  # self, architect, quantity_surveyor, main_contractor
      focus_areas: []  # workmanship, safety, tidiness, progress
      findings: []
      recommendations: []
      follow_up_date: null

  workmanship_standards:
    expected_standard: null  # building_regs_minimum, good_trade_practice, high_specification
    reference_standards: []  # NHBC, BBA, manufacturer_specs
    
    quality_issues_log:
      - issue_id: null
        date_identified: null
        location: null  # room or area
        trade: null
        issue_description: null
        severity: null  # cosmetic, minor, major, critical
        photo_evidence: []
        
        responsible_party: null
        issue_acknowledged: false
        rectification_required: null
        rectification_deadline: null
        rectification_completed: null
        re_inspected: false
        resolution_satisfactory: null
        
        cost_implications: null
        programme_implications: null
```

**Why**: Quality control is the **defense against costly mistakes**. This creates an audit trail and ensures nothing slips through the cracks.

---

### **O. Variations & Change Orders**

This is critical and completely missing:

```yaml
variations:
  - variation_id: null
    variation_number: null  # VO-001, VO-002, etc.
    raised_date: null
    raised_by: null  # client, architect, contractor, building_control
    
    change_type: null  # design_change, spec_upgrade, omission, addition, remedial_work
    
    description: null
    reason: null  # client_request, unforeseen_conditions, regulatory_requirement, error_correction
    
    affected_areas:
      rooms: []
      programme_activities: []
      design_elements: []
      contracts: []
    
    cost_impact:
      estimated: null
      quoted: null
      agreed: null
      actual: null
      
      breakdown:
        labour: null
        materials: null
        plant: null
        preliminaries: null
        overheads_profit: null
    
    programme_impact:
      delay_days: null
      critical_path_affected: false
      new_completion_date: null
    
    approval_process:
      submitted_for_approval: null
      approver: null  # client, architect, project_manager
      approved: null
      approved_date: null
      approval_conditions: []
      rejected_reason: null
    
    status: null  # pending, approved, in_progress, completed, disputed, cancelled
    
    implementation:
      start_date: null
      completion_date: null
      contractor: null
      quality_check: null
    
    payment:
      invoiced: false
      invoice_reference: null
      paid: false
      payment_date: null
    
    documentation:
      quotations: []
      instructions: []
      drawings_revised: []
      specifications_updated: []
      photos: []
    
    disputes:
      disputed: false
      dispute_reason: null
      resolution: null
    
    linked_to:
      original_design_choices: []
      original_cost_items: []
      risks: []  # If this was addressing a risk
      decisions: []

variation_summary:
  total_variations: null
  total_cost_impact: null
  total_programme_impact_days: null
  pending_approval_count: null
  disputed_count: null
```

**Why**: Variations are **inevitable** and often contentious. Clear tracking prevents disputes and budget blowouts.

---

### **P. Commissioning & Testing (Services)**

Separate from quality control—this is about making systems work:

```yaml
commissioning:
  mechanical_services:
    heating_system:
      system_type: null  # ashp, gshp, boiler, ufh, radiators
      commissioning_engineer: null
      commissioning_date: null
      
      tests_performed:
        - test: null  # pressure_test, flow_rates, cop_measurement, controls_setup
          result: null
          within_spec: null
          notes: null
      
      settings_recorded:
        flow_temperature: null
        return_temperature: null
        pressure: null
        pump_settings: []
      
      user_training_provided: false
      user_manual_provided: false
      
      certification: null  # filepath
      warranty_registered: false
    
    ventilation:
      system_type: null  # mvhr, mev, natural
      commissioning_engineer: null
      commissioning_date: null
      
      airflow_tests:
        - room: null
          required_flow_rate: null
          actual_flow_rate: null
          pass_fail: null
      
      filter_locations: []
      maintenance_schedule: null
      
      certification: null
      warranty_registered: false
    
    hot_water:
      system_type: null
      commissioning_date: null
      legionella_risk_assessment: false
      temperature_settings: []
      certification: null
  
  electrical_services:
    installation_certificate:
      reference: null
      issue_date: null
      electrician: null
      registration_number: null  # NICEIC, etc.
      filepath: null
    
    tests_performed:
      earth_continuity: null
      insulation_resistance: null
      polarity: null
      rcd_operation: null
      
    consumer_unit:
      location: null
      type: null
      main_fuse_rating: null
      rcbo_rcd_protection: null
      surge_protection: null
    
    circuits:
      - circuit_id: null
        description: null  # "Ground floor sockets", "Upstairs lights"
        cable_size: null
        protective_device: null
        test_results: []
    
    smart_home_systems:
      - system: null  # lighting_control, heating_control, security, av
        commissioned: false
        user_training: false
        documentation: null
  
  plumbing_services:
    water_supply:
      pressure_test_date: null
      test_result: null
      certification: null
    
    drainage:
      test_date: null
      test_type: null  # air_test, water_test, cctv_survey
      test_result: null
      certification: null
      
    water_treatment:
      softener_installed: false
      filtration_installed: false
      commissioning_date: null
  
  renewable_systems:
    - system_type: null  # pv, solar_thermal, battery_storage
      installation_date: null
      commissioning_date: null
      installer: null
      mcs_certificate: null
      export_tariff_registered: false
      monitoring_system: null
      expected_generation: null
      warranty_registered: false

handover_training:
  - system: null
    training_provided: false
    training_date: null
    attendees: []
    documentation_provided: []
    follow_up_required: false
```

**Why**: Systems must be **properly commissioned** to work as designed. This also creates a record for future troubleshooting and maintenance.

---

### **Q. Compliance & Certification**

Expand beyond just Building Regs:

```yaml
compliance:
  building_regulations:
    # (Your existing section is good—keep it)
    
  planning_conditions_discharge:
    - condition_reference: null  # "Condition 3", "Condition 7"
      condition_text: null
      category: null  # pre_commencement, pre_occupation, ongoing
      
      requirements: []  # What needs to be submitted
      
      submission:
        submitted: false
        submission_date: null
        documents_submitted: []
        
      officer_review:
        reviewed: false
        review_date: null
        outcome: null  # approved, further_info_required, rejected
        comments: null
        
      status: null  # pending, approved, ongoing_condition
      
      compliance_evidence:
        photos: []
        reports: []
        certificates: []
  
  energy_performance:
    epc_required: true
    epc_assessor: null
    epc_assessment_date: null
    epc_rating: null  # A-G
    epc_score: null  # Numerical value
    epc_certificate: null  # filepath
    epc_recommendations: []
    
    sap_calculation:
      completed: false
      assessor: null
      predicted_rating: null
      filepath: null
    
    renewable_energy_installation:
      mcs_certification: []  # Microgeneration Certification Scheme
      fit_seg_registration: null  # Feed-in Tariff / Smart Export Guarantee
  
  fire_safety:
    fire_strategy_document: null
    fire_door_certification: []
    fire_alarm_system:
      required: false
      installed: false
      certification: null
    smoke_alarm_system:
      installed: false
      type: null  # battery, mains, interlinked
      locations: []
    means_of_escape:
      compliant: null
      protected_routes: []
  
  water_regulations:
    notification_submitted: false
    approval_received: false
    backflow_prevention: []
    certification: null
  
  electrical_certification:
    # (Covered in commissioning—link here)
    
  gas_safety:
    required: false
    gas_safe_engineer: null
    installation_certificate: null
    annual_service_booked: false
  
  asbestos:
    survey_required: false
    survey_completed: false
    asbestos_present: false
    removal_certification: []
  
  contaminated_land:
    assessment_required: false
    remediation_required: false
    validation_report: null
  
  warranties_and_guarantees:
    structural_warranty:
      # (Covered in completion section—link here)
    
    product_warranties:
      - product: null
        warranty_duration: null
        registration_required: false
        registered: false
        expiry_date: null
        documentation: null

certification_checklist:
  - certificate_type: null
    required: false
    obtained: false
    reference: null
    issue_date: null
    expiry_date: null
    filepath: null
    issuing_body: null
```

**Why**: Compliance is **scattered across multiple authorities**. This consolidates everything to ensure nothing is missed.

---

### **R. Meetings & Site Visits**

```yaml
meetings:
  - meeting_id: null
    meeting_type: null  # site_meeting, design_review, progress_meeting, client_decision, planning_officer
    date: null
    location: null  # on_site, office, video_call
    
    attendees:
      - name: null
        role: null
        organization: null
    
    agenda_items: []
    
    discussion_points:
      - topic: null
        summary: null
        linked_to: []  # decisions, risks, tasks, costs
    
    decisions_made:
      - decision: null
        decision_maker: null
        linked_decision_id: null  # Link to decisions_made section
    
    action_items:
      - action: null
        responsible: null
        due_date: null
        status: null
        linked_task_id: null
    
    risks_identified: []
    issues_raised: []
    
    next_meeting:
      scheduled: false
      date: null
      purpose: null
    
    minutes: null  # filepath or text
    photos_taken: []
    
    attendee_satisfaction: null  # productive, mixed, frustrating

site_visits:
  - visit_id: null
    date: null
    visitor: null
    purpose: null  # inspection, progress_check, showing_stakeholders, photography
    
    weather_conditions: null
    site_conditions: null
    
    observations:
      - area: null
        observation: null
        positive_negative: null  # positive, concern, neutral
        photo_reference: null
        action_required: null
    
    progress_assessment:
      activities_on_track: []
      activities_behind: []
      upcoming_activities: []
    
    health_and_safety_observations: []
    quality_observations: []
    
    people_on_site:
      - name: null
        role: null
        company: null
    
    materials_delivered: []
    plant_on_site: []
    
    photos: []
    notes: null
```

**Why**: Meetings generate **decisions and actions** that need tracking. Site visits capture the project's **living reality**.

---

### **S. Stakeholder Management**

Expand beyond just collaboration:

```yaml
stakeholders:
  - stakeholder_id: null
    name: null
    organization: null
    role: null  # client, partner, architect, contractor, planner, lender, neighbour, supplier
    
    contact:
      email: null
      phone: null
      address: null
      preferred_method: null
    
    involvement:
      stage_involved: []  # planning, design, construction, completion
      decision_authority: null  # final_say, advisory, informed_only
      engagement_level: null  # high, medium, low
    
    interests_and_priorities: []
    concerns: []
    risks_associated: []  # e.g., neighbour objection risk
    
    communication_preferences:
      frequency: null  # daily, weekly, monthly, as_needed
      detail_level: null  # high_level, moderate, detailed
      format: null  # email, phone, meeting, report
    
    satisfaction:
      current_level: null  # 1-5
      recent_feedback: null
      issues_raised: []
    
    key_interactions:
      last_contact: null
      interaction_log: []  # References to communications section
    
    relationship_status: null  # positive, neutral, strained, adversarial
    
    influence_power:
      influence_level: null  # high, medium, low
      power_level: null  # high, medium, low
      management_strategy: null

stakeholder_engagement_plan:
  - stakeholder: null
    engagement_strategy: null
    touchpoints: []
    escalation_process: null
```

**Why**: Self-builds involve **many people with different agendas**. Managing these relationships proactively prevents conflicts.

---

### **T. Knowledge & Learning Resources**

```yaml
knowledge_base:
  learning_modules:
    - topic: null  # planning_process, building_regs, energy_efficiency, cost_management
      status: null  # not_started, in_progress, completed
      confidence_before: null  # 1-5
      confidence_after: null
      date_started: null
      date_completed: null
      resources_used: []
      notes: null
  
  reference_library:
    - resource_id: null
      title: null
      type: null  # article, video, book, website, podcast, course
      url: null
      filepath: null
      topic: []
      relevance_to_project: null  # high, medium, low
      read_watched: false
      date_consumed: null
      key_takeaways: []
      rating: null  # 1-5
  
  expert_advice_received:
    - date: null
      source: null  # professional, forum, mentor, Aven
      topic: null
      advice: null
      implemented: null
      outcome: null
  
  case_studies:
    - project_name: null
      similarity_to_own: null  # Very similar, somewhat similar, reference only
      lessons_learned: []
      avoided_mistakes: []
      adopted_ideas: []
      source: null
  
  glossary:
    - term: null
      definition: null
      context: null
      related_terms: []
      understood: false

frequently_asked_questions:
  - question: null
    answer: null
    date_asked: null
    still_relevant: true
    answered_by: null  # Aven, professional, research
```

**Why**: Self-build is a **learning journey**. Tracking this helps Aven understand what the user knows and where they need support.

---

### **U. Mental Model & Preferences**

This helps Aven adapt its communication:

```yaml
user_mental_model:
  project_understanding:
    overall_clarity: null  # confused, developing, clear, confident
    knowledge_depth:
      planning: null  # 1-5
      design: null
      construction: null
      costs: null
      programme: null
      regulations: null
  
  decision_making_style:
    approach: null  # analytical, intuitive, collaborative, delegating
    speed: null  # quick, measured, cautious, slow
    risk_tolerance: null  # risk_averse, balanced, adventurous
    information_needs: null  # minimal, moderate, comprehensive
    
  learning_preferences:
    style: null  # visual, written, video, hands_on, mentor_led
    pace: null  # intensive, steady, casual
    depth: null  # overview, moderate, deep_dive
  
  communication_preferences:
    tone: null  # formal, friendly, technical, simplified
    length: null  # brief, moderate, detailed
    examples_needed: true
    warnings_appreciated: true
    encouragement_appreciated: true
  
  interface_preferences:
    dashboard_widgets_priority: []  # What they want to see first
    notification_frequency: null  # real_time, daily, weekly
    mobile_vs_desktop: null
    
  stress_triggers:
    - trigger: null  # budget_concerns, timeline_pressure, decisions_needed
      severity: null  # 1-5
      coping_strategy: null
      support_needed: null
  
  motivation_drivers:
    - driver: null  # family_home, investment, sustainability, creativity
      importance: null  # 1-5

engagement_patterns:
  typical_session_duration: null
  peak_usage_times: []
  most_accessed_features: []
  underutilized_features: []
  
  interaction_style:
    asks_many_questions: null
    prefers_exploration: null
    follows_suggestions: null
    creates_custom_content: null
```

**Why**: This meta-layer helps Aven **personalize** its guidance and interface for each user.

---

### **V. External Integrations & Tools**

Track what other systems are in play:

```yaml
external_systems:
  project_management:
    - tool: null  # MS Project, Asana, Trello, Excel
      used_for: null
      integration_possible: false
      data_sync_frequency: null
  
  financial:
    - tool: null  # Xero, QuickBooks, Excel, bank_app
      used_for: null
      integration_possible: false
  
  design:
    - tool: null  # SketchUp, AutoCAD, Revit, Pinterest
      used_for: null
      file_locations: []
  
  communication:
    - tool: null  # Email, WhatsApp, Slack, MS Teams
      used_for: null
      key_threads: []
  
  file_storage:
    - location: null  # Google Drive, Dropbox, OneDrive, local
      structure: null
      backup_status: null
  
  obsidian:
    vault_path: null
    sync_method: null  # iCloud, Sync, Git, local
    plugins_used: []
    templates: []
    daily_notes: true
    
api_connections:
  planning_portal: false
  building_control_system: false
  mortgage_lender_portal: false
  supplier_accounts: []
  weather_data: false
```

**Why**: Self-builders use **multiple tools**. Understanding this landscape helps Aven position itself and offer integrations.

---

## **Cross-Cutting Enhancements**

### **Add to Multiple Sections:**

#### **Timestamps & Audit Trail**

Add to every major entity:

```yaml
audit:
  created_date: null
  created_by: null
  last_modified_date: null
  last_modified_by: null
  modification_count: null
  version: null
```

#### **Tags & Categorization**

Add to every major entity:

```yaml
tags: []  # Freeform user tags
categories: []  # System categories
labels: []  # Visual labels (red_flag, urgent, watching, completed)
```

#### **Comments & Notes**

Add to every major entity:

```yaml
comments:
  - comment_id: null
    date: null
    author: null
    comment: null
    reply_to: null  # For threading
    resolved: false
    
internal_notes: null  # Private notes not shared with stakeholders
```

#### **Attachments & Media**

Add to every major entity:

```yaml
attachments:
  - attachment_id: null
    filename: null
    filepath: null
    file_type: null
    file_size: null
    uploaded_date: null
    uploaded_by: null
    description: null
    thumbnail: null  # For images
    
photos:
  - photo_id: null
    filepath: null
    taken_date: null
    taken_by: null
    location: null  # GPS or room description
    caption: null
    before_after: null  # before, during, after
    linked_to: []  # tasks, issues, rooms, etc.
```

---

## **Summary of Additional Sections Added**

|Section|Purpose|Key Value|
|---|---|---|
|**L. Programme & Schedule**|Activity-level planning|Tracks dependencies, delays, critical path|
|**M. Materials & Procurement**|Full material lifecycle|Spec → order → delivery → installation|
|**N. Quality Control**|Testing and inspections|Audit trail for compliance and workmanship|
|**O. Variations**|Change order management|Prevents disputes, tracks cost/time impact|
|**P. Commissioning**|Services handover|Ensures systems work as designed|
|**Q. Compliance**|Certification consolidation|Nothing falls through regulatory cracks|
|**R. Meetings & Site Visits**|Interaction tracking|Captures decisions and progress|
|**S. Stakeholder Management**|Relationship management|Proactive conflict prevention|
|**T. Knowledge Base**|Learning tracking|Personalizes guidance|
|**U. User Mental Model**|Personalization layer|Adapts Aven to user's style|
|**V. External Integrations**|Tool landscape|Positions Aven in user's ecosystem|

# Comprehensive Schema Expansion - Final Sections

Let's complete the picture with these remaining critical areas.

---

## **W. Insurance Claims & Incidents**

```yaml
insurance_claims:
  - claim_id: null
    claim_reference: null
    insurance_provider: null
    policy_number: null
    
    incident:
      incident_date: null
      discovered_date: null
      incident_type: null  # theft, vandalism, fire, flood, storm_damage, subsidence, accident
      location: null
      description: null
      
      immediate_actions_taken: []
      emergency_services_called: false
      police_report_reference: null
      
      photos:
        damage_photos: []
        before_photos: []  # If available
        repair_photos: []
      
      witnesses:
        - name: null
          contact: null
          statement: null
    
    damage_assessment:
      affected_areas: []
      extent_of_damage: null  # minor, moderate, severe, total_loss
      safety_implications: null
      immediate_hazards: []
      
      professional_assessment:
        assessor: null
        assessment_date: null
        report: null  # filepath
        
      estimated_repair_cost: null
      estimated_programme_impact: null
    
    claim_process:
      claim_submitted_date: null
      claim_handler: null
      claim_handler_contact: null
      
      excess_payable: null
      
      claim_status: null  # submitted, under_review, approved, rejected, settled, disputed
      
      documentation_submitted:
        - document_type: null
          submission_date: null
          filepath: null
      
      insurer_correspondence:
        - date: null
          direction: null  # sent, received
          summary: null
          filepath: null
      
      loss_adjuster:
        appointed: false
        name: null
        company: null
        visit_date: null
        report_date: null
        findings: null
      
      settlement:
        approved_amount: null
        approval_date: null
        payment_received_date: null
        actual_amount_received: null
        
      dispute:
        disputed: false
        dispute_reason: null
        resolution_method: null  # negotiation, mediation, ombudsman, legal
        outcome: null
    
    remedial_works:
      contractor_appointed: null
      work_start_date: null
      work_completion_date: null
      final_cost: null
      
      quality_check: null
      sign_off_date: null
      
      further_issues: []
    
    impact_on_project:
      programme_delay_days: null
      additional_costs_not_covered: null
      design_changes_required: []
      morale_impact: null
    
    lessons_learned: []
    prevention_measures_implemented: []

incident_register:  # Non-insurance incidents
  - incident_id: null
    date: null
    type: null  # near_miss, damage, injury, complaint, dispute
    severity: null  # low, medium, high, critical
    description: null
    parties_involved: []
    
    immediate_response: null
    investigation_findings: null
    preventative_actions: []
    
    status: null  # open, investigating, resolved, ongoing
    resolution_date: null
```

**Why**: Insurance claims can **paralyze projects**. Detailed tracking ensures nothing is forgotten and claims are processed smoothly. The incident register helps identify patterns and prevent recurrence.

---

## **X. Development & Neighboring Projects**

For plots within larger developments or multiple-plot sites:

```yaml
development_context:
  development_name: null
  developer: null
  total_plots: null
  plot_number: null
  
  development_type: null  # self_build_community, custom_build, conventional_development, isolated_plots
  
  management:
    management_company: null
    management_fee_annual: null
    management_responsibilities: []
    
    residents_association:
      exists: false
      membership_required: false
      contact: null
      meeting_frequency: null
    
  shared_infrastructure:
    access_roads:
      ownership: null  # private, adopted, unadopted
      maintenance_responsibility: null
      contribution_required: null
      road_bond: null
      adoption_status: null
    
    services:
      - service_type: null  # water, sewerage, electricity, gas, broadband
        shared_infrastructure: false
        ownership: null
        maintenance_responsibility: null
        cost_sharing_arrangement: null
    
    amenities:
      - amenity: null  # playground, green_space, parking, communal_building
        ownership: null
        maintenance_responsibility: null
        usage_rights: null
  
  design_controls:
    design_code_exists: false
    design_code_document: null
    architectural_review_required: false
    
    restrictions:
      - restriction_type: null  # materials, colors, building_height, roof_form, fenestration
        requirement: null
        approval_needed_from: null
        
    boundary_treatments_specified: false
    landscaping_requirements: []
    parking_requirements: []
  
  timing_coordination:
    phasing_plan: null
    your_phase: null
    
    restrictions:
      working_hours: null
      noise_limitations: []
      delivery_times: null
      site_access_windows: []
    
  neighboring_plots:
    - plot_number: null
      owner_builder: null
      contact: null
      
      status: null  # not_started, under_construction, completed, occupied
      construction_start_date: null
      construction_completion_date: null
      
      relationship: null  # friendly, neutral, difficult, no_contact
      
      coordination_needed:
        party_wall: false
        shared_access: false
        scaffolding: false
        service_connections: false
        drainage: false
      
      agreements_in_place:
        - agreement_type: null
          agreement_date: null
          key_terms: []
          filepath: null
      
      issues:
        - issue: null
          date_raised: null
          status: null
          resolution: null
      
      opportunities:
        - opportunity: null  # bulk_material_orders, shared_plant_hire, knowledge_sharing
          pursued: false
          outcome: null
  
  community_relations:
    welcome_received: false
    introduced_to_neighbors: false
    
    community_events_attended: []
    
    neighbor_feedback:
      - date: null
        neighbor: null
        feedback_type: null  # compliment, concern, complaint, suggestion
        summary: null
        response: null
        
    dispute_resolution_process: null

serviced_plot_details:
  plot_serviced: false  # Are utilities already connected?
  
  services_included:
    - service: null
      connection_point: null
      capacity: null
      meter_location: null
      service_provider: null
      
  roads_and_access:
    constructed_to_adoptable_standard: false
    surface_type: null
    drainage_installed: false
    street_lighting: false
    
  plot_preparation:
    leveled: false
    topsoil_stripped_stockpiled: false
    drainage_installed: false
    boundaries_marked: false
```

**Why**: Multi-plot developments have **unique coordination challenges**. Design codes, shared infrastructure, and neighbor coordination can make or break a project.

---

## **Y. Utilities Setup & Connections**

```yaml
utilities:
  water_connection:
    provider: null
    
    connection_required: null  # new_connection, upgrade_existing, already_connected
    
    application:
      application_reference: null
      application_date: null
      quote_received: null
      quote_amount: null
      quote_accepted: null
      
    design:
      connection_point: null
      pipe_route: null
      pipe_diameter: null
      meter_location: null
      internal_pipework_responsibility: null  # from meter onwards
      
    installation:
      installation_date: null
      contractor: null
      meter_serial_number: null
      final_connection_date: null
      
    costs:
      quoted: null
      actual: null
      ongoing_charges: null
      
    water_quality:
      testing_required: false
      test_results: null
      treatment_required: false
      treatment_system: null
    
    alternative_if_no_mains:
      system_type: null  # borehole, spring, rainwater_harvesting
      installation_date: null
      capacity: null
      treatment_system: null
      regulations_compliance: null
      ongoing_maintenance: null
      cost: null
  
  sewerage_connection:
    provider: null
    
    connection_type: null  # mains_sewer, septic_tank, sewage_treatment_plant, cesspit
    
    mains_connection:
      application_reference: null
      application_date: null
      quote_amount: null
      
      connection_point: null
      pipe_route: null
      pipe_diameter: null
      pumping_required: false
      
      installation_date: null
      adoption_status: null  # private, to_be_adopted, adopted
      
    alternative_system:
      system_type: null
      capacity: null
      location: null
      
      regulatory:
        environment_agency_permit_required: false
        permit_reference: null
        
      installation:
        installer: null
        installation_date: null
        commissioning_certificate: null
        
      maintenance:
        maintenance_schedule: null
        service_provider: null
        annual_cost: null
        
      costs:
        installation_cost: null
        connection_to_house: null
        ongoing_costs: null
  
  electricity_connection:
    provider: null  # DNO (Distribution Network Operator)
    
    connection_required: null  # new_connection, upgrade_existing, already_connected
    
    supply_type: null  # single_phase, three_phase
    supply_capacity: null  # kVA or Amps
    
    application:
      application_reference: null
      application_type: null  # budget_estimate, formal_application
      application_date: null
      
      connection_offer:
        received_date: null
        connection_charge: null
        timescales: null
        conditions: []
        accepted: null
        
    design:
      connection_point: null
      cable_route: null
      underground_overhead: null
      service_head_location: null
      meter_location: null
      consumer_unit_location: null
      
      reinforcement_required: false  # Network upgrades needed?
      transformer_required: false
      
    temporary_supply:
      required: true
      application_date: null
      installation_date: null
      meter_number: null
      consumption_tracking: []
      disconnection_date: null
      final_cost: null
      
    permanent_connection:
      installation_date: null
      meter_serial_number: null
      energization_date: null
      
      smart_meter: false
      export_meter_required: false  # For renewable generation
      
    costs:
      connection_charge: null
      reinforcement_charge: null
      temporary_supply_cost: null
      actual_total: null
      
    renewable_generation:
      pv_system: false
      export_arrangement: null  # SEG tariff details
      g99_application: false  # Grid connection for generation
  
  gas_connection:
    available: false
    
    provider: null
    
    application:
      application_reference: null
      quote_amount: null
      
    connection_details:
      connection_point: null
      pipe_route: null
      meter_location: null
      installation_date: null
      
    costs:
      connection_charge: null
      actual_cost: null
      
    alternative:
      lpg_tank: false
      tank_location: null
      supplier: null
      installation_cost: null
  
  telecommunications:
    broadband:
      technology: null  # fibre, copper, satellite, 4g_5g
      provider: null
      
      availability:
        checked: false
        available_at_address: false
        available_speeds: null
        
      connection:
        ordered: false
        installation_date: null
        
      infrastructure_works:
        required: false
        description: null
        cost: null
        
    phone_line:
      required: false
      provider: null
      installation_date: null
      
    tv_aerial_satellite:
      type: null  # aerial, satellite, cable, none
      installation_date: null
      
  mobile_signal:
    on_site_signal_strength:
      provider_1: null
      provider_2: null
      provider_3: null
      
    signal_booster_required: false
    booster_type: null
    installation_date: null
    cost: null

utilities_coordination:
  joint_trenching: false  # Multiple services in same trench
  
  ducting_strategy:
    pre_ducting: false
    duct_locations: []
    future_proofing: []
    
  temporary_services_removal:
    - service: null
      removal_date: null
      final_cost: null
      site_reinstatement: null
```

**Why**: Utilities are **critical path items** with long lead times. Poor planning here causes massive delays. This section ensures every connection is tracked from application to commissioning.

---

## **Z. Access & Infrastructure**

For sites requiring access road construction:

```yaml
access_infrastructure:
  access_requirements:
    planning_conditions: []
    highways_approval_required: false
    
  access_road:
    required: true
    length_meters: null
    width_meters: null
    
    design:
      design_standard: null  # adoptable, private_shared, private_sole
      surface_type: null  # tarmac, block_paving, gravel, reinforced_grass
      construction_depth: null
      sub_base_specification: null
      
      drainage:
        surface_water_disposal: null  # soakaway, ditch, mains, attenuation
        drainage_design: null
        suds_required: false
        
      visibility_splays: null
      passing_places_required: false
      
    statutory_approvals:
      highways_approval:
        required: false
        application_date: null
        approval_received: false
        conditions: []
        
      section_38_agreement: false  # Adoption by highways authority
      section_278_agreement: false  # Works on public highway
      
      commuted_sum: null  # Payment for future maintenance if adopted
      road_bond: null  # Financial guarantee during construction
      
    construction:
      contractor: null
      construction_start: null
      construction_completion: null
      
      stages:
        - stage: null  # excavation, sub_base, base_course, surface_course
          completion_date: null
          inspected: false
          approved: false
          
      construction_traffic:
        routing: null
        restrictions: []
        damage_bond: null
        
    costs:
      estimated_cost: null
      actual_cost: null
      shared_costs: false
      cost_split: []
      
    maintenance:
      maintenance_responsibility: null
      maintenance_schedule: null
      winter_maintenance: null
      
  site_access_during_construction:
    temporary_access:
      required: true
      location: null
      construction_date: null
      surface_type: null
      removal_date: null
      reinstatement_cost: null
      
    construction_entrance:
      wheel_wash: false
      road_sweeping_required: false
      signage: []
      
    traffic_management:
      traffic_management_plan: null
      banksman_required: false
      
  parking:
    on_plot_parking:
      spaces_required: null
      spaces_provided: null
      surface_type: null
      ev_charging_point: false
      
    visitor_parking:
      provided: false
      spaces: null
      location: null
      
  pedestrian_access:
    footpath_required: false
    footpath_construction: null
    street_lighting: false
    
  boundaries:
    - boundary_location: null  # front, rear, side
      treatment_type: null  # fence, wall, hedge, railings
      height: null
      material: null
      
      ownership: null
      maintenance_responsibility: null
      
      planning_restrictions: []
      
      construction:
        contractor: null
        installation_date: null
        cost: null
        
  gates_and_barriers:
    required: false
    type: null  # manual, electric, remote_control
    location: null
    installation_date: null
    cost: null

landscaping_and_external_works:
  hard_landscaping:
    - element: null  # driveway, patio, paths, steps, retaining_walls
      location: null
      material: null
      area_or_length: null
      
      design:
        designed_by: null
        structural_calcs_required: false
        
      construction:
        contractor: null
        start_date: null
        completion_date: null
        
      drainage:
        permeable_surface: false
        drainage_connection: null
        
      costs:
        estimated: null
        actual: null
        
  soft_landscaping:
    - element: null  # lawn, planting_beds, trees, hedging
      location: null
      area: null
      
      specification:
        grass_type: null
        topsoil_depth: null
        plants_specified: []
        
      installation:
        contractor: null  # professional, self, mixed
        planting_date: null
        establishment_period: null
        
      maintenance:
        initial_maintenance: null  # Who's responsible?
        watering_system: null
        
      costs:
        estimated: null
        actual: null
        
  external_lighting:
    security_lighting: false
    path_lighting: false
    feature_lighting: false
    
    lights:
      - location: null
        type: null
        pir_sensor: false
        timer: false
        installation_date: null
        
  drainage:
    surface_water:
      strategy: null  # soakaway, attenuation, mains, watercourse
      
      soakaways:
        - location: null
          size: null
          percolation_test_result: null
          construction_date: null
          
      attenuation:
        required: false
        type: null  # tank, pond, permeable_paving
        capacity: null
        location: null
        construction_date: null
        
    foul_drainage:
      # Already covered in utilities section
      
  external_services:
    external_taps: []
    external_power_outlets: []
    irrigation_system: false
```

**Why**: Access infrastructure is often **underestimated** in cost and complexity. This section ensures all off-site works are properly planned and costed.

---

## **AA. Archaeology**

```yaml
archaeology:
  archaeological_potential:
    risk_level: null  # low, medium, high, known_archaeology
    source: null  # HER (Historic Environment Record), survey, planning_officer
    
  desk_based_assessment:
    required: false
    commissioned: false
    archaeologist: null
    assessment_date: null
    findings: null
    filepath: null
    
    recommendations: []
    further_work_required: false
    
  field_evaluation:
    required: false
    method: null  # trial_trenching, geophysical_survey, watching_brief
    
    archaeologist: null
    contractor: null
    evaluation_date: null
    
    discoveries:
      - discovery_type: null  # pottery, building_remains, burial, nothing_significant
        period: null  # prehistoric, roman, medieval, post_medieval
        significance: null  # low, medium, high
        location: null
        photos: []
        
    report:
      report_date: null
      filepath: null
      
    recommendations:
      - recommendation: null
        action_required: null
        cost_implication: null
        programme_implication: null
        
  archaeological_condition:
    planning_condition_exists: false
    condition_reference: null
    condition_text: null
    
    discharge_requirements: []
    
  mitigation_strategy:
    strategy: null  # preservation_in_situ, excavation, watching_brief, none
    
    excavation:
      required: false
      archaeologist: null
      excavation_period: null
      area: null
      
      costs:
        estimated: null
        actual: null
        
      programme_impact_weeks: null
      
    watching_brief:
      required: false
      archaeologist: null
      monitoring_stages: []
      
    finds_management:
      significant_finds: []
      museum_liaison: false
      public_interest: null
      
  heritage_assets:
    - asset_type: null  # scheduled_monument, listed_building, conservation_area
      significance: null
      constraints: []
      specialist_required: false
      
  costs:
    desk_based_assessment: null
    field_evaluation: null
    excavation: null
    monitoring: null
    reporting: null
    total: null
```

**Why**: Archaeological requirements can **unexpectedly halt construction**. Early identification and budgeting prevents nasty surprises.

---

## **AB. Listed Building & Heritage**

```yaml
listed_building:
  listing_status:
    listed: false
    grade: null  # I, II*, II
    listing_date: null
    listing_reference: null
    listing_description: null
    
  conservation_area:
    within_conservation_area: false
    conservation_area_name: null
    character_appraisal: null
    design_guide: null
    
  heritage_significance:
    age: null
    architectural_interest: null
    historical_interest: null
    group_value: null
    
    key_features:
      - feature: null  # roof_structure, windows, interior_features, setting
        significance: null  # high, medium, low
        condition: null
        proposed_treatment: null
        
  heritage_statement:
    required: true
    prepared_by: null
    submission_date: null
    filepath: null
    
    assessment:
      impact_on_significance: null  # none, minor, moderate, major
      justification: null
      mitigation: null
      
  listed_building_consent:
    required: true
    application_reference: null
    submission_date: null
    determination_date: null
    approved: null
    conditions: []
    
  specialist_consultants:
    conservation_architect:
      appointed: false
      name: null
      firm: null
      
    structural_engineer_heritage_experience:
      appointed: false
      name: null
      
    historic_building_consultant:
      appointed: false
      name: null
      
  works_methodology:
    - element: null  # roof_repair, window_restoration, wall_treatment
      traditional_materials_required: true
      traditional_techniques_required: true
      
      materials_specification:
        material: null
        source: null
        specification: null
        samples_required: false
        approved: false
        
      craftspeople:
        trade: null  # stone_mason, lime_plasterer, joiner
        craftsperson: null
        qualifications: []
        
      supervision_required: null  # architect, conservation_officer, specialist
      
  historic_england_involvement:
    grade_i_or_ii_star: false
    consultation_required: false
    advice_received: null
    
  recording_requirements:
    photographic_record:
      required: false
      level: null  # basic, detailed, comprehensive
      completed: false
      filepath: null
      
    drawn_record:
      required: false
      measured_survey: false
      completed: false
      
  monitoring:
    conservation_officer_visits:
      - visit_date: null
        findings: null
        actions_required: []
        
  grant_funding:
    - grant_scheme: null  # HLF, local_authority, charitable_trust
      application_submitted: false
      amount_requested: null
      amount_awarded: null
      conditions: []
      
  costs:
    specialist_fees: null
    traditional_materials_premium: null
    traditional_techniques_premium: null
    grant_income: null
    net_additional_cost: null
```

**Why**: Listed building work is **heavily regulated** and requires specialist skills. This section ensures compliance and manages the unique challenges.

---

## **AC. Self-Build Mortgage & Finance**

```yaml
self_build_mortgage:
  lender: null
  mortgage_reference: null
  mortgage_type: null  # arrears_stage_release, advance_stage_release
  
  terms:
    total_loan_amount: null
    loan_to_value_percent: null
    interest_rate: null
    term_years: null
    monthly_payment: null
    
    land_element: null
    build_element: null
    
  stage_releases:
    number_of_stages: null  # Typically 4-6
    
    stages:
      - stage_number: null
        stage_name: null  # land_purchase, foundations, watertight, first_fix, second_fix, completion
        percentage_of_build_cost: null
        amount: null
        
        release_criteria: []
        
        inspection:
          inspection_required: true
          inspector: null  # lender_surveyor, architect, monitoring_surveyor
          inspection_date: null
          inspection_passed: null
          inspection_report: null
          
          re_inspection:
            required: false
            reason: null
            date: null
            passed: null
            
        release:
          application_date: null
          approved_date: null
          funds_released_date: null
          amount_released: null
          retention_held: null
          
        timing:
          planned_date: null
          actual_date: null
          delay_days: null
          delay_reason: null
          
  bridging_finance:
    required: false
    lender: null
    amount: null
    term_months: null
    interest_rate: null
    repayment_date: null
    
  monitoring_surveyor:
    appointed_by: null  # lender, self
    name: null
    firm: null
    fee_structure: null
    
    reports_submitted: []
    
  insurance_requirements:
    buildings_insurance: null
    life_insurance: null
    income_protection: null
    
  financial_monitoring:
    cost_vs_budget_tolerance: null  # Lender's acceptable variance
    programme_vs_schedule_tolerance: null
    
    alerts:
      - alert_type: null  # over_budget, behind_schedule, quality_concern
        raised_date: null
        lender_notified: false
        resolution: null
        
  completion:
    final_valuation: null
    final_valuation_date: null
    conversion_to_standard_mortgage: null
    conversion_date: null

other_funding:
  savings:
    total_available: null
    drawdown_schedule: []
    current_balance: null
    
  family_loans:
    - lender: null
      amount: null
      interest_rate: null
      repayment_terms: null
      legal_agreement: false
      
  equity_release:
    property_released_from: null
    amount: null
    
  grants:
    - grant_name: null
      provider: null
      amount: null
      conditions: []
      claimed: false
      
  director_loans:  # If building through a company
    - amount: null
      date: null
      repayment_date: null

financial_contingency_strategy:
  contingency_fund_location: null  # savings, credit_facility, sale_of_assets
  trigger_points_for_use: []
  replenishment_plan: null
```

**Why**: Self-build mortgages are **complex and stage-dependent**. Missing an inspection or release can halt work. This section keeps the financial machinery moving.

---

## **AD. Tools, Equipment & Plant**

```yaml
tools_and_equipment:
  owned_tools:
    - tool: null
      purchase_date: null
      purchase_cost: null
      condition: null
      maintenance_due: null
      location: null  # on_site, home, storage
      insurance_value: null
      
  hired_equipment:
    - equipment: null  # scaffolding, excavator, dumper, mixer, generator
      supplier: null
      
      hire_period:
        start_date: null
        planned_return_date: null
        actual_return_date: null
        extension_charges: null
        
      costs:
        daily_weekly_rate: null
        delivery_charge: null
        collection_charge: null
        damage_waiver: null
        fuel_charge: null
        total_cost: null
        
      operator:
        operated_by: null  # self, hired_with_operator, subcontractor
        operator_qualification_verified: false
        
      usage_log:
        - date: null
          hours_used: null
          task: null
          
      condition_report:
        collection_condition: null
        return_condition: null
        damage_charges: null
        
  plant_on_site:
    current_equipment: []
    
  specialist_equipment:
    - equipment: null  # crane, piling_rig, concrete_pump
      required_for: null
      hire_date: null
      supplier: null
      cost: null
      
  site_facilities:
    site_cabin:
      provided: false
      type: null  # hired, owned, converted_container
      facilities: []  # desk, heating, power, toilet
      monthly_cost: null
      
    welfare_facilities:
      toilet: false
      water_supply: false
      first_aid_kit: true
      mess_area: false
      
    security_equipment:
      - equipment: null  # fence, alarm, camera, security_guard
        supplier: null
        installation_date: null
        monthly_cost: null
        
  ppe_and_safety:
    ppe_provided:
      - item: null  # hard_hat, hi_vis, boots, gloves, goggles
        quantity: null
        cost: null
        
    safety_equipment:
      - equipment: null  # barriers, signs, fire_extinguisher, first_aid
        location: null
        inspection_due: null

equipment_strategy:
  buy_vs_hire_decisions:
    - decision: null
      rationale: null
      cost_comparison: null
      
  bulk_hire_opportunities:
    - opportunity: null
      potential_saving: null
      coordinated_with: []
```

**Why**: Tool and plant costs can **spiral out of control**. Tracking what's hired, when, and for how long prevents waste. Shared hire with neighbors can save significantly.

---

## **AE. Site Security & Loss Prevention**

```yaml
site_security:
  security_strategy:
    risk_assessment:
      crime_rate_in_area: null
      site_visibility: null  # highly_visible, moderate, isolated
      value_of_materials_on_site: null
      risk_level: null  # low, medium, high, very_high
      
    security_measures:
      - measure: null  # fencing, lighting, cameras, alarm, security_guard
        installed: false
        cost: null
        effectiveness: null
        
  physical_security:
    perimeter_fencing:
      type: null  # heras_fencing, hoarding, none
      height: null
      installation_date: null
      removal_date: null
      condition_checks: []
      
    gates_and_locks:
      - location: null
        lock_type: null
        key_holders: []
        
    lighting:
      security_lighting_installed: false
      motion_activated: false
      timer: false
      
    secure_storage:
      - container_type: null
        contents: []
        lock_type: null
        location: null
        
  electronic_security:
    cctv:
      installed: false
      number_of_cameras: null
      recording: false
      monitored: false
      signage_displayed: false
      
    alarm_system:
      installed: false
      type: null  # bells_only, monitored
      monitoring_company: null
      
    gps_tracking:
      tools_tracked: []
      
  access_control:
    authorized_personnel: []
    
    visitor_log:
      - date: null
        visitor: null
        purpose: null
        time_in: null
        time_out: null
        
    key_register:
      - key_holder: null
        keys_held: []
        issued_date: null
        returned_date: null
        
  insurance:
    tools_and_materials_insured: true
    policy_excess: null
    security_requirements: []
    
  incident_response:
    emergency_contacts: []
    
    incident_procedure:
      discovery: null
      notification: []
      documentation: null
      
  theft_vandalism_log:
    - incident_id: null
      incident_date: null
      discovered_date: null
      incident_type: null  # theft, attempted_theft, vandalism, trespass, arson
      
      items_stolen:
        - item: null
          description: null
          serial_number: null
          value: null
          recoverable: null
          
      damage_caused:
        - area: null
          description: null
          repair_cost: null
          
      security_breach:
        method_of_entry: null
        security_weaknesses_identified: []
        
      reporting:
        police_notified: false
        crime_reference: null
        insurance_claim_made: false
        claim_reference: null
        
      investigation:
        police_visit: false
        evidence_collected: []
        suspects_identified: false
        outcome: null
        
      preventative_actions:
        - action: null
          implemented: false
          cost: null
          
      impact:
        programme_delay_days: null
        financial_loss: null
        morale_impact: null
        
  neighbourhood_watch:
    neighbours_informed: false
    neighbours_contact_details: []
    mutual_site_watching: false
    
  contractor_security_requirements:
    - contractor: null
      security_responsibilities: []
      equipment_security: null
      end_of_day_procedures: []
      
site_management:
  site_tidiness:
    tidiness_standard: null  # high, moderate, basic
    
    waste_management:
      skip_provider: null
      skip_size: null
      collection_frequency: null
      
      waste_segregation: false
      recycling_targets: []
      
      hazardous_waste:
        - waste_type: null
          quantity: null
          disposal_method: null
          disposal_certificate: null
          
    material_storage:
      organized: null
      weather_protection: null
      stock_control_method: null
      
  signage:
    - sign_type: null  # site_name, safety, prohibitory, directional
      location: null
      installed: false
      
  environmental_management:
    noise_monitoring: false
    dust_suppression: false
    pollution_prevention: []
    
    complaints_log:
      - date: null
        complainant: null
        complaint_type: null  # noise, dust, traffic, hours
        action_taken: null
        resolution: null
```

---

## **AF. Weather Impact & Environmental Monitoring**

```yaml
weather_monitoring:
  weather_station:
    on_site_monitoring: false
    weather_station_type: null  # professional, app_based, visual_observation
    data_source: null
    
  historical_weather_data:
    location: null
    data_source: null  # Met Office, local_station
    
    seasonal_patterns:
      wettest_months: []
      driest_months: []
      coldest_months: []
      typical_frost_dates: null
      typical_ground_conditions: []
      
  daily_weather_log:
    - date: null
      temperature_high: null
      temperature_low: null
      
      conditions: null  # dry, light_rain, heavy_rain, snow, frost, ice, fog, wind
      wind_speed: null
      
      ground_conditions: null  # dry, damp, wet, waterlogged, frozen, snow_covered
      
      work_impact: null  # no_impact, slowed, stopped, damage_risk
      
      activities_affected: []
      
      protective_measures_taken: []
      
      photos: []
      
  weather_related_delays:
    - delay_start_date: null
      delay_end_date: null
      total_days: null
      
      weather_type: null  # rain, snow, frost, high_winds, extreme_heat
      
      activities_stopped: []
      
      programme_impact:
        critical_path_affected: false
        recovery_plan: null
        
      cost_impact:
        standing_time_charges: null
        remedial_work_cost: null
        additional_protection_cost: null
        
  weather_protection_measures:
    - measure: null  # scaffold_sheeting, temporary_roof, heated_enclosure, frost_protection
      installed_date: null
      removed_date: null
      cost: null
      effectiveness: null
      
  weather_related_damage:
    - incident_date: null
      damage_type: null  # wind_damage, water_ingress, frost_damage, uv_degradation
      affected_area: null
      description: null
      
      immediate_actions: []
      
      repair_required:
        description: null
        contractor: null
        cost: null
        completion_date: null
        
      insurance_claim: false
      
      prevention_for_future: []
      
  seasonal_planning:
    winter_working_strategy:
      heating_provision: null
      frost_protection: null
      material_storage: null
      programme_adjustments: []
      
    summer_working:
      heat_stress_management: null
      uv_protection: null
      concrete_curing_strategy: null
      
    monsoon_typhoon_season:  # If applicable
      preparation: null
      emergency_procedures: null

environmental_conditions:
  ground_conditions_monitoring:
    - date: null
      location: null
      description: null
      water_table_level: null
      bearing_capacity: null
      issues: []
      
  ecology_monitoring:
    breeding_season_constraints:
      - species: null
        constraint_period: null
        work_restrictions: []
        
    ecological_clerk_of_works:
      appointed: false
      name: null
      visits: []
      
    protected_species_incidents:
      - date: null
        species: null
        action_taken: null
        statutory_body_notified: false
        
  pollution_incidents:
    - incident_date: null
      incident_type: null  # fuel_spill, concrete_washout, chemical_release, sediment_runoff
      location: null
      quantity: null
      
      containment:
        immediate_action: null
        effectiveness: null
        
      reporting:
        environment_agency_notified: false
        incident_reference: null
        
      remediation:
        action_taken: null
        cost: null
        completion_date: null
        
      prevention:
        measures_implemented: []
        
  noise_complaints:
    - date: null
      complainant: null
      time_of_day: null
      activity_causing_noise: null
      
      investigation: null
      action_taken: null
      follow_up: null
      
  dust_complaints:
    - date: null
      complainant: null
      source: null
      
      mitigation_implemented: []
      effectiveness: null
```

**Why**: Weather is the **silent programme killer**. Documenting weather impacts creates evidence for extension of time claims and helps with future planning. Environmental monitoring prevents regulatory breaches.

---

## **AG. Lessons Learned & Project Reflection**

```yaml
lessons_learned:
  continuous_capture:
    - date: null
      phase: null  # planning, design, procurement, construction
      category: null  # what_went_well, challenge_overcome, mistake_made, near_miss
      
      description: null
      
      root_cause: null
      
      impact:
        cost: null
        time: null
        quality: null
        stress_level: null
        
      what_would_do_differently: null
      
      advice_for_others: null
      
      preventable: null  # yes, no, partially
      
      key_learning: null
      
  post_project_review:
    review_date: null
    participants: []
    
    overall_assessment:
      project_success_rating: null  # 1-10
      would_do_it_again: null
      
      timeline:
        planned_duration: null
        actual_duration: null
        variance_weeks: null
        main_causes_of_delay: []
        
      budget:
        original_budget: null
        final_cost: null
        variance_percent: null
        main_causes_of_overspend: []
        best_value_decisions: []
        poor_value_decisions: []
        
      quality:
        overall_quality_satisfaction: null  # 1-10
        best_workmanship: []
        poor_workmanship: []
        things_to_rectify: []
        
      design:
        design_satisfaction: null  # 1-10
        design_changes_during_build: null
        things_that_work_well: []
        things_that_dont_work: []
        would_design_differently: []
        
      relationships:
        architect_relationship: null  # 1-10
        contractor_relationships: []
        supplier_relationships: []
        neighbour_relationships: null
        family_relationship_impact: null
        
      personal_impact:
        stress_level_overall: null  # 1-10
        health_impact: null
        work_life_balance_impact: null
        relationship_impact: null
        
        personal_growth: []
        skills_learned: []
        
      sustainability_performance:
        energy_performance: null
        sustainability_goals_achieved: []
        sustainability_goals_compromised: []
        
    top_successes:
      - success: null
        why_it_worked: null
        
    biggest_challenges:
      - challenge: null
        how_overcome: null
        cost_of_challenge: null
        
    biggest_regrets:
      - regret: null
        why_regret: null
        avoidable: null
        
    surprises:
      - surprise: null
        pleasant_unpleasant: null
        how_handled: null
        
    professional_team_assessment:
      - professional: null
        role: null
        performance_rating: null  # 1-10
        strengths: []
        weaknesses: []
        would_use_again: null
        would_recommend: null
        
    contractor_subcontractor_assessment:
      - contractor: null
        trade: null
        performance_rating: null
        strengths: []
        weaknesses: []
        would_use_again: null
        would_recommend: null
        
    product_supplier_assessment:
      - supplier_product: null
        category: null
        performance_rating: null
        quality: null
        value: null
        service: null
        would_use_again: null
        would_recommend: null
        
  knowledge_sharing:
    willing_to_mentor: false
    willing_to_share_story: false
    
    blog_vlog_created: false
    open_house_held: false
    
    recommendations_for_future_self_builders:
      - recommendation: null
        priority: null  # critical, important, nice_to_know
        
  project_archive:
    archive_method: null  # digital, physical, both
    
    documents_archived:
      planning_documents: false
      building_control_documents: false
      drawings_and_specifications: false
      contracts: false
      certificates: false
      warranties: false
      photographs: false
      correspondence: false
      financial_records: false
      
    archive_location: null
    backup_location: null
    
    handover_documentation_complete: false
```

**Why**: Capturing lessons learned **in real-time** creates a valuable archive. Post-project reflection helps future self-builders and provides closure for the user.

---

## **AH. Post-Occupancy Experience**

```yaml
post_occupancy:
  move_in:
    move_in_date: null
    
    initial_impressions:
      excitement_level: null  # 1-10
      concerns: []
      immediate_issues: []
      
    settling_in_period:
      adjustment_challenges: []
      unexpected_delights: []
      
  living_experience:
    - assessment_date: null
      time_since_move_in: null  # months
      
      overall_satisfaction: null  # 1-10
      
      spatial_experience:
        room_sizes_adequate: null
        layout_works_well: null
        storage_adequate: null
        flow_between_spaces: null
        
      comfort:
        thermal_comfort_winter: null  # 1-10
        thermal_comfort_summer: null
        overheating_issues: false
        cold_spots: []
        draughts: []
        
        acoustic_comfort: null  # 1-10
        noise_issues: []
        
        daylight_quality: null  # 1-10
        dark_areas: []
        glare_issues: []
        
        air_quality: null  # 1-10
        ventilation_adequate: null
        condensation_issues: []
        
      functionality:
        kitchen_layout: null  # 1-10
        bathroom_functionality: null
        storage_functionality: null
        circulation_space: null
        
      systems_performance:
        heating_system_satisfaction: null  # 1-10
        heating_system_issues: []
        running_costs_acceptable: null
        
        hot_water_performance: null
        hot_water_issues: []
        
        ventilation_system_satisfaction: null
        ventilation_issues: []
        
        electrical_system_satisfaction: null
        electrical_issues: []
        
        plumbing_satisfaction: null
        plumbing_issues: []
        
      energy_performance:
        heating_bills: []  # Monthly tracking
        electricity_bills: []
        water_bills: []
        
        renewable_generation: []  # If applicable
        
        compared_to_predictions:
          better_worse_as_expected: null
          variance_percent: null
          
      maintenance_issues:
        - issue: null
          first_noticed: null
          severity: null
          
          warranty_claim: false
          
          resolution:
            resolved: false
            resolution_date: null
            cost: null
            satisfactory: null
            
      design_modifications_desired:
        - modification: null
          reason: null
          priority: null
          estimated_cost: null
          planned_date: null
          
  neighbors_and_community:
    neighborhood_integration:
      feel_part_of_community: null
      relationships_with_neighbors: null
      
    community_feedback_on_build:
      received_compliments: []
      received_criticism: []
      
  visitors_feedback:
    - visitor: null
      comments: null
      favorite_features: []
      criticisms: []
      
  would_you_do_it_again:
    answer: null  # definitely, probably, unsure, probably_not, definitely_not
    reasoning: null
    
    what_would_need_to_change: []
    
  long_term_satisfaction:
    one_year_review:
      date: null
      overall_satisfaction: null
      has_met_expectations: null
      
    three_year_review:
      date: null
      overall_satisfaction: null
      significant_changes: []
      
    five_year_review:
      date: null
      overall_satisfaction: null
      would_still_build_same_design: null
```

**Why**: Post-occupancy evaluation closes the loop. It reveals the **performance gap** between design intent and lived reality, informing future projects and Aven's guidance.

---

## **AI. Self-Build Community & Peer Network**

```yaml
community_connections:
  self_build_groups:
    - group_name: null
      type: null  # online_forum, local_group, national_organization
      joined_date: null
      active_member: null
      
      value_gained:
        advice: []
        supplier_recommendations: []
        cost_comparisons: []
        moral_support: null
        
      contributions_made: []
      
  online_presence:
    blog_vlog:
      exists: false
      url: null
      started_date: null
      posting_frequency: null
      audience_size: null
      
    social_media:
      - platform: null  # instagram, youtube, facebook, twitter
        handle: null
        follower_count: null
        content_type: null  # progress_updates, tips, showcase
        
  peer_support:
    mentor_relationships:
      - mentor_name: null
        expertise: null
        how_met: null
        frequency_of_contact: null
        value_rating: null  # 1-10
        
    peer_comparisons:
      - peer_project: null
        similarities: []
        useful_comparisons: []
        lessons_adopted: []
        
  knowledge_sharing_contributions:
    forums_posts: null  # Number of posts
    questions_answered: null
    case_study_shared: false
    open_day_held: false
    
    helping_others:
      - person_helped: null
        nature_of_help: null
        outcome: null
        
  networking_events:
    - event_name: null
      date: null
      type: null  # self_build_show, local_meetup, webinar, site_visit
      key_contacts_made: []
      suppliers_discovered: []
      ideas_gained: []

reputation_building:
  local_recognition:
    featured_in_media: []
    awards_won: []
    speaking_engagements: []
    
  becoming_an_expert:
    topics_of_expertise: []
    willing_to_advise_others: false
```

**Why**: Self-build is a **community endeavor**. Tracking connections and knowledge-sharing helps users build support networks and contributes to the wider self-build community.

---

## **AJ. Legal Disputes & Formal Complaints**

```yaml
legal_matters:
  disputes:
    - dispute_id: null
      dispute_date: null
      
      parties:
        - party_name: null
          role: null  # contractor, architect, supplier, neighbour, local_authority
          
      nature_of_dispute: null  # payment, quality, delay, contract_interpretation, breach
      
      value_in_dispute: null
      
      timeline:
        issue_first_raised: null
        formal_complaint_date: null
        mediation_attempted: null
        litigation_commenced: null
        resolution_date: null
        
      resolution_attempts:
        - method: null  # negotiation, mediation, adjudication, arbitration, litigation
          date: null
          outcome: null
          cost: null
          
      current_status: null  # ongoing, resolved, abandoned, in_litigation
      
      legal_representation:
        solicitor: null
        firm: null
        costs_to_date: null
        
      outcome:
        resolution: null
        financial_settlement: null
        who_bore_costs: null
        relationship_aftermath: null
        
      lessons_learned: []
      
      impact:
        programme_delay: null
        cost_impact: null
        stress_impact: null  # 1-10
        
  formal_complaints:
    - complaint_id: null
      complaint_date: null
      
      complained_to: null  # professional_body, ombudsman, trading_standards, local_authority
      
      subject_of_complaint: null  # person or organization
      
      nature_of_complaint: null
      
      complaint_process:
        acknowledgment_date: null
        investigation_period: null
        outcome_date: null
        
      outcome: null  # upheld, partially_upheld, not_upheld
      
      remedy:
        compensation: null
        apology: null
        corrective_action: []
        
  professional_negligence:
    claim_made: false
    
    professional: null
    nature_of_negligence: null
    
    professional_indemnity_claim:
      notification_date: null
      insurer: null
      claim_reference: null
      status: null
      
  party_wall_disputes:
    - neighbour: null
      issue: null
      surveyor_appointed: null
      award_issued: null
      outcome: null
      
  planning_appeals:
    # Already covered in planning section
    
  building_control_disputes:
    - issue: null
      date_raised: null
      resolution_process: null
      outcome: null

adjudication:
  adjudication_commenced: false
  
  adjudicator: null
  referral_date: null
  decision_date: null
  decision: null
  
  enforcement: null
  costs_awarded: null

alternative_dispute_resolution:
  mediation_sessions:
    - session_date: null
      mediator: null
      parties: []
      outcome: null
      
  expert_determination:
    expert: null
    matter_referred: null
    determination: null
```

**Why**: Disputes are **stressful and expensive**. Documenting them protects legal position and helps identify patterns. Most importantly, it helps other self-builders avoid similar pitfalls.

---

## **AK. Personal & Family Impact**

```yaml
personal_wellbeing:
  health_tracking:
    physical_health:
      - date: null
        health_status: null  # excellent, good, fair, poor
        issues: []  # back_pain, fatigue, injury, illness
        related_to_project: null
        
    mental_health:
      - date: null
        stress_level: null  # 1-10
        anxiety_level: null  # 1-10
        mood: null  # positive, neutral, low, depressed
        
        stressors:
          - stressor: null
            severity: null  # 1-10
            
        coping_mechanisms: []
        
        professional_support:
          sought: false
          type: null  # counseling, therapy, medication, coaching
          helpful: null
          
    sleep_quality:
      - date: null
        quality: null  # 1-10
        hours: null
        project_related_sleep_issues: false
        
  work_life_balance:
    - period: null  # month or quarter
      balance_rating: null  # 1-10
      
      time_allocation:
        paid_work: null  # hours per week
        project_management: null
        on_site_work: null
        research_admin: null
        family_time: null
        personal_time: null
        
      sacrifices_made: []
      
      career_impact:
        time_off_work: null
        reduced_hours: false
        career_progression_affected: null
        income_impact: null
        
  relationship_impact:
    partner_relationship:
      - assessment_date: null
        relationship_health: null  # 1-10
        
        project_impact: null  # strengthened, neutral, strained, damaged
        
        sources_of_tension: []
        
        coping_strategies: []
        
        decision_making_dynamics: null
        
        quality_time_together: null  # sufficient, barely_enough, insufficient
        
    children_impact:
      - child: null
        age: null
        
        how_affected: []  # reduced_time, house_move, school_change, excitement, stress
        
        involvement_in_project: null
        
        positive_experiences: []
        negative_experiences: []
        
    extended_family:
      support_received: []
      tension_caused: []
      relationship_changes: []
      
  social_life:
    - period: null
      social_activity_level: null  # 1-10
      friendships_affected: []
      social_events_missed: []
      new_connections_made: []
      
  personal_growth:
    skills_developed:
      - skill: null
        confidence_level: null  # 1-10
        how_learned: null
        
    confidence_changes:
      - area: null  # decision_making, technical_knowledge, negotiation, project_management
        before: null  # 1-10
        after: null
        
    identity_changes:
      changed_self_perception: []
      others_perception_changed: []
      
    pride_and_achievement:
      moments_of_pride: []
      sense_of_accomplishment: null  # 1-10
      
  lifestyle_adjustments:
    living_arrangements_during_build:
      arrangement: null  # staying_in_existing_home, renting, with_family, caravan_on_site
      start_date: null
      end_date: null
      
      challenges: []
      cost: null
      
    commute_to_site:
      distance: null
      time: null
      frequency: null
      cost: null
      
  financial_stress:
    - date: null
      stress_level: null  # 1-10
      causes: []
      impact_on_daily_life: null
      
  regret_and_doubt:
    moments_of_regret:
      - date: null
        what_triggered: null
        severity: null  # 1-10
        how_overcome: null
        
    questioning_decision:
      - date: null
        contemplated_abandoning: false
        what_kept_going: null
        
  support_systems:
    - support_type: null  # family, friends, professional, community, spiritual
      effectiveness: null  # 1-10
      
  advice_for_future_self_builders_on_wellbeing:
    - advice: null
      importance: null  # critical, important, useful
```

**Why**: Self-build affects **every aspect of life**. Tracking wellbeing helps users recognize warning signs and seek help. It also creates a realistic picture for future self-builders about the personal cost of the journey.

---

## **AL. Project Metrics & Analytics**

```yaml
project_metrics:
  key_performance_indicators:
    timeline_performance:
      original_duration_weeks: null
      actual_duration_weeks: null
      variance_weeks: null
      variance_percent: null
      performance_rating: null  # ahead, on_time, slightly_delayed, significantly_delayed
      
    budget_performance:
      original_budget: null
      final_cost: null
      variance_amount: null
      variance_percent: null
      performance_rating: null  # under_budget, on_budget, slightly_over, significantly_over
      
    quality_performance:
      snagging_items: null
      major_defects: null
      building_control_failures: null
      overall_quality_rating: null  # 1-10
      
    safety_performance:
      reportable_incidents: null
      near_misses: null
      safety_days_lost: null
      safety_rating: null  # excellent, good, adequate, poor
      
    sustainability_performance:
      epc_rating_target: null
      epc_rating_actual: null
      renewable_energy_target: null
      renewable_energy_actual: null
      sustainability_rating: null  # 1-10
      
  productivity_metrics:
    average_build_rate_sqm_per_week: null
    
    stage_durations:
      - stage: null
        planned_duration_weeks: null
        actual_duration_weeks: null
        variance: null
        
  cost_metrics:
    cost_per_sqm: null
    cost_per_sqm_vs_local_average: null
    
    cost_breakdown_percentages:
      land: null
      groundworks: null
      structure: null
      external_envelope: null
      internal_finishes: null
      services: null
      external_works: null
      professional_fees: null
      contingency_used: null
      
    value_engineering_savings: null
    
    variations_cost_impact: null
    variations_as_percent_of_original: null
    
  decision_metrics:
    total_decisions_made: null
    average_confidence_level: null
    decisions_reversed: null
    decisions_regretted: null
    
  stakeholder_satisfaction:
    client_satisfaction: null  # 1-10
    partner_satisfaction: null
    architect_satisfaction: null
    contractor_satisfaction: null
    
  change_metrics:
    design_changes: null
    specification_changes: null
    programme_changes: null
    budget_revisions: null
    
  efficiency_metrics:
    meetings_held: null
    average_meeting_duration: null
    decisions_per_meeting: null
    
    rework_instances: null
    rework_cost: null
    
  communication_metrics:
    emails_sent_received: null
    site_visits: null
    formal_reports: null
    
  benchmark_comparisons:
    - benchmark_source: null  # RICS, BCIS, local_data, peer_projects
      metric: null
      your_project: null
      benchmark: null
      variance: null

analytics_insights:
  critical_success_factors:
    - factor: null
      impact: null  # high, medium, low
      
  critical_failure_points:
    - point: null
      impact: null
      how_avoided_or_overcome: null
      
  cost_drivers:
    - driver: null
      percentage_of_total: null
      
  time_consumers:
    - activity: null
      weeks_consumed: null
      percentage_of_total: null
      
  recurring_issues:
    - issue: null
      frequency: null
      cumulative_impact: null
      
  best_investments:
    - investment: null
      cost: null
      value_returned: null
      
  worst_investments:
    - investment: null
      cost: null
      value_returned: null
      reason_for_poor_return: null
```

**Why**: Metrics provide **objective analysis** of performance. They help identify patterns, justify decisions, and provide benchmarks for future projects. This is gold for AI-driven insights.

---

## **AM. Future Plans & Ongoing Development**

```yaml
future_development:
  planned_improvements:
    - improvement: null
      category: null  # internal, external, systems, landscaping
      priority: null  # immediate, short_term, medium_term, long_term, wishlist
      
      description: null
      estimated_cost: null
      estimated_duration: null
      
      dependencies: []
      
      planning_permission_required: null
      
      planned_start_date: null
      
      status: null  # idea, planned, approved, in_progress, completed, abandoned
      
  maintenance_schedule:
    - item: null
      frequency: null  # annual, bi_annual, five_yearly, ten_yearly
      responsibility: null  # self, contractor, manufacturer
      next_due_date: null
      cost_per_instance: null
      
  warranty_expiry_tracking:
    - item: null
      warranty_duration: null
      expiry_date: null
      action_before_expiry: null
      
  long_term_aspirations:
    - aspiration: null
      timeframe: null
      feasibility: null
      
  property_value_tracking:
    - valuation_date: null
      valuation_method: null  # estate_agent, surveyor, online_estimate
      estimated_value: null
      equity: null
      
  potential_sale_or_rental:
    intention: null  # forever_home, sell_in_5_years, potential_rental
    
    if_selling:
      target_sale_date: null
      expected_value: null
      expected_profit: null
      
    if_renting:
      target_rental_income: null
      rental_yield: null
      
  second_project_consideration:
    would_self_build_again: null
    what_would_do_differently: []
    timeline_for_next_project: null
```

**Why**: The project doesn't end at move-in. Tracking future plans, maintenance, and lessons positions the user for ongoing success and potential future projects.

---

## **Cross-Schema Relationship Map**

To make this database truly powerful, add explicit relationship tables:

```yaml
relationships:
  room_to_cost:
    - room_id: null
      cost_item_ids: []
      total_cost: null
      
  room_to_tasks:
    - room_id: null
      task_ids: []
      
  room_to_materials:
    - room_id: null
      material_ids: []
      
  decision_to_cost:
    - decision_id: null
      cost_impact: null
      cost_item_ids: []
      
  decision_to_risk:
    - decision_id: null
      risk_ids: []
      
  decision_to_variation:
    - decision_id: null
      variation_ids: []
      
  risk_to_mitigation:
    - risk_id: null
      mitigation_action_ids: []
      cost_of_mitigation: null
      
  task_to_dependencies:
    - task_id: null
      predecessor_task_ids: []
      successor_task_ids: []
      
  professional_to_stages:
    - professional_id: null
      stage_ids: []
      
  supplier_to_materials:
    - supplier_id: null
      material_ids: []
      
  incident_to_insurance_claim:
    - incident_id: null
      claim_id: null
      

  variation_to_cost_and_time:
    - variation_id: null
      cost_impact: null
      time_impact_days: null
      cost_item_ids: []
      task_ids_affected: []
      
  inspection_to_tasks:
    - inspection_id: null
      task_ids: []
      tasks_blocked_until_passed: []
      
  meeting_to_decisions:
    - meeting_id: null
      decision_ids: []
      
  meeting_to_actions:
    - meeting_id: null
      action_item_ids: []
      
  stakeholder_to_decisions:
    - stakeholder_id: null
      decision_ids: []
      influence_level: null
      
  knowledge_gap_to_learning_resource:
    - knowledge_gap_id: null
      resource_ids: []
      gap_filled: false
      
  weather_event_to_delay:
    - weather_event_id: null
      delay_id: null
      activity_ids_affected: []
      
  quality_issue_to_snagging:
    - quality_issue_id: null
      snagging_item_ids: []
      
  design_choice_to_building_reg:
    - design_choice_id: null
      building_reg_part: null  # Part A, Part L, etc.
      compliance_status: null
      
  supplier_to_delay:
    - supplier_id: null
      delay_ids: []
      delivery_reliability_score: null
      
  contractor_to_quality_issues:
    - contractor_id: null
      quality_issue_ids: []
      quality_score: null  # 1-10
      
  document_to_entities:
    - document_id: null
      linked_entity_type: null  # room, task, decision, cost, risk
      linked_entity_ids: []
```

---

## **AN. Document Management & Version Control**

```yaml
document_management:
  document_register:
    - document_id: null
      document_number: null  # e.g., DRG-001, SPEC-012, RPT-003
      document_title: null
      document_type: null  # drawing, specification, report, certificate, contract, correspondence
      
      classification:
        discipline: null  # architectural, structural, mep, landscape, planning
        category: null  # design, construction, compliance, commercial, admin
        
      versions:
        - version_number: null
          revision_code: null  # A, B, C, etc.
          issue_date: null
          issued_by: null
          issued_for: null  # information, tender, construction, record
          
          changes_from_previous: null
          
          approval:
            requires_approval: false
            approved_by: null
            approval_date: null
            
          distribution:
            - recipient: null
              distribution_date: null
              read_receipt: false
              
          superseded: false
          superseded_date: null
          superseded_by_version: null
          
      current_version: null
      
      file_details:
        file_path: null
        file_format: null  # pdf, dwg, xlsx, docx, jpg
        file_size: null
        
      metadata:
        author: null
        created_date: null
        last_modified: null
        tags: []
        
      access_control:
        confidentiality: null  # public, private, restricted, confidential
        access_list: []
        
      retention:
        retention_period: null  # 6_years, 12_years, permanent
        destruction_date: null
        
      links:
        linked_documents: []
        linked_entities: []  # rooms, tasks, decisions, etc.
        
      status: null  # draft, issued, approved, superseded, archived
      
      notes: null

  drawing_register:
    - drawing_number: null
      drawing_title: null
      scale: null
      drawing_type: null  # location_plan, site_plan, floor_plan, elevation, section, detail
      
      discipline: null  # architectural, structural, mep
      
      versions: []  # Same structure as document versions
      
      coordination:
        clashes_identified: []
        clash_resolution_status: null
        
      issued_for_construction: false
      
      as_built_revision: false
      as_built_date: null
      
      model_reference: null  # BIM model reference if applicable

  specification_register:
    - spec_number: null
      spec_title: null
      section: null  # e.g., "Groundworks", "Masonry", "Roofing"
      
      versions: []
      
      products_specified:
        - product: null
          manufacturer: null
          product_code: null
          approved_alternatives: []
          
      linked_drawings: []
      
  correspondence_register:
    - correspondence_id: null
      date: null
      direction: null  # incoming, outgoing
      method: null  # email, letter, fax, memo
      
      from: null
      to: []
      cc: []
      
      subject: null
      reference: null
      
      category: null  # instruction, information, query, approval, complaint
      
      priority: null  # low, normal, high, urgent
      
      response_required: false
      response_deadline: null
      response_received: false
      
      attachments: []
      
      file_path: null
      
      linked_to:
        project_stage: null
        room_id: null
        task_id: null
        decision_id: null
        risk_id: null
        
      status: null  # pending, actioned, filed, archived

  certificate_register:
    - certificate_type: null  # building_control, electrical, gas, energy, structural, guarantee
      certificate_number: null
      issue_date: null
      issued_by: null
      
      valid_until: null
      renewal_required: false
      renewal_date: null
      
      scope: null
      conditions: []
      
      file_path: null
      
      verification:
        verified: false
        verified_by: null
        verification_date: null
        
      insurance_required: false
      
      linked_to:
        stage: null
        inspection_id: null
        contractor_id: null

  contract_register:
    - contract_id: null
      contract_title: null
      contract_type: null  # professional_services, construction, supply
      
      parties:
        client: null
        contractor_consultant: null
        
      contract_form: null  # JCT, NEC, bespoke
      
      key_terms:
        contract_sum: null
        start_date: null
        completion_date: null
        liquidated_damages: null
        retention_percentage: null
        payment_terms: null
        insurance_requirements: []
        
      programme:
        baseline_programme: null
        current_programme: null
        
      variations: []  # Links to variation_id
      
      payment_schedule: []
      
      status: null  # draft, signed, active, completed, disputed, terminated
      
      contract_administrator: null
      
      file_path: null

  photo_library:
    - photo_id: null
      filename: null
      filepath: null
      
      taken_date: null
      taken_by: null
      
      location:
        gps_coordinates: null
        site_location: null
        room: null
        
      camera_metadata:
        camera: null
        lens: null
        settings: null
        
      categorization:
        project_stage: null
        category: null  # progress, site_conditions, quality_issue, completion, marketing
        tags: []
        
      before_during_after: null  # before, during, after, comparison
      
      linked_to:
        room_id: null
        task_id: null
        inspection_id: null
        quality_issue_id: null
        snagging_item_id: null
        
      description: null
      annotations: []
      
      watermarked: false
      
      usage_rights: null  # private, shareable, publishable
      
      featured_photo: false  # For project showcase

  video_library:
    - video_id: null
      filename: null
      filepath: null
      duration: null
      
      recorded_date: null
      recorded_by: null
      
      video_type: null  # progress_timelapse, walkthrough, tutorial, drone_footage
      
      description: null
      
      linked_to: []
      
      published: false
      publish_location: []  # youtube, instagram, vimeo

  template_library:
    - template_id: null
      template_name: null
      template_type: null  # meeting_minutes, inspection_report, decision_log, risk_assessment
      
      file_path: null
      
      usage_count: null
      last_used: null
      
      customizations: []

document_control_procedures:
  naming_convention: null
  version_control_system: null  # manual, git, cloud_versioning
  backup_frequency: null
  backup_location: []
  
  archiving_policy:
    archive_trigger: null  # project_completion, time_based, manual
    archive_location: null
    archive_format: null
    
  destruction_policy:
    retention_periods: []
    destruction_method: null
```

**Why**: Document management is where projects **lose control**. Version confusion, missing certificates, and lost correspondence cause huge problems. This section creates a single source of truth for all project documentation.

---

## **AO. BIM & Digital Twin (If Applicable)**

```yaml
bim_digital_twin:
  bim_usage:
    using_bim: false
    bim_level: null  # Level 0, 1, 2, 3
    
    bim_software:
      - software: null  # Revit, ArchiCAD, Vectorworks, SketchUp
        discipline: null
        license_type: null
        
    common_data_environment:
      platform: null  # BIM360, Viewpoint, ProjectWise
      structure: null
      access_control: null
      
  model_information:
    - model_id: null
      model_name: null
      discipline: null  # architectural, structural, mep
      
      authoring_software: null
      model_version: null
      last_updated: null
      
      level_of_detail: null  # LOD 100-500
      level_of_information: null  # LOI
      
      coordination_status: null
      clash_detection_status: null
      
      federated_model: false
      
      file_location: null
      file_size: null
      
  information_requirements:
    employers_information_requirements: null
    bim_execution_plan: null
    
  data_drops:
    - data_drop: null
      stage: null  # RIBA Stage 3, 4, etc.
      due_date: null
      delivered_date: null
      content: []
      
  clash_detection:
    - clash_detection_date: null
      clashes_identified: null
      
      clashes:
        - clash_id: null
          clash_type: null  # hard_clash, soft_clash, workflow_clash
          disciplines_involved: []
          severity: null
          
          resolution:
            resolved: false
            resolution_date: null
            resolved_by: null
            resolution_description: null
            
  asset_information_model:
    created: false
    handover_date: null
    
    asset_data:
      - asset_id: null
        asset_type: null
        location: null
        manufacturer: null
        model_number: null
        installation_date: null
        warranty_expiry: null
        maintenance_schedule: null
        
  digital_twin:
    digital_twin_created: false
    
    sensors_installed:
      - sensor_type: null  # temperature, humidity, energy, water, air_quality
        location: null
        installation_date: null
        data_feed: null
        
    real_time_monitoring: false
    
    performance_analytics:
      energy_use: null
      thermal_performance: null
      occupancy_patterns: null
      
    predictive_maintenance: false
```

**Why**: BIM and digital twins are becoming standard. Tracking this information future-proofs the property and enables sophisticated performance monitoring.

---

## **AP. Sustainability Deep Dive**

```yaml
sustainability_detailed:
  embodied_carbon:
    assessment_completed: false
    assessment_tool: null  # RICS Whole Life Carbon, OneClick LCA
    
    total_embodied_carbon: null  # kgCO2e
    embodied_carbon_per_sqm: null
    
    by_element:
      - element: null  # foundations, structure, envelope, services
        kgco2e: null
        percentage_of_total: null
        
    mitigation_strategies:
      - strategy: null
        carbon_saving: null
        cost_implication: null
        
  operational_carbon:
    predicted_annual_operational_carbon: null  # kgCO2e/year
    
    predicted_breakdown:
      heating: null
      cooling: null
      hot_water: null
      lighting: null
      appliances: null
      cooking: null
      
    renewable_offset: null
    
    net_carbon: null
    
  whole_life_carbon:
    assessment_period_years: null
    total_whole_life_carbon: null
    
  circular_economy:
    materials_reused:
      - material: null
        source: null
        quantity: null
        carbon_saving: null
        
    design_for_disassembly: false
    material_passports_created: false
    
  water_strategy:
    predicted_consumption_lpppd: null  # litres per person per day
    
    water_efficiency_measures:
      - measure: null  # low_flow_fixtures, dual_flush, flow_restrictors
        water_saving: null
        
    rainwater_harvesting:
      installed: false
      capacity: null
      uses: []  # toilet_flushing, garden_irrigation, washing_machine
      
    greywater_recycling:
      installed: false
      capacity: null
      uses: []
      
  biodiversity:
    biodiversity_net_gain:
      assessment_required: false
      baseline_biodiversity_units: null
      post_development_units: null
      net_gain_percentage: null
      
    habitat_creation:
      - habitat_type: null  # wildflower_meadow, hedgerow, pond, green_roof
        area: null
        species_supported: []
        
    bird_and_bat_boxes: null
    insect_hotels: null
    
    invasive_species_management: []
    
  materials_sustainability:
    - material: null
      sustainability_credentials:
        - credential: null  # FSC, PEFC, recycled_content, local_sourcing, A_rated
          certification: null
          
      embodied_carbon: null
      recyclability: null
      toxicity_rating: null
      
  transport_and_logistics:
    low_carbon_transport_plan:
      local_sourcing_percentage: null
      average_transport_distance: null
      transport_emissions: null
      
    construction_logistics_plan:
      delivery_consolidation: false
      route_optimization: false
      
  waste_management_detailed:
    waste_hierarchy_compliance: null  # prevent, reuse, recycle, recover, dispose
    
    waste_by_type:
      - waste_type: null
        quantity_tonnes: null
        disposal_method: null  # reused, recycled, energy_recovery, landfill
        percentage_diverted_from_landfill: null
        
    total_waste: null
    waste_per_sqm: null
    
    site_waste_management_plan: null
    
  certifications_pursued:
    - certification: null  # Passivhaus, BREEAM, LEED, Home Quality Mark
      level: null
      status: null  # pursuing, achieved, not_achieved
      assessment_date: null
      certificate_number: null
      score: null
      
  renewable_energy_detailed:
    - system_type: null  # pv, solar_thermal, wind, ground_source
      
      specification:
        capacity: null
        panel_make_model: null
        inverter_make_model: null
        battery_storage: false
        battery_capacity: null
        
      predicted_generation:
        annual_kwh: null
        percentage_of_consumption: null
        
      actual_generation:
        - period: null  # YYYY-MM
          kwh_generated: null
          kwh_exported: null
          kwh_self_consumed: null
          
      financial:
        installation_cost: null
        export_tariff: null
        annual_income: null
        payback_period_years: null
        
  energy_modeling:
    modeling_software: null  # SAP, PHPP, IES
    modeler: null
    
    predicted_performance:
      space_heating_demand: null  # kWh/m²/year
      total_energy_use: null
      primary_energy: null
      co2_emissions: null
      
    sensitivity_analysis:
      - parameter_varied: null
        impact_on_performance: null
        
  indoor_environmental_quality:
    air_quality:
      ventilation_strategy: null
      target_air_changes_per_hour: null
      filtration_level: null
      
    thermal_comfort:
      overheating_analysis_completed: false
      hours_over_threshold: null
      mitigation_strategies: []
      
    daylight:
      daylight_factor_target: null
      average_daylight_factor_achieved: null
      
    acoustics:
      sound_insulation_targets: []
      acoustic_testing_completed: false
      
  life_cycle_assessment:
    lca_completed: false
    lca_tool: null
    assessment_period: null
    
    environmental_impacts:
      global_warming_potential: null
      ozone_depletion: null
      acidification: null
      eutrophication: null
      
  climate_resilience:
    climate_risk_assessment:
      overheating_risk: null
      flood_risk: null
      drought_risk: null
      storm_risk: null
      
    adaptation_measures:
      - measure: null
        risk_addressed: null
        effectiveness: null
```

**Why**: Sustainability is increasingly **regulatory** and **market-valued**. Deep tracking enables certification, demonstrates credentials, and provides data for future performance optimization.

---

## **AQ. Technology & Smart Home Integration**

```yaml
smart_home:
  smart_home_strategy:
    approach: null  # fully_integrated, selective, future_ready_infrastructure, traditional
    
    ecosystems_used:
      - ecosystem: null  # apple_homekit, google_home, amazon_alexa, samsung_smartthings
        primary: false
        
    control_methods: []  # app, voice, automation, physical_switches
    
  infrastructure:
    network:
      wifi_system: null
      ethernet_cabling: false
      mesh_network: false
      network_cabinets: []
      
      bandwidth: null
      provider: null
      
    data_cabling:
      cat6_cat6a_installed: false
      locations: []
      
    power:
      usb_outlets: false
      locations: []
      
  smart_systems_installed:
    lighting:
      smart_lighting_installed: false
      system: null  # Philips Hue, LIFX, Lutron
      
      zones:
        - zone: null
          control_type: null  # app, voice, automation, scene
          
      scenes_configured: []
      automations: []
      
    heating_and_cooling:
      smart_thermostat: false
      system: null  # Nest, Hive, Tado
      
      zones: []
      
      scheduling: null
      geofencing: false
      learning_enabled: false
      
    security:
      smart_locks: false
      lock_locations: []
      
      video_doorbell: false
      doorbell_system: null
      
      security_cameras:
        - location: null
          camera_model: null
          recording: false
          cloud_local: null
          
      alarm_system: false
      alarm_system_type: null
      monitoring: null  # self, professional
      
    access_control:
      intercom_system: false
      gate_automation: false
      garage_door_automation: false
      
    entertainment:
      multi_room_audio: false
      audio_system: null
      
      tv_distribution: false
      
      home_cinema: false
      cinema_location: null
      
    blinds_and_shades:
      automated_blinds: false
      locations: []
      control_system: null
      
    appliances:
      smart_appliances: []
      
    energy_management:
      smart_meter: false
      
      energy_monitoring_system: false
      monitoring_platform: null
      
      battery_storage: false
      battery_capacity: null
      
      ev_charger: false
      charger_type: null
      charging_scheduling: false
      
    water_management:
      leak_detection: false
      leak_detection_system: null
      
      smart_irrigation: false
      irrigation_system: null
      
  automation_and_scenes:
    - automation_name: null
      trigger: null  # time, location, sensor, device_state
      conditions: []
      actions: []
      
  voice_assistants:
    - assistant: null
      locations: []
      integrations: []
      
  data_and_privacy:
    data_storage: null  # cloud, local, hybrid
    
    privacy_considerations:
      cameras_avoid_neighbors: null
      data_encryption: null
      local_processing_preferred: null
      
  future_upgrades_planned:
    - upgrade: null
      timeframe: null
      estimated_cost: null
      
  user_experience:
    ease_of_use_rating: null  # 1-10
    reliability_rating: null
    
    family_adoption:
      tech_savvy_users: []
      non_tech_users: []
      training_needed: []
      
    issues_encountered: []
    
  costs:
    infrastructure_cost: null
    devices_cost: null
    installation_cost: null
    ongoing_subscriptions: null
```

**Why**: Smart home tech is **increasingly expected**. Proper planning during construction avoids expensive retrofitting. Tracking what works (and what doesn't) informs future decisions.

---

## **AR. Specialist Spaces (If Applicable)**

```yaml
specialist_spaces:
  home_office:
    dedicated_office: false
    location: null
    size_sqm: null
    
    infrastructure:
      dedicated_circuit: false
      ethernet_points: null
      additional_insulation_soundproofing: false
      
    tax_considerations:
      business_use_percentage: null
      tax_relief_claimed: false
      
  workshop:
    workshop_included: false
    location: null
    size_sqm: null
    
    power_supply:
      three_phase: false
      capacity: null
      
    ventilation:
      dust_extraction: false
      
    services:
      water: false
      heating: null
      
  gym:
    home_gym: false
    location: null
    size_sqm: null
    
    flooring: null
    mirrors: false
    sound_system: false
    ventilation: null
    
  cinema_room:
    dedicated_cinema: false
    location: null
    size_sqm: null
    
    acoustic_treatment: false
    projector_screen: null
    seating: null
    
  wine_cellar:
    wine_storage: false
    location: null
    capacity: null
    
    climate_control:
      temperature_control: false
      humidity_control: false
      
  studio_creative_space:
    studio_type: null  # art, music, photography, pottery
    location: null
    size_sqm: null
    
    special_requirements:
      natural_light: null
      soundproofing: false
      water_supply: false
      ventilation: null
      
  swimming_pool:
    pool_included: false
    pool_type: null  # indoor, outdoor, natural
    
    size:
      length: null
      width: null
      depth: null
      volume: null
      
    systems:
      filtration: null
      heating: null
      cover: false
      
    enclosure:
      pool_building: false
      glazing: null
      heating_system: null
      
    costs:
      construction_cost: null
      annual_running_cost: null
      
  spa_wellness:
    sauna: false
    steam_room: false
    hot_tub: false
    
    location: null
    
  garage_workshop:
    garage_spaces: null
    
    workshop_area: false
    
    ev_charging: false
    
    storage:
      overhead_storage: false
      wall_storage: false
      
  annexe_granny_flat:
    separate_dwelling: false
    
    planning_status: null  # permitted_development, planning_permission
    
    accommodation:
      bedrooms: null
      bathrooms: null
      kitchen: null
      living_area: null
      
    services:
      separate_utilities: false
      council_tax_status: null
      
  outbuildings:
    - building_type: null  # shed, barn, stable, studio, garage
      size_sqm: null
      construction_type: null
      planning_required: false
      uses: []
      
  accessibility_features:
    wheelchair_accessible: false
    
    features:
      level_access_entrance: false
      lift_installed: false
      wet_room: false
      wider_doors: false
      turning_circles: false
      accessible_kitchen: false
      
    future_proofing:
      prepared_for_stairlift: false
      prepared_for_lift: false
```

**Why**: Specialist spaces have **unique requirements** that must be planned early. They also significantly impact cost and value. Tracking these ensures nothing is forgotten and provides benchmarks for similar projects.

---

## **AS. Final Data Validation & Quality Scores**

```yaml
data_quality:
  completeness:
    overall_completeness_percentage: null
    
    by_section:
      - section: null
        fields_total: null
        fields_populated: null
        completeness_percentage: null
        critical_fields_missing: []
        
  accuracy:
    last_verification_date: null
    verified_by: null
    
    fields_verified:
      - field: null
        verification_method: null  # document_check, professional_confirmation, measurement
        verification_date: null
        verified: false
        
    known_inaccuracies: []
    
  currency:
    - section: null
      last_updated: null
      update_frequency_required: null
      next_update_due: null
      
  confidence_scores:
    - data_category: null  # costs, timeline, specifications, performance
      confidence_level: null  # 1-10
      basis_for_confidence: null  # estimated, quoted, contracted, actual
      
  data_sources:
    - field: null
      source: null  # user_input, professional_report, measurement, calculation, external_data
      source_reliability: null  # 1-10
      
  validation_rules:
    - rule: null
      field: null
      validation_status: null  # passed, failed, warning
      

last_audit:
  audit_date: null
  auditor: null
  issues_identified: []
  recommendations: []
```

**Why**: Data quality tracking ensures the database remains **reliable and actionable**. It highlights gaps and inaccuracies, enabling continuous improvement.

---

## **Summary: Complete Schema Overview**

You now have a **comprehensive, production-ready** schema covering:

### **Pre-Project (5 sections)**

- W. Land Acquisition
- X. Development Context
- Y. Utilities Setup
- Z. Access Infrastructure
- AA. Archaeology

### **Project Execution (10 sections)**

- AB. Listed Building & Heritage
- AC. Self-Build Mortgage
- AD. Tools & Equipment
- AE. Site Security
- AF. Weather & Environmental Monitoring
- L. Programme Management (from earlier)
- M. Materials & Procurement
- N. Quality Control
- O. Variations & Change Orders
- P. Commissioning & Testing

### **Compliance & Legal (3 sections)**

- Q. Compliance & Certification (from earlier)
- AJ. Legal Disputes

### **Stakeholder & Human Factors (3 sections)**

- R. Meetings & Site Visits (from earlier)
- S. Stakeholder Management
- AK. Personal & Family Wellbeing

### **Post-Project (3 sections)**

- AG. Lessons Learned & Reflection
- AH. Post-Occupancy Experience
- AM. Future Development

### **Technical & Specialized (5 sections)**

- AI. Community & Networking
- AO. BIM & Digital Twin
- AP. Sustainability Deep Dive
- AQ. Smart Home Technology
- AR. Specialist Spaces

### **System Management (3 sections)**

- AL. Project Metrics & Analytics
- AN. Document Management
- AS. Data Quality & Validation

---

## **Database Implementation Considerations**

### **Tables Structure Recommendation**

For a relational database, organize as:

**Core Tables:**

- `projects`
- `users`
- `rooms`
- `tasks`
- `costs`
- `decisions`
- `risks`
- `documents`

**Relationship Tables:**

- `room_costs`
- `room_tasks`
- `room_materials`
- `decision_costs`
- `decision_risks`
- `task_dependencies`
- (All the relationships mapped earlier)

**Lookup Tables:**

- `building_regs_parts`
- `riba_stages`
- `trade_types`
- `document_types`
- `material_categories`

**Timeline Tables:**

- `programme_activities`
- `milestones`
- `weather_log`
- `site_diary`

**People Tables:**

- `professionals`
- `contractors`
- `suppliers`
- `stakeholders`
- `neighbors`

**Compliance Tables:**

- `planning_applications`
- `building_control_inspections`
- `certificates`
- `warranties`

**Financial Tables:**

- `budget_categories`
- `cost_items`
- `invoices`
- `payments`
- `variations`

---

## **What This Schema Enables**

With this complete schema, Aven can:

1. **Track every aspect** of a self-build from dream to post-occupancy
2. **Surface intelligent connections** (design → cost → schedule → compliance)
3. **Identify patterns** across multiple projects (what typically goes wrong, what works well)
4. **Generate insights** (you're overspent on finishes, behind on programme, need to book inspection)
5. **Provide benchmarks** (your cost/m² vs. regional average, your timeline vs. similar projects)
6. **Learn continuously** (build ML models on what predicts success/failure)
7. **Create rich exports** (stakeholder packs, completion reports, lessons learned documents)
8. **Enable true decision support** (if you change X, here's the impact on Y, Z, and W)

---

**This is now a complete, enterprise-grade data model for self-build project management.**

Would you like me to:

1. **Create an ERD (Entity Relationship Diagram)** showing how all these sections interconnect?
2. **Design the database schema** with specific table structures, foreign keys, and indexes?
3. **Map which sections feed which Aven UI features** (room pages, budget tracker, dashboard widgets)?
4. **Prioritize** which sections are MVP vs. nice-to-have for initial launch?


## Schema Summery?**

1. **Insurance Claims Management** - Tracking damage, claims process, disputes
2. **Neighboring Projects** - If building in a development with multiple plots
3. **Utilities Setup** - Detailed connection process for mains services
4. **Access Road Construction** - If building in remote location
5. **Archaeology** - If site has archaeological interest
6. **Listed Building Specific** - Additional constraints and processes
7. **Self-Build Mortgage Stages** - Detailed tracking of drawdown requirements
8. **Tool & Equipment Inventory** - What's owned vs. hired
9. **Site Security** - Theft, vandalism, insurance incidents
10. **Weather Impact Analysis** - How weather affected programme/costs