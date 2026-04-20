---
title: "open-trading-api 실거래 봇 개발 회고"
type: source
status: active
source_kind: repository-wiki
source_path: "/Users/shimhy97/open-trading-api/kb"
source_url: "https://github.com/koreainvestment/open-trading-api"
ingested_at: 2026-04-06
updated_at: 2026-04-20
tags:
  - trading-bot
  - kis-open-api
  - engineering-retrospective
  - operations
  - wiki
---

# 소스 요약

## 한 줄 요약

- `open-trading-api` 개발에서 가장 크게 남은 배움은 자동매매의 어려움이 전략 공식보다 `시간`, `데이터`, `주문`, `로컬 상태`의 경계를 실시간으로 맞추는 일에 있다는 점이다.

## 참조한 로컬 위키와 문서

- `/Users/shimhy97/open-trading-api/kb/index.md`: 현재 지식 베이스의 카탈로그와 질의 기록 목록
- `/Users/shimhy97/open-trading-api/kb/log.md`: 2026-04-06부터 2026-04-14까지 이어진 incident, 구현, 문서 동기화 이력
- `/Users/shimhy97/open-trading-api/kb/wiki/systems/open-trading-api-repo-map.md`: 샘플 코드, 실거래 런타임, 전략 빌더, 백테스터, 운영 문서의 역할 분리
- `/Users/shimhy97/open-trading-api/docs/trading-bot.md`: 현재 봇의 실행 흐름, 전략 구성, watchlist/scanner, 리스크와 복구 경계
- `/Users/shimhy97/open-trading-api/docs/implemented-trading-strategies.md`: `sma_cross_5m`, `rsi_mean_reversion_d1`, `opening_range_breakout_1m`의 현재 코드 기준 동작
- `/Users/shimhy97/open-trading-api/kb/wiki/queries/*.md`: 0수량 주문, SMA warmup, sparse intraday, ORB 세션 경계, RVOL baseline, stale open order 같은 운영 질의 기록

## 핵심 내용

- 원래 저장소는 한국투자증권 Open API 샘플 코드와 LLM 친화적 예제 구조에서 출발하지만, 로컬 개발 과정에서는 `src/` 기반 실거래 봇, `strategy_builder/`, `backtester/`, `specs/`, `kb/`가 붙어 자동매매 작업공간으로 커졌다.
- 실거래 봇은 KIS 인증, quote, intraday bar, balance, 주문 제출, SQLite 기반 주문/시그널/상태 기록, daemon loop, kill switch, startup/cycle reconciliation을 포함한다.
- 전략은 세 갈래다. `opening_range_breakout_1m`은 이름과 달리 현재 5분 ORB 중심이고, `sma_cross_5m`는 ADX, RVOL at Time, VWAP, ATR stop을 결합한 장중 추세 전략이며, `rsi_mean_reversion_d1`은 확정 일봉 기반 평균회귀 성격이 강하다.
- 장전 scanner와 active watchlist는 "많이 평가하면 더 좋다"가 아니라 "평가할 종목을 줄여야 실시간 시스템이 된다"는 방향으로 설계됐다.
- 위키에는 실제 운영 중 드러난 작은 사고들이 쌓여 있다. 0수량 주문은 시스템 오류가 아니라 리스크 한도 차단이었고, sparse intraday는 데이터 결측이 아니라 브로커가 거래가 있었던 분만 주는 현실에 가까웠고, stale open order는 장중 청산을 막는 로컬 상태 불일치였다.

## 블로그에 중요한 포인트

### 전략보다 경계가 먼저였다

- 처음에는 어떤 전략이 더 잘 벌 수 있는지가 중심 질문처럼 보인다.
- 하지만 실제 개발에서는 `MarketStatus.NORMAL`, 이전 정규장 warmup, same-day current-session cache, ORB session replay, `require_flat_before_switch` 같은 경계가 더 자주 문제를 만들었다.
- 자동매매에서 "언제부터 언제까지의 데이터인가", "이 주문은 어느 전략이 소유하는가", "이 봉은 당일 세션인가 전일 tail인가"를 코드와 로그가 설명하지 못하면 전략 성능 논의로 넘어갈 수 없다.

### 데이터는 완전한 시계열로 오지 않았다

- KIS historical intraday는 종목마다 1분봉 밀도가 크게 다를 수 있고, 어떤 종목은 특정 5분 버킷에 1분봉이 1~2개만 존재했다.
- 이 때문에 `raw_bars`가 충분해도 `aggregated_bars`가 부족해지는 일이 생겼고, `sma_cross_5m`에서는 `0-volume clock minute` 보정을 통해 5분봉의 의미를 "거래가 있던 분 5개"가 아니라 "시장 시계 기준으로 닫히는 구간"으로 다시 정의했다.
- 이 경험은 모델링보다 데이터 계약이 먼저라는 사실을 보여 준다.

### 주문하지 않는 것도 기능이었다

- 2026-04-06의 0수량 주문은 계좌 잔고와 가격, 비중 한도가 만나 1주도 만들 수 없는 상태였다.
- 이 케이스는 실패가 아니라 정상 차단이어야 했고, `ZeroQuantityOrderError`, warning, 회귀 테스트로 시스템 오류와 분리됐다.
- 장전 scanner의 fail-closed, RVOL baseline 부족 차단, ORB false breakout kill switch도 같은 계열이다. 자동매매에서 안전한 침묵은 기능이다.

### 로컬 상태는 브로커 상태와 계속 어긋날 수 있다

- startup reconciliation만으로는 부족했다.
- 로컬 DB에 stale `ACCEPTED` BUY 주문이 남으면 실제 브로커에는 보유 수량이 생겼고 미체결이 없어도, 이후 SELL 청산이 `open order already exists for symbol`로 막힐 수 있었다.
- 그래서 복구는 시작 시 한 번 하는 절차가 아니라, 각 cycle 시작에서 브로커 balance와 open orders를 다시 맞추는 운영 루틴이 됐다.

### 성능 목표는 유니버스 크기와 같이 써야 했다

- 2026-04-09 live daemon 로그에서는 100종목 full `config_universe`와 REST-only full-session replay가 약 88초 사이클로 이어졌다.
- `1초` 목표는 모든 경로의 약속이 아니라 active watchlist 또는 live scanner가 줄인 selected universe에만 정의해야 했다.
- 이 구분을 문서와 로그에 남기지 않으면 병목을 "더 병렬화하면 된다"로 오해하기 쉽다.

### 위키와 테스트가 감정을 낮춰 줬다

- 실거래 개발은 작은 불일치가 실제 계좌 상태와 연결될 수 있어서, 코드를 고치는 감각이 일반 웹 기능보다 훨씬 조심스러웠다.
- 도움이 된 것은 자신감보다 기록이었다. incident를 `kb/wiki/queries/`에 남기고, 같은 사실을 `specs/`, 운영 문서, 테스트로 동기화하면서 문제를 감정이 아니라 재현 가능한 질문으로 낮출 수 있었다.

## 블로그 초안 방향

- 공개 글은 기능 소개가 아니라 기술 회고로 쓴다.
- 중심 문장은 "자동매매 봇을 만들며 배운 건 더 좋은 진입 신호보다, 실시간 시스템의 경계를 코드와 문서로 설명하는 일이었다"로 둔다.
- 독자가 가져갈 결론은 다음 세 가지다.
  - 자동매매는 전략 엔진이 아니라 상태와 시간의 운영 시스템이다.
  - 거래하지 않는 결정, fail-closed, reconcile, degraded mode는 보조 기능이 아니라 핵심 기능이다.
  - 위키와 테스트는 개발 산출물이 아니라 실거래 불안을 낮추는 장치다.

## 연결할 위키 페이지

- [[wiki/topics/llm-friendly-trading-stack|LLM 친화적 자동매매 작업공간]]
- [[wiki/drafts/2026-04-06-open-trading-api-workbench|자동매매 봇을 만들며 배운 것]]

## 불확실성 및 후속 조사

- 이 회고는 로컬 개발 위키와 운영 문서에 기반하므로, 공개 upstream 저장소의 최신 상태와 1:1로 같다고 단정하지 않는다.
- WebSocket 기반 bar cache, 장중 미체결 정정/취소 루프, postmortem metric 자동 집계는 아직 후속 과제로 남아 있다.
- 다음 글 후보는 "sparse intraday를 5분 clock bar로 해석한 과정" 또는 "자동매매에서 reconciliation이 왜 핵심 도메인 로직이 되는가"로 분리할 수 있다.
