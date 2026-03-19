# Crest Data Case Studies Site Analysis

Analyzed on March 18, 2026.

## Short Summary

- The case studies section is a WordPress/Elementor page with a custom listing widget on `https://www.crestdata.ai/case-studies/`.
- The first listing page is server-rendered and contains 9 case-study cards in HTML.
- The listing widget reports `total_posts=59` and `num_pages=7` in its `querydata` attribute at the time of inspection.
- Detail pages follow the pattern `https://www.crestdata.ai/case-studies/<slug>/` and are also server-rendered.
- Important caveat: visible pagination links such as `/case-studies/2/` are present in the markup, but a direct request to `https://www.crestdata.ai/case-studies/2/` returns HTTP `404 Not Found`. That suggests pagination is intended to work through client-side AJAX on the landing page rather than as normal server-side archive URLs.

## Recommended Scraping Strategy

- `requests + BeautifulSoup` should be enough for:
  - the first listing page
  - individual case-study detail pages
- Do not assume you can paginate by requesting `/case-studies/2/`, `/case-studies/3/`, etc.
- Recommended flow:
  1. Request `https://www.crestdata.ai/case-studies/`
  2. Parse case-study cards from the listing widget only
  3. Extract detail URLs
  4. Request each detail page directly and parse the article fields
  5. For full archive coverage, emulate the widget's AJAX pagination rather than following the visible page-number URLs
- A headless browser is optional, not required. It is only needed if you prefer not to reverse-engineer the AJAX pagination behavior.

## Suggested Selectors and Parsing Logic

### Listing Page

- Grid container: `#uc_post_list_elementor_0a09940`
- Card wrapper: `#uc_post_list_elementor_0a09940 .uc_post_list_box`
- Detail URL:
  - `.uc_post_list_title a`
  - or `.uc_post_list_image a`
- Title: `.uc_post_list_title a`
- Date: `.ue-meta-data .ue-grid-item-meta-data:first-child`
- Author: `.ue-meta-data .ue-grid-item-meta-data:nth-child(2)`
- Category fallback: `.uc_post_list_box[data-category]`
- Pagination widget: `#uc_archive_pagination_elementor_ff772e2`
- Page-count fallback: parse the `querydata` attribute on `#uc_post_list_elementor_0a09940`

### Listing Page Notes

- Ignore `.uc_post_content` as a primary excerpt source. It is noisy and appears to flatten breadcrumb/body fragments into the card text.
- Dedupe detail URLs per card because both the image and title point to the same page.
- Restrict extraction to the listing widget container so you do not capture unrelated case-study links from menus and other page sections.

### Detail Page

- Root article: `article.lqd-post-content.type-case-studies`
- Title: `header.lqd-post-header .entry-title`
- Author: `.entry-meta .entry-author a.url.fn`
- Publish date: `.posted-on time.entry-date.published`
- Visible category: `.cat-links a`
- Extra taxonomy fallback:
  - parse article classes such as `category-aws`, `category-cloudops`, `platform-aws`
- Hero image:
  - `.lqd-post-cover .wp-post-image`
  - fallback to `.entry-content .wp-post-image`
  - fallback to `meta[property="og:image"]`
- Main article body: `.entry-content.lqd-single-post-content`
- Content blocks: `.entry-content .elementor-widget-text-editor`
- Section headings:
  - `.entry-content .elementor-widget-text-editor h3`
  - `.entry-content .elementor-widget-text-editor h4`
  - `.entry-content .elementor-widget-text-editor h5`

### Image Parsing Notes

- Prefer `data-src` or `data-lazy-src`
- Fallback to `src` only if it is not an SVG placeholder
- Use `og:image` as a reliable fallback for the hero image

### Detail Page Scoping Notes

- Limit body extraction to `.entry-content`
- Exclude:
  - `footer.blog-post-footer`
  - `.share-links`
  - `nav.post-nav`

## Field Availability on Typical Detail Pages

Observed fields on newer case-study pages include:

- title
- publish date
- author
- category via the `Published in:` block
- hero image
- article body
- section headings
- internal body images
- breadcrumb trail
- previous article link

Observed metadata and fallback fields include:

- `meta[property="article:section"]`
- `meta[property="og:image"]`
- `meta[name="twitter:image"]`
- `meta[name="description"]`
- `time.entry-date.published[datetime]`
- article class names carrying taxonomy terms

Tags are not consistently exposed as a dedicated structured field on newer pages.

## Detail Page URL Pattern

- Primary pattern: `https://www.crestdata.ai/case-studies/<slug>/`
- Examples:
  - `https://www.crestdata.ai/case-studies/business-applications-through-resilient-aws-architecture/`
  - `https://www.crestdata.ai/case-studies/scaling-enterprise-sybase-monitoring-through-datadog-integration/`
  - `https://www.crestdata.ai/case-studies/crowdstrike-integration/`

## JavaScript Requirement Assessment

- Case-study detail pages do not appear to require JavaScript rendering for core content extraction.
- The first listing page also exposes the visible cards directly in HTML.
- Pagination is the main JavaScript-sensitive area.
- Conclusion:
  - `requests + BeautifulSoup` is sufficient for page 1 and for detail pages
  - full pagination likely requires reproducing the widget's AJAX behavior or using a browser-based approach

## Pagination Findings

- The listing page includes a pagination widget:
  - `#uc_archive_pagination_elementor_ff772e2`
- Visible links point to:
  - `/case-studies/2/`
  - `/case-studies/3/`
  - ...
  - `/case-studies/7/`
- However, a direct request to `https://www.crestdata.ai/case-studies/2/` returned HTTP `404 Not Found`.
- The listing grid itself is marked with AJAX-related attributes:
  - `data-ajax='true'`
  - `data-filterbehave='ajax'`
- The listing grid also exposes:
  - `querydata='{"count_posts":9,"total_posts":59,"page":1,"num_pages":7}'`
- The pagination script binds to widget events such as:
  - `uc_ajax_reloaded`
  - `init_filter`

Inference: the user-facing pagination is intended to update the listing through AJAX inside the page, not by loading a valid standalone URL for each numbered page.

## Assumptions and Risks

### Duplicate Links

- Each card repeats the detail URL in both the image link and the title link.
- Dedupe by normalized absolute URL.

### Broken Pagination Pages

- The visible pagination URLs are not valid archive pages when requested directly.
- This is the biggest scraping risk for full coverage.

### Inconsistent Layouts

- Newer 2025-2026 case studies use a richer structure with sections like:
  - `Executive Summary`
  - `About the Customer`
  - `Customer Challenge`
  - `Proposed Solution`
  - `Outcomes & Success Metrics`
- Older case studies can use different headings, for example:
  - `Business Challenge`
  - `Customer Solution`
  - `The Crest Difference`
- Older pages may also present inline `Tags:` content near the footer.

### Missing or Inconsistent Metadata

- Category is consistently visible in the `Published in:` block on inspected pages.
- Tags are inconsistent.
- Some taxonomy terms only appear in article class names rather than in a clean visible metadata block.

### Lazy-Loaded Images

- Many images use placeholder `src` values and store the real URL in `data-src` or `data-lazy-src`.
- Raw `img["src"]` is not reliable by itself.

### Over-Capture Risk

- If parsing is not scoped carefully, the page contains many unrelated links from:
  - top navigation
  - resource widgets
  - footer
  - advisor/leadership bios
- The scraper should stay inside the listing widget for archive parsing and inside the article content wrapper for detail parsing.

## Pages Inspected

- `https://www.crestdata.ai/case-studies/`
- `https://www.crestdata.ai/case-studies/2/`
- `https://www.crestdata.ai/case-studies/business-applications-through-resilient-aws-architecture/`
- `https://www.crestdata.ai/case-studies/scaling-enterprise-sybase-monitoring-through-datadog-integration/`
- `https://www.crestdata.ai/case-studies/crowdstrike-integration/`
