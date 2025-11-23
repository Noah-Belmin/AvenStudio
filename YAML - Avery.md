Thinking as a site manager preparing for **handover and compliance sign-off**, not just chasing snags.  

Here’s the next logical step: a **RIBA-aligned “Quality Inspection & Snagging Schema”** that captures **every inspection stage**, integrates **snagging detail**, and sets the groundwork for a proper **QA + compliance audit trail**.

This `YAML` can drive an app, database, or reporting tool — it’s granular enough for trade accountability but still readable:

```yaml
quality_inspection_matrix:
  metadata:
    project_name: null
    project_id: null
    site_address: null
    client: null
    main_contractor: null
    site_manager: null
    clerk_of_works: null
    inspection_date: null
    version: 1.0
    reference_docs:
      - drawings: null
      - specifications: null
      - method_statements: null
      - health_safety_file: null

  stages:
    riba_stages:
      - stage_id: 1
        name: "Preparation & Brief"
        inspections: []
      - stage_id: 2
        name: "Concept Design"
        inspections: []
      - stage_id: 3
        name: "Developed Design"
        inspections: []
      - stage_id: 4
        name: "Technical Design"
        inspections: []
      - stage_id: 5
        name: "Construction"
        sub_stages:
          - name: "Pre-Construction Setup"
            inspections:
              - check_id: null
                category: "Site Setup"
                description: "Site fencing, welfare, H&S signage in place"
                status: open
                photos: []
                notes: null
          - name: "Groundworks & Foundations"
            inspections:
              - check_id: null
                category: "Foundations"
                description: "Trenches excavated, inspected by Building Control, reinforcement installed per drawings"
                issue: null
                severity: null
                responsible_party: null
                photos: []
                status: open
                notes: null
          - name: "Structural Frame"
            inspections:
              - check_id: null
                category: "Structure"
                description: "Load-bearing elements level, plumb, secured; welds/bolts checked"
                issue: null
                severity: null
                responsible_party: null
                photos: []
                status: open
                notes: null
          - name: "Envelope & Roofing"
            inspections:
              - check_id: null
                category: "Envelope"
                description: "Cladding/roof membrane continuity, insulation thickness, weathertightness"
                issue: null
                severity: null
                responsible_party: null
                photos: []
                status: open
                notes: null
          - name: "First Fix (M&E, Joinery)"
            inspections:
              - check_id: null
                category: "Electrical"
                description: "Cable runs and backboxes per layout; containment and circuit IDs checked"
                issue: null
                photos: []
                status: open
              - check_id: null
                category: "Plumbing"
                description: "Pipework pressure tested, isolation valves fitted, insulation installed"
                issue: null
                status: open
              - check_id: null
                category: "Carpentry"
                description: "Door linings, frames, battens installed square and secure"
                issue: null
                status: open
          - name: "Pre-Plaster Inspection"
            inspections:
              - check_id: null
                category: "Build Quality"
                description: "Wall chases filled, insulation continuous, air-tightness details sealed"
                issue: null
                severity: null
                photos: []
                status: open
          - name: "Second Fix"
            inspections:
              - check_id: null
                category: "Electrical"
                description: "Sockets/switches fitted, light fixtures secure, continuity tested"
                issue: null
                status: open
              - check_id: null
                category: "Plumbing"
                description: "Appliances connected, no leaks, commissioning records complete"
                issue: null
                status: open
              - check_id: null
                category: "Joinery"
                description: "Skirtings, architraves, doors, stairs completed to finish spec"
                issue: null
                status: open
          - name: "Decoration & Finishes"
            inspections:
              - check_id: null
                category: "Finishes"
                description: "Paintwork, plaster, and flooring checked for uniform finish and cleanliness"
                issue: null
                photos: []
                status: open
          - name: "Final Fix / Commissioning"
            inspections:
              - check_id: null
                category: "Systems Commissioning"
                description: "All M&E systems tested, certificates logged, manuals compiled"
                issue: null
                status: open
          - name: "Practical Completion"
            inspections:
              - check_id: null
                category: "Handover QA"
                description: "All snags identified, documentation pack ready, safety systems tested"
                issue: null
                status: open
          - name: "Defects Liability Period"
            inspections:
              - check_id: null
                category: "Defects Review"
                description: "Monitor defects and warranty claims during DLP"
                issue: null
                status: open

  snagging_register:
    - item_id: null
      stage: null                  # RIBA or substage reference
      location: null               # room/area
      category: null               # trade classification
      issue: null
      defect_type: null            # alignment, finish, leak, performance
      severity: null               # critical, major, minor, cosmetic
      responsible_party: null
      reported_by: null
      reported_date: null
      target_fix_date: null
      fix_verified_date: null
      status: open                 # open, in_progress, fixed, verified, closed
      reinspection_required: false
      cost_to_rectify: null
      photos: []
      notes: null

  compliance_certificates:
    structural_warranty: false
    electrical_installation_certificate: false
    gas_safety_certificate: false
    water_regulations_certificate: false
    air_permeability_test: false
    sound_insulation_test: false
    fire_safety_certificate: false
    energy_performance_certificate: false
    building_control_completion_certificate: false
    planning_compliance_certificate: false
    operation_and_maintenance_manuals: false
    as_built_drawings: false
    health_and_safety_file: false

  approvals_and_signoff:
    inspected_by:
      - name: null
        role: null
        date: null
        signature_ref: null
    signed_off_by_client: false
    final_signoff_date: null
    retention_released: false
    remarks: null
```

---

### 🔧 Breakdown & Rationale

- **RIBA alignment** – stages 0–7 are represented; stage 5 is expanded into granular site phases like _pre-plaster_ or _second fix_.
- **Nested “inspections” arrays** – each can become a live checklist or snagging log entry.
- **Centralised snagging register** – unifies all snags across stages, enabling dashboard reporting.
- **Compliance certificates section** – mirrors what Building Control and insurers expect pre-handover.
- **Approvals & sign-off** – structured for digital signoff or PDF export with signatures.

---

Perfect — we’re now stepping into **true contractor QA territory**: what a site manager, clerk of works, or NHBC inspector would use during each build stage.

Below is **Phase 1** of the full RIBA-aligned snagging and inspection schema: **Pre-Construction → Final Fix**.  
This version is _field-ready_ — structured so you can populate it from site forms, mobile apps, or manual audits later.

---

```yaml
inspection_templates:
  stage_1_pre_construction:
    name: "Pre-Construction Setup"
    description: "Establish site readiness, welfare, safety and documentation before work begins."
    checks:
      - id: PC01
        category: "Site Setup"
        item: "Perimeter fencing, signage, and site security installed"
        acceptance_criteria: "Fencing intact, secure gates, safety and hazard signage visible"
      - id: PC02
        category: "Welfare Facilities"
        item: "Toilets, wash stations, drying room, canteen in operation"
        acceptance_criteria: "Facilities clean, accessible, compliant with HSE guidelines"
      - id: PC03
        category: "Documentation"
        item: "Construction Phase Plan, Risk Assessments and Method Statements approved"
        acceptance_criteria: "Signed and version-controlled copies available on site"
      - id: PC04
        category: "Utilities"
        item: "Temporary power, lighting, and water connected safely"
        acceptance_criteria: "PAT-tested distribution, labelled, RCD protection verified"

  stage_2_groundworks_and_foundations:
    name: "Groundworks & Foundations"
    description: "Substructure works, drainage and slab installation prior to frame erection."
    checks:
      - id: GF01
        category: "Excavation"
        item: "Trenches to correct depth and width per drawings"
        acceptance_criteria: "Checked by Building Control or Engineer; no standing water or soft spots"
      - id: GF02
        category: "Concrete"
        item: "Foundation concrete poured to correct level and vibration"
        acceptance_criteria: "Cube samples taken, surface finish smooth and level"
      - id: GF03
        category: "Drainage"
        item: "Foul and surface water drainage installed and tested"
        acceptance_criteria: "CCTV/pressure test certificates; pipe gradients per design"
      - id: GF04
        category: "Ground Slab"
        item: "DPM and insulation continuous under slab"
        acceptance_criteria: "No punctures; overlaps taped; insulation full coverage"

  stage_3_superstructure:
    name: "Structural Frame & Envelope"
    description: "Structural framing, floors, walls and roof built to specification."
    checks:
      - id: SS01
        category: "Framing"
        item: "Walls and floor levels plumb, square and fixed"
        acceptance_criteria: "Measured deviation ≤ 5 mm per 2 m"
      - id: SS02
        category: "Load Paths"
        item: "Lintels, beams, and trusses installed per engineer design"
        acceptance_criteria: "All fixings correct type and location; bearing lengths achieved"
      - id: SS03
        category: "Envelope"
        item: "Breather membrane, cavity barriers and insulation continuity"
        acceptance_criteria: "No gaps or tears; taped joints; barriers fixed per spec"
      - id: SS04
        category: "Roofing"
        item: "Felt, battens, tiles/slates fixed with correct gauge and overlap"
        acceptance_criteria: "Level ridge line, secure verge details, ventilation paths clear"

  stage_4_first_fix:
    name: "First Fix (M&E and Carpentry)"
    description: "Hidden services and structural carpentry before plasterboard closure."
    checks:
      - id: FF01
        category: "Electrical"
        item: "Cable routes and backboxes per layout; circuits labelled"
        acceptance_criteria: "No exposed conductors; continuity and insulation resistance pre-test passed"
      - id: FF02
        category: "Plumbing"
        item: "Hot/cold pipework insulated, pressure tested, fixings secure"
        acceptance_criteria: "Pressure test certificate retained"
      - id: FF03
        category: "Carpentry"
        item: "Door linings, noggings, and stairs installed true"
        acceptance_criteria: "Tolerances within BS 8213 and BS 585"
      - id: FF04
        category: "Fire Stopping"
        item: "Penetrations sealed with fire-rated materials"
        acceptance_criteria: "Fire-stopping log updated and photographed"

  stage_5_pre_plaster:
    name: "Pre-Plaster / Air-Tightness Prep"
    description: "Inspect hidden works before walls are closed."
    checks:
      - id: PP01
        category: "Insulation"
        item: "All external walls and ceilings fully insulated"
        acceptance_criteria: "No voids; insulation tight against structure"
      - id: PP02
        category: "Air Sealing"
        item: "All service penetrations sealed"
        acceptance_criteria: "Smoke pencil test – no air leaks"
      - id: PP03
        category: "M&E Checks"
        item: "Cables, pipes, and ducts final fix positions correct"
        acceptance_criteria: "Checked against drawings and labelled"

  stage_6_second_fix:
    name: "Second Fix & Fit-Out"
    description: "Visible service terminations, joinery, and finishes installation."
    checks:
      - id: SF01
        category: "Electrical"
        item: "Sockets, lighting, and consumer unit connected"
        acceptance_criteria: "Testing complete; EIC issued"
      - id: SF02
        category: "Plumbing"
        item: "Sanitaryware installed, no leaks"
        acceptance_criteria: "Visual check dry; pressure test complete"
      - id: SF03
        category: "Joinery"
        item: "Doors hung, ironmongery fitted, stairs secure"
        acceptance_criteria: "Margins even, smooth operation"
      - id: SF04
        category: "Kitchen & Utility"
        item: "Units level, worktops sealed, appliances commissioned"
        acceptance_criteria: "Water-tight joints; manuals included"

  stage_7_final_fix_and_commissioning:
    name: "Final Fix & Commissioning"
    description: "System testing, certification, and decorative completion."
    checks:
      - id: FC01
        category: "Heating & Hot Water"
        item: "Boiler/heat pump commissioned; benchmark log completed"
        acceptance_criteria: "Engineer sign-off and warranty registered"
      - id: FC02
        category: "Ventilation"
        item: "MVHR/Extract systems balanced"
        acceptance_criteria: "Flow-rate test within spec"
      - id: FC03
        category: "Decoration"
        item: "Paintwork, flooring, tiling, and sealant complete"
        acceptance_criteria: "Uniform colour; no defects or contamination"
      - id: FC04
        category: "Cleaning & Presentation"
        item: "Site cleared, windows cleaned, protection removed"
        acceptance_criteria: "Ready for client inspection"

  stage_8_practical_completion:
    name: "Practical Completion & Handover"
    description: "Final inspection, snag capture, documentation, and client acceptance."
    checks:
      - id: PCOMP01
        category: "Snagging"
        item: "All defects recorded, categorised, and allocated"
        acceptance_criteria: "Snag list complete and signed by both parties"
      - id: PCOMP02
        category: "Certificates"
        item: "All test, commissioning, and compliance certificates compiled"
        acceptance_criteria: "Pack complete and handed to client"
      - id: PCOMP03
        category: "Demonstration"
        item: "Client walk-through and system demonstration completed"
        acceptance_criteria: "Sign-off form completed"
      - id: PCOMP04
        category: "Retention"
        item: "Retention release criteria met"
        acceptance_criteria: "Defects Liability Period defined; dates agreed"
```

### 🔍 How to Use This

- Each stage can be **instantiated as a live YAML or JSON node** during inspection.
- Every `check` can feed into your `snagging_register` with outcome data (`status`, `photos`, `comments`, etc.).
- The schema is **modular** — you can add bespoke trades (solar, EV charger, smart home, etc.) without breaking structure.
- It’s compliant with **RIBA Stage 5–6 workflows** and aligns with **NHBC Quality Checklist** standards.



