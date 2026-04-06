---
title: "실시간 자동매매 봇 개발기: 전략보다 운영이 더 어려웠다"
type: draft
status: published
created_at: 2026-04-06
updated_at: 2026-04-06
source_count: 1
tags:
  - trading
  - architecture
  - llm
  - backtesting
---

# 질문

`~/open-trading-api`를 블로그에 올린다면, 기능 소개보다 어떤 운영 경험과 구조적 교훈을 중심으로 정리하는 것이 적합할까?

## 결론

- 이번 글의 중심축은 전략 자체보다 운영 안정성이다.
- `run-once`, `run-daemon`, 세션 판별, heartbeat, startup reconciliation, kill switch가 실시간 봇의 핵심 운영면을 이룬다.
- 현재 `src/` 실거래 봇에는 3개 전략이 등록돼 있고, 이 전략들은 수익률 경쟁보다 시간축과 운영 조건의 차이를 드러내는 사례로 읽는 편이 맞다.
- stale quote, 중복 미체결 주문, 자금 부족, 일일 손실 제한, 0수량 주문, 포지션 없는 매도 차단 같은 규칙이 실제 운영형 봇의 품질을 좌우한다.
- DNS, TLS, reconciliation 오탐, 평균단가 파싱 실패 같은 incident를 숨기지 않고 문서와 테스트로 고정한 점이 이 레포의 가장 큰 가치다.

## 근거 페이지

- [open-trading-api](../sources/open-trading-api.md)
- [LLM 친화형 자동매매 작업공간](../topics/llm-friendly-trading-stack.md)

## 후속 액션

- 공개 글을 회고형 구조로 재작성하고, mermaid chart는 실거래 운영 흐름 중심으로 바꾼다.
- 향후 후속 글에서는 전략별 구현 세부, 백테스트 지표 해석, 운영 incident를 개별 글로 분리할 수 있다.
- `strategy_builder`와 `backtester`는 후속 글에서 별도로 다루고, 이번 글은 `src/` 운영면에 집중한다.

## 블로그 글로의 확장 가능성

- 발행 완료: [../../_posts/2026-04-06-open-trading-api-workbench.md](../../_posts/2026-04-06-open-trading-api-workbench.md)
- 후속 글 후보는 백테스트 지표 해석, 실거래 전략 현실화, 장애 복구 설계다.
