#!/usr/bin/env python3
"""Dragy GPS laptimer holder for the Radium Mach One S front swingarm, closed by a sprung gate.

v5 (2026-11-17): v4's TPU cap (it came off too easily, and its tether was hard to hook on) is replaced by a
PLA gate that drops into grooves at the open end and stops the Dragy rattling. v2-v4: the holder sits in the
recessed pad on top of the front swingarm, beyond the deck's nose, and screws into the pad's two M4 threaded holes.
(v1 bolted the tray onto the shoe in shoe.py; the shoe remains its own component.)

Parts (v2-v4 holders test-printed 2026-11-16; v4 fits the pad snugly):

    holder   one piece: a base on the pad, and on top of it a tray that holds the Dragy flat, logo up,
             parallel to the pad (30 deg, nose up). Two M4 x 16 socket-head screws go down through its floor
             into the pad's threads (heads under the Dragy, reachable when it's out); they and the pocket's
             walls locate it (an optional plug into the oval hole: PLUG).
             The Dragy slides in from the USB-C end (the rider's right); lips along both long sides and
             the far end keep it from lifting out; the far end's wall has a push-out hole (pointed top: no supports).
             The floor is thick enough to lift the USB-C port clear of the pocket's rim, so a cable plugs in.
             Past the open end the side walls run on as posts with a vertical groove each, for the gate.
    gate     a thin PLA plate that drops into the grooves and closes the USB-C end. It is the spring: two pads
             on its inside press on the Dragy's end face either side of the USB-C opening, so the plate bows
             between the grooves and holds the Dragy against the far wall. Lift it out to charge.

Coordinates: the parts are built in the PAD frame, x across the board (rider's right), y along the pad
toward the nose (rising 30 deg), z out of the pad; origin at the oval hole's centre on the pad's surface.
PAD_FRAME places them in the world (x right, y toward the nose, z up).

Usage:  .venv/bin/python dragy_mount.py [outdir]
"""
import sys
from pathlib import Path

import numpy as np
from manifold3d import CrossSection, JoinType, Manifold, OpType

import shoe as s

VERSION = 10

# --- The front swingarm's pad (owner's measurements, 2026-11-16) ---
PAD_TILT = 30.0      # from flat, rising toward the nose (the lip of the oval hole is at its front, higher end)
PAD_W = 66.3         # flat area inside the rim, across the board (66.38 measured)
PAD_L = 35.0 / np.cos(np.radians(PAD_TILT))   # along the slope: 35 measured level -> 40.4
PAD_R = 8.0          # the pocket's TAIL-side corner radius (ESTIMATE from the photo)
PAD_R_NOSE = 20.0    # its NOSE end is nearly a semicircle (photo from the tail, 2026-11-16): corners ~20 (ESTIMATE)
HOLES_NOSEWARD = 6.2 # the M4 holes (and the oval hole) sit this far toward the nose of the pocket's centre. ESTIMATE,
                     # fitted to the test prints: v3 (TRAY_Y -1) fits with its holes aligned only up to 4.2 here, and
                     # rested ~2 mm short of aligned. Measure: M4 hole centre to the nose-side and tail-side walls.
RIM_H = 15.55        # the rim stands this far above the pad
M4_SPACING = 39.5    # the two M4 threaded holes, centre to centre, across the board, either side of the oval hole
THREAD = 4.0         # the M4 threads are ~4 mm long, right through the casting
HOLE_W, HOLE_L, HOLE_D = 16.0, 17.0, 9.0   # the oval hole (as on the rear truck), centred between the M4 holes

# --- The Dragy (laptimer.com unit, measured with calipers 2026-11-16) ---
DRAGY_L, DRAGY_W, DRAGY_T = 42.98, 26.96, 13.94
DRAGY_R = 4.0        # plan-view corner radius (ESTIMATE from photos)
DRAGY_EDGE_R = 2.0   # its BOTTOM edges are rounded, 2 mm (calipers); its top edges are sharp
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
# Push-out hole through the far end's wall (y, z): to push the Dragy out toward the open end (it also leaves
# part of the white connector visible). Straight sides, then a 45 deg pointed top, so each layer is held
# by the sides and nothing overhangs.
PUSH_W, PUSH_H = 8.0, 3.4     # width; height of the straight sides (the point adds PUSH_W / 2)
PUSH_Y = 2.0                  # moved toward the NOSE (+y) off centre so it covers less of the white connector,
                              # which is off centre the other way (owner, test print 2026-11-16)

# --- Holder ---
TRAY_Y = -3.6        # the holder's body (and the Dragy and gate) sits this far toward the TAIL of the screws and
                     # the oval hole. v2 (0) hit the pocket's nose end; v3 (-1) fitted but rested with its holes about
                     # half a screw width (~2 mm) tail-ward of the pad's (test prints 2026-11-16). At -3 the body would
                     # sit where v3's rested, against the nose end; -3.6 leaves ~1 mm there (with 1.3 mm walls, NOSE_R 6).
SLOT = 1.0           # the screw holes are slots, this far each way along the board (the 2 mm above is an estimate)
NOSE_R = 6.0         # the holder's two nose-side corners (plan view) are rounded this much, to clear the pocket's
                     # rounder nose-side corners
TAIL_R = 6.0         # the far end's tail-side corner too (v8: the last sharp corner, owner 2026-11-18); the open end's
                     # tail-side corner is the posts' END_R
FIT = 0.25           # clearance per side round the Dragy
WALL = 1.3           # side walls: 3 clean lines at 0.45 mm (was 2.4, then 1.8: stiffer than needed, owner 2026-11-16)
END_WALL = 3.6       # far-end wall: thicker, as the screw's counterbore runs into it
LIP = 1.2            # top lips over the Dragy's edges (45 deg underneath, so they print without supports)
TOP_CLEAR = 0.3      # gap over the Dragy's top, under the lips
# Squeeze ribs: one inside each side wall presses SQUEEZE into the Dragy's side and the thin walls flex, so it's
# clamped up/down and side to side. v4 did this by accident (its rounded corners at the open end were ~1 mm
# too narrow) and held the Dragy tight; v5 straightened them and left ~0.3 mm of play up and down (owner,
# 2026-11-17). They replace v2-v5's grip bumps (0.05 mm).
SQUEEZE = 0.4        # into each side of the Dragy
SQ_X = (12.0, 16.0)  # the rib's flat face along x, on the straight part of the Dragy's side (its corners start at 17.5)
SQ_Z = (6.0, DRAGY_T - 0.5)   # its flat face's height above the floor: the upper part of the wall, which can flex
PLUG = False         # a plug into the oval hole: not needed (the screws and the pocket's walls locate the
                     # holder), and it would stop the holder printing floor-down
PLUG_CLR, PLUG_DEPTH = 0.2, 4.0
SCREW_LEN = 16.0     # M4 x 16: the last 4 mm catch the pad's threads and end flush with the casting's underside
BOLT_HOLE, HEAD_BORE, HEAD_H = s.BOLT_HOLE, s.HEAD_BORE, s.HEAD_H

# --- Gate: a PLA plate that drops into grooves at the open end and closes it (v5, replacing v4's TPU cap) ---
# The plate is the spring: it spans the open end between its two grooves, and two pads on its inside press
# on the Dragy's end face either side of the USB-C opening, so the plate bows between the grooves and holds
# the Dragy against the far wall (no rattle along its length). It lifts straight up out of the grooves.
GATE_T = 1.27        # the plate: 3 lines (v5's 2 lines, 0.86, felt flimsy: owner 2026-11-17); it bends as the spring,
                     # and stiffness goes as GATE_T^3, so PRELOAD is cut to match
GATE_GAP = 0.2       # from the open end to the plate's inside face (the Dragy's face is a further 2 x FIT in)
GATE_CLR = 0.2       # in the grooves, each side
GROOVE_D = 0.9       # the plate's ends reach this far into each side wall, past the pocket's side (v7: back from v6's
                     # 0.45, which let the gate slip out of its grooves: owner 2026-11-18)
END_R = 2.0          # the holder's two outer corners at the open end, in plan
FLARE = 5.0          # the side walls thicken gradually to the posts' width over this length (x), ending just short of
                     # the open end: no step (owner 2026-11-18: v5/v7's posts stood out as a jarring bump). It begins
                     # past the squeeze ribs, so the walls still flex there
# The gate's head (v10, owner 2026-11-18): a cap on top of the plate that covers both posts' tops, hiding the grooves,
# flush with the posts' sides; it reaches HEAD_OVER past the posts' ends, a square-edged lip a fingernail catches
# (it replaces v5-v9's ridge). The gate prints upside down, standing on the head.
HEAD_GAP = 0.3       # the head's underside is this far above the posts' tops (the plate stands on the shelf)
HEAD_T = 1.5         # its thickness
HEAD_OVER = 1.0      # past the posts' ends (+x)
PRELOAD = 0.2        # the pads reach this far into the Dragy's end face with the Dragy against the far wall (v5: 0.4)
PAD_Y = (7.3, -8.3)  # the pads' centres along y (Dragy-centred): clear of the USB-C cut-out, which runs
                     # from -6.57 to 3.27, and of the end face's rounded corners (|y| > 9.48)
PAD_W = 1.6          # each pad's width along y
# Click: a small ridge on the outer face of each of the plate's edges, near the bottom, drops into a notch in
# the groove's outer wall. The pads' spring pushes the plate outward, so it holds the ridge in the notch;
# lifting the gate means pushing the ridge back out against it (owner, 2026-11-17: so it can't vibrate out).
CLICK_H = 0.3        # the ridge's height (the grooves' play is 2 x GATE_CLR = 0.4, so it slides down past the wall)
CLICK_Z = (2.0, 13.4)   # its tips' heights above the shelf: one near the bottom, and (v10) one near the top, so the
                        # plate's edge is held at both ends of the groove, not just at the bottom (owner 2026-11-18)
CLICK_UP = 30.0      # its top face, from the wall (deg): shallow, so a pull lifts it out; 45 deg underneath leads it in
CLICK_CLR = 0.1      # the notch is this much bigger all round
PAD_Z = (3.0, DRAGY_T - 2.0)   # pads' height above the floor (clear of the Dragy's rounded bottom edges)

SEAT = SCREW_LEN - THREAD                    # the screws' heads seat this high above the pad
FLOOR_TOP = SEAT + HEAD_H + 0.4              # the Dragy sits on this, over the heads
POCKET_L, POCKET_W = DRAGY_L + 2 * FIT, DRAGY_W + 2 * FIT
POCKET_H = DRAGY_T + TOP_CLEAR
OUT_W = POCKET_W + 2 * WALL
X_OPEN = POCKET_L / 2                        # the open (USB-C) end
X_FAR = -POCKET_L / 2 - END_WALL             # the far end, outside
TOP = FLOOR_TOP + POCKET_H + LIP
BASE_X = M4_SPACING / 2 + HEAD_BORE / 2 + 1.6   # the base (below the Dragy) reaches past both screws' counterbores
X_GATE = X_OPEN + GATE_GAP                   # the plate's inside face
X_POST = BASE_X                              # the posts run on past the open end to the base's end, round the grooves
GROOVE_LIP = X_POST - (X_GATE + GATE_T + GATE_CLR)   # wall beyond the groove (toward +x) that takes the plate's push
X_FLARE1 = X_OPEN - 0.5                      # the walls reach the posts' full width here, before the grooves
X_FLARE0 = X_FLARE1 - FLARE
POST_W2 = POCKET_W / 2 + GROOVE_D + GATE_CLR + 1.0   # the posts are this wide (each side of the centre): 1.0 behind the groove

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


def rounded_bottom_block(l, w, r_plan, r_edge, h, grow=0.0, steps=8):
    """A block l x w x h (plan corners r_plan) whose bottom edges are rounded at r_edge; grown outward by
    `grow` in plan only (the bottom stays at z = 0). Convex, so it's a hull of thin layers."""
    layers = Manifold()
    for i in range(steps + 1):
        t = np.radians(90 * i / steps)
        inset = r_edge * (1 - np.sin(t)) - grow
        z = r_edge * (1 - np.cos(t))
        layers += rounded_rect(l - 2 * inset, w - 2 * inset, max(r_plan - inset, 0.2)).extrude(0.01).translate([0, 0, z])
    top = rounded_rect(l + 2 * grow, w + 2 * grow, r_plan + grow).extrude(0.01).translate([0, 0, h - 0.01])
    return Manifold.hull(layers + top)


def dragy():
    """The Dragy, with its USB-C socket, in place (pad frame)."""
    body = rounded_bottom_block(DRAGY_L, DRAGY_W, DRAGY_R, DRAGY_EDGE_R, DRAGY_T)
    body -= _socket(DRAGY_L / 2, DRAGY_T / 2)
    tongue_l = USB_DEPTH - TONGUE_RECESS
    body += Manifold.cube([tongue_l + 0.5, TONGUE_W, TONGUE_T]).translate(
        [DRAGY_L / 2 - USB_DEPTH - 0.5, USB_Y - TONGUE_W / 2, DRAGY_T / 2 - TONGUE_T / 2])
    return body.translate([0, TRAY_Y, FLOOR_TOP])


def usb_plug():
    """Room a charging cable's plug needs, straight out of the USB-C port (pad frame)."""
    w, h, l = USB_PLUG
    return Manifold.cube([l, w, h]).translate([DRAGY_L / 2, TRAY_Y + USB_Y - w / 2, FLOOR_TOP + DRAGY_T / 2 - h / 2])


def screws():
    m = Manifold()
    for sx in (1, -1):
        m += (s.rod(SCREW_LEN, 4.0, SEAT - SCREW_LEN) + s.rod(HEAD_H, 7.0, SEAT)).translate([sx * M4_SPACING / 2, 0, 0])
    return m


def squeeze_ribs():
    """The two squeeze ribs (holder's frame, before TRAY_Y): 45 deg ramps at both ends in plan, so the Dragy
    slides past, and a 45 deg underside, so they print without supports."""
    d = FIT + SQUEEZE                                  # out from the wall
    x0, x1 = SQ_X
    z0, z1 = FLOOR_TOP + SQ_Z[0], FLOOR_TOP + SQ_Z[1]
    w = POCKET_W / 2
    plan = [(x0 - d, w + 0.3), (x1 + d, w + 0.3), (x1 + d, w), (x1, w - d), (x0, w - d), (x0 - d, w)]
    pts = [(x, y, z) for x, y in plan for z in (z0, z1)]                               # the rib's face and ramps
    pts += [(x, y, z0 - d) for x, y in ((x0 - d, w), (x1 + d, w), (x0 - d, w + 0.3), (x1 + d, w + 0.3))]   # 45 deg below
    rib = Manifold.hull_points(pts)
    return rib + rib.mirror([0, 1, 0])


def holder(grip=True):
    w2 = OUT_W / 2
    outer = Manifold.cube([X_OPEN - X_FAR, OUT_W, TOP]).translate([X_FAR, -w2, 0])
    outer += Manifold.cube([BASE_X + X_FLARE1, OUT_W, FLOOR_TOP]).translate([-BASE_X, -w2, 0])   # base under both screws (the posts finish its +x end)
    # The pocket's floor corners are rounded like the Dragy's bottom edges, FIT clear of them.
    pocket = rounded_bottom_block(DRAGY_L, DRAGY_W, DRAGY_R, DRAGY_EDGE_R, POCKET_H, grow=FIT).translate([0, 0, FLOOR_TOP])
    # ...and its sides run straight out of the open end: v2-v4's rounded plan corners there narrowed the way
    # out by ~1 mm each side, so the Dragy only got past by bending the walls.
    pocket += pocket.translate([10, 0, 0])
    # Lips: the opening above the Dragy is the pocket less LIP at the sides and the far end; open at +x.
    # Underneath, each lip slopes at 45 deg (a hull from the pocket's outline at its top to the opening).
    open_l = POCKET_L - LIP + 20
    opening = Manifold.cube([open_l, POCKET_W - 2 * LIP, 30]).translate([-POCKET_L / 2 + LIP, -(POCKET_W - 2 * LIP) / 2, FLOOR_TOP])
    slope = Manifold.hull(rounded_rect(POCKET_L, POCKET_W, DRAGY_R + FIT).extrude(0.01).translate([0, 0, FLOOR_TOP + POCKET_H])
                          + Manifold.cube([open_l, POCKET_W - 2 * LIP, 0.01]).translate(
                              [-POCKET_L / 2 + LIP, -(POCKET_W - 2 * LIP) / 2, FLOOR_TOP + POCKET_H + LIP]))
    slope += slope.translate([10, 0, 0])   # the lips' 45 deg undersides run straight out of the open end too, like the pocket
                                           # (v5 at first left their rounded corners there: a flat ceiling that needed supports)
    # Posts: the side walls run on past the open end to the base's end, round the gate's grooves (the Dragy
    # still slides in between them: they're no narrower than the pocket). They're wider than the walls, so the
    # walls flare out to them over FLARE, and the end's two outer corners are rounded END_R.
    c = CrossSection.circle(END_R, 48)
    posts = CrossSection.batch_hull([CrossSection.square([0.01, OUT_W]).translate([X_FLARE0 - 1, -w2]),
                               CrossSection.square([0.01, OUT_W]).translate([X_FLARE0, -w2]),
                               CrossSection.square([0.01, 2 * POST_W2]).translate([X_FLARE1, -POST_W2]),
                               c.translate([X_POST - END_R, POST_W2 - END_R]), c.translate([X_POST - END_R, -POST_W2 + END_R])])
    outer += posts.extrude(TOP)
    mouth = Manifold.cube([X_POST - X_OPEN + 3, POCKET_W, TOP]).translate([X_OPEN - 1.3, -POCKET_W / 2, FLOOR_TOP])
    h = outer - pocket - opening - slope - mouth
    # Round the two nose-side (+y) corners in plan (add anything that sticks out of a wall after this: v3 lost a snap bump).
    body_plan = nose_rounded(2 * BASE_X, -w2, w2, NOSE_R, TAIL_R) - CrossSection.square([BASE_X, OUT_W + 2]).translate([X_FLARE0 - 0.5, -w2 - 1])
    h ^= (body_plan + posts).extrude(TOP + 1)   # the posts' outline takes over from X_FLARE0
    h -= grooves()
    h -= click(X_GATE + GATE_T + GATE_CLR, grow=CLICK_CLR, extra=GATE_CLR)   # the notches, for the plate pushed out
    # Push-out hole through the far wall: straight sides, then a 45 deg point (each layer held by the sides).
    # Centred on the Dragy's mid-height, PUSH_Y toward the nose; the point stays well under the lip.
    tall = PUSH_H + PUSH_W / 2
    z0 = FLOOR_TOP + DRAGY_T / 2 - tall / 2
    assert z0 + tall <= FLOOR_TOP + POCKET_H - 1.0, "the push-out hole would reach the far-end lip"
    assert abs(PUSH_Y) + PUSH_W / 2 <= POCKET_W / 2 - (DRAGY_R + FIT), "the push-out hole would reach the pocket's corner"
    prof = CrossSection([[(-PUSH_W / 2, 0), (PUSH_W / 2, 0), (PUSH_W / 2, PUSH_H), (0, tall), (-PUSH_W / 2, PUSH_H)]]).translate([PUSH_Y, 0])
    rot = np.array([[0, 0, 1.0], [1.0, 0, 0], [0, 1.0, 0]])   # profile (y, z), extruded along +x
    h -= s.place(prof.extrude(END_WALL + 2), rot, [X_FAR - 1, 0, z0])
    if grip:
        h += squeeze_ribs()
    # Move the body TRAY_Y toward the tail of the screws.
    h = h.translate([0, TRAY_Y, 0])
    # The two M4 screws: clearance holes down to the pad, counterbores up from the head's seat; both slotted
    # SLOT each way along the board, to take up error in where the pad's holes are.
    for sx in (1, -1):
        h -= slot(SEAT + 2, BOLT_HOLE, -1).translate([sx * M4_SPACING / 2, 0, 0])
        h -= slot(TOP, HEAD_BORE, SEAT).translate([sx * M4_SPACING / 2, 0, 0])
    # Optional plug into the oval hole (centred on the hole, not the body).
    if PLUG:
        h += hole_section().offset(-PLUG_CLR, circular_segments=64).extrude(PLUG_DEPTH + 0.5).translate([0, 0, -PLUG_DEPTH])
    return h


def slot(length, d, start):
    """A rod of diameter d along z from `start`, stretched SLOT each way along y."""
    return Manifold.hull(s.rod(length, d, start, seg=32).translate([0, -SLOT, 0]) + s.rod(length, d, start, seg=32).translate([0, SLOT, 0]))


def _stadium(w, t):
    """A stadium (a rectangle with round ends), w long and t tall, centred, in a 2D (y, z) section."""
    core = 1e-3                                  # a near-flat bar; rounding it by t/2 gives the stadium
    return CrossSection.square([w - t, core]).translate([-(w - t) / 2, -core / 2]).offset((t - core) / 2, circular_segments=32)


def grooves():
    """The two grooves the gate's plate slides down in, from the top to the shelf (holder's frame, before TRAY_Y)."""
    gw = GATE_T + 2 * GATE_CLR
    y2 = POCKET_W / 2 + GROOVE_D + GATE_CLR
    return Manifold.cube([gw, 2 * y2, TOP]).translate([X_GATE - GATE_CLR, -y2, FLOOR_TOP])


def pads():
    """The gate's two pads (holder's frame): from the plate's inside face to PRELOAD into the Dragy's end
    face (with the Dragy against the far wall). Their undersides are 45 deg, so as the gate goes down they
    ride over the Dragy's top edge and push it back; their tops are 45 deg too, as the gate prints upside down."""
    x_tip = X_OPEN - 2 * FIT - PRELOAD
    depth = X_GATE - x_tip
    z0, z1 = FLOOR_TOP + PAD_Z[0], FLOOR_TOP + PAD_Z[1]
    prof = CrossSection([[(0, z0 - depth), (0, z1 + depth), (-depth, z1), (-depth, z0)]])   # (x from the plate, z)
    rot = np.array([[1.0, 0, 0], [0, 0, 1.0], [0, 1.0, 0]])                          # section (x, z), extruded along y
    m = Manifold()
    for py in PAD_Y:
        m += s.place(prof.extrude(PAD_W), rot, [X_GATE, py - PAD_W / 2, 0])
    return m


def click_section(grow=0.0):
    """The clicks' ridges in section (x out from the plate's outer face, z), tips at (CLICK_H, each CLICK_Z above the shelf)."""
    up = CLICK_H / np.tan(np.radians(CLICK_UP))
    tri = CrossSection()
    for z in CLICK_Z:
        zc = FLOOR_TOP + z
        tri += CrossSection([[(-0.01, zc - CLICK_H), (CLICK_H, zc), (-0.01, zc + up)]])
    return tri.offset(grow, JoinType.Miter, miter_limit=4.0) if grow else tri   # sharp corners: a rounded tip would overhang


def click(x0, grow=0.0, extra=0.0):
    """The ridge (or, grown, its notch) along both of the plate's edges inside the grooves, with the plate's
    outer face at x0 (holder's frame, before TRAY_Y)."""
    rot = np.array([[1.0, 0, 0], [0, 0, 1.0], [0, 1.0, 0]])   # section (x, z), extruded along y
    y0, y1 = POCKET_W / 2 + 0.1 - extra, POCKET_W / 2 + GROOVE_D + extra
    m = Manifold()
    for sy in (1, -1):
        r = s.place(click_section(grow).extrude(y1 - y0), rot, [x0, y0, 0])
        m += r if sy > 0 else r.mirror([0, 1, 0])
    return m


def head():
    """The gate's head (holder's frame, before TRAY_Y): the posts' full-width outline from where the walls' flare
    ends to HEAD_OVER past the posts' ends, its outer corners rounded END_R like the posts'."""
    c = CrossSection.circle(END_R, 48)
    x1 = X_POST + HEAD_OVER
    plan = CrossSection.batch_hull([CrossSection.square([0.01, 2 * POST_W2]).translate([X_FLARE1, -POST_W2]),
                                    c.translate([x1 - END_R, POST_W2 - END_R]), c.translate([x1 - END_R, -POST_W2 + END_R])])
    return plan.extrude(HEAD_T).translate([0, 0, TOP + HEAD_GAP])


def gate(with_pads=True):
    """The plate that closes the open end, with its pads (pad frame)."""
    y2 = POCKET_W / 2 + GROOVE_D
    g = Manifold.cube([GATE_T, 2 * y2, TOP + HEAD_GAP + 0.01 - FLOOR_TOP]).translate([X_GATE, -y2, FLOOR_TOP])
    g += head()
    g += click(X_GATE + GATE_T)
    if with_pads:
        g += pads()
    return g.translate([0, TRAY_Y, 0])


def gate_spring():
    """Estimates for the plate as a spring: simply supported at the grooves, loaded at the two pads (4-point
    bending). Returns (force per pad in N, strain in %) at deflection d (mm), for PLA (E ~3.5 GPa)."""
    E, L = 3500.0, POCKET_W + GROOVE_D
    a = L / 2 - np.mean(np.abs(PAD_Y))
    I = (TOP + HEAD_GAP - FLOOR_TOP) * GATE_T ** 3 / 12
    return lambda d: (6 * E * I * d / (a * a * (3 * L - 4 * a)), 100 * 3 * d * GATE_T / (a * (3 * L - 4 * a)))


def nose_rounded(l, y0, y1, r, r_tail=0.0):
    """Plan rectangle l across (centred on x = 0), from y0 to y1, its two +y corners rounded at r (and its -x, -y
    corner at r_tail, if given)."""
    parts = [CrossSection.square([l, 0.01]).translate([-l / 2 + r_tail, y0])]
    if r_tail:
        parts += [CrossSection.circle(r_tail, 64).translate([-l / 2 + r_tail, y0 + r_tail])]
    parts += [CrossSection.circle(r, 64).translate([sx * (l / 2 - r), y1 - r]) for sx in (1, -1)]
    return CrossSection.batch_hull(parts)


def pad_outline():
    """The pad's flat area in plan: PAD_W x PAD_L, tail corners PAD_R, nose corners PAD_R_NOSE."""
    pts = []
    for (sx, sy, r) in ((1, 1, PAD_R_NOSE), (-1, 1, PAD_R_NOSE), (-1, -1, PAD_R), (1, -1, PAD_R)):
        pts.append(CrossSection.circle(r, 96).translate([sx * (PAD_W / 2 - r), sy * (PAD_L / 2 - r)]))
    return CrossSection.batch_hull(pts)


def casting():
    """The swingarm round the pad (pad frame): the pocket (rim RIM_H high), the oval hole, the M4 holes.
    Only the pocket and the holes are measured; the block round them is a placeholder."""
    block = Manifold.cube([PAD_W + 30, PAD_L + 30, RIM_H + 12]).translate([-(PAD_W + 30) / 2, -(PAD_L + 30) / 2, -12])
    pocket = pad_outline().translate([0, -HOLES_NOSEWARD]).extrude(RIM_H + 1)
    hole = hole_section().extrude(HOLE_D + 1).translate([0, 0, -HOLE_D])
    threads = Manifold()
    for sx in (1, -1):
        threads += s.rod(THREAD + 1, 3.3, -THREAD).translate([sx * M4_SPACING / 2, 0, 0])
    return block - pocket - hole - threads


def overhang_area(m):
    """Area (mm^2) of downward faces flatter than 45 deg, off the bed, as m sits (z up): what needs supports."""
    mesh = m.to_mesh()
    v, f = np.asarray(mesh.vert_properties)[:, :3], np.asarray(mesh.tri_verts)
    t = v[f]
    n = np.cross(t[:, 1] - t[:, 0], t[:, 2] - t[:, 0])
    a = np.linalg.norm(n, axis=1) / 2
    nz = n[:, 2] / (2 * a + 1e-12)
    return a[(nz < -np.cos(np.radians(45)) - 1e-4) & (t[:, :, 2].min(1) > v[:, 2].min() + 0.01)].sum()


def room(m, cast_outline, step=0.05, upto=5.0):
    """The smallest gap (to `step`) in plan between part m and the pocket's side."""
    plan = m.project()
    r = 0.0
    while r < upto and (plan - cast_outline.offset(-(r + step), circular_segments=96)).area() < 1e-6:
        r += step
    return r


def main():
    out = Path(sys.argv[1] if len(sys.argv) > 1 else "out")
    out.mkdir(parents=True, exist_ok=True)
    h, gt, d, cast, sc = holder(), gate(), dragy(), casting(), screws()
    for name, m in (("holder", h), ("gate", gt)):
        assert len(m.decompose()) == 1, f"{name} is not one piece"
        zero, bad = s.check_mesh(m, name)
        assert zero == bad == 0
    d_back = d.translate([-FIT, 0, 0])                 # the Dragy against the far wall
    pocket_plan = pad_outline().translate([0, -HOLES_NOSEWARD])
    lift = lambda m: Manifold.batch_boolean([m.translate([0, 0, 0.25 * k]) for k in range(161)], OpType.Add)   # swept up 40 mm
    lip_box = lambda sy: Manifold.cube([1.0, GROOVE_D - 0.1, TOP - FLOOR_TOP - 0.2]).translate(
        [X_GATE + GATE_T + GATE_CLR + 0.1, TRAY_Y + (POCKET_W / 2 + 0.05 if sy > 0 else -POCKET_W / 2 - GROOVE_D + 0.05), FLOOR_TOP + 0.1])
    checks = {
        "holder inside the pad's pocket": (h ^ cast).volume() < 0.01,
        "gate inside the pad's pocket": (gt ^ cast).volume() < 0.01,
        "Dragy fits the holder (apart from the squeeze ribs)": (d ^ holder(grip=False)).volume() < 0.01,
        "the ribs press SQUEEZE into each side of the Dragy": (d ^ h).volume() > 1.0 and (h ^ d.translate([0, -TRAY_Y, 0]).scale(
            [1, (DRAGY_W - 2 * SQUEEZE - 0.02) / DRAGY_W, 1]).translate([0, TRAY_Y, 0])).volume() < 0.01,
        "Dragy slides in and out between the posts": (Manifold.hull(d + d.translate([40, 0, 0])) ^ holder(grip=False)).volume() < 0.01,
        "screws clear of holder and Dragy (heads seated)": all((sc ^ m).volume() < 0.01 for m in (h, d)),
        "screws end flush with the casting's underside": abs(SEAT - SCREW_LEN + THREAD) < 1e-9,
        "gate clear of the holder": (gt ^ h).volume() < 0.01,
        "gate lifts straight up out, its clicks pushed back into the grooves' play": (lift(gt.translate([-0.15, 0, 0])) ^ h).volume() < 0.01,
        "...but not while the spring holds it out against the grooves (the clicks hold)": (lift(gt.translate([GATE_CLR, 0, 0])) ^ h).volume() > 0.5,
        "gate clear of the holder, pushed out against the grooves": (gt.translate([GATE_CLR, 0, 0]) ^ h).volume() < 0.01,
        "the clicks fit inside the grooves' play (they can slide down past the walls)": CLICK_H + 0.05 <= 2 * GATE_CLR,
        "gate clear of the screws": (gt ^ sc).volume() < 0.01,
        "the head covers both grooves": X_FLARE1 <= X_GATE - GATE_CLR and X_POST + HEAD_OVER >= X_GATE + GATE_T + GATE_CLR
            and POST_W2 >= POCKET_W / 2 + GROOVE_D + GATE_CLR,
        "the clicks' notches stay below the posts' tops": FLOOR_TOP + max(CLICK_Z) + CLICK_H / np.tan(np.radians(CLICK_UP)) + 0.5 <= TOP,
        "both grooves have a full-height lip behind the plate (bar the click's notch)": all(
            (lip_box(sy) - h - click(X_GATE + GATE_T + GATE_CLR, grow=CLICK_CLR, extra=GATE_CLR).translate([0, TRAY_Y, 0])).volume() < 0.01
            for sy in (1, -1)),
        "the pads press PRELOAD into the Dragy (against the far wall)": (gt ^ d_back).volume() > 0.5
            and (gt ^ d_back.translate([-PRELOAD - 0.01, 0, 0])).volume() < 0.01,
        "only the pads touch the Dragy, even pushed out to the open end": (gate(with_pads=False) ^ d.translate([FIT, 0, 0])).volume() < 0.01,
        "the pads stay 0.3 mm clear of the USB-C cut-out and the end's rounded corners": all(
            (abs(py) + PAD_W / 2 <= DRAGY_W / 2 - DRAGY_R - 0.3) and
            (py - PAD_W / 2 >= USB_Y + 9.84 / 2 + 0.3 or py + PAD_W / 2 <= USB_Y - 9.84 / 2 - 0.3) for py in PAD_Y),
        "each screw head seated on plastic (either side of the slot, anywhere along it)": all(
            ((s.rod(0.5, 7.0, SEAT - 0.5).translate([0, sy * SLOT, 0]) - slot(0.5, BOLT_HOLE + 0.1, SEAT - 0.5))
             .translate([sx * M4_SPACING / 2, 0, 0]) - h).volume() < 0.01 for sx in (1, -1) for sy in (1, -1, 0)),
        "holder prints floor down with no overhang past 45 deg (no supports)": overhang_area(h) < 0.01,
        "gate prints upside down on its ridge with no overhang past 45 deg": overhang_area(s.face_down(gt, [0, 0, 1.0])) < 0.01,
        "a charging plug clears the pocket's rim and the posts": (usb_plug() ^ cast).is_empty() and (usb_plug() ^ h).is_empty(),
    }
    for k, v in checks.items():
        print(f"  {k}: {v}")
    assert all(checks.values())
    spring = gate_spring()
    (f0, e0), (f1, e1) = spring(PRELOAD), spring(PRELOAD + 2 * FIT)
    print(f"holder {h.volume() / 1000:.1f} cm^3, gate {gt.volume() / 1000:.2f} cm^3; room to the pocket's side "
          f"{room(h, pocket_plan):.2f} mm (holder); the Dragy's top is {FLOOR_TOP + DRAGY_T - RIM_H:.1f} mm above the rim")
    print(f"gate spring (estimate): {f0:.1f}-{f1:.1f} N per pad, strain {e0:.2f}-{e1:.2f} % (pads pushed {PRELOAD}-{PRELOAD + 2 * FIT:.1f} mm)")
    al, mu = np.radians(CLICK_UP), 0.3      # each groove carries one pad's push (shared by its two clicks); PLA on PLA, friction ~0.3
    k = (np.sin(al) + mu * np.cos(al)) / (np.cos(al) - mu * np.sin(al))
    print(f"lifting the gate out past its clicks (estimate): {2 * k * f0:.0f}-{2 * k * f1:.0f} N in all")
    s.write_stl(s.face_down(h, [0, 0, -1.0]), out / f"dragy_holder_v{VERSION}.stl")   # floor down: no supports
    s.write_stl(s.face_down(gt, [0, 0, 1.0]), out / f"dragy_gate_v{VERSION}.stl")     # upside down, on its ridge
    colours = {"truck": (0.55, 0.55, 0.58), "tray": (0.80, 0.15, 0.12), "gate": (0.95, 0.65, 0.10),
               "dragy": (0.25, 0.45, 0.85), "steel": (0.2, 0.2, 0.2)}
    scene = {"front_swingarm_pad_schematic": (to_world(cast), "truck"), "dragy_holder": (to_world(h), "tray"),
             "gate": (to_world(gt), "gate"), "dragy": (to_world(d_back), "dragy"), "screws": (to_world(sc), "steel")}
    s.write_obj(scene, out / f"dragy_assembly_v{VERSION}.obj", colours)


if __name__ == "__main__":
    main()
