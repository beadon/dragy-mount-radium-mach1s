#!/usr/bin/env python3
"""Shaded renders of the Dragy mount for checking by eye (numpy + Pillow z-buffer; no 3D viewer).

Usage:  .venv/bin/python render.py [docs/render.png]
"""
import sys

import numpy as np
from PIL import Image, ImageDraw

import dragy_mount as g


def tris(m):
    mesh = m.to_mesh()
    return np.asarray(mesh.vert_properties)[:, :3][np.asarray(mesh.tri_verts)]


def view_matrix(az, el):
    """az 0 looks from the tail, 90 from the rider's right; el > 0 from above."""
    az, el = np.radians(az), np.radians(el)
    d = np.array([np.cos(el) * np.sin(az), -np.cos(el) * np.cos(az), np.sin(el)])
    right = np.cross([0, 0, 1], d)
    right /= np.linalg.norm(right)
    return np.array([right, np.cross(d, right), d])


def render(objs, az, el, title, W=700, H=560):
    R = view_matrix(az, el)
    P = np.vstack([tris(m).reshape(-1, 3) for m, _ in objs]) @ R.T
    centre = (P.min(0) + P.max(0)) / 2
    scale = 0.85 * min(W / np.ptp(P[:, 0]), H / np.ptp(P[:, 1]))
    zbuf = np.full((H, W), -1e9)
    img = np.full((H, W, 3), 245.0)
    light = np.array([0.3, 0.5, 0.8]) / np.linalg.norm([0.3, 0.5, 0.8])
    for m, col in objs:
        T = tris(m) @ R.T
        n = np.cross(T[:, 1] - T[:, 0], T[:, 2] - T[:, 0])
        n /= np.linalg.norm(n, axis=1, keepdims=True) + 1e-12
        shade = 0.35 + 0.65 * np.abs(n @ light)
        S = np.empty_like(T)
        S[..., 0] = (T[..., 0] - centre[0]) * scale + W / 2
        S[..., 1] = H / 2 - (T[..., 1] - centre[1]) * scale
        S[..., 2] = T[..., 2]
        for k, (a, b, c) in enumerate(S):
            x0, x1 = int(max(0, min(a[0], b[0], c[0]))), int(min(W - 1, np.ceil(max(a[0], b[0], c[0]))))
            y0, y1 = int(max(0, min(a[1], b[1], c[1]))), int(min(H - 1, np.ceil(max(a[1], b[1], c[1]))))
            den = (b[1] - c[1]) * (a[0] - c[0]) + (c[0] - b[0]) * (a[1] - c[1])
            if x1 < x0 or y1 < y0 or abs(den) < 1e-9:
                continue
            xs, ys = np.meshgrid(np.arange(x0, x1 + 1) + 0.5, np.arange(y0, y1 + 1) + 0.5)
            l1 = ((b[1] - c[1]) * (xs - c[0]) + (c[0] - b[0]) * (ys - c[1])) / den
            l2 = ((c[1] - a[1]) * (xs - c[0]) + (a[0] - c[0]) * (ys - c[1])) / den
            inside = (l1 >= -1e-6) & (l2 >= -1e-6) & (1 - l1 - l2 >= -1e-6)
            z = l1 * a[2] + l2 * b[2] + (1 - l1 - l2) * c[2]
            zb = zbuf[y0:y1 + 1, x0:x1 + 1]
            upd = inside & (z > zb)
            zb[upd] = z[upd]
            img[y0:y1 + 1, x0:x1 + 1][upd] = np.array(col) * shade[k]
    im = Image.fromarray(img.astype(np.uint8))
    ImageDraw.Draw(im).text((10, 8), title, fill=(0, 0, 0))
    return im


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "docs/render.png"
    w = g.to_world
    cast, h, gt, d, sc = w(g.casting()), w(g.holder()), w(g.gate()), w(g.dragy().translate([-g.FIT, 0, 0])), w(g.screws())
    grey, red, amber, blue, dark = (170, 170, 175), (205, 50, 40), (240, 170, 30), (60, 110, 210), (40, 40, 40)
    up = g.PAD_FRAME[:, 2]                           # out of the pad, for the exploded view
    lift = lambda m, k: m.translate(list(k * up))
    ims = [render([(cast, grey), (h, red), (gt, amber), (d, blue)], -40, 35,
                  f"v{g.VERSION} in the front swingarm's pad (schematic casting): holder red, Dragy blue, gate amber"),
           render([(cast, grey), (lift(sc, 25), dark), (lift(h, 25), red), (lift(d, 55), blue), (lift(gt, 75), amber)],
                  -40, 30, "exploded: two M4x16 into the pad's threads; the Dragy slides in from the right; the gate drops in"),
           render([(cast, grey), (h, red), (gt, amber), (d, blue)], 90, 10, "from the rider's right (nose to the right): pad and holder at 30 deg"),
           render([(h, red), (lift(gt, 22), amber), (d, blue)], 120, 30, "the USB-C end: the gate lifted out of its grooves (pads on its inside)")]
    W, H = ims[0].size
    sheet = Image.new("RGB", (2 * W, 2 * H), "white")
    for i, im in enumerate(ims):
        sheet.paste(im, ((i % 2) * W, (i // 2) * H))
    sheet.save(path)

if __name__ == "__main__":
    main()
