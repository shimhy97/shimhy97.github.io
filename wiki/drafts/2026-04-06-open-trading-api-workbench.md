---
title: "자동매매 봇 개발에서 배운 건 전략보다 경계였어요"
type: draft
status: published
created_at: 2026-04-06
updated_at: 2026-04-20
source_count: 1
tags:
  - trading
  - architecture
  - llm
  - backtesting
  - wiki
---

# 중심 문장

- `open-trading-api` 개발에서 가장 오래 남은 배움은 전략 공식이 아니라, 예제와 실거래, 설계와 검증, 신호와 주문, 기억과 기록의 경계를 계속 고정하는 일이었다.

## 오프닝 메모

이번 재작성은 기존 공개 글의 운영 로직 설명을 확장하지 않고, `wiki/sources/open-trading-api`와 `wiki/topics/llm-friendly-trading-stack`에서 정리한 작업공간 관점을 블로그 회고로 다시 번역한다. 글의 독자는 특정 전략 구현보다 "자동매매 시스템을 만들며 어떤 설계 감각을 얻었는가"를 기대한다고 보고, 구체 로직은 최소화한다.

## 섹션 구조

### 작업공간은 경계를 드러낼 때 쓸모 있어요

- `examples`, `strategy_builder`, `.kis.yaml`, `backtester`, `src`, `wiki/kb`를 한 흐름으로 보되, 각 층의 책임이 다르다는 점을 먼저 말한다.
- Mermaid 다이어그램으로 전략 아이디어가 설계, 검증, 운영, 기록으로 이동하는 경로를 보여 준다.

### 공통 계약은 번역 비용을 줄였어요

- `.kis.yaml`을 전략 설계 UI와 백테스터 사이의 중간 계약으로 설명한다.
- 단일 계약이 실거래 런타임까지 어디까지 확장될 수 있는지는 열린 질문으로 남긴다.

### 구현보다 먼저 물어야 할 질문이 있었어요

- "어떤 전략이 수익을 내는가"보다 "무엇이 데모이고 무엇이 운영인가", "어떤 상태를 신뢰할 수 있는가"를 먼저 물어야 했다는 배움으로 쓴다.
- 예제, 전략 설계, 백테스트, 실거래 런타임, 위키/로그의 역할 차이를 표로 정리한다.

### 위키는 기억보다 판단을 남겼어요

- `wiki/sources/open-trading-api`, `wiki/topics/llm-friendly-trading-stack`, `wiki/log`가 개발 사실보다 판단의 이유를 남기는 역할을 한다고 설명한다.
- 운영 판단이 다음 구현에서 다시 읽히려면 채팅이 아니라 파일로 남아야 한다는 관점으로 정리한다.

### LLM 친화성은 다시 읽힘에서 나왔어요

- LLM 친화성은 생성 속도가 아니라 폴더, 설정, 문서, 위키가 안정적으로 연결된 구조에서 나온다고 설명한다.
- `examples_llm`, `examples_user`, `SPEC_v0.1.md`, `AGENTS.md`는 다음 구현자가 같은 경계를 따라가게 하는 장치로 다룬다.

### 다음 과제는 경계의 수렴이에요

- `.kis.yaml`의 실거래 런타임 확장 가능성, 백테스트 프리셋과 운영 전략 목록의 정책, 운영 상태의 문서 반영 자동화를 다음 관찰 지점으로 남긴다.

## 근거 페이지

- [[wiki/sources/open-trading-api|open-trading-api]]
- [[wiki/topics/llm-friendly-trading-stack|LLM 친화형 자동매매 작업공간]]
- [[wiki/log|블로그 위키 로그]]

## 발행 결과

- 게시글: [../../_posts/2026-04-06-open-trading-api-workbench.md](../../_posts/2026-04-06-open-trading-api-workbench.md)
