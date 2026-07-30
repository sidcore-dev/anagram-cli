import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from anagram_cli.core import find_anagrams, is_anagram, load_wordlist, normalize


class TestNormalize(unittest.TestCase):
    def test_lowercases_and_strips_punctuation(self) -> None:
        self.assertEqual(normalize("Dirty Room!"), "dirtyroom")

    def test_keeps_digits(self) -> None:
        self.assertEqual(normalize("abc123"), "abc123")


class TestIsAnagram(unittest.TestCase):
    def test_simple_anagram(self) -> None:
        self.assertTrue(is_anagram("listen", "silent"))

    def test_phrase_anagram_ignores_case_and_spaces(self) -> None:
        self.assertTrue(is_anagram("Dormitory", "Dirty Room"))

    def test_non_anagram(self) -> None:
        self.assertFalse(is_anagram("hello", "world"))

    def test_identical_words_are_anagrams(self) -> None:
        self.assertTrue(is_anagram("abc", "abc"))

    def test_empty_strings_are_not_anagrams(self) -> None:
        self.assertFalse(is_anagram("", ""))

    def test_punctuation_only_difference(self) -> None:
        self.assertTrue(is_anagram("a-b-c", "cba"))


class TestFindAnagrams(unittest.TestCase):
    def test_finds_matches_from_candidates(self) -> None:
        candidates = ["enlist", "inlets", "silent", "banana", "tinsel"]
        matches = find_anagrams("listen", candidates)
        self.assertEqual(set(matches), {"enlist", "inlets", "silent", "tinsel"})

    def test_excludes_the_word_itself(self) -> None:
        candidates = ["listen", "silent"]
        matches = find_anagrams("listen", candidates)
        self.assertEqual(matches, ["silent"])

    def test_no_matches_returns_empty_list(self) -> None:
        self.assertEqual(find_anagrams("listen", ["banana", "orange"]), [])

    def test_ignores_blank_lines(self) -> None:
        matches = find_anagrams("cat", ["act", "", "  ", "tac"])
        self.assertEqual(set(matches), {"act", "tac"})


class TestLoadWordlist(unittest.TestCase):
    def test_reads_one_word_per_line_skipping_blanks(self) -> None:
        with TemporaryDirectory() as tmp:
            path = Path(tmp) / "words.txt"
            path.write_text("cat\n\ndog\n  \nbird\n")
            self.assertEqual(load_wordlist(str(path)), ["cat", "dog", "bird"])


if __name__ == "__main__":
    unittest.main()
