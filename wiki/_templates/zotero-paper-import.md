---
title: "{{title}}"
type: source
status: draft
source_kind: paper
source_url: '{% if DOI %}https://doi.org/{{DOI | replace("https://doi.org/", "") | replace("http://doi.org/", "") }}{% elseif url %}{{url}}{% endif %}'
citekey: "{{citekey}}"
zotero_item_key: "{{key}}"
zotero_pdf_uri: '{% for attachment in attachments | filterby("path", "endswith", ".pdf") %}{% if loop.first %}{{attachment.desktopURI | replace("/select/", "/open-pdf/")}}{% endif %}{% endfor %}'
ingested_at: '{{importDate | format("YYYY-MM-DD")}}'
updated_at: '{{importDate | format("YYYY-MM-DD")}}'
tags:
  - paper
  - zotero
---

# 소스 요약

## 한 줄 요약

{% persist "summary" %}
- 
{% endpersist %}

## 다시 읽을 때 먼저 볼 것

{% for attachment in attachments | filterby("path", "endswith", ".pdf") %}
{% if loop.first %}
- 원문 PDF: [Zotero PDF]({{attachment.desktopURI | replace("/select/", "/open-pdf/")}})
{% endif %}
{% endfor %}
{% persist "quick_return" %}
- 이 논문을 다시 볼 때 먼저 확인할 핵심:
- 지금 내 질문으로 다시 읽으면 좋은 지점:
- 다음에 이어서 볼 쟁점:
{% endpersist %}

## 핵심 내용

{% persist "claims" %}
- 
{% endpersist %}

## 질의응답으로 정리한 이해

{% persist "qa" %}
### 질문 1

- 질문:
- 답:
{% endpersist %}

## 헷갈리는 수식과 표기

{% persist "formulas" %}
### 항목 1

- 표기:
- 무엇을 뜻하는가:
- 왜 헷갈렸는가:
- 내 식으로 다시 설명:
{% endpersist %}

## 기억할 실험 / 수치

{% persist "experiments" %}
- 
{% endpersist %}

## 연결할 위키 페이지

{% persist "links" %}
- [[wiki/topics/...]]
{% endpersist %}

## 블로그에 중요한 포인트

{% persist "blog_points" %}
- 
{% endpersist %}

## 불확실성 및 후속 조사

{% persist "followups" %}
- 
{% endpersist %}

## Zotero annotation log

{% persist "annotation_log" %}
{% set newAnnotations = annotations | filterby("date", "dateafter", lastImportDate) %}
{% if newAnnotations.length > 0 %}
### Imported: {{importDate | format("YYYY-MM-DD HH:mm")}}

{% for annotation in newAnnotations %}
#### p. {% if annotation.pageLabel %}{{annotation.pageLabel}}{% else %}{{annotation.page}}{% endif %}

{% if annotation.annotatedText %}
> {{annotation.annotatedText}}
{% endif %}
{% if annotation.comment %}
- 내 메모: {{annotation.comment}}
{% endif %}
{% if annotation.tags and annotation.tags.length > 0 %}
- 태그: {% for tag in annotation.tags %}#{{tag.tag}} {% endfor %}
{% endif %}
{% if annotation.colorCategory %}
- 색상 분류: {{annotation.colorCategory}}
{% endif %}

{% endfor %}
{% endif %}
{% endpersist %}
