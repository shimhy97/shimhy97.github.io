---
title: "자동매매 봇을 만들며 배운 것"
type: draft
status: published
created_at: 2026-04-06
updated_at: 2026-04-20
source_count: 1
tags:
  - trading-bot
  - kis-open-api
  - retrospective
  - operations
  - engineering
---

# 중심 문장

- 자동매매 봇을 만들며 배운 건 더 좋은 진입 신호를 찾는 일보다, 실시간 시장에서 `시간`, `데이터`, `주문`, `상태`의 경계를 코드와 문서로 설명하는 일이 먼저라는 점이다.

## 오프닝 메모

처음에는 이 개발을 전략 구현기로 쓰고 싶었다. 하지만 `open-trading-api`의 로컬 위키를 다시 읽어 보면 실제로 많이 배운 지점은 전략 공식이 아니라 운영 경계였다. 0수량 주문, sparse intraday, ORB 세션 경계 오염, stale open order, 88초 사이클 병목은 모두 "전략이 틀렸다"보다 "시스템이 자기 상태를 충분히 설명하지 못했다"에 가까웠다.

이번 글은 그래서 기능 나열보다 회고로 쓴다. 기술적으로는 `src/`, `kb/`, `specs/`, `docs/`, 테스트가 어떻게 맞물렸는지 적고, 개인적으로는 실거래 코드 앞에서 느낀 조심스러움과 기록의 효용을 남긴다.

## 섹션 구조

### 샘플에서 계좌로 넘어가며 기준이 바뀌었어요

- KIS Open API 샘플은 API 호출법을 알려 주지만, 실거래 봇은 계좌 상태와 주문 결과를 책임져야 한다.
- `src/` 런타임이 생기면서 인증, quote, intraday bar, balance, 주문 제출, SQLite 상태, daemon, kill switch가 하나의 폐회로가 됐다.
- 이 전환에서 가장 먼저 느낀 것은 "예제는 성공 경로를 보여 주지만, 봇은 실패 경로를 기억해야 한다"는 점이다.

### 전략보다 먼저 시장의 시계를 배웠어요

- `opening_range_breakout_1m`는 현재 5분 ORB로 동작하고, `sma_cross_5m`는 09:30 이후 추세 확인 전략에 가깝다.
- 두 전략을 붙일 때 핵심은 handoff가 아니라 소유권이었다. ORB 포지션이 남아 있으면 ORB가 청산까지 관리하고, SMA는 flat 이후 신규 진입만 맡아야 한다.
- `09:00`, `09:10`, `09:30`, 정규장, 이전 정규장 tail, current-session cache 같은 시간 경계가 전략보다 먼저 확정돼야 했다.

### 데이터는 빈칸을 품은 채로 온다는 걸 배웠어요

- KIS intraday 데이터는 종목마다 1분봉 밀도가 달랐다.
- `raw_bars=147`이어도 5분 버킷이 충분히 닫히지 않아 `bars=19`처럼 줄어들 수 있었다.
- 이 경험은 sparse 데이터를 5분 clock bar로 다시 정의하게 만들었고, 데이터 집계는 단순 전처리가 아니라 전략 의미를 정하는 일이라는 점을 보여 줬다.

### 주문하지 않는 판단도 기능이어야 했어요

- 0수량 주문은 시스템 오류가 아니라, 최종 비중 한도로는 1주도 살 수 없는 상태였다.
- `rvol_baseline_missing`, fail-closed scanner, ORB kill switch도 같은 성격이다.
- 자동매매에서 "아무 주문도 내지 않았다"는 결과는 실패가 아니라 안전한 판단으로 기록돼야 한다.

### 상태 복구는 장 시작 전에만 끝나지 않았어요

- startup reconciliation은 필요했지만 충분하지 않았다.
- stale `ACCEPTED` BUY 주문이 로컬 DB에 남아 있으면, 실제로는 보유 수량이 있고 미체결이 없어도 SELL 청산이 막힐 수 있었다.
- 그래서 reconciliation은 시작 시 한 번 수행하는 부트 절차가 아니라, cycle 시작마다 브로커 truth와 로컬 truth를 맞추는 운영 루틴이 됐다.

### 성능 목표는 유니버스 크기와 함께 써야 했어요

- 2026-04-09 live 로그에서 100종목 full `config_universe`와 REST-only full-session replay는 약 88초 사이클로 나타났다.
- `1초` 목표는 모든 경로가 아니라 selected universe 경로에만 붙어야 했다.
- 이 배움은 성능 최적화보다 먼저 "정상 경로와 degraded 경로를 구분하라"는 운영 계약으로 남았다.

### 가장 남은 건 위키와 테스트로 생각을 고정한 경험이에요

- incident를 채팅에서 끝내지 않고 `kb/wiki/queries/`에 남긴 덕분에, 다음 문제를 분석할 때 같은 맥락을 다시 조립하지 않아도 됐다.
- `specs/`, 운영 문서, 테스트가 같은 결론을 가리키도록 맞추는 과정이 실거래 불안을 낮췄다.
- 이 글의 감정적 결론은 자신감보다 겸손이다. 시장과 브로커와 로컬 상태가 조금씩 비동기일 때, 코드는 그 어긋남을 조용히 설명해야 한다.

## 화면 구성 메모

- 서론 다음 `이번 글에서 볼 것` 요약 박스를 둔다.
- `샘플 -> 실거래 런타임 -> 운영 incident -> 위키/스펙/테스트 -> 다음 cycle` 흐름을 Mermaid로 보여 준다.
- 중간에 `처음 기대한 일`과 `실제로 배운 일`을 표로 비교한다.
- 주문하지 않는 기능과 degraded mode를 notice box로 분리해 읽는 리듬을 만든다.

## 근거 페이지

- [[wiki/sources/open-trading-api|open-trading-api 실거래 봇 개발 회고]]
- `/Users/shimhy97/open-trading-api/kb/wiki/queries/zero-quantity-order-sizing-incident-2026-04-06.md`
- `/Users/shimhy97/open-trading-api/kb/wiki/queries/sma-cross-lookback-warmup-incident-2026-04-07.md`
- `/Users/shimhy97/open-trading-api/kb/wiki/queries/runtime-log-diagnostics-and-sparse-intraday-2026-04-09.md`
- `/Users/shimhy97/open-trading-api/kb/wiki/queries/orb-session-boundary-incident-2026-04-10.md`
- `/Users/shimhy97/open-trading-api/kb/wiki/queries/sma-cross-rvol-baseline-cold-start-2026-04-13.md`
- `/Users/shimhy97/open-trading-api/kb/wiki/queries/sma-cross-stale-open-order-exit-block-2026-04-13.md`

## 발행 결과

- 게시글: [../../_posts/2026-04-06-open-trading-api-workbench.md](../../_posts/2026-04-06-open-trading-api-workbench.md)
- 후속 글 후보:
  - sparse intraday를 5분 clock bar로 해석한 과정
  - 자동매매에서 reconciliation이 도메인 로직이 되는 이유
  - 장전 scanner와 selected universe가 저지연 경로를 만드는 방식
