# Zotero 논문 정리 Workflow

## 문서 목적

이 문서는 새 논문을 Zotero에 저장한 뒤, 이 레포의 Obsidian + 위키 구조로 어떻게 정리할지 실제 작업 순서를 고정한다. 목표는 논문 PDF를 이 레포에 복제하지 않고도, `wiki/sources/`에 다시 읽기 쉬운 canonical source note를 만들고 관련 topic, query, draft까지 자연스럽게 이어 가는 것이다.

## 전제

- 논문 원문 PDF와 주석은 Zotero가 source of truth다.
- 이 레포에는 논문 PDF나 PDF-to-Markdown dump를 커밋하지 않는다.
- Obsidian에서 이 레포를 vault로 열고 작업한다.
- Zotero Integration과 Dataview가 켜져 있어야 한다.
- Zotero Integration import format은 `Import paper to wiki`를 사용한다.
- import 결과 파일은 `wiki/sources/{{title-slug}}.md` 형태의 사람용 slug source note다.

## 새 논문 정리 절차

### 1. Zotero에서 원문과 메타데이터를 먼저 정리한다

1. Zotero에 논문을 저장한다.
2. DOI, URL, 제목, 저자, 발행 연도 같은 기본 메타데이터가 맞는지 확인한다.
3. PDF에서 최소한의 하이라이트와 코멘트를 남긴다.
4. Better BibTeX citation key가 비어 있지 않은지 확인한다.

### 2. 기존 source note가 있는지 먼저 확인한다

1. Obsidian에서 `[[wiki/dashboard]]`를 열고 `논문 source note` 목록을 본다.
2. 같은 논문이 이미 `wiki/sources/`에 있으면 새 note를 만들지 말고 기존 note를 연다.
3. 제목이 비슷한 논문이 여러 개면 DOI와 `source_url`로 동일 문서인지 먼저 확인한다.

### 3. Zotero Integration으로 canonical source note를 만든다

1. Obsidian 명령 팔레트에서 Zotero Integration import를 실행한다.
2. import format으로 `Import paper to wiki`를 선택한다.
3. 생성 위치가 `wiki/sources/{{title-slug}}.md`인지 확인한다.
4. note가 열리면 frontmatter에 아래 필드가 자동으로 들어갔는지 확인한다.
   - `title`
   - `type: source`
   - `source_kind: paper`
   - `source_url`
   - `citekey`
   - `zotero_item_key`
   - `zotero_pdf_uri`
   - `ingested_at`
   - `updated_at`

### 4. source note를 사람이 다시 읽기 쉬운 상태로 정리한다

source note는 단순 annotation dump가 아니라, 다음에 다시 볼 때 빠르게 맥락을 복구할 수 있어야 한다. 아래 순서대로 채운다.

1. `한 줄 요약`
   - 이 논문을 한 문장으로 어떻게 이해할지 먼저 적는다.
2. `다시 읽을 때 먼저 볼 것`
   - 다음에 이 note만 봐도 왜 중요한 논문인지 떠오르도록 핵심 전제, 다시 볼 포인트, 열린 쟁점을 적는다.
3. `핵심 내용`
   - 모델, 주장, 실험, 기여를 3~6개 bullet로 정리한다.
4. `질의응답으로 정리한 이해`
   - 실제로 읽으며 막혔던 질문을 `질문 / 답` 형식으로 적는다.
   - 나중에 같은 질문이 다시 나올 만한 지점만 남긴다.
5. `헷갈리는 수식과 표기`
   - 각 항목을 아래 네 줄 패턴으로 정리한다.
   - `표기`
   - `무엇을 뜻하는가`
   - `왜 헷갈렸는가`
   - `내 식으로 다시 설명`
6. `기억할 실험 / 수치`
   - 데이터셋, 메트릭, 핵심 수치, 비교 기준 중 다음에도 다시 쓸 만한 것만 남긴다.
7. `연결할 위키 페이지`
   - topic, query, draft로 이어질 wikilink를 넣는다.
8. `블로그에 중요한 포인트`
   - 공개 글로 키울 때 논지가 될 만한 포인트를 적는다.
9. `불확실성 및 후속 조사`
   - 아직 헷갈리는 점, 비교할 후속 논문, 서비스 적용 시 빈칸을 남긴다.
10. `Zotero annotation log`
   - annotation log는 아래쪽에 남겨 두고, 위 요약 섹션을 오염시키지 않게 관리한다.

## source note 다음 단계

### 5. 관련 topic note를 만들거나 갱신한다

1. 논문이 기존 topic을 강화하는 경우:
   - 해당 `wiki/topics/*.md`를 열어 현재 이해, 열린 질문, 연결 페이지를 보강한다.
2. 반복해서 재등장할 새 개념이면:
   - `[[wiki/_templates/topic-page]]`를 기준으로 새 topic note를 만든다.
3. source note의 `연결할 위키 페이지`에는 최소 1개 topic wikilink를 넣는다.

### 6. 질의응답이 생기면 query note로 분리한다

1. 읽는 중 특정 질문에 답을 길게 정리하게 되면 `wiki/queries/`로 분리한다.
2. `[[wiki/_templates/query-note]]` 형식을 따라 질문, 결론, 근거 페이지를 정리한다.
3. source note와 topic note에서 해당 query note를 서로 연결한다.

### 7. 공개 가치가 생기면 draft로 승격한다

1. 블로그 글로 쓸 논지가 생기면 `wiki/drafts/`에 초안을 만든다.
2. source note는 근거와 기억 복구용이고, draft는 독자용 논지 설계라는 역할 차이를 유지한다.
3. source note에서 draft로 갈 때는 그대로 복사하지 말고, `왜 이 논문을 지금 다시 읽어야 하는가`를 중심으로 재구성한다.

## 마무리 체크리스트

논문 1편 정리를 마친 뒤 아래 항목을 확인한다.

- `wiki/sources/`에 canonical source note가 1개만 있는가
- `source_url`, `citekey`, `zotero_item_key`, `zotero_pdf_uri`가 남아 있는가
- source note 상단이 annotation dump가 아니라 사람이 다시 읽기 쉬운 구조인가
- 관련 topic, query, draft가 필요한 만큼 연결됐는가
- `wiki/index.md`에 새 source / topic / query / draft가 반영됐는가
- `wiki/log.md`에 이번 ingest 또는 revise 이력이 남았는가
- 내부 문서 링크가 wikilink로 연결돼 있는가

## 하지 말아야 할 것

- 논문 PDF를 `raw/sources/`에 넣지 않는다.
- 같은 논문에 대해 `@citekey` intake note와 사람용 slug note를 둘 다 유지하지 않는다.
- source note를 annotation raw dump처럼 방치하지 않는다.
- 수식을 원문 그대로만 옮기고, 내 언어로 다시 설명하는 문장을 빼지 않는다.
- query나 draft로 커질 만한 내용을 source note 한 파일에 계속 밀어 넣지 않는다.

## 관련 문서

- [[wiki/dashboard]]
- [[wiki/index]]
- [[wiki/_templates/zotero-paper-import]]
- [[wiki/_templates/topic-page]]
- [[wiki/_templates/query-note]]
- [[wiki/queries/2026-04-13-obsidian-zotero-research-workflow]]
- [[docs/blog-wiki-workflow]]
