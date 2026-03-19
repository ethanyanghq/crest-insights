# Crest Data Case Studies Scraper Architecture

Based on [crestdata-case-studies-site-analysis.md](/Users/ethanyang/Documents/GitHub/crest-insights/crestdata-case-studies-site-analysis.md).

## 1. Scraper Architecture

- Workflow: fetch `https://www.crestdata.ai/case-studies/` -> parse page 1 cards from `#uc_post_list_elementor_0a09940` -> read `querydata.num_pages` -> fetch pages `2..N` through the widget's AJAX transport -> normalize and dedupe detail URLs -> fetch each detail page -> parse structured content -> write one Markdown file per slug -> rebuild master JSON atomically.
- Pagination strategy is determined by the analysis: visible `/case-studies/2/` links exist but direct requests return `404`, while the grid exposes `data-ajax='true'`, `data-filterbehave='ajax'`, and `querydata={"page":1,"num_pages":7,...}`. The scraper must replay the widget AJAX, not crawl numbered archive URLs.
- Link extraction logic is determined by the analysis: only read links inside `#uc_post_list_elementor_0a09940`; extract from `.uc_post_list_title a` and `.uc_post_list_image a`; normalize and dedupe because both point to the same detail URL.
- Detail-page parsing logic is determined by the analysis: scope to `article.lqd-post-content.type-case-studies`, body to `.entry-content.lqd-single-post-content`, and explicitly remove `footer.blog-post-footer`, `.share-links`, and `nav.post-nav`.
- Metadata extraction is determined by the analysis: parse visible selectors first for title, author, publish date, taxonomy, hero image, and body; then fall back to `og:image`, `article:section`, and article class tokens such as `category-*` and `platform-*`.
- Fallback behavior: missing scalar fields become `null`, `tags` becomes `[]`, and if no headings exist the scraper emits one section with `heading: null`.

### Modules / Functions

- `client.py`
  - `build_session()`
  - `fetch_html()`
  - `fetch_fragment()`
  - rate limiting, retries, timeout handling
- `pagination.py`
  - `extract_listing_config()`
  - `fetch_listing_page_ajax(page_num, config)`
- `parsers.py`
  - `parse_listing_cards()`
  - `parse_detail_page()`
  - `extract_hero_image()`
  - `extract_sections()`
  - `extract_tags()`
- `state.py`
  - `load_state()`
  - `mark_success()`
  - `mark_failure()`
  - `should_skip()`
- `writers.py`
  - `write_markdown()`
  - `write_item_checkpoint()`
  - `write_master_json()`

### Data Flow

- Listing HTML or AJAX fragment -> URL set -> detail HTML -> parsed record -> `markdown/<slug>.md` + `state/items/<slug>.json` -> `case_studies.json`

## 2. Proposed Python File Structure

```text
crestdata_case_studies/
  __init__.py
  main.py
  config.py
  client.py
  pagination.py
  parsers.py
  models.py
  state.py
  writers.py
  utils.py
```

## 3. Proposed Output Folder Structure

```text
output/crestdata_case_studies/
  case_studies.json
  markdown/
    <slug>.md
  logs/
    scrape.log
  state/
    progress.json
    failures.json
    items/
      <slug>.json
```

## 4. JSON Schema Per Case Study

```json
{
  "url": "https://www.crestdata.ai/case-studies/<slug>/",
  "canonical_url": "https://www.crestdata.ai/case-studies/<slug>/",
  "slug": "<slug>",
  "title": "string|null",
  "publish_date": "ISO-8601 string|null",
  "author": "string|null",
  "tags": ["string"],
  "hero_image": {
    "url": "string|null",
    "alt": "string|null",
    "source": "data-src|data-lazy-src|src|og:image|null"
  },
  "sections": [
    {
      "heading": "string|null",
      "level": "h3|h4|h5|null",
      "html": "string",
      "text": "string"
    }
  ],
  "plain_text": "string",
  "raw_html": "string"
}
```

- `tags` should hold all taxonomy-like labels because the requested schema has no separate `category` field.
- `raw_html` should be the cleaned article-body HTML, not the full page HTML.

## 5. Parsing Strategy

### Listing Pages

- Parse only inside `#uc_post_list_elementor_0a09940`.
- Ignore `.uc_post_content` as a primary excerpt source because the analysis shows it is noisy.
- Extract URLs from `.uc_post_list_title a` and `.uc_post_list_image a`.
- Use `querydata.num_pages` as the authoritative page count fallback.
- Fetch additional pages through AJAX, not `/case-studies/<n>/`.
- Support both full-document and HTML-fragment responses from the AJAX endpoint.

### Detail Pages

- Parse `article.lqd-post-content.type-case-studies`.
- Extract title from `header.lqd-post-header .entry-title`.
- Extract author from `.entry-meta .entry-author a.url.fn`.
- Extract date from `.posted-on time.entry-date.published`, preferring `datetime`.
- Extract hero image from `.lqd-post-cover .wp-post-image`, then `.entry-content .wp-post-image`, then `meta[property="og:image"]`.
- For images, prefer `data-src` or `data-lazy-src`; only use `src` if it is not a placeholder.
- Scope content to `.entry-content.lqd-single-post-content`.
- Remove `footer.blog-post-footer`, `.share-links`, and `nav.post-nav` before body extraction.

### Sections

- Walk `.entry-content .elementor-widget-text-editor` blocks in DOM order.
- Start a new section on `h3`, `h4`, or `h5`.
- Append following paragraphs, lists, and inline images until the next heading.
- If no heading is found, emit a single catch-all section with `heading: null`.

### Metadata Fallbacks

- Visible taxonomy first: `.cat-links a` and any older inline `Tags:` content near the footer if present.
- Then `meta[property="article:section"]`.
- Then article class tokens such as `category-aws`, `category-cloudops`, and `platform-aws`.

## 6. Error Handling Strategy

- Retries: `requests.Session` with `urllib3.Retry` for `429`, `500`, `502`, `503`, and `504`, plus connection and read timeouts.
- Backoff: exponential backoff with jitter.
- Timeouts: separate connect and read timeouts, for example `(10, 30)`.
- Logging: INFO to console, DEBUG to `logs/scrape.log`; log page discovery, retries, fallback selector use, skips, and failures.
- Broken pages: if HTTP is non-200 or the article root is missing, record the URL in `failures.json`, continue the run, and do not abort the crawl.
- Duplicate links: normalize to absolute HTTPS URLs, strip fragments, collapse trailing slash differences, then dedupe via a set.
- Missing metadata: fill scalars with `null`, `tags` with `[]`, and keep the record if core article content exists.
- Inconsistent layouts: use layered selector fallbacks and a catch-all section strategy so older layouts still serialize cleanly.

## 7. Resume Strategy

- Track progress in `state/progress.json`:
  - listing pages completed
  - discovered URL keys
  - completed URL keys
  - failed attempts
  - timestamps
- Use `canonical_url` if present, otherwise normalized `url`, as the unique record key.
- After each successful detail parse, immediately write:
  - `state/items/<slug>.json`
  - `markdown/<slug>.md`
- Rebuild `case_studies.json` from `state/items/*.json` so resume is safe if interrupted mid-run.
- Skip a case study when its unique key is marked complete and both checkpoint files exist; otherwise requeue it.

## 8. Whether `requests + BeautifulSoup` Is Sufficient

- Yes, with one caveat: pagination must be reproduced with HTTP requests to the widget's AJAX backend.
- Evidence from the analysis:
  - the first listing page exposes 9 cards directly in HTML
  - detail pages are server-rendered
  - detail pages do not require JavaScript for core content extraction
  - pagination is the only JavaScript-sensitive area
- Evidence against naive archive pagination:
  - `/case-studies/2/` returned `404`
  - the listing grid exposes `data-ajax='true'`
  - the listing grid exposes `data-filterbehave='ajax'`
  - the listing grid exposes `querydata` with `num_pages=7`
- Conclusion: use `requests + BeautifulSoup` as the default approach. Keep Playwright only as a contingency if the widget AJAX request cannot be reproduced from page markup and scripts.

## 9. Self-Contained Implementation Brief

```text
Build a Python scraper for Crest Data case studies using requests + BeautifulSoup.

Targets:
- Listing root: https://www.crestdata.ai/case-studies/
- Detail URL pattern: https://www.crestdata.ai/case-studies/<slug>/

Required behavior:
- Fetch the listing root and parse case-study cards only inside #uc_post_list_elementor_0a09940.
- Read the widget querydata JSON to get page counts; do not request /case-studies/2/ style URLs because they 404.
- Reproduce the listing widget's AJAX pagination with requests and crawl all listing pages.
- Extract detail URLs from .uc_post_list_title a and .uc_post_list_image a, normalize to absolute HTTPS URLs, strip fragments, and dedupe.
- Fetch each detail page and parse article.lqd-post-content.type-case-studies.
- Extract title, publish date, author, tags/taxonomy, hero image, ordered sections, plain text, and cleaned body HTML.
- For hero images, prefer data-src or data-lazy-src, then non-placeholder src, then og:image.
- Scope body parsing to .entry-content.lqd-single-post-content and exclude footer.blog-post-footer, .share-links, and nav.post-nav.
- Group section content by h3/h4/h5 headings inside .entry-content .elementor-widget-text-editor; if no headings exist, create one catch-all section.
- Save one Markdown file per slug and one master JSON file containing all case studies.
- Support retries, timeouts, rate limiting, structured logging, and resumable execution via a state/progress file.
- Skip already completed items on resume using canonical_url or normalized url as the unique key.
- Use atomic writes for state and master JSON.
- Keep Playwright out unless the AJAX paginator cannot be reproduced with requests.
```
