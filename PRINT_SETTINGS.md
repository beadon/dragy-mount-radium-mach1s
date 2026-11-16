# Print settings

The parts are printed on an **Original Prusa MK4 (Input Shaper), 0.4 mm nozzle**, in PrusaSlicer,
with the profile below. The support settings matter most: they're tuned so supports break away cleanly.

## Profile

Based on the system profile **0.20mm SPEED @MK4IS 0.4**, saved as a copy, with filament **Generic PLA**
(TPU for the USB-C cap).

| Setting | Value |
|---|---|
| Layer height / first layer | 0.2 mm / 0.2 mm |
| Perimeters | 2 |
| Top / bottom solid layers | 5 / 3 |
| Infill | 15–20 %, grid |
| Seam | aligned |
| Brim, skirt | none |

### Support material (Print Settings → Support material)

| Setting | Value |
|---|---|
| Generate support material | on |
| Auto generated supports | on |
| Overhang threshold | 40° |
| Enforce support for the first | 0 layers |
| Raft layers | 0 |
| Style | **Organic** |
| Top contact Z distance | **0.25 mm** |
| Bottom contact Z distance | same as top |
| Pattern | rectilinear, 2 mm spacing, 0° |
| With sheath around the support | off |
| Top interface layers | 2 |
| Bottom interface layers | 0 (off) |
| Interface pattern | default, **0.3 mm** spacing |
| Interface loops | off |
| Support on build plate only | **on** |
| XY separation between an object and its support | **0.6 mm** |
| Don't support bridges | **on** |
| Organic: max / preferred branch angle | 40° / 25° |
| Organic: branch diameter, angle, double-wall diameter | 2 mm, 5°, 8 mm |
| Organic: tip diameter, branch distance, density | 0.8 mm, 1, 30 % |

The 0.25 mm top contact gap, the 0.6 mm XY gap, the sparse 0.3 mm interface and "don't support
bridges" are what let supports snap off cleanly. "Build plate only" keeps supports out of
pockets and slots that would be hard to clear.

## Per part

- **Holder** (`dragy_holder_v2.stl`): floor down. Supports off: the lips' undersides are 45°, the
  screw counterbores are vertical, and the far-end window's top edge is a 16 mm bridge.
- **USB-C cap** (`dragy_usbc_cap_v2.stl`): end plate down, gasket up, the tether flat on the bed. TPU
  (e.g. a 95A TPU profile, slow), supports off.
- **Shoe** (`shoe.stl`, not used by v2): as exported, top face down, plug up. Supports off: with them on,
  build-plate-only supports can reach into the side-opening nut slots.
