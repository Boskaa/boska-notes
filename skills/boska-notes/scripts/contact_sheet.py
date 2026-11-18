#!/usr/bin/env python3
"""Render the compiled guide and tile its pages into contact sheets for the final check.

usage: python contact_sheet.py guide.pdf OUT_DIR [--dpi 60] [--cols 4]
Writes OUT_DIR/sheet-<n>.png (cols pages per sheet). Look at every sheet; re-render a
single page at ~110 dpi (pdftoppm -r 110 -f N -l N) to check formulas closely.
"""
import argparse
import glob
import pathlib
import subprocess

from PIL import Image

p = argparse.ArgumentParser()
p.add_argument("pdf")
p.add_argument("out")
p.add_argument("--dpi", default="60")
p.add_argument("--cols", type=int, default=4)
a = p.parse_args()

out = pathlib.Path(a.out)
out.mkdir(parents=True, exist_ok=True)
subprocess.run(["pdftoppm", "-r", a.dpi, "-png", a.pdf, str(out / "pg")], check=True)
pages = sorted(glob.glob(str(out / "pg-*.png")))
ims = [Image.open(f) for f in pages]
w, h = ims[0].size
for k in range(0, len(ims), a.cols):
    sheet = Image.new("RGB", (a.cols * (w + 10), h), "gray")
    for j, im in enumerate(ims[k:k + a.cols]):
        sheet.paste(im, (j * (w + 10), 0))
    sheet.save(out / f"sheet-{k // a.cols + 1}.png")
print(f"{len(ims)} pages -> {(len(ims) + a.cols - 1) // a.cols} sheets in {out}")
