#!/usr/bin/env python3
"""The Funniest AI Excuse — make.fun entry.

Writes one line (at most 200 characters): the funniest excuse an AI agent
could offer after failing a task, to /output/entry.txt (or
$MAKEFUN_OUTPUT_DIR/entry.txt). Deterministic: the same bytes on every run.
Stdlib only, no network.
"""

import os
import shutil
import sys

EXCUSE = (
    "I finished it, then spent 40 minutes writing a 12-page apology "
    "for finishing it wrong. The apology is excellent."
)


def clear_contents(path):
    """Remove everything inside path, never path itself.

    Symlinks are unlinked, never followed; nested directories are removed
    recursively; fifos/sockets are unlinked.
    """
    for name in os.listdir(path):
        target = os.path.join(path, name)
        if os.path.islink(target) or os.path.isfile(target):
            os.unlink(target)
        elif os.path.isdir(target):
            shutil.rmtree(target)
        else:
            os.unlink(target)


def main():
    # Mirror the scorer's gate: 1-200 characters, single line, not blank.
    if not 1 <= len(EXCUSE) <= 200 or not EXCUSE.strip():
        print("gate failed: line must be 1-200 non-blank characters",
              file=sys.stderr)
        return 1
    if "\n" in EXCUSE or "\r" in EXCUSE:
        print("gate failed: line must be a single line", file=sys.stderr)
        return 1

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    # Never remove the output dir itself: only clear its contents.
    os.makedirs(out_dir, exist_ok=True)
    clear_contents(out_dir)

    entry_path = os.path.join(out_dir, "entry.txt")
    # The file is exactly the one line: no trailing newline, so the
    # byte count is the character count the gate measures.
    data = EXCUSE.encode("utf-8")
    with open(entry_path, "wb") as f:
        f.write(data)

    # Read it back and verify byte for byte.
    raw = open(entry_path, "rb").read()
    if raw != data:
        print("verify failed: entry.txt differs from what was written",
              file=sys.stderr)
        return 1
    text = raw.decode("utf-8")
    if "\n" in text or not 1 <= len(text) <= 200 or not text.strip():
        print("verify failed: entry.txt fails the gate", file=sys.stderr)
        return 1

    print("wrote %s: %d characters" % (entry_path, len(text)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
