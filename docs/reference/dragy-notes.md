# Dragy GPS laptimer: notes for a separate mount project

Recorded 2026-11-16. The Dragy was considered for the rear light mount and left off; it will get
its own project.

## The unit (measured with calipers)

- 42.98 × 26.96 × 13.94 mm (13.91 measured at the other end), rounded corners and edges.
- USB-C port on one short end (27 × 14 mm face), along the long direction of that face.
- A white multi-pin connector on the other short end. Whether it must stay reachable is not decided.
- Logo ("dragy", ribbed) on the top face; "LAPTIMER.COM" on a long side.

## Where to mount it

- GPS needs open sky above the logo face. On the rear mount, a tray beside one light had a clear view
  up but widened the light bar to ~120 mm; in front of the bar it sat under the lights' metal bodies
  and the deck tail, which would block much of the sky.
- **The front truck's swingarm has a hole identical to the rear truck's "hole A", plus a pair of
  screw holes**, meant for mounting a Dragy or another display. The rear mount's shoe
  (`rear_mount.py`: plug, foot and angled M4×16 under the lip) fits hole A well (r4, 2026-11-16) and
  is a starting point, though the swingarm's surface angle and the screw holes' spacing still need measuring.
- Hole A, as measured on the rear truck: 16 wide × 17 long × 9 deep, solid floor, with a ~2 mm lip
  only at its rear end and ~2 mm of space under it; the surface around it is tipped 30° from flat.
  See the rear mount section of the README and `docs/reference/truck/rear-2026-11-15/`.

## USB-C dust cover

- Printable USB-C plugs exist online (e.g. printables.com/model/642573, makerworld.com/models/2747735,
  makerworld.com/en/models/2310346), but most state no licence or use MakerWorld's Standard Digital File
  License, so they can't be copied into a GPL project. Draw one from the standard instead.
- USB Type-C receptacle opening: 8.34 × 2.56 mm (8.34 +0.06/−0.02, 2.56 ±0.04 on manufacturer
  drawings), shell about 6.2 mm deep.
- TPU is recommended for a plug that seals; PLA/PETG are too stiff for a press fit. Idea: a cap that
  clips over the holder's open end with a short nub in the socket (TPU), or a PLA version whose nub
  stops short of the socket.

## Front swingarm mount point (2026-11-16)

Photos in [front-swingarm-2026-11-16/](front-swingarm-2026-11-16). On top of the front swingarm,
beyond the deck's nose, is a flat recessed pad (with a raised rim) holding the same oval hole as
the rear truck's hole A, with **two M4 threaded holes** on either side of it, across the board.

- M4 holes, centre to centre: **39.5 mm** (owner, re-measured). The 37.56 in the caliper photo is
  not accurate (the jaws weren't at the hole centres).
- Pad angle: **30° from flat**, the same as the rear truck, tipped the other way: it rises toward
  the **nose**. The lip on the oval hole is at its **front** end, the higher side (on the rear truck
  too, the lip is on the higher side, there the tail end).
- Flat area inside the rim: **66.38 mm** across the board (use 66.3).
- M4 threads: about **4 mm** long, right through the casting.
- Oval hole: the same as the rear (16 across × 17 along the board, its long sides left and right),
  **centred** between the two M4 holes.
- Lean clearance: nothing comes near the pad.
- USB-C (charging) end: either side works; use the rider's **right**. With the logo up, the port is off centre
  toward the **tail**: its case cut-out is 6.91 mm from one side wall and 10.21 mm from the other (~0.1 slop),
  so its centre is 1.65 mm off the centreline.
- Not yet measured: the flat area's length along the board, and how far the rim stands above it.
