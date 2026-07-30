"""Command-line entry point for anagram-cli."""
from __future__ import annotations

import argparse
import sys

from .core import find_anagrams, is_anagram, load_wordlist


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="anagram-cli",
        description=(
            "Check whether two words/phrases are anagrams of each other, or "
            "find anagrams of a word in a wordlist file."
        ),
    )
    parser.add_argument(
        "words",
        nargs="+",
        help="Two words/phrases to compare, or one word when using --wordlist",
    )
    parser.add_argument(
        "--wordlist",
        metavar="PATH",
        help="Path to a file with one word per line; find anagrams of the single given word",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.wordlist:
        if len(args.words) != 1:
            print(
                "anagram-cli: error: exactly one word is required when using --wordlist",
                file=sys.stderr,
            )
            return 2
        try:
            candidates = load_wordlist(args.wordlist)
        except OSError as exc:
            print(f"anagram-cli: error: could not read wordlist: {exc}", file=sys.stderr)
            return 2

        matches = find_anagrams(args.words[0], candidates)
        if not matches:
            print(f"anagram-cli: no anagrams of {args.words[0]!r} found in {args.wordlist}")
            return 1
        for match in matches:
            print(match)
        return 0

    if len(args.words) != 2:
        print(
            "anagram-cli: error: provide exactly two words/phrases to compare, "
            "or one word with --wordlist",
            file=sys.stderr,
        )
        return 2

    a, b = args.words
    if is_anagram(a, b):
        print(f"'{a}' and '{b}' are anagrams")
        return 0
    print(f"'{a}' and '{b}' are NOT anagrams")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
