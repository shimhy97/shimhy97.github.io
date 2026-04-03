"""공식 소스 수집과 후보 선별 로직을 제공한다."""

from __future__ import annotations

import json
import re
from collections import defaultdict
from datetime import UTC, datetime, timedelta
from email.utils import parsedate_to_datetime
from urllib.parse import urljoin, urlparse

import feedparser
import httpx
from bs4 import BeautifulSoup
from dateutil import parser as date_parser

from models import CandidateEntry, CollectedEntry, DigestConfig, SourceProfile

_KIND_WEIGHTS = {
    "release_api": 5.0,
    "changelog": 4.0,
    "blog": 2.0,
}

_KEYWORD_BONUSES = {
    "security": 3.0,
    "breaking": 3.0,
    "deprecation": 3.0,
    "deprecated": 3.0,
    "release": 2.0,
    "released": 2.0,
    "launch": 2.0,
    "preview": 2.0,
    "beta": 2.0,
    "availability": 2.0,
    "general availability": 2.0,
    "migration": 2.0,
    "api": 1.0,
    "sdk": 1.0,
    "model": 1.0,
    "support": 1.0,
}


def collect_entries(
    config: DigestConfig,
    as_of: datetime,
    client: httpx.Client | None = None,
) -> tuple[list[CollectedEntry], list[dict[str, str]]]:
    """활성화된 공식 소스를 순회하며 최근 항목을 정규화한다.

    의도:
        서로 다른 원천을 돌면서 실패는 실패대로 기록하고, 성공한 항목은
        공통 스키마로 모아 후속 선별 단계를 단순하게 만든다.

    Args:
        config: 전역 quota와 소스 목록이 들어 있는 설정 객체.
        as_of: lookback 계산 기준 시각.
        client: 재사용 가능한 HTTP 클라이언트. 생략 시 내부에서 생성한다.

    Returns:
        수집된 CollectedEntry 목록과 실패 소스 요약 목록의 튜플.
    """

    owns_client = client is None
    http_client = client or httpx.Client(
        follow_redirects=True,
        timeout=20.0,
        headers={
            "User-Agent": "shimhy97-weekly-tech-digest/1.0 (+https://github.com/shimhy97/shimhy97.github.io)",
            "Accept": "application/json, application/rss+xml, application/xml, text/xml, text/html;q=0.9",
        },
    )

    collected: list[CollectedEntry] = []
    failures: list[dict[str, str]] = []

    try:
        for source in config.sources:
            if not source.enabled:
                continue

            try:
                if source.source_type == "rss":
                    collected.extend(_collect_from_rss(source, as_of, config.lookback_days, http_client))
                elif source.source_type == "github_releases":
                    collected.extend(_collect_from_github_releases(source, as_of, config.lookback_days, http_client))
                elif source.source_type == "html_listing":
                    collected.extend(_collect_from_html_listing(source, as_of, config.lookback_days, http_client))
            except Exception as exc:  # noqa: BLE001
                failures.append({"source_id": source.id, "source_name": source.name, "error": str(exc)})
    finally:
        if owns_client:
            http_client.close()

    return collected, failures


def select_candidates(
    entries: list[CollectedEntry],
    config: DigestConfig,
    as_of: datetime,
) -> list[CandidateEntry]:
    """수집 항목을 중복 제거하고 quota에 맞춰 최종 후보로 압축한다.

    의도:
        changelog와 release, blog가 섞여 들어온 원시 항목을 운영자가 검토할
        만한 크기의 다이제스트 후보 집합으로 줄인다.

    Args:
        entries: 정규화된 원시 수집 항목 목록.
        config: include/exclude 규칙과 quota를 가진 설정.
        as_of: recency bonus 계산 기준 시각.

    Returns:
        점수와 dedupe key가 붙은 CandidateEntry 목록.
    """

    filtered: list[CandidateEntry] = []
    source_keyword_map = {
        source.id: {
            "include": source.include_keywords,
            "exclude": source.exclude_keywords,
        }
        for source in config.sources
    }
    for entry in entries:
        source_keywords = source_keyword_map.get(entry.source_id, {"include": [], "exclude": []})
        include_hits = _matched_keywords(
            entry.title,
            entry.summary,
            config.include_keywords + source_keywords["include"],
        )
        matched_keywords = [keyword for keyword in include_hits if keyword in _KEYWORD_BONUSES]
        if _should_exclude(entry, config.exclude_keywords + source_keywords["exclude"]):
            continue

        # 블로그성 글은 변경 신호가 없으면 우선 제외해 마케팅 글 유입을 줄인다.
        if entry.source_kind == "blog" and not include_hits:
            continue

        filtered.append(
            CandidateEntry(
                entry=entry,
                score=_compute_score(entry, matched_keywords, as_of),
                matched_keywords=matched_keywords,
                dedupe_key=_build_dedupe_key(entry),
            )
        )

    deduped = _deduplicate(filtered)
    if not deduped:
        return []

    by_category: dict[str, list[CandidateEntry]] = defaultdict(list)
    for candidate in deduped:
        by_category[candidate.entry.category].append(candidate)

    for candidates in by_category.values():
        candidates.sort(key=lambda item: (-item.score, -item.entry.published_at.timestamp()))

    selected: list[CandidateEntry] = []
    selected_keys: set[str] = set()
    source_counts: dict[str, int] = defaultdict(int)

    # 카테고리별 quota를 먼저 채워 한 주가 특정 제품군으로 쏠리지 않게 한다.
    for category, quota in config.category_quotas.items():
        for candidate in sorted(by_category.get(category, []), key=lambda item: (-item.score, -item.entry.published_at.timestamp())):
            # quota 단계에서는 최신성과 점수를 함께 보고 대표 항목을 먼저 선발한다.
            if len([item for item in selected if item.entry.category == category]) >= quota:
                break
            if candidate.dedupe_key in selected_keys:
                continue
            if source_counts[candidate.entry.source_id] >= config.max_items_per_source:
                continue
            selected.append(candidate)
            selected_keys.add(candidate.dedupe_key)
            source_counts[candidate.entry.source_id] += 1

    if len(selected) < config.max_items:
        remaining = sorted(
            [candidate for candidate in deduped if candidate.dedupe_key not in selected_keys],
            key=lambda item: (-item.score, -item.entry.published_at.timestamp()),
        )
        for candidate in remaining:
            if len(selected) >= config.max_items:
                break
            if source_counts[candidate.entry.source_id] >= config.max_items_per_source:
                continue
            selected.append(candidate)
            selected_keys.add(candidate.dedupe_key)
            source_counts[candidate.entry.source_id] += 1

    selected.sort(key=lambda item: (-item.score, -item.entry.published_at.timestamp()))
    return selected[: config.max_items]


def _collect_from_rss(
    source: SourceProfile,
    as_of: datetime,
    lookback_days: int,
    client: httpx.Client,
) -> list[CollectedEntry]:
    """RSS 또는 Atom 피드에서 최근 항목을 수집한다."""

    response = client.get(source.url)
    response.raise_for_status()
    feed = feedparser.parse(response.text)
    threshold = as_of - timedelta(days=lookback_days)

    entries: list[CollectedEntry] = []
    for raw_entry in feed.entries:
        published_at = _parse_datetime(
            raw_entry.get("published")
            or raw_entry.get("updated")
            or raw_entry.get("created")
        )
        if not published_at or published_at < threshold:
            continue

        summary = _clean_text(
            raw_entry.get("summary")
            or raw_entry.get("description")
            or raw_entry.get("title")
            or ""
        )
        link = raw_entry.get("link")
        title = _clean_text(raw_entry.get("title") or "")
        if not link or not title:
            continue

        entries.append(
            CollectedEntry(
                source_id=source.id,
                source_name=source.name,
                source_type=source.source_type,
                source_kind=source.source_kind,
                category=source.category,
                title=title,
                url=link,
                published_at=published_at,
                summary=summary,
                weight=source.weight,
            )
        )

    return entries


def _collect_from_github_releases(
    source: SourceProfile,
    as_of: datetime,
    lookback_days: int,
    client: httpx.Client,
) -> list[CollectedEntry]:
    """GitHub Releases API에서 최근 릴리즈 정보를 수집한다."""

    response = client.get(
        f"https://api.github.com/repos/{source.repo}/releases",
        params={"per_page": 12},
        headers={"Accept": "application/vnd.github+json"},
    )
    response.raise_for_status()
    payload = response.json()
    threshold = as_of - timedelta(days=lookback_days)

    entries: list[CollectedEntry] = []
    for release in payload:
        if release.get("draft"):
            continue

        published_at = _parse_datetime(release.get("published_at") or release.get("created_at"))
        if not published_at or published_at < threshold:
            continue

        summary = _clean_text(release.get("body") or "")
        title = _clean_text(release.get("name") or release.get("tag_name") or "")
        link = release.get("html_url")
        if not title or not link:
            continue

        entries.append(
            CollectedEntry(
                source_id=source.id,
                source_name=source.name,
                source_type=source.source_type,
                source_kind=source.source_kind,
                category=source.category,
                title=title,
                url=link,
                published_at=published_at,
                summary=summary,
                weight=source.weight,
            )
        )

    return entries


def _collect_from_html_listing(
    source: SourceProfile,
    as_of: datetime,
    lookback_days: int,
    client: httpx.Client,
) -> list[CollectedEntry]:
    """HTML listing 페이지에서 기사 링크를 모아 최근 항목을 수집한다."""

    response = client.get(source.url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    threshold = as_of - timedelta(days=lookback_days)

    entries: list[CollectedEntry] = []
    seen_urls: set[str] = set()

    for node in soup.select(source.item_selector or "a")[:30]:
        anchor = node if node.name == "a" else node.find("a")
        if not anchor:
            continue

        href = anchor.get("href")
        if not href:
            continue

        article_url = urljoin(source.link_prefix or source.url or "", href)
        if article_url in seen_urls:
            continue
        seen_urls.add(article_url)

        title = _clean_text(anchor.get_text(" ", strip=True))
        if source.title_selector:
            title_node = node.select_one(source.title_selector)
            if title_node:
                title = _clean_text(title_node.get_text(" ", strip=True))

        article_published_at, article_summary, canonical_url = _fetch_article_metadata(article_url, client)
        if not article_published_at or article_published_at < threshold:
            continue

        entries.append(
            CollectedEntry(
                source_id=source.id,
                source_name=source.name,
                source_type=source.source_type,
                source_kind=source.source_kind,
                category=source.category,
                title=title,
                url=canonical_url or article_url,
                published_at=article_published_at,
                summary=article_summary,
                weight=source.weight,
            )
        )

    return entries


def _fetch_article_metadata(article_url: str, client: httpx.Client) -> tuple[datetime | None, str, str | None]:
    """개별 기사 페이지에서 발행일과 요약을 추출한다."""

    response = client.get(article_url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    canonical = soup.find("link", rel="canonical")
    canonical_url = canonical.get("href") if canonical else None

    published_at = None
    meta_candidates = [
        ("property", "article:published_time"),
        ("name", "publish_date"),
        ("name", "date"),
        ("property", "og:published_time"),
    ]
    for attr_name, attr_value in meta_candidates:
        tag = soup.find("meta", attrs={attr_name: attr_value})
        if tag and tag.get("content"):
            published_at = _parse_datetime(tag["content"])
            if published_at:
                break

    if not published_at:
        time_tag = soup.find("time")
        if time_tag and time_tag.get("datetime"):
            published_at = _parse_datetime(time_tag["datetime"])

    if not published_at:
        published_at = _parse_date_from_json_ld(soup)

    summary = ""
    description = soup.find("meta", attrs={"name": "description"}) or soup.find(
        "meta",
        attrs={"property": "og:description"},
    )
    if description and description.get("content"):
        summary = _clean_text(description["content"])
    if not summary:
        paragraph = soup.find("p")
        if paragraph:
            summary = _clean_text(paragraph.get_text(" ", strip=True))

    return published_at, summary, canonical_url


def _parse_date_from_json_ld(soup: BeautifulSoup) -> datetime | None:
    """JSON-LD 안에 들어 있는 datePublished를 찾아 datetime으로 바꾼다."""

    for script in soup.find_all("script", attrs={"type": "application/ld+json"}):
        try:
            payload = json.loads(script.get_text())
        except json.JSONDecodeError:
            continue

        for node in _walk_json_nodes(payload):
            date_value = node.get("datePublished")
            if date_value:
                parsed = _parse_datetime(date_value)
                if parsed:
                    return parsed

    return None


def _walk_json_nodes(payload: object) -> list[dict]:
    """중첩된 JSON-LD를 평탄화해 딕셔너리 노드만 반환한다."""

    nodes: list[dict] = []
    if isinstance(payload, dict):
        nodes.append(payload)
        for value in payload.values():
            nodes.extend(_walk_json_nodes(value))
    elif isinstance(payload, list):
        for item in payload:
            nodes.extend(_walk_json_nodes(item))
    return nodes


def _should_exclude(entry: CollectedEntry, exclude_keywords: list[str]) -> bool:
    """전역 및 소스별 exclude 규칙으로 후보 제외 여부를 판단한다."""

    haystack = f"{entry.title}\n{entry.summary}".lower()
    for keyword in exclude_keywords:
        if keyword in haystack:
            return True
    return False


def _matched_keywords(title: str, summary: str, include_keywords: list[str]) -> list[str]:
    """제목과 요약에서 중요 키워드를 찾아 점수 계산용 목록을 만든다."""

    haystack = f"{title}\n{summary}".lower()
    matched = [keyword for keyword in include_keywords if keyword in haystack]
    # 점수 계산은 사전에 정의한 중요 키워드만 사용하되, filtering은 설정 키워드 전체를 사용한다.
    return [keyword for keyword in matched if keyword in _KEYWORD_BONUSES]


def _compute_score(entry: CollectedEntry, matched_keywords: list[str], as_of: datetime) -> float:
    """카테고리 quota 적용 전에 사용할 우선도 점수를 계산한다."""

    score = _KIND_WEIGHTS.get(entry.source_kind, 1.0) + entry.weight
    age = as_of - entry.published_at
    if age <= timedelta(days=2):
        score += 3.0
    elif age <= timedelta(days=4):
        score += 2.0
    else:
        score += 1.0

    # 키워드 보너스는 중복 가산을 허용하되, 과도하게 치우치지 않도록 상한을 둔다.
    score += min(sum(_KEYWORD_BONUSES[keyword] for keyword in matched_keywords), 6.0)
    return round(score, 2)


def _deduplicate(candidates: list[CandidateEntry]) -> list[CandidateEntry]:
    """URL과 제목 기반 정규화 키로 중복 항목을 병합한다."""

    deduped: dict[str, CandidateEntry] = {}
    for candidate in sorted(candidates, key=lambda item: (-item.score, -item.entry.published_at.timestamp())):
        existing = deduped.get(candidate.dedupe_key)
        if not existing:
            deduped[candidate.dedupe_key] = candidate
            continue

        if len(candidate.entry.summary) > len(existing.entry.summary):
            deduped[candidate.dedupe_key] = candidate

    return list(deduped.values())


def _build_dedupe_key(entry: CollectedEntry) -> str:
    """URL과 제목을 정규화해 중복 제거용 키를 만든다."""

    parsed = urlparse(entry.url)
    normalized_url = f"{parsed.netloc}{parsed.path}".rstrip("/").lower()
    normalized_title = re.sub(r"[^a-z0-9]+", "-", entry.title.lower()).strip("-")
    if normalized_url:
        return normalized_url
    return normalized_title


def _parse_datetime(raw_value: str | None) -> datetime | None:
    """여러 날짜 문자열 형식을 UTC aware datetime으로 바꾼다."""

    if not raw_value:
        return None

    try:
        parsed = parsedate_to_datetime(raw_value)
    except (TypeError, ValueError, IndexError):
        try:
            parsed = date_parser.parse(raw_value)
        except (TypeError, ValueError, OverflowError):
            return None

    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=UTC)
    return parsed.astimezone(UTC)


def _clean_text(raw_text: str) -> str:
    """HTML과 과도한 공백을 제거해 요약 문장 재료로 정리한다."""

    if not raw_text:
        return ""

    soup = BeautifulSoup(raw_text, "html.parser")
    text = soup.get_text(" ", strip=True)
    text = re.sub(r"\s+", " ", text)
    return text.strip()
