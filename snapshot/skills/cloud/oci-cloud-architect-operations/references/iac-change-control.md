# Terraform and Resource Manager Change Control

공식 근거(2026-07-09 확인): [Resource Manager](https://docs.oracle.com/en-us/iaas/Content/ResourceManager/Concepts/resourcemanager.htm), [Terraform Configurations](https://docs.oracle.com/en-us/iaas/Content/ResourceManager/Concepts/terraformconfigresourcemanager.htm).

1. provider/module version/source와 state backend/locking/access를 검토한다.
2. secret/credential/`.tfstate`를 bundle/Git/log에 넣지 않는다.
3. fmt/validate/policy/security scan을 실행한다.
4. plan을 보존하고 create/update/replace/destroy, IAM, network, public exposure, 비용을 요약한다.
5. 다른 검수자가 승인한다.
6. maintenance window에서 승인 plan만 apply하고 job/work request terminal state를 확인한다.
7. 기능/SLO/보안/비용과 drift/fresh plan 수렴을 확인한다.

Terraform은 자동 rollback 도구가 아니다. 이전 구성 재적용, recreation, backup restore, traffic/DNS 전환 중 방법을 정한다. partial apply 뒤 실제 상태/dependency를 먼저 조회한다. `-target`은 예외 복구용이다. Console emergency change는 Audit·승인을 기록하고 import/config 수정/rollback으로 reconcile한다.
