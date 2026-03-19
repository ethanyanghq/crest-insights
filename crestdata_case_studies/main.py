from __future__ import annotations

import logging
from pathlib import Path

from . import config
from .client import RateLimiter, build_session, fetch_html
from .pagination import extract_listing_config, fetch_listing_page_ajax
from .parsers import parse_detail_page, parse_listing_cards
from .state import (
    load_state,
    mark_failure,
    mark_success,
    record_discovered_urls,
    record_listing_page,
    should_skip,
)
from .utils import ensure_directories, normalize_url
from .writers import write_item_checkpoint, write_markdown, write_master_json


def main() -> None:
    ensure_directories(
        [
            config.OUTPUT_ROOT,
            config.MARKDOWN_DIR,
            config.LOG_DIR,
            config.STATE_DIR,
            config.ITEMS_DIR,
        ]
    )
    logger = _setup_logging()
    session = build_session()
    rate_limiter = RateLimiter(config.RATE_LIMIT_SECONDS)
    state = load_state()

    logger.info("Fetching listing root: %s", config.LISTING_ROOT)
    listing_html = fetch_html(
        session,
        config.LISTING_ROOT,
        logger=logger,
        rate_limiter=rate_limiter,
    )
    listing_config = extract_listing_config(listing_html)

    page_one_cards = parse_listing_cards(listing_html, base_url=config.LISTING_ROOT)
    page_one_urls = [card.url for card in page_one_cards]
    record_listing_page(state, 1)
    record_discovered_urls(state, page_one_urls)
    logger.info("Listing page 1 discovered %s URLs", len(page_one_urls))

    for page_num in range(2, listing_config.num_pages + 1):
        if page_num in state["listing_pages_completed"]:
            logger.info("Skipping listing page %s because it is already recorded", page_num)
            continue

        try:
            payload = fetch_listing_page_ajax(
                session,
                page_num,
                listing_config,
                logger=logger,
                rate_limiter=rate_limiter,
            )
            page_cards = parse_listing_cards(payload, base_url=config.LISTING_ROOT)
            page_urls = [card.url for card in page_cards]
            record_listing_page(state, page_num)
            record_discovered_urls(state, page_urls)
            logger.info("Listing page %s discovered %s URLs", page_num, len(page_urls))
        except Exception as exc:
            logger.exception("Failed to crawl listing page %s: %s", page_num, exc)

    discovered_urls = sorted(state["discovered_urls"].values())
    logger.info("Discovered %s unique case study URLs", len(discovered_urls))

    for detail_url in discovered_urls:
        provisional_key = normalize_url(detail_url, base=config.BASE_URL) or detail_url
        provisional_slug = Path(detail_url.rstrip("/")).name

        if should_skip(state, provisional_key, provisional_slug):
            logger.info("Skipping already completed case study: %s", detail_url)
            continue

        try:
            logger.info("Scraping detail page: %s", detail_url)
            detail_html = fetch_html(
                session,
                detail_url,
                logger=logger,
                rate_limiter=rate_limiter,
            )
            record = parse_detail_page(detail_html, detail_url)
            unique_key = record.canonical_url or record.url

            write_item_checkpoint(record)
            write_markdown(record)
            mark_success(state, unique_key, record.url, record.slug)
            if unique_key != provisional_key:
                state["discovered_urls"][unique_key] = record.url
            write_master_json()
            logger.info("Completed case study: %s", record.slug)
        except Exception as exc:
            logger.exception("Failed to scrape detail page %s: %s", detail_url, exc)
            mark_failure(state, provisional_key, detail_url, str(exc))

    write_master_json()

    completed_count = len(state["completed"])
    failed_count = len(state["failures"])
    listing_pages_crawled = len(set(state["listing_pages_completed"]))

    logger.info("listing pages crawled: %s", listing_pages_crawled)
    logger.info("URLs discovered: %s", len(state["discovered_urls"]))
    logger.info("successfully scraped: %s", completed_count)
    logger.info("failed: %s", failed_count)


def _setup_logging() -> logging.Logger:
    logger = logging.getLogger("crestdata_case_studies")
    logger.setLevel(logging.DEBUG)
    logger.handlers.clear()

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(logging.Formatter("%(levelname)s %(message)s"))

    file_handler = logging.FileHandler(config.LOG_DIR / "scrape.log", encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(
        logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s")
    )

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    logger.propagate = False
    return logger


if __name__ == "__main__":
    main()

