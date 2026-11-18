#!/usr/bin/env python3
"""Entrypoint for news-image-20261118 (Python 3.13).

Copies the validated master image (assets/master.png) to the output
directory as entry.png. Deterministic, offline, no timestamps, no random
elements: two runs produce byte-identical output.
"""
import os
import shutil
import sys


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "assets", "master.png")
    if not os.path.isfile(src):
        print(f"missing master image: {src}", file=sys.stderr)
        sys.exit(1)
    if os.path.getsize(src) > 1048576:
        print(f"master image exceeds 1 MiB: {src}", file=sys.stderr)
        sys.exit(1)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    print(f"wrote {dst} ({os.path.getsize(dst)} bytes)")


if __name__ == "__main__":
    main()
