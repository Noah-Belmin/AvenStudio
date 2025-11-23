**Phase 4: Digital Integration & Aven Linkage**, where the schema becomes a _live ecosystem_ rather than static documentation.

Think of this layer as the connective tissue between your YAML data, files, dashboards, and the Aven assistant itself — so data moves freely between inspection devices, document vaults, and analysis dashboards.


```YAML
digital_integration:
  system_overview:
    description: "Defines how snagging and QA data connect to digital systems, storage, and Aven intelligence."
    integration_version: 1.0
    data_flow:
      - source: "Site inspection device / mobile app"
        format: "YAML or JSON payload"
        destination: "Aven ingestion API"
        frequency: "real-time"
      - source: "Aven QA Knowledge Graph"
        format: "JSON-LD / YAML"
        destination: "Dashboard visualisation layer"
        frequency: "daily sync"
      - source: "File storage / NAS / Cloud"
        format: "PDF, JPG, MP4, DOCX"
        destination: "Linked asset registry"
        frequency: "on upload"

  file_management:
    root_directory: "/project_data/"
    subfolders:
      - "inspections"
      - "snag_photos"
      - "certificates"
      - "as_built_drawings"
      - "o_and_m_manuals"
      - "reports"
      - "lessons_learned"
    file_naming_convention: "{project_id}_{stage}_{trade}_{date}_{descriptor}"
    metadata_schema:
      - field: "file_id"
        type: "UUID"
      - field: "linked_item_id"
        type: "inspection_id or snag_id"
      - field: "uploaded_by"
        type: "user_ref"
      - field: "timestamp"
        type: "ISO8601"
      - field: "checksum"
        type: "sha256"
      - field: "tags"
        type: "array"
      - field: "version"
        type: "int"

  aven_knowledge_graph:
    description: "Semantic graph connecting entities across QA, defects, and lessons learned."
    entities:
      - node_type: "Project"
        properties: ["project_id", "address", "start_date", "completion_date"]
      - node_type: "Stage"
        properties: ["stage_id", "riba_stage", "inspection_score"]
      - node_type: "Trade"
        properties: ["name", "subcontractor", "performance_rating"]
      - node_type: "Snag"
        properties: ["snag_id", "location", "severity", "responsible_party", "status"]
      - node_type: "Defect"
        properties: ["defect_id", "reported_date", "warranty_related", "resolution"]
      - node_type: "Certificate"
        properties: ["certificate_id", "type", "issue_date", "expiry_date"]
      - node_type: "Lesson"
        properties: ["reference_stage", "observation", "corrective_action"]
    relationships:
      - "Project HAS Stage"
      - "Stage INCLUDES Snag"
      - "Snag ASSIGNED_TO Trade"
      - "Snag LINKED_TO Photo"
      - "Defect LINKED_TO Warranty"
      - "Stage GENERATES Lesson"
      - "Lesson INFORMED_BY Feedback"
      - "Certificate VALIDATES Stage"
    graph_query_examples:
      - name: "Find all unresolved snags by trade"
        query: "MATCH (t:Trade)-[:ASSIGNED_TO]->(s:Snag {status:'open'}) RETURN t.name, count(s)"
      - name: "Identify recurring defects"
        query: "MATCH (d:Defect)-[:LINKED_TO]->(t:Trade) RETURN t.name, count(d) ORDER BY count(d) DESC"

  api_endpoints:
    - name: "POST /api/v1/snag"
      purpose: "Create or update snag items from mobile or desktop client."
      payload: "snagging_register item"
      response: "snag_id, status"
    - name: "GET /api/v1/report"
      purpose: "Generate project-level QA report."
      parameters: ["project_id", "period_start", "period_end"]
      response: "JSON analytics payload"
    - name: "GET /api/v1/photos/{snag_id}"
      purpose: "Retrieve linked images for a snag item."
      response: "array of URLs"
    - name: "POST /api/v1/feedback"
      purpose: "Submit client satisfaction data."
      payload: "feedback_form"
      response: "success/failure"

  dashboard_integration:
    description: "Defines metrics visualised in Aven’s dashboard or external BI tool."
    visuals:
      - title: "Snag Status Overview"
        type: "pie_chart"
        data_source: "snagging_register.status"
      - title: "Defect Density by Room"
        type: "heatmap"
        data_source: "defect_density_analysis.hotspots"
      - title: "Trade Performance Trend"
        type: "line_chart"
        data_source: "trade_performance.trend"
      - title: "Cost Breakdown"
        type: "bar_chart"
        data_source: "cost_analysis.cost_by_trade"
      - title: "Stage Quality Scores"
        type: "gauge"
        data_source: "stage_quality_scores.inspection_score_percent"
      - title: "Risk and Mitigation Tracker"
        type: "table"
        data_source: "risk_assessment.risk_items"
      - title: "Client Experience"
        type: "sentiment_chart"
        data_source: "client_experience_dashboard.key_themes"

  user_roles_and_permissions:
    - role: "Site Manager"
      access: ["inspections", "snagging_register", "analytics"]
      write: true
    - role: "Subcontractor"
      access: ["assigned_snags", "upload_photos"]
      write: true
    - role: "Client"
      access: ["summary_reports", "feedback_form"]
      write: limited
    - role: "Aven Engine"
      access: ["all"]
      write: restricted
    - role: "QA Auditor"
      access: ["reports", "risk_assessment", "lessons_learned"]
      write: true

  notifications_and_triggers:
    - trigger: "New snag logged"
      action: "Notify responsible_party via email and Aven chat"
    - trigger: "Snag overdue > 7 days"
      action: "Escalate to Site Manager and QA Auditor"
    - trigger: "Certificate uploaded"
      action: "Mark checklist item complete"
    - trigger: "Client feedback received"
      action: "Add to knowledge graph and analytics refresh queue"

  data_backup_and_security:
    backup_frequency: "daily"
    encryption: "AES-256"
    access_control: "role-based"
    retention_policy_months: 36
    audit_log_enabled: true
    last_backup: null

```

| Layer                            | Function                                                  | Outcome                                                   |
| -------------------------------- | --------------------------------------------------------- | --------------------------------------------------------- |
| **`file_management`**            | Handles all visual and certificate evidence with metadata | Every snag or test is traceable to a file                 |
| **`aven_knowledge_graph`**       | Core intelligence layer                                   | Links everything — stages, trades, lessons — for querying |
| **`api_endpoints`**              | Connects front-end or mobile app                          | Enables push/pull between inspection tools and dashboard  |
| **`dashboard_integration`**      | Defines visual metrics                                    | Gives live, board-ready project quality reporting         |
| **`user_roles_and_permissions`** | Secures access                                            | Ensures audit integrity and accountability                |
| **`notifications_and_triggers`** | Automates alerts                                          | Keeps site teams responsive                               |
| **`data_backup_and_security`**   | Protects records                                          | Provides evidential continuity for insurers and clients   |