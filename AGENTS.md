# Notes for agents working in this repo

Read this first. It records how the project is built, what is measured versus assumed, and how the
owner likes to work.

## What this is

A Dragy GPS laptimer holder and a USB-C dust cover for a Radium Mach One S electric skateboard.
v2 sits in the recessed pad on top of the front swingarm and screws into its two M4 threaded holes.
v1 bolted onto the **shoe** (`shoe.py`), which locks into the oval "hole A"; the shoe stays here as
its own component. Sister project:
[beadon/shredlight-mounts](https://github.com/beadon/shredlight-mounts), where the shoe was developed
(`rear_mount.py`) for the rear lights. The owner keeps the shoe in both repos for easy reference and
will split it into its own repo once a third component needs it. **If the shoe changes, keep both
copies in step** (and say so in both READMEs).

## Layout

- `shoe.py`: hole A, the shoe, its angled locking screw, and the **INTERFACE** other parts bolt onto
  (a flat pad at `TOP_Z`, two M4 bolts at (±`BOLT_X`, `BOLT_Y`) into hex nuts at `NUT_Z`;
  `head_seat(L)` gives the counterbore floor for an M4 × L bolt). Also shared helpers (`place`,
  `along`, `rod`, `nut_pocket`, `face_down`, `write_stl`, `write_obj`, `check_mesh`, `min_gap_ok`) and
  `surroundings()`, a rough model of the rear truck round hole A.
- `dragy_mount.py`: the holder and its gate (v5-v8; v2-v4 had a TPU USB-C cap), built in the PAD frame (x across, y up the pad's
  slope toward the nose, z out of the pad; `PAD_FRAME` places them in the world), the schematic pad
  (`casting()`), the fit checks, and the outputs in `out/`.
- `render.py`: shaded PNG renders (no 3D viewer needed) to `docs/render.png`.
- `docs/reference/`: measurements and notes.

Build: `python3 -m venv .venv && .venv/bin/pip install -r requirements.txt`, then
`.venv/bin/python dragy_mount.py out` and `.venv/bin/python render.py`. Geometry is manifold3d CSG.

## Conventions

- Millimetres. World frame: x to the rider's right, y toward the nose, z up (sky); origin at the
  centre of hole A on the surface around it. Hole-local frame `HOLE_FRAME`: (X, s, h) with s along the
  surface toward the tail and h out of the surface.
- Every printed part must pass its checks (one piece, clean mesh, no overlaps, fits, can't lift) before
  it's written. Add a check for anything new that could collide.
- Export each STL in its print orientation (`face_down`), support-free where possible. Check overhangs
  by rendering faces steeper than 40° from the bed, as in shredlight-mounts.
- Versions: bump `VERSION` in `dragy_mount.py` for any change to a printed part, and the filenames
  carry it (`_v1`). Record each version's purpose and test result in the README roadmap.
- Hardware: M4 socket-head cap screws and **plain** M4 hex nuts, 3.11 mm thick (measured), not nylocs.
  The owner has M4 × 16 and M4 × 20 on hand. Captive nuts in side slots; no threads cut into plastic.
- Print settings: [PRINT_SETTINGS.md](PRINT_SETTINGS.md). Prusa MK4 Input Shaper, PrusaSlicer as a
  Flatpak. Never run PrusaSlicer with `--loglevel=5`: it logs the Prusa Connect bearer token.

## Measured vs assumed

Measured (owner, calipers/inclinometer):
- Dragy: 42.98 × 26.96 × 13.94 mm. USB-C on one short end, a white connector on the other.
- Hole A (rear truck): 16 wide × 17 long × 9 deep, solid floor; ~2 mm lip only at the rear end, ~2 mm
  of space under it (possibly a little more); the surface round it is tipped 30° from flat, facing the
  nose. Behind it the surface steps up 7.5 mm (vertical) to the charging port, whose centre is 22 mm
  behind the hole (level). The charging plug is 17.5 mm across and stands vertically.
- The shoe as built fits the rear hole A well (shredlight-mounts r4, 2026-11-16).

Assumed / unknown:
- Front swingarm pad (measured 2026-11-16): 30° from flat, rising toward the **nose** (the oval hole's
  lip is at its front, higher end); flat area 66.3 across × 35 measured level (40.4 along the slope);
  rim 15.55 above it; M4 threaded holes 39.5 apart across the board (an earlier 37.56 was a bad caliper
  reading), threads ~4 mm, right through; oval hole 16 × 17, centred. Nothing comes near when leaning.
  The pocket's nose end is nearly a semicircle (~20 mm corners, photo); tail corners assumed 8 mm. The holes are NOT
  centred along the pad: fitted to the v2/v3 test prints, they sit ~6.2 mm nose-ward of its centre
  (`HOLES_NOSEWARD`, an estimate; v3 rested with its holes ~2 mm tail-ward of the pad's). v4 puts the holder's body
  3.6 mm tail-ward of the screws (`TRAY_Y`) with slotted holes (`SLOT`, ±1 mm), and rounds its nose-side corners
  (`NOSE_R`). Anything that sticks out of a wall must be added after the corner rounding (v3 lost a snap bump that way).
  The pocket's nose end leaves little room past the holder's open end on its nose side: v5's gate posts (2.5 mm)
  fit with 1.4 mm to spare in the model; a zig-zag spring there (~6 mm) would not. v6 made the posts flush with the
  1.3 mm walls (0.45 mm grooves): the gate didn't stay in (print, 2026-11-18), so v7 is back to v5's posts and 0.9 mm
  grooves (1.3 mm to spare), and v8 flares the walls out to the posts over 5 mm and runs them to the base's end
  (1.15 mm to spare). Keep grooves at least 0.9 mm deep.
- Dragy: USB-C on its end face, long side across the 27 mm width, its case cut-out 6.91 from one side wall
  and 10.21 from the other (measured, ~0.1 slop): centre 1.65 off centre, toward the TAIL with the logo up and
  the USB-C end on the rider's right (owner, `USB_SIDE = -1`). Mid-height assumed. 4 mm plan corner radius; bottom edges rounded 2 mm, top edges sharp (owner). The far wall has an 8 mm push-out hole,
  2 mm toward the nose of centre (`PUSH_Y`; owner, test print 2026-11-16: centred, it uncovered part of the white
  connector, which is off centre toward the tail), with a 45° pointed top (a flat-topped window was a bridge the screw counterbore broke up; a 45° ramp through
  the wall's thickness still left a 16 mm span; its cutter also clipped the lip, leaving a floating sliver).
- USB-C receptacle opening 8.34 × 2.56 mm, ~6.2 mm deep (USB Type-C spec / maker drawings).
  Its centre tongue (contacts on both faces) is about 6.69 wide × 0.7 thick, so nothing should enter the socket
  (a nub would clear the tongue by ~0.15 mm, under the measurements' slop). v2-v4's TPU cap pressed a gasket ring
  round the opening; it came off too easily (v4 print, 2026-11-17), so v5 closes the end with a PLA gate whose
  pads press on the end face beside the opening.

## How the owner likes to work

- Ask how a measurement was taken (surface to surface? square to what?) and cross-check it against an
  overall dimension before relying on it.
- Use pictures (renders, sections) for 3D or orientation questions, not ASCII, and use
  nose / tail / sky / ground / rider's left/right wording.
- They open models in Blender to review (`out/*.obj`, written Y-up so Blender's default import is sky-up), and test-print before committing to a design.
- Commit or push only when asked. Keep notes of measurements in the repo (`docs/reference/`).
