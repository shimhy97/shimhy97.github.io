# 주간 최신 기술 다이제스트 Workflow

## 문서 목적

이 문서는 주간 최신 기술 다이제스트 기능을 어떤 개발 절차로 만들고, 운영 중에는 어떤 순서로 실행할지 정리한다. 개발 절차는 spec-kit 방식을 그대로 복제하지 않고, 이 저장소 구조에 맞게 `spec -> plan -> tasks -> implementation` 흐름만 차용한다.

공개 글의 최종 어투와 구조는 `docs/technical-post-writing-guide.md`를 기준으로 삼는다.

## 개발 Workflow

### 1. Spec 작성

기능 목표, 사용자 시나리오, 기능 요구사항, 성공 기준을 먼저 `specs/001-weekly-tech-digest-agent/spec.md`에 고정한다.

이 단계에서 정하는 내용:

- 무엇을 수집할지
- 무엇을 제외할지
- 어떤 수준까지 자동화할지
- 초기 운영 모드를 PR 기반으로 둘지
- 어떤 조건을 만족해야 구현 완료로 볼지

### 2. Plan 작성

spec이 합의되면 같은 디렉터리에 `plan.md`를 추가한다. plan 문서에는 구현 언어, 파일 배치, 실행 진입점, GitHub Actions 구조, 외부 의존성, 검증 방식을 적는다.

예상 plan 항목:

- Python 기반 수집기 사용 여부
- `scripts/weekly-tech/` 모듈 구성
- `data/weekly-tech/sources.yml` 스키마
- GitHub Releases API와 RSS 파서 선택
- LLM 호출 인터페이스
- 실패 처리 및 로그 파일 위치

### 3. Tasks 작성

구현 전 마지막 단계로 `tasks.md`를 만든다. 작업은 사용자가 독립 검증 가능한 단위로 쪼갠다.

예상 작업 묶음:

- 소스 설정 스키마와 샘플 파일 추가
- RSS/API 수집기 구현
- 정규화 및 중복 제거 로직 구현
- quota 및 제외 규칙 구현
- Markdown 초안 생성기 구현
- GitHub Actions workflow 추가
- PR 생성 및 품질 검증 단계 추가

### 4. Implementation

구현은 `tasks.md`에 정의한 순서로 진행한다. 모든 구현은 같은 저장소 안에서 끝나야 하며, 기본 품질 검사는 `./scripts/blog-build.sh`로 통일한다.

## 운영 Workflow

### 주간 실행 흐름

```text
스케줄 도래
-> 공식 소스 수집
-> 최근 7일 항목 정규화
-> 중복 제거 및 제외 규칙 적용
-> 카테고리 quota 반영
-> LLM 한국어 요약 생성
-> Jekyll 포스트 파일 작성
-> 빌드 검증
-> PR 생성
-> 운영자 검토 및 merge
-> 기존 Pages workflow로 배포
```

### 각 단계 설명

#### 1. 공식 소스 수집

`sources.yml`에 등록된 공식 RSS, changelog, GitHub Releases API를 읽는다. 수집 단위는 최근 7일이며, 원문 URL과 발행일을 반드시 확보한다.

#### 2. 정규화와 중복 제거

소스별로 제각각인 필드를 공통 구조로 바꾸고, 같은 내용을 다른 경로로 수집한 경우 하나의 후보로 병합한다.

#### 3. 규칙 기반 선별

포함 규칙과 제외 규칙을 먼저 적용한다. 그 다음 카테고리 quota를 반영해 주간 글이 특정 기업 공지로 편향되지 않게 한다.

#### 4. 한국어 초안 생성

선택된 항목만 대상으로 한국어 초안을 만든다. 내부 요약 데이터는 일관되게 유지하되, 공개 글은 `docs/technical-post-writing-guide.md`의 규약에 따라 서술형 문단으로 재구성한다.

- 도입부에서 이번 주의 관찰 한 줄을 먼저 제시한다.
- 섹션마다 짧은 편집 메모를 붙인다.
- 각 항목은 사실 문장, 해석 문장, 체크 포인트 또는 원문 링크로 정리한다.
- 내부 필드인 `what_changed`, `why_it_matters`, `practical_impact`를 그대로 노출하지 않는다.

#### 5. 포스트 파일 작성

결과를 `_posts/YYYY-MM-DD-weekly-tech-roundup.md` 형식의 Jekyll 포스트로 만든다. front matter에는 제목, 날짜, 카테고리, 태그, excerpt를 넣는다.

#### 6. 품질 검증

생성된 글은 `./scripts/blog-build.sh`를 통과해야 한다. 빌드가 실패하면 PR 생성 또는 merge 단계로 넘어가지 않는다.

#### 7. PR 생성과 검토

초기 운영 모드는 자동 PR 생성이다. 운영자는 아래 항목을 검토한다.

- 제목이 자연스러운가
- 항목 수가 너무 적거나 많지 않은가
- 중요 항목이 누락되지 않았는가
- 링크와 발행일이 정확한가
- 마케팅성 표현이 과하지 않은가
- 첫 문장에서 이번 주의 관찰이 드러나는가
- 같은 경고 문장과 같은 문장형이 반복되지 않는가
- 마무리가 자동화 설명이 아니라 다음 확인 포인트로 끝나는가

#### 8. Merge와 배포

운영자가 PR을 merge하면 기존 [[.github/workflows/pages.yml|pages.yml]] 이 `main` 브랜치 변경을 감지해 GitHub Pages를 다시 배포한다.

## 운영 체크리스트

주간 실행 전:

- 소스 목록이 최신인지 확인한다.
- API 한도와 자격 증명이 유효한지 확인한다.
- 이번 주에 제외할 특수 이벤트가 없는지 본다.

주간 실행 후:

- 수집 실패 소스가 있었는지 본다.
- 최종 채택 수가 기대 범위에 있는지 본다.
- 중복 또는 낮은 가치의 항목이 섞이지 않았는지 본다.
- 생성된 Markdown이 빌드되는지 확인한다.

월간 점검:

- 거의 선택되지 않는 소스를 제거한다.
- 자주 깨지는 파서를 고친다.
- quota와 필터 규칙을 조정한다.
- 자동 발행 전환 가능성을 평가한다.

## 저장소 문서 간 관계

- 기능 범위와 성공 기준: `specs/001-weekly-tech-digest-agent/spec.md`
- 업무 목적과 운영 원칙: `docs/weekly-tech-digest-agent.md`
- 일반 기술 글 작성 가이드: `docs/technical-post-writing-guide.md`
- 구현 이후 코드와 workflow: `.github/workflows/`, `scripts/weekly-tech/`, `data/weekly-tech/`

이 문서는 구현 전에 방향을 고정하는 문서이며, 실제 파일 경로와 명령은 plan 단계에서 구체화한다.
