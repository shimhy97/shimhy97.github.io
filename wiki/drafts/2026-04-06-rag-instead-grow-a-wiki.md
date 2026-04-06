---
title: "RAG 대신 위키를 키우는 블로그 운영법"
type: draft
status: published
created_at: 2026-04-06
updated_at: 2026-04-06
source_count: 1
tags:
  - llm
  - wiki
  - blog
  - knowledge-management
---

# 질문

블로그를 일회성 글 묶음이 아니라 LLM이 관리하는 누적형 지식 시스템으로 운영하려면 어떤 구조가 필요한가?

## 결론

- 핵심은 LLM을 검색 도우미가 아니라 위키 유지보수 담당자로 배치하는 것이다.
- `raw/`에는 원문을 보존하고, `wiki/`에는 해석과 연결을 축적하고, `_posts/`에는 최종 글만 발행한다.
- 질문 응답, 비교 메모, 시리즈 관점도 위키로 환원할 때 이후 게시글 품질과 속도가 함께 좋아진다.

## 근거 페이지

- [LLM Wiki](../sources/llm-wiki.md)
- [LLM 위키형 블로그 운영](../topics/llm-wiki-blogging.md)

## 후속 액션

- 주간 발행 전, 관련 소스를 먼저 `wiki/sources/`에 요약한다.
- 반복되는 질문은 `wiki/queries/`에 남겨 차기 글의 재료로 삼는다.
- 발행 후에는 공개 글 링크와 배운 점을 로그에 남긴다.

## 블로그 글로의 확장 가능성

- 발행 완료: [../../_posts/2026-04-06-build-your-blog-as-an-llm-wiki.md](../../_posts/2026-04-06-build-your-blog-as-an-llm-wiki.md)
- 후속 글에서는 실제 ingest 루틴과 lint 체크리스트를 사례 중심으로 풀 수 있다.
