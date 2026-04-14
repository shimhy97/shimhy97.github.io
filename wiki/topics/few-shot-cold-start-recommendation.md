---
title: "few-shot 콜드스타트 추천"
type: topic
status: active
updated_at: 2026-04-09
source_count: 1
tags:
  - recommender-systems
  - cold-start
  - meta-learning
  - few-shot
---

# 주제 개요

## 한 줄 정의

- 콜드스타트 추천을 완전 무정보 추론이 아니라, 소량의 초기 반응으로 즉석 개인화를 수행하는 few-shot 적응 문제로 다루는 관점이다.

## 현재 이해

- 이 관점에서는 추천 모델이 처음부터 유저를 완전히 아는 것이 아니라, 몇 개 반응을 통해 빠르게 적응할 수 있는 초기값을 갖는지가 더 중요하다.
- MeLU는 공통 임베딩 공간은 유지한 채 decision layer만 유저별로 업데이트하는 구조를 택해, 적은 반응에서의 안정성을 우선한다.
- `support set`은 적응용 데이터, `query set`은 적응 뒤 일반화 성능을 보는 검증용 데이터로 나뉜다.
- 서비스 단계에서는 새 유저의 support set으로 local update를 수행한 뒤, 아직 보지 않은 아이템 전체를 재점수화해 추천하는 흐름으로 이해하는 편이 맞다.
- 이 관점의 약점도 분명하다. 어떤 반응을 초기 evidence로 받을지, 1~2개 반응만 있을 때 얼마나 흔들리는지, truly zero-shot은 어떻게 처리할지가 따로 남는다.

## 근거 소스

- [[wiki/sources/melu-cold-start-recommendation|MeLU: Meta-Learned User Preference Estimator for Cold-Start Recommendation]]

## 연결 페이지

- [[wiki/queries/2026-04-09-how-melu-serves-a-new-user|MeLU는 새 유저에게 어떻게 추천하나]]
- [[wiki/drafts/2026-04-09-melu-few-shot-cold-start-recommendation|MeLU를 다시 읽기: 콜드스타트 추천은 몇 개 반응 뒤에 시작돼요]]

## 열린 질문

- 새 유저 onboarding에서 evidence candidate를 어떤 UI와 반응 형식으로 구현해야 이 논문의 가정이 실제 서비스로 이어질까
- 임베딩까지 함께 적응시키는 후속 설계가 few-shot 안정성과 성능 사이에서 어떤 균형을 만들까
- 오프라인 support/query 분할이 실제 온라인 초기 세션의 잡음과 편향을 얼마나 잘 대변할까

## 발행 후보 아이디어

- cold-start 논문을 읽을 때 0-shot과 few-shot을 먼저 구분해야 하는 이유
- 추천 모델 논문에서 `support set`, `query set`, `local update`를 서비스 흐름으로 번역하는 방법
- MeLU 이후 few-shot 추천 모델이 임베딩 적응 문제를 어떻게 다뤘는지 비교하는 후속 글
