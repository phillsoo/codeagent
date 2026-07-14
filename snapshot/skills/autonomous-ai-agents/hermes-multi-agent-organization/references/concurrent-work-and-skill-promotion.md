# Concurrent Work and Skill Promotion

Use this checklist when a coordinator, specialist workers, and quality reviewers may touch the same live state or when a reviewed artifact is promoted into active Hermes profiles.

## Single-writer rule

Assign one active writer per artifact tree or mutable state domain. Before dispatching a second task, compare its outputs with every running card.

Examples of one state domain:

- The same report and validation log.
- One skill candidate directory and checksum manifest.
- `~/.oci`, cloud credentials, package state, or another shared runtime configuration.
- Active profile skill directories.

If outputs overlap, serialize the tasks with a dependency. Do not create a duplicate repair card merely because another worker or reviewer also proposed one.

## Coordinator changes during worker execution

A coordinator-side change can invalidate a worker's evidence even when both actions are individually correct. If the coordinator must change shared state while a worker is running:

1. Record actor, timestamp, exact path/state, authorization basis, and intended effect.
2. Comment on or amend the running card immediately.
3. Require the worker to refresh its before/after inventory before completion.
4. Treat any report based on the old snapshot as stale until reconciled.

Independent quality should distinguish a product defect from a concurrent-observation defect, but evidence must still be corrected before PASS.

## Repair workflow

1. Preserve the failed quality report; do not overwrite history.
2. Create exactly one repair card assigned to the producer role.
3. Include every defect ID, affected path, expected evidence, deadline with timezone, and prohibited actions.
4. Link the failed review and original producer card as parents.
5. Let the producer create or receive one independent re-review card.
6. Do not install or publish the repaired candidate until that re-review reaches PASS.

## Promoting a reviewed skill

1. Validate the candidate in an isolated `HERMES_HOME` first.
2. Obtain independent quality PASS on the candidate.
3. Confirm the user's request authorizes installation into the named profiles.
4. Copy the reviewed bytes into each active profile, excluding generated caches such as `__pycache__` and `.pyc`.
5. Compare relative-path-to-SHA-256 maps between candidate and every installation; allow only documented cache exclusions.
6. Verify each profile lists the skill as local and enabled. Avoid exact-name `grep` against narrow rich tables because names may be visually ellipsized; use a wide terminal or structured/full output.
7. Start new profile sessions with the skill explicitly loaded and run behavior-focused smoke tests, including a denial/blocked case for safety gates.
8. Create a separate quality card to verify installed-byte identity, loader discovery, and observed smoke-session behavior.

## Card invariant

Every child, repair, and re-review card needs its own assignee, completion criteria, exact deadline with timezone, inputs, output path, approval boundary, and review role. A parent deadline does not satisfy the child-card requirement.