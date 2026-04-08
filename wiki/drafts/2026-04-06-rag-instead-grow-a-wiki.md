---
title: "카파시의 llm-wiki를 블로그 운영 규칙으로 옮기기"
type: draft
status: published
created_at: 2026-04-06
updated_at: 2026-04-08
source_count: 1
tags:
  - llm
  - wiki
  - blog
  - knowledge-management
---

# 중심 문장

- `llm-wiki`의 핵심은 RAG를 더 잘 쓰는 법이 아니라, raw와 공개 글 사이에 LLM이 유지하는 wiki를 두어 맥락 복구 비용을 줄이는 운영 패턴이라는 점이다.

## 오프닝 메모

Andrej Karpathy의 `llm-wiki` gist는 완성된 제품 소개보다, LLM을 지식 유지보수 담당자로 배치하는 추상 설계 문서에 가깝다. 블로그 관점에서 다시 읽으면 중요한 포인트는 검색 정확도가 아니라, 조사 과정이 다음 글에 다시 쓰일 수 있게 남는 구조를 만드는 일이다.

## 섹션 구조

### RAG로는 맥락이 남지 않아요

- 문서 기반 LLM 활용이 왜 매번 다시 조립되는 답변에 머무르기 쉬운지 설명한다.
- `_posts/`만 쌓이는 블로그 운영이 왜 조사 맥락을 잃기 쉬운지 연결한다.

### 위키를 중간 계층으로 세워요

- `persistent wiki`와 사람/LLM 역할 분담이 원문의 중심이라는 점을 앞쪽에서 분명히 둔다.
- Obsidian 같은 도구 예시는 주변부로 두고, 운영 철학을 먼저 설명한다.

### 이 저장소에선 이렇게 번역했어요

- `raw/`, `wiki/`, `_posts/`, `AGENTS.md`를 나란히 보여 주고 각 계층의 책임을 설명한다.
- 디렉터리 이름보다 원문, 해석, 공개 결과를 섞지 않는 경계를 강조한다.

### 블로그와 위키의 역할을 갈라놔요

- `wiki/drafts/`와 `wiki/queries/`를 강조해 발행 전 사고의 중간층을 설명한다.
- `index.md`와 `log.md`가 검색과 이력 관리에서 왜 필요한지 연결한다.

### 먼저 고정할 운영 루틴이 있어요

- `raw/inbox` -> `wiki/sources` -> `wiki/topics`/`wiki/drafts` -> `wiki/index`/`wiki/log` -> `_posts/` 순서를 구체 단계로 적는다.
- 거대한 도구 체인보다 작은 위키 습관을 먼저 고정하자는 문장으로 마무리한다.

## 근거 페이지

- [LLM Wiki](../sources/llm-wiki.md)
- [LLM 위키형 블로그 운영](../topics/llm-wiki-blogging.md)

## 발행 결과

- 게시글: [../../_posts/2026-04-06-build-your-blog-as-an-llm-wiki.md](../../_posts/2026-04-06-build-your-blog-as-an-llm-wiki.md)
- 후속 글 후보: ingest 루틴 실험기, `wiki/queries/` 운영 기준, `index.md`와 `log.md` 유지 전략
