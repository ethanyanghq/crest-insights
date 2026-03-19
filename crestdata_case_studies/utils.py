from __future__ import annotations

import json
import re
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable
from urllib.parse import parse_qsl, urlencode, urljoin, urlparse, urlunparse

from . import config

_WHITESPACE_RE = re.compile(r"\s+")

TOKEN_MAP = {
    "ai": "AI",
    "aiml": "AI/ML",
    "aiops": "AIOps",
    "aws": "AWS",
    "cloudops": "CloudOps",
    "devops": "DevOps",
    "devsecops": "DevSecOps",
    "itsm": "ITSM",
    "mlops": "MLOps",
    "siem": "SIEM",
    "soar": "SOAR",
    "soc": "SOC",
    "sre": "SRE",
    "xdr": "XDR",
    "google-secops": "Google SecOps",
}


def ensure_directories(paths: Iterable[Path]) -> None:
    for path in paths:
        path.mkdir(parents=True, exist_ok=True)


def atomic_write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp_path = path.with_suffix(f"{path.suffix}.tmp")
    temp_path.write_text(content, encoding="utf-8")
    temp_path.replace(path)


def atomic_write_json(path: Path, data: Any) -> None:
    atomic_write_text(path, json.dumps(data, indent=2, ensure_ascii=False) + "\n")


def normalize_whitespace(value: str | None) -> str:
    if not value:
        return ""
    return _WHITESPACE_RE.sub(" ", value).strip()


def normalize_url(
    url: str | None,
    *,
    base: str | None = None,
    keep_query: bool = False,
) -> str | None:
    if not url:
        return None
    if url.startswith("data:"):
        return url

    joined = urljoin(base or config.BASE_URL, url)
    parsed = urlparse(joined)
    if not parsed.scheme or not parsed.netloc:
        return None

    scheme = "https" if parsed.scheme in {"http", "https"} else parsed.scheme
    netloc = parsed.netloc.lower()
    path = parsed.path or "/"
    if "." not in Path(path).name and not path.endswith("/"):
        path = f"{path}/"

    query = parsed.query if keep_query else ""
    return urlunparse((scheme, netloc, path, "", query, ""))


def normalize_url_with_query(url: str) -> str:
    parsed = urlparse(url)
    query_items = sorted(parse_qsl(parsed.query, keep_blank_values=True))
    return urlunparse(
        (parsed.scheme, parsed.netloc.lower(), parsed.path, "", urlencode(query_items), "")
    )


def slug_from_url(url: str) -> str:
    parts = [part for part in urlparse(url).path.split("/") if part]
    return parts[-1] if parts else ""


def inner_html(tag: Any) -> str:
    return "".join(str(child) for child in getattr(tag, "contents", []))


def dedupe_preserve_order(values: Iterable[str]) -> list[str]:
    seen: set[str] = set()
    output: list[str] = []
    for value in values:
        key = value.casefold()
        if key in seen:
            continue
        seen.add(key)
        output.append(value)
    return output


def isoformat_datetime(datetime_value: str | None, text_value: str | None = None) -> str | None:
    if datetime_value:
        try:
            return datetime.fromisoformat(datetime_value.replace("Z", "+00:00")).isoformat()
        except ValueError:
            pass

    if text_value:
        cleaned = normalize_whitespace(text_value)
        for fmt in ("%B %d, %Y", "%b %d, %Y"):
            try:
                return datetime.strptime(cleaned, fmt).replace(tzinfo=UTC).isoformat()
            except ValueError:
                continue

    return None


def humanize_taxonomy_token(token: str) -> str:
    cleaned = token.strip().strip("-").lower()
    if not cleaned:
        return ""
    if cleaned in TOKEN_MAP:
        return TOKEN_MAP[cleaned]
    parts = [TOKEN_MAP.get(part, part.capitalize()) for part in cleaned.split("-")]
    return " ".join(part for part in parts if part)

