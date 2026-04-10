---
title: "MeLU를 다시 읽기: 콜드스타트 추천은 0-shot이 아니라 몇 개 반응 뒤에 시작돼요"
date: 2026-04-09 17:30:00 +0900
categories:
  - machine-learning
  - recommender-systems
tags:
  - paper
  - cold-start
  - few-shot
  - meta-learning
  - recommender-systems
  - maml
excerpt: "MeLU는 새 유저를 아무 정보 없이 맞히는 추천기가 아니라, 몇 개 반응을 받은 뒤 decision layer만 즉석 적응시키는 few-shot 개인화 모델로 읽는 편이 더 정확하다."
---

Hoyeop Lee 등은 KDD 2019에서 발표한 MeLU를 콜드스타트 추천 모델로 소개했지만, 이 논문을 실제로 읽을 때 더 중요한 포인트는 0-shot보다 few-shot에 가깝다는 점이에요.<sup><a href="#src-1">[1]</a></sup> 새 유저가 아무 정보도 없는 상태에서 바로 개인화 추천이 시작되는 게 아니라, 먼저 몇 개 아이템에 대한 반응을 받아 유저 전용 모델을 짧게 적응시킨 뒤 전체 아이템을 다시 점수화하는 흐름이기 때문입니다.<sup><a href="#src-1">[1]</a></sup> 그래서 MeLU는 "콜드스타트를 해결했다"는 한 문장보다, "새 유저 onboarding을 메타러닝 문제로 다시 썼다"는 설명이 더 잘 맞아요. 이번 글에서는 먼저 논문의 핵심 주장과 abstract 수준 요약을 짚고, 그다음 읽다가 가장 자주 막히는 지점인 `support set`, `query set`, `local update`, 그리고 "임베딩은 고정하고 해석기만 바꾼다"는 말을 중심으로 다시 정리해보려 해요.

## Abstract를 서비스 흐름으로 옮기면 이런 논문이에요

논문의 큰 주장은 단순합니다. 새 유저는 히스토리가 거의 없어서 일반 추천 모델이 약해지는데, 그렇다고 유저가 충분히 많은 데이터를 남길 때까지 기다릴 수는 없으니 몇 개 반응만으로도 빠르게 개인화할 수 있는 초기 모델을 메타러닝으로 학습하자는 거예요.<sup><a href="#src-1">[1]</a></sup> 논문 abstract는 기존 추천 연구의 한계를 두 가지로 요약하는데, 하나는 몇 개 아이템만 소비한 유저에게 추천이 약하다는 점이고, 다른 하나는 취향을 식별하기 위한 evidence candidate가 부정확하다는 점입니다.<sup><a href="#src-1">[1]</a></sup> 이때 MeLU는 모델 전체를 매번 다시 학습하지 않고, 공통 파라미터에서 출발한 뒤 새 유저의 소량 반응으로 decision layer를 짧게 적응시키는 방식을 택합니다.<sup><a href="#src-1">[1]</a></sup>

구조를 더 압축하면 세 문장으로 요약할 수 있어요. 첫째, 유저 속성과 아이템 속성을 임베딩해 하나의 입력 벡터를 만듭니다.<sup><a href="#src-1">[1]</a></sup> 둘째, 많은 유저를 대상으로 "몇 개 예시만 보고도 빨리 적응하는 출발점"을 메타학습합니다.<sup><a href="#src-1">[1]</a></sup> 셋째, 새 유저가 들어오면 evidence candidate 몇 개에 대한 반응을 support set으로 삼아 local update를 수행하고, 그 유저가 아직 보지 않은 아이템 전체를 다시 점수화해 추천합니다.<sup><a href="#src-1">[1]</a></sup> 논문이 MovieLens 1M과 BookCrossing에서 성능을 비교하고, 초록에서는 MAE가 최대 5.92% 개선됐다고 강조하는 것도 바로 이 흐름이 실제로 통한다는 점을 보여 주려는 맥락이에요.<sup><a href="#src-1">[1]</a></sup>

## 수식은 결국 입력을 만들고, 조금 고치고, 다시 점수 매기는 흐름이에요

논문 수식이 처음엔 복잡해 보여도, 실제로는 아래 세 단계만 따라가면 됩니다.<sup><a href="#src-1">[1]</a></sup>

$$
U_i = [e_{i1}c_{i1}; \cdots ; e_{iP}c_{iP}]^\top
$$

$$
I_j = [e_{j1}c_{j1}; \cdots ; e_{jQ}c_{jQ}]^\top
$$

$$
x_0 = [U_i; I_j], \qquad \hat{y}_{ij} = f_{\theta_1, \theta_2}(x_0)
$$

첫 줄과 둘째 줄은 "유저와 아이템을 벡터로 바꾼다"는 뜻이에요. <span markdown="0">\(c_{i1}\)</span>, <span markdown="0">\(c_{i2}\)</span> 같은 값은 성별, 나이대, 직업처럼 각 속성을 나타내는 one-hot 벡터이고, <span markdown="0">\(e_{i1}\)</span>, <span markdown="0">\(e_{i2}\)</span>는 그걸 임베딩 벡터로 바꾸는 행렬입니다.<sup><a href="#src-1">[1]</a></sup> 여기서 세미콜론 `;`은 더하기가 아니라 이어붙이기예요. 즉 성별 임베딩 하나, 나이대 임베딩 하나, 직업 임베딩 하나를 길게 붙여서 유저 벡터 <span markdown="0">\(U_i\)</span>를 만든다는 뜻입니다. 아이템 벡터 <span markdown="0">\(I_j\)</span>도 같은 방식이고요. 그다음 <span markdown="0">\(x_0 = [U_i; I_j]\)</span>는 "유저 <span markdown="0">\(i\)</span>가 아이템 <span markdown="0">\(j\)</span>를 만났을 때"의 입력 하나를 뜻합니다. <span markdown="0">\(x_0\)</span>가 새 유저 자체가 아니라 유저-아이템 pair 입력이라는 점을 여기서 분리해 두면 뒤 문장이 훨씬 잘 읽혀요.

그다음은 예측 단계입니다. <span markdown="0">\(\hat{y}_{ij} = f_{\theta_1, \theta_2}(x_0)\)</span>는 지금 가진 모델 파라미터로 유저 <span markdown="0">\(i\)</span>가 아이템 <span markdown="0">\(j\)</span>를 얼마나 좋아할지 점수를 내는 식이에요.<sup><a href="#src-1">[1]</a></sup> 여기서 <span markdown="0">\(\theta_1\)</span>은 임베딩 쪽 파라미터, <span markdown="0">\(\theta_2\)</span>는 그 임베딩을 읽고 최종 점수를 내는 MLP head 쪽 파라미터로 이해하면 충분합니다. 아직은 "평균적인 유저에게 무난한 해석기"에 가깝고, support set을 보고 나서 이 해석기가 개인화됩니다.

$$
L_i = \frac{1}{|H_i|}\sum_{j \in H_i}(y_{ij} - \hat{y}_{ij})^2
$$

$$
\theta_{2,i} = \theta_2 - \alpha \nabla_{\theta_2} L_i\bigl(f_{\theta_1, \theta_2}\bigr)
$$

이 부분이 local update예요. <span markdown="0">\(L_i\)</span>는 새 유저의 support set에서 실제 반응 <span markdown="0">\(y_{ij}\)</span>와 예측값 <span markdown="0">\(\hat{y}_{ij}\)</span> 차이가 얼마나 큰지 계산한 오차입니다.<sup><a href="#src-1">[1]</a></sup> 그리고 <span markdown="0">\(\nabla\)</span>는 gradient, 즉 "오차를 줄이려면 어느 방향으로 파라미터를 움직여야 하는가"를 알려 주는 기울기예요. 식 전체를 사람 말로 바꾸면 "새 유저가 이미 반응한 몇 개 아이템을 보고, 그 유저에게 맞게 MLP head를 한 걸음 수정한다"는 뜻입니다. 논문 method와 Figure 3도 local update에서 바뀌는 부분을 decision-making layers와 output layer, 즉 <span markdown="0">\(W\)</span>와 <span markdown="0">\(b\)</span>가 있는 파란 박스로 제한해 설명합니다.<sup><a href="#src-1">[1]</a></sup> 중요한 건 이때 임베딩까지 같이 흔들지 않고 <span markdown="0">\(\theta_2\)</span> 쪽만 고친다는 점이에요. 그래서 공통 좌표계는 유지하면서, 점수를 읽는 기준만 유저별로 잠깐 바꿀 수 있습니다.

## 콜드스타트라는 말이 논문을 더 모호하게 만들어요

MeLU가 겨냥하는 대상은 분명 새 유저입니다. 다만 여기서 "새 유저"는 완전 무반응 유저라기보다, 몇 개 상호작용만 가진 유저에 더 가까워요.<sup><a href="#src-1">[1]</a></sup> 논문도 추천 시점에 먼저 evidence candidate를 보여 주고, 사용자의 item-consumption history를 바탕으로 local update를 수행한 뒤 아직 평가하지 않은 아이템 전체를 재점수화한다고 설명합니다.<sup><a href="#src-1">[1]</a></sup> 즉 질문을 한 번 더 풀어 쓰면 "아무 정보 없이 바로 추천"이 아니라 "몇 개를 먼저 물어본 뒤 그 답으로 추천"하는 구조예요.

이 차이를 먼저 잡아 두지 않으면 논문의 거의 모든 식이 헷갈립니다. 새 유저를 표현하는 기호와 유저-아이템 쌍 입력을 구분하기 어려워지고, 왜 support set과 query set을 따로 두는지도 모호해져요. MeLU를 읽을 때는 콜드스타트라는 단어를 잠시 내려놓고, "few-shot 개인화 추천"이라는 문장으로 바꿔 읽는 편이 훨씬 덜 혼란스럽습니다.

## 추천 전에 몇 개를 먼저 물어보는 구조예요

이 논문에서 제가 흥미롭게 본 부분은 evidence candidate selection입니다. 새 유저에게 처음 보여 줄 아이템을 아무 인기작으로 채우지 않고, 그 반응이 들어왔을 때 취향을 더 잘 구분해낼 수 있는 아이템을 고르려는 설계예요.<sup><a href="#src-1">[1]</a></sup> 논문은 이를 gradient 기반 구분력과 아이템 인지도(popularity)를 함께 반영하는 방식으로 설명합니다. 쉽게 말하면 "유저 차이를 잘 드러내면서도 사용자가 알아볼 만한 항목"을 먼저 보여 주겠다는 뜻이죠.

서비스 흐름으로 옮기면 그림은 단순합니다. 새 유저에게 초기 후보 아이템을 몇 개 보여 주고, 그중 일부에 대한 클릭이나 평점 같은 반응을 받습니다. 그 소량의 반응이 support set이 되고, 모델은 이 support set으로 유저 전용 파라미터를 잠깐 업데이트합니다. 그다음 업데이트된 모델로 아직 보지 않은 모든 아이템의 선호 점수를 계산해 상위 결과를 추천합니다.<sup><a href="#src-1">[1]</a></sup> 논문을 읽다가 "그래서 새 유저에게 실제로 어떻게 추천한다는 거지?"라는 질문이 생겼다면, 답은 결국 이 네 단계에 있습니다.

## 임베딩은 그대로 두고 해석기만 유저별로 틀어요

MeLU에서 가장 중요한 설계 선택은 local update 때 유저와 아이템 임베딩을 바꾸지 않고, decision-making layers와 output layer만 업데이트한다는 점입니다.<sup><a href="#src-1">[1]</a></sup> 논문 표현을 빌리면 users and items do not change, only the users' thoughts change라는 가정에 가까워요.<sup><a href="#src-1">[1]</a></sup> 저는 이 문장을 "공통 좌표계는 그대로 두고, 그 좌표계를 읽는 기준만 유저별로 조금 틀어 준다"는 뜻으로 읽는 편이 이해가 쉬웠습니다.

여기서 `x0 = [Ui; Ij]`도 같이 풀어야 합니다. `Ui`는 유저 속성을 임베딩해 만든 벡터이고, `Ij`는 아이템 속성을 임베딩해 만든 벡터예요. `x0`는 이 둘을 이어붙인 유저-아이템 pair 입력이지, 새 유저 자체를 뜻하는 기호가 아닙니다.<sup><a href="#src-1">[1]</a></sup> 그래서 새 유저가 들어왔을 때는 `x0`가 하나만 생기는 게 아니라, "새 유저 × 각 후보 아이템" 수만큼 만들어집니다. local update가 일어나는 위치는 `x0`가 아니라 그 위에서 점수를 읽는 MLP head 쪽이고, 이 덕분에 공통 표현 공간을 흔들지 않으면서도 유저별 해석 방식을 빠르게 적응시킬 수 있습니다.

## support와 query를 나눠 봐야 학습과 평가가 분리돼요

이 논문에서 가장 자주 생기는 오해는 "새 유저의 몇 개 안 되는 반응으로 모든 사용자 모델을 같이 업데이트하는 건가?"라는 질문입니다. 하지만 학습 단계에서 local update 대상은 그 iteration에서 뽑힌 유저 미니배치이고, 각 유저는 공통 파라미터의 복사본에서 출발해 자기 support set으로 personalized parameter를 만듭니다.<sup><a href="#src-1">[1]</a></sup> 즉 유저 A의 반응으로 유저 B의 개인화 파라미터를 직접 바꾸는 구조는 아니에요. 여러 유저에 대해 이렇게 만든 personalized result를 모아, query set 성능이 좋아지도록 공통 초기 파라미터를 global update 하는 게 메타러닝 단계입니다.<sup><a href="#src-1">[1]</a></sup>

support set과 query set을 나누는 이유도 여기서 분명해집니다. support set은 적응용 데이터이고, query set은 적응 뒤 일반화 성능을 보는 검증용 데이터예요.<sup><a href="#src-1">[1]</a></sup> 논문은 메타러닝 설명에서도 support set은 training loss, query set은 test loss에 대응한다고 분리해 둡니다.<sup><a href="#src-1">[1]</a></sup> 평가 단계에서는 이미 학습된 공통 파라미터를 고정해 둔 채, 테스트 유저의 support set으로 local update만 수행하고 query set에서 MAE나 nDCG를 계산합니다.<sup><a href="#src-1">[1]</a></sup> 반면 실서비스에서는 미래 정답이 아직 없기 때문에 query-set 오차를 즉시 계산할 수 없고, local update 뒤 예측 점수 `ŷ`만 산출해 추천하는 흐름으로 이해해야 맞아요.

한 번에 보면 아래 표처럼 정리할 수 있어요.

| 단계 | support set 역할 | query set 역할 | local update | global update |
| --- | --- | --- | --- | --- |
| 학습(train) | 각 유저에 맞는 personalized parameter를 만드는 적응용 데이터 | 적응 뒤 일반화 성능을 보는 검증용 데이터 | 배치에 뽑힌 각 유저별로 수행 | query set loss를 모아 공통 초기 파라미터를 갱신 |
| 평가(test) | 테스트 유저를 잠깐 개인화하는 적응용 데이터 | MAE, nDCG 같은 오프라인 성능을 계산하는 데이터 | 각 테스트 유저별로 수행 | 수행하지 않음 |
| 서비스(serving) | 새 유저 반응 몇 개를 받아 즉석 개인화에 사용 | 보통 없음. 미래 반응이 아직 없어서 즉시 오차 계산 불가 | 새 유저에게만 수행 | 수행하지 않음 |

이 표로 보면 헷갈리던 지점이 조금 정리됩니다. `support set`은 세 경우 모두 "적응용"이라는 역할이 유지되고, `query set`은 학습과 평가에서만 의미가 있어요. 그리고 `global update`는 훈련 단계에서만 일어나며, 서비스 시점에는 새 유저에게 맞춘 local update만 남습니다.

## 성능 수치보다 서비스 빈칸이 더 먼저 보여요

논문은 MovieLens 1M과 BookCrossing에서 실험했고, 초록 기준으로 기존 방법보다 MAE를 최대 5.92% 줄였다고 보고합니다.<sup><a href="#src-1">[1]</a></sup> 이 수치는 분명 중요하지만, 저는 오히려 서비스 설계 쪽 빈칸이 더 눈에 들어왔어요. 논문이 상정한 "new user"도 극단적 0-interaction이 아니라 어느 정도 히스토리를 가진 사용자이며, 평가에서도 support/query 분할이 가능한 오프라인 설정을 씁니다.<sup><a href="#src-1">[1]</a></sup> 그래서 onboarding 첫 세션처럼 반응이 1~2개뿐인 상황에서 얼마나 안정적인지, 반응 형식을 클릭으로 볼지 평점으로 볼지, local update를 실제 서비스 지연 안에 넣을 수 있는지는 여전히 남습니다.

이건 논문의 약점이라기보다 읽는 쪽이 함께 챙겨야 할 번역 문제에 가깝습니다. MeLU는 메타러닝이 추천에 어떻게 들어올 수 있는지 잘 보여 주지만, 그 자체로 완성된 제품 설계 문서는 아니에요. 그래서 이 논문을 실무 관점에서 읽을 때는 "성능이 얼마나 좋아졌나"보다 "새 유저에게 정확히 무엇을 먼저 묻고, 어떤 파라미터를 어디까지 즉석 적응시킬 것인가"를 같이 적어 두는 편이 더 남는다고 느꼈습니다.

## 마무리

MeLU를 한 문장으로 줄이면, 새 유저를 처음부터 이해하는 추천기가 아니라 몇 개 반응을 받은 뒤 유저별 해석기를 빠르게 보정하는 추천기라고 할 수 있어요. 이 관점으로 보면 `support set`, `query set`, `local update`, evidence candidate selection이 하나의 흐름으로 연결됩니다. 콜드스타트 추천 논문을 읽다가 막힐 때도, 먼저 "이 모델은 0-shot인가 few-shot인가"를 구분해 두면 훨씬 많은 문장이 풀려요.

## 출처

<span id="src-1"></span>[1] Hoyeop Lee, Jinbae Im, Seongwon Jang, Hyunsouk Cho, Sehee Chung, MeLU: Meta-Learned User Preference Estimator for Cold-Start Recommendation, KDD 2019, <a href="https://doi.org/10.1145/3292500.3330859" target="_blank" rel="noopener noreferrer">[원문보기]</a>
