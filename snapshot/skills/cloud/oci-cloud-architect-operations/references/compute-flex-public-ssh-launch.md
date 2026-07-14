# OCI Flex Compute 생성: Public SSH, Balanced Boot, 검증

Compute Flex 인스턴스를 기존 VCN/subnet에 생성할 때 적용하는 증거 기반 절차다. 서비스·CLI 버전·이미지는 실행 시 다시 조회한다.

## 1. 요청과 승인 범위 고정

최소 입력:
- region, compartment, display name
- shape, OCPU, memory
- OS 계열/버전 또는 이미지 선택 규칙
- boot volume 용량과 VPU/GB
- VCN/subnet, public IP 여부
- SSH 공개키의 출처와 fingerprint
- 월 비용 가정과 제외 항목
- public exposure 예외, rollback/삭제 권한

`등록된 public key`를 API signing key로 해석하지 않는다. SSH용 OpenSSH 공개키인지 확인하고, 키 원문 대신 경로·개수·fingerprint를 증거로 남긴다. 대응 private key를 실제로 확인하지 않았다면 SSH 로그인 성공을 주장하지 않는다.

## 2. Read-only discovery

```bash
oci iam availability-domain list --compartment-id "$OCI_COMPARTMENT_ID"
oci compute shape list --compartment-id "$OCI_COMPARTMENT_ID" \
  --availability-domain "$AD" --all
oci compute image list --compartment-id "$OCI_COMPARTMENT_ID" \
  --operating-system 'Oracle Linux' --shape "$SHAPE" \
  --sort-by TIMECREATED --sort-order DESC --all
oci network vcn list --compartment-id "$OCI_COMPARTMENT_ID" --all
oci network subnet list --compartment-id "$OCI_COMPARTMENT_ID" --all
oci compute instance list --compartment-id "$OCI_COMPARTMENT_ID" \
  --display-name "$DISPLAY_NAME" --all
```

기존 public subnet이면 반드시 route table, security list, NSG를 읽는다. `0.0.0.0/0 -> Internet Gateway`와 TCP/22 `0.0.0.0/0` 허용을 별도 위험으로 표시한다. Security List와 NSG 허용은 합집합이므로 NSG를 추가해 기존 넓은 Security List 허용을 축소할 수 있다고 가정하지 않는다.

## 3. Limit와 capacity

Limit definition 목록은 tenancy OCID를 요구할 수 있고, resource availability는 workload compartment와 AD를 사용한다.

```bash
oci limits definition list \
  --compartment-id "$TENANCY_OCID" \
  --service-name compute --all

oci limits resource-availability get \
  --compartment-id "$OCI_COMPARTMENT_ID" \
  --service-name compute \
  --limit-name standard-e5-core-count \
  --availability-domain "$AD"
```

Limit 여유는 물리 capacity 보장이 아니다. launch 응답과 work request/waiter 결과를 최종 근거로 삼는다.

## 4. Balanced Boot Volume 가격

Balanced boot 비용을 단순 `GB-month`로만 계산하지 않는다. 공개 가격표에서 다음을 별도 합산한다.

1. Compute OCPU/hour
2. Compute memory GB/hour
3. Block Volume capacity GB/month
4. Balanced performance VPU/month 또는 해당 feed의 공식 과금 단위

Decimal로 계산하고 730시간/월 같은 가정을 표시한다. 세금, 계약 할인, 크레딧, egress, backup, logging은 포함 여부를 명시한다. 견적이 수정되면 증가분과 새 합계를 보여 주고 비용 승인을 갱신한다.

## 5. 설치된 CLI의 payload 확인

명령을 문서 기억으로 작성하지 말고 설치된 CLI에서 확인한다.

```bash
oci --version
oci compute instance launch --help
oci compute instance launch --generate-param-json-input source-details
```

일부 OCI CLI 버전은 `--boot-volume-vpus-per-gb` 같은 독립 옵션을 제공하지 않는다. 이 경우 image source details 안에 `bootVolumeSizeInGBs`와 `bootVolumeVpusPerGB`를 넣는다.

```bash
SOURCE_DETAILS=$(jq -cn --arg image_id "$IMAGE_ID" '{
  sourceType: "image",
  imageId: $image_id,
  bootVolumeSizeInGBs: 50,
  bootVolumeVpusPerGB: 10
}')

oci compute instance launch \
  --compartment-id "$OCI_COMPARTMENT_ID" \
  --availability-domain "$AD" \
  --display-name "$DISPLAY_NAME" \
  --shape 'VM.Standard.E5.Flex' \
  --shape-config '{"ocpus":1,"memoryInGBs":8}' \
  --subnet-id "$SUBNET_ID" \
  --assign-public-ip true \
  --ssh-authorized-keys-file "$SSH_PUBLIC_KEY_FILE" \
  --source-details "$SOURCE_DETAILS" \
  --wait-for-state RUNNING
```

실제 필드명은 `--generate-param-json-input source-details` 결과와 대조한다. launch 스크립트는 단일 write만 포함하고, preflight에서 이름 중복·target·hash·승인·용량을 확인하며, 한 번의 API 시도 여부를 기록한다.

클라이언트 parser가 API 호출 전에 실패했다면 resource ID/service response가 없음을 증거로 확인한다. 교정은 승인된 리소스 사양·수량·비용·노출 범위를 바꾸지 않는 구현 수정으로 분류할 수 있지만, 새 payload는 독립 재검수 후 실행한다. 범위가 달라지면 사용자 재승인을 받는다.

## 6. 사후 검증

독립 검수자는 fresh read-only API로 확인한다.

- display name 결과가 정확히 1개
- lifecycle state `RUNNING`
- shape와 shape config의 OCPU/memory
- image OCID와 승인 이미지
- boot volume 크기와 VPU/GB
- VNIC가 승인 subnet에 연결
- public/private IP 존재 여부
- TCP/22 도달성
- 추가 VCN/subnet/route/security/IAM 변경 부재

TCP connect 성공은 SSH 인증 성공이 아니다. 대응 private key로 host key를 확인하고 실제 로그인한 경우에만 `ssh opc@<ip>` 인증 성공을 보고한다.

## 7. 실패와 rollback

- parser 실패: API 호출 부재를 확인하고 payload를 교정·재검수한다.
- 부분 생성/UNKNOWN: 추가 write를 멈추고 instance/work request/VNIC/boot volume을 read-only 수집한다.
- stop/terminate/delete가 승인 범위에 없으면 자동 rollback하지 않는다.
- compute 과금 중단을 위해 stop이 필요해도 별도 승인 범위를 확인한다. boot volume·public IP·backup 비용은 계속될 수 있음을 알린다.
