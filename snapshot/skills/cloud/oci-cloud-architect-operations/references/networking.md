# Networking

공식 근거(2026-07-09 확인): [Networking](https://docs.oracle.com/en-us/iaas/Content/Network/Concepts/overview.htm), [Security Rules](https://docs.oracle.com/en-us/iaas/Content/Network/Concepts/securityrules.htm).

CIDR가 on-prem/peer/DR/향후 확장과 겹치지 않는지, regional subnet 우선 여부, public IP 대안(NAT/Service Gateway/private endpoint), 양방향 route/return path, DRG distribution, NSG/security list/host firewall, stateful/stateless와 ephemeral port, DNS/MTU/LB timeout/retry/FastConnect·IPSec 이중화를 검토한다.

Read-only:
```bash
oci network vcn list --compartment-id "$COMPARTMENT_OCID" --all --output json
oci network subnet list --compartment-id "$COMPARTMENT_OCID" --all --output json
oci network nsg list --compartment-id "$COMPARTMENT_OCID" --all --output json
oci network route-table get --rt-id "$ROUTE_TABLE_OCID" --output json
oci network security-list get --security-list-id "$SECURITY_LIST_OCID" --output json
```

장애 순서: source/destination/port/protocol/UTC 고정 → DNS → client route → DRG/gateway/route → NSG/security list → Flow Logs → LB/backend → host firewall/listener → return path.

route/DRG/gateway/NSG/security list/public IP/LB listener는 고위험이다. flow matrix, before/after, 기존 연결, asymmetric route, canary, rollback, maintenance window 승인이 필요하다. 진단을 위해 허용 범위를 넓히지 않는다.
