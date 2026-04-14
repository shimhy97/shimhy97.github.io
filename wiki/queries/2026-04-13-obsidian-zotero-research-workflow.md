---
title: "논문 연구용 Obsidian + Zotero 워크플로 조사"
type: query
status: filed
created_at: 2026-04-13
updated_at: 2026-04-14
source_count: 10
tags:
  - research
  - papers
  - obsidian
  - zotero
  - llm-wiki
---

# 질문

논문을 Zotero로 관리 중일 때, Obsidian을 함께 쓰는 보편적 방식은 무엇이며, 현재 이 블로그 LLM 위키 구조에는 어떤 세팅이 맞는가?

## 결론

- Zotero와 Obsidian은 대체재보다 역할 분담 조합에 가깝다. Zotero는 논문 수집, 메타데이터, PDF, 주석의 원본 시스템이고, Obsidian은 문헌 노트, 주제 노트, MOC, 그래프 탐색, 장기 합성에 강하다.
- 외부 사례를 보면 "Zotero만으로 끝내는 사람"도 있지만, 논문 간 연결과 장기 지식 그래프를 만들려는 경우는 대체로 혼합형을 쓴다.
- 내 상황에는 `Zotero = source of truth`, `Obsidian = thinking layer`, `이 블로그 repo = publish layer` 3단 분리가 가장 안전하다.
- 이 레포를 Obsidian vault로 계속 열 수는 있지만, 논문 원문 PDF 자체는 커밋하지 않고 DOI, URL, Zotero 식별자와 source note로만 추적하는 편이 맞다.
- 현재 레포는 `[[wiki/dashboard]]`와 Dataview를 기본 진입점으로 두고, Zotero import도 `@citekey` intake note 대신 사람용 slug source note를 바로 만드는 방향으로 정리하는 것이 자연스럽다.

## 외부 사례에서 보인 대표 패턴

### 1. Zotero 중심형

- Zotero 자체가 PDF 주석, annotation note, note template를 지원하므로, 읽고 밑줄 긋고 간단한 정리까지는 Zotero 안에서 끝내는 흐름이 가능하다.
- 이 방식은 메타데이터와 PDF가 한곳에 모여 관리가 단순하다.
- 대신 논문 간 연결, 개념 노트, 그래프 탐색, topic map 같은 기능은 약하다.

### 2. Zotero + Obsidian 혼합형

- 가장 흔하게 보인 패턴이다.
- 자료 수집과 인용키 관리는 Zotero와 Better BibTeX가 맡고, Obsidian에는 literature note와 permanent note만 쌓는다.
- Obsidian Forum 사례를 보면 Zotero Integration으로 전체 노트를 동기화하기보다 "annotation만 가져오고, 요약과 해석은 Obsidian에서 따로 쓰는" 흐름이 실무적으로 더 흔하다.
- Dataview로 문헌 카탈로그를 만들거나, MOC와 local graph를 이용해 source note에서 topic note로 확장하는 사례가 많다.

### 3. Obsidian 중심형

- Zotero Integration 템플릿을 강하게 커스터마이즈해서 메타데이터, PDF 링크, 색상별 주석, 관계 필드까지 전부 Obsidian note로 끌어오는 방식이다.
- Zettelkasten 스타일로 `source -> literature -> permanent -> MOC`를 엄격하게 나누는 사례도 있다.
- 다만 플러그인과 템플릿 의존성이 커지고, Zotero 쪽 필드 변화나 citekey 이슈가 나면 흐름이 깨질 수 있다.

## 플러그인 상태 메모

- Obsidian Zotero Integration은 Zotero의 citation, bibliography, note, PDF annotation을 Obsidian으로 가져오는 커뮤니티 플러그인이고 Better BibTeX를 요구한다.
- GitHub release 기준 최신 릴리스는 `3.2.1`, 배포일은 `2024-08-11`이다.
- 2026-02 Obsidian Forum 글에서는 Zotero 8 이후 citation key migration 때문에 import가 비는 사례가 보고됐다. 커뮤니티 답변에서는 `Better BibTeX 활성화`, `Citation Key 재생성`, `extensions.zotero.httpServer.localAPI.enabled = true` 확인을 해결책으로 제시했다.
- 즉 지금도 쓸 수는 있지만 "설치 후 영원히 잊는" 종류의 안정성까지 기대하면 안 된다.

## 내 상황에 맞는 권장 구조

### 권장 계층

- Zotero
  - 논문 원본 PDF
  - 메타데이터
  - 하이라이트와 annotation
  - citation key
- Obsidian private vault
  - literature note
  - topic / permanent note
  - MOC
  - 아직 공개하지 않을 연구 메모
- 블로그 repo
  - `raw/`: 공개해도 되는 원천 자료
  - `wiki/sources/`: 블로그용 소스 요약
  - `wiki/topics/`: 공개 가능한 주제 페이지
  - `wiki/drafts/`: 글 후보
  - `_posts/`: 최종 공개 글

### 왜 별도 vault가 더 맞는가

- 논문 PDF와 미공개 메모를 블로그 repo에 오래 쌓아 두면 공개/비공개 경계가 흐려진다.
- Git 저장소에 PDF를 계속 넣으면 저장소가 빨리 무거워진다.
- Obsidian 공식 도움말도 vault는 로컬 폴더 전체를 기준으로 보며, vault 안에 vault를 중첩하지 말라고 안내한다.

## 내가 지금 바로 쓸 세팅

### Zotero

1. Better BibTeX 설치
2. citation key 생성 규칙 고정
3. Zotero `Export`에서 `Better BibTeX Quick Copy`를 기본 quick copy 형식으로 지정
4. Zotero 8 사용 중이고 Obsidian import가 비면:
   - Better BibTeX가 켜져 있는지 확인
   - 기존 항목들에 citation key가 실제로 들어 있는지 확인
   - 필요하면 항목 선택 후 `Better BibTeX -> Refresh`
   - `extensions.zotero.httpServer.localAPI.enabled = true` 확인

### Obsidian

- Core plugin
  - Templates
  - Backlinks
  - Outgoing links
  - Graph view
  - Search
- Community plugin
  - Zotero Integration
  - Dataview
- Templates folder
  - 이 repo를 vault로 여는 경우 `wiki/_templates`
- 첨부 파일 폴더
  - 이 repo를 vault로 여는 경우 `raw/assets`
- Zotero Integration import template
  - `[[wiki/_templates/zotero-paper-import]]`
- Dataview 기본 진입점
  - `[[wiki/dashboard]]`

### Zotero Integration에서 권장할 출력 경로

- 이 블로그 repo를 바로 실험용 vault로 쓸 때:
  - `wiki/sources/{{title-slug}}.md`
- 별도 research vault를 만들 때:
  - `01 Sources/{{title-slug}}.md`

## 추천 노트 흐름

1. Zotero에 논문 저장
2. PDF에서 하이라이트와 annotation 작성
3. Obsidian Zotero Integration으로 source note 생성
4. source note에서 핵심 주장 1~3개만 permanent note로 분리
5. topic note나 MOC에 permanent note를 연결
6. 블로그로 공개할 가치가 생기면 이 repo의 `wiki/sources/`, `wiki/topics/`, `wiki/drafts/`로 승격

## 과하게 하지 말아야 할 것

- 처음부터 플러그인을 많이 깔지 않는다.
- PDF 전체를 Obsidian에 복제하는 흐름을 기본값으로 잡지 않는다.
- 논문 원문 PDF를 이 블로그 repo에 커밋하는 흐름을 기본값으로 잡지 않는다.
- 요약, 해석, 블로그 초안까지 source note 한 파일에 몰아넣지 않는다.
- Zotero 메타데이터를 Obsidian에서 수동으로 덮어쓰기 시작하지 않는다.

## 이 저장소에 남겨 둔 템플릿

- [[wiki/_templates/zotero-paper-import]]: Zotero Integration import용 source note 템플릿
- [[wiki/_templates/obsidian-permanent-note]]: source note에서 뽑아낼 permanent note 템플릿
- [[wiki/dashboard]]: source, query, draft를 Dataview로 훑는 기본 대시보드
- [[docs/zotero-paper-ingest-workflow]]: 새 논문 1편을 Zotero에서 canonical source note로 정리하는 실제 순서

## 블로그 글로의 확장 가능성

- "왜 Zotero만으로는 부족했고, 왜 Obsidian을 thinking layer로 붙였는가"라는 글로 확장 가능하다.
- 발행한다면 `source of truth`와 `thinking layer`를 분리하는 개인 연구 워크플로 관점이 중심 논지다.

## 참고 자료

- [Obsidian Help: How Obsidian stores data](https://obsidian.md/help/data-storage)
- [Obsidian Help: Community plugins](https://obsidian.md/help/community-plugins)
- [Obsidian Help: Templates](https://obsidian.md/help/plugins/templates)
- [Obsidian Help: Graph view](https://help.obsidian.md/plugins/graph)
- [Zotero Documentation: PDF Reader and annotations](https://www.zotero.org/support/pdf_reader)
- [Obsidian Zotero Integration README](https://github.com/obsidian-community/obsidian-zotero-integration/blob/main/README.md)
- [Obsidian Zotero Integration releases](https://github.com/obsidian-community/obsidian-zotero-integration/releases)
- [Better BibTeX: Citation Keys](https://retorque.re/zotero-better-bibtex/citing/index.html)
- [Better BibTeX: Automatic export](https://retorque.re/zotero-better-bibtex/exporting/auto/)
- [Obsidian Forum: Pull in via zotero integration the notes](https://forum.obsidian.md/t/pull-in-via-zotero-integration-the-notes/98021/9)
- [Obsidian Forum: Academic Note Taking and Making System](https://forum.obsidian.md/t/academic-note-taking-and-making-system-with-the-zettelkasten-method-obsidian-zotero/64941/2)
- [Obsidian Forum: Search literature notes in a library-catalog interface](https://forum.obsidian.md/t/search-literature-notes-in-a-library-catalog-interface/39757)
- [Obsidian Forum: Zotero Integration template for Literature Notes](https://forum.obsidian.md/t/zotero-integration-template-for-literature-notes/71111)
- [Obsidian Forum: Zotero Plugin](https://forum.obsidian.md/t/zotero-plugin/111390/3)
