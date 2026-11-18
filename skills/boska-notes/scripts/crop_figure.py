#!/usr/bin/env python3
"""Crop a figure from a rendered page and (optionally) remove a light background grid.

usage: python crop_figure.py PAGE.png OUT.png X0 Y0 X1 Y1 [--frac] [--grid] [--thr 165]
                             [--blank X0 Y0 X1 Y1 ...]

Coordinates are pixels of PAGE.png, or fractions 0..1 of its width/height with --frac.
--grid   : turn near-white/pale pixels (min RGB channel > thr) to pure white. This removes
           the pale squared/lined paper of handwritten notes while keeping dark ink and
           saturated highlighter colours (cyan, green, ...).
--blank  : whiten a rectangle (same unit as the crop, relative to the page) to hide stray
           text that falls inside the crop box; repeatable.
Needs Pillow and numpy.
"""
import argparse

import numpy as np
from PIL import Image

p = argparse.ArgumentParser()
p.add_argument("page")
p.add_argument("out")
p.add_argument("box", nargs=4, type=float)
p.add_argument("--frac", action="store_true")
p.add_argument("--grid", action="store_true")
p.add_argument("--thr", type=int, default=165)
p.add_argument("--blank", nargs=4, type=float, action="append", default=[])
a = p.parse_args()

im = Image.open(a.page).convert("RGB")
W, H = im.size


def px(b):
    if a.frac:
        return [int(b[0] * W), int(b[1] * H), int(b[2] * W), int(b[3] * H)]
    return [int(v) for v in b]


arr = np.array(im)
if a.grid:
    arr[arr.min(axis=2) > a.thr] = 255
for b in a.blank:
    x0, y0, x1, y1 = px(b)
    arr[y0:y1, x0:x1] = 255
Image.fromarray(arr).crop(tuple(px(a.box))).save(a.out)
print("saved", a.out)
