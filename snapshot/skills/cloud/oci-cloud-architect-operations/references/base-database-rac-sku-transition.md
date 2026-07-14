# Base Database RAC SKU 전환·최소견적 검증

Base Database Service의 가격체계 또는 shape 세대가 바뀔 때 기존 RAC 고객의 SKU를 매핑하고 최소 구성을 비교하는 절차다. 신규 SKU가 보인다는 이유만으로 기존 RAC의 후속 SKU라고 단정하지 않는다.

## Applicability gate

가격 계산 전에 다음을 Oracle 현재 서비스 문서와 UCM에서 확인한다.

1. shape가 single-node 또는 multi-node RAC를 지원하는가
2. 지원 DB 버전과 edition은 무엇인가
3. 노드당 최소 OCPU/ECPU와 증분 단위는 무엇인가
4. RAC에 필요한 edition 또는 BYOL option 권리는 무엇인가
5. shape별 storage meter가 Base Database Storage인지 OCI Block Volume/Performance인지
6. UCM의 `For use with` 결합 규칙이 무엇인가

지원 범위가 다르면 비용이 낮아도 **비동등 대안**으로 분리한다. RAC, 노드 HA, Extreme Performance, DB 버전 중 하나라도 빠지면 “후속 SKU” 또는 “절감 대체안”으로 표현하지 않는다.

## 2026-06-30 검증 사례

Oracle UCM v063026 및 Base Database 현재 문서에서 확인한 구조:

- Multi-node RAC는 2 VM이며 최소 2 OCPU/node, 총 4 OCPU다.
- RAC는 Extreme Performance가 필요하거나 BYOL 시 고객의 Database EE/RAC Option 권리가 필요하다.
- `VM.BaseDB.x86`/`VM.Standard.x86` generation-agnostic ECPU shapes는 최소 4 ECPU, 26ai only, single-node only다.
- 따라서 신규 `B112724 + B112725~B112728 + B111584` 조합은 기존 2-node RAC의 동등 대체가 아니다.
- RAC 요구 유지 시 OCPU 기반 shape에서 `B90572`(Extreme Performance license included) 또는 `B90573`(BYOL)과 해당 storage meter를 유지한다.
- UCM Appendix 매핑: `B88291 → B90572`, `B88404 → B90573`.
- `B111584`는 신규 SKU가 아니라 기존 storage SKU의 가격 변경 및 신규 x86 조합 구성요소다. 신설 SKU 표에 함께 넣어 신규로 오인시키지 않는다.

### 날짜를 종료일로 오해하지 않기

- UCM·가격표·문서의 `2026-06-30` 발효일 또는 갱신일만으로 **OCPU RAC 신규 생성 종료**를 결론내리지 않는다.
- Oracle 공개 문서가 OCPU flexible shapes(AMD E4/E5, Intel X9 등)를 “available shapes”로 열거하고, provisioning 문맥에서 “Multi-node RAC DB systems require a minimum of two OCPUs per node”라고 명시하면 공개 정책상 OCPU RAC 생성 경로가 유지되는 근거다.
- generation-agnostic x86 ECPU shape가 추가돼도 이는 26ai·single-node 전용이므로 RAC의 OCPU 경로를 대체하거나 폐지했다는 뜻이 아니다.
- 종료 여부를 확정하려면 공개 문서 외에도 대상 tenancy/region의 Console 또는 API shape 노출, service limit, capacity, 계약 주문서와 Oracle의 별도 retirement 공지를 확인한다. 리전 용량 부족이나 SKU 미노출을 전사 정책 종료로 일반화하지 않는다.
- 고객 답변에서는 `정책상 생성 가능`과 `특정 tenancy/region에서 지금 생성 가능`을 구분한다.

공식 근거:

- Oracle Base Database Service, **About DB Systems → Available Shapes and How It Determines the Resources Allocated**: https://docs.oracle.com/en/cloud/paas/base-database/about-dbs/index.html#AVDDS-GUID-3452CF5F-0245-4F5C-8C96-378F2A41D5A1
- Oracle Base Database Service, **Change the Shape of a DB System**: https://docs.oracle.com/en/cloud/paas/base-database/shape-dbs/

위 SKU·단가·지원범위는 시점별 사례이며 현재값으로 재사용하지 말고 Oracle 최신 문서/feed/주문서로 다시 확인한다.

## 최소 구성 계산 템플릿

가정을 먼저 적는다.

```text
monthly_hours = 744  # 가정이며 계약/견적기 기준 재확인
nodes = 2
cpu_per_node = 2 OCPU
billable_cpu = nodes * cpu_per_node
storage_gb = published minimum total storage
vpu_per_gb = selected performance tier
```

월 비용:

```text
compute = billable_cpu * compute_rate_per_hour * monthly_hours
storage = storage_gb * storage_rate_per_gb_month
performance = storage_gb * vpu_per_gb * performance_rate
monthly_total = compute + storage + performance
```

- storage 표의 data/recovery/system reserved 합계가 실제 billable capacity와 같은지 견적기에서 검증한다.
- RAC 공유 storage라도 compute는 두 노드의 합계로 계산한다.
- 공개 PAYG list price와 계약 할인/세금/리전 가격을 구분한다.
- BYOL 가격에는 고객의 기존 라이선스 비용이 포함되지 않는다.

## 결과 표 권장 형식

```markdown
| 요구사항 | 기존 SKU | 현재 제안 SKU | 단위/수량 | 전 월비용 | 후 월비용 | 동등성 | 근거 |
```

동등성은 `동등`, `비동등(single-node)`, `권리 확인 필요(BYOL)`처럼 명시한다.

## 제안 분기

- RAC/19c/2-node 유지: 기존 OCPU RAC shape와 현재 UCM에 등재된 Base Database RAC SKU를 유지한다.
- RAC 불필요 + 지원 버전 single-node 허용: 신규 x86 infrastructure + edition/BYOL + storage SKU를 별도 대안으로 계산한다.
- RAC는 불필요하지만 HA 필요: Data Guard 등 2-system 설계로 다시 산정한다. single-node 최소 금액을 HA 견적으로 재사용하지 않는다.
- 고객용 확정 견적: region availability, capacity, DB version, discount, tax, storage/VPU, BYOL/RAC 권리를 OCI Estimator·주문서·라이선스 담당자와 재확인한다.

## Pitfalls

1. 신규 ECPU SKU를 이름·단가만 보고 RAC 후속 SKU로 매핑한다.
2. `B111584` 같은 기존 SKU를 신규 조합에 포함됐다는 이유로 신규 SKU라고 부른다.
3. 2-node RAC와 1-node 비용을 절감률만으로 비교하고 기능/HA 차이를 숨긴다.
4. 구 명칭 SKU와 현재 SKU의 UCM Appendix 매핑을 확인하지 않는다.
5. OCPU shape의 Block Volume meter와 ECPU x86 shape의 Database Storage meter를 섞는다.
6. BYOL 고객의 RAC Option 권리를 확인하지 않고 BYOL 견적을 확정한다.
7. quality 검수에서 표현 또는 가정 결함이 발견됐는데 수정본을 다시 확인하지 않고 PASS로 보고한다.
