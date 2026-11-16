# Dragy mount for the Radium Mach One S

A 3D-printable holder for a **Dragy GPS laptimer** on a Radium Mach One S electric skateboard,
plus a **USB-C dust cover** for the Dragy's charging port.

The holder bolts onto the **shoe**: a small printed anchor that locks into the oval hole ("hole A")
that Radium puts in the rear truck's hanger pocket and, identically, on the front swingarm. The shoe
is its own component (`shoe.py`), so other things (a display, a light) can bolt onto it too.

**Status:** first cut (v1), **not yet printed**. The shoe itself is proven: it's the rear-light
mount's shoe from [beadon/shredlight-mounts](https://github.com/beadon/shredlight-mounts)
(`rear_mount.py`, r4), which fits the rear truck's hole A well (2026-11-16). The tray and the cap
are new.

![Dragy mount v1, shaded renders](docs/render.png)

## Parts

| Part | File (in `out/`) | Print |
|---|---|---|
| Shoe | `shoe.stl` | Top face down, plug up. No supports. |
| Dragy tray | `dragy_tray_v1.stl` | Floor down. No supports: the lips over the Dragy's edges have 45° undersides. |
| USB-C cap | `dragy_usbc_cap_v1.stl` | End plate down, nub up. **TPU** (it seals and grips). For PLA, set `CAP_NUB = 0` in `dragy_mount.py`. |
| Assembly | `dragy_assembly_v1.obj` (+ `.mtl`) | For Blender: the parts on hole A with the rear truck's rough surroundings. Not for printing. |

See [PRINT_SETTINGS.md](PRINT_SETTINGS.md) for the slicer profile.

## How it goes together

- **The Dragy** (42.98 × 26.96 × 13.94 mm, measured) lies flat, logo up, so the GPS sees open sky.
  It slides into the tray from the USB-C end (the rider's right). Lips along both long sides and the
  far end stop it lifting out, and two small bumps inside the side walls hold it while it charges.
  The far end's wall has a window for the Dragy's white connector.
- **The cap** slips over the tray's open end and clicks onto two bumps on the tray's sides. It closes
  that end, holding the Dragy in, and a nub plugs the USB-C socket. Pull it off to charge.
- **The tray** sits on the shoe's flat top and is held by two M4×16 bolts going down through its floor
  into hex nuts in the shoe. The bolt heads sit under the Dragy.
- **The shoe** drops into hole A and is locked by one M4×16 that goes in from the nose side, 30° below
  level, through a hex nut and under the lip at the hole's rear end. The tray leaves the hex key's
  path to that screw clear.

Hardware: three M4×16 socket-head screws and three plain M4 hex nuts (3 mm thick; the pockets fit
3.11 mm with 0.3 mm to spare). The nuts have no nylon insert, so use a drop of removable threadlocker.

To fit it: slide the nuts into the shoe's three side slots, bolt the tray onto the shoe (before the
shoe goes on the board), back the angled screw off until its end is inside the plug, drop the plug
into hole A, and tighten the angled screw from the nose side until it's snug.

## Building

```sh
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python dragy_mount.py out   # shoe, tray, cap STLs and the assembly OBJ (runs every fit check)
.venv/bin/python shoe.py out          # the shoe on its own
.venv/bin/python render.py            # docs/render.png
```

Every dimension is a named constant, in millimetres, at the top of `shoe.py` and `dragy_mount.py`.
The scripts stop with an error if a check fails (parts overlapping, the Dragy not fitting, the
shoe not dropping into the hole or not locking, a pinched mesh).

## Not yet known

- **Where it goes.** The front swingarm has the same hole plus two screw holes, but its surface angle
  and surroundings aren't measured; the shoe's shape was fitted to the rear truck (30° surface, a step
  up to the charging port behind the hole, the Ra button in front). See [AGENTS.md](AGENTS.md).
- The Dragy's USB-C position on its end face (assumed centred), its plan-view corner radius (assumed
  4 mm), and the white connector's size (a 16 × 8 mm window is left for it).

## Roadmap

- [x] v1: shoe (from shredlight-mounts r4), Dragy tray and USB-C cap
- [ ] Print v1 and test-fit the Dragy in the tray and the cap on the tray
- [ ] Measure the front swingarm round its hole: surface angle, the two screw holes, nearby parts
- [ ] Decide where the Dragy rides (front swingarm or rear truck) and adapt the shoe if needed

## License

[GPL-3.0](LICENSE), the same as [shredlight-mounts](https://github.com/beadon/shredlight-mounts).
Dragy is a trademark of its owner, and Radium and Mach One of theirs. This project is not affiliated
with or endorsed by them.
