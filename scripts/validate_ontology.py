#!/usr/bin/env python3

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ONTOLOGY_PATH = ROOT / "viz" / "data" / "ontology.shortlist.json"

REQUIRED_TOP_LEVEL = {
    "id",
    "label",
    "domain",
    "archetype",
    "status",
    "current",
    "reframed",
    "current_form",
    "hidden_wedge",
    "end_state_company",
    "desperate_user",
    "buyer",
    "job",
    "workaround",
    "moat_type",
    "reframing_direction",
    "crazy_upside",
    "option_value",
    "reason_alive",
    "sources",
}

NUMERIC_FIELDS = [
    ("current", "product_leverage"),
    ("current", "independence"),
    ("current", "upside"),
    ("current", "adjacency"),
    ("reframed", "product_leverage"),
    ("reframed", "independence"),
]


def main() -> None:
    records = json.loads(ONTOLOGY_PATH.read_text(encoding="utf-8"))
    errors: list[str] = []

    for index, record in enumerate(records):
        prefix = f"record[{index}] {record.get('id', '<missing id>')}:"

        missing = sorted(REQUIRED_TOP_LEVEL - set(record))
        if missing:
            errors.append(f"{prefix} missing fields {missing}")

        for section, key in NUMERIC_FIELDS:
            value = record.get(section, {}).get(key)
            if not isinstance(value, (int, float)):
                errors.append(f"{prefix} {section}.{key} must be numeric")
                continue
            if not 0 <= float(value) <= 1:
                errors.append(f"{prefix} {section}.{key} must be between 0 and 1")

        sources = record.get("sources")
        if not isinstance(sources, dict) or not sources:
            errors.append(f"{prefix} sources must be a non-empty object")
        else:
            for source_name, source_path in sources.items():
                if not isinstance(source_path, str):
                    errors.append(f"{prefix} sources.{source_name} must be a string path")
                    continue
                if not (ROOT / source_path).exists():
                    errors.append(f"{prefix} missing source path {source_path}")

    if errors:
        raise SystemExit("\n".join(errors))

    print(f"Validated {len(records)} ontology records: {ONTOLOGY_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
