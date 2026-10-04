#!/usr/bin/env python3
"""Remove duplicate CSV rows while preserving order."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--columns", nargs="*", help="dedupe by these header names")
    args = parser.parse_args()

    with args.input.open("r", newline="", encoding="utf-8-sig") as source:
        reader = csv.DictReader(source)
        if not reader.fieldnames:
            raise SystemExit("Input CSV has no header row.")
        columns = args.columns or reader.fieldnames
        missing = [column for column in columns if column not in reader.fieldnames]
        if missing:
            raise SystemExit(f"Missing columns: {', '.join(missing)}")

        seen: set[tuple[str, ...]] = set()
        rows = []
        for row in reader:
            key = tuple(row.get(column, "") for column in columns)
            if key in seen:
                continue
            seen.add(key)
            rows.append(row)

    with args.output.open("w", newline="", encoding="utf-8") as target:
        writer = csv.DictWriter(target, fieldnames=reader.fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"wrote {len(rows)} unique rows to {args.output}")


if __name__ == "__main__":
    main()

