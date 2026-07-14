# Organization Change Checklist

Use this checklist for adding, renaming, or materially changing a specialist in a Hermes profile-based organization.

## Intake

- [ ] Goal and scope identified.
- [ ] New role does not duplicate an existing primary domain.
- [ ] Neighboring-role handoffs specified.
- [ ] User-facing coordinator remains the single default command channel.
- [ ] Internal target deadline includes date, time, and timezone and is marked as an assumption if user did not provide it.

## Profile

- [ ] `hermes profile list` inspected before creation.
- [ ] Profile name is lowercase and routing-friendly.
- [ ] Profile created with `--description` for Kanban auto-routing.
- [ ] Configuration cloned from the closest working profile when appropriate.
- [ ] Cloned `SOUL.md` replaced with the new role contract.
- [ ] `hermes profile show <role>` confirms path, model, alias, `.env`, and `SOUL.md`.

## Role contract

- [ ] Reporting chain points to the coordinator/Kanban rather than directly to the user.
- [ ] In-scope work listed.
- [ ] Out-of-scope work and handoffs listed.
- [ ] External send/post approval gate included.
- [ ] Payment/purchase approval gate included.
- [ ] Destructive delete approval gate included.
- [ ] Contract/legal commitment approval gate included.
- [ ] Domain-specific high-risk changes are gated.
- [ ] Secret-handling rule included.
- [ ] Evidence, verification, rollback, and known-issues fields required.
- [ ] Permanent artifact path included.

## Shared governance

- [ ] Coordinator `SOUL.md` organization list updated.
- [ ] Coordinator routing rule updated.
- [ ] Execution-versus-review ownership updated.
- [ ] Minimum-team count updated.
- [ ] Organization README hierarchy updated.
- [ ] Operating-model role table and ownership updated.
- [ ] Task-template assignee options updated.
- [ ] Role artifact directory and README created.
- [ ] Stale old role counts searched and removed.

## Diagram

- [ ] Editable SVG produced.
- [ ] Self-contained HTML contains inline SVG.
- [ ] PNG rendered at 2000×1125 or greater for Slack.
- [ ] User ↔ coordinator arrows are directional and labeled.
- [ ] Every specialist card is visible.
- [ ] Coordinator connects to every specialist.
- [ ] Every specialist joins the shared repository bus.
- [ ] Producer and operational-role arrows point toward quality review.
- [ ] No premature static `PASS` badge.
- [ ] Full-size visual QA passes.
- [ ] Thumbnail render succeeds and core labels remain understandable.
- [ ] No clipping, overlap, broken Korean glyphs, orphan text, or floating arrows.

## Runtime verification

- [ ] `<role> doctor` exits successfully for required capabilities.
- [ ] `<role> chat -Q -q '<role smoke test>'` returns the expected identity/boundary.
- [ ] Optional integration warnings are separated from blocking readiness defects.

## Independent quality card

Card body includes:

- [ ] Background and goal.
- [ ] Assignee=`quality`.
- [ ] Enumerated completion criteria.
- [ ] Exact deadline and timezone.
- [ ] Inputs and authoritative paths.
- [ ] Output report path.
- [ ] Approval requirement.
- [ ] Prohibited external actions.

Completion checks:

- [ ] Dispatcher actually spawned the quality profile.
- [ ] Task reached `done`, not merely `running`.
- [ ] Verdict is one of PASS / CONDITIONAL PASS / FAIL / BLOCKED.
- [ ] Report exists at the declared absolute path.
- [ ] Task metadata contains criteria, evidence, defects, risks, approval check, deadline status, and limitations.
- [ ] Report and key artifacts are read back or checksummed by the coordinator.

## Final report

- [ ] Status and deadline status.
- [ ] Implementer and independent reviewer.
- [ ] Profile name/path/model/alias.
- [ ] Doctor and smoke-test evidence.
- [ ] Kanban task ID and verdict.
- [ ] Absolute paths and user-viewable media attachment.
- [ ] Risks, limitations, unresolved decisions.
- [ ] Persistent organization memory updated only after verification passes.
