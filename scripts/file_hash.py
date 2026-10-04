#!/usr/bin/env python3
"""Print file hashes."""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path


def hash_file(path: Path, algorithm: str) -> str:
    digest = hashlib.new(algorithm)
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("files", nargs="+", type=Path)
    parser.add_argument("-a", "--algorithm", default="sha256", choices=("sha256", "sha1", "md5"))
    args = parser.parse_args()

    for file_path in args.files:
        if not file_path.is_file():
            print(f"{file_path}: not a file")
            continue
        print(f"{hash_file(file_path, args.algorithm)}  {file_path}")


if __name__ == "__main__":
    main()

