# Observability and SLO

공식 근거(2026-07-09 확인): [Logging](https://docs.oracle.com/en-us/iaas/Content/Logging/Concepts/loggingoverview.htm), [Monitoring](https://docs.oracle.com/en-us/iaas/Content/Monitoring/Concepts/monitoringoverview.htm).

최소 범위: user SLI(availability/latency/errors/correctness), CPU/memory/disk/network/queue saturation, Audit/VCN Flow/LB/WAF/OS/app/DB 로그, UTC와 request/trace ID, PII/secret redaction, retention/archive/SIEM, 파이프라인 실패 알람, severity/threshold/window/absence/suppression/owner/runbook/escalation.

```bash
oci logging log-group list --compartment-id "$COMPARTMENT_OCID" --all --output json
oci monitoring alarm list --compartment-id "$COMPARTMENT_OCID" --all --output json
# metric/query syntax는 서비스 문서와 CLI help로 확정
```

Console graph만으로 운영 준비를 주장하지 않는다. 승인된 test alarm → Notification → 실제 on-call 수신 → ack → runbook → OK 복구를 증명한다. metric dimension 누락과 absent data 처리도 표본 검증한다.
