import io
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from tempfile import TemporaryDirectory

from anagram_cli.cli import main


class TestCli(unittest.TestCase):
    def test_two_words_that_are_anagrams(self) -> None:
        out = io.StringIO()
        with redirect_stdout(out):
            code = main(["listen", "silent"])
        self.assertEqual(code, 0)
        self.assertIn("are anagrams", out.getvalue())

    def test_two_words_that_are_not_anagrams(self) -> None:
        out = io.StringIO()
        with redirect_stdout(out):
            code = main(["hello", "world"])
        self.assertEqual(code, 1)
        self.assertIn("NOT anagrams", out.getvalue())

    def test_wordlist_mode_finds_matches(self) -> None:
        with TemporaryDirectory() as tmp:
            wordlist = Path(tmp) / "words.txt"
            wordlist.write_text("enlist\nsilent\nbanana\n")
            out = io.StringIO()
            with redirect_stdout(out):
                code = main(["listen", "--wordlist", str(wordlist)])
            self.assertEqual(code, 0)
            self.assertIn("enlist", out.getvalue())
            self.assertIn("silent", out.getvalue())
            self.assertNotIn("banana", out.getvalue())

    def test_wordlist_mode_no_matches(self) -> None:
        with TemporaryDirectory() as tmp:
            wordlist = Path(tmp) / "words.txt"
            wordlist.write_text("banana\norange\n")
            out = io.StringIO()
            with redirect_stdout(out):
                code = main(["listen", "--wordlist", str(wordlist)])
            self.assertEqual(code, 1)
            self.assertIn("no anagrams", out.getvalue())

    def test_wordlist_mode_requires_single_word(self) -> None:
        code = main(["listen", "extra", "--wordlist", "/nonexistent"])
        self.assertEqual(code, 2)

    def test_wrong_word_count_without_wordlist(self) -> None:
        code = main(["onlyone"])
        self.assertEqual(code, 2)

    def test_missing_wordlist_file_returns_error(self) -> None:
        code = main(["listen", "--wordlist", "/no/such/wordlist.txt"])
        self.assertEqual(code, 2)


if __name__ == "__main__":
    unittest.main()
