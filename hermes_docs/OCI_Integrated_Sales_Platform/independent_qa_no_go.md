# 통합 영업 플랫폼 독립 QA — 누락 위험 및 승인 게이트

- 검수 관점: 독립 QA / 배포 전 문서·증거 검토
- 대상: OCI 서울 리전 `ADBHERMES`, 기존 인터넷 노출 가능 웹 서버, Price List·Consumption·CRM·Weekly Report·Demo 기능
- 판정: **NO-GO (배포·실데이터·외부 공개 금지 유지)**
- 비밀정보: 본 보고서에 IP, OCID, Wallet, 키, 암호, 토큰, 실명 고객 데이터 미기록
- 검수 한계: 현재 확인 가능한 산출물은 Compute/공인 IP 조회 JSON과 기존 ADB Wallet·CRUD·계정 적재 보고서뿐이다. 애플리케이션 설계, IAM policy, NSG/security list, host firewall, 소스코드, 데이터 사전, 테스트 결과, 운영·복구 문서는 확인되지 않았다.

## 1. 심각도 기준

- **Critical**: 인터넷 침해, 비밀/개인정보 노출, 과도 권한, 데이터 손실 또는 복구 불능 가능성. 해당 게이트 미충족 시 배포·실데이터·외부 공개 금지.
- **Major**: 핵심 업무 수치 오류, 감사 불능, 운영 실패, 비용 급증 또는 UAT 품질 실패 가능성. 운영 승인 전 해소 필요.
- **Minor**: 즉시 보안/데이터 손실 위험은 낮지만 운영성·가독성·증거 품질을 저하. 운영 전 계획과 담당·기한 필요.

## 2. 독립 QA 결과

### Critical

| ID | 영역 | 누락/위험 | 현재 근거 | 필수 조치 및 승인 게이트 |
|---|---|---|---|---|
| C-01 | Public IP 서버 보안 | 웹 서버의 실제 공인 노출 경로, VNIC, NSG/security list, route, LB/WAF, TLS, host firewall, 열린 포트가 입증되지 않았다. 인터넷 직접 SSH/RDP·관리 포트 노출 가능성을 배제할 수 없다. | 공인 IP 증거에는 NAT Gateway 주소만 있으며 웹 서버 직접 공인 IP 연결은 확인되지 않음. Compute 증거상 Vulnerability Scanning·OS Management Hub·Bastion 플러그인은 비활성이다. | **Security GO 전 금지:** VNIC→subnet→route→NSG/security list→host firewall의 effective path를 read-only로 고정. 80은 443 redirect만, 443은 승인 LB/WAF 경유, 관리 포트는 인터넷 차단·Bastion/VPN/허용 CIDR·JIT 사용. TLS 인증서/자동갱신, 패치 기준, EDR/취약점 검사, access/WAF/flow 로그와 경보를 검증. Security + Network + 독립 QA 승인 필요. |
| C-02 | 서버 하드닝/공급망 | OS 이미지·패치 수준, CIS 기준, 서비스 계정, sudo, SSH 키 수명·회수, root 로그인, 애플리케이션 포트, SBOM/취약점·이미지 서명이 없다. Secure Boot/TPM도 비활성으로 관찰된다. | Compute 조회 증거에 레거시 IMDS 차단은 확인되나 Secure Boot·TPM 비활성, 패치/취약점 운영 증거 없음. | Golden image 또는 하드닝 baseline, 최소 패키지, root/암호 SSH 금지, 사용자별 단기 키/인증서, 자동 보안 패치·재부팅 창, SAST/SCA/container scan, critical/high 0 또는 승인 예외를 증명. 예외는 만료일·보완통제·owner 포함. |
| C-03 | `HERMESUSER` 최소 권한 | 기존 검증에서 `HERMESUSER`가 테이블 생성/삭제를 수행했고 `ACCOUNTS` 소유자다. 웹 애플리케이션 런타임 계정으로 재사용하면 DDL·스키마 소유권과 업무 DML이 결합된다. SQL injection/credential 탈취 시 blast radius가 과도하다. | 임시 테이블 CREATE/DROP와 `HERMESUSER.ACCOUNTS` 생성·적재 성공 보고가 존재. 전체 effective privilege/role/grant 목록은 없음. | **DB Security GO 전 금지:** schema owner/migration 계정과 runtime 계정 분리. runtime은 승인된 객체별 `SELECT/INSERT/UPDATE/DELETE`만, DDL·ANY privilege·ADMIN role 금지. read-only report 계정과 batch 계정도 분리. `SESSION_PRIVS`, roles, system/object grants, synonyms, future-object grant 경계를 증거화하고 positive/negative 접근 테스트. REVOKE rollback을 사전 작성. DBA + App Owner + Security + 독립 QA 승인. |
| C-04 | Wallet/Secret 관리 | Wallet·DB 비밀번호가 현재 호스트 로컬 파일에 존재한다. 운영 웹 서버 배포 시 복사·백업·로그·프로세스 환경·CI/CD를 통한 유출, 공용 Wallet 재사용 및 회전 불능 위험이 있다. | 기존 보고서는 디렉터리 0700/파일 0600과 로그 비노출만 확인. Vault, 수명, 회전, 접근 감사, 폐기 증거 없음. | OCI Vault/Secrets 또는 승인 secret manager의 **참조만** 배포. 코드·PPT·Git·이미지·user-data·환경 dump 금지. 서비스별 Wallet/secret 분리, 다운로드 주체 최소화, rotation/revoke runbook, 만료·접근 경보, 백업 제외/암호화, incident 즉시 회전 테스트. Secret Owner + Security 승인. |
| C-05 | OCI IAM | 실행 주체, 사용자 그룹/dynamic group, instance/resource principal, compartment 범위, policy 조건, MFA·break-glass, 분리된 prod/demo 권한이 없다. Compute Run Command 활성 상태에서 과도한 IAM이면 원격 코드 실행 경로가 된다. | IAM policy/effective access diff 증거 없음. 인스턴스에서 Run Command 활성만 확인. | tenancy-wide `manage all-resources` 금지. 사용자 API key보다 instance/resource principal 우선; verb/resource/compartment/condition 최소화. Run Command 권한은 소수 운영그룹·MFA·ticket/JIT로 제한. policy simulator/허용·거부 테스트, break-glass 60분 이하·사후감사, before/after diff와 rollback을 Security/IAM Owner/독립 QA가 승인. |
| C-06 | CRM 개인정보 | 고객 담당자 이름·이메일·전화·활동 메모·소유자 정보가 포함될 수 있으나 처리 근거, 데이터 분류, 최소수집, 마스킹, 행/필드 RBAC, 동의/거부, 보존·삭제, 데이터 주체 요청, 국외이전/리전 적합성, export/DLP가 미확정이다. 기존 ACCOUNTS에는 담당자 이름 계열 필드가 존재한다. | 계정 적재 보고에는 `OWNER_NAME`; CRM 개인정보 영향평가·법무 승인·접근 테스트 없음. | **실데이터 업로드 금지:** DPIA/Privacy review, 목적·근거·분류·보존기간·파기, 데이터 residency, do-not-contact, Contact PII 필드 마스킹·default deny, export 제한/워터마크/DLP, 조회·내보내기 감사, 합성 데이터 접근 테스트를 완료. Privacy/Legal + Data Owner + Security 승인. |
| C-07 | Demo 격리 | Demo가 운영 ADB/Wallet/CRM/Consumption/Price List와 계정·네트워크·secret을 공유하면 실데이터 노출, 테스트 메일/보고서 발송, 데이터 변조·비용 발생 위험이 있다. | prod/demo compartment, DB schema/instance, IAM, DNS, secret, 수신자 격리 증거 없음. | Demo 전용 compartment/VCN 또는 명시적 non-prod 경계, 별도 DB/schema·runtime principal·Wallet·DNS·도메인·로그·예산 태그. 합성 데이터만 사용하고 외부 발송은 sink/allowlist로 차단. prod endpoint·secret 접근 negative test 100% 통과. Demo Owner + Security + Data Owner 승인. |
| C-08 | 백업/복구 | ADB 자동 백업 여부만으로는 애플리케이션·설정·Wallet/secret reference·서버·보고서·감사로그 복구를 보장하지 못한다. RTO/RPO, 보존, 불변/격리, 복원 시험, 논리손상 대응이 없다. | restore drill, 복구 시간, checksum/DB consistency/app smoke 증거 없음. | BIA 기반 RTO/RPO 승인, ADB PITR/backup 정책과 IaC·app config·report evidence의 별도 백업, immutable/cross-fault-boundary 검토. 격리 restore에서 DB consistency·행 수/checksum·앱 smoke·권한·secret 재연결을 시험하고 측정 RTO/RPO 기록. Data Owner + Operations + Security + 독립 QA 승인. |
| C-09 | 테스트·UAT·롤백 | end-to-end 기능, 권한 거부, 보안, 성능, 장애, 데이터 정합, 동시성, 배치 재실행, UAT sign-off, canary·abort threshold·rollback이 없다. 기존 CRUD 1행 성공은 플랫폼 승인 근거가 아니다. | ADB 연결/임시 CRUD와 계정 252행 적재 검증만 존재. 애플리케이션/E2E/UAT 증거 없음. | 합성 데이터 기반 unit/integration/E2E/security/performance/restore 테스트, 역할별 UAT, defect 기준(Critical 0, Major 0 또는 승인 예외), 배포 canary, 관측 지표, abort threshold, DB migration backward compatibility, 앱/DB/config/IAM/network rollback과 소요시간을 rehearsal. Product Owner + UAT Lead + Ops + Security + 독립 QA 승인. |

### Major

| ID | 영역 | 누락/위험 | 필수 조치 및 승인 게이트 |
|---|---|---|---|
| M-01 | Price List 최신성 | 가격 출처·effective date·region·currency·SKU/part number·단위·license model·discount/tax·종료 SKU·캐시 TTL이 없다. 오래된 가격이 견적처럼 제시될 수 있다. | Oracle 공식 Price List/Cost Estimator/API를 source of truth로 정하고 `source_url/version_or_retrieved_at/effective_from/effective_to/region/currency/unit/SKU` 저장. 매일 또는 승인 주기 sync, checksum·diff·품질검사, stale 배너와 고객 견적 아님 문구, 실패 시 last-known-good + 만료 경고. 가격 변경 승인자는 Pricing/Finance, 운영 전 독립 샘플 대조 필요. |
| M-02 | Consumption 지연·통화·단위 | OCI Usage/Consumption은 반영 지연과 조정이 있고, 당일/최근 데이터는 잠정치다. 다중 통화, null 금액, 크레딧·Free Tier·세금, OCPU/ECPU·GB-month·GB-hour·request 단위를 섞으면 합계가 틀린다. | 조회 UTC 시각·usage 시작/종료·ingestion watermark·잠정/확정 상태를 표시. home region API 사용 여부 검증. 원통화별 합계 유지 후 승인 FX source/rate/date로 별도 환산. null/빈 currency는 0 처리 금지. SKU별 quantity·unit·computed amount·credits·subscription 포함 여부를 보존하고 invoice와 월별 reconciliation. Finance/FinOps 승인. |
| M-03 | Weekly Report 감사 | 보고서 생성 규칙, 기준 시각, 데이터 snapshot, 필터, 환율, 작성/승인/배포자, 수정 이력, 수신자, 보존이 없다. 재생성 시 수치가 바뀌거나 CRM PII가 과다 노출될 수 있다. | `report_run_id`, UTC/KST 기준기간, source watermark/checksum, query/code version, price snapshot, FX snapshot, row counts·exclusions, actor/service principal, approval, recipient allowlist, delivery result를 append-only 저장. 생성본은 immutable 보존하고 정정본은 supersede 링크. 다운로드/외부 발송은 별도 승인과 PII redaction. Audit/Finance/Sales Ops sign-off. |
| M-04 | 비용/TCO | Compute·ADB·backup·egress·public IP/LB/WAF·Vault·Logging/Monitoring·Data Safe·DR·라이선스·운영인력 비용과 태그/budget/forecast가 없다. Budget을 hard cap으로 오해할 위험이 있다. | 월별 low/base/high 시나리오, 일회성/월간/egress/로그/backup/DR 비용, 30/90일 forecast, Owner/CostCenter/Environment/DataClassification/Expiry defined tags, budget alert와 대응 owner를 제시. Budget은 soft alert로 명시. 자동 stop/delete는 별도 위험 승인. Finance/FinOps + Product Owner 승인. |
| M-05 | 관측·감사 보존 | 앱/DB/OCI Audit/WAF/flow/access 로그의 상관관계 ID, PII/secret redaction, 보존, 무결성, 경보 전달 테스트가 없다. | request/report/import/change ID로 추적, secret·PII redaction, 시간 동기화, 로그 저장소 최소권한·불변성, 고위험 이벤트(권한·secret·export·대량조회·가격 sync 실패·Consumption stale) 경보와 실제 전달 테스트. Security/Ops 승인. |
| M-06 | 데이터 품질·정합성 | Price/Consumption/CRM 간 account/tenancy/SKU/timezone 키와 중복·late arriving·재처리·idempotency·삭제/정정 규칙이 없다. | 데이터 계약, source-of-truth, immutable raw landing, idempotency key, watermarks, late-arrival backfill, reconciliation totals, quarantine/DLQ, 재처리와 rollback을 정의하고 합성 오류 케이스로 검증. Data Owner 승인. |

### Minor

| ID | 영역 | 누락/위험 | 필수 조치 |
|---|---|---|---|
| m-01 | 증거 최소화 | 원본 조회 JSON에는 운영 식별자와 SSH 공개키가 포함되어 공유 범위를 넓힌다. 비밀은 아니지만 공격 표면 정보다. | PPT/보고서에는 식별자 마스킹, raw evidence는 제한 저장소·RBAC·보존기간 적용. sanitized manifest만 공유. |
| m-02 | 시간대·표시 | Weekly/Consumption/감사에서 UTC와 KST 경계·DST 없는 KST 기준이 명확하지 않으면 주간 집계가 어긋난다. | 저장 UTC, 표시 KST, 보고 기간을 `[start,end)`로 명시하고 주차 정의·휴일 기준을 문서화. |
| m-03 | PPT 주장 수준 | 제안·가정·검증 완료·승인 완료가 시각적으로 분리되지 않으면 배포가 승인된 것으로 오해된다. | 모든 슬라이드에 상태 라벨(제안/미검증/검증완료), 기준일, owner, evidence ID를 표시하고 마지막에 명시적 Go/No-Go를 둔다. |

## 3. 승인 게이트

| Gate | 승인 전 금지 | 통과 조건(증거) | 필수 승인자 | 현재 |
|---|---|---|---|---|
| G0 범위·데이터 분류 | 설계 확정 | prod/demo 범위, owner, 데이터 분류, RTO/RPO, 비용 상한, 성공/중단 기준 | Product, Data Owner, Security, Finance | **BLOCKED** |
| G1 보안 설계 | public DNS/ingress, secret 배포 | trust boundary, network effective path, IAM/DB least privilege, secret lifecycle, logging, threat model | Security, Network, DBA, IAM Owner, 독립 QA | **BLOCKED** |
| G2 Privacy | 실 CRM 데이터 적재·내보내기 | DPIA, 처리 근거, 최소수집, residency, 보존/파기, DSAR, RBAC/export test | Privacy/Legal, Data Owner, Security | **BLOCKED** |
| G3 가격·소비 데이터 | 고객/경영 수치 공개 | 최신 Price List evidence, unit/currency mapping, watermark/stale 처리, invoice reconciliation | Pricing/Finance, FinOps, Data Owner | **BLOCKED** |
| G4 Build/Test | 운영 배포 | CI 품질, high/critical 0, E2E·권한 negative·성능·장애·복원 시험, traceable defects | Engineering, QA, Security, Ops | **BLOCKED** |
| G5 UAT | 사용자 확대 | 역할별 핵심 시나리오, 데이터 정합, report audit, Critical/Major 0 또는 문서화된 예외 | UAT Lead, Product, Sales Ops, 독립 QA | **BLOCKED** |
| G6 Change Approval | apply/배포 | before evidence, exact diff, blast radius, cost delta, canary, abort threshold, rollback rehearsal, maintenance window, approval ID | Change Owner, Ops, Security, DBA, Finance(비용 시) | **BLOCKED** |
| G7 Go-Live | public 공개·실데이터·보고서 발송 | G0~G6 모두 PASS, 모니터링/경보 전달, on-call/runbook, restore evidence, known risk 수용 | Business Owner + Security + Ops + Privacy + 독립 QA | **NO-GO** |
| G8 Demo | Demo 공개 | prod negative access, 합성 데이터, 별도 principal/secret/DNS/예산, 발송 sink, 자동 expiry | Demo Owner, Security, Data Owner | **BLOCKED** |

## 4. PPT 필수 체크리스트

다음 항목은 PPT의 마지막 1~2장에 **체크박스 + Owner + Due date + Evidence ID + PASS/BLOCKED** 열로 넣어야 한다.

### A. 범위·상태
- [ ] 본 문서는 제안이며 현재 배포/실데이터/외부 공개 승인이 아님을 표지에 명시
- [ ] 대상 region·compartment·환경(prod/demo)과 시스템 owner 표시
- [ ] trust boundary와 데이터 흐름(웹→API→ADBHERMES→Price/Consumption→Weekly Report) 표시
- [ ] 가정·미검증·검증완료를 구분하고 기준 UTC/KST 시각 표시

### B. 인터넷·서버 보안
- [ ] 웹 서버의 실제 public exposure와 VNIC/NSG/security list/route/host firewall evidence
- [ ] 443 최소 노출, 관리 포트 인터넷 차단, Bastion/VPN/JIT 경로
- [ ] TLS·WAF/rate limit·DDoS·access/flow/WAF 로그와 경보
- [ ] OS patch, 취약점 스캔, CIS hardening, SSH/root/sudo, EDR/SBOM 상태
- [ ] high/critical 취약점 0 또는 만료 포함 승인 예외

### C. IAM·DB·Secret
- [ ] OCI principal→group/dynamic group→policy→resource의 최소권한 그림
- [ ] tenancy-wide manage 금지, compartment/verb/resource/condition 명시
- [ ] schema owner/migration/runtime/read-only/report 계정 분리
- [ ] `HERMESUSER` DDL/ANY privilege 제거 및 객체별 DML 허용·거부 테스트
- [ ] Wallet/DB password/API secret의 Vault 참조, rotation/revoke, 로그·PPT·Git 비노출
- [ ] break-glass/JIT/MFA/만료/사후감사와 rollback

### D. 데이터 정확성
- [ ] Price List 공식 출처, retrieved/effective date, region, SKU, currency, unit, TTL
- [ ] stale/동기화 실패 시 last-known-good·경고·고객 견적 아님 표시
- [ ] Consumption watermark/반영 지연/잠정치, usage 기간 `[start,end)`, 조회 시각
- [ ] null 금액 0 처리 금지, 원통화 보존, FX source/rate/date, 세금·credit 구분
- [ ] OCPU/ECPU, GB-hour/GB-month, request 등 단위 매핑과 invoice reconciliation

### E. CRM 개인정보·감사
- [ ] 개인정보 항목, 목적/근거, 분류, 최소수집, residency, 보존/파기
- [ ] 행·필드 RBAC, default deny, masking, export/DLP, do-not-contact
- [ ] 조회·내보내기·권한·병합·삭제·보고서 발송 감사 이벤트
- [ ] 실데이터 이전 합성 데이터 negative-access 테스트 100% 통과
- [ ] Weekly Report run ID, snapshot/watermark, query·price·FX version, 승인자·수신자·보존

### F. Demo·복구·운영
- [ ] Demo 전용 compartment/network/DB 또는 명시적 격리 경계와 별도 secret/principal
- [ ] 합성 데이터만 사용, 외부 발송 sink/allowlist, prod endpoint 접근 거부 테스트
- [ ] RTO/RPO, backup/PITR/보존/불변성 및 격리 restore 실측 결과
- [ ] DB consistency·checksum·앱 smoke·권한·secret 재연결 복구 증거
- [ ] 모니터링, 로그 redaction, alarm delivery, on-call·incident runbook

### G. 테스트·UAT·배포·롤백
- [ ] unit/integration/E2E/security/performance/failure/restore 테스트 결과
- [ ] UAT 역할·시나리오·합격률·잔여 결함·서명
- [ ] Critical 0, Major 0 또는 owner/만료/보완통제 포함 예외 승인
- [ ] exact change diff, blast radius, maintenance window, canary와 abort threshold
- [ ] 앱·DB migration·config·IAM·network rollback rehearsal와 예상 소요시간
- [ ] 배포 후 기능/보안/SLO/비용/drift 검증 및 rollback 결정권자

### H. 비용·의사결정
- [ ] Compute, ADB, LB/WAF, public IP, Vault, backup, egress, Logging, Data Safe, DR 포함 TCO
- [ ] low/base/high, 30/90일 forecast, 비용 owner와 defined tags
- [ ] Budget은 hard cap이 아니라 alert임을 명시
- [ ] 자동 stop/delete가 별도 위험 변경·승인 대상임을 명시
- [ ] 마지막 슬라이드에 G0~G8 상태와 **현재 NO-GO**를 명시

## 5. 최소 승인 패키지 산출물

1. Sanitized before-state manifest와 네트워크 effective-path 다이어그램
2. OCI IAM/DB privilege effective-access matrix 및 positive/negative 테스트
3. Secret inventory(값 제외), Vault reference, rotation/revoke 증거
4. Price List 데이터 계약·동기화/품질 결과와 Consumption currency/unit reconciliation
5. CRM DPIA·RBAC/export 테스트와 Weekly Report audit schema/샘플 run manifest
6. Demo 격리 증거와 prod 접근 거부 결과
7. RTO/RPO 승인 및 격리 restore 실행 보고
8. 테스트 추적표, UAT 서명, defect/예외 register
9. change diff, canary/abort, rollback rehearsal, cost delta, 승인 ID

## 6. 독립 결론

현재는 **Critical 9 / Major 6 / Minor 3**의 배포 전 미충족 항목이 있다. 확인된 ADB CRUD와 계정 적재는 연결성·기초 데이터 적재 증거일 뿐, 인터넷 공개 웹 플랫폼의 보안·최소권한·Privacy·정확성·감사·복구·UAT·운영 승인 근거가 아니다. 따라서 실제 배포, public DNS/ingress 활성화, Wallet/secret 배포, 실 CRM 데이터 적재, Weekly Report 외부 발송, Demo 공개는 G0~G8의 해당 gate가 PASS 될 때까지 금지한다.
