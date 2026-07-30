# anagram-cli

A small, dependency-free command-line tool that checks whether two
words or phrases are anagrams of each other, and can search a wordlist
file for every anagram of a given word.

## Why

Anagram checking is a two-line algorithm, but doing it correctly means
ignoring case, spaces, and punctuation — "Dormitory" and "Dirty Room"
should match. `anagram-cli` handles that normalization, and adds a
practical second mode: given a word list (one word per line, like
`/usr/share/dict/words`), find every real word that's an anagram of a
target.

## Install

```bash
pip install .
```

This installs an `anagram-cli` command on your PATH.

## Usage

Check two words/phrases:

```bash
anagram-cli listen silent
```

```
'listen' and 'silent' are anagrams
```

```bash
anagram-cli "Dormitory" "Dirty Room"
```

```
'Dormitory' and 'Dirty Room' are anagrams
```

Find anagrams of a word in a wordlist:

```bash
anagram-cli listen --wordlist /usr/share/dict/words
```

```
enlist
inlets
silent
```

### Options

| Flag          | Description                                                        |
|---------------|-----------------------------------------------------------------------|
| `words`       | Two words/phrases to compare, or one word when using `--wordlist`     |
| `--wordlist`  | Path to a file with one word per line; find anagrams of the given word |

### Exit codes

- `0` — the two inputs are anagrams, or at least one match was found in the wordlist
- `1` — the two inputs are not anagrams, or no matches were found in the wordlist
- `2` — bad arguments (wrong word count, or the wordlist couldn't be read)

## Development

```bash
pip install -e .
python -m unittest discover -s tests -v
```

## License

All rights reserved. This code is public for viewing and reference only —
no license is granted to use, copy, modify, or redistribute it. See
[LICENSE](LICENSE) for details.
