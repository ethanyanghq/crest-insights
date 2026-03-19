from __future__ import annotations

import inspect
import logging
import time

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from . import config


class RateLimiter:
    def __init__(self, min_interval_seconds: float) -> None:
        self.min_interval_seconds = min_interval_seconds
        self._last_request_at = 0.0

    def wait(self) -> None:
        if self.min_interval_seconds <= 0:
            return
        now = time.monotonic()
        remaining = self.min_interval_seconds - (now - self._last_request_at)
        if remaining > 0:
            time.sleep(remaining)
        self._last_request_at = time.monotonic()


def build_session() -> requests.Session:
    retry_kwargs: dict[str, object] = {
        "total": config.RETRY_TOTAL,
        "connect": config.RETRY_TOTAL,
        "read": config.RETRY_TOTAL,
        "status": config.RETRY_TOTAL,
        "allowed_methods": frozenset({"GET", "HEAD"}),
        "status_forcelist": config.RETRY_STATUS_FORCELIST,
        "backoff_factor": config.RETRY_BACKOFF_FACTOR,
        "raise_on_status": False,
        "respect_retry_after_header": True,
    }
    if "backoff_jitter" in inspect.signature(Retry.__init__).parameters:
        retry_kwargs["backoff_jitter"] = config.RETRY_BACKOFF_JITTER

    retry = Retry(**retry_kwargs)
    adapter = HTTPAdapter(max_retries=retry)

    session = requests.Session()
    session.headers.update(
        {
            "User-Agent": config.USER_AGENT,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
        }
    )
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session


def fetch_html(
    session: requests.Session,
    url: str,
    *,
    logger: logging.Logger,
    rate_limiter: RateLimiter,
) -> str:
    return _fetch_text(session, url, logger=logger, rate_limiter=rate_limiter)


def fetch_fragment(
    session: requests.Session,
    url: str,
    *,
    logger: logging.Logger,
    rate_limiter: RateLimiter,
) -> str:
    return _fetch_text(session, url, logger=logger, rate_limiter=rate_limiter)


def _fetch_text(
    session: requests.Session,
    url: str,
    *,
    logger: logging.Logger,
    rate_limiter: RateLimiter,
) -> str:
    logger.debug("Fetching URL: %s", url)
    rate_limiter.wait()
    response = session.get(url, timeout=config.REQUEST_TIMEOUT)
    response.raise_for_status()
    response.encoding = response.encoding or "utf-8"
    return response.text

