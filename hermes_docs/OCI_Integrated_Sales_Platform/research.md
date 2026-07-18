# OCI 가격·Consumption·AI 연동 조사 및 설계 기준

## 1. OCI Price List / Pricing API

### 검증된 공개 API
- Endpoint: `https://apexapps.oracle.com/pls/apex/cetools/api/v1/products/`
- 2026-07-18 HTTP 상태: 200
- 지원 확인 파라미터 예: `currencyCode`, `partNumber`
- 샘플 응답 필드: `lastUpdated`, `items[].partNumber`, `displayName`, `metricName`, `serviceCategory`, `currencyCodeLocalizations[].currencyCode`, `prices[].model`, `prices[].value`

### 구현 원칙
1. 가격을 코드에 고정하지 않는다.
2. 원본 응답과 정규화 테이블을 분리한다.
3. `source_last_updated`, `fetched_at`, `currency_code`, `price_model`, `unit/metric_name`, `part_number`를 필수 저장한다.
4. 견적 생성 시 사용한 가격은 Quote Snapshot으로 고정해 이후 가격 변경과 분리한다.
5. 최신 동기화 실패 시 마지막 성공 버전과 경과시간을 표시하고, 허용 기준을 넘으면 견적 확정을 차단한다.
6. 금액 계산은 binary float가 아닌 Decimal/Oracle NUMBER를 사용한다.

## 2. OCI Consumption

### 공식 경로
- Cost Analysis: https://docs.oracle.com/en-us/iaas/Content/Billing/Concepts/costanalysisoverview.htm
- Cost and Usage Reports: https://docs.oracle.com/en-us/iaas/Content/Billing/Concepts/costusagereportsoverview.htm
- OCI CLI Usage API: https://docs.oracle.com/en-us/iaas/tools/oci-cli/latest/oci_cli_docs/cmdref/usage-api/usage-summary/request-summarized-usages.html

### 실제 CLI 검증
- 명령군: `oci usage-api usage-summary request-summarized-usages`
- 필수 입력: tenant ID, usage start/end time
- 시스템 수집 기본안: Usage API 일 단위 증분 수집
- 대량 원본·재처리 대안: Cost and Usage Reports(Object Storage 기반 보고서)

### 구현 원칙
1. `source_time_usage_started`, `source_time_usage_ended`, `ingested_at`을 분리한다.
2. 서비스·SKU·region·compartment·tag·currency·unit을 차원으로 보존한다.
3. 원천 usage key와 기간을 이용해 upsert/idempotency를 보장한다.
4. Cost와 Usage를 같은 수치로 취급하지 않는다. 통화·단위 없는 집계는 금지한다.
5. 원천 데이터 지연시간을 화면에 표시한다.
6. 예산·비용 이상은 알림만 생성하며 자동 리소스 삭제나 중지는 수행하지 않는다.

## 3. Autonomous AI Database / Select AI

### 현재 확인 상태
- DB: `ADBHERMES`
- Region: `ap-seoul-1`
- Workload: `LH`
- Compute model: ECPU, 1 ECPU
- Storage: 1TB
- Auto Scaling: enabled
- Backup retention: 60 days
- mTLS: required
- Wallet/driver/TCPS 1522 준비 완료
- DB login/grant: HERMESUSER credential과 실제 schema scope 미확정으로 차단

### Demo 설계 원칙
- Select AI와 Select AI Agent Demo는 운영 CRM 데이터에 직접 접근하지 않는다.
- Demo 전용 schema/view, read-only credential, 샘플 데이터 또는 마스킹 데이터 사용.
- AI profile/provider credential은 Vault 또는 보안 파일 참조만 사용.
- prompt, generated SQL, execution result, latency, token/cost metadata를 감사 가능하게 저장.
- generated SQL은 allowlist/read-only guard를 통과한 뒤 실행.

## 4. 보안·운영 제약

- 공개 GitHub에는 고객 원본 Account, Wallet, DB 비밀번호, OCI private key를 게시하지 않는다.
- Price/Usage 수집에는 Instance Principal 또는 Dynamic Group + 최소 IAM Policy를 권장한다.
- 운영 서버는 localhost app bind + Nginx TLS reverse proxy를 사용한다.
- 현재 Security List에서 22/8765/3389/1521이 0.0.0.0/0에 공개되어 있어 배포 전 축소 승인 필요.
- 443 ingress, DNS, TLS certificate, SSH key, DB credential, migration backup, rollback owner가 승인 게이트다.

## 5. 권장 동기화 일정

- Price List: 매일 1회 + 견적 확정 전 freshness 검증
- Usage API: 매일 1~4회, 이전 3일 재수집으로 후행 보정
- Cost and Usage Reports: 매일 원본 보존/재처리용
- CRM Account import: 사용자 업로드 시 검증 후 staging → approve → merge
- Weekly Report snapshot: 매주 지정 시각, 승인 후 immutable revision
- Demo catalog health check: 매일 링크·상태 점검, 실제 Demo 실행은 수동 승인

## 6. 조사 시점

- 기준일: 2026-07-18
- 샘플 Pricing API의 `lastUpdated`: 2026-07-16T13:52:41.483Z
- 샘플 가격값은 API 구조 검증용이며 견적 기준값으로 사용하지 않는다.
