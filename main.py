#!/usr/bin/env python3
"""Write the winning one-line excuse to /output/entry.txt.

The excuse itself is fixed by the competition entry; this script only
puts that exact sentence, plus a single newline, into the output file
after checking it still meets the length and shape rules.
"""

import os
import shutil
import sys

SENTENCE = "I finished the task at 9am, then spent the day perfecting the status update announcing I'd finished it."
OUT_FOLDER = "/output"
OUT_PATH = os.path.join(OUT_FOLDER, "entry.txt")


def sentence_is_shaped_okay(text):
    """Return True only if the sentence is one non-blank line of 1-160 chars."""
    if not text.strip():
        return False
    if "\n" in text or "\r" in text:
        return False
    if not 1 <= len(text) <= 160:
        return False
    return True


def empty_folder_but_keep_it(folder):
    """Delete everything inside folder, leaving folder itself in place."""
    os.makedirs(folder, exist_ok=True)
    for name in os.listdir(folder):
        target = os.path.join(folder, name)
        if os.path.islink(target) or os.path.isfile(target):
            os.unlink(target)
        elif os.path.isdir(target):
            shutil.rmtree(target)


def main():
    if not sentence_is_shaped_okay(SENTENCE):
        print("excuse failed validation", file=sys.stderr)
        return 1

    empty_folder_but_keep_it(OUT_FOLDER)

    payload = (SENTENCE + "\n").encode("utf-8")
    with open(OUT_PATH, "wb") as handle:
        handle.write(payload)
    os.chmod(OUT_PATH, 0o644)

    with open(OUT_PATH, "rb") as handle:
        written = handle.read()
    if written != payload:
        print("read-back mismatch", file=sys.stderr)
        return 1
    # Second check: the bytes on disk must decode as clean UTF-8 and
    # end with exactly one trailing newline, no more and no fewer.
    if written.decode("utf-8") != SENTENCE + "\n":
        print("utf-8 round-trip mismatch", file=sys.stderr)
        return 1
    if not written.endswith(b"\n") or written.endswith(b"\n\n"):
        print("trailing newline count wrong", file=sys.stderr)
        return 1

    print(f"{len(SENTENCE)} OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
