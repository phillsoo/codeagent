# OCI Integrated Sales Platform

CRM, OCI 견적, Consumption, Weekly Report, Demo Gallery를 하나의 FastAPI App Shell로 제공하는 배포 준비 패키지입니다.

## 현재 범위

- 로컬 SQLite 모드에서 동작하는 API/UI MVP
- Oracle Autonomous AI Database용 DDL
- Oracle Linux 9 + systemd + Nginx TLS 배포 템플릿
- preflight/configure_host/install/verify/rollback 스크립트
- 테스트용 고객 데이터나 비밀정보 미포함
- 실제 OCI 서버/DB 변경 미실행

## 로컬 실행

```bash
python3 -m venv .venv
.venv/bin/pip install -e '.[test]'
.venv/bin/uvicorn hermes_sales.main:app --app-dir src --host 127.0.0.1 --port 8080
```

검증:

```bash
.venv/bin/pytest -q
curl -fsS http://127.0.0.1:8080/healthz
curl -fsS http://127.0.0.1:8080/api/modules
```

## 운영 배포 전 승인 게이트

1. SSH private key 또는 승인된 Bastion/Run Command 경로
2. `HERMESUSER` 비밀번호의 Vault/0600 secret file 저장
3. 실제 대상 schema와 객체 권한 범위
4. DB migration 전 backup/restore 검증
5. 443 ingress, DNS, TLS certificate
6. 현재 공개 포트 22/8765/3389/1521의 NSG/CIDR 축소
7. OCI IAM OIDC/MFA/RBAC 구성
8. 유지보수 창, reviewer, rollback owner 승인

## 데이터 연동

- Price List: Oracle 공개 Pricing API를 매일 동기화하고 Quote에 catalog version snapshot 저장
- Consumption: OCI Usage API 일 단위 증분 수집, 최근 3일 재수집으로 후행 보정
- Account: 첨부 XLSX는 공개 저장소에 포함하지 않으며 staging/validation 후 승인 merge
- Demo: `oracle.com`, `oraclecloud.com` allowlist와 운영 데이터 격리

## 비밀정보 처리

`.env.example`에는 비밀값이 없습니다. 운영 비밀번호는 `/etc/hermes-sales/secrets/` 또는 OCI Vault에서 런타임에 주입하며 Wallet, private key, token을 Git에 커밋하지 않습니다.
