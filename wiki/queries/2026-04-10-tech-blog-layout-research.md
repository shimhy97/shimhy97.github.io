---
title: "기술 블로그를 덜 빽빽하게 만드는 게시 형식 조사"
type: query
status: filed
created_at: 2026-04-10
updated_at: 2026-04-10
source_count: 11
tags:
  - blog
  - jekyll
  - layout
  - content-design
  - editorial-design
---

# 질문

기술 블로그에서 글이 너무 빽빽해 보이지 않게 하려면, 다른 엔지니어링 블로그들은 게시 형식을 어떻게 설계하는가?

## 결론

- 상위권 기술 블로그들은 글을 "잘 쓰는" 문제와 "잘 보이게 배치하는" 문제를 분리해서 다룬다. 본문 문장력과 별개로, 요약 박스, in-page navigation, 그림과 캡션, 시각적 구획, 메타데이터, 관련 글 연결을 템플릿 수준에서 관리한다.
- 즉흥적인 볼드체 남발보다, 반복 가능한 콘텐츠 컴포넌트를 정해 두는 쪽이 일반적이다. 예를 들면 `TL;DR`, `In this article`, 아키텍처 다이어그램, 비교 표, 주의 박스, figure caption 같은 형식이다.
- 이건 실무에서 실제로 별도 역할로 다뤄진다. 흔히 `content design`, `editorial design`, `publication design`, `developer experience content`, `front-end system for publishing` 같은 이름으로 나뉜다.
- 이 저장소는 이미 `toc`, `toc_sticky`, `read_time`, `related`, `notice--primary`를 갖고 있어서 바닥 공사는 끝난 상태다. 현재의 답답함은 기능 부재보다, 모든 글을 거의 같은 리듬의 `H2 + 본문` 반복으로 쓰고 있다는 점에 더 가깝다.
- 특히 `_config.yml`의 `classes: wide` 기본값은 본문 폭을 넓혀 긴 문단이 더 빽빽하게 보이게 만들 수 있다. Minimal Mistakes 문서 기준으로 `wide`와 `toc`를 함께 쓰면 TOC가 우측 사이드가 아니라 본문 상단으로 들어가므로, 긴 글의 스캔성도 같이 떨어질 수 있다.

## 외부 사례에서 보인 공통 패턴

### 1. 긴 글일수록 초반에 요약 경로를 준다

- GitHub Engineering은 긴 글 상단에 `TL;DR`를 두는 관행을 명시적으로 언급한다. 빠르게 훑고 읽을지 말지 결정하게 해 주는 장치다.
- USWDS는 섹션이 3개 이상이거나 3개 화면 높이 이상인 긴 페이지에 in-page navigation이 큰 UX 개선을 준다고 안내한다.
- Thoughtworks / Martin Fowler 글은 본문 전에 `Contents`를 따로 두고 `H2/H3`를 노출해, 독자가 먼저 구조를 본 뒤 원하는 구간으로 진입하게 만든다.

### 2. 서술만 이어 가지 않고 시각적 멈춤점을 넣는다

- Vercel과 Cloudflare의 기술 글은 초반 lede 다음에 아키텍처 다이어그램이나 개념 비교 이미지를 넣고, 캡션으로 "이 그림을 왜 봐야 하는지"를 바로 붙인다.
- Cloudflare 글은 "Let’s dig in" 같은 전환 문장 앞에 큰 다이어그램을 배치해 독자의 인지 부담을 한 번 끊는다.
- Stripe의 Dev Blog는 목록 단계부터 요약, 주제 태그, 작성자, 읽기 링크를 분리해 두어 클릭 전 피로도를 낮춘다. 개별 글도 읽기 시간과 메타데이터를 강하게 노출한다.

### 3. 강조는 문장 내부가 아니라 박스와 캡션으로 처리한다

- GitHub, Stripe, Vercel, Cloudflare 계열 글은 핵심 문장을 온통 bold 처리하기보다, 별도 summary block, CTA block, note block, figure caption으로 정보 위계를 만든다.
- Atlassian Design System도 긴 글은 최소 16px 본문, 짧고 명확한 heading, 명확한 heading 크기 차이, 적절한 단락 간격 같은 typography 규칙을 별도 기준으로 다룬다.

### 4. 글쓰기와 게시 UI를 따로 설계한다

- Microsoft Design은 content designer가 이제 문구 보정 역할이 아니라, UX 디자이너·PM·엔지니어와 처음부터 함께 설계한다고 설명한다.
- 즉 "글을 쓰는 사람"과 "읽는 흐름을 설계하는 사람"이 분리되는 건 드문 일이 아니다. 기술 블로그에서도 같은 분리가 일어난다.

## 사례별 메모

### GitHub

- `TL;DR`를 빠른 스캔 장치로 쓴다.
- 긴 글이어도 상단에서 핵심 판단을 먼저 노출한다.
- 내부 글쓰기 원칙 자체에 "quick skimmability"가 들어가 있다.

### Vercel

- 제목 아래에 `카테고리 / 저자 / 읽기 시간 / 발행일 / 한 문장 deck`를 강하게 노출한다.
- 초반부에 결과 수치와 변화 요약을 먼저 준 뒤, 다이어그램으로 본론에 들어간다.
- 중간 CTA 블록이 본문 리듬을 끊어 주는 역할도 한다.

### Cloudflare

- 아키텍처 글에서 거의 항상 큰 그림과 캡션을 먼저 준다.
- 섹션 진입 전 다이어그램이 들어가서 "이제 구조를 보고 들어간다"는 신호가 분명하다.
- 깊은 기술 글이어도 이미지와 캡션이 단락 더미를 계속 분절한다.

### Stripe

- 글 목록 단계에서부터 `Summary`, `Topics`, `Author`를 구조화해 둔다.
- 독자는 제목만이 아니라 "이 글이 어떤 문제를 다루는지"를 짧게 파악하고 들어간다.
- 기술 글이 길더라도 메타데이터와 주제 태그가 먼저 보여서 난이도를 미리 가늠하게 만든다.

### Thoughtworks / Martin Fowler

- 긴 해설 글은 본문 전에 `Contents`를 분명히 노출한다.
- `H2/H3` 계층을 그대로 탐색 장치로 쓰며, 섹션 구조가 먼저 보인다.
- 다이어그램과 figure caption을 설명 단락 사이에 자주 끼워 넣는다.

## 이 블로그에 바로 적용할 수 있는 형식 레버

### 1. 글 맨 위에 요약 박스를 추가한다

- 2~4줄짜리 `이 글에서 볼 것` 박스를 두면 긴 글 진입 장벽이 크게 낮아진다.
- 형식은 `이번 글에서 볼 것`, `세 줄 요약`, `먼저 결론` 중 하나로 고정하는 편이 낫다.

### 2. 모든 섹션을 같은 길이로 쓰지 않는다

- 지금 글들은 `H2 + 문단 2~4개` 반복이 많아서 리듬이 단조롭다.
- 한 섹션쯤은 표, 한 섹션쯤은 그림, 한 섹션쯤은 짧은 bullet summary로 바꾸는 편이 훨씬 덜 피곤하다.

### 3. 논문 글은 그림과 표를 적극적으로 넣는다

- 논문 글은 원문 Figure, 실험 표, 개념도 한 장만 들어가도 피로도가 크게 줄어든다.
- 그림 아래에는 "이 그림에서 봐야 할 포인트"를 1문장 캡션으로 적는 게 중요하다.

### 4. 강조는 bold보다 notice box로 옮긴다

- 핵심 문장을 문장 내부 bold로 여러 번 때리는 것보다, `왜 중요한가`, `실무에서 볼 포인트`, `헷갈리기 쉬운 점` 같은 박스를 두는 편이 덜 소란스럽고 더 눈에 잘 들어온다.
- 이 저장소에는 이미 `notice--primary` 스타일이 있어서 바로 활용할 수 있다.

### 5. 긴 글은 본문 폭을 다시 본다

- `_config.yml` 기본값이 `classes: wide`라서 긴 문단이 한 줄에 많이 들어간다.
- 긴 기술 글만큼은 `wide`를 빼거나, 본문 `max-width`를 줄여 줄 길이를 줄이는 편이 낫다.
- TOC를 우측에 붙이고 싶다면 `wide` 기본값과의 충돌도 같이 점검해야 한다.

### 6. 글머리 구조를 "본문용"과 "스캔용"으로 이중화한다

- 본문 소제목은 지금처럼 서술형으로 유지하되, 각 섹션 첫 문장만큼은 짧고 단단하게 핵심을 먼저 말해 주면 스캔성이 올라간다.
- 예를 들어 섹션 첫 문장을 굵게 한 줄로 두고, 그 아래 설명을 붙이는 방식이 가능하다.

## 현재 레포에서 확인한 관련 상태

- [`_config.yml`](/Users/shimhy97/shimhy97-github.io/_config.yml): posts 기본값으로 `read_time`, `related`, `toc`, `toc_sticky`, `classes: wide`가 켜져 있다.
- [`assets/css/main.scss`](/Users/shimhy97/shimhy97-github.io/assets/css/main.scss): `notice--primary` 좌측 강조선 스타일이 이미 있다.
- [`_posts/2026-04-06-build-your-blog-as-an-llm-wiki.md`](/Users/shimhy97/shimhy97-github.io/_posts/2026-04-06-build-your-blog-as-an-llm-wiki.md): 서술은 좋지만 `H2 + 단락` 중심이라 시각적 멈춤점이 많지 않다.
- [`_posts/2026-04-09-melu-few-shot-cold-start-recommendation.md`](/Users/shimhy97/shimhy97-github.io/_posts/2026-04-09-melu-few-shot-cold-start-recommendation.md): 수식은 좋아졌지만 figure, summary box, 비교 표를 더 넣을 여지가 크다.

## 후속 액션

- 긴 글용 front matter 프리셋을 하나 정한다. 예: `summary_box`, `hero_figure`, `show_toc_aside`.
- `notice`, `figure`, `caption`, `table`, `summary box`를 글 템플릿 수준에서 재사용 가능하게 정리한다.
- `classes: wide` 기본값을 유지할지, 긴 글에서만 해제할지 결정한다.
- 논문 리뷰 글 템플릿에는 최소 1개 figure와 1개 요약 표를 넣는 규칙을 둘 수 있다.

## 블로그 글로의 확장 가능성

- 이 메모는 단순 운영 참고를 넘어서, `기술 블로그는 글쓰기만이 아니라 게시 형식도 설계해야 한다`는 주제로 확장 가능하다.
- 발행한다면 "왜 엔지니어링 블로그는 덜 빽빽해 보이는가" 같은 제목으로, 실제 사례와 현재 블로그 개선안을 함께 묶는 형식이 적절하다.

## 참고 자료

- [GitHub Engineering: How to communicate like a GitHub engineer](https://github.blog/engineering/engineering-principles/how-to-communicate-like-a-github-engineer-our-principles-practices-and-tools/)
- [GitHub Blog: How to build reliable AI workflows with agentic primitives and context engineering](https://github.blog/ai-and-ml/how-to-build-reliable-ai-workflows-with-agentic-primitives-and-context-engineering/)
- [Vercel: How Vercel adopted microfrontends](https://vercel.com/blog/how-vercel-adopted-microfrontends)
- [Cloudflare: How we built it: the technology behind Cloudflare Radar 2.0](https://blog.cloudflare.com/technology-behind-radar2/)
- [Cloudflare: Building Cloudflare on Cloudflare](https://blog.cloudflare.com/building-cloudflare-on-cloudflare/)
- [Stripe Dev Blog](https://stripe.dev/blog)
- [USWDS: In-page navigation](https://designsystem.digital.gov/components/in-page-navigation/)
- [Atlassian Design: Applying typography](https://atlassian.design/foundations/typography/applying-typography/)
- [Microsoft Design: Content Designers: The unsung heroes of design](https://microsoft.design/articles/content-designers-the-unsung-heroes-of-design/)
- [Minimal Mistakes: Layouts](https://mmistakes.github.io/minimal-mistakes/docs/layouts/)
- [Minimal Mistakes: Helpers](https://mmistakes.github.io/minimal-mistakes/docs/helpers/)
