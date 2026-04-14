---
title: "블로그 위키 대시보드"
type: dashboard
status: active
updated_at: 2026-04-14
tags:
  - wiki
  - obsidian
  - dataview
---

# 블로그 위키 대시보드

Obsidian에서 위키를 열었을 때 가장 먼저 보는 진입점입니다. `index.md`는 사람이 관리하는 정적 카탈로그로 두고, 이 노트는 Dataview로 현재 상태를 빠르게 훑는 용도로 씁니다.

## 최근 업데이트된 source note

```dataview
TABLE file.link AS "노트", source_kind AS "종류", updated_at AS "업데이트", status AS "상태"
FROM "wiki/sources"
SORT updated_at DESC
```

## 논문 source note

```dataview
TABLE file.link AS "논문", updated_at AS "업데이트", source_url AS "원문", status AS "상태"
FROM "wiki/sources"
WHERE source_kind = "paper"
SORT updated_at DESC
```

## 최근 query note

```dataview
TABLE file.link AS "질문", updated_at AS "업데이트", source_count AS "근거 수"
FROM "wiki/queries"
SORT updated_at DESC
```

## 발행된 draft

```dataview
TABLE file.link AS "초안", updated_at AS "업데이트", source_count AS "근거 수"
FROM "wiki/drafts"
WHERE status = "published"
SORT updated_at DESC
```

## 점검이 필요한 노트

```dataview
TABLE file.link AS "노트", type AS "유형", status AS "상태", updated_at AS "업데이트"
FROM "wiki"
WHERE status AND status != "active" AND status != "filed" AND status != "published"
SORT updated_at DESC
```
