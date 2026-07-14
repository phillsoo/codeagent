# Default compartment and API-key readiness

Use this when making OCI resource creation defaults durable across an agent organization.

## Validate identifier semantics first

- A child compartment OCID starts with `${REDACTED}.`.
- A tenancy/root compartment identifier starts with `${REDACTED}.`.
- If a user labels a tenancy OCID as a compartment, stop and ask whether they intend the tenancy root or will provide a child compartment. Never silently treat the two as equivalent: root placement weakens IAM, cost, lifecycle, and blast-radius separation.

## Persisting an organizational default

OCI CLI config has authentication/profile fields but no universal setting that injects `--compartment-id` into every service command. A durable organization default therefore needs all of:

1. A mode-0600 source file containing the chosen compartment OCID and region.
2. `OCI_COMPARTMENT_ID` and `OCI_REGION` upserted without printing existing secrets into the coordinator, IT, and quality profile environments.
3. Role policy stating that commands and IaC must explicitly reference the default, for example `--compartment-id "$OCI_COMPARTMENT_ID"` or `compartment_id = var.compartment_id`.
4. An override rule: another compartment requires explicit user direction and must be recorded in the change package.
5. Independent quality verification that the actual target equals either the default or the documented override.

Environment changes normally require a new Hermes session or `/reload`; do not claim a running session inherited them without testing.

## Profile-isolated verification

When testing profile environment loading, inherited `HERMES_PROFILE` or `HERMES_HOME` can defeat `hermes -p <profile>` and produce a false result. Launch the smoke test with those inherited selectors removed, then verify only:

- variable present/not present;
- OCID type (`compartment` vs invalid);
- expected region;
- exactly one definition per profile.

Never print the full OCID or unrelated `.env` contents in reports.

## API signing-key readiness

For a user API signing key:

1. Build config from `user`, locally derived `fingerprint`, `tenancy`, `region`, and `key_file`; enforce config/key mode 0600.
2. Validate required field names and key parseability without printing values or private-key material.
3. Run one harmless read-only call such as `oci iam region-subscription list`.
4. On HTTP 401 `NotAuthenticated`, do not widen IAM. Check, in order: public key registered on the same user, registered fingerprint matches local public key, User OCID, config profile/region, clock skew, and propagation delay.
5. Treat local configuration as complete but operational authentication as BLOCKED until the read-only call succeeds.

A local 401 cannot prove the public key is unregistered because the API-key list cannot be queried without working authentication. Report it as the leading diagnosis, not a confirmed fact.
