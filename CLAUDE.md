# CLAUDE.md

## Project Overview

**crest-insights** is a web scraper that crawls [Crest Data's case studies](https://www.crestdata.ai/case-studies/) and transforms them into structured JSON and markdown files. It scraped 59 case studies from the site with 100% success rate.

## Tech Stack

- **Python 3.10+** (uses `from __future__ import annotations`, `|` union types)
- **requests** (HTTP client with retry/backoff) and **beautifulsoup4** (HTML parsing)
- No test framework, no linter, no formatter currently configured
- Dependencies in `requirements.txt` (just `requests>=2.31.0` and `beautifulsoup4>=4.12.0`)

## Directory Structure

```
crestdata_case_studies/       # Main Python package (the scraper)
  main.py                     # Entry point, orchestrates scraping workflow
  config.py                   # All configuration: URLs, selectors, paths, rate limits
  client.py                   # HTTP session with rate limiting + retries
  pagination.py               # Elementor AJAX pagination for listing pages
  parsers.py                  # HTML parsing for listing cards and detail pages
  models.py                   # Dataclasses: HeroImage, Section, ListingCard, CaseStudyRecord
  state.py                    # Resumable state management (progress, failures)
  writers.py                  # Output: markdown rendering + JSON serialization
  utils.py                    # URL normalization, atomic writes, helpers
scripts/
  render_case_studies_markdown.py   # Re-render markdown from existing JSON
data/
  case_studies.json           # Master JSON output (59 records)
  logs/scrape.log             # Scraper execution log (gitignored)
  state/                      # Scraper state files (gitignored)
    progress.json
    failures.json
    items/*.json              # Per-case-study JSON checkpoints
markdown/                     # 59 generated markdown files (one per case study)
```

## How to Run

```bash
# Install dependencies
pip install -r requirements.txt

# Run the full scraper (fetches all case studies from crestdata.ai)
python -m crestdata_case_studies.main

# Re-render markdown from existing JSON (no network requests)
python scripts/render_case_studies_markdown.py
python scripts/render_case_studies_markdown.py --input data/case_studies.json --output-dir markdown
```

## Key Architecture Decisions

- **Elementor AJAX pagination**: Direct pagination URLs (`/case-studies/2/`) return 404. The scraper emulates the Elementor widget's internal AJAX requests (`?ucfrontajaxaction=getfiltersdata&...&ucpage=N`) to paginate through 7 listing pages.
- **Resumable scraping**: State is tracked in `data/state/`. The scraper skips already-completed URLs on re-run, allowing interrupted sessions to resume.
- **Atomic writes**: All file output uses temp-file-then-rename to prevent corruption on interruption.
- **Rate limiting**: 0.75s minimum between requests. Retries with exponential backoff (factor=1.0, jitter=0.35) on 429/5xx errors.
- **Hero image fallback chain**: Tries `data-src` -> `data-lazy-src` -> `src` -> `og:image` to handle WordPress lazy loading.

## Important Patterns

- **Config is centralized** in `config.py` -- CSS selectors, URLs, timeouts, paths are all defined there. Change selectors there if the site structure changes.
- **parsers.py is the most complex module** (~380 lines). It handles both listing card extraction and full detail page parsing with multiple fallback strategies for metadata.
- **writers.py `render_markdown()`** does custom HTML-to-markdown conversion supporting headings, lists, blockquotes, figures, tables, and inline formatting.
- All paths in config are relative (`Path("data")`, `Path("markdown")`). Run commands from the project root.

## Output Format

Each markdown file follows this structure:
```markdown
# Title
- URL: ...
- Canonical URL: ...
- Publish Date: ...
- Author: ...
- Tags: ...
- Hero Image: ...

![hero](url)

## Section Heading
Content...
```

JSON records contain: `url`, `canonical_url`, `slug`, `title`, `publish_date`, `author`, `tags`, `hero_image` (url/alt/source), `sections` (heading/level/html/text), `plain_text`, `raw_html`.

## What's Gitignored

- `__pycache__/`, `*.pyc`
- `data/logs/` (scraper logs)
- `data/state/` (progress tracking, item checkpoints)

Note: `data/case_studies.json`, `markdown/`, and `data/` root are tracked in git.
