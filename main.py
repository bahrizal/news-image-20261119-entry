#!/usr/bin/env python3
"""news-image-20261119: place the rendered front page where the harness reads it.

Reads the PNG this repository ships and writes it to the harness output
directory as entry.png. No network, no randomness: the bytes out are the
bytes in, every run.
"""
import os
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "entry.png"


def place_front_page() -> int:
    payload = SOURCE.read_bytes()
    if not payload:
        raise ValueError("entry.png is empty")
    target_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / "entry.png"
    target.write_bytes(payload)
    written = target.stat().st_size
    if written != len(payload):
        raise IOError("entry.png came out the wrong size")
    return written


if __name__ == "__main__":
    place_front_page()
