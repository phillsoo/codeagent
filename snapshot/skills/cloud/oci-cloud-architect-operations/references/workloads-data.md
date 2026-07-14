# Compute, Storage, Database

공식 근거(2026-07-09 확인): [Compute](https://docs.oracle.com/en-us/iaas/Content/Compute/References/bestpracticescompute.htm), [Block Volume](https://docs.oracle.com/en-us/iaas/Content/Block/Concepts/overview.htm), [Object Storage](https://docs.oracle.com/en-us/iaas/Content/Object/Concepts/objectstorageoverview.htm), [Database](https://docs.oracle.com/en-us/iaas/Content/Database/Concepts/databaseoverview.htm).

Compute: shape/OCPU/memory/NUMA/local NVMe/license를 측정 부하와 연결한다. FD/AD, pool/autoscaling, reservation, image provenance, cloud-init, patch SLA, 재생성 가능성을 검토한다. instance 안에 유일 데이터/장기 secret을 두지 않는다. OCI 필수 metadata/iSCSI/firewall 경로를 임의 수정하지 않는다.

Storage: Block 성능·attachment·backup과 Object tier/lifecycle/retention/replication을 RPO/RTO·비용에 연결한다. application-consistent와 crash-consistent를 구분한다. multi-attach는 지원 cluster semantics 없이 동시 write하지 않는다. lifecycle/retention/key 변경은 삭제·복구 불능 위험 변경이다.

Database: Base DB, Exadata, Autonomous, HeatWave, PostgreSQL의 HA, backup, patch, CLI가 다르다. 서비스별 문서에서 HA unit, maintenance, PITR/archive log, retention/cross-region, standby lag, failover/failback, app reconnect, key/wallet/secret을 다시 확인한다. 보편 RPO/명령을 단정하지 않는다.

```bash
oci compute instance list --compartment-id "$COMPARTMENT_OCID" --all --output json
oci bv volume list --compartment-id "$COMPARTMENT_OCID" --all --output json
oci bv backup list --compartment-id "$COMPARTMENT_OCID" --all --output json
oci os bucket list --compartment-id "$COMPARTMENT_OCID" --all --output json
# DB는 대상 서비스 확정 후 `oci <service> --help` 사용
```

변경 전 backup 존재뿐 아니라 최근 restore, encryption/key access, 실제 RPO/RTO를 검증한다.
