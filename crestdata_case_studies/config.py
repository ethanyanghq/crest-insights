from pathlib import Path

BASE_URL = "https://www.crestdata.ai"
LISTING_ROOT = f"{BASE_URL}/case-studies/"

LISTING_GRID_ID = "uc_post_list_elementor_0a09940"
PAGINATION_WIDGET_ID = "uc_archive_pagination_elementor_ff772e2"

REQUEST_TIMEOUT = (10, 30)
RATE_LIMIT_SECONDS = 0.75
RETRY_TOTAL = 5
RETRY_BACKOFF_FACTOR = 1.0
RETRY_BACKOFF_JITTER = 0.35
RETRY_STATUS_FORCELIST = (429, 500, 502, 503, 504)
USER_AGENT = (
    "crestdata-case-studies-scraper/1.0 "
    "(requests; +https://www.crestdata.ai/case-studies/)"
)

OUTPUT_ROOT = Path("data")
MASTER_JSON_PATH = OUTPUT_ROOT / "case_studies.json"
MARKDOWN_DIR = OUTPUT_ROOT / "markdown"
LOG_DIR = OUTPUT_ROOT / "logs"
STATE_DIR = OUTPUT_ROOT / "state"
PROGRESS_PATH = STATE_DIR / "progress.json"
FAILURES_PATH = STATE_DIR / "failures.json"
ITEMS_DIR = STATE_DIR / "items"

ARTICLE_SELECTOR = "article.lqd-post-content.type-case-studies"
BODY_SELECTOR = ".entry-content.lqd-single-post-content"
TITLE_SELECTOR = "header.lqd-post-header .entry-title"
AUTHOR_SELECTOR = ".entry-meta .entry-author a.url.fn"
DATE_SELECTOR = ".posted-on time.entry-date.published"
CATEGORY_SELECTOR = ".cat-links a"
HERO_SELECTORS = (
    ".lqd-post-cover .wp-post-image",
    ".entry-content .wp-post-image",
)
SECTION_WIDGET_SELECTOR = ".elementor-widget-text-editor"
SECTION_HEADING_SELECTOR = "h3, h4, h5"
EXCLUDED_CONTENT_SELECTORS = (
    "footer.blog-post-footer",
    ".share-links",
    "nav.post-nav",
    "noscript",
    "script",
    "style",
)

