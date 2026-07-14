---
name: technical-presentation-storytelling
description: Turn complex technical research into clear, audience-centered presentation narratives, especially learning guides, architecture explainers, POC proposals, and role-readiness decks. Use alongside the powerpoint skill when the challenge is not only creating a PPTX but deciding what the audience should understand, in what order, and from whose perspective.
version: 1.0.0
created_by: agent
metadata:
  hermes:
    tags: [presentation, storytelling, technical-communication, architecture, poc, learning-roadmap]
    related_skills: [powerpoint, architecture-diagram]
---

# Technical Presentation Storytelling

Use this skill when a user asks to make complex technical material “easy to understand,” “visible at a glance,” suitable for executives or non-specialists, or explicitly framed from the user’s own perspective.

This skill governs **narrative, information hierarchy, and presentation QA**. Use the `powerpoint` skill for PPTX mechanics and rendering.

## Core principle

Do not convert a long answer into slides verbatim. Rebuild it as a decision-oriented story:

1. What is the audience worried about?
2. What does the presenter already know?
3. What is genuinely new?
4. How does the system work?
5. What should happen next?

A good technical deck lets a reader understand the thesis from slide titles alone.

## Workflow

### 1. Define presenter, audience, and decision

Before outlining, identify:

- Presenter’s current expertise and credibility.
- Audience’s likely technical level.
- The decision or action expected after the presentation.
- Whether the deck is for self-study, kickoff, approval, design review, or POC closure.

When the user says “from my perspective,” write the deck around **their position and responsibilities**, not as a generic vendor brochure.

### 2. Write the one-sentence thesis

Create one sentence that should remain in the audience’s memory. Examples of useful patterns:

- “I am not starting from zero; my existing expertise transfers, and I only need to close specific gaps.”
- “The technology is familiar, but the control plane and responsibility boundary have changed.”
- “The POC must prove operability, not merely successful provisioning.”

Put this thesis on the cover or executive-summary slide.

Avoid invented readiness percentages unless there is a defensible scoring model.

### 3. Build a comprehension-first slide sequence

For a readiness or POC deck, prefer this sequence:

1. Title and personal framing.
2. One-page executive summary.
3. Plain-language architecture.
4. Existing knowledge versus new knowledge.
5. Learning priorities.
6. Provisioning or execution flow.
7. POC success criteria.
8. Role and responsibility split.
9. Risks and preconditions.
10. What can be delegated versus what requires the user.
11. Short learning/execution roadmap.
12. Questions to ask and immediate next step.
13. Sources or appendix.

Remove slides that do not advance understanding or a decision.

### 4. Make every slide answer one question

Use a declarative title, not a topic label alone.

Weak: `Architecture`

Strong: `The infrastructure is in AWS, but database control is split across AWS and OCI`

Keep supporting text subordinate to the title. Prefer:

- 3–5 cards,
- a comparison,
- a process flow,
- a role split,
- or a short checklist.

Avoid paragraphs and dense tables.

### 5. Translate jargon without erasing it

Show the official term and its plain-language meaning together.

Examples:

- `ODB Network` — private network that hosts the database-side resources.
- `Control Plane` — where resources are created and managed.
- `Peering` — private path between the application network and database network.

Use consistent colors for domains, providers, or responsibilities across the deck. Do not rely on color alone; add labels and line styles.

### 6. Show personal role boundaries

For cross-functional technology, explicitly separate:

- What the presenter leads.
- What another specialist leads.
- What is jointly owned.
- What requires commercial, security, or operational approval.

This prevents a learning deck from implying that the presenter must become an expert in every adjacent domain.

### 7. Turn POC claims into evidence

A POC slide should define completion using evidence such as:

- Provisioning records.
- Connectivity tests.
- Performance measurements.
- Backup and actual restore.
- HA/DR behavior and RPO/RTO.
- Security and audit logs.
- Monitoring evidence.
- Cost and operational runbooks.

Prefer “measurement + log + reproducible runbook” over screenshots alone.

### 8. Cite authoritative sources

For rapidly changing cloud products:

- Prefer vendor product documentation over blogs.
- Put a verification date on the deck.
- Add a source slide or compact slide-level citations.
- State that regions, capacity, service support, and commercial terms must be reconfirmed before execution.

### 9. Perform content and visual QA

At minimum:

1. Generate the PPTX.
2. Validate its ZIP structure.
3. Convert to PDF.
4. Extract PDF or PPTX text to check omissions and ordering.
5. Render every slide to images.
6. Inspect a contact sheet for global consistency.
7. Inspect dense architecture and process slides individually.
8. Use an independent visual reviewer when available.
9. Fix at least one identified issue and rerender affected slides.
10. Verify slide count, page size, final file path, and checksum.

Check especially:

- Korean text wrapping in narrow cards.
- Low contrast on pale badges and orange backgrounds.
- Labels covering connectors or panel boundaries.
- Font substitution that changes line breaks.
- Footer collisions and unsafe edge margins.
- English terms split awkwardly across lines.

For executive cloud/pricing decks, apply measurable release gates rather than visual judgment alone:

- Every text box must leave at least 0.50 in at the bottom edge; target 0.58–0.60 in.
- Source/footer text must be at least 10.5 pt.
- Chart axis/unit text must be at least 10 pt and terminal value labels at least 12 pt.
- URLs and commercial/legal caveats must be at least 11 pt.
- Normal text contrast must be at least 4.5:1.
- Parse PPTX XML to verify geometry and font sizes; also verify ZIP integrity, slide count, 16:9 dimensions, PDF page count, and rendered-image count.
- A fix requires a fresh independent re-review of the regenerated PPTX, PDF, and renders. Do not treat the previous review as approval of the revised artifact.

For dated cloud-price comparisons, follow the evidence and seven-slide narrative pattern in `references/cloud-pricing-comparison-decks.md`.

### 10. Isolate rendering failures systematically

If a full deck opens but PDF export fails:

- Do not assume the whole deck is corrupt.
- Export progressively larger slide subsets to locate the first problematic slide.
- Regenerate or simplify that slide, especially unusual shapes, connector labels, or unsupported effects.
- Export with a fresh office user profile and a unique intermediate output name.
- Rebuild the final artifact from the verified deck, then validate again.

Capture the successful isolation method, not a transient claim that a renderer is broken.

## Design guidance

- Use 16:9 unless a template dictates otherwise.
- Use one dominant dark or neutral color and provider/domain accents.
- Give each slide a visual device: cards, flow, comparison, role map, or checklist.
- Use readable Korean fonts with regular or medium weight.
- Keep body text large enough for projection.
- Use high-contrast text on accent colors; avoid white text on bright yellow-orange.
- Keep architecture diagrams conceptual unless the audience needs deployable detail.

## Final delivery

Report:

- Presentation status.
- Slide count and aspect ratio.
- PPTX and optional PDF absolute paths.
- Sources and verification date.
- QA performed and any limitation.
- Independent reviewer status if required; never imply completion while review is still pending.

See `references/cloud-architecture-deck-patterns.md` for reusable slide patterns and a concise QA checklist.
