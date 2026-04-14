---
title: "open-trading-api"
type: source
status: active
source_kind: repository
source_path: "/Users/shimhy97/open-trading-api"
source_url: "https://github.com/koreainvestment/open-trading-api"
ingested_at: 2026-04-06
updated_at: 2026-04-06
tags:
  - trading
  - architecture
  - backtesting
  - llm
---

# 소스 요약

## 한 줄 요약

- `open-trading-api`는 한국투자증권 Open API 샘플 저장소를 출발점으로 삼되, LLM 친화 샘플 코드, 전략 설계기, 백테스터, 실거래 봇, 지식 위키를 한 저장소 안에 묶어 자동매매 작업공간으로 확장한 레포다.

## 핵심 내용

- 루트 `README.md`는 저장소를 단순 API 예제가 아니라 `examples_llm/`, `examples_user/`, `strategy_builder/`, `backtester/`, `src/`, `kb/`가 연결된 작업 체계로 소개한다.
- `strategy_builder/README.md`와 `backtester/README.md`는 `.kis.yaml`을 공통 계약으로 삼아 전략 설계와 과거 검증을 왕복시키는 흐름을 전면에 둔다.
- `src/app.py`와 `docs/implemented-trading-strategies.md`를 보면, 실제 런타임은 전략 레지스트리, 리스크 엔진, 실행 엔진, 복구 서비스가 조립된 실거래 봇 구조를 가진다.
- `SPEC_v0.1.md`는 주문 API 규칙, 시장코드와 거래소 코드의 구분, 복구 우선순위 같은 도메인 제약을 문서로 고정해 구현 방향을 명시한다.
- `kb/` 디렉터리는 이 저장소 자체도 `llm-wiki` 패턴으로 관리하려는 시도를 보여 주며, 코드와 문서를 LLM이 함께 유지보수하는 운영 방식을 드러낸다.

## 블로그에 중요한 포인트

- 이 레포의 핵심 가치는 기능 수보다도 "학습용 샘플 -> 전략 설계 -> 백테스트 -> 실거래"가 한 흐름으로 이어진다는 점에 있다.
- `.kis.yaml` 같은 공통 포맷이 있어야 UI 도구와 검증 엔진이 느슨하게 연결되면서도 같은 전략을 공유할 수 있다.
- 블로그 글에서는 홍보성 기능 나열보다, 구현된 것과 아직 설계 단계인 것을 분리해 설명하는 편이 신뢰도가 높다.
- 특히 `strategy_builder`와 `backtester`는 10개 프리셋 전략을 전면에 두지만, 현재 `src/` 실거래 봇에 등록된 전략은 3개라는 점이 중요한 현실 정보다.

## 연결할 위키 페이지

- [[wiki/topics/llm-friendly-trading-stack|LLM 친화형 자동매매 작업공간]]
- [[wiki/drafts/2026-04-06-open-trading-api-workbench|샘플 코드 저장소를 자동매매 워크벤치로 키운 open-trading-api]]

## 불확실성 및 후속 조사

- `strategy_builder`, `backtester`, `src/`의 전략 정의가 장기적으로 하나의 단일 스키마로 수렴할지, 아니면 도구별 표현을 계속 분리할지는 추가 구현을 더 봐야 판단할 수 있다.
- 백테스트 지표와 실거래 리스크 통제가 어디까지 같은 규칙을 공유하는지는 향후 운영 문서와 실제 주문 경로를 더 읽어 봐야 명확해진다.
