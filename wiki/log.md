---
title: "블로그 위키 로그"
type: log
status: active
updated_at: 2026-04-08
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
