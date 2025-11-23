
If we’re thinking like a **main contractor preparing a home for client handover**, we’re not just ticking boxes — we’re performing a structured _quality assurance and defect management audit_ across all trades and finishes. 

Expanding on the YAML schema into a **comprehensive snagging framework**, capturing everything from structural integrity and M&E (mechanical & electrical) systems to cosmetic finishes and safety compliance. This mirrors what a contractor, site manager, or clerk of works would use pre-completion.

```YAML
snagging_audit:
  metadata:
    project_name: null
    project_id: null
    site_address: null
    client_name: null
    main_contractor: null
    surveyor_or_clerk: null
    inspection_date: null
    report_version: 1.0
    reference_docs:
      - drawings: null
      - specifications: null
      - contracts: null
      - inspection_checklist: null

  overall_status:
    total_items: 0
    open_items: 0
    closed_items: 0
    verified_items: 0
    completion_percentage: 0
    summary_notes: null

  inspection_categories:
    structure:
      - item_id: null
        element: null          # e.g. foundations, walls, roof trusses
        issue: null
        severity: null         # critical, major, minor
        responsible_party: null
        status: open           # open, in_progress, fixed, verified
        reported_date: null
        target_fix_date: null
        verified_date: null
        photos: []
        notes: null

    external_works:
      - item_id: null
        element: null          # e.g. brickwork, render, roof, gutters, fascias
        issue: null
        severity: null
        responsible_party: null
        status: open
        photos: []
        notes: null

    internal_finishes:
      - item_id: null
        room: null             # e.g. living room, hallway, bedroom 1
        surface_type: null     # wall, ceiling, skirting, joinery, flooring
        issue: null
        defect_type: null      # paint run, chipped tile, uneven plaster, gap, scratch
        severity: null         # cosmetic, minor, major
        photos: []
        responsible_party: null
        status: open
        notes: null

    doors_and_windows:
      - item_id: null
        location: null
        component: null        # internal door, patio slider, window
        issue: null
        defect_type: null      # alignment, latch, seal, glazing scratch, draught
        operable: true
        compliant: null
        responsible_party: null
        status: open
        photos: []
        notes: null

    m_and_e_services:
      electrical:
        - item_id: null
          location: null
          issue: null
          defect_type: null    # missing faceplate, loose socket, non-functional circuit
          test_certificate_received: false
          responsible_party: null
          status: open
          photos: []
          notes: null
      plumbing:
        - item_id: null
          location: null
          issue: null
          defect_type: null    # leak, poor alignment, missing isolation valve
          water_pressure_test_passed: false
          responsible_party: null
          status: open
          photos: []
          notes: null
      hvac:
        - item_id: null
          location: null
          issue: null
          defect_type: null    # thermostat calibration, filter missing, duct noise
          commissioning_cert_received: false
          responsible_party: null
          status: open
          photos: []
          notes: null

    kitchens_and_bathrooms:
      - item_id: null
        room: null
        fixture: null          # basin, toilet, shower, unit, worktop
        issue: null
        defect_type: null      # sealant gap, chip, alignment, leak
        responsible_party: null
        photos: []
        status: open
        notes: null

    joinery_and_carpentry:
      - item_id: null
        location: null
        component: null        # staircase, skirting, door frame, wardrobe
        issue: null
        defect_type: null      # rough finish, loose fixings, misalignment
        severity: null
        responsible_party: null
        status: open
        photos: []
        notes: null

    decoration:
      - item_id: null
        room: null
        surface: null          # wall, ceiling, trim
        issue: null
        defect_type: null      # missed patch, brush marks, discolouration
        finish_spec: null      # paint code, gloss level
        responsible_party: null
        photos: []
        status: open
        notes: null

    flooring:
      - item_id: null
        room: null
        material: null         # timber, tile, carpet, vinyl
        issue: null
        defect_type: null      # uneven joint, damaged board, loose tile
        responsible_party: null
        photos: []
        status: open
        notes: null

    landscaping_and_externals:
      - item_id: null
        area: null             # driveway, patio, fencing, turf
        issue: null
        defect_type: null      # settlement, poor drainage, uneven surface
        responsible_party: null
        photos: []
        status: open
        notes: null

    compliance_and_safety:
      - item_id: null
        category: null         # fire safety, gas, electrics, ventilation, glazing
        test_certificate_received: false
        issue: null
        risk_level: null       # high, medium, low
        responsible_party: null
        photos: []
        status: open
        notes: null

  signoff_process:
    preliminary_inspection_date: null
    reinspection_date: null
    final_signoff_date: null
    signed_off_by:
      client: null
      contractor: null
      surveyor: null
    documentation_checklist:
      as_built_drawings: false
      electrical_certificates: false
      gas_safe_certificate: false
      commissioning_certificates: false
      test_results: false
      warranties_pack: false
      o_and_m_manuals: false
      building_control_certificate: false
    retention_release_approved: false
    remarks: null

```

### **Design Rationale**

- **Trade-segmented structure** – mirrors site inspection and QA sheets used by `NHBC`, `RICS` or `CIOB` standards.
- **Photos per item** – enables visual record and proof on dispute
- **Test & certification flags** for M&E and compliance.
- **Preliminary, reinspection and final sign-off workflow** built in.
- **Retention release** and documentation linkage integrated — so financial closeout ties to quality closeout.