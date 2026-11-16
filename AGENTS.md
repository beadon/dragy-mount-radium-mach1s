# Notes for agents working in this repo

Read this first. It records how the project is built, what is measured versus assumed, and how the
owner likes to work.

## What this is

A Dragy GPS laptimer holder and a USB-C dust cover for a Radium Mach One S electric skateboard,
mounted on the **shoe** (`shoe.py`), which locks into the oval "hole A". Sister project:
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
- `dragy_mount.py`: the tray and the USB-C cap, the fit checks, and all outputs in `out/`.
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
- **Front swingarm**: the owner says it has an identical hole plus a pair of screw holes for a Dragy
  or display. Its surface angle, the screw holes' size and spacing, and what's around the hole are not
  measured. The shoe's rear overhang (over the rear truck's step) and its 3 mm-shortened nose (clear
  of the rear truck's Ra button) may not suit it. Ask for these before adapting the shoe.
- Dragy: USB-C centred on its end face with its long side across the 27 mm width; 4 mm plan corner
  radius; white connector fits a 16 × 8 mm window.
- USB-C receptacle opening 8.34 × 2.56 mm, ~6.2 mm deep (USB Type-C spec / maker drawings).

## How the owner likes to work

- Ask how a measurement was taken (surface to surface? square to what?) and cross-check it against an
  overall dimension before relying on it.
- Use pictures (renders, sections) for 3D or orientation questions, not ASCII, and use
  nose / tail / sky / ground / rider's left/right wording.
- They open models in Blender to review (`out/*.obj`), and test-print before committing to a design.
- Commit or push only when asked. Keep notes of measurements in the repo (`docs/reference/`).
