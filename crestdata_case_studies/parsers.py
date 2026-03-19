from __future__ import annotations

from typing import Iterator
from urllib.parse import urlparse

from bs4 import BeautifulSoup, NavigableString, Tag

from . import config
from .models import CaseStudyRecord, HeroImage, ListingCard, Section
from .pagination import extract_listing_payload
from .utils import (
    dedupe_preserve_order,
    humanize_taxonomy_token,
    inner_html,
    isoformat_datetime,
    normalize_url,
    normalize_whitespace,
    slug_from_url,
)

_CAPTURE_TAGS = {"h3", "h4", "h5", "p", "ul", "ol", "figure", "img", "blockquote", "table", "hr"}
_PARENT_CAPTURE_TAGS = {"h3", "h4", "h5", "p", "ul", "ol", "figure", "blockquote", "table"}
_PLACEHOLDER_PREFIXES = ("data:image/svg+xml", "data:image/gif")


def parse_listing_cards(payload: str, *, base_url: str) -> list[ListingCard]:
    fragment_html, parsed_payload = extract_listing_payload(payload)
    if parsed_payload and fragment_html:
        wrapped_html = f'<div id="{config.LISTING_GRID_ID}">{fragment_html}</div>'
    else:
        wrapped_html = fragment_html or payload

    soup = BeautifulSoup(wrapped_html, "html.parser")
    grid = soup.select_one(f"#{config.LISTING_GRID_ID}")
    if grid is None:
        if soup.select(".uc_post_list_box"):
            synthetic = BeautifulSoup(
                f'<div id="{config.LISTING_GRID_ID}">{wrapped_html}</div>',
                "html.parser",
            )
            grid = synthetic.select_one(f"#{config.LISTING_GRID_ID}")
        else:
            raise ValueError("Listing grid not found in listing payload")

    seen_urls: set[str] = set()
    cards: list[ListingCard] = []

    for card in grid.select(".uc_post_list_box"):
        urls: list[str] = []
        for link in card.select(".uc_post_list_title a, .uc_post_list_image a"):
            normalized = normalize_url(link.get("href"), base=base_url)
            if normalized and normalized not in urls:
                urls.append(normalized)

        if not urls:
            continue

        detail_url = urls[0]
        if detail_url in seen_urls:
            continue
        seen_urls.add(detail_url)

        title = _text_or_none(card.select_one(".uc_post_list_title a"))
        meta_items = card.select(".ue-meta-data .ue-grid-item-meta-data")
        publish_date = _text_or_none(meta_items[0]) if len(meta_items) >= 1 else None
        author = _text_or_none(meta_items[1]) if len(meta_items) >= 2 else None
        category = normalize_whitespace(card.get("data-category"))
        category = category or None

        cards.append(
            ListingCard(
                url=detail_url,
                title=title,
                publish_date=publish_date,
                author=author,
                category=category,
            )
        )

    return cards


def parse_detail_page(html: str, url: str) -> CaseStudyRecord:
    soup = BeautifulSoup(html, "html.parser")
    canonical_url = _extract_canonical_url(soup, url)

    article = soup.select_one(config.ARTICLE_SELECTOR)
    if article is None:
        raise ValueError(f"Article root {config.ARTICLE_SELECTOR} not found")

    article_clone_soup = BeautifulSoup(str(article), "html.parser")
    article_clone = article_clone_soup.select_one(config.ARTICLE_SELECTOR) or article_clone_soup
    for selector in config.EXCLUDED_CONTENT_SELECTORS:
        for node in article_clone.select(selector):
            node.decompose()

    body = article_clone.select_one(config.BODY_SELECTOR)
    if body is None:
        raise ValueError(f"Article body {config.BODY_SELECTOR} not found")

    _normalize_image_tags(body)

    title = _text_or_none(soup.select_one(config.TITLE_SELECTOR))
    if title is None:
        title = _text_or_none(article.select_one("h1"))

    author = _text_or_none(soup.select_one(config.AUTHOR_SELECTOR))

    time_tag = soup.select_one(config.DATE_SELECTOR)
    publish_date = isoformat_datetime(
        time_tag.get("datetime") if time_tag else None,
        _text_or_none(time_tag),
    )

    slug = slug_from_url(canonical_url or url)
    hero_image = extract_hero_image(soup, article)
    tags = extract_tags(soup, article)
    sections = extract_sections(body)
    plain_text = build_plain_text(title, sections)
    raw_html = inner_html(body).strip()

    return CaseStudyRecord(
        url=normalize_url(url, base=config.BASE_URL) or url,
        canonical_url=canonical_url,
        slug=slug,
        title=title,
        publish_date=publish_date,
        author=author,
        tags=tags,
        hero_image=hero_image,
        sections=sections,
        plain_text=plain_text,
        raw_html=raw_html,
    )


def extract_hero_image(soup: BeautifulSoup, article: Tag) -> HeroImage:
    for selector in config.HERO_SELECTORS:
        image_tag = soup.select_one(selector)
        if image_tag:
            resolved = _resolve_image_tag(image_tag)
            if resolved.url:
                return resolved

    og_image = soup.select_one('meta[property="og:image"]')
    if og_image and og_image.get("content"):
        return HeroImage(
            url=normalize_url(og_image.get("content"), base=config.BASE_URL),
            alt=_meta_content(soup, 'meta[property="og:image:alt"]'),
            source="og:image",
        )

    return HeroImage(url=None, alt=None, source=None)


def extract_sections(body: Tag) -> list[Section]:
    widgets = body.select(config.SECTION_WIDGET_SELECTOR)
    if not widgets:
        widgets = [body]

    sections: list[Section] = []
    current_section: Section | None = None
    saw_heading = False

    for widget in widgets:
        for node in _iter_section_nodes(widget):
            if node.name in {"h3", "h4", "h5"}:
                saw_heading = True
                current_section = Section(
                    heading=normalize_whitespace(node.get_text(" ", strip=True)) or None,
                    level=node.name,
                    html="",
                    text="",
                )
                sections.append(current_section)
                continue

            if current_section is None:
                current_section = Section(heading=None, level=None, html="", text="")
                sections.append(current_section)

            fragment_html = str(node).strip()
            fragment_text = _node_text(node)

            if fragment_html:
                current_section.html = _append_fragment(current_section.html, fragment_html)
            if fragment_text:
                current_section.text = _append_text(current_section.text, fragment_text)

    if not sections:
        catchall_html = inner_html(body).strip()
        catchall_text = normalize_whitespace(body.get_text(" ", strip=True))
        return [Section(heading=None, level=None, html=catchall_html, text=catchall_text)]

    if not saw_heading and len(sections) != 1:
        merged_html = "\n".join(section.html for section in sections if section.html).strip()
        merged_text = "\n\n".join(section.text for section in sections if section.text).strip()
        return [Section(heading=None, level=None, html=merged_html, text=merged_text)]

    return sections


def extract_tags(soup: BeautifulSoup, article: Tag) -> list[str]:
    tags: list[str] = []

    visible_category_tags = [
        normalize_whitespace(link.get_text(" ", strip=True))
        for link in soup.select(f"{config.CATEGORY_SELECTOR}")
    ]
    tags.extend(tag for tag in visible_category_tags if tag)

    footer_tags = [
        normalize_whitespace(link.get_text(" ", strip=True))
        for link in soup.select("footer.blog-post-footer .tags-links a")
    ]
    tags.extend(tag for tag in footer_tags if tag)

    article_section = _meta_content(soup, 'meta[property="article:section"]')
    if article_section:
        tags.append(article_section)

    for class_name in article.get("class", []):
        if class_name.startswith("category-"):
            tags.append(humanize_taxonomy_token(class_name.removeprefix("category-")))
        elif class_name.startswith("platform-"):
            tags.append(humanize_taxonomy_token(class_name.removeprefix("platform-")))

    return dedupe_preserve_order([tag for tag in tags if tag])


def build_plain_text(title: str | None, sections: list[Section]) -> str:
    parts: list[str] = []
    if title:
        parts.append(title)

    for section in sections:
        if section.heading:
            parts.append(section.heading)
        if section.text:
            parts.append(section.text)

    return "\n\n".join(part for part in parts if part).strip()


def _extract_canonical_url(soup: BeautifulSoup, fallback_url: str) -> str | None:
    canonical = soup.select_one('link[rel="canonical"]')
    normalized = normalize_url(canonical.get("href") if canonical else None, base=config.BASE_URL)
    if normalized:
        return normalized
    return normalize_url(fallback_url, base=config.BASE_URL)


def _resolve_image_tag(tag: Tag) -> HeroImage:
    for attr, source in (("data-src", "data-src"), ("data-lazy-src", "data-lazy-src")):
        candidate = _normalize_image_candidate(tag.get(attr), tag)
        if candidate:
            return HeroImage(url=candidate, alt=_image_alt(tag), source=source)

    source_candidate = tag.get("src")
    if source_candidate and not source_candidate.startswith(_PLACEHOLDER_PREFIXES):
        candidate = _normalize_image_candidate(source_candidate, tag)
        if candidate:
            return HeroImage(url=candidate, alt=_image_alt(tag), source="src")

    srcset_candidate = _first_srcset_url(tag)
    if srcset_candidate:
        return HeroImage(url=srcset_candidate, alt=_image_alt(tag), source="src")

    return HeroImage(url=None, alt=_image_alt(tag), source=None)


def _normalize_image_tags(body: Tag) -> None:
    for image in body.select("img"):
        resolved = _resolve_image_tag(image)
        if resolved.url:
            image["src"] = resolved.url
        for attr in (
            "data-src",
            "data-lazy-src",
            "data-srcset",
            "data-lazy-srcset",
            "data-sizes",
            "data-lazy-sizes",
            "srcset",
        ):
            image.attrs.pop(attr, None)


def _normalize_image_candidate(candidate: str | None, tag: Tag) -> str | None:
    if not candidate:
        return None
    candidate = candidate.strip()
    if not candidate or candidate.startswith(_PLACEHOLDER_PREFIXES):
        return None

    parsed = urlparse(candidate)
    if parsed.hostname in {"localhost", "127.0.0.1"}:
        srcset_candidate = _first_srcset_url(tag)
        if srcset_candidate:
            return srcset_candidate

    return normalize_url(candidate, base=config.BASE_URL)


def _first_srcset_url(tag: Tag) -> str | None:
    for attr in ("data-srcset", "data-lazy-srcset", "srcset"):
        srcset = tag.get(attr)
        if not srcset:
            continue
        first_part = srcset.split(",")[0].strip().split(" ")[0].strip()
        normalized = normalize_url(first_part, base=config.BASE_URL)
        if normalized:
            return normalized
    return None


def _image_alt(tag: Tag) -> str | None:
    alt = normalize_whitespace(tag.get("alt"))
    return alt or None


def _iter_section_nodes(container: Tag) -> Iterator[Tag]:
    for node in container.descendants:
        if not isinstance(node, Tag):
            continue
        if node.name not in _CAPTURE_TAGS:
            continue
        if _is_nested_captured_tag(node, container):
            continue
        yield node


def _is_nested_captured_tag(node: Tag, container: Tag) -> bool:
    for parent in node.parents:
        if parent == container:
            return False
        if not isinstance(parent, Tag):
            continue
        if parent.name in _PARENT_CAPTURE_TAGS:
            return True
    return False


def _node_text(node: Tag) -> str:
    if node.name == "img":
        return _image_alt(node) or ""
    if node.name == "figure":
        image = node.find("img")
        caption = node.find("figcaption")
        parts = []
        if image:
            parts.append(_image_alt(image) or "")
        if caption:
            parts.append(normalize_whitespace(caption.get_text(" ", strip=True)))
        return normalize_whitespace(" ".join(part for part in parts if part))
    return normalize_whitespace(node.get_text(" ", strip=True))


def _append_fragment(existing: str, fragment: str) -> str:
    if not existing:
        return fragment
    return f"{existing}\n{fragment}"


def _append_text(existing: str, fragment: str) -> str:
    if not existing:
        return fragment
    return f"{existing}\n\n{fragment}"


def _meta_content(soup: BeautifulSoup, selector: str) -> str | None:
    meta = soup.select_one(selector)
    value = normalize_whitespace(meta.get("content") if meta else None)
    return value or None


def _text_or_none(tag: Tag | None) -> str | None:
    if tag is None:
        return None
    value = normalize_whitespace(tag.get_text(" ", strip=True))
    return value or None
