---
title: "블로그 위키 인덱스"
type: index
status: active
updated_at: 2026-04-14
tags:
  - wiki
  - index
---

# 블로그 위키 인덱스

이 파일은 위키 전체를 훑는 시작점이다. 새 소스를 ingest 하거나 가치 있는 질의를 파일링할 때마다 함께 갱신한다.

## 운영 페이지

- [[wiki/dashboard|dashboard.md]]: Obsidian에서 source, query, draft 상태를 Dataview로 훑는 동적 진입점이다.
- [[wiki/overview|overview.md]]: 블로그 위키의 범위, 독자, 콘텐츠 축, 발행 원칙을 요약한다.
- [[wiki/log|log.md]]: ingest, query, lint, publish 이력을 시간순으로 기록한다.
- [[docs/technical-post-writing-guide]]: 공개 기술 글 작성의 단일 기준 문서다.
- [[docs/blog-engineering-guide]]: 요약 박스, 본문 폭, figure, notice 같은 게시 형식 기준을 정리한다.

## 소스 페이지

- [[wiki/sources/llm-wiki|sources/llm-wiki.md]]: LLM이 raw 문서 대신 지속적으로 유지되는 중간 위키를 관리한다는 패턴을 요약한다.
- [[wiki/sources/open-trading-api|sources/open-trading-api.md]]: 한국투자증권 Open API 샘플 저장소가 자동매매 작업공간으로 확장된 구조를 요약한다.
- [[wiki/sources/melu-cold-start-recommendation|sources/melu-cold-start-recommendation.md]]: MeLU 논문을 few-shot 콜드스타트 추천 관점에서 요약한다.

## 주제 페이지

- [[wiki/topics/llm-wiki-blogging|topics/llm-wiki-blogging.md]]: 블로그를 누적형 지식 시스템으로 운영하는 구조와 판단 기준을 정리한다.
- [[wiki/topics/llm-friendly-trading-stack|topics/llm-friendly-trading-stack.md]]: API 예제, 전략 설계기, 백테스터, 실거래 봇, 위키를 잇는 자동매매 작업공간 관점을 정리한다.
- [[wiki/topics/few-shot-cold-start-recommendation|topics/few-shot-cold-start-recommendation.md]]: 새 유저 onboarding을 메타러닝 기반 few-shot 적응 문제로 읽는 관점을 정리한다.

## 시리즈 페이지

- 준비 중

## 질의 기록

- [[wiki/queries/2026-04-09-how-melu-serves-a-new-user|queries/2026-04-09-how-melu-serves-a-new-user.md]]: MeLU가 새 유저에게 실제로 어떻게 추천하고 local/global update를 어디에 쓰는지 정리한다.
- [[wiki/queries/2026-04-10-enable-latex-in-jekyll-blog|queries/2026-04-10-enable-latex-in-jekyll-blog.md]]: 블로그 전역에 MathJax를 붙여 `$...$`, `$$...$$` 수식을 렌더링하는 설정 과정과 안전한 inline 수식 작성 규칙을 정리한다.
- [[wiki/queries/2026-04-10-tech-blog-layout-research|queries/2026-04-10-tech-blog-layout-research.md]]: 기술 블로그가 덜 빽빽하게 보이도록 만드는 게시 형식, in-page navigation, 요약 박스, figure, notice box 관행을 외부 사례와 함께 정리한다.
- [[wiki/queries/2026-04-13-obsidian-zotero-research-workflow|queries/2026-04-13-obsidian-zotero-research-workflow.md]]: Zotero와 Obsidian을 논문 연구 워크플로에서 어떻게 나누어 쓰는지, 그리고 이 블로그 LLM 위키에 어떤 세팅이 맞는지 정리한다.

## 발행 후보 초안

- [[wiki/drafts/2026-04-06-rag-instead-grow-a-wiki|drafts/2026-04-06-rag-instead-grow-a-wiki.md]]: 위키형 블로그 운영법을 공개 글로 정리한 발행 초안이다.
- [[wiki/drafts/2026-04-06-open-trading-api-workbench|drafts/2026-04-06-open-trading-api-workbench.md]]: `open-trading-api`를 실시간 자동매매 운영 회고 중심의 블로그 글로 승격한 발행 초안이다.
- [[wiki/drafts/2026-04-09-melu-few-shot-cold-start-recommendation|drafts/2026-04-09-melu-few-shot-cold-start-recommendation.md]]: MeLU 논문을 0-shot이 아닌 few-shot 추천 흐름으로 해설한 발행 초안이다.
