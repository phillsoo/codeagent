# IAM, Compartment, Tagging

공식 근거(2026-07-09 확인): [IAM](https://docs.oracle.com/en-us/iaas/Content/Identity/Concepts/overview.htm), [Policies](https://docs.oracle.com/en-us/iaas/Content/Identity/Concepts/policies.htm), [Compartments](https://docs.oracle.com/en-us/iaas/Content/Identity/Tasks/managingcompartments.htm), [Tagging](https://docs.oracle.com/en-us/iaas/Content/Tagging/Concepts/taggingoverview.htm).

1. tenancy owner, federation/MFA, break-glass, RACI를 정한다.
2. prod/non-prod, 플랫폼/워크로드, 데이터 등급, 수명주기, 비용 owner로 compartment를 나눈다.
3. principal→group/dynamic group→policy→resource 경로를 그린다.
4. `inspect/read/use/manage`, resource type, scope, condition을 최소화한다. 일반 policy는 allow + implicit deny 모델이다.
5. CostCenter, Owner, Environment, DataClassification, Expiry를 defined tag/tag default로 검토한다.
6. inheritance, resource move, network `use`, tag namespace의 간접 권한을 검토한다.

Read-only 예:
```bash
oci iam compartment list --compartment-id "$TENANCY_OCID" --compartment-id-in-subtree true --all --output json
oci iam policy list --compartment-id "$COMPARTMENT_OCID" --all --output json
oci iam dynamic-group list --compartment-id "$TENANCY_OCID" --all --output json
oci iam tag-default list --compartment-id "$COMPARTMENT_OCID" --all --output json
```

policy/group/dynamic-group/identity-domain/MFA/tag-default/compartment move는 접근 확대·상실·비용 귀속 영향이 있다. effective access diff, break-glass, 승인, rollback과 독립 검수 전 실행하지 않는다.
