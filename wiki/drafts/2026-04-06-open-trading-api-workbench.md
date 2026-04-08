---
title: "자동매매 봇 개발기: 전략보다 운영 루프를 먼저 고치게 됐어요"
type: draft
status: published
created_at: 2026-04-06
updated_at: 2026-04-08
source_count: 1
tags:
  - trading
  - architecture
  - llm
  - backtesting
  - wiki
  - ralph
---

# 중심 문장

- `open-trading-api`를 직접 구현하고 운영해보니, 전략 공식을 설명하는 글보다 시간축, 주문 차단, 재기동 복구, incident 기록, Ralph와 위키 기반 구현 루프를 함께 보여주는 글이 더 이 저장소의 성격에 가깝다.

## 오프닝 메모

자동매매 봇 글이라고 해서 전략 소개부터 길게 풀기보다, 이 저장소가 왜 샘플 코드 모음이 아니라 작업공간처럼 보이게 됐는지부터 설명하는 편이 맞다. `strategy_builder`, `backtester`, `src`, `kb`, `scripts/ralph`가 함께 돌아가고, 실제 운영에서 부딪힌 incident가 테스트와 문서로 되돌아오는 흐름이 이 레포의 더 큰 특징이다. 약어와 내부 식별자는 첫 등장 때 풀어쓴 이름과 역할을 같이 적는다.

## 섹션 구조

### 샘플 저장소가 작업공간으로 커졌어요

- `examples_llm`, `examples_user`, `strategy_builder`, `backtester`, `src`, `kb`, `scripts/ralph`가 왜 하나의 작업 체계로 읽히는지 설명한다.
- 10개 프리셋 전략과 실제 실거래 3개 전략의 차이를 초반에 분명히 둔다.

### 알고리즘보다 시간축이 더 까다로웠어요

- 시가 구간 돌파 전략(Opening Range Breakout, ORB)인 `opening_range_breakout_1m`, 5분 이동평균 교차 전략인 `sma_cross_5m`, 일봉 RSI 평균회귀 전략인 `rsi_mean_reversion_d1`의 현재 구현 경계를 설명한다.
- ORB 세션 재생, 상대거래량(Relative Volume, RVOL), 미완성 일봉 제외처럼 시간과 상태가 더 어려웠던 지점을 적는다.

### 주문은 신호보다 차단 로직에서 흔들렸어요

- 리스크 엔진 `RiskEngine`과 주문 실행 엔진 `ExecutionEngine`이 실제 운영에서 더 자주 문제를 드러낸다는 흐름으로 쓴다.
- 0수량 주문, 매도(`SELL`) 수량 계산, stale quote, 정규장 상태인 `MarketStatus.NORMAL`, open order 중복 차단을 구체 예시로 넣는다.

### incident를 남기니 테스트가 달라졌어요

- `kb/wiki/queries/`에 남은 0수량, warmup, reconciliation, TLS 관련 incident를 묶어 설명한다.
- 문제를 숨기지 않고 문서 + 회귀 테스트로 고정하는 저장소라는 인상을 주는 방향으로 정리한다.

### Ralph와 위키가 구현 방식을 바꿨어요

- `scripts/ralph/prd.json`, `progress.txt`, `CLAUDE.md`, `kb/`를 함께 설명한다.
- "코드를 한 번 생성하는 LLM"이 아니라 "반복 구현 루프를 유지하는 LLM"이라는 관점으로 정리한다.

## 근거 페이지

- [open-trading-api](../sources/open-trading-api.md)
- [LLM 친화형 자동매매 작업공간](../topics/llm-friendly-trading-stack.md)

## 발행 결과

- 게시글: [../../_posts/2026-04-06-open-trading-api-workbench.md](../../_posts/2026-04-06-open-trading-api-workbench.md)
- 후속 글 후보: active watchlist 자동 스캐너, startup reconciliation 설계, Ralph 기반 반복 구현 루프
