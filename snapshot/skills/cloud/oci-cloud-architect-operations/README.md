# Installation Candidate

이 디렉터리는 검수 전 설치 후보이며 현재 Hermes profile을 변경하지 않았다.

후보: `${HOME}/astra-organization/artifacts/it/oci-cloud-architect-skill/`

독립 검수 후 active profile의 skill tree(예: `~/.hermes/profiles/<profile>/skills/cloud/oci-cloud-architect-operations/`)에 복사하거나 승인된 skill-management 절차로 설치한다. OCI credential은 절대 복사하지 않는다.

검증:
```bash
python3 scripts/validate_skill.py
```

신규 설치 skill은 loader cache 때문에 새 Hermes session에서 `skills_list`/`skill_view`에 나타날 수 있다. 예상 이름은 `oci-cloud-architect-operations`다.
