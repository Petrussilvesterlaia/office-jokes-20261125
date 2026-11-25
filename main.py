#!/usr/bin/env python3
"""One-Line Office Jokes — entry program.

Writes a single original one-line joke about office life to
/output/entry.txt, then validates it against the scorer gate:
UTF-8 text, 1-199 characters, one line, not only whitespace.
"""

import os
import sys

OUTPUT_PATH = "/output/entry.txt"

# Original one-line office joke, written in this session.
JOKE = "I declined Monday's meeting to finally get some work done, so they rescheduled it for Monday."


def validate(text):
    """Check the entry against the scorer gate. Returns a list of problems."""
    problems = []
    if not isinstance(text, str):
        problems.append("entry is not text")
        return problems
    if len(text) < 1:
        problems.append("entry is empty (must be 1-199 characters)")
    if len(text) > 199:
        problems.append("entry is %d characters (must be 1-199)" % len(text))
    if text.strip() == "":
        problems.append("entry is only whitespace")
    if "\n" in text or "\r" in text:
        problems.append("entry spans more than one line")
    # No control characters other than the ones already excluded above:
    # they would not survive as clean single-line UTF-8 text.
    for ch in text:
        if ord(ch) < 0x20 and ch not in ("\t",):
            problems.append("entry contains control character U+%04X" % ord(ch))
    # No stray leading/trailing space: the joke must read as one clean line.
    if text != text.strip():
        problems.append("entry has leading or trailing whitespace")
    # UTF-8 round-trip: the exact bytes written must decode back identically.
    try:
        if text.encode("utf-8").decode("utf-8") != text:
            problems.append("entry fails UTF-8 round-trip")
    except UnicodeError as exc:
        problems.append("entry is not valid UTF-8: %s" % exc)
    return problems


def main():
    problems = validate(JOKE)
    if problems:
        for problem in problems:
            print("VALIDATION FAILED: %s" % problem, file=sys.stderr)
        return 1

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="") as f:
        f.write(JOKE)

    # Read-back verification: the file must contain exactly the joke,
    # as valid UTF-8, on one line, within the length gate.
    with open(OUTPUT_PATH, "r", encoding="utf-8") as f:
        read_back = f.read()
    if read_back != JOKE:
        print("READ-BACK FAILED: file content differs from the joke",
              file=sys.stderr)
        return 1
    read_back_problems = validate(read_back)
    if read_back_problems:
        for problem in read_back_problems:
            print("READ-BACK VALIDATION FAILED: %s" % problem, file=sys.stderr)
        return 1

    print("OK: wrote %d characters to %s" % (len(JOKE), OUTPUT_PATH))
    print("Entry: %s" % JOKE)
    return 0


if __name__ == "__main__":
    sys.exit(main())
