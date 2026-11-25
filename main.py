"""Invent a Word We Need entry for make.fun.

Writes one line to /output/entry.txt: a freshly coined English word
with its one-line definition. The sandbox runs this program twice and
both runs must write the same bytes, so the line is a fixed string
with no randomness, clock, or network access. The word names a small
household loss everyone recognises at once: the lone sock left after
laundry, its partner vanished without explanation, a thing English
has never had a single word for.
"""

import os

MAX_CHARS = 140
ENTRY_PATH = "/output/entry.txt"

LINE = "sockorphan (n.): the lone sock left after laundry, its partner vanished without explanation."


def check_line(line: str) -> str:
    """Return the line unchanged, guarding the gate's limits.

    The gate accepts UTF-8 text of 1 to 140 characters that is not
    only white space, so fail loudly here rather than write an entry
    the judge never sees.
    """
    if not line or len(line) > MAX_CHARS:
        raise ValueError(
            f"length rule failed: entry is {len(line)} characters, limit is {MAX_CHARS}"
        )
    if not line.strip():
        raise ValueError("entry must not be only white space")
    if line.strip() != line or "\n" in line or "\r" in line:
        raise ValueError(
            "single-line rule failed: entry has surrounding whitespace or a line break"
        )
    if any(ord(ch) < 32 for ch in line):
        raise ValueError(
            "control-character rule failed: entry contains a control character"
        )
    return line


def write_entry(path: str = ENTRY_PATH) -> None:
    """Write the line as UTF-8 with no trailing newline, then verify it.

    Read back what was written and compare bytes, so a partial write
    is caught here instead of in the sandbox.
    """
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    text = check_line(LINE)
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(text)
    with open(path, "r", encoding="utf-8", newline="") as handle:
        written = handle.read()
    if written != text:
        raise ValueError("read-back verification failed: written bytes differ")
    if len(written.encode("utf-8")) != len(text.encode("utf-8")):
        raise ValueError("read-back verification failed: byte length differs")
    print(f"wrote {len(text)} characters, {len(text.split())} words to {path}")


if __name__ == "__main__":
    write_entry()
