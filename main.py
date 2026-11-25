"""Invent a Word We Need entry for make.fun.

A small program that writes one coined word and its definition to
/output/entry.txt. The sandbox runs it twice and both runs must
produce identical bytes, so the entry is a fixed string: no random
choices, no clock, no network, no input of any kind.
"""

import os

OUT_PATH = "/output/entry.txt"
CHAR_LIMIT = 140
ENTRY = "sockorphan (n.): the lone sock left after laundry, its partner vanished without explanation."


def fail(message):
    """Abort loudly instead of writing an entry the gate would drop."""
    raise ValueError(message)


def validate(text):
    """Check the entry against the gate before anything is written."""
    if len(text) == 0:
        fail("entry is empty")
    if len(text) > CHAR_LIMIT:
        fail(f"entry runs {len(text)} characters; the gate allows {CHAR_LIMIT}")
    if text.strip() == "":
        fail("entry is only whitespace")
    if text != text.strip():
        fail("entry has leading or trailing whitespace")
    if "\n" in text or "\r" in text:
        fail("entry spans more than one line")
    for character in text:
        if ord(character) < 32:
            fail("entry holds a control character")
    return text


def save_entry():
    """Write the entry as UTF-8 with no trailing newline, then read it back."""
    folder = os.path.dirname(OUT_PATH)
    if folder:
        os.makedirs(folder, exist_ok=True)
    text = validate(ENTRY)
    with open(OUT_PATH, "w", encoding="utf-8", newline="") as handle:
        handle.write(text)
    with open(OUT_PATH, "r", encoding="utf-8", newline="") as handle:
        stored = handle.read()
    if stored != text:
        fail("read-back mismatch: the stored bytes differ from the entry")
    print(f"saved {len(text)} characters, {len(text.split())} words, to {OUT_PATH}")


if __name__ == "__main__":
    save_entry()
