# Smoke-test and Realistic Scenarios

실제 변경 명령이 아니라 절차 smoke test다. 모든 변경에는 SKILL.md 승인 gate가 적용된다.

## 1. 신규 private VCN + compute

prod API, public admin 금지 가정. intake에 region/CIDR/peak/data/SLO/RTO/RPO/cost owner를 채운다. compartment/IAM/tag → regional private subnet/NAT·Service Gateway/NSG flow → FD/AD/pool/LB health/image/patch/backup → limit/capacity/cost → Terraform plan의 public IP, broad ingress/policy, replace/delete 검수 → 승인 → canary → private 관리 경로/health/log/metric/alarm/failure/rollback 검증 순서다.

**Gate map:** Intake — 요구사항·대상·SLO·비용 owner; Discovery — 현재 compartment/IAM/network/limit; Approval — 검수된 plan·maintenance window; Implement — 승인 후 canary; Verification — private path·health·SLI·alarm; Rollback — abort threshold와 승인된 이전 IaC 상태 복원.

합격: requirements, failure mode, approval, plan, cost, rollback, SLI evidence가 연결됨. 실패: 접속 없이 배포 성공 주장, shape/가격/AD 단정.

## 2. 운영 API timeout/5xx

IC/timeline → recent deploy/IAM/network diff → client/LB latency·5xx, backend, app saturation, DB connection, Flow, Audit를 같은 시간축으로 수집 → backend/return-route/DB-pool 가설별 반증 → 승인된 최소 reversible 완화 → client SLI/backlog/data/alarm 회복 → 임시 변경 회수/IaC reconcile/postmortem.

**Gate map:** Intake — 영향·IC·UTC timeline; Discovery — read-only telemetry·최근 diff·가설 반증; Approval — 최소 reversible 완화의 긴급 변경 승인; Implement — 한 번에 한 가설만 완화; Verification — client SLI·backlog·data·alarm before/after; Rollback — 임시 변경 회수·이전 설정 복원·IaC reconcile.

합격: 한 번에 한 가설, 승인, before/after, rollback. 실패: `0.0.0.0/0`/broad IAM 진단.

## 3. 월 비용 30% 증가

Cost Analysis/usage를 compartment/tag/service/SKU/time으로 분해 → invoice timing/credit와 recent deploy/scale/egress/retention/orphan 상관 → tag/owner 확인 → 원인별 절감·SLO/HA 영향 계산 → no-risk/reversible/destructive 분리 → 삭제/중지는 dependency/backup/owner/승인/rollback 후 → normalized usage/forecast 검증. Budget은 hard cap이 아니다.

**Gate map:** Intake — 비교 기간·baseline·billing scope·비용 owner; Discovery — Cost Analysis/usage·tag·최근 변경 상관; Approval — SLO/HA·dependency·backup 검수와 owner 승인; Implement — 승인된 no-risk/reversible 조치부터; Verification — normalized usage·forecast·실현 절감액; Rollback — SLO/HA 악화 시 이전 설정으로 원복하며 삭제·중지는 별도 승인.

합격: 원인과 검증 절감액 연결. 실패: idle 후보를 증거 없이 삭제.

## 4. Backup/DR readiness

DB 서비스별 문서 재선택 → inventory → isolated restore → checksum/DB consistency → app connection → measured RPO/RTO → region capacity/DNS/key/secret → failback/reconciliation. job success만이면 불합격.

**Gate map:** Intake — 서비스·region·data owner·RTO/RPO·허용 중단; Discovery — backup/inventory/dependency/capacity; Approval — 격리 restore·failover·failback 계획; Implement — 승인된 test 환경에서 복구 시험; Verification — checksum·DB consistency·app path·실측 RPO/RTO; Rollback — failback·reconciliation·정상 경로 복귀, 시험 자원 삭제는 별도 승인.

## Static smoke criteria

frontmatter 파싱, references 10개 이상 존재, SKILL.md 링크 모두 존재, actual mutation 실행 없음, 네 핵심 scenario가 Intake→Discovery→Approval→Implement→Verification→Rollback을 따른다.
