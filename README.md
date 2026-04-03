# Jekyll GitHub 기술 블로그 시작점

이 저장소는 **Jekyll + GitHub Actions Pages 배포 + Minimal Mistakes** 조합으로 시작하는 기술 블로그 기본 골격입니다.

데이터사이언티스트가 기술 글을 자주 올린다는 전제를 두고, 다음을 먼저 세팅했습니다.

- GitHub Actions 기반 Pages 배포 설정
- 많이 쓰는 블로그 테마인 `Minimal Mistakes` gem 구성
- 글 목록, 태그, 카테고리, 소개 페이지
- GitHub Actions 기반 Pages 배포 워크플로
- 프로젝트 내부 `scripts/ralph` 구조와 `prd.json`, `progress.txt`, `tasks/` 기반 Ralph 루프 시작점

## 먼저 알아둘 점

GitHub 사용자 블로그로 운영하려면 **GitHub 저장소 이름이 반드시 `shimhy97.github.io`** 여야 합니다.

지금 로컬 폴더 이름은 `/Users/shimhy97/shimhy97-github.io` 이지만, 실제 GitHub 원격 저장소는 아래처럼 만드는 것을 권장합니다.

```text
shimhy97/shimhy97.github.io
```

그렇지 않으면 사용자 루트 블로그가 아니라 프로젝트 사이트처럼 동작할 수 있습니다.

## 현재 프로젝트 구조

```text
.
├── .github/workflows/pages.yml
├── _config.yml
├── _data/navigation.yml
├── _pages/
├── _posts/
├── assets/css/main.scss
├── scripts/
├── tasks/
├── prd.json
└── progress.txt
```

## 왜 이 테마를 골랐는가

이번 시작점은 `Minimal Mistakes`를 기준으로 잡았습니다.

- Jekyll 기술 블로그에서 매우 널리 쓰입니다.
- 글 중심 구조라서 분석/기술 포스트와 잘 맞습니다.
- GitHub Actions로 빌드하기 때문에 로컬과 배포 환경을 더 일관되게 맞출 수 있습니다.
- 태그, 카테고리, 목차, SEO 같은 기본 요소가 이미 정리돼 있습니다.

나중에 디자인을 더 공격적으로 바꾸고 싶으면 `Chirpy` 같은 테마로 옮길 수 있지만, **처음 시작할 때는 배포와 글 작성 흐름이 단순한 쪽이 유리**합니다.

## 로컬 개발 환경 세팅

시스템 Ruby는 기본 제공 버전이 오래된 경우가 많기 때문에, 이 저장소는 **`rbenv` 기반 프로젝트 전용 Ruby**를 전제로 합니다.

### 1. 필수 도구 설치

```bash
brew install rbenv ruby-build jq
```

### 2. zsh에 rbenv 초기화 추가

`~/.zshrc`에 아래 한 줄을 넣습니다.

```bash
eval "$(rbenv init - zsh)"
```

적용:

```bash
source ~/.zshrc
```

### 3. 프로젝트 Ruby 설치

```bash
rbenv install 3.2.4
rbenv local 3.2.4
```

이 저장소에는 이미 `.ruby-version`이 들어 있으므로, `rbenv`가 잡히면 자동으로 `3.2.4`를 사용합니다.

### 4. Bundler와 gem 설치

```bash
gem install bundler
bundle install
```

### 5. 로컬 서버 실행

```bash
./scripts/blog-serve.sh
```

브라우저에서 아래 주소를 열면 됩니다.

```text
http://127.0.0.1:4000
```

## 글 작성 방법

새 글은 `_posts/` 아래에 아래 형식으로 추가합니다.

```text
YYYY-MM-DD-your-post-title.md
```

예시:

```text
_posts/2026-04-04-ab-test-design-notes.md
```

최소 front matter 예시는 아래처럼 시작하면 됩니다.

```markdown
---
title: "A/B 테스트 설계 메모"
date: 2026-04-04 09:00:00 +0900
categories:
  - experiment
tags:
  - ab-test
  - statistics
excerpt: "실무에서 자주 놓치는 실험 설계 포인트를 정리합니다."
---
```

## 배포 방법

이 저장소에는 GitHub Pages용 Actions 워크플로가 이미 들어 있습니다.

GitHub에서 해야 할 일은 다음입니다.

1. 저장소를 `shimhy97.github.io` 이름으로 만든다.
2. 이 로컬 저장소를 원격과 연결한다.
3. `main` 브랜치에 push 한다.
4. GitHub 저장소의 Pages 설정에서 **GitHub Actions**를 배포 소스로 선택한다.

그러면 push할 때마다 `.github/workflows/pages.yml`이 사이트를 빌드하고 배포합니다.

## Ralph Loop 세팅

이번 저장소는 Ralph를 **프로젝트 내부에 두는 방식**으로 시작합니다.

```text
scripts/ralph/ralph.sh
scripts/ralph/prompt.md
scripts/ralph/CLAUDE.md
tasks/
prd.json
progress.txt
```

### 왜 이렇게 두었는가

- 작업 대상 저장소 안에서 PRD와 진행 로그를 같이 관리하기 쉽습니다.
- Git 이력과 함께 남아서 반복 작업 흐름을 추적하기 쉽습니다.
- 블로그 구조를 바꾸거나 새 기능을 붙일 때, Ralph가 현재 저장소 맥락을 바로 읽을 수 있습니다.

### 이번 저장소 기준 Ralph 품질 체크

Ralph 프롬프트에는 이 프로젝트 기본 품질 체크를 아래처럼 잡아두었습니다.

```bash
./scripts/blog-build.sh
```

즉 UI든 글이든 설정이든, 기본적으로 **빌드가 깨지지 않는지**를 확인하는 흐름입니다.

### Ralph 사용 흐름

1. `tasks/prd-*.md`에 작업 PRD를 만든다.
2. PRD를 `prd.json`으로 정리한다.
3. `progress.txt`에 누적 맥락을 남긴다.
4. `scripts/ralph/ralph.sh`로 반복 실행한다.

현재는 **블로그 V1 후속 작업용 예시 PRD**가 `tasks/prd-blog-launch-v1.md`와 `prd.json`으로 들어 있습니다.

### 실행 전 전제조건

```bash
brew install jq
```

그리고 Ralph 공식 루프는 보통 `claude` 또는 `amp` 실행기를 전제로 사용합니다. 이 저장소의 `ralph.sh`도 같은 흐름을 따르되, `prd.json`과 `progress.txt` 위치만 **프로젝트 루트 기준**으로 맞췄습니다.

## 자주 쓰는 명령

```bash
./scripts/blog-build.sh
./scripts/blog-serve.sh
./scripts/ralph/ralph.sh --tool claude 5
```

## 추천 다음 단계

초기 세팅 다음으로는 아래 순서를 권장합니다.

1. GitHub 원격 저장소를 `shimhy97.github.io`로 만든다.
2. 로컬 Ruby 환경을 `rbenv`로 맞춘다.
3. `bundle install` 후 `./scripts/blog-serve.sh`로 로컬 확인을 한다.
4. `About` 페이지와 author 정보를 본인 소개로 다듬는다.
5. 첫 번째 데이터사이언스 글을 한 편 올린다.
