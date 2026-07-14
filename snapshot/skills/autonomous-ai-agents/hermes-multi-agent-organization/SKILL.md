---
name: hermes-multi-agent-organization
description: Design, extend, document, visualize, and independently verify profile-based Hermes Agent organizations coordinated through Kanban.
version: 1.1.0
created_by: agent
metadata:
  hermes:
    tags: [hermes, profiles, kanban, multi-agent, organization-design, governance, diagrams, quality-assurance]
    related_skills: [hermes-agent, architecture-diagram]
---

# Hermes Multi-Agent Organization

Use this skill when creating or changing a durable organization made of named Hermes profiles, a coordinating profile, a shared Kanban board, role-specific artifact directories, and independent quality review.

This skill governs the **organization lifecycle** rather than Hermes installation itself. Load the protected `hermes-agent` skill and consult the current official Hermes docs for authoritative profile and Kanban commands.

## Core model

A robust small organization has:

- One user-facing coordinator/orchestrator.
- A minimal set of named specialist profiles with non-overlapping primary domains.
- A shared Kanban board for durable assignments and audit trails.
- Role-specific artifact directories.
- Explicit approval gates for external, financial, destructive, legal, and high-risk operational actions.
- Independent quality review for important results.

Profiles are identity and state boundaries, not filesystem sandboxes. Role instructions guide behavior but do not replace OS-level access controls.

## Workflow

### 1. Discover the live organization

Before changing anything, inspect:

- `hermes profile list` and `hermes profile show <name>`.
- Coordinator and specialist `SOUL.md` files.
- Organization README, operating model, and task-card template.
- Named Kanban board location and current state.
- Existing artifact directories and diagrams.

Do not rely on an earlier chat summary when the live files and CLI are available.

### 2. Define the new role before creating it

Specify:

- Primary domain and representative outputs.
- Explicit exclusions and handoff boundaries with neighboring roles.
- Required inputs, completion evidence, and artifact path.
- Approval gates and high-risk actions.
- Which role performs independent review.

A specialist should return out-of-domain work to the coordinator instead of silently expanding scope.

### 3. Create the profile from the closest working role

Prefer cloning configuration from a nearby proven profile while giving Kanban a routing description:

```bash
hermes profile create <role> \
  --clone-from <closest-profile> \
  --description "<one or two sentences describing routing expertise>"
```

Immediately replace the cloned `SOUL.md`; cloning a profile intentionally copies the source identity and is not the final role definition.

Keep gateways stopped unless that specialist needs its own messaging identity. Kanban workers can be spawned on demand without a dedicated gateway.

### 4. Write a complete role contract

The specialist `SOUL.md` should contain:

1. Identity and reporting chain.
2. In-scope responsibilities.
3. Out-of-scope responsibilities and handoffs.
4. Approval gates.
5. Evidence and verification requirements.
6. Independent-review requirements.
7. Required completion metadata.
8. Permanent artifact directory.

For operational roles, require read-only diagnosis first and a written impact, dependency, backup, verification, rollback, maintenance-window, and approval plan before high-risk change.

### 5. Update the coordinator and shared governance atomically

Update every durable source of truth in the same change:

- Coordinator `SOUL.md`: organization list, routing rule, execution/review separation, current minimum-team statement.
- Organization README: hierarchy and artifact directory.
- Operating model: role table, representative outputs, ownership, review relationships.
- Task template: new assignee option and approval/review fields.
- Role artifact directory with a short purpose README.

Search for stale role counts such as “4 managers” after adding a fifth role.

### 5a. Rename an organization without breaking its history

Treat the public organization name and technical identifiers as separate layers:

- Rename the Kanban **display name** with `hermes kanban boards rename <slug> "<new name>"`; the slug is immutable and may remain an internal compatibility identifier.
- Preserve an established board slug, DB path, workspace path, and artifact root unless the user explicitly requests a storage migration. Renaming a concept does not require moving its history.
- Update the coordinator identity, every specialist reporting-chain sentence, README, operating model, task template, board description, diagram accessibility text, titles, legends, and footer in one pass.
- Create canonical diagram files under the new public name while updating any legacy-named preview files that existing links may still reference. Never leave an old-name artifact containing stale public branding.
- Document the compatibility policy explicitly: which name is public and which slug/path remains internal.
- Verify both absence of stale public-name phrases in active governance files and presence of the new name/role wording. Historical audit reports may retain the old name as history and should not be rewritten merely for branding.

See `references/organization-rename-migration.md` for the migration and verification checklist.

### 6. Update the organization diagram

Produce all three forms:

- Editable SVG.
- Self-contained HTML with inline SVG.
- High-resolution PNG suitable for messaging previews.

Diagram invariants:

- User ↔ coordinator flows are explicit and directional.
- Every specialist has a visible card and a direct coordinator connection.
- Every specialist connects to one shared result bus/repository.
- Producer → quality-review arrows point toward the reviewer.
- The diagram does not claim `PASS` before verification; use a neutral configuration badge until QA completes.

For a 16:9 Slack artifact, render at least 2000×1125 and test both full-size and thumbnail readability.

### 7. Verify real execution

At minimum run:

```bash
hermes profile show <role>
hermes profile list
<role> doctor
<role> chat -Q -q '<short role-boundary smoke test>'
```

Verify the response reflects the new role and approval boundary. A profile existing on disk is not enough.

Treat optional-tool warnings separately from role readiness. Report them as limitations; do not fail the profile if its configured model, auth, core chat, and required task tools work.

### 8. Use a real independent quality card

For an important organization change, create a Kanban task assigned to the quality profile. The card must include:

- Background and goal.
- Assignee.
- Enumerated completion criteria.
- Exact deadline with timezone; label coordinator-set deadlines as assumptions.
- Inputs and artifact paths.
- Approval requirement.
- Independent-review purpose and prohibited external actions.

Dispatch the card and wait for `done`; do not equate process spawn with completion. Read back the report and task metadata before reporting success.

### 9. Report evidence, not assertions

The final report should include:

- Status.
- Implementer and reviewer.
- New profile name, path, model, and alias.
- Doctor and smoke-test results.
- Kanban task ID and verdict.
- Absolute artifact paths.
- Deadline status.
- Limitations and any decision still needed.

## Diagram rendering pitfalls

- Some SVG rasterizers handle CSS filters and `rgba(...)` presentation attributes inconsistently. If cards disappear in PNG, use solid hex fills and simple strokes, then rerender and visually inspect the pixels.
- Connect outer cards to a common bus before entering a narrower repository card. Direct vertical arrows outside the repository width look disconnected.
- A label placed in a narrow inter-card gap may be hidden by later-drawn cards. Put essential semantics inside the reviewer card and use directional arrows in the gap.
- Draw connectors before opaque cards so lines remain behind nodes, but verify arrowheads are still visible at card boundaries.
- When embedding `read_file` output into HTML programmatically, strip its display line-number prefixes before writing; never persist the tool’s numbered display text.

## Kanban verification pitfalls

- A task card’s `--skill` is resolved inside the **assignee profile**, not the coordinator profile. Before forcing a skill, verify it is discoverable/loadable under that profile (profile-scoped skill list or a short load smoke test). If it is absent, either omit `--skill` and put the necessary source paths/rules in the card body, or perform an explicitly authorized profile installation first. Do not consume the failure circuit with retries that can only repeat `Unknown skill(s)`.
- When independent quality returns FAIL, keep the failed report as evidence and create one producer-owned repair card followed by a dependent quality re-review card. The overall deliverable is not complete until the re-review reaches PASS; give both repair and re-review cards their own exact deadlines and approval boundaries.
- Vision-enabled quality workers may take several minutes. Check task status and the per-task log; a living process with advancing heartbeats is not stuck.
- For asynchronous visual QA, never let the reviewer inspect mutable generic filenames that may become stale after edits. Render each revision into a revision-specific directory, record the source artifact hash or revision ID in the review card, and re-review every slide changed after dispatch. Treat findings against an older render as useful input, not as verification of the current final artifact.
- After applying visual-QA findings, distinguish actual pixel defects from OCR or text-extraction artifacts. Confirm suspected overlap, clipping, or odd spacing against a freshly rendered slide image before editing source text; then complete at least one fix-and-rerender cycle.
- A failed verification assertion may be a test-expression error rather than a product defect. Correct the assertion and rerun it; record the false negative transparently in the quality report.
- Enforce a **single writer per artifact tree or mutable state domain**. Coordinator actions and duplicate repair cards can race with workers, stale checksums, and make an otherwise correct report contradict live state. Serialize overlapping outputs with dependencies and immediately annotate a running card if the coordinator changes shared state.
- Before creating a repair card, inspect whether the producer or reviewer already created one for the same paths. Keep one producer-owned repair stream followed by one independent re-review stream. Recheck the parent’s children immediately before dispatch: a reviewer can create a repair card after the coordinator’s first inspection. If duplicates race into `running`, reclaim and archive the duplicate before the next dispatch, record the superseding card IDs, and preserve the role-specific single writers.
- Assign exactly one card-creation authority for every repair/re-review edge. If a reviewer or producer is explicitly required to create the next card, the coordinator must wait for that parent to finish, inspect its children, and reuse the created card rather than pre-creating a duplicate. If the coordinator owns follow-up creation, tell the worker to report findings only and not create children. This prevents races where two valid re-review cards target the same mutable artifact.
- A producer may finish every acceptance check yet mark its card `blocked` only because independent review is still required. Treat that as a workflow-state error rather than a product defect: read the handoff and independently rerun the producer checks; if they pass, complete the producer card with structured evidence so its dependent quality card can start. Never do this when an approval, test, or substantive defect is actually unresolved.
- Every child and re-review card needs its own exact deadline with timezone; inheriting or merely mentioning a parent's deadline is insufficient. Put the deadline in the card body at creation time. A later comment is useful operational context but is not a substitute for a complete card body; if a worker-created card is missing required fields, replace it with one complete coordinator-owned card before dispatch rather than preserving incomplete audit metadata.
- Promote reviewed skills in stages: isolated loader test → independent candidate PASS → authorized active-profile installation → byte-map comparison → new-session behavior smoke tests → independent installed-state PASS. Do not equate a candidate PASS with installation verification.
- Rich CLI tables may ellipsize long skill names, so exact-name filtering can report a false negative. Use a wide terminal, structured output when available, or inspect the unfiltered table before changing paths.
- Verify external side effects by reading the created profile, report, and artifacts back from their authoritative paths.

See `references/concurrent-work-and-skill-promotion.md` for the single-writer, repair, and reviewed-skill promotion checklist.

## Reference

Use `references/organization-change-checklist.md` for a reusable implementation and acceptance checklist, including evidence fields and diagram QA criteria.
