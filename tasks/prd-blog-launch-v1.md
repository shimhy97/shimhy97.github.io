# PRD: 데이터사이언티스트 기술 블로그 V1 런치

## Introduction

Jekyll 기반 GitHub 기술 블로그의 초기 골격은 만들어졌지만, 실제 운영 가능한 블로그가 되려면 브랜딩, 첫 글, 반복 가능한 작성 흐름, 배포 체크리스트가 더 필요하다. 이 PRD는 블로그를 "설정만 된 상태"에서 "실제로 글을 올릴 수 있는 상태"로 끌어올리는 것을 목표로 한다.

## Goals

- 블로그의 주제와 작성자 정체성이 첫 화면에서 분명히 드러나게 한다.
- 첫 번째 데이터사이언스 실전 글을 게시 가능한 수준으로 올린다.
- 반복 가능한 글 작성 템플릿과 체크리스트를 만든다.
- 배포와 운영 절차를 초보자도 따라갈 수 있게 문서화한다.

## User Stories

### US-001: 작성자 정보와 홈 화면 카피를 정리한다
**Description:** As a blog owner, I want to update the site identity so that readers immediately understand who I am and what this blog covers.

**Acceptance Criteria:**
- [ ] `_config.yml`의 title, description, author 정보를 실제 운영 정보에 맞게 수정한다
- [ ] 홈 화면 소개 문구가 데이터사이언스/기술 블로그 방향을 명확히 설명한다
- [ ] About 페이지 내용이 현재 경력과 다룰 주제를 반영한다
- [ ] `bundle exec jekyll build` passes

### US-002: 첫 번째 데이터사이언스 실전 글을 발행한다
**Description:** As a reader, I want to see a substantive first article so that I can judge the tone and depth of the blog.

**Acceptance Criteria:**
- [ ] `_posts/` 아래에 데이터사이언스 주제의 새 글을 1개 추가한다
- [ ] 글에는 문제 배경, 접근 방식, 코드 또는 쿼리 예시, 회고가 포함된다
- [ ] 카테고리와 태그가 실제 주제에 맞게 설정된다
- [ ] `bundle exec jekyll build` passes

### US-003: 재사용 가능한 포스트 템플릿과 작성 체크리스트를 만든다
**Description:** As a frequent writer, I want a repeatable writing template so that I can publish technical posts consistently.

**Acceptance Criteria:**
- [ ] 새 글 작성을 위한 Markdown 템플릿 파일 또는 문서를 추가한다
- [ ] front matter, 권장 섹션, 코드 블록 예시가 포함된다
- [ ] README 또는 별도 문서에 글 발행 체크리스트가 정리된다
- [ ] `bundle exec jekyll build` passes

### US-004: SEO와 공유에 필요한 기본 자산을 추가한다
**Description:** As a blog owner, I want better metadata and static assets so that shared links look more trustworthy.

**Acceptance Criteria:**
- [ ] 기본 social preview 또는 대표 이미지 전략이 문서화되거나 자산이 추가된다
- [ ] 404 페이지 또는 기본 안내 페이지를 추가한다
- [ ] 사이트 설명과 피드/SEO 관련 설정이 누락 없이 정리된다
- [ ] `bundle exec jekyll build` passes

### US-005: 배포 체크리스트와 운영 루틴을 정리한다
**Description:** As a beginner blog owner, I want a deployment and maintenance checklist so that I do not get stuck during publishing.

**Acceptance Criteria:**
- [ ] GitHub 저장소 생성, 원격 연결, Pages 활성화 순서가 문서화된다
- [ ] 로컬 개발, 초안 작성, 배포 확인 절차가 정리된다
- [ ] Ralph 사용 흐름과 수동 작업 흐름의 역할 분담이 설명된다
- [ ] `bundle exec jekyll build` passes

## Functional Requirements

- FR-1: 블로그 전역 메타데이터는 `_config.yml`에서 관리할 수 있어야 한다.
- FR-2: 홈 화면은 블로그의 주제와 작성자 성격을 짧게 설명해야 한다.
- FR-3: 첫 실전 포스트는 데이터사이언스 독자가 읽을 만한 수준의 깊이를 가져야 한다.
- FR-4: 반복 작성용 템플릿과 체크리스트가 저장소 안에 있어야 한다.
- FR-5: 초보자도 배포 흐름을 README만 보고 따라갈 수 있어야 한다.

## Non-Goals

- 이번 범위에서 댓글 시스템까지 붙이지 않는다.
- 이번 범위에서 커스텀 도메인까지 연결하지 않는다.
- 이번 범위에서 대규모 디자인 리브랜딩까지 하지 않는다.

## Technical Considerations

- GitHub Pages 호환성을 위해 `github-pages` gem 기준을 유지한다.
- 테마는 `Minimal Mistakes` 원격 테마를 유지한다.
- 품질 체크는 우선 `bundle exec jekyll build`를 기본으로 한다.

## Success Metrics

- 첫 방문자가 블로그 주제를 10초 안에 이해할 수 있다.
- 블로그 운영자가 새 글 초안을 30분 내에 시작할 수 있다.
- 배포 절차를 README만 보고 한 번에 재현할 수 있다.

## Open Questions

- author 소개에 어느 정도까지 개인 경력을 공개할지 아직 정하지 않았다.
- 첫 대표 글 주제를 실험 설계, SQL, MLOps 중 어디로 할지 확정하지 않았다.
