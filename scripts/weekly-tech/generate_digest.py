"""주간 최신 기술 다이제스트 생성 CLI 엔트리포인트다."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict
from datetime import UTC, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from collector import collect_entries, select_candidates
from config_loader import load_digest_config
from models import RunMetadata
from renderer import render_weekly_post
from summarizer import summarize_candidates


def main() -> int:
    """설정 파일을 읽어 주간 다이제스트를 생성하고 실행 결과를 기록한다.

    의도:
        로컬 실행과 GitHub Actions에서 같은 진입점으로 전체 파이프라인을
        호출할 수 있게 해 운영 경로를 하나로 유지한다.

    Args:
        없음. CLI 인자를 통해 설정 경로와 출력 위치를 받는다.

    Returns:
        정상 처리 시 0, 실행 오류 시 1을 반환한다.
    """

    parser = argparse.ArgumentParser(description="Generate weekly tech digest post.")
    parser.add_argument(
        "--config",
        default="data/weekly-tech/sources.yml",
        help="YAML configuration path for official sources.",
    )
    parser.add_argument(
        "--output-dir",
        default="data/weekly-tech/output",
        help="Directory to write run metadata.",
    )
    parser.add_argument(
        "--as-of",
        default=None,
        help="ISO8601 datetime override for reproducible runs.",
    )
    parser.add_argument(
        "--write-post",
        action="store_true",
        help="Actually write the generated markdown under _posts.",
    )
    args = parser.parse_args()

    config = load_digest_config(args.config)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    as_of = _resolve_as_of(args.as_of, config.timezone)
    started_at = datetime.now(tz=UTC)

    entries, failures = collect_entries(config, as_of)
    candidates = select_candidates(entries, config, as_of)

    if len(candidates) < config.min_items:
        metadata = RunMetadata(
            started_at=started_at,
            summary_mode_used="none",
            collected_count=len(entries),
            selected_count=len(candidates),
            failed_sources=failures,
            selected_urls=[candidate.entry.url for candidate in candidates],
            post_path=None,
        )
        _write_run_metadata(output_dir, metadata)
        print(f"선택된 항목 수가 최소 기준({config.min_items})보다 적어 포스트를 만들지 않았습니다.")
        return 0

    overview, digest_items, summary_mode_used = summarize_candidates(candidates, config, as_of)
    post_path, markdown = render_weekly_post(overview, digest_items, config, as_of)

    written_post_path: str | None = None
    if args.write_post:
        post_path.parent.mkdir(parents=True, exist_ok=True)
        post_path.write_text(markdown, encoding="utf-8")
        written_post_path = str(post_path)

    metadata = RunMetadata(
        started_at=started_at,
        summary_mode_used=summary_mode_used,
        collected_count=len(entries),
        selected_count=len(candidates),
        failed_sources=failures,
        selected_urls=[candidate.entry.url for candidate in candidates],
        post_path=written_post_path,
    )
    _write_run_metadata(output_dir, metadata, markdown if written_post_path else None)

    print(f"COLLECTED_COUNT={len(entries)}")
    print(f"SELECTED_COUNT={len(candidates)}")
    print(f"SUMMARY_MODE_USED={summary_mode_used}")
    print(f"POST_PATH={written_post_path or ''}")
    return 0


def _resolve_as_of(raw_value: str | None, timezone_name: str) -> datetime:
    """CLI 입력 또는 현재 시각으로 기준 시각을 결정한다."""

    if raw_value:
        parsed = datetime.fromisoformat(raw_value)
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=ZoneInfo(timezone_name))
        return parsed.astimezone(UTC)

    return datetime.now(tz=ZoneInfo(timezone_name)).astimezone(UTC)


def _write_run_metadata(output_dir: Path, metadata: RunMetadata, markdown_preview: str | None = None) -> None:
    """실행 메타데이터와 미리보기를 JSON 파일로 남긴다."""

    payload = asdict(metadata)
    payload["started_at"] = metadata.started_at.isoformat()
    latest_run_path = output_dir / "latest-run.json"
    latest_run_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    if markdown_preview:
        (output_dir / "latest-preview.md").write_text(markdown_preview, encoding="utf-8")


if __name__ == "__main__":
    sys.exit(main())
