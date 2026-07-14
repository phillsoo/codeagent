# OCI 인증 선택 지침

확인일: 2026-07-09 UTC. 공식 근거: [SDK/CLI Configuration](https://docs.oracle.com/en-us/iaas/Content/API/Concepts/sdkconfig.htm), [Instance Principals](https://docs.oracle.com/en-us/iaas/Content/Identity/Tasks/callingservicesfrominstances.htm), [Token Authentication](https://docs.oracle.com/en-us/iaas/Content/API/SDKDocs/clitoken.htm).

| 상황 | 후보 | 통제 |
|---|---|---|
| OCI Compute 자동화 | instance principal | dynamic group/policy 최소 scope, instance compromise 검토 |
| 지원 OCI resource 자동화 | resource principal | 지원 여부와 policy를 현재 문서로 확인 |
| 사람의 단기 작업 | session/token auth | federation/MFA, 만료·profile·region 확인 |
| OCI 외부 CI/호스트 | API signing key 또는 지원 federation | 공유 금지, private key 0600, rotation/revocation, secret manager |
| Cloud Shell | 제공 세션 인증 | tenancy/region/session과 저장공간 취급 확인 |

금지: credential을 문서/Git/log/Terraform state에 저장, 개인 key 공유, 인증 장애를 tenancy-wide policy로 우회, `--auth`를 help 없이 추정.

Preflight: `oci --version`, `oci --help`, config 내용을 출력하지 않는 파일 존재/권한 점검, 조직이 허용한 harmless read-only call. 증거에는 auth 방식/profile만 남긴다. 실패 시 clock skew, region/profile, key permission, session expiry, dynamic-group matching rule, policy propagation 순으로 본다.
