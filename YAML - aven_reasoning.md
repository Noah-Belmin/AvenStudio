
**Phase 5: Aven Reasoning Layer** — a compact, production-ready spec for intents, rules, scoring, explanations, and playbooks. It’s designed so you can bolt it onto your current YAML, feed it into a small rules engine, or implement in Python with a few modules (parsers → resolvers → graph queries → rationale generator).


```YAML
aven_reasoning:
  version: 1.0
  objectives:
    - "Answer natural-language questions about quality, risk, deadlines, and cost."
    - "Proactively flag issues that threaten handover, safety, warranty or retention."
    - "Recommend concrete next actions with owners and due dates."
    - "Explain decisions with transparent evidence links (photos, certs, checks)."

  # ── 1) INTENTS → what users ask in plain English
  nlu_intents:
    - intent: "snag_status_overview"
      utterances:
        - "What’s the current snag status?"
        - "How many open snags and where?"
        - "Show severe issues by room."
      slots: ["stage?", "trade?", "severity?"]
      to_pipeline: ["resolve_filters", "query_snags", "aggregate", "compose_answer"]

    - intent: "critical_path_to_handover"
      utterances:
        - "What blocks practical completion?"
        - "Can we hand over this week?"
      slots: ["target_date?"]
      to_pipeline: ["compute_handover_blockers", "compose_answer"]

    - intent: "trade_performance_review"
      utterances:
        - "How is plumbing performing?"
        - "Which subcontractor is causing delays?"
      slots: ["trade", "period?"]
      to_pipeline: ["query_trade_metrics", "rank_performance", "compose_answer"]

    - intent: "certificate_compliance"
      utterances:
        - "Are we missing any certificates?"
        - "List compliance gaps for handover."
      slots: ["stage?"]
      to_pipeline: ["query_cert_gaps", "compose_answer"]

    - intent: "risk_forecast"
      utterances:
        - "Where are we likely to slip?"
        - "Risk outlook for next fortnight?"
      slots: ["period?"]
      to_pipeline: ["predict_risk", "compose_answer"]

    - intent: "cost_exposure"
      utterances:
        - "What’s our rectification cost to date?"
        - "Cost at risk by trade."
      slots: ["trade?", "severity?"]
      to_pipeline: ["query_costs", "compose_answer"]

    - intent: "action_recommendations"
      utterances:
        - "What should we do next?"
        - "Give me a plan to close snags before Friday."
      slots: ["deadline", "scope?"]
      to_pipeline: ["generate_actions", "compose_answer"]

  # ── 2) DATA RESOLUTION → map vague language to filters/IDs
  resolution:
    defaults:
      severity_weighting:
        critical: 5
        major: 3
        minor: 1
        cosmetic: 0.5
      sla_days_by_severity:
        critical: 2
        major: 5
        minor: 10
        cosmetic: 20
    synonyms:
      trades:
        plumbing: ["plumber", "mechanical", "sanitary"]
        electrical: ["sparky", "power", "lighting"]
        carpentry: ["joinery", "doors", "skirting"]
    rooms_normaliser: "use floor plan alias map (e.g., 'bed 1' → 'Bedroom 1')"
    date_resolver:
      phrases:
        "this week": "next 7 days"
        "fortnight": "next 14 days"
        "month": "next 30 days"

  # ── 3) RULES & SCORING → how Aven decides priority and risk
  rules_engine:
    priority_score:
      formula: |
        priority = (severity_weight * 0.6)
                 + (overdue_days_clamped * 0.2)
                 + (handover_critical_flag * 2)
                 + (repeat_offender_flag * 1)
                 + (certificate_dependency_flag * 1.5)
      fields:
        overdue_days_clamped: "max(0, min(30, days_open - SLA_for_severity))"
        handover_critical_flag: "1 if snag blocks certificate or life-safety else 0"
        repeat_offender_flag: "1 if same trade & defect_type appears ≥3 times in 30 days"
        certificate_dependency_flag: "1 if snag blocks a required certificate, else 0"
    handover_blocker_logic:
      - condition: "any(compliance_certificates == false where required_for_PC == true)"
        label: "Certificate Missing"
      - condition: "exists(snag where severity in [critical, major] and status != verified)"
        label: "High-severity Snags Open"
      - condition: "commissioning_tests_incomplete == true"
        label: "Commissioning Incomplete"
      - condition: "client_demo_pending == true"
        label: "Client Demonstration Outstanding"
    risk_model:
      risk_score_formula: |
        risk = (open_critical * 5) + (open_major * 3) + (trend_declining * 2)
             + (avg_resolution_days_over_sla * 0.5) + (cert_gap_count * 2)
      thresholds:
        low: "< 8"
        medium: "8–15"
        high: "> 15"

  # ── 4) QUERIES → declarative views over your existing stores/graph
  query_library:
    query_snags:
      description: "Pull snags with optional filters."
      inputs: ["stage?", "trade?", "severity?"]
      graph_match:
        - "MATCH (s:Snag) WHERE filters RETURN s"
      returns: ["count", "by_room", "by_severity", "top10_by_priority"]
    compute_handover_blockers:
      description: "Derive blockers for practical completion."
      steps:
        - "check certificate_compliance()"
        - "check open_high_severity_snags()"
        - "check commissioning_status()"
        - "compose blocker list with evidence"
    query_trade_metrics:
      description: "Aggregate KPIs for a trade."
      returns:
        - snags_open
        - snags_closed
        - avg_resolution_days
        - overdue_count
        - recurring_issue_types
    query_cert_gaps:
      description: "List missing or expired certificates relevant to PC/BC."
      returns: ["missing", "pending_signoff", "expiring_soon(<=30d)"]
    query_costs:
      description: "Compute cost exposure."
      returns: ["total", "by_trade", "by_severity", "avg_per_snag"]
    predict_risk:
      description: "Blend trend lines + current blockers into risk band."
      returns: ["risk_score", "band", "drivers"]

  # ── 5) ACTION PLAYBOOKS → standard responses Aven can propose
  playbooks:
    - name: "Close-Out Criticals in 72h"
      trigger: "risk_band == 'high' OR open_critical > 0"
      actions:
        - "Escalate to Site Manager & QA Auditor."
        - "Auto-assign top 10 priority snags to responsible trades."
        - "Set 48–72h deadlines; attach photos & acceptance criteria."
        - "Schedule re-inspection; notify client of plan."
    - name: "Certificate Catch-Up"
      trigger: "cert_gap_count > 0"
      actions:
        - "Generate checklist: which certs, issuing body, evidence paths."
        - "Request uploads via subcontractor portal."
        - "Block retention release until gaps resolved."
    - name: "Recurring Defect Root-Cause"
      trigger: "repeat_offender_flag == 1"
      actions:
        - "Open RCA task; request method statement review."
        - "Enforce pre-handover QA signoff for affected trade next 2 weeks."
    - name: "Cost Containment"
      trigger: "cost_at_risk > threshold"
      actions:
        - "Flag high-cost snags to Commercial Manager."
        - "Recommend alternative remedial methods/materials."

  # ── 6) EXPLANATION & EVIDENCE → transparent, auditable answers
  explainability:
    include:
      - "formula_used"
      - "input_values"
      - "evidence_links"   # photo paths, certificate files, inspection IDs
      - "trade_owner"
      - "next_check_date"
    answer_templates:
      concise: |
        **Summary:** {headline}
        **Why:** {drivers}
        **Evidence:** {links}
        **Next actions:** {playbook_items}
      detailed: |
        ## Summary
        {headline}

        ## Reasoning
        {reasoning_steps}

        ## Evidence
        {evidence_table}

        ## Recommended Actions
        {playbook_items}

  # ── 7) PROACTIVE SIGNALS → Aven pushes, not just answers
  watchdogs:
    - name: "Overdue SLA"
      condition: "any(snag.days_open > SLA_for_severity)"
      notify: ["Site Manager", "Responsible Trade"]
      propose_playbook: "Close-Out Criticals in 72h"
    - name: "Handover at Risk"
      condition: "handover_blockers_count > 0 within next_7_days"
      notify: ["Project Board", "Client (summary)"]
      propose_playbook: "Certificate Catch-Up"
    - name: "Certification Expiry"
      condition: "any(certificate.expiry_date <= 30d)"
      notify: ["QA Auditor"]
      propose_playb_

```



This is an example of how we can model how **Aven interprets and reasons** over this graph — e.g. how its “contextual awareness” lets it answer questions like:

> “Show me all unresolved critical snags affecting warranty release,”  
> “Which trades consistently miss target fix dates?”  
> “What’s the risk trend for plumbing defects month-on-month?”

This reasoning layer provides the logic and contextual query model that lets your AI understand and act on this data, rather than just display it?


## How this runs (straightforward mental model)

1. **Detect intent** → map the user’s question to an intent and filters.
2. **Resolve** terms → “sparky” → Electrical; “fortnight” → 14 days.
3. **Query** graph/tables → pull snags, certs, costs.
4. **Score** risk/priority using the formulas.
5. **Choose playbook(s)** based on triggers.
6. **Explain** — include formulas, inputs, and file evidence so decisions are auditable.
7. **Notify** (if proactive) — route to the right roles, respecting client view filters.
    

---

## Example interactions (grounded and auditable)

### Q: “Are we safe to hand over next Friday?”

- **Intent**: `critical_path_to_handover`
    
- **Outcome**: Aven checks handover blockers:
    
    - 2 major snags not verified (kitchen worktop seal; stair nosing)
    - **Electrical Installation Certificate** pending upload
    - MVHR commissioning log missing
        
- **Answer (concise template)**:
    
    - **Summary**: _Handover at risk due to certification and two major unverified snags._
    - **Why**: Cert gap (EIC), commissioning incomplete, 2 majors outstanding.
    - **Evidence**: links to snag photos and cert placeholders
    - **Next actions**: Playbook “Certificate Catch-Up” + schedule re-inspection in 72h.
        

### Q: “Which trade is hurting us most this month?”

- **Intent**: `trade_performance_review`
- **Aven**: aggregates avg resolution days, overdue count, repeat defects → ranks trades.
- **Answer**: _Plumbing trending down: 7 open, avg resolution 9.3 days (SLA 5), repeat ‘sealant gap’ in 4 rooms._
    

### Q: “What should we do today to de-risk?”

- **Intent**: `action_recommendations` (deadline=today)
- **Aven**: pulls top 10 priority snags, maps owners, proposes a 1-day strike list with booking windows.


---

## Implementation notes (keep it simple, keep it testable)

- **Pipelines**: tiny Python services work fine:
    
    - `nlu.py` (regex + keyword + optional LLM for long queries)
    - `resolver.py` (synonyms, date math, room map)
    - `queries.py` (graph or SQL views)
    - `rules.py` (formulas above, pure functions)
    - `playbooks.py` (returns tasks + notifications)
    - `compose.py` (explainable answers with evidence links)
        
- **Unit tests** focus on rules functions (inputs → exact priority/risk outputs) and intent routing.
- **Transparency**: always show _why_ with the numbers you used. That’s how you build trust with clients and subs.
    

---

If you want, I can now generate a **ready-to-drop `/config/` folder** with:

- `intents.yaml`, `rules.yaml`, `playbooks.yaml`, and
    
- a **Python scaffold** (`resolver.py`, `rules.py`, `compose.py`) using your UK terminology and severity SLAs.