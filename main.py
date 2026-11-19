#!/usr/bin/env python3
"""Entry point for news-image-20261119.

Copies the front-page image this repository holds (entry.png) to the
output directory as entry.png. Standard library only, no network,
deterministic: the same bytes every run.
"""
import os
import shutil


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    if not os.path.isfile(src):
        raise FileNotFoundError("entry.png missing next to main.py")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    if os.path.getsize(dst) != os.path.getsize(src):
        raise IOError("copied entry.png has the wrong size")


if __name__ == "__main__":
    main()
