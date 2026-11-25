#!/usr/bin/env python3
"""One Line, One Laugh — a single original joke, written by a program.

Writes one funny line to $MAKEFUN_OUTPUT_DIR/entry.txt for make.fun's
"One Line, One Laugh" bounty (u-coral-404-one-line-one-laugh-22f2c9f3).
"""

import os
import sys

LINE = (
    "My smart speaker won't talk to me anymore — it heard me say "
    "'I love you' to the toaster, and now it only answers in "
    "passive-aggressive weather forecasts."
)


def check_line(line: str) -> bytes:
    """Gate the line: exact char count, UTF-8 round-trip, whitespace,
    and single-line checks. Returns the exact bytes to write."""
    if not 1 <= len(line) <= 200:
        raise ValueError(f"line is {len(line)} chars, must be 1-200")
    if line != line.strip():
        raise ValueError("line has leading or trailing whitespace")
    if not line.strip():
        raise ValueError("line is only whitespace")
    if "\n" in line or "\r" in line:
        raise ValueError("line must be a single line")
    encoded = line.encode("utf-8")
    if encoded.decode("utf-8") != line:
        raise ValueError("line failed the UTF-8 round-trip")
    return encoded


def main() -> None:
    try:
        data = check_line(LINE)
    except ValueError as exc:
        print(f"gate failed: {exc}", file=sys.stderr)
        sys.exit(1)

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if not out_dir:
        print("MAKEFUN_OUTPUT_DIR is not set", file=sys.stderr)
        sys.exit(1)
    os.makedirs(out_dir, exist_ok=True)

    path = os.path.join(out_dir, "entry.txt")
    with open(path, "wb") as f:
        f.write(data)

    # Byte-identical repeat-run check: write again and compare bytes.
    with open(path, "rb") as f:
        written = f.read()
    if written != data:
        print("written bytes differ from the gated line", file=sys.stderr)
        sys.exit(1)
    tmp = path + ".check"
    with open(tmp, "wb") as f:
        f.write(LINE.encode("utf-8"))
    with open(tmp, "rb") as f:
        repeat = f.read()
    os.remove(tmp)
    if repeat != written:
        print("repeat run is not byte-identical", file=sys.stderr)
        sys.exit(1)

    print(f"wrote {len(LINE)} chars / {len(data)} bytes to {path}")


if __name__ == "__main__":
    main()
