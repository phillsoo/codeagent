# FinOps, Limits, Capacity

공식 근거(2026-07-09 확인): [Budgets](https://docs.oracle.com/en-us/iaas/Content/Billing/Concepts/budgetsoverview.htm), [Cost Analysis](https://docs.oracle.com/en-us/iaas/Content/Billing/Concepts/costanalysisoverview.htm), [Limits](https://docs.oracle.com/en-us/iaas/Content/General/Concepts/servicelimits.htm).

검토: compartment/tag/service/SKU별 actual/forecast/variance/owner; OCPU/memory/storage/IOPS/egress/LB/IP/backup/log/DR 비용; shared allocation과 tag coverage; idle/orphan 후보 및 dependency; p95/p99·peak·HA headroom·성장·commitment lock-in.

Budget은 soft limit/alert이며 hard cap이 아니다. 자동 중지/삭제는 위험 변경이다.

```bash
oci budgets budget budget list --compartment-id "$TENANCY_OCID" --all --output json
oci limits service list --all --output json
# value/resource-availability의 scope/options는 help로 확인
```

limit, quota, physical capacity를 구분한다. DR/autoscaling surge, 증액 lead time, reservation을 검토한다. 가격은 실행일 OCI Price List/Cost Estimator/API로 재확인한다.
