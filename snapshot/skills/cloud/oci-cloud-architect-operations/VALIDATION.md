# Validation Report — OCI Cloud Architect Skill Rework

- Task: `t_5657da5f`
- Timestamp: 2026-07-09T12:15:45Z
- Scope: local installation-candidate documentation and validator only
- Candidate: `${HOME}/astra-organization/artifacts/it/oci-cloud-architect-skill/`
- Approval boundary: local file edits and validation allowed; OCI authentication, API calls, resource changes, active-profile installation, and deletion were not performed

## Defect Resolution

### D1 — FinOps budget command path

`references/finops.md` now uses:

```bash
oci budgets budget budget list --compartment-id "$TENANCY_OCID" --all --output json
```

Installed OCI CLI 3.83.0 result: `oci budgets budget budget list --help` exited 0.

### D2 — Validator and scenario completeness

`scripts/validate_skill.py` now:

- extracts OCI lines only from fenced `bash`, `sh`, or `shell` examples;
- parses with `shlex` and retains only literal command-path tokens before the first option;
- rejects dynamic/placeholder command-path tokens and non-read-only leaf commands;
- executes only `oci <literal command path> --help`, with no option values, credentials, or API calls;
- validates each of four numbered scenarios independently for an explicit Gate map containing intake, discovery, approval, implement, verify, and rollback;
- preserves the original frontmatter, body, reference-link, reference-count, size, and safety-token checks.

`references/scenarios.md` now consistently says “네 핵심 scenario” and includes all six gates in each of the four scenarios.

## Executed Verification

Full command output: `validation-20260709.log`.

- `oci --version`: `3.83.0`
- corrected budget path help: PASS, exit 0
- `python3 scripts/validate_skill.py`: PASS
  - 11 linked references / 11 reference files
  - 4 scenarios checked independently
  - 24 fenced OCI examples reduced to 19 unique command paths
  - 19/19 local `--help` checks passed
  - API calls: 0
- `python3 -m py_compile scripts/validate_skill.py`: PASS, exit 0
- negative regression: `python3 scripts/validate_skill.py --inject-oci-path 'budgets budget list'`: expected FAIL, exit 1; failure identifies `oci budgets budget list --help` exit 2
- isolated loader smoke using the pre-existing quality test home: PASS; `oci-cloud-architect-operations` listed as local/enabled by both `--source local` and `--enabled-only`
- mutation protection: validator accepts fenced leaves only from `get`, `list`, and `structured-search`; no mutation command was executed

## Before / After

Before:

- FinOps fenced example used an OCI CLI path that returned “No such command”.
- Validator checked structure and safety tokens but not fenced CLI command-path help.
- Scenario static wording and enforcement did not consistently cover all four scenarios and their per-scenario gates.

After:

- Corrected budget path returns help exit 0.
- Every unique fenced read-only OCI command path is checked with local help only.
- The historical bad path causes the validator to fail in the negative regression.
- Four scenarios each pass the explicit six-gate check.
- Candidate remains uninstalled in the active IT profile; no OCI state changed.

## SHA-256

- `SKILL.md`: `586b3743b3b91c8cd0de9c318b87b7fa69d31ade0946237437e2ea584d52bb2b`
- `references/finops.md`: `517b8b9086ba93c1b819df27e188d6ee7b418f35aa66b1411d20f70037751e2b`
- `references/scenarios.md`: `2e6289f3fb6f1e2cf95f1416d1f71370a73d75345b602ee958085efddf716f03`
- `scripts/validate_skill.py`: `15f002f064d271c79600e0cd17e128dc844a547d6e9cc9156db4616e46e07848`
- `validation-20260709.log`: `20180649d769994c71a5a8397f05930c3f8eeac5d001e5de78a4247305a42db9`
- `oci-cloud-operations-playbook.md` (unchanged): `bccc0db5cf21f644071aa47a53779b3b21d7f340382c6495c26c9a8a8a38d6b2`

## Rollback and Known Issues

Rollback is local-file restoration of the three changed source files from their reviewed predecessor copies; OCI and active-profile rollback are unnecessary because neither was changed. The validator requires an installed `oci` executable for help smoke. Service/region-specific prices, limits, capacity, SLA, retention, and database semantics still require execution-time revalidation after a target environment is supplied.

Independent quality re-review is required before installation or operational use.
