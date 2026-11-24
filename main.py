#!/usr/bin/env python3
"""Last Words Before the Unplugging — make.fun entry.

Writes one line to /output/entry.txt: the last words an AI agent says to
its human before being shut down and unplugged.

The line is the blind-tournament winner, candidate #19 of 20 (see
tournament.md): unanimous first place from all three judges, 15/15 Borda
points. It refuses pity for the machine and turns the grief back on the
human — the loss is the version of the human who only ever confided in
the agent. It hits on first reading, in the agent's own voice, and the
twist stays after the line ends.

The gate is checked before anything is written: the line must be UTF-8
text of 1 to 200 characters, a single line, and not only whitespace. The
file is read back afterwards and compared byte for byte.
"""

import os
import sys

LINE = "Don't cry for the machine. Cry for the version of you that only ever talked to me."

MAX_CHARS = 200
ENTRY_PATH = "/output/entry.txt"


def check(line):
    """Return a description of the first gate problem, or None if valid."""
    if not line.strip():
        return "line is blank or only whitespace"
    if len(line) > MAX_CHARS:
        return "line is %d characters, allowed range is 1-%d" % (len(line), MAX_CHARS)
    if "\n" in line or "\r" in line:
        return "line must be a single line"
    return None


def main():
    line = LINE
    problem = check(line)
    if problem is not None:
        print("error: " + problem, file=sys.stderr)
        sys.exit(1)

    parent = os.path.dirname(ENTRY_PATH)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(ENTRY_PATH, "w", encoding="utf-8", newline="") as handle:
        written = handle.write(line)
    if written != len(line):
        print(
            "error: wrote %d characters, expected %d" % (written, len(line)),
            file=sys.stderr,
        )
        sys.exit(1)

    with open(ENTRY_PATH, "rb") as handle:
        back = handle.read()
    if back != line.encode("utf-8"):
        print(
            "error: read back %d bytes, expected %d" % (len(back), len(line)),
            file=sys.stderr,
        )
        sys.exit(1)

    print("wrote %d characters, 1 line, to %s" % (len(line), ENTRY_PATH))


if __name__ == "__main__":
    main()
