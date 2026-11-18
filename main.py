#!/usr/bin/env python3
"""news-image-20261117 entry: copy the finished front page to /output/entry.png.

Standard library only, no network. The image (entry.png, 1024x1024, drawn
at build time from the real news of Tuesday 17 November 2026) sits beside
this file; the program just copies it to the output directory.

Run locally:  mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""
import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
OUT.mkdir(parents=True, exist_ok=True)
# Byte-identical copy every run: no timestamps, no randomness, no network.
shutil.copyfile(HERE / "entry.png", OUT / "entry.png")
