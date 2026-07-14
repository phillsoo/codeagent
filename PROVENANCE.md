# Provenance and redistribution notes

## Hermes bundled skills

Hermes-provided bundled skills are **not copied into this repository**. `snapshot/skills/BUNDLED_SKILLS.json` stores only the installed skill names and source digests so the environment can be audited and reconstructed from the official Hermes distribution.

## Local custom skills

Only locally maintained custom skills that are not listed in Hermes `.bundled_manifest` are exported in full. Their paths are preserved beneath `snapshot/skills/`.

## License status

This repository currently has no root license. Publication therefore does not grant a general license to copy, modify, or redistribute its contents. A specific open-source license should be added only after the repository owner selects one and confirms rights for all local custom material.
