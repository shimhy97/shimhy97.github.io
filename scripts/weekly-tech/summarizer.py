"""선정된 후보를 한국어 다이제스트 문단으로 변환한다."""

from __future__ import annotations

import json
import os
from datetime import datetime

import httpx

from models import CandidateEntry, DigestConfig, DigestItem


def summarize_candidates(
    candidates: list[CandidateEntry],
    config: DigestConfig,
    as_of: datetime,
) -> tuple[str, list[DigestItem], str]:
    """후보 목록을 한국어 다이제스트 문단으로 바꾼다.

    의도:
        선별된 항목을 사람이 바로 읽고 검토할 수 있는 블로그 초안 형태로
        바꾸기 위해 LLM 또는 추출형 fallback을 적용한다.

    Args:
        candidates: quota와 점수 계산을 거친 최종 후보 목록.
        config: 기본 요약 방식과 카테고리 레이블이 들어 있는 설정.
        as_of: 도입 문단과 기간 표기에 사용할 기준 시각.

    Returns:
        도입 요약, 항목별 DigestItem 목록, 실제 사용한 summary mode를 담은 튜플.
    """

    requested_mode = os.getenv("WEEKLY_TECH_SUMMARY_MODE", config.summary_mode).lower()
    api_key = os.getenv("OPENAI_API_KEY")

    if requested_mode in {"openai", "auto"} and api_key:
        try:
            return _summarize_with_openai(candidates, config, as_of)
        except Exception:  # noqa: BLE001
            if requested_mode == "openai":
                raise

    overview, items = _summarize_extractive(candidates, config, as_of)
    return overview, items, "extractive"


def _summarize_with_openai(
    candidates: list[CandidateEntry],
    config: DigestConfig,
    as_of: datetime,
) -> tuple[str, list[DigestItem], str]:
    """OpenAI Responses API를 호출해 한국어 문단을 생성한다."""

    model = os.getenv("OPENAI_MODEL", "gpt-5.4-mini")
    prompt_payload = {
        "date": as_of.date().isoformat(),
        "timezone": config.timezone,
        "categories": config.category_labels,
        "items": [
            {
                "index": index,
                "title": candidate.entry.title,
                "source_name": candidate.entry.source_name,
                "source_kind": candidate.entry.source_kind,
                "category": candidate.entry.category,
                "published_at": candidate.entry.published_at.isoformat(),
                "summary": candidate.entry.summary[:2000],
                "url": candidate.entry.url,
            }
            for index, candidate in enumerate(candidates, start=1)
        ],
    }

    system_prompt = (
        "너는 한국어 기술 블로그 에디터다. "
        "공식 소스 기반 최신 기술 소식을 과장 없이 요약한다. "
        "반드시 JSON만 반환하고, 각 항목은 사실을 과장하지 말아라."
    )
    user_prompt = (
        "다음 입력을 바탕으로 한국어 JSON을 만들어라. "
        "형식은 {\"overview\": str, \"items\": [{\"index\": int, "
        "\"what_changed\": str, \"why_it_matters\": str, \"practical_impact\": str}]} 이어야 한다. "
        "문장은 블로그 초안에 바로 넣을 수 있게 자연스럽게 쓰되, 원문에 없는 사실은 추가하지 마라.\n\n"
        f"{json.dumps(prompt_payload, ensure_ascii=False)}"
    )

    response = httpx.post(
        "https://api.openai.com/v1/responses",
        headers={
            "Authorization": f"Bearer {os.environ['OPENAI_API_KEY']}",
            "Content-Type": "application/json",
        },
        json={
            "model": model,
            "input": f"{system_prompt}\n\n{user_prompt}",
            "max_output_tokens": 3500,
        },
        timeout=60.0,
    )
    response.raise_for_status()
    payload = response.json()
    output_text = _extract_output_text(payload)
    parsed = json.loads(output_text)

    overview = parsed["overview"].strip()
    by_index = {item["index"]: item for item in parsed["items"]}
    digest_items: list[DigestItem] = []
    for index, candidate in enumerate(candidates, start=1):
        item = by_index[index]
        digest_items.append(
            DigestItem(
                candidate=candidate,
                what_changed=item["what_changed"].strip(),
                why_it_matters=item["why_it_matters"].strip(),
                practical_impact=item["practical_impact"].strip(),
            )
        )

    return overview, digest_items, "openai"


def _extract_output_text(payload: dict) -> str:
    """Responses API 응답에서 텍스트 본문만 안전하게 꺼낸다."""

    if payload.get("output_text"):
        return payload["output_text"]

    text_parts: list[str] = []
    for output_item in payload.get("output", []):
        for content in output_item.get("content", []):
            text = content.get("text")
            if text:
                text_parts.append(text)

    return "\n".join(text_parts).strip()


def _summarize_extractive(
    candidates: list[CandidateEntry],
    config: DigestConfig,
    as_of: datetime,
) -> tuple[str, list[DigestItem]]:
    """API 키가 없을 때 제목과 설명 기반 추출형 요약을 만든다."""

    category_counts: dict[str, int] = {}
    for candidate in candidates:
        category_counts[candidate.entry.category] = category_counts.get(candidate.entry.category, 0) + 1

    dominant_categories = [
        config.category_labels.get(category, category)
        for category, _count in sorted(category_counts.items(), key=lambda item: item[1], reverse=True)[:2]
    ]
    categories_text = ", ".join(dominant_categories) if dominant_categories else "주요 플랫폼"
    overview = (
        f"이번 주에는 {categories_text} 영역의 공식 업데이트가 두드러졌습니다. "
        f"아래 다이제스트는 {config.lookback_days}일 내 공개된 공식 changelog, engineering blog, "
        "GitHub Releases를 기준으로 선별했습니다."
    )

    items: list[DigestItem] = []
    for candidate in candidates:
        entry = candidate.entry
        summary_sentence = _summarize_sentence(entry.summary, entry.title)
        items.append(
            DigestItem(
                candidate=candidate,
                what_changed=f"{entry.title} 공지의 핵심은 {summary_sentence}",
                why_it_matters=_build_why_it_matters(entry.category, entry.source_kind, candidate.matched_keywords),
                practical_impact=_build_practical_impact(entry.source_kind, candidate.matched_keywords),
            )
        )

    return overview, items


def _summarize_sentence(summary: str, title: str) -> str:
    """원문 요약에서 가장 앞쪽 문장을 골라 한국어 문단 재료로 만든다."""

    if not summary:
        return f"제목 기준으로 확인된 최신 업데이트입니다."

    shortened = summary.split(". ")[0].strip()
    if len(shortened) < 20:
        return f"{title}와 관련된 최신 업데이트가 공개됐다는 점입니다."
    return shortened.rstrip(".") + "."


def _build_why_it_matters(category: str, source_kind: str, matched_keywords: list[str]) -> str:
    """카테고리와 키워드에 따라 중요도를 설명하는 문장을 만든다."""

    if any(keyword in matched_keywords for keyword in ["security", "breaking", "deprecation", "deprecated"]):
        return "보안이나 호환성 리스크로 이어질 수 있어 기존 서비스와 배포 파이프라인 영향을 우선 점검할 가치가 있습니다."
    if source_kind == "release_api":
        return "공식 릴리즈 단위로 공개된 변경이라 실제 배포나 업그레이드 시점 판단에 바로 활용할 수 있습니다."
    if category == "ai_platform":
        return "모델, API, 플랫폼 정책 변화는 애플리케이션 품질과 비용 구조에 직접 영향을 줄 수 있습니다."
    if category == "web_runtime":
        return "런타임과 프레임워크 변화는 개발 경험과 배포 호환성, 성능 튜닝 포인트를 바꿀 수 있습니다."
    return "공식 제품 채널에서 나온 변화라 로드맵과 운영 정책을 다시 읽어볼 신호로 볼 수 있습니다."


def _build_practical_impact(source_kind: str, matched_keywords: list[str]) -> str:
    """실무 영향과 확인 포인트를 짧게 생성한다."""

    if any(keyword in matched_keywords for keyword in ["security", "breaking"]):
        return "실무에서는 관련 버전 사용 여부를 확인하고, 릴리즈 노트와 마이그레이션 가이드를 기준으로 긴급도부터 판단하는 편이 안전합니다."
    if any(keyword in matched_keywords for keyword in ["deprecation", "deprecated", "migration"]):
        return "기존 코드 경로가 영향을 받는지 확인하고, 대체 API나 설정으로 옮길 계획을 미리 세워두는 것이 좋습니다."
    if any(keyword in matched_keywords for keyword in ["api", "sdk", "model", "support"]):
        return "새 기능을 바로 도입하기보다 샌드박스에서 SDK 버전, 응답 형식, 가격 또는 성능 차이를 먼저 검증하는 흐름이 적절합니다."
    if source_kind == "release_api":
        return "운영 중인 버전과 비교해 패치 범위, 포함된 수정 사항, 회귀 가능성을 릴리즈 노트 기준으로 확인해보면 됩니다."
    return "공식 원문 링크를 기준으로 상세 변경점과 적용 범위를 확인한 뒤, 실제 도입 여부를 팀의 현재 로드맵과 함께 판단하면 됩니다."
