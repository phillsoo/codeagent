---
name: oci-cloud-architect-operations
description: "Use when designing, reviewing, deploying, operating, troubleshooting, recovering, securing, or optimizing Oracle Cloud Infrastructure (OCI). Enforces evidence-first discovery, least privilege, explicit approval gates, plan/review/apply separation, verification, rollback, and current Oracle documentation checks without claiming undocumented defaults."
version: 1.2.0
author: Nexus IT
license: Internal
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [oci, cloud-architecture, operations, iam, networking, finops, disaster-recovery]
    related_skills: []
---

# OCI Cloud Architect & Operations

## Overview

OCI 설계·구축·운영·장애·보안·비용 판단을 반복 가능한 증거 기반 절차로 만든다. 경력 연차를 주장하지 않고 숙련자의 판단 습관—요구사항 수치화, 실패 경계 분석, 최소 권한, 변경 통제, 복구 시험, 비용 귀속—을 강제한다.

## When to Use

- OCI landing zone, compartment, IAM, VCN, compute, storage, database, observability, HA/DR 또는 비용 설계·검토
- OCI CLI/Terraform/Resource Manager 변경 준비·실행·검증·rollback
- 운영 장애 triage, 완화, 복구, 사후분석
- 예산 초과, idle 자원, service limit/capacity, security posture 검토

사용하지 말 것: OCI와 무관한 질문, 대상 서비스·리전 없이 서비스별 SLA/기본값 단정, 승인 없는 실제 리소스 변경.

## Progressive Disclosure

- 인증: `references/authentication.md`
- 조직 기본 compartment·API-key 준비: `references/default-compartment-and-api-key-readiness.md`
- IAM/compartment/tag: `references/iam-compartments.md`
- 네트워크: `references/networking.md`
- compute/storage/database: `references/workloads-data.md`
- Autonomous AI Database의 Native MCP·SQLcl MCP·OCI Database/Database Tools MCP 선택, 최소권한, Hermes 설정, 검증·rollback: `references/autonomous-database-mcp.md`
- Flex Compute·기존 public subnet·SSH key·Balanced boot 생성과 사후검증: `references/compute-flex-public-ssh-launch.md`
- observability: `references/observability.md`
- HA/DR: `references/ha-dr.md`
- 비용/한도: `references/finops.md`
- OCI 공개 가격표의 시점별 SKU·단가 변경 조사: `references/public-price-list-change-research.md`
- Base Database RAC의 shape 적용성·구/신 SKU 매핑·최소견적 검증: `references/base-database-rac-sku-transition.md`
- OCI 공개가격 견적 시스템의 원장·캐시·계산·가격 무결성·독립 검수: `references/public-pricing-estimator-systems.md`
- IaC: `references/iac-change-control.md`
- 장애: `references/incident-response.md`
- 적용 예: `references/scenarios.md`
- 출처: `references/official-sources.md`

## Non-Negotiable Safety Gates

1. **읽기 우선.** 변경 전에 현재 상태를 read-only CLI/API/Console export로 보존한다.
2. **명시적 승인.** IAM 권한, 방화벽/NSG/security list/route/DRG, 운영 중단, DB/storage, 삭제, public exposure, key, 비용 발생 리소스는 승인 증거와 maintenance window 없이는 실행하지 않는다.
3. **비밀 금지.** private key, auth token, secret, wallet, 전체 config를 산출물/로그/plan에 기록하지 않는다.
4. **최소 권한.** tenancy-wide `manage all-resources`를 기본으로 삼지 않는다. verb/resource/scope/condition을 최소화하고 dynamic group/instance/resource principal을 우선 검토한다.
5. **역할 분리.** 실행자와 검수자를 분리한다. 검수자는 영향·삭제/교체·권한·비용·rollback을 독립 확인한다.
6. **현재성.** 가격, region availability, capacity, limits, SLA, retention은 실행 시점 Oracle 문서/API로 다시 확인한다.
7. **Budget은 hard cap이 아니다.** 자동 중지·삭제는 별도 위험 변경으로 승인한다.

## Required Intake

| 항목 | 필수 내용 |
|---|---|
| 요청자/owner | 역할, 승인 권한 |
| 목표/완료 조건 | 수치 결과와 검증 방법 |
| 기한/변경 창 | UTC, 허용 중단 시간 |
| 대상 | tenancy/region/compartment/서비스/환경 |
| 중요도 | prod, 데이터 등급, 규제 |
| SLO/RTO/RPO | workload tier별 수치와 승인자 |
| 부하/성장 | peak, p95/p99, IOPS/throughput, 성장률 |
| 비용 | 월 한도, owner, 태그, 예상 증분 |
| 입력/산출물 | diagram/IaC/runbook, 증거 위치 |
| 승인 | 승인 ID, 검수자, rollback 권한 |

누락값을 도구로 조회할 수 없으면 가정으로 표시한다. 위험 변경에 필요한 값이면 BLOCKED 처리한다.

## Standard Workflow

### 1. Scope and classify

설계/배포/운영/장애/보안/비용을 분류한다. instance/FD/AD/region/tenancy/operator failure boundary, 데이터 흐름과 trust boundary, dependency를 적는다. public exposure, IAM, 데이터 변경, 삭제/교체, 중단, 비용 여부를 표시한다.

완료: 요구사항표, dependency, 위험 등급, 성공·중단 기준이 있다.

### 2. Read-only discovery

`oci --version`, `oci <group> <command> --help`로 설치 명령을 확인한다. 인증은 authentication 문서에서 고른다. JSON을 보존하고 secret을 제거한다.

```bash
oci iam region-subscription list --output json
oci iam compartment list --compartment-id "$TENANCY_OCID" --compartment-id-in-subtree true --all --output json
oci search resource structured-search --query-text 'query all resources' --output json
oci iam policy list --compartment-id "$COMPARTMENT_OCID" --all --output json
oci network vcn list --compartment-id "$COMPARTMENT_OCID" --all --output json
oci compute instance list --compartment-id "$COMPARTMENT_OCID" --all --output json
oci monitoring alarm list --compartment-id "$COMPARTMENT_OCID" --all --output json
```

완료: timestamp, CLI version, auth mode, region, sanitized command, exit code, request ID(있을 때), raw evidence path가 있다.

### 3. Design and failure-mode review

compartment/IAM/tag guardrail을 먼저 확정한다. CIDR/return path/DNS/NSG/security list/host firewall을 함께 검토한다. compute/storage/database를 SLO, 성능, patch 책임, HA/backup/DR에 연결한다. backup 성공이 아니라 restore/application consistency를 설계한다. user SLI, saturation, audit/flow/access/app/DB log와 alarm delivery를 포함한다. limit, quota, physical capacity를 구분하고 failover surge를 검토한다.

완료: architecture, ADR, failure-mode 표, RTO/RPO, 비용 추정, 검증·rollback 초안이 있다.

### 4. Change package and approval

필수 항목: before evidence; 정확한 대상·제외; Terraform plan 또는 CLI/API 단계; create/update/replace/delete 및 IAM/network/public diff; blast radius/중단; 유효한 backup/restore 증거; pre/post-check·canary·abort threshold; rollback과 소요시간; 초기/월간/egress/backup/log 비용; 실행자/검수자; 승인 ID와 maintenance window.

**BLOCKED:** 필요한 승인, 복구 가능 backup, rollback, 검수자 또는 허용 중단 시간이 없으면 실행하지 않는다.

### 5. Implement with checkpoints

IaC는 fmt/validate/security scan/plan → 독립 검토 → 승인 apply 순서다. manual change는 request ID/work request/명령/exit code를 기록하고 IaC에 reconcile한다. canary부터 진행하며 단계마다 health/SLO/Audit을 확인한다. plan·대상·시간·승인이 달라지면 중지한다.

완료: 승인 범위만 변경되었고 work request terminal state가 확인된다.

### 6. Verify

기능(client path), 보안(effective access/public route/ingress/encryption), 신뢰성(분산·health·restore/failover), 관측(log/metric/alarm delivery), 성능(baseline 대비 p95/p99/throughput), 비용(SKU/forecast/tag/budget), IaC(drift/state/real resource)를 검증한다.

완료: acceptance criterion마다 명령·로그·resource ID·before/after·판정이 연결된다.

### 7. Roll back or close

abort threshold를 넘으면 변경을 멈추고 승인된 rollback을 실행한다. 삭제·복원·DNS/route/IAM rollback도 승인 범위를 확인한다. rollback 후 같은 검증을 반복한다. 정상 종료 시 evidence manifest, known issues, 잔여 risk, 비용 변화, 다음 review date를 남긴다.

## Incident Mode

IC/communication owner 지정 → UTC timeline·영향 고정 → Audit/Logging/Monitoring/LB/Flow/work request read-only 수집 → 가설별 반증 → 최소 reversible mitigation → 긴급 승인 → client SLI·dependency 복구 확인 → 임시 변경 reconcile/rollback → blame-free postmortem 순서다. 상세는 incident reference를 읽는다.

## Evidence Manifest

```text
change_or_incident_id / timestamp_utc:
actor_role / reviewer_role / approval_reference:
target_region / compartment / resource_ids:
auth_mode / cli_version / sanitized actions:
before_state / plan_diff / backup_restore evidence:
work_request_ids / after_state / verification:
rollback_trigger / rollback_result / cost_delta / known_issues:
```

## Common Pitfalls

1. Console만 current truth로 간주 → API/CLI JSON, Audit, work request와 교차 확인.
2. `manage all-resources`/`0.0.0.0/0`으로 해결 → 최소 scope/port/source와 만료 사용.
3. HA=backup=DR로 오해 → 가용성, 논리 손상, region 재해를 각각 시험.
4. backup job 성공만 확인 → 격리 restore와 checksum/DB consistency 검증.
5. Budget=hard stop으로 오해 → alert 뒤 승인된 대응 설계.
6. DB 서비스 간 명령/RPO/patch를 일반화 → 대상 서비스 문서 재선택.
7. apply 뒤 성공 선언 → work request terminal state와 사후 검증 확인.
8. secret을 plan/state/log에 남김 → secret reference와 redaction 사용.
9. `${REDACTED}...`를 일반 compartment로 오인 → OCID type을 먼저 검사하고 root 사용 의도인지 확인.
10. CLI profile에 기본 compartment가 자동 적용된다고 가정 → 명령/IaC에 `$OCI_COMPARTMENT_ID`를 명시하고 실제 target을 검수.
11. profile smoke에서 상속된 `HERMES_PROFILE`/`HERMES_HOME`을 방치 → selector를 제거한 새 프로세스로 profile별 환경 로딩을 검증.
12. API-key 401을 IAM 확대나 확정 진단으로 처리 → 공개키 등록·fingerprint·사용자·profile·clock·전파 순서로 확인하고 성공 전 BLOCKED 유지.
13. Balanced boot 가격을 GB-month만 계산 → capacity와 VPU/GB 성능 SKU를 각각 Decimal로 합산하고 비용 수정 시 재승인.
14. 설치된 CLI에 없는 boot VPU 독립 옵션을 가정 → `launch --help`와 `--generate-param-json-input source-details`를 확인하고 `bootVolumeVpusPerGB`를 source details에 포함.
15. API signing public key를 SSH key로 재사용하거나 TCP connect를 SSH 성공으로 보고 → OpenSSH key 경로·fingerprint와 private-key counterpart를 구분하고 실제 인증 전에는 port reachability만 보고.
16. 기존 public subnet에 NSG를 추가하면 넓은 Security List가 좁아진다고 가정 → effective allow는 합집합임을 반영하고 route/security list/NSG를 함께 검토하며 `0.0.0.0/0:22`는 명시적 예외 승인.
17. parser 실패를 OCI write 실패와 혼동 → resource ID/service response 부재를 확인하고, 승인 범위가 동일한 payload 교정은 독립 재검수 후 재시도하며 범위 변경만 사용자 재승인.
18. ADB 데이터 MCP 요구를 SQLcl 또는 OCI 제어면 MCP로 바로 매핑 → ADB Native managed MCP의 현재 공식 문서와 region/DB 지원을 먼저 확인하고 데이터 경로·SQLcl 경로·OCI 제어면을 분리.
19. MCP YAML이 parse되면 최소 노출 설정도 유효하다고 간주 → `tools.include`, `tools.prompts`, `tools.resources`의 실제 중첩 구조를 semantic assertion으로 검증하고 server-level 오배치를 거부.

## Verification Checklist

- [ ] 담당자, 목표, 완료 조건, 기한, 대상, 입력, 산출물, 승인, 허용 중단 시간을 확인했다.
- [ ] read-only before evidence와 blast radius가 있다.
- [ ] least privilege와 실행자/검수자 분리를 확인했다.
- [ ] backup/restore, 검증, rollback, abort threshold가 있다.
- [ ] 가격·region 기능·limits/capacity를 현재 자료로 재확인했다.
- [ ] Balanced/block volume 견적은 capacity와 VPU/GB 성능 비용을 분리 합산했다.
- [ ] 명령은 설치된 CLI help와 complex parameter의 generated JSON schema로 검증했다.
- [ ] SSH key 유형·fingerprint·private counterpart와 port reachability/인증 성공을 구분했다.
- [ ] before/after, work request, 기능·보안·SLO·비용·drift 증거가 있다.
- [ ] secret/PII가 없다. 미실행 작업을 성공으로 표현하지 않았다.
- [ ] 중요 변경은 독립 검수가 재현할 manifest를 남겼다.
