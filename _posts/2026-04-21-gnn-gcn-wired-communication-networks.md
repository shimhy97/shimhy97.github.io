---
title: "통신망 GNN을 읽는 법: GCN 수식은 이웃을 섞는 순서예요"
date: 2026-04-21 13:20:00 +0900
categories:
  - machine-learning
  - networking
classes:
  - reading-post
toc: true
toc_label: "이 글의 구조"
toc_icon: stream
tags:
  - paper
  - graph-neural-network
  - gcn
  - communication-networks
  - wired-networks
excerpt: "Jiang의 통신망 GNN 서베이를 유선 네트워크 활용, message passing, GCN 수식, W의 feature 변환 순서로 다시 읽는다."
---

Weiwei Jiang의 `Graph-based Deep Learning for Communication Networks: A Survey`를 처음 읽을 때는 "통신망에 GNN이 어디에 쓰였나"가 먼저 보였어요.<sup><a href="#src-1">[1]</a></sup> 그런데 질문을 계속 쌓다 보니, 더 중요한 갈림길은 모델 목록이 아니었습니다. 통신망을 그래프로 본다는 말이 실제 수식에서는 어떻게 <span markdown="0">\(\hat{A}H W\)</span> 같은 형태로 바뀌는지가 핵심이었어요.

그래서 이 글은 논문 요약만 하지 않습니다. 유선 네트워크에서 GNN이 어떤 운영 문제로 이어지는지 먼저 잡고, 그다음 제가 Q&A로 정리했던 그래프 신경망 (Graph Neural Network, GNN)과 그래프 합성곱 네트워크 (Graph Convolutional Network, GCN)의 수식을 초심자 순서로 다시 풀어봅니다. 마지막에는 왜 <span markdown="0">\(W\)</span>가 필요한지, 왜 <span markdown="0">\(HW\)</span>로 쓰는지, GraphSAGE로 넘어가기 전에 무엇을 가져가야 하는지도 같이 정리합니다.

<div class="notice--primary" markdown="1">

**이번 글에서 볼 것**

- 통신망 GNN의 출발점은 "라우터, 링크, 트래픽, 경로를 그래프로 다시 읽기"입니다.
- 유선망에서는 GNN 예측이 delay, routing, configuration, security 같은 운영 판단으로 이어져야 의미가 생깁니다.
- GNN 일반식은 `message -> aggregate -> update`이고, GCN은 그 흐름을 정규화 adjacency와 weight matrix로 줄인 표기입니다.
- <span markdown="0">\(W\)</span>는 차원을 무조건 키우는 장치가 아니라, 이웃 정보를 문제에 맞는 feature 의미로 다시 조합하는 학습 파라미터입니다.

</div>

## 0. 논문은 토폴로지를 입력으로 되살립니다

이 서베이는 2016년부터 2021년까지의 graph-based deep learning 연구 81편을 무선 네트워크, 유선 네트워크, 소프트웨어 정의 네트워킹 (Software Defined Networking, SDN) 세 축으로 나눠 정리합니다.<sup><a href="#src-1">[1]</a></sup> 논문이 다루는 문제는 channel allocation, power control, routing, traffic prediction, virtual network embedding, intrusion detection처럼 넓습니다. 하지만 이 넓은 목록을 관통하는 질문은 하나예요. "네트워크 문제에서 구조 자체를 어떻게 모델 입력으로 넣을 것인가?"

기존 딥러닝은 이미지처럼 격자 구조가 있거나, 시계열처럼 순서가 분명한 데이터에 잘 맞았습니다. 반면 통신망은 라우터와 링크, 송수신 페어와 간섭, 플로우와 경로가 얽힌 비유클리드 구조입니다. 논문은 이 지점에서 GNN이 자연스럽다고 봅니다. 유선 backbone에서는 node가 router이고 edge가 physical transmission link입니다. node feature에는 in-flow와 out-flow traffic이 들어갈 수 있고, edge feature에는 bandwidth나 delay 같은 transmission metric이 들어갈 수 있어요.<sup><a href="#src-1">[1]</a></sup>

<figure class="diagram-figure">
  <iframe class="diagram-frame" src="/assets/diagrams/gnn-gcn-wired-communication-networks/network-to-gnn.html" title="통신망 topology가 GNN 입력이 되는 흐름"></iframe>
  <figcaption class="figure-caption">이 글에서 중요한 흐름은 통신망을 표나 시계열로만 펴지 않고, topology를 가진 그래프로 만든 뒤 운영 판단으로 연결하는 점이에요.</figcaption>
</figure>

여기서 "그래프로 만든다"는 말은 생각보다 구체적입니다. 무엇을 node로 볼지, 어떤 관계를 edge로 둘지, node feature와 edge feature에 무엇을 넣을지를 먼저 정해야 합니다. 이 결정을 흐리면 GNN 모델 이름을 바꿔도 문제 정의가 선명해지지 않습니다. GraphSAGE를 공부하기 전에도 결국 같은 질문으로 돌아옵니다. "내 문제의 node feature는 무엇이고, edge는 어떤 기준으로 만들 것인가?"

## 1. 유선망에서는 예측이 운영으로 넘어갑니다

유선 네트워크 섹션은 이 논문에서 특히 실무 감각이 잘 드러나는 부분입니다. 논문은 computer network를 중심으로 network modeling, network configuration, network prediction, network management, network security를 나누고, 이어서 blockchain platform, data center network, optical network 같은 특수한 유선망 사례를 설명합니다.<sup><a href="#src-1">[1]</a></sup>

제가 이 섹션을 다시 읽으며 잡은 기준은 "예측 자체가 목표인가, 예측이 운영 행동으로 이어지는가"였습니다. 유선망에서 GNN이 쓸모 있으려면 delay나 traffic을 맞히는 데서 끝나지 않고 routing, load balancing, configuration validation, alert correlation 같은 판단으로 넘어가야 합니다.

| 활용 축 | 그래프로 보는 입력 | 모델이 돕는 판단 |
| --- | --- | --- |
| Network modeling | topology, routing scheme, traffic matrix | delay, jitter, loss, throughput 같은 end-to-end metric 추정 |
| Configuration | 부분 설정, routing policy, network property | BGP configuration synthesis, MPLS property analysis, feasibility 판단 |
| Prediction | traffic history, origin-destination relation, graph structure | backbone traffic prediction, delay prediction, demand 변화 감지 |
| Management | 예측된 링크/경로 상태 | routing optimization, load balancing, traffic engineering |
| Security | botnet connection, alert graph, intrusion pattern | botnet detection, intrusion detection, alert correlation |
| Data center / optical | dynamic topology, flow, lightpath relation | Flow Completion Time (FCT) 예측, unseen topology routing |

Network modeling은 topology, routing scheme, traffic matrix를 함께 넣고 end-to-end metric을 추정하려는 축입니다.<sup><a href="#src-1">[1]</a></sup> 이때 GNN은 단순 분류기라기보다 네트워크 simulator에 가까운 역할을 맡습니다. 아직 보지 못한 topology나 traffic 조합에서 delay, jitter, loss가 어떻게 나올지 추정하려는 거죠.

Traffic prediction 쪽에서는 공간 의존성과 시간 의존성이 같이 나옵니다. 예를 들어 논문은 graph convolution과 GRU를 결합해 실제 IP backbone traffic data를 예측하는 흐름을 소개합니다.<sup><a href="#src-1">[1]</a></sup> graph convolution은 "어느 라우터와 어느 링크가 연결되어 있는가"를 보고, GRU 같은 recurrent 구조는 "시간에 따라 traffic이 어떻게 바뀌는가"를 봅니다.

<div class="notice--info" markdown="1">

**유선망 섹션을 읽는 기준**

- GNN이 무엇을 node로 삼는지 먼저 봅니다.
- 예측 대상이 delay인지, traffic인지, routing cost인지 구분합니다.
- 그 예측이 configuration, routing, security 판단으로 어떻게 넘어가는지 확인합니다.

</div>

Data center network 사례는 이 연결을 더 분명하게 보여 줍니다. topology가 바뀌어도 FCT를 예측하고, 그 예측을 flow routing, flow scheduling, topology management에 쓰려는 흐름이 나옵니다.<sup><a href="#src-1">[1]</a></sup> Optical Transport Network (OTN)에서는 unseen topology에서 routing을 다루기 위해 GNN의 일반화 능력과 deep reinforcement learning을 결합하는 방향도 소개됩니다.<sup><a href="#src-1">[1]</a></sup>

그래서 이 논문을 유선망 관점으로 읽을 때 모델 이름을 먼저 외우는 것은 효율이 낮았습니다. 더 좋은 질문은 이것이었어요. "이 연구는 topology, traffic, routing 중 무엇을 함께 읽고, 그 결과를 어떤 운영 판단에 넘기는가?"

## 2. GNN 수식은 메시지를 모으는 문장입니다

Q&A에서 가장 오래 붙잡은 부분은 GNN 일반식이었습니다. 처음 보면 기호가 많아서 어려워 보이지만, 사실 한 문장으로 줄일 수 있어요. 노드는 이웃에게서 메시지를 받고, 그 메시지를 모아 자기 표현을 새로 만듭니다.

논문은 공간 기반 GNN을 설명하면서 Message Passing Neural Network (MPNN) 관점의 식을 소개합니다.<sup><a href="#src-1">[1]</a></sup>

$$
m_i^{(t)}=\sum_{j\in N(i)}M^{(t)}(X_i^{(t-1)},X_j^{(t-1)},e_{ij})
$$

$$
X_i^{(t)}=U^{(t)}(X_i^{(t-1)},m_i^{(t)})
$$

이 수식의 흐름은 작은 그래프 하나를 놓고 보면 훨씬 덜 추상적입니다. 아래 그림은 `1 - 2 - 3` 그래프에서 중심 노드 2가 양쪽 이웃의 메시지를 받아 새 표현을 만드는 과정을 보여 줍니다.

<figure class="diagram-figure">
  <iframe class="diagram-frame" src="/assets/diagrams/gnn-gcn-wired-communication-networks/message-passing.html" title="1-2-3 그래프에서 message passing 읽기"></iframe>
  <figcaption class="figure-caption">message passing은 이웃이 보낸 메시지를 모으고, 그 집계값으로 중심 노드 표현을 갱신하는 순서로 읽으면 됩니다.</figcaption>
</figure>

첫 번째 식은 이웃이 보내는 메시지를 모으는 단계입니다. <span markdown="0">\(i\)</span>는 지금 업데이트하려는 중심 노드이고, <span markdown="0">\(N(i)\)</span>는 그 노드의 이웃 집합입니다. <span markdown="0">\(X_i^{(t-1)}\)</span>는 중심 노드의 이전 표현, <span markdown="0">\(X_j^{(t-1)}\)</span>는 이웃 노드의 이전 표현입니다. <span markdown="0">\(e_{ij}\)</span>는 두 노드 사이의 edge feature인데, 통신망에서는 링크 대역폭, 지연, 거리, 연결 종류 같은 값이 들어갈 수 있습니다.

두 번째 식은 업데이트 단계입니다. 이웃에게서 모은 메시지 <span markdown="0">\(m_i^{(t)}\)</span>와 내 이전 표현을 합쳐 새 표현 <span markdown="0">\(X_i^{(t)}\)</span>를 만듭니다. 여기서 <span markdown="0">\(t\)</span>는 꼭 실제 시간이 아닙니다. 일반적인 GNN 설명에서는 layer, propagation step, iteration으로 읽는 편이 자연스럽습니다. 한 번 업데이트하면 1-hop 이웃 정보가 들어오고, 두 번 업데이트하면 이웃의 이웃까지 간접적으로 들어오는 식이에요.

작은 예시로 보면 더 쉽습니다. 그래프가 `1 - 2 - 3`이고, 지금 2번 노드를 업데이트한다고 해봅시다.

| 항목 | 값 |
| --- | --- |
| 중심 노드 | <span markdown="0">\(i=2\)</span> |
| 이웃 집합 | <span markdown="0">\(N(2)=\{1,3\}\)</span> |
| 이전 표현 | <span markdown="0">\(X_1=10, X_2=20, X_3=30\)</span> |
| 메시지 함수 | <span markdown="0">\(M(X_i,X_j)=X_j\)</span> |
| 업데이트 함수 | <span markdown="0">\(U(X_i,m_i)=X_i+\frac{1}{2}m_i\)</span> |

이때 1번 노드는 2번에게 10을 보내고, 3번 노드는 2번에게 30을 보냅니다. 메시지를 합치면 <span markdown="0">\(m_2=40\)</span>입니다. 업데이트 함수에 넣으면 새 표현은 아래처럼 됩니다.

$$
X_2^{(t)}=20+\frac{1}{2}\cdot 40=40
$$

이 장난감 예시는 실제 모델이 아니라 수식을 읽기 위한 번역입니다. 그래도 핵심은 충분히 보여 줍니다. GNN은 이웃 수가 노드마다 달라도 쓸 수 있어야 하고, 이웃 순서가 바뀌어도 결과가 흔들리지 않아야 합니다. 그래서 sum, mean, max처럼 순서에 둔감한 aggregation이 자주 등장합니다.

## 3. GCN은 그 문장을 행렬곱으로 줄입니다

GCN은 GNN의 한 종류입니다. 더 정확히 말하면, 방금 본 message passing의 여러 선택지를 상당히 단순하게 고른 모델입니다. 메시지는 이웃 feature 자체로 두고, aggregation은 adjacency matrix를 이용한 가중합으로 두며, update는 선형변환과 활성화로 둡니다.

먼저 그래프를 인접행렬 (adjacency matrix) <span markdown="0">\(A\)</span>로 둡니다. <span markdown="0">\(A_{ij}=1\)</span>이면 노드 <span markdown="0">\(i\)</span>와 <span markdown="0">\(j\)</span>가 연결되어 있고, 0이면 연결되어 있지 않다는 뜻입니다. 노드 feature를 모두 모은 행렬을 <span markdown="0">\(H\in\mathbb{R}^{N\times d}\)</span>라고 하면, <span markdown="0">\(AH\)</span>는 각 노드가 이웃 feature를 모은 결과가 됩니다.

예를 들어 다시 `1 - 2 - 3` 그래프를 보겠습니다.

$$
A=
\begin{bmatrix}
0&1&0\\
1&0&1\\
0&1&0
\end{bmatrix},
\quad
H=
\begin{bmatrix}
1\\
2\\
3
\end{bmatrix}
$$

그러면 <span markdown="0">\(AH\)</span>는 아래처럼 됩니다.

$$
AH=
\begin{bmatrix}
2\\
1+3\\
2
\end{bmatrix}
=
\begin{bmatrix}
2\\
4\\
2
\end{bmatrix}
$$

1번 노드는 이웃 2번의 값 2를 받고, 2번 노드는 이웃 1번과 3번의 값인 1과 3을 합쳐 4를 받습니다. 즉 adjacency matrix 곱셈은 "연결된 이웃의 feature를 모으는 연산"으로 읽을 수 있습니다.

그런데 <span markdown="0">\(A\)</span>만 쓰면 자기 자신의 feature가 빠집니다. 그래서 GCN은 보통 self-loop를 추가합니다.

$$
\tilde{A}=A+I_N
$$

이제 자기 자신도 이웃 집계에 들어갑니다. 하지만 그냥 더하기만 하면 이웃이 많은 node의 값이 커지는 문제가 생깁니다. 그래서 degree matrix <span markdown="0">\(\tilde{D}\)</span>를 이용해 정규화합니다.

$$
\hat{A}=\tilde{D}^{-1/2}\tilde{A}\tilde{D}^{-1/2}
$$

이렇게 만든 <span markdown="0">\(\hat{A}\)</span>를 쓰면 GCN의 대표 식이 나옵니다.

$$
H^{(l+1)}=\sigma(\hat{A}H^{(l)}W^{(l)})
$$

이 식을 너무 어렵게 볼 필요는 없습니다. <span markdown="0">\(\hat{A}H^{(l)}\)</span>는 "정규화된 자기 자신 + 이웃 feature 섞기"이고, <span markdown="0">\(W^{(l)}\)</span>는 "섞인 feature를 새 표현 공간으로 바꾸기"입니다. <span markdown="0">\(\sigma\)</span>는 ReLU 같은 활성화 함수입니다.

<figure class="diagram-figure">
  <iframe class="diagram-frame" src="/assets/diagrams/gnn-gcn-wired-communication-networks/gcn-layer-pipeline.html" title="GCN layer에서 node 축 집계와 feature 축 변환이 이어지는 순서"></iframe>
  <figcaption class="figure-caption">GCN 식은 message passing을 행렬곱으로 압축한 표기입니다. 먼저 node 축에서 이웃을 섞고, 그다음 feature 축에서 표현을 바꿉니다.</figcaption>
</figure>

여기까지 오면 "GCN에도 aggregation이 들어가나?"라는 질문에는 분명히 답할 수 있습니다. 들어갑니다. 오히려 GCN의 핵심이 aggregation입니다. 다만 이 aggregation을 <span markdown="0">\(\hat{A}H\)</span>라는 행렬곱으로 깔끔하게 쓴 것뿐이에요.

## 4. W는 차원보다 의미를 바꿉니다

두 번째로 많이 헷갈렸던 지점은 <span markdown="0">\(W\)</span>였습니다. "이웃을 섞는 게 목적이면 평균만 내면 되지, 왜 굳이 <span markdown="0">\(W\)</span>로 다른 차원으로 보내야 하나?"라는 질문입니다.

결론부터 말하면, <span markdown="0">\(\hat{A}H\)</span>는 정보를 모으는 단계이고 <span markdown="0">\(W\)</span>는 그 정보를 문제에 맞는 의미로 다시 조합하는 단계입니다. 통신망 node feature가 `traffic`과 `error rate` 두 개라고 해봅시다. 이웃 평균을 내면 주변 traffic과 error rate가 섞인 숫자는 얻습니다. 하지만 실제로 알고 싶은 것은 단순 평균이 아닐 수 있어요.

- 트래픽 대비 에러가 비정상적으로 큰가
- 정상 고트래픽과 장애성 고트래픽을 구분할 수 있는가
- 이웃과 함께 혼잡 전조 패턴을 보이는가
- 특정 링크 장애가 주변 노드 표현에 어떻게 퍼지는가

이런 질문은 원래 feature를 그대로 평균내는 것만으로는 부족합니다. <span markdown="0">\(W\)</span>는 기존 feature들을 다른 비율로 조합해 hidden feature를 만듭니다. 사람이 미리 `congestion risk`나 `failure precursor`라는 열을 만들어 넣지 않아도, 학습 과정에서 문제를 잘 푸는 조합을 찾게 하는 장치입니다.

수식의 shape로 보면 역할이 더 분명합니다.

$$
H^{(l)}\in\mathbb{R}^{N\times d},
\quad
W^{(l)}\in\mathbb{R}^{d\times d'},
\quad
H^{(l)}W^{(l)}\in\mathbb{R}^{N\times d'}
$$

노드 수 <span markdown="0">\(N\)</span>은 그대로 남고, feature 차원만 <span markdown="0">\(d\)</span>에서 <span markdown="0">\(d'\)</span>로 바뀝니다. 예시에서 2차원을 4차원으로 보내는 것은 하나의 설명일 뿐입니다. 실제로는 더 크게 만들 수도, 더 작게 압축할 수도, 같은 크기를 유지할 수도 있습니다.

| 변환 | 언제 쓰기 쉬운가 | 직관 |
| --- | --- | --- |
| 2 -> 8 | 입력 feature가 너무 단순할 때 | 숨은 패턴을 더 풍부하게 표현 |
| 100 -> 16 | 원래 feature가 많거나 노이즈가 클 때 | 요약 embedding으로 압축 |
| 32 -> 32 | 크기는 충분하지만 조합을 바꾸고 싶을 때 | 같은 크기의 표현 공간을 재정렬 |

Q&A에서 썼던 <span markdown="0">\(hW\)</span> 예시는 한 노드만 떼어 본 경우입니다. 예를 들어 한 노드의 feature가 <span markdown="0">\(h=[10,2]\)</span>라면, 이것은 전체 행렬 <span markdown="0">\(H\)</span>의 한 행입니다. 실제 GCN에서는 전체 노드를 한꺼번에 씁니다.

$$
H=
\begin{bmatrix}
10&2\\
7&1\\
4&3
\end{bmatrix},
\quad
W=
\begin{bmatrix}
1&0&1&-1\\
0&1&2&1
\end{bmatrix}
$$

여기서 <span markdown="0">\(H\)</span>는 <span markdown="0">\(3\times2\)</span>이고, <span markdown="0">\(W\)</span>는 <span markdown="0">\(2\times4\)</span>입니다. 결과 <span markdown="0">\(HW\)</span>는 <span markdown="0">\(3\times4\)</span>가 됩니다. 3개 노드는 그대로이고, 각 노드의 feature만 2개에서 4개로 바뀌는 거예요.

이제 "왜 <span markdown="0">\(W\)</span>가 뒤에 붙나"도 shape로 읽을 수 있습니다. 선형대수 교재에서 벡터를 열벡터로 두면 <span markdown="0">\(Wx\)</span>가 자연스럽습니다. 하지만 GCN 설명에서는 한 노드를 행벡터로 두고, 전체 노드를 <span markdown="0">\(H\in\mathbb{R}^{N\times d}\)</span>로 쌓는 convention을 자주 씁니다. 이 convention에서는 feature 변환이 <span markdown="0">\(HW\)</span>입니다.

<div class="notice--warning" markdown="1">

**헷갈리기 쉬운 표기**

- 열벡터 convention에서는 <span markdown="0">\(Wx\)</span>가 자연스럽습니다.
- 행벡터 convention에서는 <span markdown="0">\(xW\)</span>가 자연스럽습니다.
- GCN에서는 전체 노드 feature를 <span markdown="0">\(N\times d\)</span> 행렬로 두는 경우가 많아서 <span markdown="0">\(HW\)</span>가 자주 나옵니다.

</div>

여기서 한 걸음 더 가면 <span markdown="0">\(\hat{A}HW\)</span>와 <span markdown="0">\(HWA\)</span>의 차이도 보입니다. <span markdown="0">\(\hat{A}\)</span>는 node-to-node 관계를 담은 행렬입니다. 그래서 왼쪽에서 곱해 node 축에 작용해야 합니다. <span markdown="0">\(W\)</span>는 feature-to-feature 변환이므로 오른쪽에서 곱해 feature 축에 작용합니다.

| 곱 | 작용하는 축 | 의미 |
| --- | --- | --- |
| <span markdown="0">\(\hat{A}H\)</span> | node 축 | graph topology를 따라 이웃 node 정보를 섞음 |
| <span markdown="0">\(HW\)</span> | feature 축 | 각 node의 feature vector를 새 표현 공간으로 변환 |
| <span markdown="0">\(\hat{A}HW\)</span> | node 축 다음 feature 축 | 이웃 집계와 feature 변환을 함께 수행 |
| <span markdown="0">\(HWA\)</span> | 보통 의미와 차원이 어긋남 | adjacency를 feature 변환 뒤 오른쪽에 붙여 GCN 집계로 읽기 어려움 |

다만 <span markdown="0">\((\hat{A}H)W\)</span>와 <span markdown="0">\(\hat{A}(HW)\)</span>는 별개로 봐야 합니다. 차원이 맞으면 행렬 곱의 결합법칙 때문에 수학적 결과는 같습니다. 하지만 설명할 때는 <span markdown="0">\(\hat{A}H\)</span>를 "이웃과 섞기", <span markdown="0">\(HW\)</span>를 "feature 바꾸기"로 분리해 읽는 편이 훨씬 덜 헷갈립니다.

## 5. 다음 모델은 집계 방식을 바꿔 읽습니다

GCN을 여기까지 읽으면 GAT과 GraphSAGE도 덜 낯설어집니다. 둘 다 GNN의 message passing 틀에서 출발하지만, "이웃을 어떻게 고르고 얼마나 반영할 것인가"를 다르게 설계합니다.

GCN은 정규화된 adjacency를 쓰기 때문에 이웃의 가중치가 graph degree에서 나옵니다. 반면 그래프 어텐션 네트워크 (Graph Attention Network, GAT)는 attention weight를 학습해 중요한 이웃에 더 큰 가중치를 줍니다.<sup><a href="#src-1">[1]</a></sup> 그래서 GCN을 "정규화된 이웃 평균"에 가깝게 기억한다면, GAT은 "이웃별 중요도를 학습하는 집계"로 넘어갈 수 있습니다.

GraphSAGE도 완전히 다른 철학은 아닙니다. GraphSAGE는 local neighborhood feature를 aggregate하는 함수 자체를 학습하고, 모든 이웃을 다 보지 않고 sampling을 사용합니다. 그래서 seen node만 외우는 transductive setting보다, 새 node가 들어와도 주변 feature를 모아 embedding을 만들 수 있는 inductive setting에 더 잘 맞습니다. GraphSAGE를 공부하기 전에 GCN을 봐야 하는 이유는 여기에 있습니다. 먼저 "이웃 정보를 모아 node 표현을 갱신한다"는 뼈대가 잡혀야 sampling과 aggregation 함수의 의미가 보입니다.

하지만 논문은 GNN을 장점만 있는 도구로 마무리하지 않습니다. 공개 학습 데이터가 부족하고, 많은 연구가 100개 미만 node 수준의 작은 topology에 머물렀으며, 실제 대규모 네트워크로 가려면 graph partitioning과 parallel computing이 필요할 수 있다고 봅니다.<sup><a href="#src-1">[1]</a></sup> GCN layer를 너무 깊게 쌓으면 node 표현이 서로 비슷해지는 over-smoothing도 문제입니다.<sup><a href="#src-1">[1]</a></sup>

통신망에서는 안정성도 따로 봐야 합니다. link failure, congestion, targeted attack 같은 perturbation이 실제로 생기기 때문입니다. routing이나 resource allocation에 모델 예측을 연결하려면, 운영자가 왜 그런 판단이 나왔는지 설명할 수 있어야 합니다. 그러니 이 논문을 읽고 남길 결론은 "GNN을 쓰자"가 아니라 "그래프 구조를 모델에 넣을 수 있지만, 운영망에서는 데이터, 규모, 안정성, 설명가능성을 같이 검증해야 한다"에 가깝습니다.

## 마무리

이번에 Q&A를 길게 쌓으면서 글의 중심이 바뀌었습니다. 처음에는 Jiang의 서베이를 유선 네트워크 적용 사례 중심으로 읽으려 했지만, 실제로 오래 남은 질문은 <span markdown="0">\(\hat{A}H W\)</span>가 무슨 일을 하는지였습니다. 이제는 이 식을 "node 축에서 이웃과 섞고, feature 축에서 의미를 바꾼다"로 읽을 수 있습니다.

이 관점으로 다시 보면 통신망 GNN도 조금 덜 추상적입니다. 유선망의 라우터와 링크, traffic matrix와 routing scheme은 <span markdown="0">\(H\)</span>와 <span markdown="0">\(\hat{A}\)</span>가 되고, 예측하려는 delay, traffic, FCT, security signal은 운영 판단으로 넘어갈 후보가 됩니다. 다음에 이어서 본다면 RouteNet이나 SGCRN 같은 모델 하나를 잡고, 실제로 topology와 traffic이 어떤 입력 텐서로 들어가고 어떤 운영 지표로 나오는지 더 좁게 추적하는 편이 좋겠습니다.

## 출처

<span id="src-1"></span>[1] Weiwei Jiang, Graph-based Deep Learning for Communication Networks: A Survey, Computer Communications, 2022, <a href="https://doi.org/10.1016/j.comcom.2021.12.015" target="_blank" rel="noopener noreferrer">[원문보기]</a>
