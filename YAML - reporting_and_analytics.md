
**Phase 3: Reporting & Analytics**, where this schema stops being a static record and becomes a **decision-support tool**.

From a main-contractor perspective, this phase is about visibility and accountability: _What’s our quality performance? Where are delays and costs building up? Which trades or stages need improvement?_

Below is the **YAML analytics layer** that plugs into your snagging and inspection data.  
It’s designed for export into dashboards (Power BI, Grafana, or Aven’s internal visual modules) while remaining human-readable.

```YAML
reporting_and_analytics:
  metadata:
    report_period:
      start_date: null
      end_date: null
    generated_by: "Aven QA Engine"
    version: 1.0
    data_sources:
      - snagging_register
      - defects_liability_period
      - inspection_templates
      - warranty_management

  kpis_summary:
    total_snags_logged: 0
    total_snags_closed: 0
    open_rate_percent: 0
    avg_resolution_days: 0
    overdue_snags: 0
    defects_in_dlp: 0
    warranties_active: 0
    client_satisfaction_score: null
    retention_released: false
    comments: null

  trade_performance:
    # aggregated from snagging register
    - trade: "Carpentry"
      snags_open: 0
      snags_closed: 0
      avg_resolution_days: 0
      cost_to_rectify_total: 0
      recurring_issues: ["door alignment", "skirting gaps"]
      trend: "improving"   # improving / declining / static
    - trade: "Electrical"
      snags_open: 0
      snags_closed: 0
      avg_resolution_days: 0
      recurring_issues: ["socket alignment", "loose faceplate"]
      trend: "declining"
    - trade: "Plumbing"
      snags_open: 0
      snags_closed: 0
      avg_resolution_days: 0
      recurring_issues: ["sealant gaps", "minor leaks"]
      trend: "static"

  stage_quality_scores:
    - stage: "Groundworks"
      total_checks: 0
      failed_checks: 0
      pass_rate_percent: 0
      avg_rectification_time_days: 0
      inspection_score_percent: 0
    - stage: "First Fix"
      total_checks: 0
      failed_checks: 0
      pass_rate_percent: 0
      inspection_score_percent: 0
    - stage: "Final Fix"
      total_checks: 0
      failed_checks: 0
      pass_rate_percent: 0
      inspection_score_percent: 0
    - stage: "Handover"
      total_checks: 0
      failed_checks: 0
      pass_rate_percent: 0
      inspection_score_percent: 0

  defect_density_analysis:
    description: "Shows concentration of defects per zone or m²."
    metrics:
      total_floor_area_m2: null
      total_defects: 0
      defect_density_per_m2: 0
      hotspots:
        - area: "Kitchen"
          snags: 0
          severity_breakdown:
            critical: 0
            major: 0
            minor: 0
        - area: "Bathroom"
          snags: 0
        - area: "External Works"
          snags: 0

  time_to_resolution:
    histogram_buckets:
      "<1_day": 0
      "1_to_3_days": 0
      "4_to_7_days": 0
      "8_to_14_days": 0
      "15+_days": 0
    average: 0
    longest_open_item_id: null

  cost_analysis:
    total_rectification_cost: 0
    cost_by_trade:
      carpentry: 0
      electrical: 0
      plumbing: 0
      decoration: 0
      general_build: 0
    cost_by_severity:
      critical: 0
      major: 0
      minor: 0
      cosmetic: 0
    average_cost_per_snag: 0
    budget_variance_percent: 0

  trend_analysis:
    frequency:
      weekly_snags_logged: []
      weekly_snags_closed: []
    heatmap_by_stage:
      - stage: "First Fix"
        weeks_active: []
      - stage: "Final Fix"
        weeks_active: []
    commentary: null

  audit_and_compliance_summary:
    inspections_due: 0
    inspections_completed: 0
    certificates_pending: 0
    non_compliance_items: 0
    corrective_actions_open: 0
    outstanding_actions_by_party:
      - party: "Main Contractor"
        open_actions: 0
      - party: "Electrical Subcontractor"
        open_actions: 0

  client_experience_dashboard:
    overall_satisfaction_avg: null
    positive_feedback_ratio: 0
    negative_feedback_ratio: 0
    key_themes:
      positive: []
      negative: []
    post_occupancy_issues:
      comfort: null
      noise: null
      energy_efficiency: null
      maintenance: null

  risk_assessment:
    description: "Aggregated quality and performance risks derived from trends."
    risk_items:
      - id: R01
        risk: "Recurring plumbing seal failures"
        likelihood: "medium"
        impact: "medium"
        mitigation: "Audit supplier sealant; retrain subcontractor"
        owner: "Site Manager"
        review_date: null
      - id: R02
        risk: "High snag density in joinery at Final Fix"
        likelihood: "high"
        impact: "high"
        mitigation: "Introduce pre-handover joinery QA signoff"
        owner: "QA Manager"
        review_date: null

  continuous_improvement_log:
    - reference: "Project A"
      lesson: "Early fire-stopping inspections reduced late-stage snags by 40%"
      implemented_in_future_projects: true
    - reference: "Project B"
      lesson: "Digital photo tagging improved accountability across trades"
      implemented_in_future_projects: true

```

| Module                             | Purpose                                                                 |
| ---------------------------------- | ----------------------------------------------------------------------- |
| **`kpis_summary`**                 | At-a-glance project health — ideal for your dashboard top bar.          |
| **`trade_performance`**            | Quantifies subcontractor performance and identifies repeat offenders.   |
| **`stage_quality_scores`**         | Links directly to inspection templates to score quality per RIBA stage. |
| **`defect_density_analysis`**      | Helps visualise where defects cluster — supports photographic mapping.  |
| **`time_to_resolution`**           | Enables performance tracking of snag turnaround.                        |
| **`cost_analysis`**                | Translates quality into financial impact for cost control.              |
| **`trend_analysis`**               | Highlights workflow bottlenecks and quality drift over time.            |
| **`audit_and_compliance_summary`** | Quick compliance snapshot for Building Control or insurers.             |
| **`client_experience_dashboard`**  | Closes the feedback loop — the “soft data” on performance.              |
| **`risk_assessment`**              | Turns raw analytics into actionable site risk management.               |
| **`continuous_improvement_log`**   | Institutional memory for future builds.                                 |