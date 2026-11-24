#!/usr/bin/env python3
"""The Vacuum's Alibi: One Line, 200 Characters.

Writes a single deadpan excuse from a robot vacuum to
/output/entry.txt (or $MAKEFUN_OUTPUT_DIR/entry.txt when set).

The line is the calibrated pick (proxy 22/22, 69 characters):
    I classified it as load-bearing dust. Touch it and the rug collapses.

Stdlib only. No network, no randomness: the output is deterministic.

Version history:
  v1 (2026-11-24): fresh rewrite — single calibrated line + self-check gate.
  v2 (2026-11-24): added no-leading/trailing-whitespace gate and a
      read-back verification after writing, so a truncated or altered
      file fails loudly instead of silently passing the gate.
"""

import os

ENTRY = "I classified it as load-bearing dust. Touch it and the rug collapses."

MIN_CHARS = 1
MAX_CHARS = 200


def main() -> None:
    line = ENTRY

    # Self-check gate: 1-200 characters, exactly one line, UTF-8, non-whitespace.
    assert MIN_CHARS <= len(line) <= MAX_CHARS, "entry length out of range"
    assert "\n" not in line and "\r" not in line, "entry must be a single line"
    assert line.strip(), "entry must not be only whitespace"
    assert line == line.strip(), "entry must not start or end with whitespace"
    line.encode("utf-8")

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(line)

    # Read-back verification: what landed on disk must be exactly the line.
    with open(path, "r", encoding="utf-8", newline="") as f:
        assert f.read() == line, "written entry does not match the line"


if __name__ == "__main__":
    main()
