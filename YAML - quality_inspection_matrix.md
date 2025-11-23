
**RIBA-aligned “Quality Inspection & Snagging Schema”** that captures **every inspection stage**, integrates **snagging detail**, and sets the groundwork for a proper **QA + compliance audit trail**.

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

- **RIBA alignment** – stages 0–7 are represented; stage 5 is expanded into granular site phases like _pre-plaster_ or _second fix_.
    
- **Nested “inspections” arrays** – each can become a live checklist or snagging log entry.
    
- **Centralised snagging register** – unifies all snags across stages, enabling dashboard reporting.
    
- **Compliance certificates section** – mirrors what Building Control and insurers expect pre-handover.
    
- **Approvals & sign-off** – structured for digital signoff or PDF export with signatures.