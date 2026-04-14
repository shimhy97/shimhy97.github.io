---
title: "MeLU는 새 유저에게 어떻게 추천하고, local update는 누구 파라미터를 바꾸나"
type: query
status: filed
created_at: 2026-04-09
updated_at: 2026-04-09
source_count: 1
tags:
  - recommender-systems
  - cold-start
  - meta-learning
  - query
---

# 질문

MeLU는 새 유저에게 어떻게 추천하고, local update는 누구 파라미터를 바꾸나

## 결론

- MeLU는 완전 무반응 유저를 바로 개인화하는 0-shot 추천기가 아니라, evidence candidate 몇 개에 대한 반응을 받은 뒤 개인화를 시작하는 few-shot 추천 구조다.
- 새 유저가 남긴 소량의 반응은 그 유저 전용 head 파라미터에만 직접 반영된다. 모든 유저의 파라미터를 한 번에 영구 저장하거나 동시에 덮어쓰는 구조는 아니다.
- 학습 단계에서는 미니배치로 뽑힌 여러 유저 각각에 대해 local update를 수행하고, 그 결과를 바탕으로 공통 초기 파라미터를 global update 한다.
- 평가 단계에서는 공통 파라미터를 고정한 채, 테스트 유저별 local update만 수행한 뒤 query set에서 MAE나 nDCG를 계산한다.
- 서비스 단계에서는 support set으로 local update를 한 뒤, 아직 보지 않은 아이템 전부에 대해 예측 점수를 계산해 상위 아이템을 추천한다. 이 순간에는 미래 정답이 없으니 즉시 오차를 계산하지 못한다.

## 근거 페이지

- [[wiki/sources/melu-cold-start-recommendation|MeLU: Meta-Learned User Preference Estimator for Cold-Start Recommendation]]
- [[wiki/topics/few-shot-cold-start-recommendation|few-shot 콜드스타트 추천]]

## 후속 액션

- 서비스 관점 후속 글에서는 `support set`, `query set`, `train/test/serving`을 3열 표로 정리해 두면 재사용성이 높다.
- 후속 비교 대상으로 zero-shot onboarding 논문이나 user attribute 기반 추천 논문을 묶어 읽을 필요가 있다.

## 블로그 글로의 확장 가능성

- 논문 자체 요약보다, "MeLU를 읽을 때 독자가 가장 자주 헷갈리는 지점"을 풀어 주는 설명형 포스트로 확장하기 좋다.
- 특히 `x0`, 임베딩 고정, local/global update 구분, new user의 의미를 하나의 흐름으로 재구성하면 교육용 글 밀도가 높아진다.
