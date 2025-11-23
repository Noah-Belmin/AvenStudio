
Below is **Phase 1** of the full RIBA-aligned snagging and inspection schema: **Pre-Construction → Final Fix**.  
This version is _field-ready_ — structured so you can populate it from site forms, mobile apps, or manual audits later.

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

- Each stage can be **instantiated as a live YAML or JSON node** during inspection.
- Every `check` can feed into your `snagging_register` with outcome data (`status`, `photos`, `comments`, etc.).
- The schema is **modular** — you can add bespoke trades (solar, EV charger, smart home, etc.) without breaking structure.
- It’s compliant with **RIBA Stage 5–6 workflows** and aligns with **NHBC Quality Checklist** standards.
