"""주간 최신 기술 다이제스트 파이프라인의 공통 데이터 구조를 정의한다."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime


@dataclass(slots=True)
class SourceProfile:
    """공식 소스 하나의 설정 정보를 보관한다.

    의도:
        RSS, GitHub Releases API, HTML listing 등 서로 다른 수집 원천을
        동일한 설정 객체로 다뤄 수집기 선택과 가중치 계산을 단순화한다.

    Args:
        id: 설정 파일 안에서 소스를 식별하는 고유 ID.
        name: 블로그 글과 로그에 노출할 소스 이름.
        source_type: `rss`, `github_releases`, `html_listing` 중 하나.
        source_kind: `blog`, `changelog`, `release_api` 같은 성격 구분.
        category: quota 계산에 사용할 상위 분류.
        enabled: 수집 대상 포함 여부.
        weight: 기본 점수 보정값.
        url: RSS 또는 listing 원본 URL.
        repo: GitHub Releases API용 `owner/repo`.
        item_selector: HTML listing에서 항목을 찾는 CSS selector.
        title_selector: listing 항목 안에서 제목을 보강할 selector.
        date_selector: listing 항목 안에서 날짜를 직접 읽고 싶을 때 쓸 selector.
        link_prefix: 상대 경로 링크를 절대 경로로 바꿀 때 붙일 prefix.
        include_keywords: 전역 include 규칙 외에 추가할 키워드.
        exclude_keywords: 전역 exclude 규칙 외에 추가할 키워드.

    Returns:
        SourceProfile 인스턴스.
    """

    id: str
    name: str
    source_type: str
    source_kind: str
    category: str
    enabled: bool
    weight: float = 1.0
    url: str | None = None
    repo: str | None = None
    item_selector: str | None = None
    title_selector: str | None = None
    date_selector: str | None = None
    link_prefix: str | None = None
    include_keywords: list[str] = field(default_factory=list)
    exclude_keywords: list[str] = field(default_factory=list)


@dataclass(slots=True)
class DigestConfig:
    """주간 다이제스트 전체 실행 설정을 보관한다.

    의도:
        소스 목록과 quota, 포스트 메타데이터를 한 객체로 묶어 CLI와
        수집기, 렌더러가 동일한 기준을 공유하게 한다.

    Args:
        timezone: 발행 날짜와 lookback 계산에 사용할 시간대.
        lookback_days: 최근 며칠을 수집 대상으로 삼을지 나타내는 값.
        max_items: 최종 글에 허용할 최대 항목 수.
        min_items: 글을 생성하기 위한 최소 항목 수.
        max_items_per_source: 같은 source_id에서 허용할 최대 항목 수.
        summary_mode: `auto`, `openai`, `extractive` 중 하나.
        category_labels: 카테고리 코드와 화면 노출 이름의 매핑.
        category_quotas: 카테고리별 최대 선발 수.
        post_categories: Jekyll front matter의 categories 값.
        post_tags: Jekyll front matter의 tags 값.
        slug_prefix: 포스트 파일명 접두사.
        include_keywords: 전역 include 키워드 목록.
        exclude_keywords: 전역 exclude 키워드 목록.
        sources: 활성/비활성 소스를 포함한 전체 설정 목록.

    Returns:
        DigestConfig 인스턴스.
    """

    timezone: str
    lookback_days: int
    max_items: int
    min_items: int
    max_items_per_source: int
    summary_mode: str
    category_labels: dict[str, str]
    category_quotas: dict[str, int]
    post_categories: list[str]
    post_tags: list[str]
    slug_prefix: str
    include_keywords: list[str]
    exclude_keywords: list[str]
    sources: list[SourceProfile]


@dataclass(slots=True)
class CollectedEntry:
    """정규화된 수집 항목 한 건을 표현한다.

    의도:
        소스별로 다른 필드 구조를 공통 형태로 맞춰 이후 점수 계산과
        중복 제거를 단순하게 만든다.

    Args:
        source_id: 항목을 가져온 소스 ID.
        source_name: 사람에게 보이는 소스 이름.
        source_type: 수집 방식.
        source_kind: blog/changelog/release_api 구분.
        category: quota 계산용 카테고리.
        title: 항목 제목.
        url: 원문 링크.
        published_at: 게시 시각.
        summary: 항목 요약 또는 설명 본문.
        weight: 소스 가중치.

    Returns:
        CollectedEntry 인스턴스.
    """

    source_id: str
    source_name: str
    source_type: str
    source_kind: str
    category: str
    title: str
    url: str
    published_at: datetime
    summary: str
    weight: float


@dataclass(slots=True)
class CandidateEntry:
    """다이제스트 후보로 선별된 항목을 표현한다.

    의도:
        수집 항목에 점수와 선발 사유를 부여해 최종 글에 어떤 기준으로
        포함되었는지 추적할 수 있게 한다.

    Args:
        entry: 원본 수집 항목.
        score: 정렬과 quota 적용에 사용할 최종 점수.
        matched_keywords: 점수 계산에 사용된 주요 키워드 목록.
        dedupe_key: 중복 제거에 사용한 정규화 키.

    Returns:
        CandidateEntry 인스턴스.
    """

    entry: CollectedEntry
    score: float
    matched_keywords: list[str]
    dedupe_key: str


@dataclass(slots=True)
class DigestItem:
    """최종 포스트에 들어갈 요약 문단 한 묶음을 보관한다.

    의도:
        수집 데이터와 한국어 요약 문장을 같이 보관해 Markdown 렌더링을
        단순한 문자열 조합으로 끝낼 수 있게 한다.

    Args:
        candidate: 원본 후보 항목.
        what_changed: 무엇이 바뀌었는지 설명하는 문단.
        why_it_matters: 왜 중요한지 설명하는 문단.
        practical_impact: 실무 영향과 확인 포인트를 설명하는 문단.

    Returns:
        DigestItem 인스턴스.
    """

    candidate: CandidateEntry
    what_changed: str
    why_it_matters: str
    practical_impact: str


@dataclass(slots=True)
class RunMetadata:
    """주간 실행 결과를 파일과 로그로 남기기 위한 메타데이터다.

    의도:
        수집 실패, 선발 수, 생성 파일 경로를 구조적으로 남겨
        GitHub Actions artifact와 운영 점검에 재사용한다.

    Args:
        started_at: 실행 시작 시각.
        summary_mode_used: 실제 사용된 요약 방식.
        collected_count: 수집된 전체 항목 수.
        selected_count: 최종 선별된 항목 수.
        failed_sources: 실패한 소스 요약 목록.
        selected_urls: 최종 채택된 원문 URL 목록.
        post_path: 생성된 포스트 경로. 생성 실패 시 `None`.

    Returns:
        RunMetadata 인스턴스.
    """

    started_at: datetime
    summary_mode_used: str
    collected_count: int
    selected_count: int
    failed_sources: list[dict[str, str]]
    selected_urls: list[str]
    post_path: str | None
