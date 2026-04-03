"""수집 결과를 Jekyll용 Markdown 포스트로 렌더링한다."""

from __future__ import annotations

from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

from models import DigestConfig, DigestItem


def render_weekly_post(
    overview: str,
    digest_items: list[DigestItem],
    config: DigestConfig,
    as_of: datetime,
) -> tuple[Path, str]:
    """다이제스트 요약과 항목 목록을 Jekyll 포스트 Markdown으로 만든다.

    의도:
        자동 수집 결과를 사람이 다시 포맷팅하지 않아도 바로 `_posts/`에
        넣을 수 있게 front matter와 본문 구조를 일관되게 생성한다.

    Args:
        overview: 글 도입부에 들어갈 전체 요약 문단.
        digest_items: 최종 글에 포함할 항목 목록.
        config: 카테고리 레이블과 포스트 메타데이터를 가진 설정.
        as_of: 파일명과 날짜 front matter에 사용할 기준 시각.

    Returns:
        생성 파일 경로와 Markdown 문자열의 튜플.
    """

    local_now = as_of.astimezone(ZoneInfo(config.timezone))
    start_date = local_now.date() - timedelta(days=config.lookback_days - 1)
    title = f"이번 주 최신 IT 개발 기술 동향 ({start_date.isoformat()} ~ {local_now.date().isoformat()})"
    excerpt = overview[:150].rstrip()
    file_path = Path("_posts") / f"{local_now.date().isoformat()}-{config.slug_prefix}.md"

    grouped_items: dict[str, list[DigestItem]] = defaultdict(list)
    for item in digest_items:
        grouped_items[item.candidate.entry.category].append(item)

    lines: list[str] = [
        "---",
        f'title: "{title}"',
        f"date: {local_now.strftime('%Y-%m-%d %H:%M:%S %z')}",
        "categories:",
    ]
    for category in config.post_categories:
        lines.append(f"  - {category}")
    lines.extend(["tags:"])
    for tag in config.post_tags:
        lines.append(f"  - {tag}")
    lines.extend(
        [
            f'excerpt: "{_escape_yaml(excerpt)}"',
            "---",
            "",
            overview,
            "",
            "## 이번 주 선정 기준",
            "",
            f"- 수집 기간: {start_date.isoformat()} ~ {local_now.date().isoformat()}",
            "- 공식 changelog, engineering blog, GitHub Releases API만 대상으로 삼았습니다.",
            "- 릴리즈, 보안, deprecation, API/SDK 업데이트 중심으로 선별했습니다.",
            "- 자동 생성 초안이므로 원문 링크와 릴리즈 노트를 함께 확인하는 것을 권장합니다.",
            "",
        ]
    )

    for category in config.category_quotas:
        items = grouped_items.get(category)
        if not items:
            continue

        lines.extend([f"## {config.category_labels.get(category, category)}", ""])
        for item in items:
            entry = item.candidate.entry
            lines.extend(
                [
                    f"### {entry.title}",
                    "",
                    f"- 출처: **{entry.source_name}**",
                    f"- 발행일: {entry.published_at.astimezone(ZoneInfo(config.timezone)).strftime('%Y-%m-%d %H:%M %Z')}",
                    f"- 원문 링크: [{entry.url}]({entry.url})",
                    f"- 무슨 변화인가: {item.what_changed}",
                    f"- 왜 중요한가: {item.why_it_matters}",
                    f"- 실무 영향: {item.practical_impact}",
                    "",
                ]
            )

    lines.extend(
        [
            "## 마무리",
            "",
            "이번 주 글은 공식 소스 기반 자동 수집과 요약 파이프라인으로 생성한 초안입니다. "
            "다음 주부터는 소스 품질과 quota를 계속 다듬으면서 더 안정적인 주간 발행 흐름으로 가져갈 예정입니다.",
            "",
        ]
    )

    return file_path, "\n".join(lines)


def _escape_yaml(text: str) -> str:
    """YAML 문자열 안에서 문제가 되는 큰따옴표를 이스케이프한다."""

    return text.replace('"', '\\"')
