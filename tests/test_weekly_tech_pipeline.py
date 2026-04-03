"""주간 다이제스트 파이프라인의 핵심 선별 규칙을 검증한다."""

from __future__ import annotations

import sys
import unittest
from datetime import UTC, datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts/weekly-tech"))

from collector import select_candidates  # noqa: E402
from models import CollectedEntry, DigestConfig, SourceProfile  # noqa: E402
from renderer import render_weekly_post  # noqa: E402
from summarizer import summarize_candidates  # noqa: E402


def _build_config() -> DigestConfig:
    return DigestConfig(
        timezone="Asia/Seoul",
        lookback_days=7,
        max_items=4,
        min_items=2,
        max_items_per_source=1,
        summary_mode="extractive",
        category_labels={
            "ai_platform": "AI / LLM 플랫폼",
            "web_runtime": "웹 / 프론트엔드 / 런타임",
            "cloud_devtools": "클라우드 / DevTools / 플랫폼",
            "oss_release": "OSS 릴리즈 / 보안",
        },
        category_quotas={
            "ai_platform": 1,
            "web_runtime": 1,
            "cloud_devtools": 1,
            "oss_release": 1,
        },
        post_categories=["weekly", "roundup"],
        post_tags=["weekly-digest"],
        slug_prefix="weekly-tech-roundup",
        include_keywords=["release", "api", "security", "breaking", "launch"],
        exclude_keywords=["event"],
        sources=[
            SourceProfile(
                id="dummy",
                name="Dummy",
                source_type="rss",
                source_kind="blog",
                category="web_runtime",
                enabled=True,
            )
        ],
    )


def _build_entry(
    *,
    title: str,
    category: str,
    source_kind: str,
    days_ago: int = 1,
    summary: str = "New release adds API support.",
    url: str | None = None,
) -> CollectedEntry:
    return CollectedEntry(
        source_id=f"{category}-{title}",
        source_name=f"{category} Source",
        source_type="rss",
        source_kind=source_kind,
        category=category,
        title=title,
        url=url or f"https://example.com/{title.replace(' ', '-').lower()}",
        published_at=datetime.now(tz=UTC) - timedelta(days=days_ago),
        summary=summary,
        weight=1.0,
    )


class WeeklyTechPipelineTest(unittest.TestCase):
    """주간 다이제스트 파이프라인 핵심 동작을 검증한다."""

    def test_select_candidates_respects_category_quota(self) -> None:
        """카테고리 quota를 먼저 채워 대표 항목이 빠지지 않게 한다.

        의도:
            특정 카테고리 항목이 많아도 quota를 먼저 적용해 주간 글이 한쪽으로
            쏠리지 않게 만드는 선별 규칙을 검증한다.

        Args:
            없음.

        Returns:
            없음.
        """

        config = _build_config()
        as_of = datetime.now(tz=UTC)
        entries = [
            _build_entry(title="High release", category="oss_release", source_kind="release_api"),
            _build_entry(title="Web runtime API update", category="web_runtime", source_kind="blog"),
            _build_entry(title="Cloud platform changelog", category="cloud_devtools", source_kind="changelog"),
            _build_entry(title="Model support launch", category="ai_platform", source_kind="blog"),
            _build_entry(title="Second OSS release", category="oss_release", source_kind="release_api"),
        ]

        candidates = select_candidates(entries, config, as_of)
        categories = [candidate.entry.category for candidate in candidates]

        self.assertIn("ai_platform", categories)
        self.assertIn("web_runtime", categories)
        self.assertIn("cloud_devtools", categories)
        self.assertEqual(categories.count("oss_release"), 1)

    def test_render_weekly_post_outputs_jekyll_front_matter(self) -> None:
        """렌더러가 Jekyll front matter와 본문 섹션을 생성해야 한다.

        의도:
            자동 생성 결과가 블로그 빌드에 바로 들어갈 수 있는 형식을 갖추는지
            확인한다.

        Args:
            없음.

        Returns:
            없음.
        """

        config = _build_config()
        as_of = datetime(2026, 4, 3, 9, 0, tzinfo=UTC)
        entries = [
            _build_entry(
                title="Security release",
                category="oss_release",
                source_kind="release_api",
                summary="Security release adds patch support.",
            ),
            _build_entry(
                title="API launch",
                category="ai_platform",
                source_kind="blog",
                summary="API launch introduces new model support.",
            ),
        ]

        candidates = select_candidates(entries, config, as_of)
        overview, digest_items, _mode = summarize_candidates(candidates, config, as_of)
        path, markdown = render_weekly_post(overview, digest_items, config, as_of)

        self.assertTrue(str(path).endswith("2026-04-03-weekly-tech-roundup.md"))
        self.assertTrue(markdown.startswith("---"))
        self.assertIn("## 이번 주 선정 기준", markdown)
        self.assertIn("원문 링크", markdown)


if __name__ == "__main__":
    unittest.main()
