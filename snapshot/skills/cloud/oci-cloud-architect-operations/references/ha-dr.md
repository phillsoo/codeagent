# HA, Backup, Disaster Recovery

공식 근거(2026-07-09 확인): [Well-Architected](https://docs.oracle.com/en/solutions/oci-best-practices/index.html), [Architecture Center](https://docs.oracle.com/en/solutions/).

- HA: component/FD/AD 장애 중 지속 또는 빠른 회복
- Backup: 삭제·논리 손상·ransomware·operator error의 시점 복구
- DR: region/tenancy 재해의 business service 복구

절차: BIA와 승인 RTO/RPO → failure mode 분리 → compute/network/DNS/cert/key/secret/data/integration/observability dependency → consistency/보존/separate fault boundary/cross-region → 격리 restore와 checksum/DB consistency/app smoke → measured RPO/RTO → split-brain/reconciliation/failback → DR capacity/limit/quota/DNS TTL/credential 검증.

Full Stack DR 채택과 CLI subcommand는 대상 서비스·리전 확정 뒤 최신 Oracle 문서와 설치 CLI help로 재검증한다. 조사에서 추정 deep link가 404였으므로 고정 명령을 제공하지 않는다. backup job 성공만 있으면 복구 준비 완료가 아니다.
