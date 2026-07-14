# OCI 공개가격 견적 시스템 구현 패턴

OCI 공개 정가를 검색·계산·내보내기하는 시스템을 만들 때의 재사용 가능한 설계와 검증 기준이다.

## 데이터 원장과 메타데이터

- 가격 원장: `https://www.oracle.com/a/ocom/docs/pricing/cloud-price-list.json`
- 상품명·서비스·과금 단위 보강: `https://apexapps.oracle.com/pls/apex/cetools/api/v1/products/`
- `partNumber`로 결합한다. 정적 feed에만 있고 API 메타데이터가 없는 SKU는 단위를 추정하지 말고 자동 계산에서 제외한다.
- Feed의 `items`/`rangeItems`가 청구 단가 원장이고 `vcpuItems`/`vcpuRangeItems`는 별도 공식 overlay다. OCPU 가격을 일괄 1/2로 환산하지 않는다.
- `0`은 유효한 공개 가격이며 누락/null/빈 배열과 구분한다.
- 통화는 Oracle이 SKU에 직접 제공한 값을 사용하고 자체 환율 fallback을 하지 않는다.

## 동기화와 감사성

1. HTTPS로 임시 파일에 다운로드한다.
2. HTTP 상태·Content-Type·JSON schema·Decimal 값·range 연속성을 검증한다.
3. `buildId.buildDate`, `buildNumber`, 원본 byte size, SHA-256, 수집 UTC, URL을 기록한다.
4. API 메타데이터와 교집합 가격을 대조하고 대표 SKU를 재계산한다.
5. 검증 성공 후에만 atomic replace로 `latest` 캐시를 승격한다.
6. 실패 시 기존 정상 캐시를 byte-for-byte 보존하고 UI/export에 offline/stale 상태를 표시한다.

가격 feed가 현재 Oracle 응답과 같은지는 실행 시마다 다시 확인한다. 특정 build 번호나 hash를 영구 현재값으로 간주하지 않는다.

## 계산 모델

- 모든 계산은 binary float가 아니라 Decimal로 수행한다.
- Flat: `unit_price × quantity × monthly_usage × conversion_factor ÷ price_unit_size`.
- Range/tier는 구간 정렬, 0 시작, 연속성, 비중첩, 비음수 가격을 검증한 뒤 누진 합산한다.
- 공개 문서가 경계 포함 여부를 명시하지 않으면 `[min,max)`는 구현 가정으로 표시하고 실제 청구서 경계 대사를 잔여 위험으로 둔다.
- 시간→월 환산(예: 730시간), 할인율, 최소 사용량, 약정은 숨은 상수가 아니라 사용자에게 보이는 가정이어야 한다.
- 계약가격, 세금, Free Tier, 크레딧, 환율, 리전 가용성은 공개 정가 견적과 분리한다.

## 가격 무결성 신뢰 경계

브라우저나 API 호출자가 보낸 `unit_price`, `tiers`, `price_unit_size`, `conversion_factor`를 절대 계산 원장으로 사용하지 않는다.

- 클라이언트는 immutable product variant ID, SKU, 통화, 수량, 사용량만 전송한다.
- 서버는 variant ID+SKU+통화를 검증된 캐시에 다시 결합한다.
- 단가·tier·단위 크기·변환 계수는 서버 캐시에서만 읽는다.
- 클라이언트가 가격 메타데이터를 보내면 무시하기보다 4xx로 거부해 변조를 드러낸다.
- Export의 출처 URL/build/hash는 실제 계산에 사용한 서버 snapshot과 동일해야 한다.

이 경계가 없으면 임의 단가가 Oracle 공식 가격처럼 계산·내보내질 수 있다.

## 최소 API 검증

- 최상위 JSON object와 정확한 허용 키
- `lines`가 1개 이상인 배열이며 합리적인 최대 개수 이하
- 각 line이 object이고 필수/허용 키가 정확함
- finite Decimal, 수량 > 0, 사용량 >= 0, 할인율 0–100
- SKU/variant/currency 일치와 혼합 통화 차단
- invalid JSON, null/string/object lines, 빈 lines, 과다 lines, 알 수 없는 필드 모두 일관된 JSON 4xx
- malformed 요청 뒤 정상 요청이 성공하고 서버 로그에 traceback/connection abort가 없음
- loopback 전용 MVP라면 `127.0.0.1` 외 bind를 거부

## 독립 검수 세트

1. 현재 공식 feed를 새로 받고 build/hash를 캐시와 대조한다.
2. 제작 코드 계산 함수를 쓰지 않는 독립 Decimal 스크립트로 flat 5개 이상, tier 2개 이상을 재계산한다.
3. 임의 단가·tier·variant·SKU·통화 변조를 시도한다.
4. invalid/empty JSON, 타입 오류, 빈/최대 경계 line 수를 검사한다.
5. 네트워크 실패 시 정상 캐시 보존을 확인한다.
6. 정상 브라우저 흐름에서 검색→라인 추가→수량/사용량→할인→JSON/CSV export를 재현한다.
7. 제작자와 다른 검수자가 PASS/FAIL, 명령, exit code, 절대 경로를 기록한다.

## 운영·배포 게이트

로컬 산출물과 loopback 테스트는 준비 단계다. 외부 공개, 사내망 bind, `/api/refresh` 원격 호출, OCI 리소스 생성은 인증·TLS·권한·rate limit·감사로그 설계와 사용자 승인을 거친 별도 변경으로 취급한다.
