from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


@dataclass
class HeroImage:
    url: str | None
    alt: str | None
    source: str | None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any] | None) -> "HeroImage":
        data = data or {}
        return cls(
            url=data.get("url"),
            alt=data.get("alt"),
            source=data.get("source"),
        )


@dataclass
class Section:
    heading: str | None
    level: str | None
    html: str
    text: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any] | None) -> "Section":
        data = data or {}
        return cls(
            heading=data.get("heading"),
            level=data.get("level"),
            html=data.get("html") or "",
            text=data.get("text") or "",
        )


@dataclass
class ListingCard:
    url: str
    title: str | None = None
    publish_date: str | None = None
    author: str | None = None
    category: str | None = None


@dataclass
class ListingConfig:
    root_url: str
    layout_id: str
    grid_widget_id: str
    addelids: list[str]
    num_pages: int
    querydata: dict[str, Any]


@dataclass
class CaseStudyRecord:
    url: str
    canonical_url: str | None
    slug: str
    title: str | None
    publish_date: str | None
    author: str | None
    tags: list[str]
    hero_image: HeroImage
    sections: list[Section]
    plain_text: str
    raw_html: str

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["hero_image"] = self.hero_image.to_dict()
        data["sections"] = [section.to_dict() for section in self.sections]
        return data

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "CaseStudyRecord":
        return cls(
            url=data.get("url") or "",
            canonical_url=data.get("canonical_url"),
            slug=data.get("slug") or "",
            title=data.get("title"),
            publish_date=data.get("publish_date"),
            author=data.get("author"),
            tags=list(data.get("tags") or []),
            hero_image=HeroImage.from_dict(data.get("hero_image")),
            sections=[Section.from_dict(section) for section in data.get("sections") or []],
            plain_text=data.get("plain_text") or "",
            raw_html=data.get("raw_html") or "",
        )
