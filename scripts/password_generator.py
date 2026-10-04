#!/usr/bin/env python3
"""Generate strong passwords or readable passphrases."""

from __future__ import annotations

import argparse
import secrets
import string


WORDS = (
    "anchor", "atlas", "binary", "breeze", "cactus", "candle", "cobalt",
    "comet", "coral", "delta", "ember", "falcon", "forest", "galaxy",
    "harbor", "island", "jacket", "kernel", "lantern", "matrix", "meteor",
    "nebula", "orange", "pixel", "quantum", "river", "signal", "silver",
    "summit", "tiger", "velvet", "voyage", "window", "yellow", "zenith",
)


def build_charset(args: argparse.Namespace) -> str:
    chars = ""
    if args.lower:
        chars += string.ascii_lowercase
    if args.upper:
        chars += string.ascii_uppercase
    if args.digits:
        chars += string.digits
    if args.symbols:
        chars += "!@#$%^&*()-_=+[]{};:,.?/"
    if not chars:
        raise SystemExit("Choose at least one character set.")
    return chars


def generate_password(length: int, chars: str) -> str:
    return "".join(secrets.choice(chars) for _ in range(length))


def generate_passphrase(words: int, separator: str) -> str:
    return separator.join(secrets.choice(WORDS) for _ in range(words))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("-n", "--count", type=int, default=5, help="number to generate")
    parser.add_argument("-l", "--length", type=int, default=20, help="password length")
    parser.add_argument("--passphrase", action="store_true", help="generate word passphrases")
    parser.add_argument("--words", type=int, default=5, help="words per passphrase")
    parser.add_argument("--separator", default="-", help="passphrase separator")
    parser.add_argument("--lower", action=argparse.BooleanOptionalAction, default=True)
    parser.add_argument("--upper", action=argparse.BooleanOptionalAction, default=True)
    parser.add_argument("--digits", action=argparse.BooleanOptionalAction, default=True)
    parser.add_argument("--symbols", action=argparse.BooleanOptionalAction, default=True)
    args = parser.parse_args()

    if args.count < 1:
        raise SystemExit("Count must be at least 1.")
    if args.passphrase:
        if args.words < 2:
            raise SystemExit("Passphrases need at least 2 words.")
        for _ in range(args.count):
            print(generate_passphrase(args.words, args.separator))
        return

    if args.length < 8:
        raise SystemExit("Use length 8 or higher.")
    chars = build_charset(args)
    for _ in range(args.count):
        print(generate_password(args.length, chars))


if __name__ == "__main__":
    main()

