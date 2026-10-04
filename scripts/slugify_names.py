#!/usr/bin/env python3
"""Rename files to lowercase safe names."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


def slugify(name: str) -> str:
    stem, dot, suffix = name.rpartition(".")
    base = stem if dot else name
    ext = f".{suffix.lower()}" if dot else ""
    safe = re.sub(r"[^a-z0-9]+", "-", base.lower()).strip("-")
    return f"{safe or 'file'}{ext}"


def unique_path(path: Path) -> Path:
    if not path.exists():
        return path
    stem, suffix = path.stem, path.suffix
    counter = 2
    while True:
        candidate = path.with_name(f"{stem}-{counter}{suffix}")
        if not candidate.exists():
            return candidate
        counter += 1


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="+", type=Path)
    parser.add_argument("--apply", action="store_true", help="actually rename files")
    args = parser.parse_args()

    for original in args.paths:
        if not original.exists():
            print(f"{original}: missing")
            continue
        target = unique_path(original.with_name(slugify(original.name)))
        if original == target:
            print(f"{original}: already clean")
            continue
        print(f"{original} -> {target}")
        if args.apply:
            original.rename(target)


if __name__ == "__main__":
    main()

