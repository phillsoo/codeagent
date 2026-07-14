# Cloud Architecture Deck Patterns

Use these patterns when explaining a service that spans providers, control planes, networks, or operating teams.

## 1. Three-zone architecture

Lay out the system left to right:

1. **Application zone** — where callers or workloads run.
2. **Service/data zone** — where the managed platform physically runs.
3. **Management zone** — where the control plane, identity, backup, or observability services live.

Show data and management paths differently:

- Solid arrow: application or data traffic.
- Dashed arrow: management/control traffic.
- Label each connector without covering panel borders.

Under the diagram, summarize the split in one sentence: physical location, data path, and management owner.

## 2. Transferable knowledge versus new gaps

Use two balanced columns:

- **What I already know:** core platform, database, operations, migration, performance.
- **What I need to add:** cloud networking, identity, dual control planes, commercial onboarding, provider support boundaries.

This pattern reassures the presenter without overstating readiness.

## 3. Learning-priority ladder

Order topics by dependency, not by documentation order:

1. Network/address design.
2. Connectivity and routing.
3. Control-plane boundaries.
4. IAM/security/audit.
5. Operations, DR, cost, and support.

Each row should contain topic, concrete subtopics, and priority label.

## 4. Provisioning flow

Use 5–8 numbered steps. For each step, show:

- Resource or action.
- Two short configuration examples.
- Owner color.

Add a role strip beneath the flow showing what the presenter leads and what another team co-owns.

## 5. POC evidence grid

Use a 2×4 grid for eight proof areas:

- Provisioning.
- Connectivity.
- Performance.
- Backup and actual restore.
- HA/DR.
- Security.
- Observability.
- Cost and operations.

End with the completion rule: measurement + log + reproducible runbook.

## 6. Three-party responsibility map

Use three columns:

- Presenter/platform specialist.
- Cloud/network team.
- Vendor or managed-service operator.

For each, list only five responsibilities. Show joint ownership in wording rather than duplicating every bullet.

## 7. Risk gate list

For each risk, show:

- Risk title.
- Why it blocks the POC.
- Preventive action.

Common cloud-service gates include immutable address ranges, account linking, IAM permissions, regional capacity, and support escalation paths.

## 8. Delegation boundary

Split the slide into:

- Work an assistant can prepare: research, comparison, architecture draft, policy draft, runbook, test plan, result analysis, reporting.
- Work requiring the user or organization: requirements, credentials, commercial acceptance, security approval, production change, final decision.

## Compact visual QA checklist

- No title or body text wraps unexpectedly after PDF conversion.
- Korean and English do not split awkwardly inside narrow cards.
- Accent badges meet readable contrast.
- Connector labels do not cover arrowheads or panel borders.
- Every slide has a clear takeaway visible from the title.
- Footer and sources remain inside safe margins.
- Dense slides are checked individually, not only in a contact sheet.
- At least one issue from the first pass is fixed and rerendered.
