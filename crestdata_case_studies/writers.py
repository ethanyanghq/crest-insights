from __future__ import annotations

import json
from pathlib import Path

from bs4 import BeautifulSoup, NavigableString, Tag

from . import config
from .models import CaseStudyRecord, Section
from .utils import atomic_write_json, atomic_write_text, normalize_whitespace


def write_markdown(record: CaseStudyRecord) -> Path:
    path = config.MARKDOWN_DIR / f"{record.slug}.md"
    atomic_write_text(path, render_markdown(record))
    return path


def write_item_checkpoint(record: CaseStudyRecord) -> Path:
    path = config.ITEMS_DIR / f"{record.slug}.json"
    atomic_write_json(path, record.to_dict())
    return path


def write_master_json() -> Path:
    items: list[dict] = []
    for item_path in sorted(config.ITEMS_DIR.glob("*.json")):
        items.append(json.loads(item_path.read_text(encoding="utf-8")))
    atomic_write_json(config.MASTER_JSON_PATH, items)
    return config.MASTER_JSON_PATH


def render_markdown(record: CaseStudyRecord) -> str:
    lines: list[str] = [f"# {record.title or record.slug}", ""]
    lines.append(f"- URL: {record.url}")
    lines.append(f"- Canonical URL: {record.canonical_url or ''}")
    lines.append(f"- Publish Date: {record.publish_date or ''}")
    lines.append(f"- Author: {record.author or ''}")
    lines.append(f"- Tags: {', '.join(record.tags)}")
    if record.hero_image.url:
        lines.append(f"- Hero Image: {record.hero_image.url}")
    lines.append("")

    if record.hero_image.url:
        alt = record.hero_image.alt or record.title or record.slug
        lines.append(f"![{alt}]({record.hero_image.url})")
        lines.append("")

    for section in record.sections:
        heading = section.heading
        if heading:
            lines.append(f"{_markdown_heading_prefix(section.level)} {heading}")
            lines.append("")

        section_markdown = _html_fragment_to_markdown(section.html)
        if section_markdown:
            lines.append(section_markdown)
            lines.append("")
        elif section.text:
            lines.append(section.text)
            lines.append("")

    return "\n".join(lines).strip() + "\n"


def _markdown_heading_prefix(level: str | None) -> str:
    if level == "h4":
        return "###"
    if level == "h5":
        return "####"
    return "##"


def _html_fragment_to_markdown(fragment: str) -> str:
    if not fragment.strip():
        return ""

    soup = BeautifulSoup(fragment, "html.parser")
    blocks: list[str] = []
    for child in soup.contents:
        rendered = _render_block(child)
        if rendered:
            blocks.append(rendered)
    return "\n\n".join(blocks).strip()


def _render_block(node: Tag | NavigableString) -> str:
    if isinstance(node, NavigableString):
        return normalize_whitespace(str(node))

    if not isinstance(node, Tag):
        return ""

    name = node.name.lower()
    if name == "p":
        return _render_inline_children(node)
    if name == "ul":
        items = [_render_list_item(item, ordered=False, index=0) for item in node.find_all("li", recursive=False)]
        return "\n".join(item for item in items if item)
    if name == "ol":
        items = [
            _render_list_item(item, ordered=True, index=index)
            for index, item in enumerate(node.find_all("li", recursive=False), start=1)
        ]
        return "\n".join(item for item in items if item)
    if name == "blockquote":
        content = _render_inline_children(node)
        return "\n".join(f"> {line}" for line in content.splitlines() if line.strip())
    if name == "figure":
        image = node.find("img")
        caption = node.find("figcaption")
        parts: list[str] = []
        if image:
            parts.append(_render_block(image))
        if caption:
            caption_text = _render_inline_children(caption)
            if caption_text:
                parts.append(caption_text)
        return "\n\n".join(part for part in parts if part)
    if name == "img":
        src = node.get("src") or ""
        alt = normalize_whitespace(node.get("alt")) or ""
        if not src:
            return alt
        return f"![{alt}]({src})"
    if name == "hr":
        return "---"
    if name in {"div", "section"}:
        parts = [_render_block(child) for child in node.contents]
        return "\n\n".join(part for part in parts if part)
    if name == "table":
        return normalize_whitespace(node.get_text(" ", strip=True))
    return _render_inline_children(node)


def _render_list_item(node: Tag, *, ordered: bool, index: int) -> str:
    bullet = f"{index}." if ordered else "-"
    contents: list[str] = []
    nested_blocks: list[str] = []

    for child in node.contents:
        if isinstance(child, NavigableString):
            text = normalize_whitespace(str(child))
            if text:
                contents.append(text)
            continue

        if child.name in {"ul", "ol"}:
            nested_blocks.append(_render_block(child))
        else:
            rendered = _render_inline(child)
            if rendered:
                contents.append(rendered)

    line = f"{bullet} {normalize_whitespace(' '.join(contents))}".rstrip()
    if nested_blocks:
        return "\n".join([line] + [block for block in nested_blocks if block])
    return line


def _render_inline_children(node: Tag) -> str:
    parts = [_render_inline(child) for child in node.contents]
    return normalize_whitespace(" ".join(part for part in parts if part))


def _render_inline(node: Tag | NavigableString) -> str:
    if isinstance(node, NavigableString):
        return normalize_whitespace(str(node))

    if not isinstance(node, Tag):
        return ""

    name = node.name.lower()
    if name in {"strong", "b"}:
        content = _render_inline_children(node)
        return f"**{content}**" if content else ""
    if name in {"em", "i"}:
        content = _render_inline_children(node)
        return f"*{content}*" if content else ""
    if name == "a":
        text = _render_inline_children(node)
        href = node.get("href") or ""
        return f"[{text}]({href})" if href and text else text
    if name == "br":
        return "\n"
    if name == "img":
        return _render_block(node)
    if name in {"span", "small", "sup", "sub"}:
        return _render_inline_children(node)
    return _render_inline_children(node)
