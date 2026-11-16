#!/usr/bin/env python3
"""The "shoe": a printed anchor that locks into the oval hole ("hole A") on a Radium Mach One S.

It's a separate component on purpose: anything (the Dragy tray in dragy_mount.py, a display, a
light) bolts onto its flat top with two M4 bolts into captive nuts. See INTERFACE below.

Geometry is the rear-mount shoe from github.com/beadon/shredlight-mounts (rear_mount.py, r4),
which was printed and fitted in the rear truck's hole A on 2026-11-16 ("fits beautifully").
The front swingarm has an identical hole (user, 2026-11-16), but its surroundings and surface
angle are NOT measured yet: see AGENTS.md.

How it holds: the plug fills hole A and drops straight in. An M4 x 16 socket-head screw goes in
from the nose side, 30 deg below level, through a captive M4 hex nut and out of the plug's rear
face, under the ~2 mm lip at the hole's rear end. The steel shank holds the shoe down, and its end
presses on the back of the space under the lip, pulling the plug tight against the hole's front
wall. Tightened, its head sits just inside its counterbore.

World frame: x to the rider's right, y toward the nose, z up (sky). Origin: centre of hole A, on
the surface around it. That surface faces the nose, tipped 30 deg up from flat (rear truck).

Usage:  .venv/bin/python shoe.py [outdir]     writes shoe.stl (top face down, plug up, no supports)
"""
import sys
from pathlib import Path

import numpy as np
from manifold3d import CrossSection, Manifold

# --- Hole A (measured on the rear truck, 2026-11-15) ---
SURFACE_TILT = 30.0  # surface round the hole: tipped 30 deg from flat, facing the nose (inclinometer)
HOLE_W = 16.0        # across the board
HOLE_L = 17.0        # along the surface, nose to tail
HOLE_D = 9.0         # deep, square to the surface; solid floor
LIP_T = 2.0          # the plate forming the lip at the hole's rear end is ~2 mm thick
LIP_OVER = 2.0       # how far the space under the lip reaches past the lip's edge
# Only the rear end has a lip; the sides and the front are plain walls.

# --- Behind the hole on the rear truck: a step up to the charging port (measured 2026-11-15) ---
STEP_Z = 7.5         # the port's surface is 7.5 mm higher than the hole's surface, measured vertically
PORT_Y = -22.0       # port centre behind the hole's centre, measured level
PORT_PLUG_D = 17.5   # charging plug as fitted; it stands vertically on the port
PORT_CLEAR = 2.0

# --- Plug and shoe ---
CLR = 0.2            # clearance per side, plug to hole
PLUG_DEPTH = HOLE_D - 0.6
SHOE_W = 24.0        # across the board: inside the pocket floor's two hex screws
SHOE_FRONT = 7.5     # nose end (y): clear of the Ra button (r3's 10.5 overhung it by ~3 mm)
SHOE_REAR = -7.0     # tail end below the step's top (the step's face is 7.36 behind the hole's centre)
SHOE_REAR_TOP = -10.0  # above the step's top the shoe reaches further back, short of the charging plug
STEP_GAP = 1.2       # gap over the step's top
TOP_Z = 15.0         # the shoe's flat top (the pad), this high above the hole

# --- Hardware: M4 socket-head cap screws and plain M4 hex nuts (3.11 mm thick, measured) ---
NUT_AF, NUT_T = 7.0 + 0.3, 3.11 + 0.3  # nut pocket: across flats and thickness, with clearance
BOLT_HOLE = 4.5      # clearance hole for M4
HEAD_BORE = 8.5      # counterbore for the M4 head (7 mm) and the hex key
HEAD_H = 4.0         # M4 socket head height

# Angled screw under the lip
SCREW_ANGLE = 60.0   # axis from the surface; in the world it rises 30 deg toward the nose
SCREW_LEN = 16.0     # M4 x 16
SCREW_RETRACT = 5.0  # backed off this far, its end is inside the plug, so the plug drops straight in
SCREW_NUT_AT = 11.5  # nut centre, along the screw from its end

# INTERFACE: what bolts onto the shoe. An accessory sits flat on the pad (z = TOP_Z) and is held
# by two M4 socket-head bolts going down at (+-BOLT_X, BOLT_Y) into plain M4 hex nuts in the shoe
# (centre height NUT_Z; they slide in from the shoe's sides). A bolt of length L ends flush with
# its nut's underside when its head seats at z = head_seat(L): the accessory must give the head a
# counterbore whose floor is at that height.
BOLT_X, BOLT_Y = 7.0, -5.0
NUT_Z = 11.8


def head_seat(length):
    return NUT_Z - NUT_T / 2 + length


T_RAD = np.radians(SURFACE_TILT)
N = np.array([0.0, np.sin(T_RAD), np.cos(T_RAD)])    # out of the surface (up, toward the nose)
A = np.array([0.0, -np.cos(T_RAD), np.sin(T_RAD)])   # along the surface, toward the tail (and up)
HOLE_FRAME = np.column_stack([[-1.0, 0, 0], A, N])   # local (X, s, h) -> world; right-handed


# ---------------------------------------------------------------- helpers (also used by accessories)

def place(part, rot, offset=(0, 0, 0)):
    return part.transform(np.column_stack([rot, offset]))


def at_hole(m):
    return place(m, HOLE_FRAME)


def along(m, tip, d, t0=0.0):
    """A z-axis primitive moved so it starts t0 along the axis from `tip` and runs along d."""
    z = np.array([0, 0, 1.0])
    k = np.cross(z, d)
    s, c = np.linalg.norm(k), z @ d
    K = np.array([[0, -k[2], k[1]], [k[2], 0, -k[0]], [-k[1], k[0], 0]])
    r = np.eye(3) + K + K @ K * ((1 - c) / s ** 2) if s > 1e-9 else np.eye(3)
    return place(m, r, np.asarray(tip) + t0 * np.asarray(d))


def rod(length, d, start=0.0, seg=24):
    return Manifold.cylinder(length, d / 2, circular_segments=seg).translate([0, 0, start])


def nut_pocket(slot=30.0):
    """Hex nut pocket, axis z, centred; corners point along +x, and a slot of the nut's width runs
    out along +x so the nut slides in from that side."""
    hexa = CrossSection.circle(NUT_AF / np.sqrt(3), 6)
    return (hexa + hexa.translate([slot, 0])).hull().extrude(NUT_T).translate([0, 0, -NUT_T / 2])


def face_down(m, normal):
    """Rotate so `normal` points at the bed, then sit the part on z = 0."""
    n = np.asarray(normal, float) / np.linalg.norm(normal)
    target = np.array([0, 0, -1.0])
    c = n @ target
    if c < -0.999999:
        r = np.diag([1.0, -1, -1])
    else:
        k = np.cross(n, target)
        K = np.array([[0, -k[2], k[1]], [k[2], 0, -k[0]], [-k[1], k[0], 0]])
        r = np.eye(3) + K + K @ K / (1 + c)
    m = place(m, r)
    lo = np.array(m.bounding_box())[:3]
    return m.translate([-lo[0], -lo[1], -lo[2]])


def write_stl(m, path):
    mesh = m.to_mesh()
    v = np.asarray(mesh.vert_properties)[:, :3].astype(np.float32)
    f = np.asarray(mesh.tri_verts)
    tri = v[f]
    n = np.cross(tri[:, 1] - tri[:, 0], tri[:, 2] - tri[:, 0])
    n /= np.linalg.norm(n, axis=1, keepdims=True) + 1e-12
    rec = np.zeros(len(f), dtype=[("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
    rec["n"], rec["v"] = n, tri
    with open(path, "wb") as fh:
        fh.write(b"dragy-mount-radium-mach1s".ljust(80, b"\0"))
        fh.write(np.uint32(len(f)).tobytes())
        fh.write(rec.tobytes())


def write_obj(objects, path, colours):
    """One OBJ with a named, coloured object per part (plus its .mtl), for Blender.
    OBJ is Y-up by convention (Blender's importer assumes it), so world (x, y, z) is written as (x, z, -y):
    with Blender's default import, sky is up and the nose points along Blender's +y."""
    mtl = path.with_suffix(".mtl")
    with open(mtl, "w") as fh:
        for name, rgb in colours.items():
            fh.write(f"newmtl {name}\nKd {rgb[0]} {rgb[1]} {rgb[2]}\n\n")
    with open(path, "w") as fh:
        fh.write(f"mtllib {mtl.name}\n")
        base = 1
        for name, (m, material) in objects.items():
            mesh = m.to_mesh()
            v = np.asarray(mesh.vert_properties)[:, :3]
            f = np.asarray(mesh.tri_verts) + base
            fh.write(f"o {name}\nusemtl {material}\n")
            fh.writelines(f"v {x:.4f} {z:.4f} {-y:.4f}\n" for x, y, z in v)
            fh.writelines(f"f {a} {b} {c}\n" for a, b, c in f)
            base += len(v)


def check_mesh(m, name):
    """No pinched (non-manifold, once vertices are welded) edges and no zero-area triangles."""
    mesh = m.to_mesh()
    v = np.asarray(mesh.vert_properties)[:, :3].astype(np.float32)
    f = np.asarray(mesh.tri_verts)
    tri = v[f].astype(np.float64)
    zero = int((np.linalg.norm(np.cross(tri[:, 1] - tri[:, 0], tri[:, 2] - tri[:, 0]), axis=1) < 2e-10).sum())
    _, inv = np.unique(v, axis=0, return_inverse=True)
    fw = inv.ravel()[f]
    e = np.sort(np.concatenate([fw[:, [0, 1]], fw[:, [1, 2]], fw[:, [2, 0]]]), axis=1)
    _, count = np.unique(e, axis=0, return_counts=True)
    bad = int((count != 2).sum())
    print(f"  {name}: {len(f)} triangles, {zero} zero-area, {bad} non-manifold/open edges")
    return zero, bad


def min_gap_ok(a, b, gap):
    """True if solids a and b stay at least `gap` apart (checked along the axes and diagonals)."""
    dirs = [np.array(v, float) for v in [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]]
    dirs += [np.array(v) / np.sqrt(2) for v in [(1, 1, 0), (1, -1, 0), (-1, 1, 0), (-1, -1, 0),
                                                 (0, 1, 1), (0, 1, -1), (0, -1, 1), (0, -1, -1)]]
    return all((a.translate(list(gap * v)) ^ b).is_empty() for v in dirs) and (a ^ b).is_empty()


# ---------------------------------------------------------------- the shoe

def hole_section():
    return CrossSection.circle(HOLE_W / 2, 96).scale([1, HOLE_L / HOLE_W])


def plug_and_screw():
    """Plug and the angled screw's cutters (hole, counterbore and key path, nut pocket), in
    hole-local coordinates (X, s, h), and the screw's axis."""
    q = hole_section().offset(-CLR, circular_segments=64)
    plug = q.extrude(PLUG_DEPTH + 1).translate([0, 0, -PLUG_DEPTH])
    a = np.radians(SCREW_ANGLE)
    d = np.array([0.0, -np.cos(a), np.sin(a)])     # out of the hole toward the nose, rising
    edge = HOLE_L / 2                              # the lip's edge (the hole's rear end)
    # The shank's top passes just under the lip's edge; its end (a disc square to the axis)
    # stops 0.1 short of the back of the space under the lip.
    h_edge = -(LIP_T + 0.2 + 2.0 / np.cos(a))
    s_tip = edge + LIP_OVER - 2.0 * np.sin(a) - 0.1
    tip = np.array([0.0, s_tip, h_edge - (s_tip - edge) * np.tan(a)])
    cut = along(rod(SCREW_LEN + 1, BOLT_HOLE, -1), tip, d)
    cut += along(rod(60, HEAD_BORE, SCREW_LEN - 0.5), tip, d)
    cut += along(nut_pocket(), tip, d, SCREW_NUT_AT)
    return plug, cut, {"tip": tip, "d": d, "len": SCREW_LEN, "loose": SCREW_RETRACT}


def bolt_cutters():
    """The interface's bolt holes and nut pockets, in world coordinates (slots run out to each side)."""
    holes, nuts = Manifold(), Manifold()
    for sx in (1, -1):
        holes += rod(40, BOLT_HOLE).translate([sx * BOLT_X, BOLT_Y, NUT_Z - NUT_T / 2 - 0.3])
        nut = nut_pocket()
        nuts += (nut if sx > 0 else nut.mirror([1, 0, 0])).translate([sx * BOLT_X, BOLT_Y, NUT_Z])
    return holes, nuts


def shoe():
    """The shoe in world coordinates, the screw's world-space cutter, and the screw's axis."""
    plug, cut, screw = plug_and_screw()
    above = at_hole(Manifold.cube([200, 200, 100]).translate([-100, -100, 0]))
    w = SHOE_W / 2
    body = Manifold.cube([SHOE_W, SHOE_FRONT - SHOE_REAR, TOP_Z + 40]).translate([-w, SHOE_REAR, -40]) ^ above
    z0 = STEP_Z + STEP_GAP
    body += Manifold.cube([SHOE_W, SHOE_REAR - SHOE_REAR_TOP + 1, TOP_Z - z0]).translate([-w, SHOE_REAR_TOP, z0])
    holes, nuts = bolt_cutters()
    cut_w = at_hole(cut)
    part = body + at_hole(plug) - cut_w - holes - nuts
    return part, cut_w, screw


def screw_solid(screw, travel=0.0):
    """The angled screw (shank and head), `travel` backed off from tight, in world coordinates."""
    m = along(rod(screw["len"], 4.0, 0) + rod(HEAD_H, 7.0, screw["len"]), screw["tip"], screw["d"], travel)
    return at_hole(m)


def bolt_solids(length):
    """The interface's two bolts, tightened, in world coordinates."""
    seat = head_seat(length)
    m = Manifold()
    for sx in (1, -1):
        m += (rod(length, 4.0, seat - length) + rod(HEAD_H, 7.0, seat)).translate([sx * BOLT_X, BOLT_Y, 0])
    return m


def surroundings():
    """Rough model round hole A on the REAR truck: the pocket floor with the hole and the space under
    the lip, the step to the charging port, and the charging plug's column (kept clear)."""
    floor = Manifold.cube([50, 52, 20]).translate([-25, -38, -20])
    hole = hole_section().extrude(HOLE_D + 1).translate([0, 0, -HOLE_D])
    under_lip = hole_section().translate([0, LIP_OVER]).extrude(HOLE_D - LIP_T).translate([0, 0, -HOLE_D])
    floor = at_hole(floor - hole - under_lip)
    rear_edge = (HOLE_L / 2 * A)[1]
    step = Manifold.cube([50, 40, STEP_Z + 20]).translate([-25, rear_edge - 40, -20]) - at_hole(hole + under_lip)
    housing = floor + step + Manifold.cylinder(6, 9, circular_segments=32).translate([0, PORT_Y, STEP_Z])
    port = Manifold.cylinder(200, PORT_PLUG_D / 2 + PORT_CLEAR, circular_segments=48).translate([0, PORT_Y, STEP_Z])
    return housing, port


def check_shoe(part, cut, screw):
    housing, port = surroundings()
    assert len(part.decompose()) == 1, "shoe is not one piece"
    assert (part ^ housing).volume() < 0.01 and (part ^ port).is_empty(), "shoe runs into the truck or the charging plug"
    holes, nuts = bolt_cutters()
    assert min_gap_ok(cut, holes + nuts, 1.0), "less than 1 mm between the screw's pockets and the bolts'"
    set_, loose = screw_solid(screw), screw_solid(screw, screw["loose"])
    assert (set_ ^ housing).is_empty(), "the screw, set, runs into the truck"
    assert all(((part + loose).translate(list(dd * N)) ^ housing).volume() < 0.01 for dd in (0, 2, 5, 10, 20)), \
        "the shoe doesn't drop straight in with the screw backed off"
    assert ((part + set_).translate(list(0.5 * N)) ^ housing).volume() > 0.01, "the shoe can lift with the screw set"
    zero, bad = check_mesh(part, "shoe")
    assert zero == bad == 0


def main():
    out = Path(sys.argv[1] if len(sys.argv) > 1 else "out")
    out.mkdir(parents=True, exist_ok=True)
    part, cut, screw = shoe()
    check_shoe(part, cut, screw)
    print(f"shoe: {part.volume() / 1000:.1f} cm^3; drops in with the screw backed off, can't lift once it's set")
    write_stl(face_down(part, [0, 0, 1.0]), out / "shoe.stl")   # top face down, plug up: no supports


if __name__ == "__main__":
    main()
