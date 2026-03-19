from __future__ import annotations

import json
import logging
from typing import Any
from urllib.parse import urlencode

from bs4 import BeautifulSoup, Tag
import requests

from . import config
from .client import RateLimiter, fetch_fragment
from .models import ListingConfig


def extract_listing_config(listing_html: str) -> ListingConfig:
    soup = BeautifulSoup(listing_html, "html.parser")
    grid = soup.select_one(f"#{config.LISTING_GRID_ID}")
    if grid is None:
        raise ValueError(f"Listing grid #{config.LISTING_GRID_ID} not found")

    querydata_raw = grid.get("querydata")
    if not querydata_raw:
        raise ValueError("Listing grid querydata attribute not found")
    querydata = json.loads(querydata_raw)

    grid_widget = _closest_widget(grid)
    if grid_widget is None or not grid_widget.get("data-id"):
        raise ValueError("Grid widget wrapper with data-id not found")

    layout = grid.find_parent(class_="elementor")
    if layout is None:
        raise ValueError("Elementor layout wrapper not found for listing grid")

    layout_id = layout.get("data-elementor-id") or layout.get("data-id")
    if not layout_id:
        raise ValueError("Elementor layout id not found")

    addelids: list[str] = []
    for filter_element in layout.select(".uc-grid-filter, .uc-filter-pagination"):
        widget = _closest_widget(filter_element)
        widget_id = widget.get("data-id") if widget else None
        if widget_id and widget_id not in addelids:
            addelids.append(widget_id)

    return ListingConfig(
        root_url=config.LISTING_ROOT,
        layout_id=str(layout_id),
        grid_widget_id=str(grid_widget["data-id"]),
        addelids=addelids,
        num_pages=int(querydata.get("num_pages") or 1),
        querydata=querydata,
    )


def fetch_listing_page_ajax(
    session: requests.Session,
    page_num: int,
    listing_config: ListingConfig,
    *,
    logger: logging.Logger,
    rate_limiter: RateLimiter,
) -> str:
    if page_num < 2:
        raise ValueError("AJAX pagination is only required for pages 2..N")

    params: list[tuple[str, str]] = [
        ("ucfrontajaxaction", "getfiltersdata"),
        ("layoutid", listing_config.layout_id),
        ("elid", listing_config.grid_widget_id),
        ("ucpage", str(page_num)),
    ]
    if listing_config.addelids:
        params.append(("addelids", ",".join(listing_config.addelids)))

    ajax_url = f"{listing_config.root_url}?{urlencode(params)}"
    logger.info("Fetching listing page %s via AJAX", page_num)
    return fetch_fragment(session, ajax_url, logger=logger, rate_limiter=rate_limiter)


def extract_listing_payload(payload: str) -> tuple[str, dict[str, Any] | None]:
    payload = payload.strip()
    if not payload:
        return "", None

    try:
        parsed = json.loads(payload)
    except json.JSONDecodeError:
        return payload, None

    if isinstance(parsed, dict):
        html_items = str(parsed.get("html_items") or "")
        return html_items, parsed

    return payload, None


def _closest_widget(element: Tag) -> Tag | None:
    return element.find_parent(class_="elementor-widget")

