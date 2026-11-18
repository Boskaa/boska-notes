#!/usr/bin/env python3
"""Rasterize every page of the source PDFs so they can be inspected visually.

usage: python render_pages.py OUT_DIR DPI file1.pdf [file2.pdf ...]
Writes OUT_DIR/<stem>-<page>.png (needs poppler's pdftoppm on PATH).
Use ~110 dpi to read pages, ~220-300 dpi to zoom on formulas and to crop figures.
"""
import pathlib
import subprocess
import sys

if len(sys.argv) < 4:
    sys.exit(__doc__)
out = pathlib.Path(sys.argv[1])
dpi = sys.argv[2]
out.mkdir(parents=True, exist_ok=True)
for f in sys.argv[3:]:
    stem = pathlib.Path(f).stem.replace(" ", "_")
    subprocess.run(["pdftoppm", "-r", dpi, "-png", f, str(out / stem)], check=True)
    print("rendered", f)
