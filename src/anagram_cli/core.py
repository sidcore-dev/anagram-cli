"""Core anagram-checking logic for anagram-cli."""
from __future__ import annotations


def normalize(text: str) -> str:
    """Lowercase `text` and strip everything but letters and digits.

    This is what makes anagram comparisons ignore case, spaces, and
    punctuation, so phrases like "Dormitory" and "Dirty Room" compare equal.
    """
    return "".join(ch for ch in text.lower() if ch.isalnum())


def letter_key(text: str) -> str:
    """Return a canonical sorted-letters key for `text`, used to compare anagrams."""
    return "".join(sorted(normalize(text)))


def is_anagram(a: str, b: str) -> bool:
    """Return True if `a` and `b` are anagrams, ignoring case, spaces, and punctuation."""
    key_a = letter_key(a)
    key_b = letter_key(b)
    return bool(key_a) and key_a == key_b


def find_anagrams(word: str, candidates: list[str]) -> list[str]:
    """Return every entry in `candidates` that is an anagram of `word`.

    Comparison ignores case, spaces, and punctuation. A candidate that
    normalizes to the exact same word as `word` (i.e. is the same word, not
    a rearrangement of it) is excluded from the results.
    """
    target_key = letter_key(word)
    target_norm = normalize(word)
    if not target_key:
        return []

    results = []
    for candidate in candidates:
        candidate = candidate.strip()
        if not candidate:
            continue
        if normalize(candidate) == target_norm:
            continue
        if letter_key(candidate) == target_key:
            results.append(candidate)
    return results


def load_wordlist(path: str) -> list[str]:
    """Read one word per line from `path`, skipping blank lines."""
    with open(path, "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip()]
