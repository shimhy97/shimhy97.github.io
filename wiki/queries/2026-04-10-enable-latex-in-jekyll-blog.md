---
title: "Jekyll 블로그에 MathJax를 붙여 $...$, $$...$$ 수식을 렌더링하기"
type: query
status: filed
created_at: 2026-04-10
updated_at: 2026-04-10
source_count: 0
tags:
  - blog
  - jekyll
  - latex
  - mathjax
---

# 질문

Jekyll 블로그에 MathJax를 붙여 `$...$`, `$$...$$` 수식을 렌더링하기

## 결론

- 이 블로그는 기본 상태에서 LaTeX 렌더링이 꺼져 있었고, `_config.yml`에는 `kramdown`만 설정되어 있었으며 `_includes/head/custom.html`에는 `mermaid`만 로드되고 있었다.
- 전역 head include에 MathJax 3 설정과 CDN 스크립트를 추가해 `$...$`, `$$...$$`, `\(...\)`, `\[...\]` 문법을 렌더링하도록 설정했다.
- `skipHtmlTags`에 `pre`, `code`를 넣어 코드 블록 안 문자열은 수식으로 잘못 처리하지 않게 막았다.
- 실제 적용 예시는 `_posts/2026-04-09-melu-few-shot-cold-start-recommendation.md`에서 기존 `text` 코드 블록 수식을 MathJax 문법으로 바꿔 두었다.
- 시스템 기본 Ruby 2.6에서는 `bundler 4.0.9`를 직접 설치할 수 없었지만, 이 레포의 `.ruby-version`이 가리키는 `rbenv` Ruby 3.2.4 환경에는 `bundler 4.0.9`가 이미 준비돼 있었다.
- `rbenv exec bundle exec jekyll doctor`는 통과했고, `rbenv exec bundle exec jekyll build`도 성공했다.
- 생성된 `_site/machine-learning/recommender-systems/melu-few-shot-cold-start-recommendation/index.html`에서 MathJax CDN 스크립트와 수식 마크업이 실제로 출력되는 것을 확인했다.

## 근거 페이지

- [../../_includes/head/custom.html](/Users/shimhy97/shimhy97-github.io/_includes/head/custom.html)
- [../../_config.yml](/Users/shimhy97/shimhy97-github.io/_config.yml)
- [../../_posts/2026-04-09-melu-few-shot-cold-start-recommendation.md](/Users/shimhy97/shimhy97-github.io/_posts/2026-04-09-melu-few-shot-cold-start-recommendation.md)

## 후속 액션

- 수식이 많은 글이 늘어날 경우, 공통 사용 규칙을 `wiki/topics/` 또는 `docs/`에 별도 스타일 가이드로 승격할 수 있다.
- 필요하면 `rbenv exec bundle exec jekyll serve`를 표준 미리보기 명령으로 위키에 추가 문서화할 수 있다.

## 블로그 글로의 확장 가능성

- 수식이 많은 머신러닝 논문 리뷰를 자주 쓸 예정이라면, 블로그 운영 메모로 끝내지 말고 "Jekyll 블로그에 MathJax 붙이기" 자체를 짧은 기술 글로 확장할 수 있다.
