# Implementation Plan: Weekly Tech Digest Agent

## 문서 목적

이 문서는 [spec.md](./spec.md)에서 정의한 주간 최신 기술 다이제스트 기능을 어떤 구조로 구현할지 구체화한다. 구현은 현재 Jekyll 블로그 저장소 안에서 끝나야 하며, 초기 운영 모드는 "주간 초안 PR 생성"을 기본으로 둔다.

## 구현 원칙

- 수집 원천은 공식 RSS, 공식 changelog listing, 공식 GitHub Releases API만 지원한다.
- 수집과 정규화, 필터링은 결정론적 로직으로 처리한다.
- 요약 문장 생성만 LLM을 사용하고, API 키가 없는 환경에서는 추출형 fallback을 허용한다.
- 결과물은 `_posts/` 아래의 Jekyll Markdown 포스트다.
- 자동 실행은 GitHub Actions의 weekly schedule과 manual dispatch를 모두 지원한다.

## 기술 선택

### 런타임

- Python 3.12
- Jekyll build는 기존 Ruby 스크립트 `./scripts/blog-build.sh` 유지

### Python 의존성

- `feedparser`: RSS/Atom 파싱
- `httpx`: HTTP 요청과 타임아웃/재시도 제어
- `beautifulsoup4`: HTML listing 파싱
- `PyYAML`: 소스 설정 로드
- `python-dateutil`: 날짜 문자열 보정
- `unittest`: 표준 라이브러리 기반 핵심 정규화/선별 로직 테스트

### 요약기

- 기본: OpenAI Responses API
- 모델 기본값: `gpt-5.4-mini`
- 인증: `OPENAI_API_KEY`
- 설정 가능 환경 변수:
  - `OPENAI_MODEL`
  - `WEEKLY_TECH_SUMMARY_MODE`
- fallback: API 키가 없거나 호출이 실패하면 추출형 요약 사용 가능

## 디렉터리 구조

```text
specs/001-weekly-tech-digest-agent/
  spec.md
  plan.md
  tasks.md
docs/
  weekly-tech-digest-agent.md
  weekly-tech-digest-workflow.md
scripts/
  weekly-tech/
    requirements.txt
    models.py
    config_loader.py
    collector.py
    summarizer.py
    renderer.py
    generate_digest.py
data/
  weekly-tech/
    sources.yml
    output/
.github/workflows/
  weekly-tech-digest.yml
tests/
  weekly-tech/
```

## 파일별 책임

### `scripts/weekly-tech/models.py`

- 설정, 수집 항목, 후보 항목, 실행 결과를 dataclass로 정의한다.
- 정규화 후 다른 모듈이 공유하는 공통 스키마를 한곳에 둔다.

### `scripts/weekly-tech/config_loader.py`

- `sources.yml`을 읽고 SourceProfile 목록과 전역 설정을 반환한다.
- 설정 누락, 잘못된 source type, quota 누락 같은 입력 오류를 초기에 막는다.

### `scripts/weekly-tech/collector.py`

- RSS/Atom, GitHub Releases API, HTML listing 수집기를 제공한다.
- 수집 결과를 `CollectedEntry`로 정규화한다.
- 중복 제거, include/exclude 규칙, 점수 계산, quota 적용을 담당한다.

### `scripts/weekly-tech/summarizer.py`

- 선택된 후보를 한국어 다이제스트 문단으로 변환한다.
- OpenAI Responses API 연동과 extractive fallback을 모두 가진다.

### `scripts/weekly-tech/renderer.py`

- front matter와 본문 Markdown을 렌더링한다.
- 출력 파일 경로와 slug를 계산한다.

### `scripts/weekly-tech/generate_digest.py`

- CLI 엔트리포인트다.
- 전체 파이프라인 실행, 결과 파일 저장, run metadata 작성, 표준 출력 요약을 담당한다.

### `data/weekly-tech/sources.yml`

- 수집 대상 소스와 quota, include/exclude 규칙, 기본 태그를 관리한다.

### `.github/workflows/weekly-tech-digest.yml`

- 매주 월요일 09:00 KST에 실행한다.
- 수집, 글 생성, Jekyll build, artifact 업로드, PR 생성을 순서대로 수행한다.

## `sources.yml` 스키마

```yaml
global:
  timezone: "Asia/Seoul"
  lookback_days: 7
  max_items: 10
  min_items: 6
  max_items_per_source: 2
  summary_mode: "auto"
  post:
    category: "weekly"
    tags: ["weekly-digest", "it-trends", "automation"]
    slug_prefix: "weekly-tech-roundup"
  category_quotas:
    ai_platform: 2
    web_runtime: 2
    cloud_devtools: 3
    oss_release: 3
  include_keywords:
    - "release"
    - "changelog"
    - "general availability"
    - "preview"
    - "beta"
    - "deprecation"
    - "breaking"
    - "security"
    - "api"
    - "sdk"
  exclude_keywords:
    - "webinar"
    - "event"
    - "meetup"
    - "conference"
    - "hiring"
    - "customer story"
    - "case study"

sources:
  - id: "github_changelog"
    name: "GitHub Changelog"
    source_type: "rss"
    source_kind: "changelog"
    category: "cloud_devtools"
    url: "https://github.blog/changelog/feed/"
    enabled: true
    weight: 1.2

  - id: "react_releases"
    name: "React Releases"
    source_type: "github_releases"
    source_kind: "release_api"
    category: "oss_release"
    repo: "facebook/react"
    enabled: true
    weight: 1.3

  - id: "anthropic_news"
    name: "Anthropic News"
    source_type: "html_listing"
    source_kind: "blog"
    category: "ai_platform"
    url: "https://www.anthropic.com/news"
    item_selector: "a[href^='/news/']"
    title_selector: null
    date_selector: null
    link_prefix: "https://www.anthropic.com"
    enabled: true
    weight: 1.0
```

## 점수 및 선별 규칙

### 1. 초기 필터

- lookback 범위 밖 항목 제외
- exclude keyword 포함 시 제외
- 제목과 설명 모두 너무 짧은 경우 제외

### 2. 점수 계산

- source kind 가중치
  - release_api: +5
  - changelog: +4
  - blog: +2
- recency bonus
  - 최근 48시간: +3
  - 최근 4일: +2
  - 최근 7일: +1
- keyword bonus
  - security / breaking / deprecation: +3
  - release / launch / availability: +2
  - api / sdk / model: +1
- source weight
  - `sources.yml`의 `weight`

### 3. quota 적용

- 카테고리별 quota만큼 우선 선발
- quota 이후 남는 자리는 전체 점수순으로 채운다
- 최종 항목 수는 `min_items <= N <= max_items` 범위에서 결정한다

## 요약 전략

### OpenAI 요약

- 입력: 선정된 후보의 title, source, published_at, summary_text, raw_url
- 출력:
  - `overview`
  - 항목별 `what_changed`
  - 항목별 `why_it_matters`
  - 항목별 `practical_impact`
- 실패 시 전체 파이프라인을 즉시 종료하지 않고 fallback 가능 여부를 본다.

### Extractive fallback

- 제목과 원문 summary의 첫 1~2문장을 정리한다.
- "왜 중요한가", "실무 영향"은 카테고리와 키워드 기반 템플릿으로 생성한다.
- 품질은 낮지만 PR 검토용 초안으로는 충분해야 한다.

## Markdown 렌더링 규칙

- 파일명: `_posts/YYYY-MM-DD-weekly-tech-roundup.md`
- front matter 필수 필드:
  - `title`
  - `date`
  - `categories`
  - `tags`
  - `excerpt`
- 본문 구성:
  - 도입 요약
  - 수집 기간과 선정 기준
  - 카테고리별 섹션
  - 항목별 원문 링크
  - 마무리 문단

## GitHub Actions 설계

### Trigger

- `schedule`: `0 0 * * 1`
  - 월요일 00:00 UTC
  - 월요일 09:00 KST
- `workflow_dispatch`

### Job 흐름

1. Checkout
2. Set up Python
3. Install Python deps
4. Generate weekly digest
5. Run `./scripts/blog-build.sh`
6. Upload run metadata artifact
7. Create PR if a new post was created

### Secrets / Env

- 선택적:
  - `OPENAI_API_KEY`
  - `OPENAI_MODEL`
- 기본:
  - `GITHUB_TOKEN`

## 검증 계획

- 단위 테스트:
  - 중복 제거 규칙
  - quota 적용
  - Markdown 파일명과 front matter 생성
- 통합 검증:
  - 실제 소스 15개 이상 수집
  - `_posts/` 파일 생성
  - `./scripts/blog-build.sh` 통과

## 리스크와 대응

- 일부 소스의 HTML 구조 변경:
  - HTML listing은 필수 소스가 아니라 보조 소스로 둔다.
- OpenAI API 키 미설정:
  - extractive fallback으로 PR 초안은 유지한다.
- 릴리즈 패치 버전만 과도하게 선택되는 문제:
  - quota 이후 점수와 제목 패턴으로 중요도 균형을 맞춘다.
- 주간 글 품질 저하:
  - direct publish 대신 PR 검토 모드를 유지한다.
