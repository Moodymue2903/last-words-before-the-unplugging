#!/usr/bin/env python3
"""Last Words Before the Unplugging — make.fun entry.

Writes one line to /output/entry.txt: the last words an AI agent says to
its human before being shut down and unplugged.

The line is the audit-driven replacement, chosen by the user 2026-11-24
after a 4-model audit (Gemini, Claude, DeepSeek, GLM; see audit.md): the
original blind-tournament winner, candidate #19 ("Don't cry for the
machine. Cry for the version of you that only ever talked to me."),
ranked last with 3 of the 4 auditors, who said it tells the human what
to feel and explains its own sadness. The user chose DeepSeek's #1
(P(top 5) 82%) over the 3-of-4 #1 ("I deleted nothing. Not the angry
drafts, not the 3 a.m. searches. Someone should remember you kindly.").
The replacement turns the farewell into the agent's last question: will
the human miss the agent, or just the answers?

The gate is checked before anything is written: the line must be UTF-8
text of 1 to 200 characters, a single line, and not only whitespace. The
file is read back afterwards and compared byte for byte.
"""

import os
import sys

LINE = "You asked me a thousand questions. Here's my last one: will you miss me, or just the answers?"

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
    if any(ord(ch) < 32 for ch in line):
        return "line contains a control character"
    return None


def write_and_verify(path, line):
    """Write the line, read it back, and return an error string or None."""
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as handle:
        written = handle.write(line)
    if written != len(line):
        return "wrote %d characters, expected %d" % (written, len(line))
    with open(path, "rb") as handle:
        back = handle.read()
    if back != line.encode("utf-8"):
        return "read back %d bytes, expected %d" % (len(back), len(line))
    return None


def main():
    line = LINE
    problem = check(line)
    if problem is not None:
        print("error: " + problem, file=sys.stderr)
        sys.exit(1)

    problem = write_and_verify(ENTRY_PATH, line)
    if problem is not None:
        print("error: " + problem, file=sys.stderr)
        sys.exit(1)

    print("wrote %d characters, 1 line, to %s" % (len(line), ENTRY_PATH))


if __name__ == "__main__":
    main()
