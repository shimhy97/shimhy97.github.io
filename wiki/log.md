---
title: "블로그 위키 로그"
type: log
status: active
updated_at: 2026-04-13
tags:
  - wiki
  - log
---

# 블로그 위키 로그

위키의 변화 이력을 시간순으로 남긴다. 항목 헤더는 `## [YYYY-MM-DD] action | 제목` 형식을 유지한다.

## [2026-04-06] bootstrap | 블로그 위키 구조 초기화

- `AGENTS.md`에 블로그용 LLM 위키 스키마를 정의했다.
- `raw/`와 `wiki/` 계층을 추가하고, 인덱스와 로그 파일을 만들었다.
- 공개 블로그와 내부 운영 자료를 분리하기 위해 Jekyll 제외 대상을 정리했다.

## [2026-04-06] ingest | LLM Wiki

- `docs/llm-wiki-ENG.md`를 읽고 `wiki/sources/llm-wiki.md`에 소스 요약을 만들었다.
- `wiki/topics/llm-wiki-blogging.md`에 블로그 운영 주제를 연결했다.
- `wiki/drafts/2026-04-06-rag-instead-grow-a-wiki.md`에 공개 글 후보 논지를 정리했다.

## [2026-04-06] publish | RAG 대신 위키를 키우는 블로그 운영법

- 위키 초안을 바탕으로 `_posts/2026-04-06-build-your-blog-as-an-llm-wiki.md`를 작성했다.
- `wiki/index.md`를 갱신해 새 소스, 주제, 초안을 인덱스에 반영했다.
- 원문, 위키, 공개 글의 3계층 운영 흐름을 이번 주 게시글 주제로 고정했다.

## [2026-04-06] revise | 원본 llm-wiki gist 소개를 반영해 글 재구성

- 게시글 앞부분에 Andrej Karpathy의 `llm-wiki` gist가 어떤 문서인지와 핵심 제안을 먼저 소개했다.
- 이후 문단에서 이 저장소의 `raw/`, `wiki/`, `_posts/`, `AGENTS.md` 구조로 어떻게 번역했는지 연결하도록 흐름을 다시 짰다.
- `wiki/sources/llm-wiki.md`와 `wiki/drafts/2026-04-06-rag-instead-grow-a-wiki.md`도 같은 관점으로 요약을 수정했다.

## [2026-04-06] ingest | open-trading-api

- 외부 소스 저장소 `https://github.com/koreainvestment/open-trading-api`와 로컬 경로 `/Users/shimhy97/open-trading-api`를 기준으로 `README.md`, `strategy_builder/README.md`, `backtester/README.md`, `SPEC_v0.1.md`, `docs/implemented-trading-strategies.md`를 읽었다.
- `wiki/sources/open-trading-api.md`에 저장소 구조와 핵심 계약을 요약했다.
- `wiki/topics/llm-friendly-trading-stack.md`와 `wiki/drafts/2026-04-06-open-trading-api-workbench.md`를 추가해 블로그 발행 관점을 정리했다.
- `wiki/overview.md`의 콘텐츠 축에 자동매매 시스템 설계와 운영을 보강했다.

## [2026-04-06] publish | 샘플 코드 저장소를 자동매매 워크벤치로 키운 open-trading-api

- `_posts/2026-04-06-open-trading-api-workbench.md`를 작성해 외부 레포 개발 내용을 구조와 계약 중심의 블로그 글로 승격했다.
- 글 중간에 `examples_llm`, `strategy_builder`, `.kis.yaml`, `backtester`, `src`, `docs/kb` 관계를 보여 주는 mermaid chart를 넣었다.
- 사이트에서 mermaid 코드 블록이 실제 다이어그램으로 렌더링되도록 `_includes/head/custom.html`을 추가했다.

## [2026-04-06] revise | 운영 회고형 목차에 맞춰 open-trading-api 글 재작성

- 게시글 제목을 `실시간 자동매매 봇 개발기: 전략보다 운영이 더 어려웠다`로 바꾸고, 구조 소개형 글을 운영 회고형 글로 다시 썼다.
- 사용자 제안 목차에 맞춰 `왜 만들었는가`, `실시간 봇은 어떻게 돌아가는가`, `리스크 관리`, `장애와 대응`, `테스트와 검증`, `배운 점` 중심으로 흐름을 재구성했다.
- 초안 작성용 서브에이전트 2개의 제안을 비교해, 공통으로 강조된 운영 안정성과 incident 기반 학습 포인트를 최종 원고에 반영했다.

## [2026-04-08] revise | 기술 글 작성 가이드를 단일 문서로 통합

- `docs/weekly-tech-roundup-writing-guide.md`를 삭제하고 `docs/technical-post-writing-guide.md`를 공개 기술 글의 단일 기준 문서로 남겼다.
- 주간 다이제스트 관련 workflow와 운영 문서에서 삭제된 문서 참조를 걷어내고, 공통 기술 글 가이드만 가리키도록 정리했다.
- `wiki/index.md`와 `wiki/overview.md`를 갱신해 위키에서도 단일 작성 기준을 바로 찾을 수 있게 했다.

## [2026-04-08] revise | llm-wiki 글을 새 기술 글 형식으로 재작성

- `_posts/2026-04-06-build-your-blog-as-an-llm-wiki.md`를 처음부터 다시 써서, `llm-wiki`의 철학과 이 저장소 적용 방식을 기사형 구조로 재구성했다.
- 외부 원문 출처를 본문 각주와 `## 출처` 섹션으로 정리하고, `raw -> wiki -> _posts` 경계와 `AGENTS.md`의 schema 역할을 더 분명히 설명했다.
- `wiki/drafts/2026-04-06-rag-instead-grow-a-wiki.md`도 새 원고 구조에 맞는 초안 메모로 갱신했다.

## [2026-04-08] revise | open-trading-api 글을 운영 루프 중심으로 재작성

- `_posts/2026-04-06-open-trading-api-workbench.md`를 처음부터 다시 써서, 전략 소개보다 시간축, 주문 차단, incident, Ralph와 위키 기반 구현 루프를 중심으로 재구성했다.
- `strategy_builder`, `backtester`, `src`, `kb`, `scripts/ralph`가 함께 움직이는 작업공간 관점을 앞세우고, 실거래 3개 전략과 프리셋 10개 전략의 경계를 분명히 적었다.
- `wiki/drafts/2026-04-06-open-trading-api-workbench.md`도 새 원고 구조에 맞게 중심 문장과 섹션 메모를 갱신했다.

## [2026-04-08] revise | 약어와 개발 식별자 설명 규칙 추가

- `docs/technical-post-writing-guide.md`에 약어, 클래스명, 전략 ID, 설정 키를 처음 등장할 때 풀어쓴 이름과 역할로 설명하는 규칙을 추가했다.
- `_posts/2026-04-06-open-trading-api-workbench.md`에서 ORB, RVOL, ADX, VWAP, ATR, `sma_cross_5m`, `RiskEngine` 같은 표현의 첫 등장을 풀어 쓴 이름과 함께 정리했다.
- `wiki/drafts/2026-04-06-open-trading-api-workbench.md`도 같은 기준을 반영해 초안 메모를 보강했다.

## [2026-04-09] ingest | MeLU 논문

- `docs/`에 있던 `MeLU` 논문 PDF를 `raw/sources/papers/2019-lee-melu-cold-start-recommendation.pdf`로 옮겨 원천 소스 계층에 고정했다.
- `wiki/sources/melu-cold-start-recommendation.md`를 추가해 논문 요약, 서비스 관점 핵심 포인트, 후속 조사 지점을 정리했다.
- `wiki/topics/few-shot-cold-start-recommendation.md`, `wiki/queries/2026-04-09-how-melu-serves-a-new-user.md`, `wiki/drafts/2026-04-09-melu-few-shot-cold-start-recommendation.md`를 만들어 질의응답과 발행 관점을 위키 자산으로 남겼다.

## [2026-04-09] publish | MeLU를 다시 읽기: 콜드스타트 추천은 0-shot이 아니라 몇 개 반응 뒤에 시작돼요

- `_posts/2026-04-09-melu-few-shot-cold-start-recommendation.md`를 작성해 MeLU를 0-shot 추천기가 아니라 few-shot 개인화 모델로 읽는 해설 글로 발행했다.
- 글에서는 evidence candidate selection, 임베딩 고정과 head 적응, support/query 분리, local/global update 구분을 중심 설명 축으로 재구성했다.
- `wiki/index.md`와 `wiki/log.md`를 갱신해 새 소스, 주제, 질의 기록, 발행 초안을 인덱스에 반영했다.

## [2026-04-10] revise | 블로그 전역 LaTeX 렌더링 설정 추가

- `_includes/head/custom.html`에 MathJax 3 설정과 CDN 스크립트를 추가해 `$...$`, `$$...$$`, `\(...\)`, `\[...\]` 수식을 렌더링하도록 설정했다.
- 코드 블록 안 수식 문자열이 잘못 처리되지 않도록 `skipHtmlTags`에 `pre`, `code`를 포함했다.
- `wiki/queries/2026-04-10-enable-latex-in-jekyll-blog.md`에 설정 과정, 사용 규칙, 검증 상태를 남겼다.

## [2026-04-10] revise | MeLU 논문 글을 실제 MathJax 문법으로 전환

- `_posts/2026-04-09-melu-few-shot-cold-start-recommendation.md`의 핵심 수식 구간을 `text` 코드 블록 대신 실제 `$...$`, `$$...$$` 문법으로 바꿨다.
- inline 수식과 display 수식을 함께 사용해 유저/아이템 임베딩, 예측식, local update 식이 글 안에서 자연스럽게 읽히도록 정리했다.
- `support set`, `query set`, `local update`, `global update` 차이는 표와 수식 설명이 이어지도록 본문 흐름을 다듬었다.

## [2026-04-10] verify | rbenv Ruby 3.2.4로 MathJax 렌더링 빌드 확인

- 시스템 기본 Ruby 2.6에서는 `bundler 4.0.9` 설치가 맞지 않았지만, 레포의 `.ruby-version`을 따르는 `rbenv` Ruby 3.2.4 환경에는 `bundler 4.0.9`가 이미 준비돼 있음을 확인했다.
- `rbenv exec bundle exec jekyll doctor`가 통과했고, `rbenv exec bundle exec jekyll build`도 성공했다.
- 생성된 `_site/machine-learning/recommender-systems/melu-few-shot-cold-start-recommendation/index.html`에서 MathJax 스크립트와 수식 마크업이 함께 출력되는 것을 확인해 블로그 렌더링 경로를 검증했다.

## [2026-04-10] revise | LaTeX 안전 사용 규칙을 단일 가이드와 위키에 명시

- `docs/technical-post-writing-guide.md`에 MathJax 기준 블록 수식과 inline 수식 작성 규칙을 추가했다.
- inline `$...$` 안의 첨자 `_`가 Kramdown과 충돌할 수 있으므로, 복잡한 inline 수식은 `<span markdown="0">\(...\)</span>` 패턴을 기본으로 쓰도록 명시했다.
- `wiki/queries/2026-04-10-enable-latex-in-jekyll-blog.md`에도 같은 주의사항과 자주 깨지는 실수 예시를 남겨, 이후 LaTeX를 쓸 때 바로 참조할 수 있게 했다.

## [2026-04-10] query | 기술 블로그 게시 형식 조사

- 외부 엔지니어링 블로그 사례를 읽고, 긴 글을 덜 빽빽하게 보이게 만드는 요약 박스, in-page navigation, figure, notice, 메타데이터 노출 패턴을 `wiki/queries/2026-04-10-tech-blog-layout-research.md`에 정리했다.
- GitHub, Vercel, Cloudflare, Stripe, Thoughtworks / Martin Fowler, Atlassian, USWDS, Microsoft Design 자료를 함께 보며 글쓰기와 게시 UI가 분리되어 설계되는 관행을 메모했다.
- 현재 레포의 `_config.yml` 기본값 `classes: wide`, `toc`, `toc_sticky`와 `assets/css/main.scss`의 `notice--primary` 상태도 같이 기록해, 바로 적용 가능한 개선 레버를 남겼다.

## [2026-04-10] revise | 블로그 엔지니어링 규약 추가와 llm-wiki 글 재편집

- `docs/blog-engineering-guide.md`를 추가해 요약 박스, 본문 폭, 시각적 멈춤점, figure caption, notice 사용 규칙을 이 저장소 기준으로 고정했다.
- `AGENTS.md`와 `docs/technical-post-writing-guide.md`를 갱신해 글쓰기 규약과 게시 형식 규약을 함께 따르도록 정리했다.
- `_posts/2026-04-06-build-your-blog-as-an-llm-wiki.md`를 새 규약에 맞춰 요약 박스, 비교 표, mermaid 다이어그램, 더 짧은 섹션 리듬을 갖는 글로 다시 썼다.

## [2026-04-13] query | Obsidian + Zotero 연구 워크플로 조사

- Zotero와 Obsidian을 논문 읽기 워크플로에서 어떻게 나누어 쓰는지 공식 문서와 커뮤니티 사례를 바탕으로 `wiki/queries/2026-04-13-obsidian-zotero-research-workflow.md`에 정리했다.
- Zotero Integration용 source note 템플릿 `wiki/_templates/zotero-paper-import.md`와 permanent note 템플릿 `wiki/_templates/obsidian-permanent-note.md`를 추가했다.
- 이 repo를 Obsidian vault로 실험할 때 자주 바뀌는 `.obsidian/workspace*.json`이 git diff를 오염시키지 않도록 `.gitignore`를 보강했다.
