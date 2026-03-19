#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any, Iterable

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from crestdata_case_studies.models import CaseStudyRecord
from crestdata_case_studies.utils import atomic_write_text, ensure_directories, slug_from_url
from crestdata_case_studies.writers import render_markdown


def main() -> None:
    args = parse_args()
    input_path = args.input
    output_dir = args.output_dir

    ensure_directories([output_dir])
    records = list(load_records(input_path))
    if not records:
        raise SystemExit(f"No case study records found in {input_path}")

    written = 0
    for record in records:
        slug = record.slug or slug_from_url(record.canonical_url or record.url)
        if not slug:
            raise ValueError(f"Unable to determine slug for record: {record.url!r}")

        markdown = render_markdown(record)
        output_path = output_dir / f"{slug}.md"
        atomic_write_text(output_path, markdown)
        written += 1

    print(f"Wrote {written} Markdown files to {output_dir}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Render Crest Data case-study JSON records into individual Markdown files."
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=Path("data/case_studies.json"),
        help="Path to the master JSON file, a single item JSON file, or a directory of item JSON files.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("data/markdown"),
        help="Directory where individual Markdown files will be written.",
    )
    return parser.parse_args()


def load_records(input_path: Path) -> Iterable[CaseStudyRecord]:
    if not input_path.exists():
        raise FileNotFoundError(f"Input path does not exist: {input_path}")

    if input_path.is_dir():
        for json_path in sorted(input_path.glob("*.json")):
            payload = json.loads(json_path.read_text(encoding="utf-8"))
            yield CaseStudyRecord.from_dict(_coerce_record_dict(payload, source=json_path))
        return

    payload = json.loads(input_path.read_text(encoding="utf-8"))
    if isinstance(payload, list):
        for item in payload:
            yield CaseStudyRecord.from_dict(_coerce_record_dict(item, source=input_path))
        return

    if isinstance(payload, dict):
        yield CaseStudyRecord.from_dict(_coerce_record_dict(payload, source=input_path))
        return

    raise ValueError(f"Unsupported JSON payload in {input_path}: expected object or array")


def _coerce_record_dict(payload: Any, *, source: Path) -> dict[str, Any]:
    if not isinstance(payload, dict):
        raise ValueError(f"Record in {source} is not a JSON object")
    return payload


if __name__ == "__main__":
    main()
