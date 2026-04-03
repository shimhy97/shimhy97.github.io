# Tasks: Weekly Tech Digest Agent

**Input**: Design documents from `/specs/001-weekly-tech-digest-agent/`  
**Prerequisites**: `spec.md`, `plan.md`

## Phase 1: Planning and Ralph State

- [x] T001 `specs/001-weekly-tech-digest-agent/plan.md`를 작성한다
- [x] T002 `specs/001-weekly-tech-digest-agent/tasks.md`를 작성한다
- [x] T003 `tasks/prd-weekly-tech-digest-agent-v1.md`와 `prd.json`을 새 기능 기준으로 정리한다

## Phase 2: Configuration and Data Shape

- [x] T004 `data/weekly-tech/sources.yml`을 추가하고 기본 소스 15개 이상을 등록한다
- [x] T005 `scripts/weekly-tech/models.py`에 공통 dataclass를 정의한다
- [x] T006 `scripts/weekly-tech/config_loader.py`에 YAML 로더와 검증 로직을 구현한다
- [x] T007 `.gitignore`에 Python 실행 산출물과 `data/weekly-tech/output/` 예외 규칙을 추가한다

## Phase 3: Collection and Selection

- [x] T008 `scripts/weekly-tech/collector.py`에 RSS/Atom 수집기를 구현한다
- [x] T009 `scripts/weekly-tech/collector.py`에 GitHub Releases API 수집기를 구현한다
- [x] T010 `scripts/weekly-tech/collector.py`에 HTML listing 수집기를 구현한다
- [x] T011 `scripts/weekly-tech/collector.py`에 중복 제거와 점수 계산 로직을 구현한다
- [x] T012 `scripts/weekly-tech/collector.py`에 category quota 적용 로직을 구현한다

## Phase 4: Summarization and Rendering

- [x] T013 `scripts/weekly-tech/summarizer.py`에 OpenAI Responses API 요약기를 구현한다
- [x] T014 `scripts/weekly-tech/summarizer.py`에 extractive fallback 요약기를 구현한다
- [x] T015 `scripts/weekly-tech/renderer.py`에 Jekyll Markdown 렌더링을 구현한다
- [x] T016 `scripts/weekly-tech/generate_digest.py`에 CLI 엔트리포인트를 구현한다
- [x] T017 `scripts/weekly-tech/requirements.txt`를 추가한다

## Phase 5: Automation and Validation

- [x] T018 `.github/workflows/weekly-tech-digest.yml`을 추가한다
- [x] T019 `tests/weekly-tech/`에 핵심 로직 테스트를 추가한다
- [x] T020 실제 수집을 한 번 실행해 `_posts/`에 주간 글을 생성한다
- [x] T021 `./scripts/blog-build.sh`와 Python 테스트로 기능을 검증한다
- [x] T022 `README.md`, `progress.txt`에 새 명령과 운영 흐름을 반영한다

## Phase 6: Delivery

- [x] T023 변경을 작은 단위 커밋으로 정리한다
- [x] T024 원격 PR 또는 배포 가능한 상태까지 반영한다
