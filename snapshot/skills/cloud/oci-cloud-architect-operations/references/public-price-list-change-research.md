# OCI 공개 가격표 변경 조사

OCI의 특정 날짜 전후 SKU·단가 변경을 재현 가능하게 확인할 때 사용한다. 검색 결과나 현재 가격표만으로 과거 가격을 추정하지 않는다.

## 핵심 출처

1. 사람이 읽는 현재 가격표: `https://www.oracle.com/cloud/price-list/`
2. 가격표가 동적으로 읽는 JSON feed: `https://www.oracle.com/a/ocom/docs/pricing/cloud-price-list.json`
3. Oracle PaaS/IaaS Universal Credits Service Descriptions PDF: `https://www.oracle.com/contracts/docs/paas_iaas_universal_credits_3940775.pdf`
4. 서비스별 Oracle What's New / release notes
5. Internet Archive CDX와 원본(raw) snapshot

가격표 HTML은 가격을 직접 포함하지 않고 `data-partnumber`만 넣은 뒤 JSON feed에서 통화를 주입할 수 있다. 따라서 HTML 텍스트만 비교하면 상품명/SKU 추가는 찾을 수 있어도 단가 차이를 놓친다.

## 절차

### 1. 변경 경계 고정

- 요청 날짜 직전과 직후의 HTML, 가격 JSON, UCM PDF snapshot을 각각 찾는다.
- CDX 예시:

```text
https://web.archive.org/cdx/search/cdx?url=www.oracle.com/cloud/price-list/&from=YYYY&to=YYYY&output=json&fl=timestamp,original,statuscode,digest&filter=statuscode:200
https://web.archive.org/cdx/search/cdx?url=www.oracle.com/a/ocom/docs/pricing/cloud-price-list.json&from=YYYY&to=YYYY&output=json&fl=timestamp,original,statuscode,digest&filter=statuscode:200&collapse=digest
https://web.archive.org/cdx/search/cdx?url=www.oracle.com/contracts/docs/paas_iaas_universal_credits_3940775.pdf&from=YYYY&to=YYYY&output=json&fl=timestamp,original,statuscode,digest&filter=statuscode:200
```

- snapshot 원문은 `https://web.archive.org/web/<timestamp>id_/https://...` 형식으로 받는다. `id_`는 Wayback이 링크나 본문을 다시 쓰지 않은 원문 비교에 유용하다.
- CDX가 일시적으로 5xx/timeout이면 쿼리 범위와 반환 필드를 줄여 재시도한다. 실패 자체를 영구적 제약으로 기록하지 않는다.

### 2. 가격 JSON 자체 시각 확인

JSON의 `buildId.buildDate`, `buildId.buildNumber`, `buildId.instance`를 기록한다. Wayback 캡처 시각과 실제 feed build 시각을 구분한다.

주요 구조:

- `items[partNumber][currency]`: 기본/OCPU/서비스 단가
- `vcpuItems[partNumber][currency]`: 비교용 vCPU 단가
- `rangeItems`, `vcpuRangeItems`: 구간 단가

USD 조사라면 `items[SKU].USD`를 기준으로 하고, 웹 표의 “comparison price (/vCPU)”를 실제 청구 단가와 혼동하지 않는다.

### 3. HTML에서 SKU-상품명-단위 매핑

현재 공개 PAYG 단가를 SKU별로 빠르게 재검증할 때는 Oracle Pricing API도 함께 사용할 수 있다.

```text
https://apexapps.oracle.com/pls/apex/cetools/api/v1/products/?partNumber=<PART_NUMBER>
```

응답에서 `displayName`, `metricName`, USD `PAY_AS_YOU_GO` 값을 함께 보존한다. 가격 페이지의 동적 셀보다 재현하기 쉽지만, 이 endpoint는 **현재값 확인용**이므로 과거 가격은 반드시 같은 시점의 archived JSON feed와 비교한다.

각 `<tr data-partnumber="B...">`에서:

- SKU: `data-partnumber`
- 상품명: 첫 번째 셀
- 단위: 마지막 셀

을 추출한다. 같은 SKU가 여러 구간에 나타날 수 있으므로 `data-minrange`도 보존한다. 변경 전·후 HTML의 SKU 집합을 비교해 신규/삭제/명칭 변경을 찾고, 단가는 같은 시점의 JSON에서 조인한다.

### 4. UCM PDF로 SKU 존재와 사용 규칙 교차검증

직전·변경 PDF를 텍스트로 변환하여 다음을 확인한다.

- 표지의 `Effective Date`와 문서판(`Oracle UCM V...`)
- part number가 어느 판본에서 처음 등장하는지
- metric/unit
- “For use with” 결합 규칙
- 신규 shape 사용 시 infrastructure + storage + license SKU가 함께 청구되는지

UCM은 SKU와 서비스 규칙의 공식 근거지만 공개 list price를 항상 포함하지는 않는다. 단가는 가격 JSON에서 가져오고 PDF에서 임의 계산하지 않는다.

### 5. 공식 서비스 문서/공지 교차검증

Oracle What's New에서 release date, 신규 hardware generation, 신규 infrastructure SKU, billing metric 설명을 찾는다. 별도 가격변경 공지를 발견하지 못했다면 그대로 명시한다. 제품 출시일과 가격 시행일을 같은 것으로 단정하지 않는다.

### 6. 결과 분류

각 SKU를 다음 중 하나로 분류한다.

- 기존 SKU 단가 변경
- 신규 SKU와 최초 확인 단가
- 명칭만 변경
- 비교 범위 내 변화 없음
- 근거 부족/미확인

변화 없음도 핵심 서비스군별로 명시한다. “찾지 못함”을 “변경 없음”으로 바꾸지 말고, 동일 SKU가 양쪽 snapshot에 있고 값이 같을 때만 변경 없음이라고 한다.

## 산출물 표

```markdown
| 서비스군 | SKU | 상품명 | 단위 | 전 단가 | 후 단가 | 절대 증감 | 증감률 | 근거 |
```

- 통화와 list price 여부를 제목에 명시한다.
- 증감률은 계산 도구로 산출한다.
- 신규 SKU의 전 단가는 `없음(직전 snapshot 미등재)`으로 표시하며 0으로 처리하지 않는다.
- 정확한 시행일은 UCM effective date, JSON build timestamp, archive capture timestamp를 각각 분리해 제시한다.
- 계약/가격표의 effective date를 전 서비스의 일괄 가격변경일로 표현하지 않는다. 공식 근거가 없다면 `YYYY-MM-DD 기준으로 확인된 현재 구조` 또는 `해당 날짜 문서에 반영된 신규 SKU`라고 쓴다.
- 중요 고객 자료는 원시 가격 증거를 보존하고 독립 검수한다. 검수 지적을 반영해 파일이 바뀌면 수정본을 다시 검수하며, 이전 revision의 conditional pass를 최종 승인으로 간주하지 않는다.

## 해석 규칙

- 동일한 DB ECPU 라이선스 단가가 유지되어도 별도 infrastructure SKU가 신설되거나 storage 단가가 오르면 총비용은 변한다. DB software, infrastructure, storage를 분리해서 diff한다.
- 기존 SKU 값 변경과 신규 hardware shape/SKU 추가는 별도 사건으로 기록한다.
- 공개 가격 셀이 공란이면 `$0`이 아니다. 견적/계약 가격일 수 있으므로 “공개 자료로 증감 확인 불가”라고 쓴다.
- Developer `$0` SKU는 흔히 DB 라이선스 fee waiver다. Dedicated 인프라비는 남을 수 있고 Cloud@Customer는 이미 약정한 인프라 안에서만 추가비용이 없을 수 있으므로 공식 문구를 확인한다.
- legacy OCPU와 신규 ECPU SKU가 함께 남아 있어도 신규 배포에 모두 적용된다고 단정하지 않는다. shape/세대별 applicability와 `For use with` 규칙을 확인한다.
- OCPU/ECPU 단가 비율은 공개 가격의 반올림 때문에 정확히 정수가 아닐 수 있다. 서비스별 관계를 확인한 뒤 `공개 반올림 단가 기준 약 4배`처럼 표현하고, 단위 전환과 실질 가격 인상을 구분한다.
- 최소 구성 총액이나 증감률은 계산 도구로 산출하고 서버 수·노드 수·가동시간 가정을 명시한다.

## 검증 사례: 2026-06-30 전후 OCI Database

공식 JSON 보존본의 경계는 다음과 같았다.

- 직전: Wayback `20260614104929`, Oracle `buildId.buildDate=2026-06-11`, build 345
- 직후: Wayback `20260702031831`, Oracle `buildId.buildDate=2026-07-01`, build 347

대표 diff:

- Base Database Storage `B111584`: USD `0.0595 → 0.12`; x86 compute infrastructure `B112724`와 x86 DB SKU `B112725`–`B112728` 신규
- Exadata Dedicated X11M DB server `B110627`: `2.9032 → 6.3014`; storage server `B110629`: `2.9032 → 5.4795`; X11MV `B112666`/`B112667` 신규
- Exascale RDMA compute `B109355`: `0.025 → 0.0375`; VM filesystem `B107951`: `0.0425 → 0.0999`; smart DB storage `B107952`: `0.1156 → 0.1953`; flash cache `B109375`: `0.0005 → 0.0009`
- ExaCC 공개 DB ECPU/BYOL SKU는 양쪽에서 동일했고 랙 인프라 가격 셀은 공란이었다. 따라서 공개 자료로는 랙 인프라 가격 증감을 확정하지 않았다.

이 숫자는 조사법 검증 사례이며 영구 현재값이 아니다. 향후 사용 시 Oracle 현재 feed와 문서를 다시 조회한다.

## Pitfalls

1. 현재 웹페이지와 검색 snippet만 비교해 과거 가격을 복원하지 않는다.
2. HTML 표의 빈 가격 셀을 무료/0으로 읽지 않는다. JavaScript가 JSON feed에서 주입한다.
3. 요청 날짜의 가격 HTML snapshot 시각을 JSON URL에 그대로 대입하고 그 응답을 당시 JSON으로 간주하지 않는다. 해당 JSON 캡처가 실제로 존재하는지 CDX에서 찾고 `buildId`와 해시를 검증한다.
4. vCPU comparison price와 OCPU/ECPU 청구 단가를 섞지 않는다.
5. 새 SKU가 기존 SKU를 완전히 대체했다고 사용 규칙 확인 없이 단정하지 않는다.
6. 제품 release date나 PDF 시행일만으로 모든 가격이 그 시각에 청구 반영됐다고 단정하지 않는다. feed build 시각, archive capture 시각, 별도 공지를 분리해 보고한다.
7. 공식 가격 인상 공지를 못 찾았으면 추측성 원인을 붙이지 않는다.
8. 라이선스 단가가 동일하다는 이유만으로 “가격 변화 없음”이라 쓰지 않는다. 인프라·스토리지 SKU를 먼저 확인한다.
