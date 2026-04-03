# Ralph Loop for This Blog

이 폴더는 Ralph 실행 스크립트와 프롬프트를 프로젝트 안에 두는 방식으로 구성되어 있습니다.

## 중요한 차이점

공식 Ralph 예제는 `ralph.sh`, `prompt.md`, `prd.json`, `progress.txt`가 같은 디렉터리에 있는 구성을 자주 보여줍니다. 이 저장소는 사용 편의를 위해 아래처럼 정리했습니다.

```text
scripts/ralph/ralph.sh
scripts/ralph/prompt.md
scripts/ralph/CLAUDE.md
prd.json
progress.txt
tasks/
```

즉:

- 실행 스크립트와 프롬프트는 `scripts/ralph/`
- 작업 상태 파일은 프로젝트 루트

## 실행 전 준비

```bash
brew install jq
```

그리고 `claude` 또는 `amp` CLI 중 하나가 설치돼 있어야 합니다.

## 실행 예시

```bash
./scripts/ralph/ralph.sh --tool claude 5
```

위 명령은 최대 5회 반복하면서 `prd.json`에서 아직 완료되지 않은 가장 높은 우선순위 스토리 하나씩 처리합니다.

이 저장소에서 Ralph가 호출해야 하는 기본 품질 체크는 아래입니다.

```bash
./scripts/blog-build.sh
```
