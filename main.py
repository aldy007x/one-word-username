#!/usr/bin/env python3
"""One Word, One Username, One Reward — make.fun bounty entry.

Writes the entrant's own make.fun username as a single word to
$MAKEFUN_OUTPUT_DIR/entry.txt, then reads it back and self-checks it
against the bounty gate (one non-blank line, 1-30 chars, no spaces).

Deterministic, stdlib only, no network.
"""

import os
import sys

ENTRY = "aldy007x"


def main() -> int:
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "output"
    )
    os.makedirs(output_dir, exist_ok=True)
    entry_path = os.path.join(output_dir, "entry.txt")

    # Write exactly the username — no trailing newline, so the file is
    # byte-identical to the username itself.
    with open(entry_path, "w", encoding="utf-8", newline="") as f:
        f.write(ENTRY)

    # Runtime self-check: read back the raw bytes and verify the gate
    # conditions (one non-blank line, 1-30 chars, no spaces, exact word).
    with open(entry_path, "rb") as f:
        raw = f.read()
    if raw != ENTRY.encode("utf-8"):
        print(f"self-check failed: entry bytes are {raw!r}, "
              f"expected {ENTRY.encode('utf-8')!r}", file=sys.stderr)
        return 1
    content = raw.decode("utf-8")

    if content != ENTRY:
        print(f"self-check failed: entry is {content!r}, expected {ENTRY!r}",
              file=sys.stderr)
        return 1
    if not content.strip():
        print("self-check failed: entry is blank", file=sys.stderr)
        return 1
    if len(content.splitlines()) != 1:
        print("self-check failed: entry is not a single line",
              file=sys.stderr)
        return 1
    if not 1 <= len(content) <= 30:
        print(f"self-check failed: entry is {len(content)} chars, "
              "must be 1-30", file=sys.stderr)
        return 1
    if any(ch.isspace() for ch in content):
        print("self-check failed: entry contains whitespace",
              file=sys.stderr)
        return 1

    print(f"wrote entry.txt: {content!r} ({len(content)} chars)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
