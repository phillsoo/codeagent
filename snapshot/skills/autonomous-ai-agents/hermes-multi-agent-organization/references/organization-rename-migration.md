# Organization Rename and Compatibility Checklist

Use this when changing the public name of an existing Hermes multi-profile organization.

## Decide the migration boundary

Separate these identifiers before editing:

| Layer | Typical value | Default rename policy |
|---|---|---|
| Public organization name | `Nexus` | Rename |
| Coordinator role label | `Nexus main assistant` | Rename |
| Kanban display name | `Nexus organization work` | Rename |
| Kanban slug | `astra-organization` | Keep unless explicit migration requested |
| Kanban DB path | `~/.hermes/kanban/boards/<slug>/kanban.db` | Keep with slug |
| Workspace/artifact root | `/path/to/astra-organization/` | Keep for compatibility unless explicit migration requested |
| Diagram canonical basename | `nexus-organization-chart` | Rename/create |
| Legacy artifact basename | old public-name basename | Update content or provide a compatibility copy |

The safe default is a **public-name rename with stable internal identifiers**. This preserves task history, links, logs, absolute paths, and automation.

## Files and metadata to update

1. Coordinator `SOUL.md`
   - Organization heading.
   - Coordinator role description.
   - Public reporting chain.
2. Every specialist `SOUL.md`
   - “Member of <organization>” sentence.
   - “Reports to <coordinator role>” sentence.
3. Organization governance
   - README title and hierarchy.
   - Operating-model title and role table.
   - Task template requester/coordinator label.
4. Kanban
   - Run `hermes kanban boards rename <slug> "<display name>"`.
   - Confirm display name through `hermes kanban boards show`.
   - If the board description is separately stored and no supported CLI edits it, update the board metadata carefully and validate its format.
5. Diagrams
   - SVG `<title>` and `<desc>`.
   - Header, coordinator card, shared-hub label, legend/footer.
   - Self-contained HTML `<title>`, inline SVG, and explanatory note.
   - PNG rerender from the updated SVG.
6. Compatibility note
   - State that the public name changed while the slug/path remains an internal identifier.

## Verification

- Check the new organization name and exact coordinator role phrase in all active governance and profile files.
- Search active files for stale public branding. Exclude immutable logs and historical audit reports from forced rewrites.
- Parse SVG as XML and HTML structurally.
- Render the canonical SVG to PNG at messaging resolution (for example 2000×1125).
- Compare the delivered PNG with an independent rerender when deterministic rasterization is available.
- Visually verify title, coordinator role, all specialist cards, shared repository, and producer→reviewer arrow direction.
- Create a quality-profile Kanban card with explicit criteria, deadline/timezone, evidence paths, approval status, and report path; wait for `done`, then read back the report and task metadata.

## Pitfalls

- A display-name change does not rename an immutable Kanban slug.
- Moving the workspace merely to make the path match the new brand can break old cards and absolute artifact links.
- Updating only the diagram title leaves stale identity in accessibility text, HTML metadata, specialist role contracts, or board descriptions.
- Leaving old-name preview files unchanged creates conflicting public artifacts. Update them or replace them with compatibility copies of the canonical content.
- Do not rewrite historical quality reports just to erase the former name; they are audit evidence.
