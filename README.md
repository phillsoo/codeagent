# codeagent — Hermes configuration snapshot

재현 가능한 Hermes Agent 설정과 Nexus 에이전트 리소스를 **비밀정보 없이** 보관하는 저장소입니다.

## 포함 범위

- `snapshot/config/`: 기본 및 프로필별 Hermes 설정의 비밀값 제거본
- `snapshot/agents/`: 기본/전문 매니저의 `SOUL.md`, `profile.yaml`
- `snapshot/skills/`: 로컬 커스텀 스킬 전체와 Hermes 번들 스킬의 이름·소스 다이제스트 인벤토리
- `snapshot/automation/cron.jobs.sanitized.json`: Slack 식별자와 실행 상태를 제거한 자동화 정의
- `snapshot/organization/board.json`: Nexus Kanban 보드의 비밀정보 제거 메타데이터
- `manifest.json`: 생성 시각과 포함/제외 정책
- `scripts/sync_hermes.py`: 로컬 Hermes 상태에서 위 스냅샷을 다시 생성하는 스크립트

## 의도적으로 제외되는 항목

이 저장소는 현재 **공개(public)** 상태이므로 다음은 동기화하지 않습니다.

- `.env`, `auth.json`, OAuth/API 토큰, GitHub/Slack/클라우드 자격증명
- 세션 대화, 개인 메모리, Slack 채널·스레드·사용자 ID
- 로그, 캐시, 프로세스 상태, SQLite DB/WAL/lock
- `${HOME}/astra-organization/` 업무 산출물(고객·클라우드·운영 정보가 포함될 수 있음)
- Hermes 설치 소스와 가상환경(공식 저장소에서 재설치 가능)

## 동기화

```bash
python3 scripts/sync_hermes.py
```

실행 후 반드시 비밀정보 검사를 통과한 경우에만 커밋/푸시합니다.

> 이 저장소만으로 인증정보를 복원할 수는 없습니다. 인증은 대상 시스템에서 `hermes auth` 및 `gh auth login`으로 별도 구성해야 합니다.
