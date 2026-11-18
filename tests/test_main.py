#!/usr/bin/env python3
"""Small checks for news-image-20261118: run main.py twice, outputs must
be byte-identical to each other and to assets/master.png, 1024x1024,
under 1 MiB."""
import hashlib
import os
import subprocess
import sys
import tempfile
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def sha256(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def main():
    master = os.path.join(ROOT, "assets", "master.png")
    assert os.path.isfile(master), "master.png missing; run src/image_pipeline.py first"
    assert os.path.getsize(master) <= 1048576, "master.png exceeds 1 MiB"
    with Image.open(master) as im:
        assert im.size == (1024, 1024), f"master.png is {im.size}"
    with tempfile.TemporaryDirectory() as d1, tempfile.TemporaryDirectory() as d2:
        env1 = dict(os.environ, MAKEFUN_OUTPUT_DIR=d1)
        env2 = dict(os.environ, MAKEFUN_OUTPUT_DIR=d2)
        subprocess.run([sys.executable, os.path.join(ROOT, "main.py")],
                       env=env1, check=True, capture_output=True)
        subprocess.run([sys.executable, os.path.join(ROOT, "main.py")],
                       env=env2, check=True, capture_output=True)
        o1, o2 = os.path.join(d1, "entry.png"), os.path.join(d2, "entry.png")
        assert os.path.isfile(o1) and os.path.isfile(o2), "missing output"
        h1, h2, hm = sha256(o1), sha256(o2), sha256(master)
        assert h1 == h2 == hm, f"not byte-identical: {h1} {h2} {hm}"
    print(f"OK: deterministic, byte-identical to master, 1024x1024, "
          f"under 1 MiB (sha256 {hm[:16]}...)")


if __name__ == "__main__":
    main()
