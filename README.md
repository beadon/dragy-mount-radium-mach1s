# Dragy mount for the Radium Mach One S

A 3D-printable holder for a **Dragy GPS laptimer** on a Radium Mach One S electric skateboard,
plus a **USB-C dust cover** for the Dragy's charging port.

The holder sits in the recessed pad on top of the **front swingarm**, beyond the deck's nose, where
the sky is open, and screws into the pad's two M4 threaded holes, which Radium put there for
accessories like this.

**Status:** v3. v2's holder was test-printed (2026-11-16): the Dragy fits; v3 moves the push-out hole. The cap is not yet printed. v1 bolted a tray onto the **shoe** (`shoe.py`), the anchor that
locks into the oval hole and that holds the rear lights in
[beadon/shredlight-mounts](https://github.com/beadon/shredlight-mounts). The front pad's threaded
holes make that unnecessary here, but the shoe stays in this repo as its own component for other uses.

![Dragy mount v3, shaded renders](docs/render.png)


## Parts

| Part | File (in `out/`) | Print |
|---|---|---|
| Holder | `dragy_holder_v3.stl` | Floor down. No supports: nothing overhangs (45° lip undersides, a pointed top on the far-end push-out hole, a tether hook that rises out of the wall at 45°). |
| USB-C cap (with its tether) | `dragy_usbc_cap_v3.stl` | End plate down, gasket up, the tether flat on the bed. **TPU**: the gasket must squash and the tether bend. |
| Assembly | `dragy_assembly_v3.obj` (+ `.mtl`) | For Blender: the parts in a schematic front swingarm pad. Not for printing. |
| Shoe (separate component) | `shoe.stl` | Not used by v2/v3. Top face down, plug up, no supports. See `shoe.py`. |

See [PRINT_SETTINGS.md](PRINT_SETTINGS.md) for the slicer profile.

## How it goes together

- **The pad** (measured): a flat area 66.3 mm across and 40.4 mm along the board (35 mm measured
  level), at the bottom of a pocket whose rim stands 15.55 mm above it. It's tipped 30° from flat,
  rising toward the nose. The oval hole is in its middle, with an M4 threaded hole either side,
  39.5 mm apart, across the board. The threads are about 4 mm long, right through the casting.
- **The holder** sits in the pocket, on the pad, held by two **M4×16** socket-head screws. They seat
  12 mm up in its floor, so their last 4 mm catch all of the pad's thread and stop flush with the
  casting's underside. The screws and the pocket's walls locate it. (An optional plug into the oval
  hole is `PLUG` in `dragy_mount.py`; it's off, because it would stop the holder printing floor-down.)
- **The Dragy** (42.98 × 26.96 × 13.94 mm, measured) lies parallel to the pad, logo up, long side
  across the board, so the GPS sees open sky. It slides in from the USB-C end, the rider's right.
  Lips along both long sides and the far end stop it lifting out, and two small bumps inside the side
  walls hold it while it charges. The far end's wall has an 8 mm push-out hole (pointed top, so it
  prints without supports): push through it to slide the Dragy out. It's 2 mm toward the nose of centre,
  so the wall covers the white connector (off centre toward the tail) and pushing can't damage it. The pocket's floor corners are
  rounded to match the Dragy's rounded bottom edges (2 mm; its top edges are sharp). The
  screw heads sit under the Dragy: slide it out to reach them.
- **The floor is thick on purpose:** it lifts the Dragy so its top is 14.8 mm above the rim and the
  USB-C port's centre 7.8 mm above it, so a charging cable plugs straight in from the right, over the rim.
- **The cap** slips over the holder's open end, sitting on the base's shelf, and clicks onto two
  bumps on the tray's sides. It holds the Dragy in. Inside, a soft **gasket ring** presses on the
  Dragy's end face round the USB-C opening (pushing the Dragy back against the far wall); nothing goes
  into the socket, so its contacts and centre tongue are never touched, and a millimetre of error in
  the port's position doesn't matter. A **tether** strap, printed flat with the cap, ends in a ring that
  hooks onto the holder's tail-side wall, so the cap can't be lost: an arm rises out of the wall at
  45°, and its tip flares wider than the ring's hole, so the TPU ring stretches over the tip, relaxes
  onto the arm, and has to stretch again to come off. Pull the cap off to charge.
- **The USB-C port is off centre** (measured): its case cut-out is 6.91 mm from one side wall and 10.21 mm
  from the other, so its centre is 1.65 mm off the Dragy's centreline. With the logo up and the USB-C end
  on the rider's right, it's toward the **tail** (`USB_SIDE` in `dragy_mount.py`).

Hardware: two M4×16 socket-head screws. A drop of removable threadlocker keeps them from backing out.

## Building

```sh
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python dragy_mount.py out   # holder and cap STLs and the assembly OBJ (runs every fit check)
.venv/bin/python shoe.py out          # the shoe on its own
.venv/bin/python render.py            # docs/render.png
```

Every dimension is a named constant, in millimetres, at the top of `shoe.py` and `dragy_mount.py`.
The scripts stop with an error if a check fails (parts overlapping, the Dragy not fitting, the
shoe not dropping into the hole or not locking, a pinched mesh).

## Not yet known

- The USB-C port's height on the Dragy's end face (assumed mid-height; the gasket tolerates ~1 mm); the Dragy's plan-view corner radius (assumed 4 mm); and the white connector's exact position (the push-out hole was moved 2 mm toward the nose after the first test print, to keep it off the connector).
- Where the M4 holes sit along the pad (assumed centred; v2 hit the nose-side corners, so they may be nose-ward) and the pocket's corner radii (assumed 12 mm at the nose, 8 mm at the tail) and the size of a charging plug's moulding (assumed
  13 × 7.5 mm, 30 mm long) for the rim-clearance check.

## Roadmap

- [x] v1: a tray bolted onto the shoe (`shoe.py`, from shredlight-mounts r4), and the USB-C cap. Not printed.
- [x] Measure the front swingarm's pad: 30° (nose up), 66.3 × 40.4 mm, rim 15.55 mm, M4 holes 39.5 mm apart, 4 mm threads
- [x] v2: a holder in the front swingarm's pad, screwed into its two M4 holes, and the USB-C cap
- [x] Print v2's holder (2026-11-16): prints without supports (after rooting the tether hook in the wall); the Dragy fits but
  rattles left/right with the cap off; the centred push-out hole uncovered part of the white connector
- [x] v3: the push-out hole 2 mm toward the nose, so the wall covers the white connector
- [x] v2 in the pad (2026-11-16): its nose-side corners hit the pocket's rounded corners (the model's pad doesn't show this)
- [x] v3: the holder's body 1 mm toward the tail of the screws (`TRAY_Y`), its nose-side corners rounded 8 mm (`NOSE_R`)
- [ ] Measure where the M4 holes sit along the pad (to its nose- and tail-side walls) and the pocket's nose corner radius
- [ ] Print v3 and the TPU cap: test-fit in the pad, the cap on the holder (does it stop the rattle?), and a charging cable over the rim

## License

[GPL-3.0](LICENSE), the same as [shredlight-mounts](https://github.com/beadon/shredlight-mounts).
Dragy is a trademark of its owner, and Radium and Mach One of theirs. This project is not affiliated
with or endorsed by them.
