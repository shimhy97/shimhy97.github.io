---
title: "LLM 친화형 자동매매 작업공간"
type: topic
status: active
updated_at: 2026-04-06
source_count: 1
tags:
  - trading
  - architecture
  - llm
  - systems
---

# 주제 개요

## 한 줄 정의

- 학습용 API 예제, 전략 설계 UI, 백테스트 엔진, 실거래 런타임, 지식 위키를 한 저장소 안에서 연결해 두고 LLM이 이해하기 쉬운 문서 구조를 유지하는 자동매매 작업공간 설계다.

## 현재 이해

- `examples_llm/`와 `examples_user/`를 분리하면 LLM이 단일 기능을 탐색하기 쉬운 계층과 사람이 실제 사용 흐름을 따라가기 쉬운 계층을 동시에 유지할 수 있다.
- `strategy_builder`와 `backtester`는 `.kis.yaml`이라는 공통 계약을 통해 같은 전략을 설계와 검증 단계에서 왕복시킨다.
- `src/`는 실거래 봇 런타임이고, `docs/implemented-trading-strategies.md`는 현재 실제 등록 전략과 미완료 지점을 문서로 드러낸다.
- `SPEC_v0.1.md`, `AGENTS.md`, `kb/`는 구현만이 아니라 운영 규칙과 판단 근거까지 저장소 안에 남긴다는 점에서 중요하다.
- 따라서 이 주제는 "자동매매 기능 소개"보다 "도구 간 계약을 어떻게 유지하는가"와 "LLM이 읽기 쉬운 저장소 구조를 어떻게 만드는가"에 더 가깝다.

## 근거 소스

- [[wiki/sources/open-trading-api|open-trading-api]]

## 연결 페이지

- [[wiki/overview|블로그 위키 개요]]
- [[wiki/drafts/2026-04-06-open-trading-api-workbench|샘플 코드 저장소를 자동매매 워크벤치로 키운 open-trading-api]]

## 열린 질문

- `.kis.yaml`이 장기적으로 실거래 봇 `src/`까지 포괄하는 단일 전략 계약이 될 수 있는가
- 백테스트에서 보이는 10개 프리셋과 실거래 봇의 3개 등록 전략을 어떤 정책으로 수렴시킬 것인가
- 시그널 생성, 리스크 통제, 주문 실행 사이의 운영 상태를 위키와 문서에 어디까지 자동 반영할 수 있는가

## 발행 후보 아이디어

- 샘플 코드 저장소를 LLM 친화 작업공간으로 바꾸는 구조적 기준
- `.kis.yaml` 같은 중간 계약이 전략 설계기와 백테스터를 연결하는 방식
- 실거래 봇 문서에서 "이미 구현된 것"과 "아직 설계 단계인 것"을 분리해 읽는 법
