# OCI Integrated Sales Platform

CRM, OCI 견적, Consumption, Weekly Report, Demo Gallery를 하나의 FastAPI App Shell로 보여주는 **localhost Preview와 목표 배포 템플릿**입니다. 운영 배포 패키지가 아닙니다.

## 현재 범위

- 로컬 SQLite 모드에서 동작하는 API/UI MVP
- Oracle Autonomous AI Database용 DDL
- Oracle Linux 9 + systemd + Nginx TLS 배포 템플릿
- preflight/configure_host/install/verify/rollback 스크립트
- 테스트용 고객 데이터나 비밀정보 미포함
- 실제 OCI 서버/DB 변경 미실행

> **NO-GO:** Oracle runtime adapter는 v0.1.1에 포함되지 않음. 현재 wheel은 localhost SQLite preview 전용이며 인증·OIDC/RBAC도 구현되지 않았습니다. Nginx 템플릿은 원격 접근을 차단하며 preflight는 항상 운영 배포를 중단합니다. `ADBHERMES` 운영 배포는 Oracle repository adapter, 인증·권한, DB credential, 실제 migration·복구·UAT 검증 및 G0~G8 승인 후에만 가능합니다.

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
2. schema owner/migration/runtime/read-only 계정 분리와 객체별 최소권한 증거
3. DB secret·Wallet의 Vault reference, rotation/revoke 및 접근 감사
4. DB migration 전 backup/restore 검증
5. 443 ingress, DNS, TLS certificate
6. VNIC→subnet→route→NSG/security list→host firewall effective-path 증거
7. OCI IAM OIDC/MFA/RBAC, API authorization 및 감사 구현
8. CRM Privacy/DPIA, Demo 격리, E2E/UAT/복구 drill
9. 유지보수 창, reviewer, rollback owner 및 G0~G8 승인

`deploy/preflight.sh`는 v0.1.1에서 항상 NO-GO로 종료합니다. 승인 게이트와 Oracle·인증 구현이 끝나기 전에는 `configure_host.sh` 또는 `install.sh`를 운영 서버에서 실행하지 마십시오.

## 데이터 연동

- Price List: Oracle 공개 Pricing API를 매일 동기화하고 Quote에 catalog version snapshot 저장
- Consumption: OCI Usage API 일 단위 증분 수집, 최근 3일 재수집으로 후행 보정
- Account: 첨부 XLSX는 공개 저장소에 포함하지 않으며 staging/validation 후 승인 merge
- Demo: `oracle.com`, `oraclecloud.com` allowlist와 운영 데이터 격리

## 비밀정보 처리

`.env.example`에는 비밀값이 없습니다. 운영 비밀번호는 `/etc/hermes-sales/secrets/` 또는 OCI Vault에서 런타임에 주입하며 Wallet, private key, token을 Git에 커밋하지 않습니다.
