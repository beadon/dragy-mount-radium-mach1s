#!/usr/bin/env python3
"""Dragy GPS laptimer holder for the Radium Mach One S, on the shoe (shoe.py), plus a USB-C cap.

Parts (first cut, not yet printed):

    tray       holds the Dragy flat, logo up (GPS needs open sky above it). It bolts onto the
               shoe's flat top with the shoe's two M4 bolts. The Dragy slides in from the USB-C
               end (+x, the rider's right); top lips along both long sides and the far end keep it
               from lifting out. The far end's wall has a window for the Dragy's white connector.
    cap        the USB-C dust cover. It slips over the tray's open end, plugs the USB-C socket
               with a nub, and holds the Dragy in. Print it in TPU; in PLA, set CAP_NUB = 0.

World frame and origin as in shoe.py (centre of hole A; y toward the nose, z up).

Usage:  .venv/bin/python dragy_mount.py [outdir]
"""
import sys
from pathlib import Path

import numpy as np
from manifold3d import CrossSection, Manifold

import shoe as s

VERSION = 1

# --- The Dragy (laptimer.com unit, measured with calipers 2026-11-16) ---
DRAGY_L, DRAGY_W, DRAGY_T = 42.98, 26.96, 13.94
DRAGY_R = 4.0        # plan-view corner radius (ESTIMATE from photos)
USB_W, USB_H, USB_DEPTH = 8.34, 2.56, 6.2   # USB Type-C receptacle opening (spec), centred on the +x end face
                                            # with its long side along y (ESTIMATE: centred, from photos)
WHITE_CONN_WIN = (16.0, 8.0)  # window (y, z) in the far end's wall for the white connector (ESTIMATE)

# --- Tray ---
FIT = 0.25           # clearance per side round the Dragy
WALL = 2.4
LIP = 1.2            # top lips over the Dragy's edges (45 deg underneath, so they print without supports)
TOP_CLEAR = 0.3      # gap over the Dragy's top, under the lips
TRAY_Y = -4.25       # tray centre (y): over the shoe, and clear of the hex key's path to the angled screw
BOLT_LEN = 16.0      # the shoe's two bolts: M4 x 16 (an M4 x 10 would let the floor be 6 mm thinner)
GRIP = 0.3           # small bumps inside the side walls near the open end, so the Dragy stays put while charging

# --- Cap (USB-C dust cover) ---
CAP_WALL = 1.6
CAP_DEPTH = 7.0      # how far the cap's sleeve reaches over the tray's end
CAP_FIT = 0.2        # clearance per side, sleeve over tray
CAP_NUB = 4.0        # nub into the USB-C socket (0 for a PLA cap: rigid plastic doesn't seal or flex)
NUB_FIT = 0.12       # nub smaller than the socket opening, per side
CAP_SNAP = 0.5       # bumps on the tray's sides that click into the cap's side holes

FLOOR_TOP = s.head_seat(BOLT_LEN) + s.HEAD_H + 0.4      # the Dragy sits on this, over the bolt heads
POCKET_L, POCKET_W = DRAGY_L + 2 * FIT, DRAGY_W + 2 * FIT
POCKET_H = DRAGY_T + TOP_CLEAR
OUT_W = POCKET_W + 2 * WALL
X_OPEN = POCKET_L / 2                                   # the open (USB-C) end of the tray
X_FAR = -POCKET_L / 2 - WALL                            # the far end, outside
TOP = FLOOR_TOP + POCKET_H + LIP


def rounded_rect(l, w, r):
    return CrossSection.square([l - 2 * r, w - 2 * r]).translate([-(l - 2 * r) / 2, -(w - 2 * r) / 2]).offset(
        r, circular_segments=48)


def dragy():
    """The Dragy, with its USB-C socket, in place in the tray (world coordinates)."""
    body = rounded_rect(DRAGY_L, DRAGY_W, DRAGY_R).extrude(DRAGY_T)
    body -= _socket(DRAGY_L / 2, DRAGY_T / 2)
    return body.translate([0, TRAY_Y, FLOOR_TOP])


def _socket(x_end, z_mid, shrink=0.0, depth=USB_DEPTH):
    """USB-C stadium (long side along y), from the end face at x_end running depth along -x."""
    w, h = USB_W - 2 * shrink, USB_H - 2 * shrink
    st = CrossSection.square([w - h, h]).translate([-(w - h) / 2, -h / 2]).offset(h / 2 - 1e-3, circular_segments=24)
    # st is in (u, v) = (y, z); extrude along local z, then turn local z to -x
    m = st.extrude(depth)                       # local: x=y_world, y=z_world, z=-x_world
    rot = np.array([[0, 0, -1.0], [1.0, 0, 0], [0, 1.0, 0]])   # columns: local x->world y, local y->world z, local z->world -x
    return s.place(m, rot, [x_end, 0, z_mid])


def tray(grip=True):
    w2 = OUT_W / 2
    outer = Manifold.cube([X_OPEN - X_FAR, OUT_W, TOP - s.TOP_Z]).translate([X_FAR, -w2, s.TOP_Z])
    pocket = rounded_rect(POCKET_L, POCKET_W, DRAGY_R + FIT).extrude(POCKET_H).translate([0, 0, FLOOR_TOP])
    # Lips: the opening above the Dragy is the pocket less LIP at the sides and the far end; open at +x.
    # Underneath, each lip slopes at 45 deg (a hull from the pocket's outline at its top to the opening).
    open_l = POCKET_L - LIP + 20
    opening = Manifold.cube([open_l, POCKET_W - 2 * LIP, 30]).translate([-POCKET_L / 2 + LIP, -(POCKET_W - 2 * LIP) / 2, FLOOR_TOP])
    slope = Manifold.hull(rounded_rect(POCKET_L, POCKET_W, DRAGY_R + FIT).extrude(0.01).translate([0, 0, FLOOR_TOP + POCKET_H])
                          + Manifold.cube([open_l, POCKET_W - 2 * LIP, 0.01]).translate(
                              [-POCKET_L / 2 + LIP, -(POCKET_W - 2 * LIP) / 2, FLOOR_TOP + POCKET_H + LIP]))
    # The open end: the pocket runs out through the +x wall.
    mouth = Manifold.cube([WALL + 2, POCKET_W, POCKET_H + LIP + 1]).translate([X_OPEN - 1, -POCKET_W / 2, FLOOR_TOP])
    t = (outer - pocket - opening - slope - mouth).translate([0, TRAY_Y, 0])
    # Window in the far wall for the white connector.
    wy, wz = WHITE_CONN_WIN
    t -= Manifold.cube([WALL + 2, wy, wz]).translate([X_FAR - 1, TRAY_Y - wy / 2, FLOOR_TOP + DRAGY_T / 2 - wz / 2])
    # Grip bumps inside the side walls near the open end (half-cylinders along z): GRIP - FIT
    # (0.05 mm) of interference holds the Dragy while the cap is off.
    for sy in ((1, -1) if grip else ()):
        bump = Manifold.cylinder(POCKET_H - 1, 1.5, circular_segments=24).scale([1, GRIP / 1.5, 1])
        t += bump.translate([X_OPEN - 4, TRAY_Y + sy * POCKET_W / 2, FLOOR_TOP + 0.5]) ^ Manifold.cube(
            [10, POCKET_W, 40]).translate([X_OPEN - 9, TRAY_Y - POCKET_W / 2, 0])
    # Snap bumps on the outside of both side walls, for the cap (domes, half sunk into the wall).
    for sy in (1, -1):
        dome = Manifold.sphere(1.5, circular_segments=24).scale([1, CAP_SNAP / 1.5, 1])
        t += dome.translate([X_OPEN - CAP_DEPTH / 2, TRAY_Y + sy * w2, (s.TOP_Z + TOP) / 2])
    # Counterbores and holes for the shoe's two bolts (heads under the Dragy).
    seat = s.head_seat(BOLT_LEN)
    for sx in (1, -1):
        t -= s.rod(60, s.BOLT_HOLE, s.TOP_Z - 1).translate([sx * s.BOLT_X, s.BOLT_Y, 0])
        t -= s.rod(FLOOR_TOP - seat + 1, s.HEAD_BORE, seat).translate([sx * s.BOLT_X, s.BOLT_Y, 0])
    return t


def cap():
    """Sleeve over the tray's open end, closed by an end plate with the USB-C nub (world coordinates)."""
    w2 = OUT_W / 2 + CAP_FIT
    z0, z1 = s.TOP_Z - CAP_FIT - CAP_WALL, TOP + CAP_FIT + CAP_WALL
    outer = Manifold.cube([CAP_DEPTH + CAP_WALL, 2 * (w2 + CAP_WALL), z1 - z0]).translate([X_OPEN - CAP_DEPTH, -w2 - CAP_WALL, z0])
    inner = Manifold.cube([CAP_DEPTH + 1, 2 * w2, z1 - z0 - 2 * CAP_WALL]).translate([X_OPEN - CAP_DEPTH - 1, -w2, z0 + CAP_WALL])
    c = (outer - inner).translate([0, TRAY_Y, 0])
    # Holes through the side walls for the tray's snap bumps.
    for sy in (1, -1):
        c -= Manifold.cylinder(2 * CAP_WALL + 2, 1.5 + 0.15, circular_segments=24).rotate([90, 0, 0]).translate(
            [X_OPEN - CAP_DEPTH / 2, TRAY_Y + sy * (w2 + CAP_WALL / 2) + (CAP_WALL + 1), (s.TOP_Z + TOP) / 2])
    # The nub: from the end plate's inside face back into the socket.
    z_mid = FLOOR_TOP + DRAGY_T / 2
    if CAP_NUB > 0:
        reach = FIT + CAP_NUB                    # the gap to the Dragy's end face, then into the socket
        c += _socket(X_OPEN + 0.01, 0, shrink=NUB_FIT, depth=reach + 0.01).translate([0, TRAY_Y, z_mid])
    return c


def main():
    out = Path(sys.argv[1] if len(sys.argv) > 1 else "out")
    out.mkdir(parents=True, exist_ok=True)
    sh, cut, screw = s.shoe()
    s.check_shoe(sh, cut, screw)
    t, c, d = tray(), cap(), dragy()
    bolts = s.bolt_solids(BOLT_LEN)
    key = s.at_hole(s.along(s.rod(60, 4.0, s.SCREW_LEN + s.HEAD_H), screw["tip"], screw["d"]))  # hex key's path
    for name, m in (("tray", t), ("cap", c)):
        assert len(m.decompose()) == 1, f"{name} is not one piece"
        zero, bad = s.check_mesh(m, name)
        assert zero == bad == 0
    checks = {
        "tray clear of the shoe": (t ^ sh).volume() < 0.01,
        "tray clear of the hex key's path to the angled screw": (t ^ key).is_empty(),
        "Dragy fits the tray (apart from the grip bumps)": (d ^ tray(grip=False)).volume() < 0.01,
        "bolts clear of tray, shoe and Dragy (heads seated)": all((bolts ^ m).volume() < 0.01 for m in (t, sh, d)),
        "cap clear of the tray": (c ^ t).volume() < 0.01,
        "cap clear of the Dragy (nub inside the socket)": (c ^ d).volume() < 0.01,
    }
    for k, v in checks.items():
        print(f"  {k}: {v}")
    assert all(checks.values())
    print(f"tray {t.volume() / 1000:.1f} cm^3, cap {c.volume() / 1000:.1f} cm^3; the Dragy's top is "
          f"{FLOOR_TOP + DRAGY_T:.1f} mm above hole A")
    s.write_stl(s.face_down(sh, [0, 0, 1.0]), out / "shoe.stl")                      # top face down, plug up
    s.write_stl(s.face_down(t, [0, 0, -1.0]), out / f"dragy_tray_v{VERSION}.stl")     # floor down
    s.write_stl(s.face_down(c, [1.0, 0, 0]), out / f"dragy_usbc_cap_v{VERSION}.stl")  # end plate down, nub up
    housing, port = s.surroundings()
    colours = {"truck": (0.55, 0.55, 0.58), "shoe": (0.15, 0.60, 0.35), "tray": (0.80, 0.15, 0.12),
               "cap": (0.95, 0.65, 0.10), "dragy": (0.25, 0.45, 0.85), "steel": (0.2, 0.2, 0.2)}
    scene = {"hole_A_surroundings_rear_truck": (housing, "truck"), "shoe": (sh, "shoe"), "dragy_tray": (t, "tray"),
             "usbc_cap": (c, "cap"), "dragy": (d, "dragy"), "screws": (s.screw_solid(screw) + bolts, "steel")}
    s.write_obj(scene, out / f"dragy_assembly_v{VERSION}.obj", colours)


if __name__ == "__main__":
    main()
