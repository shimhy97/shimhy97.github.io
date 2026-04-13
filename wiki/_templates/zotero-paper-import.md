---
title: "{{title}}"
type: source
status: draft
source_kind: paper
source_path: ""
source_url: "{% if DOI %}https://doi.org/{{DOI | replace('https://doi.org/', '') | replace('http://doi.org/', '') }}{% elseif url %}{{url}}{% endif %}"
ingested_at: {{importDate | format("YYYY-MM-DD")}}
updated_at: {{importDate | format("YYYY-MM-DD")}}
tags:
  - paper
  - zotero
---

# 소스 요약

## 서지 정보

{{bibliography}}

{% if abstractNote %}
## 초록

{{abstractNote}}
{% endif %}

## PDF

{% for attachment in attachments | filterby("path", "endswith", ".pdf") %}
- [PDF{% if not loop.first %} {{loop.index}}{% endif %}]({{attachment.desktopURI | replace("/select/", "/open-pdf/")}})
{% endfor %}

## 한 줄 요약

{% persist "summary" %}
- 
{% endpersist %}

## 핵심 주장

{% persist "claims" %}
- 
{% endpersist %}

## 방법 / 실험 설정

{% persist "method" %}
- 
{% endpersist %}

## 새로 가져온 주석

{% persist "annotations" %}
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

## 연결할 위키 페이지

{% persist "links" %}
- [[...]]
{% endpersist %}

## 블로그에 중요한 포인트

{% persist "blog_points" %}
- 
{% endpersist %}

## 불확실성 및 후속 조사

{% persist "followups" %}
- 
{% endpersist %}
