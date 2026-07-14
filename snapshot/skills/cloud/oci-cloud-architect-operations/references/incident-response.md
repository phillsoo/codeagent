# OCI Incident Response

공식 근거(2026-07-09 확인): [Logging](https://docs.oracle.com/en-us/iaas/Content/Logging/Concepts/loggingoverview.htm), [Monitoring](https://docs.oracle.com/en-us/iaas/Content/Monitoring/Concepts/monitoringoverview.htm), [Cloud Guard](https://docs.oracle.com/en-us/iaas/cloud-guard/using/index.htm).

1. severity, IC, communications, scribe, UTC start, 영향/SLO를 기록한다.
2. Audit, alarms/metrics, logs, work requests, deploy/IAM/network diff 원본을 보존한다.
3. tenancy/region/AD/compartment/service/resource/client와 데이터 무결성 범위를 구분한다.
4. 가설마다 예상 관측, query, 결과, 반증 조건을 붙인다.
5. 가장 작은 reversible mitigation을 고른다. IAM/network/data/traffic/scale은 긴급 승인과 rollback owner가 필요하다.
6. synthetic/실제 client SLI, dependency, backlog/data consistency, alarms를 확인한다.
7. 임시 권한/route/scale을 회수하고 IaC를 reconcile한다.
8. timeline, root/contributing cause, detection/response gap, owner/date/evidence 조치를 작성한다.

네트워크 evidence chain: DNS → source route → DRG/gateway/route → NSG/security list → Flow Logs → LB/backend → host firewall/listener → return path.

금지: 증거 전 로그/자원 삭제, broad ingress/tenancy-wide 권한으로 시험, 다중 동시 변경, 고객 영향 종료 전 성공 선언.
