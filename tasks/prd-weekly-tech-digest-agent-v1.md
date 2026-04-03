# PRD: 주간 최신 기술 다이제스트 에이전트 V1

## Introduction

이 기능은 공식 소스의 최신 개발 기술 업데이트를 1주 단위로 수집하고, 한국어 다이제스트 초안을 생성한 뒤 GitHub Pages 블로그에 게시 가능한 형태로 만드는 것을 목표로 한다. 초기 버전은 사람이 검토할 수 있도록 자동 PR 생성까지를 기본 운영 방식으로 둔다.

## Goals

- 공식 소스 15개 이상에서 최근 7일 후보를 수집한다.
- 규칙 기반 필터링으로 8~12개 핵심 항목을 선택한다.
- 한국어 다이제스트 Markdown 초안을 `_posts/`에 생성한다.
- GitHub Actions weekly schedule로 PR 생성까지 자동화한다.
- Jekyll build를 통과하는 실제 주간 글 1편을 생성한다.

## User Stories

### US-001: 소스 설정과 수집 파이프라인을 만든다
**Description:** As a blog owner, I want to collect official updates from curated sources so that I can build a reliable weekly candidate pool.

**Acceptance Criteria:**
- [ ] `data/weekly-tech/sources.yml`에 공식 소스 15개 이상이 등록된다
- [ ] RSS/Atom, GitHub Releases API, HTML listing 중 최소 2종 이상이 구현된다
- [ ] 최근 7일 항목만 정규화된 공통 스키마로 저장된다
- [ ] 중복 항목이 병합되거나 제거된다

### US-002: 주간 다이제스트 초안을 생성한다
**Description:** As a blog owner, I want the selected updates to be summarized into a Korean draft so that I can review and publish quickly.

**Acceptance Criteria:**
- [ ] category quota와 규칙 기반 필터링으로 8~12개 항목이 선택된다
- [ ] OpenAI 요약 또는 fallback 요약으로 한국어 문단이 생성된다
- [ ] `_posts/YYYY-MM-DD-weekly-tech-roundup.md` 파일이 생성된다
- [ ] `./scripts/blog-build.sh` passes

### US-003: 주간 실행을 GitHub Actions로 자동화한다
**Description:** As a blog owner, I want the digest generation to run weekly and open a PR so that I can keep publishing without manual repetition.

**Acceptance Criteria:**
- [ ] `.github/workflows/weekly-tech-digest.yml`이 schedule과 workflow_dispatch를 지원한다
- [ ] workflow가 Python 의존성을 설치하고 생성 스크립트를 실행한다
- [ ] 새 글 생성 시 PR을 자동으로 만든다
- [ ] run metadata artifact가 업로드된다

### US-004: 실제 초안 1편을 생성하고 검증한다
**Description:** As a reader, I want to see an actual weekly digest article so that I can evaluate the quality of the new automation.

**Acceptance Criteria:**
- [ ] 실제 실행으로 최신 기술 다이제스트 글이 1편 생성된다
- [ ] 글에는 수집 기간, 선정 기준, 카테고리별 항목, 원문 링크가 포함된다
- [ ] Python 테스트와 `./scripts/blog-build.sh`가 통과한다
- [ ] README와 progress log가 최신 상태를 반영한다

## Functional Requirements

- FR-1: 시스템은 공식 소스를 YAML 설정 파일로 관리해야 한다.
- FR-2: 시스템은 최근 7일 항목만 수집 대상으로 삼아야 한다.
- FR-3: 시스템은 중복 제거, include/exclude 규칙, quota 기반 선별을 지원해야 한다.
- FR-4: 시스템은 한국어 Markdown 초안을 자동 생성해야 한다.
- FR-5: 시스템은 GitHub Actions로 주간 실행과 PR 생성을 지원해야 한다.

## Non-Goals

- 이번 범위에서 완전 자동 무인 발행까지 진행하지 않는다.
- 이번 범위에서 데이터베이스나 외부 캐시를 도입하지 않는다.
- 이번 범위에서 비공식 커뮤니티 소스를 수집하지 않는다.

## Technical Considerations

- Python 3.12를 사용한다.
- 요약기는 OpenAI Responses API를 기본으로 두되 fallback을 허용한다.
- 기존 Jekyll Pages build는 `./scripts/blog-build.sh`를 그대로 사용한다.

## Success Metrics

- 주간 실행에서 최소 15개 공식 소스를 읽는다.
- 최종 글에 8개 이상 항목이 포함된다.
- 생성된 글이 추가 수동 수정 없이 빌드된다.
- 운영자가 PR을 15분 이내에 검토할 수 있다.

## Open Questions

- 기본 주간 발행 시각을 월요일 오전 9시 KST로 고정할지 추후 조정할지 검토가 필요하다.
- OpenAI API 키가 없는 환경에서 fallback 품질이 어느 정도까지 허용 가능한지 운영 중 판단이 필요하다.
