---
title: "{{title}}"
type: source
status: draft
updated_at: {{importDate | format("YYYY-MM-DD")}}
---

# 디버그 노트

- citekey: {{citekey}}
- title: {{title}}
- importDate: {{importDate | format("YYYY-MM-DD HH:mm")}}

{% if abstractNote %}
## abstract

{{abstractNote}}
{% endif %}
