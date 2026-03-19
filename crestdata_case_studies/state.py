from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from . import config
from .utils import atomic_write_json


def load_state() -> dict[str, Any]:
    progress = _load_json(config.PROGRESS_PATH) or {}
    failures = _load_json(config.FAILURES_PATH) or {}

    state: dict[str, Any] = {
        "started_at": progress.get("started_at") or _now_iso(),
        "updated_at": progress.get("updated_at") or _now_iso(),
        "listing_pages_completed": progress.get("listing_pages_completed") or [],
        "discovered_urls": progress.get("discovered_urls") or {},
        "completed": progress.get("completed") or {},
        "failed_attempts": progress.get("failed_attempts") or {},
        "failures": failures if isinstance(failures, dict) else {},
    }
    save_state(state)
    return state


def save_state(state: dict[str, Any]) -> None:
    state["updated_at"] = _now_iso()
    progress_payload = {
        "started_at": state["started_at"],
        "updated_at": state["updated_at"],
        "listing_pages_completed": sorted(set(state["listing_pages_completed"])),
        "discovered_urls": dict(sorted(state["discovered_urls"].items())),
        "completed": dict(sorted(state["completed"].items())),
        "failed_attempts": dict(sorted(state["failed_attempts"].items())),
    }
    atomic_write_json(config.PROGRESS_PATH, progress_payload)
    atomic_write_json(config.FAILURES_PATH, dict(sorted(state["failures"].items())))


def should_skip(state: dict[str, Any], unique_key: str, slug: str) -> bool:
    if unique_key not in state["completed"]:
        return False

    item_path = config.ITEMS_DIR / f"{slug}.json"
    markdown_path = config.MARKDOWN_DIR / f"{slug}.md"
    return item_path.exists() and markdown_path.exists()


def mark_success(state: dict[str, Any], unique_key: str, url: str, slug: str) -> None:
    state["completed"][unique_key] = {
        "url": url,
        "slug": slug,
        "completed_at": _now_iso(),
    }
    state["failed_attempts"].pop(unique_key, None)
    state["failures"].pop(unique_key, None)
    save_state(state)


def mark_failure(state: dict[str, Any], unique_key: str, url: str, error: str) -> None:
    attempts = int(state["failed_attempts"].get(unique_key, 0)) + 1
    state["failed_attempts"][unique_key] = attempts
    state["failures"][unique_key] = {
        "url": url,
        "error": error,
        "attempts": attempts,
        "failed_at": _now_iso(),
    }
    save_state(state)


def record_listing_page(state: dict[str, Any], page_num: int) -> None:
    if page_num not in state["listing_pages_completed"]:
        state["listing_pages_completed"].append(page_num)
        save_state(state)


def record_discovered_urls(state: dict[str, Any], urls: list[str]) -> None:
    changed = False
    for url in urls:
        if url not in state["discovered_urls"]:
            state["discovered_urls"][url] = url
            changed = True
    if changed:
        save_state(state)


def _load_json(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    raw = path.read_text(encoding="utf-8").strip()
    if not raw:
        return None
    return json.loads(raw)


def _now_iso() -> str:
    return datetime.now(tz=UTC).isoformat()
