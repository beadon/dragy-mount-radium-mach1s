#!/usr/bin/env python3
"""Dragy GPS laptimer holder for the Radium Mach One S front swingarm, plus a USB-C dust cap.

v2 (2026-11-16): the holder sits in the recessed pad on top of the front swingarm, beyond the deck's
nose, and screws into the pad's two M4 threaded holes.
(v1 bolted the tray onto the shoe in shoe.py; the shoe remains its own component.)

Parts (not yet printed):

    holder   one piece: a base on the pad, with the plug, and on top of it a tray that holds the
             Dragy flat, logo up, parallel to the pad (30 deg, nose up). Two M4 x 16 socket-head screws go
             down through its floor into the pad's threads (heads under the Dragy, reachable when it's out);
             they and the pocket's walls locate it (an optional plug into the oval hole: PLUG).
             The Dragy slides in from the USB-C end (the rider's right); lips along both long sides and
             the far end keep it from lifting out; the far end's wall has a window for the white connector.
             The floor is thick enough to lift the USB-C port clear of the pocket's rim, so a cable plugs in.
    cap      the USB-C dust cover: it slips over the tray's open end and holds the Dragy in; a gasket ring
             on its inside presses on the Dragy's end face round the USB-C opening (nothing enters the
             socket). A tether strap, printed flat with it, rings over a peg on the holder. Print it in TPU.

Coordinates: the parts are built in the PAD frame, x across the board (rider's right), y along the pad
toward the nose (rising 30 deg), z out of the pad; origin at the oval hole's centre on the pad's surface.
PAD_FRAME places them in the world (x right, y toward the nose, z up).

Usage:  .venv/bin/python dragy_mount.py [outdir]
"""
import sys
from pathlib import Path

import numpy as np
from manifold3d import CrossSection, Manifold

import shoe as s

VERSION = 2

# --- The front swingarm's pad (owner's measurements, 2026-11-16) ---
PAD_TILT = 30.0      # from flat, rising toward the nose (the lip of the oval hole is at its front, higher end)
PAD_W = 66.3         # flat area inside the rim, across the board (66.38 measured)
PAD_L = 35.0 / np.cos(np.radians(PAD_TILT))   # along the slope: 35 measured level -> 40.4
PAD_R = 8.0          # the pocket's corner radius (ESTIMATE from the photo)
RIM_H = 15.55        # the rim stands this far above the pad
M4_SPACING = 39.5    # the two M4 threaded holes, centre to centre, across the board, either side of the oval hole
THREAD = 4.0         # the M4 threads are ~4 mm long, right through the casting
HOLE_W, HOLE_L, HOLE_D = 16.0, 17.0, 9.0   # the oval hole (as on the rear truck), centred between the M4 holes

# --- The Dragy (laptimer.com unit, measured with calipers 2026-11-16) ---
DRAGY_L, DRAGY_W, DRAGY_T = 42.98, 26.96, 13.94
DRAGY_R = 4.0        # plan-view corner radius (ESTIMATE from photos)
USB_W, USB_H, USB_DEPTH = 8.34, 2.56, 6.2   # USB Type-C receptacle opening (spec), on the +x end face, its long
                                            # side along y, at mid-height (z) of the Dragy
# Off centre along y (owner, 2026-11-16): the connector's opening in the case is 6.91 from one side wall and
# 10.21 from the other, so it's 26.96 - 17.12 = 9.84 wide and its centre is 1.65 off the Dragy's centreline,
# toward the 6.91 side. USB_SIDE says which way: +1 toward the nose (+y), -1 toward the tail.
USB_SIDE = -1        # toward the tail (owner, 2026-11-16: logo up, USB-C end to the rider's right)
USB_Y = USB_SIDE * (DRAGY_W / 2 - 6.91 - (DRAGY_W - 6.91 - 10.21) / 2)
TONGUE_W, TONGUE_T = 6.69, 0.70   # the socket's centre tongue (contacts on both faces), from its back wall to
TONGUE_RECESS = 0.3               # this far inside the end face (ESTIMATE: as close to the face as plausible)
USB_PLUG = (13.0, 7.5, 30.0)  # a charging plug's moulding, across x height x length (ESTIMATE, for the clearance check)
WHITE_CONN_WIN = (16.0, 8.0)  # window (y, z) in the far end's wall for the white connector (ESTIMATE)

# --- Holder ---
FIT = 0.25           # clearance per side round the Dragy
WALL = 2.4           # side walls
END_WALL = 3.6       # far-end wall: thicker, as the screw's counterbore runs into it
LIP = 1.2            # top lips over the Dragy's edges (45 deg underneath, so they print without supports)
TOP_CLEAR = 0.3      # gap over the Dragy's top, under the lips
GRIP = 0.3           # small bumps inside the side walls near the open end, so the Dragy stays put while charging
PLUG = False         # a plug into the oval hole: not needed (the screws and the pocket's walls locate the
                     # holder), and it would stop the holder printing floor-down
PLUG_CLR, PLUG_DEPTH = 0.2, 4.0
SCREW_LEN = 16.0     # M4 x 16: the last 4 mm catch the pad's threads and end flush with the casting's underside
BOLT_HOLE, HEAD_BORE, HEAD_H = s.BOLT_HOLE, s.HEAD_BORE, s.HEAD_H

# --- Tether: a TPU strap, printed flat with the cap, from its end plate to a peg on the holder ---
TETHER_W, TETHER_T, TETHER_L = 4.0, 1.0, 32.0   # strap width, thickness, length (to the ring's centre)
RING_OD, RING_ID = 7.5, 3.2                     # the ring at its end; it stretches over the peg's head
PEG_D, PEG_HEAD, PEG_L = 3.0, 4.6, 3.0          # mushroom peg on the holder's -y (tail-side) wall
PEG_X = -6.0                                    # along the holder; the strap wraps round the cap's side to reach it

# --- Cap (USB-C dust cover) ---
CAP_WALL = 1.6
CAP_DEPTH = 7.0      # how far the cap's sleeve reaches over the tray's end
CAP_FIT = 0.2        # clearance per side, sleeve over tray
# A gasket ring on the end plate's inside presses on the Dragy's end face round the USB-C opening; nothing
# goes into the socket (a nub would have to clear the socket's tongue by ~0.15 mm, less than the
# measurements' slop). The case's cut-out round the connector is ~9.84 wide (owner's measurements).
GASKET_IN = (11.0, 5.0)  # inside of the ring (stadium), across y x z: ~0.6 mm round the 9.84 cut-out
GASKET_WALL = 1.2
GASKET_SQUEEZE = 0.4     # how far the ring presses into the Dragy's end face, with the Dragy pushed fully
                         # away (it can slide 2 x FIT in its pocket)
CAP_SNAP = 0.5       # bumps on the tray's sides that click into the cap's side holes

SEAT = SCREW_LEN - THREAD                    # the screws' heads seat this high above the pad
FLOOR_TOP = SEAT + HEAD_H + 0.4              # the Dragy sits on this, over the heads
POCKET_L, POCKET_W = DRAGY_L + 2 * FIT, DRAGY_W + 2 * FIT
POCKET_H = DRAGY_T + TOP_CLEAR
OUT_W = POCKET_W + 2 * WALL
X_OPEN = POCKET_L / 2                        # the open (USB-C) end
X_FAR = -POCKET_L / 2 - END_WALL             # the far end, outside
TOP = FLOOR_TOP + POCKET_H + LIP
BASE_X = M4_SPACING / 2 + HEAD_BORE / 2 + 1.6   # the base (below the Dragy) reaches past both screws' counterbores
SNAP_Z = (FLOOR_TOP + TOP) / 2                    # the cap's snap bumps, on the tray's side walls

T_RAD = np.radians(PAD_TILT)
PAD_FRAME = np.column_stack([[1.0, 0, 0], [0, np.cos(T_RAD), np.sin(T_RAD)], [0, -np.sin(T_RAD), np.cos(T_RAD)]])


def to_world(m):
    return s.place(m, PAD_FRAME)


def rounded_rect(l, w, r):
    return CrossSection.square([l - 2 * r, w - 2 * r]).translate([-(l - 2 * r) / 2, -(w - 2 * r) / 2]).offset(
        r, circular_segments=48)


def hole_section():
    """The oval hole: 16 across (x), 17 along the board (y)."""
    return CrossSection.circle(HOLE_W / 2, 96).scale([1, HOLE_L / HOLE_W])


def _socket(x_end, z_mid, shrink=0.0, depth=USB_DEPTH):
    """USB-C stadium (long side along y), from the end face at x_end running `depth` along -x."""
    st = _stadium(USB_W - 2 * shrink, USB_H - 2 * shrink)
    rot = np.array([[0, 0, -1.0], [1.0, 0, 0], [0, 1.0, 0]])   # section (y, z), extruded along -x
    return s.place(st.extrude(depth), rot, [x_end, USB_Y, z_mid])


def dragy():
    """The Dragy, with its USB-C socket, in place (pad frame)."""
    body = rounded_rect(DRAGY_L, DRAGY_W, DRAGY_R).extrude(DRAGY_T)
    body -= _socket(DRAGY_L / 2, DRAGY_T / 2)
    tongue_l = USB_DEPTH - TONGUE_RECESS
    body += Manifold.cube([tongue_l + 0.5, TONGUE_W, TONGUE_T]).translate(
        [DRAGY_L / 2 - USB_DEPTH - 0.5, USB_Y - TONGUE_W / 2, DRAGY_T / 2 - TONGUE_T / 2])
    return body.translate([0, 0, FLOOR_TOP])


def usb_plug():
    """Room a charging cable's plug needs, straight out of the USB-C port (pad frame)."""
    w, h, l = USB_PLUG
    return Manifold.cube([l, w, h]).translate([DRAGY_L / 2, USB_Y - w / 2, FLOOR_TOP + DRAGY_T / 2 - h / 2])


def screws():
    m = Manifold()
    for sx in (1, -1):
        m += (s.rod(SCREW_LEN, 4.0, SEAT - SCREW_LEN) + s.rod(HEAD_H, 7.0, SEAT)).translate([sx * M4_SPACING / 2, 0, 0])
    return m


def holder(grip=True):
    w2 = OUT_W / 2
    outer = Manifold.cube([X_OPEN - X_FAR, OUT_W, TOP]).translate([X_FAR, -w2, 0])
    outer += Manifold.cube([2 * BASE_X, OUT_W, FLOOR_TOP]).translate([-BASE_X, -w2, 0])   # base under both screws
    pocket = rounded_rect(POCKET_L, POCKET_W, DRAGY_R + FIT).extrude(POCKET_H).translate([0, 0, FLOOR_TOP])
    # Lips: the opening above the Dragy is the pocket less LIP at the sides and the far end; open at +x.
    # Underneath, each lip slopes at 45 deg (a hull from the pocket's outline at its top to the opening).
    open_l = POCKET_L - LIP + 20
    opening = Manifold.cube([open_l, POCKET_W - 2 * LIP, 30]).translate([-POCKET_L / 2 + LIP, -(POCKET_W - 2 * LIP) / 2, FLOOR_TOP])
    slope = Manifold.hull(rounded_rect(POCKET_L, POCKET_W, DRAGY_R + FIT).extrude(0.01).translate([0, 0, FLOOR_TOP + POCKET_H])
                          + Manifold.cube([open_l, POCKET_W - 2 * LIP, 0.01]).translate(
                              [-POCKET_L / 2 + LIP, -(POCKET_W - 2 * LIP) / 2, FLOOR_TOP + POCKET_H + LIP]))
    mouth = Manifold.cube([WALL + 2, POCKET_W, POCKET_H + LIP + 1]).translate([X_OPEN - 1, -POCKET_W / 2, FLOOR_TOP])
    h = outer - pocket - opening - slope - mouth
    # Window in the far wall for the white connector.
    wy, wz = WHITE_CONN_WIN
    h -= Manifold.cube([END_WALL + 2, wy, wz]).translate([X_FAR - 1, -wy / 2, FLOOR_TOP + DRAGY_T / 2 - wz / 2])
    # Optional plug into the oval hole.
    if PLUG:
        h += hole_section().offset(-PLUG_CLR, circular_segments=64).extrude(PLUG_DEPTH + 0.5).translate([0, 0, -PLUG_DEPTH])
    # Grip bumps inside the side walls near the open end: GRIP - FIT (0.05 mm) of interference.
    for sy in ((1, -1) if grip else ()):
        bump = Manifold.cylinder(POCKET_H - 1, 1.5, circular_segments=24).scale([1, GRIP / 1.5, 1])
        h += bump.translate([X_OPEN - 4, sy * POCKET_W / 2, FLOOR_TOP + 0.5]) ^ Manifold.cube(
            [10, POCKET_W, 40]).translate([X_OPEN - 9, -POCKET_W / 2, 0])
    # Snap bumps on the outside of both side walls, for the cap (domes, half sunk into the wall).
    for sy in (1, -1):
        h += Manifold.sphere(1.5, circular_segments=24).scale([1, CAP_SNAP / 1.5, 1]).translate(
            [X_OPEN - CAP_DEPTH / 2, sy * w2, SNAP_Z])
    # Peg for the cap's tether, on the tail-side (-y) wall: a shaft and a head with a 45 deg lead-in.
    shaft = Manifold.cylinder(PEG_L + 0.5, PEG_D / 2, circular_segments=24)
    head = Manifold.cylinder((PEG_HEAD - PEG_D) / 2, PEG_D / 2, PEG_HEAD / 2, circular_segments=24)
    head += Manifold.cylinder(0.6, PEG_HEAD / 2, PEG_HEAD / 2, circular_segments=24).translate([0, 0, -0.6])
    peg = shaft + head.mirror([0, 0, 1]).translate([0, 0, PEG_L + 0.5])
    h += peg.rotate([90, 0, 0]).translate([PEG_X, -w2 + 0.5, SNAP_Z])
    # The two M4 screws: clearance holes down to the pad, counterbores up from the head's seat.
    for sx in (1, -1):
        h -= s.rod(SEAT + 2, BOLT_HOLE, -1).translate([sx * M4_SPACING / 2, 0, 0])
        h -= s.rod(TOP, HEAD_BORE, SEAT).translate([sx * M4_SPACING / 2, 0, 0])
    return h


def _stadium(w, t):
    """A stadium (a rectangle with round ends), w long and t tall, centred, in a 2D (y, z) section."""
    core = 1e-3                                  # a near-flat bar; rounding it by t/2 gives the stadium
    return CrossSection.square([w - t, core]).translate([-(w - t) / 2, -core / 2]).offset((t - core) / 2, circular_segments=32)


def gasket(squeeze=GASKET_SQUEEZE):
    """The ring on the end plate's inside face, round the USB-C opening (pad frame)."""
    h = 2 * FIT + squeeze                        # from the plate to the Dragy's end face, pushed fully away, plus squeeze
    wi, hi = GASKET_IN
    ring = _stadium(wi + 2 * GASKET_WALL, hi + 2 * GASKET_WALL) - _stadium(wi, hi)
    rot = np.array([[0, 0, -1.0], [1.0, 0, 0], [0, 1.0, 0]])   # section (y, z), extruded along -x
    return s.place(ring.extrude(h + 0.01), rot, [X_OPEN + 0.01, USB_Y, FLOOR_TOP + DRAGY_T / 2])


def cap(squeeze=GASKET_SQUEEZE):
    """Sleeve (top and sides) over the tray's open end, closed by an end plate with the gasket ring, plus the tether (pad frame).
    It has no bottom: it sits on the base's shelf beyond the tray's open end."""
    w2 = OUT_W / 2 + CAP_FIT
    z0, z1 = FLOOR_TOP + CAP_FIT, TOP + CAP_FIT + CAP_WALL
    outer = Manifold.cube([CAP_DEPTH + CAP_WALL, 2 * (w2 + CAP_WALL), z1 - z0]).translate([X_OPEN - CAP_DEPTH, -w2 - CAP_WALL, z0])
    inner = Manifold.cube([CAP_DEPTH + 1, 2 * w2, z1 - CAP_WALL + 1]).translate([X_OPEN - CAP_DEPTH - 1, -w2, -1])
    c = outer - inner
    for sy in (1, -1):   # holes through the side walls for the tray's snap bumps
        c -= Manifold.cylinder(2 * CAP_WALL + 2, 1.5 + 0.15, circular_segments=24).rotate([90, 0, 0]).translate(
            [X_OPEN - CAP_DEPTH / 2, sy * (w2 + CAP_WALL / 2) + (CAP_WALL + 1), SNAP_Z])
    c += gasket(squeeze)
    # Tether: a strap from the end plate's tail-side edge, flush with its outer face (flat on the bed as
    # printed), ending in a ring. On the board it bends round the cap's side to the holder's peg.
    y0 = -(w2 + CAP_WALL)
    xs = X_OPEN + CAP_WALL - TETHER_T
    c += Manifold.cube([TETHER_T, TETHER_L + 0.5, TETHER_W]).translate([xs, y0 - TETHER_L, SNAP_Z - TETHER_W / 2])
    ring = (Manifold.cylinder(TETHER_T, RING_OD / 2, circular_segments=48)
            - Manifold.cylinder(TETHER_T + 2, RING_ID / 2, circular_segments=32).translate([0, 0, -1]))
    c += ring.rotate([0, 90, 0]).translate([xs, y0 - TETHER_L, SNAP_Z])
    return c


def casting():
    """The swingarm round the pad (pad frame): the pocket (rim RIM_H high), the oval hole, the M4 holes.
    Only the pocket and the holes are measured; the block round them is a placeholder."""
    block = Manifold.cube([PAD_W + 30, PAD_L + 30, RIM_H + 12]).translate([-(PAD_W + 30) / 2, -(PAD_L + 30) / 2, -12])
    pocket = rounded_rect(PAD_W, PAD_L, PAD_R).extrude(RIM_H + 1)
    hole = hole_section().extrude(HOLE_D + 1).translate([0, 0, -HOLE_D])
    threads = Manifold()
    for sx in (1, -1):
        threads += s.rod(THREAD + 1, 3.3, -THREAD).translate([sx * M4_SPACING / 2, 0, 0])
    return block - pocket - hole - threads


def main():
    out = Path(sys.argv[1] if len(sys.argv) > 1 else "out")
    out.mkdir(parents=True, exist_ok=True)
    h, c, d, cast, sc = holder(), cap(), dragy(), casting(), screws()
    for name, m in (("holder", h), ("cap", c)):
        assert len(m.decompose()) == 1, f"{name} is not one piece"
        zero, bad = s.check_mesh(m, name)
        assert zero == bad == 0
    checks = {
        "holder inside the pad's pocket": (h ^ cast).volume() < 0.01,
        "cap inside the pad's pocket": (c ^ cast).volume() < 0.01,
        "Dragy fits the holder (apart from the grip bumps)": (d ^ holder(grip=False)).volume() < 0.01,
        "screws clear of holder and Dragy (heads seated)": all((sc ^ m).volume() < 0.01 for m in (h, d)),
        "screws end flush with the casting's underside": abs(SEAT - SCREW_LEN + THREAD) < 1e-9,
        "cap clear of the holder": (c ^ h).volume() < 0.01,
        "cap clear of the screws": (c ^ sc).volume() < 0.01,
        "the tether's ring fits round the peg's shaft": RING_ID > PEG_D and RING_ID < PEG_HEAD,
        "each screw head fully seated on plastic": all(((s.rod(0.5, 7.0, SEAT - 0.5) - s.rod(0.5, BOLT_HOLE + 0.1, SEAT - 0.5))
                                                        .translate([sx * M4_SPACING / 2, 0, 0]) - h).volume() < 0.01 for sx in (1, -1)),
        # The ring pushes the Dragy back against the far wall; there it presses GASKET_SQUEEZE into its end face.
        "gasket just touches the Dragy (pushed back) before its squeeze": (cap(squeeze=0) ^ d.translate([-FIT, 0, 0])).volume() < 0.01,
        "gasket's opening holds the USB-C opening with 0.5 mm to spare all round": (
            _stadium(USB_W, USB_H).offset(0.5, circular_segments=32) - _stadium(*GASKET_IN)).area() < 1e-6,
        "a charging plug clears the pocket's rim": (usb_plug() ^ cast).is_empty(),
    }
    for k, v in checks.items():
        print(f"  {k}: {v}")
    assert all(checks.values())
    print(f"holder {h.volume() / 1000:.1f} cm^3, cap {c.volume() / 1000:.1f} cm^3; the Dragy's top is "
          f"{FLOOR_TOP + DRAGY_T - RIM_H:.1f} mm above the rim; USB-C port centre {FLOOR_TOP + DRAGY_T / 2 - RIM_H:.1f} mm above it")
    s.write_stl(s.face_down(h, [0, 0, -1.0]), out / f"dragy_holder_v{VERSION}.stl")   # floor down: no supports
    s.write_stl(s.face_down(c, [1.0, 0, 0]), out / f"dragy_usbc_cap_v{VERSION}.stl")  # end plate down, gasket up, tether flat
    colours = {"truck": (0.55, 0.55, 0.58), "tray": (0.80, 0.15, 0.12), "cap": (0.95, 0.65, 0.10),
               "dragy": (0.25, 0.45, 0.85), "steel": (0.2, 0.2, 0.2)}
    scene = {"front_swingarm_pad_schematic": (to_world(cast), "truck"), "dragy_holder": (to_world(h), "tray"),
             "usbc_cap": (to_world(c), "cap"), "dragy": (to_world(d), "dragy"), "screws": (to_world(sc), "steel")}
    s.write_obj(scene, out / f"dragy_assembly_v{VERSION}.obj", colours)


if __name__ == "__main__":
    main()
