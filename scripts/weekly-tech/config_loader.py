"""주간 최신 기술 다이제스트 설정 파일을 읽고 검증한다."""

from __future__ import annotations

from pathlib import Path

import yaml

from models import DigestConfig, SourceProfile

_SUPPORTED_SOURCE_TYPES = {"rss", "github_releases", "html_listing"}


def load_digest_config(config_path: str | Path) -> DigestConfig:
    """YAML 설정 파일을 읽어 다이제스트 실행 설정으로 변환한다.

    의도:
        실행 초기에 설정 누락과 오타를 잡아 수집 도중에 원인을 알기
        어려운 실패가 늦게 터지지 않도록 한다.

    Args:
        config_path: `data/weekly-tech/sources.yml` 경로.

    Returns:
        검증을 마친 DigestConfig 객체.

    Raises:
        FileNotFoundError: 설정 파일이 존재하지 않을 때 발생한다.
        ValueError: 필수 필드가 없거나 지원하지 않는 source type이 있을 때 발생한다.
    """

    path = Path(config_path)
    raw = yaml.safe_load(path.read_text(encoding="utf-8"))

    global_config = raw.get("global", {})
    post_config = global_config.get("post", {})
    sources = [_build_source_profile(item) for item in raw.get("sources", [])]

    if not sources:
        raise ValueError("최소 1개 이상의 소스를 sources.yml에 등록해야 합니다.")

    return DigestConfig(
        timezone=global_config["timezone"],
        lookback_days=int(global_config["lookback_days"]),
        max_items=int(global_config["max_items"]),
        min_items=int(global_config["min_items"]),
        max_items_per_source=int(global_config.get("max_items_per_source", 2)),
        summary_mode=str(global_config.get("summary_mode", "auto")),
        category_labels=dict(global_config["category_labels"]),
        category_quotas={key: int(value) for key, value in global_config["category_quotas"].items()},
        post_categories=list(post_config["categories"]),
        post_tags=list(post_config["tags"]),
        slug_prefix=str(post_config["slug_prefix"]),
        include_keywords=[keyword.lower() for keyword in global_config.get("include_keywords", [])],
        exclude_keywords=[keyword.lower() for keyword in global_config.get("exclude_keywords", [])],
        sources=sources,
    )


def _build_source_profile(raw_source: dict) -> SourceProfile:
    """원시 소스 설정 딕셔너리를 SourceProfile로 바꾼다."""

    source_type = raw_source["source_type"]
    if source_type not in _SUPPORTED_SOURCE_TYPES:
        raise ValueError(f"지원하지 않는 source_type입니다: {source_type}")

    if source_type in {"rss", "html_listing"} and not raw_source.get("url"):
        raise ValueError(f"{raw_source['id']} 소스는 url이 필요합니다.")
    if source_type == "github_releases" and not raw_source.get("repo"):
        raise ValueError(f"{raw_source['id']} 소스는 repo가 필요합니다.")

    return SourceProfile(
        id=str(raw_source["id"]),
        name=str(raw_source["name"]),
        source_type=source_type,
        source_kind=str(raw_source["source_kind"]),
        category=str(raw_source["category"]),
        enabled=bool(raw_source.get("enabled", True)),
        weight=float(raw_source.get("weight", 1.0)),
        url=raw_source.get("url"),
        repo=raw_source.get("repo"),
        item_selector=raw_source.get("item_selector"),
        title_selector=raw_source.get("title_selector"),
        date_selector=raw_source.get("date_selector"),
        link_prefix=raw_source.get("link_prefix"),
        include_keywords=[keyword.lower() for keyword in raw_source.get("include_keywords", [])],
        exclude_keywords=[keyword.lower() for keyword in raw_source.get("exclude_keywords", [])],
    )
