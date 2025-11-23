
**Phase 2: Post-Completion** — extends the YAML into a _living defects and warranty management layer_ that runs from handover through the end of the Defects Liability Period (DLP).  

It covers defect tracking, warranty claims, seasonal checks, and client satisfaction review — just as a professional builder or site manager would maintain.

```yaml
post_completion:
  defects_liability_period:
    name: "Defects Liability Period"
    description: "Monitor, record and rectify all defects arising after practical completion."
    duration_months: 12
    start_date: null
    end_date: null
    inspections_schedule:
      - id: DLP01
        type: "3-Month Review"
        planned_date: null
        conducted_date: null
        inspected_by: null
        summary: null
      - id: DLP02
        type: "6-Month Review"
        planned_date: null
        conducted_date: null
        inspected_by: null
        summary: null
      - id: DLP03
        type: "12-Month / Final Review"
        planned_date: null
        conducted_date: null
        inspected_by: null
        summary: null

    defects_register:
      - defect_id: null
        reported_date: null
        reported_by: null
        category: null               # structure, services, finishes, external
        location: null
        description: null
        severity: null               # critical, major, minor, cosmetic
        responsible_party: null
        status: open                 # open, in_progress, resolved, verified, closed
        target_completion_date: null
        actual_completion_date: null
        verification_by: null
        warranty_related: false
        cost_to_rectify: null
        photos: []
        notes: null

    performance_monitoring:
      - system: "Heating"
        observation: null            # e.g. inconsistent temperature, noise
        service_required: false
      - system: "Ventilation"
        observation: null
        service_required: false
      - system: "Plumbing"
        observation: null
        service_required: false
      - system: "Electrical"
        observation: null
        service_required: false
      - system: "Smart / Controls"
        observation: null
        service_required: false

  warranty_management:
    description: "Register and monitor all active warranties, guarantees and service obligations."
    warranties:
      - warranty_id: null
        type: null                    # structural, workmanship, product, waterproofing
        provider: null                # NHBC, LABC, manufacturer
        reference: null
        coverage_details: null
        contact_information: null
        start_date: null
        expiry_date: null
        renewal_required: false
        claim_process: null
        claim_history:
          - claim_id: null
            reported_date: null
            issue_summary: null
            resolution_date: null
            cost: null
            status: null
        documentation_path: null
        active: true

  seasonal_maintenance_checks:
    description: "Planned post-handover checks to maintain building performance."
    schedules:
      - season: "Spring"
        focus: ["roof drainage", "external paintwork", "MVHR filter clean"]
      - season: "Autumn"
        focus: ["gutter clearing", "boiler service", "sealant check"]
      - season: "Winter"
        focus: ["heating efficiency", "insulation integrity", "frost protection"]

  client_feedback_and_lessons_learned:
    feedback_form:
      issued_date: null
      returned_date: null
      sections:
        - category: "Design & Functionality"
          rating_out_of_5: null
          comments: null
        - category: "Workmanship & Finish"
          rating_out_of_5: null
          comments: null
        - category: "Communication & Handover"
          rating_out_of_5: null
          comments: null
        - category: "Overall Satisfaction"
          rating_out_of_5: null
          comments: null
    lessons_learned:
      - reference_stage: null        # e.g. Stage_4_First_Fix
        observation: null
        corrective_action: null
        responsibility: null
        implemented_on_future_projects: false

  closeout_and_retention_release:
    criteria_met: false
    final_defects_list_cleared: false
    client_approval_received: false
    final_account_settled: false
    retention_released: false
    completion_certificate_issued: false
    archive_pack:
      o_and_m_manuals: true
      warranties_pack: true
      as_built_drawings: true
      test_certificates: true
      photographic_record: true
      maintenance_schedule: true
    archive_location: null           # path or URL to digital file vault
    remarks: null

```

| Section                                   | Purpose                                            | Mirrors Industry Practice                       |
| ----------------------------------------- | -------------------------------------------------- | ----------------------------------------------- |
| **`defects_liability_period`**            | Records every defect and timed inspections         | Matches JCT / NHBC DLP clauses                  |
| **`warranty_management`**                 | Tracks multiple overlapping warranties             | Aligns with NHBC Buildmark / product guarantees |
| **`seasonal_maintenance_checks`**         | Encourages preventative maintenance                | Typical homeowner handover advice               |
| **`client_feedback_and_lessons_learned`** | Captures satisfaction & learning                   | ISO 9001 / CIOB quality review                  |
| **`closeout_and_retention_release`**      | Formalises final financial & documentation release | Standard main-contractor closeout               |