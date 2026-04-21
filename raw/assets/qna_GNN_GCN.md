좋습니다.
이 두 질문은 **GNN → GCN으로 넘어갈 때 가장 중요한 핵심**입니다.

둘 다 정확한 의문입니다.

---

# 1. “GNN의 한 종류가 GCN”이면, 그 일반식이 어떻게 GCN으로 이어지나?

먼저 일반 GNN의 메시지 패싱 식을 다시 보겠습니다.

[
m_i^{(t)}=\sum_{j\in N(i)} M^{(t)}\big(X_i^{(t-1)},X_j^{(t-1)},e_{ij}\big)
]

[
X_i^{(t)}=U^{(t)}\big(X_i^{(t-1)},m_i^{(t)}\big)
]

이건 서베이 논문이 MPNN 형태로 설명한 **가장 일반적인 틀**입니다. 즉, “이웃에서 메시지를 모으고, 그걸로 내 상태를 업데이트한다”는 큰 골격입니다. 

GCN은 이 일반식에서 **메시지 함수 (M)** 와 **업데이트 함수 (U)** 를 아주 단순하고 깔끔하게 고른 특수한 경우라고 보면 됩니다. 서베이 논문도 GCN을 그래프 convolution의 대표적 형태로 소개하면서, 최종적으로는 정규화된 adjacency와 가중치 행렬을 곱하는 형태로 씁니다. 

즉 구조적으로는:

* **GNN 일반형**: 메시지 함수, 집계 방식, 업데이트 함수를 자유롭게 설계
* **GCN**: 그 자유도를 줄이고 “정규화된 이웃 평균 + 선형변환”으로 고정

입니다.

---

## 1-1. GNN 일반식을 아주 단순화해 보자

GCN으로 가려면 일반식에서 선택을 해야 합니다.

가장 단순하게 다음처럼 정해봅시다.

### 메시지 함수

이웃 (j)가 보내는 메시지를 그냥 자기 feature라고 두겠습니다.

[
M^{(t)}(X_i,X_j,e_{ij}) = X_j
]

그러면 메시지 합은

[
m_i^{(t)}=\sum_{j\in N(i)} X_j^{(t-1)}
]

이 됩니다.

즉 “이웃들의 feature를 그냥 더한다”입니다.

### 업데이트 함수

그다음 내 자신의 feature도 같이 반영하고 싶으니,

[
X_i^{(t)} = \sigma\left(W^{(t)}\Big(X_i^{(t-1)} + \sum_{j\in N(i)}X_j^{(t-1)}\Big)\right)
]

처럼 둘 수 있습니다.

이건 말로 하면:

> 자기 자신 + 이웃들의 정보를 합친 뒤,
> 가중치 (W)를 통해 새 표현으로 바꾸고,
> 활성화 함수 (\sigma)를 통과시킨다.

이제 이미 GCN 느낌이 많이 납니다.

---

## 1-2. self-loop를 넣으면 “자기 자신도 이웃”이 된다

GCN에서는 보통 self-loop를 넣습니다.

즉 원래 adjacency (A)에 항등행렬 (I)를 더해서

[
\tilde A = A + I
]

로 둡니다. 서베이 논문도 GCN 식에서 self-loop가 추가된 (\tilde A)를 사용한다고 설명합니다. 

그럼 “자기 자신 + 이웃의 합”을 따로 쓸 필요 없이

[
\sum_{j\in N(i)\cup {i}} X_j
]

처럼 쓸 수 있습니다.

즉 일반 GNN 식이

* 원래는 “자기 자신”과 “이웃”을 따로 다룰 수도 있었는데
* GCN에서는 self-loop를 넣어서 **하나로 합친 것**

입니다.

---

## 1-3. 그런데 그냥 더하면 문제가 생긴다

여기서 한 가지 문제가 있습니다.

이웃이 많은 노드는 값이 너무 커집니다.

예를 들어:

* 노드 A는 이웃 2개
* 노드 B는 이웃 100개

이면, 그냥 합(sum)을 쓰면 B 쪽 값이 훨씬 커지기 쉽습니다.

그래서 GCN은 degree 정규화를 넣습니다.

서베이 논문은 GCN의 정규화된 convolution을 다음처럼 씁니다.

[
X *_G = W\left(\tilde D^{-1/2}\tilde A \tilde D^{-1/2}\right)X
]

혹은 같은 의미로 보통

[
H^{(l+1)}=\sigma\left(\hat A H^{(l)}W^{(l)}\right)
]

라고 많이 씁니다. 여기서

[
\hat A=\tilde D^{-1/2}\tilde A \tilde D^{-1/2}
]

입니다. 

즉 GCN은 일반 메시지 패싱에서

1. 메시지는 이웃 feature 자체
2. aggregation은 정규화된 합
3. update는 선형변환 + 활성화

로 정한 경우입니다.

---

## 1-4. 일반식과 GCN 식을 1:1로 대응시키면

일반식:

[
m_i^{(t)}=\sum_{j\in N(i)} M^{(t)}(\cdot)
]

[
X_i^{(t)}=U^{(t)}(\cdot)
]

GCN에서는 이걸 사실상 이렇게 볼 수 있습니다.

### 메시지

이웃 (j)가 (i)에게 보내는 메시지:

[
M_{GCN}^{(t)}(i,j)=\hat A_{ij} H_j^{(l)}
]

즉 “이웃 feature”에다가 **정규화 weight (\hat A_{ij})** 를 곱해서 보낸다고 생각할 수 있습니다.

### aggregation

그 메시지를 모두 더하면

[
m_i^{(t)}=\sum_j \hat A_{ij} H_j^{(l)}
]

입니다.

### update

그다음 선형변환과 활성화를 하면

[
H_i^{(l+1)}=\sigma\left(m_i^{(t)}W^{(l)}\right)
]

가 됩니다.

이걸 전체 노드에 대해 행렬로 한 번에 쓰면

[
H^{(l+1)}=\sigma\left(\hat A H^{(l)} W^{(l)}\right)
]

가 됩니다.

즉 GCN도 분명히 aggregation이 들어갑니다.
오히려 GCN의 핵심도 aggregation입니다. 다만 GCN은 그 aggregation을 **정규화된 adjacency 행렬 곱**으로 매우 깔끔하게 쓴 것입니다. 

---

# 2. “GCN에서 (H^{(l+1)} = \sigma(AH^{(l)}W^{(l)}))인데, 왜 (W)가 뒤에 있나? 선형변환이면 (WX) 아닌가?”

이 질문도 정말 좋습니다.

결론부터 말하면:

**둘 다 가능합니다.**
다만 **벡터를 행(row)로 쓰느냐, 열(column)로 쓰느냐에 따라 표기법이 달라집니다.**

즉,

* **열벡터 convention**이면 (Wx)
* **행벡터 convention**이면 (xW)

가 됩니다.

GCN 교재와 논문에서는 보통 **노드 하나를 행(row)** 으로 두고, 전체 노드 feature를

[
H \in \mathbb{R}^{N\times d}
]

형태로 씁니다.

여기서:

* (N): 노드 수
* (d): feature 차원

즉 **한 행이 한 노드의 feature** 입니다.

이 convention에서는 feature 변환이

[
HW
]

가 맞습니다.

---

## 2-1. 왜 (HW)가 맞는지 shape로 보면 바로 보인다

GCN에서 보통

[
H^{(l)} \in \mathbb{R}^{N\times d}
]

[
W^{(l)} \in \mathbb{R}^{d\times d'}
]

입니다.

그러면

[
H^{(l)}W^{(l)} \in \mathbb{R}^{N\times d'}
]

가 됩니다.

즉:

* 노드 수 (N)은 그대로 유지
* feature 차원만 (d \to d')로 바뀜

이건 우리가 원하는 exactly 그 동작입니다.

반대로 (WH)를 하려면

[
W^{(l)}H^{(l)}
]

의 shape가 맞아야 하는데,

[
(d\times d') (N\times d)
]

는 일반적으로 곱셈이 안 됩니다.

즉 지금 이 표기에서는 (WH)가 차원상 성립하지 않습니다.

---

## 2-2. “선형변환이면 보통 (Wx) 아닌가?”가 맞는 이유

네가 익숙한 선형대수에서는 보통 벡터를 **열벡터**로 씁니다.

예를 들어 feature 2개짜리 벡터를

[
x=
\begin{bmatrix}
x_1\
x_2
\end{bmatrix}
\in \mathbb{R}^{2\times 1}
]

처럼 씁니다.

이 경우 선형변환은

[
Wx
]

입니다.

예를 들어

[
W\in\mathbb{R}^{4\times 2}
]

이면

[
Wx \in \mathbb{R}^{4\times 1}
]

이 되어 2차원을 4차원으로 보냅니다.

이건 완전히 맞는 표기입니다.

---

## 2-3. 그런데 GCN에서는 노드 feature를 행으로 쓴다

GCN에서는 전체 노드를 한 번에 행렬로 처리하려고, 보통 각 노드를 **행벡터**로 둡니다.

즉 한 노드 feature를

[
h_i=
\begin{bmatrix}
x_1 & x_2
\end{bmatrix}
\in \mathbb{R}^{1\times 2}
]

처럼 씁니다.

이 경우 선형변환은

[
h_iW
]

가 됩니다.

예를 들어

[
W\in\mathbb{R}^{2\times 4}
]

이면

[
h_iW \in \mathbb{R}^{1\times 4}
]

가 됩니다.

즉 같은 선형변환인데:

* 열벡터로 쓰면 (Wx)
* 행벡터로 쓰면 (xW)

입니다.

둘은 convention 차이입니다.

---

## 2-4. 아주 쉬운 숫자 예시

### 열벡터 방식

[
x=
\begin{bmatrix}
10\
2
\end{bmatrix},
\quad
W=
\begin{bmatrix}
1 & 0\
0 & 1\
1 & 2\
-1 & 1
\end{bmatrix}
]

그러면

[
Wx=
\begin{bmatrix}
10\
2\
14\
-8
\end{bmatrix}
]

입니다.

### 행벡터 방식

같은 정보를 행벡터로 쓰면

[
h=
\begin{bmatrix}
10 & 2
\end{bmatrix}
]

이고, 가중치는 전치된 모양으로 써서

[
W'=
\begin{bmatrix}
1 & 0 & 1 & -1\
0 & 1 & 2 & 1
\end{bmatrix}
]

입니다.

그러면

[
hW'=
\begin{bmatrix}
10 & 2 & 14 & -8
\end{bmatrix}
]

입니다.

결과는 같습니다.
단지 벡터를 세로로 썼냐 가로로 썼냐의 차이입니다.

---

# 3. 그럼 GCN에서 (AHW)와 (HWA)의 차이도 있나?

네. 순서가 중요합니다.

GCN의 핵심은

[
\hat A H
]

가 먼저 **이웃 aggregation** 을 하고,

그 다음

[
(\hat A H)W
]

가 feature 변환을 하는 것입니다.

즉:

1. (\hat A H): 그래프 구조를 따라 이웃 정보를 섞는다
2. (W): 섞인 feature를 새로운 공간으로 바꾼다

입니다.

이 순서는 차원상도 자연스럽고 의미상도 자연스럽습니다.

서베이 논문도 GCN을 adjacency 기반 집계와 learnable weight matrix를 결합한 형태로 설명합니다. 

---

## 3-1. 그런데 (AHW)와 (HWA)는 왜 다르냐

왜냐하면:

* (A)는 **노드와 노드 사이 관계**를 다루는 행렬
* (W)는 **feature와 feature 사이 변환**을 다루는 행렬

이기 때문입니다.

즉 둘은 작용하는 축이 다릅니다.

* (A): 노드 축에 작용
* (W): feature 축에 작용

그래서 GCN에서는 보통

[
H \in \mathbb{R}^{N\times d}
]

에 대해

* 왼쪽에서 (A)를 곱해 노드끼리 섞고
* 오른쪽에서 (W)를 곱해 feature를 변환합니다

즉:

[
\hat A H W
]

는

* 왼쪽 곱: 행(노드) 방향 집계
* 오른쪽 곱: 열(feature) 방향 변환

입니다.

아주 예쁜 구조입니다.

---

# 4. 질문 1에 대한 짧은 요약

GCN은 GNN 일반식의 특수한 경우입니다.

일반 GNN:
[
\text{message} \to \text{aggregate} \to \text{update}
]

GCN:

* message = 이웃 feature
* aggregate = 정규화된 adjacency로 가중합
* update = 선형변환 + 활성화

그래서 행렬로 쓰면

[
H^{(l+1)}=\sigma(\hat A H^{(l)}W^{(l)})
]

가 됩니다. GCN에서도 aggregation은 분명히 들어가며, 그 aggregation이 바로 (\hat A H^{(l)}) 부분입니다. 

---

# 5. 질문 2에 대한 짧은 요약

“선형변환이면 왜 (WH)가 아니고 (HW)냐?”

→ **GCN에서는 노드 feature를 행(row)으로 쓴 convention이라서 (HW)가 맞습니다.**

* 열벡터 convention: (Wx)
* 행벡터 convention: (xW)

GCN은 전체 노드 행렬을

[
H\in\mathbb{R}^{N\times d}
]

로 쓰기 때문에

[
HW
]

가 자연스럽습니다.

---

# 6. 마지막 직관 한 줄

GCN 식

[
H^{(l+1)}=\sigma(\hat A H^{(l)}W^{(l)})
]

을 초보자용으로 해석하면 그냥 이겁니다.

[
\boxed{
\text{이웃과 섞는다} ;\rightarrow; \text{feature를 새로 바꾼다}
}
]

* (\hat A H^{(l)}): 이웃 aggregation
* (W^{(l)}): 선형변환
* (\sigma): 비선형성 추가

입니다.

다음으로 이어서 보면 가장 좋은 주제는
**“그렇다면 (\hat A H W)에서 (AH)를 먼저 하든 (HW)를 먼저 하든 결과가 같은가?”** 입니다.
이건 또 아주 중요한 포인트입니다.
