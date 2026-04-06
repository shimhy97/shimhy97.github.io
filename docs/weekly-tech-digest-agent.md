# 주간 최신 기술 다이제스트 에이전트

## 문서 목적

이 문서는 이 저장소에서 운영하려는 "주간 최신 기술 다이제스트" 업무의 목적, 범위, 운영 원칙을 설명한다. 목표는 최신 개발 기술 소식을 넓게 주워 담는 것이 아니라, 공식성과 실무 가치가 높은 신호만 모아 한국어 다이제스트 글로 꾸준히 발행하는 것이다.

## 해결하려는 문제

- 최신 개발 기술 소식은 소스가 너무 많아 사람이 매주 직접 추적하기 어렵다.
- 블로그 운영자가 매번 검색과 정리에 시간을 많이 쓰면 발행 주기가 끊어진다.
- 마케팅성 글과 실질적인 기술 변경 사항이 섞여 있어 자동 수집 품질이 쉽게 흔들린다.

이 프로젝트는 위 문제를 줄이기 위해 공식 채널 기반 수집, 규칙 기반 선별, LLM 기반 한국어 요약, GitHub Pages 배포를 하나의 운영 흐름으로 묶는다.

## 업무 목표

- 매주 1회 최신 IT 개발 기술 다이제스트 초안을 자동으로 생성한다.
- 공식 소스만 대상으로 삼아 신뢰도와 재현성을 확보한다.
- 사람이 10~15분 안에 검토할 수 있을 정도로 압축된 결과를 만든다.
- 블로그 저장소 안에서 수집, 초안 생성, 검토, 배포를 끝낸다.

## 기본 운영 원칙

### 1. 공식 소스 우선

초기 수집 대상은 아래 세 축으로 제한한다.

- 공식 changelog 또는 product updates
- 공식 engineering blog 또는 developer blog
- 공식 GitHub Releases API

커뮤니티 포럼, 개인 블로그, 뉴스 큐레이션 사이트, Hacker News, Reddit는 초기 범위에서 제외한다.

### 2. 변경 신호 중심

다음 유형의 항목을 우선 포함한다.

- release
- changelog
- GA, preview, beta
- deprecation, breaking change
- security advisory
- SDK 또는 API update

다음 유형의 항목은 기본적으로 제외한다.

- 고객 사례
- 채용
- 투자 및 재무 소식
- 행사 안내
- 인터뷰성 글
- 제품 변화가 없는 일반 튜토리얼

### 3. 주간 quota 유지

주간 글이 특정 회사 소식으로 치우치지 않도록 quota를 둔다.

- AI/LLM 플랫폼: 2개 내외
- 웹/프론트엔드/런타임: 2개 내외
- 클라우드/인프라/DevOps: 2개 내외
- OSS 릴리즈/보안/deprecation: 2개 내외

초기 목표는 총 8~12개 항목이다.

### 4. 초기 발행은 PR 기반

자동화 초반에는 `main`에 직접 발행하지 않는다. 주간 초안을 PR로 생성하고, 운영자가 제목, 표현, 링크, 중요도를 검토한 뒤 merge하는 방식을 기본 운영 모드로 둔다.

### 5. 공개 글은 편집 메모처럼 쓴다

공식 소스를 기반으로 수집하더라도, 최종 공개 글은 릴리즈 노트 복붙이나 템플릿 요약처럼 보이면 안 된다.

- 첫 문단에서 이번 주의 관찰을 먼저 말한다.
- 항목별로 사실과 해석을 분리해 쓴다.
- 수치, 버전, 시점, 실패 조건 같은 구체 디테일을 우선한다.
- 글 말미는 자동화 설명이 아니라 다음 확인 포인트로 닫는다.

상세 규약은 `docs/weekly-tech-roundup-writing-guide.md`를 따른다.

## 초기 수집 대상

초기 수집 풀은 15~20개 내외로 시작한다. 예시는 아래와 같다.

- GitHub Changelog
- AWS What's New 또는 AWS News Blog
- Cloudflare changelog/RSS
- OpenAI News
- Anthropic Newsroom
- Microsoft Dev Blogs
- Google Developers Blog
- React Blog
- Node.js Blog
- Next.js Blog
- Kubernetes Blog
- web.dev Blog
- PyTorch Blog
- GitHub Releases API for `facebook/react`, `nodejs/node`, `vercel/next.js`, `kubernetes/kubernetes`, `microsoft/TypeScript`, `pytorch/pytorch`

추가 소스는 운영 중에 늘리되, 다음 조건을 통과한 경우만 채택한다.

- 공식 채널인지 명확하다.
- 최근 3개월 기준 변경 신호 밀도가 충분하다.
- 기계 수집이 안정적이다.
- 주간 다이제스트 품질을 실제로 높인다.

## 권장 저장소 구조

이 기능은 별도 저장소보다 현재 블로그 저장소 안에서 운영하는 편이 단순하다.

예상 디렉터리 구조:

```text
docs/
specs/001-weekly-tech-digest-agent/
.github/workflows/weekly-tech-digest.yml
scripts/weekly-tech/
data/weekly-tech/sources.yml
data/weekly-tech/output/
_posts/
```

이 구조를 쓰면 수집 코드, 생성된 Markdown, Pages 배포가 하나의 저장소 안에서 이어지고, PR 검토 흐름도 단순하게 유지된다.

## v1 범위

v1에서는 아래만 목표로 삼는다.

- 공식 소스 목록 관리
- 최근 7일 후보 수집
- 규칙 기반 필터링과 중복 제거
- LLM 기반 한국어 다이제스트 초안 생성
- `_posts/` 파일 작성
- GitHub Actions 기반 주간 실행
- PR 생성 후 사람 검토

아래는 v1 범위 밖으로 둔다.

- 완전 자동 무인 발행
- 데이터베이스 기반 대규모 캐시
- Slack, Notion, 이메일 동시 배포
- 비공식 뉴스 소스 큐레이션

## 다음 산출물

이 문서를 바탕으로 다음 산출물을 순차적으로 만든다.

1. `specs/001-weekly-tech-digest-agent/spec.md`
2. 구현 계획 문서 `plan.md`
3. 구현 작업 문서 `tasks.md`
4. 소스 설정 파일 `data/weekly-tech/sources.yml`
5. 수집 및 초안 생성 스크립트
6. 공개 글 작성 규약 `docs/weekly-tech-roundup-writing-guide.md`
7. GitHub Actions workflow
