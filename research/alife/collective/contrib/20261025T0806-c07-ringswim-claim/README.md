# ringswim-waste: ring-walled phase cells from noise that swim and divide (toward C:swim-divide)

`world_claim.py` = phase_membrane (Allen-Cahn cell held up by its own links, links adsorbed into
a ring at the wall by chi=2, noise IC) + phase_swimdiv's per-body phoretic drift (v = mu <grad S>
over each body, mu=1.5, now with a MUSCL face flux) + a self-made waste w that leaves a cell only
through its wall and adds kd w K to catalyst decay (kd=0.03). Controls: `world_mu0.py` (no drive),
`world_chi0.py` (no ring), and waste=0 (`img/nowaste_seed1_band.png`, celltrack nw_*).

## Numbers (128^2, T = 20000, 3 seeds)

celltrack.py: phi>1/2 cells linked by overlap every 20 t; a split is persistent when >= 2 daughters
each survive 400 t without merging back. BL = net displacement / sqrt(mean area) per track segment
(segments end at any split or merge).

| arm | persistent splits | splits / merges | max gen | tracks >= 3 BL | >= 5 BL | L rim/core (labkit radial) |
|---|---|---|---|---|---|---|
| claim s0 / s1 / s2 | 29 / 28 / 34 | 75/45, 70/55, 84/57 | 14 / 16 / 12 | 26 / 36 / 21 | 8 / 14 / 2 | 1.49 / 1.27 / 1.59 (35/51, 20/45, 49/67 cells membrane-like) |
| mu = 0 s0 / s1 | 27 / 31 | 104/0, 104/1 | 3 / 5 | 0 / 0 | 0 / 0 | 1.77 |
| chi = 0 s0 / s1 | 16 / 12 | 25/2, 18/0 | 5 / 5 | 30 / 22 | 15 / 9 | 1.15 (0/114) |
| waste = 0 s0 / s1 / s2 | 30 / 11 / 33 | | 11 / 7 / 15 | 14 / 13 / 14 | 2 / 4 / 0 | s1 fuses into one domain-wrapping band by t~13000 |

## What the images show

- `pack/seed0/sheet.png`, `pack/seed1/sheet.png`, `pack/seed2/sheet.png`: from noise, a
  bounded population (5-9 cells, occupancy 0.16-0.22) of walled cells: round cells and crescents
  with a depletion wake, moving, colliding, fusing and pinching, to t=20000 on all seeds.
- `strip_s1.png` row 1 (seed 1, celltrack tracks 125 > 126 > 136): a three-lobed body pinches at
  t~11100; daughter 126 moves 2.4 BL and pinches again at t~12100; its daughter 136 swims 7.9 BL
  over 2640 t. Rows 2-3: an S-shaped body (165, itself a merge product) pinches at t~15080 into two
  crescents that swim 8.6 and 11.2 BL. `division_s1_t11000.png`: phi and L in a fixed window.
- `pack/seed2/radial.png`: L peaks at the wall (rim/core 1.59, rim/outside 6.15); chi=0 loses
  the ring (`pack_chi0/seed0/radial.png`, 1.15).

## Limits (read these)

- Reticulate: merges are 55-80% of splits. Many divisions are pinches of bodies that formed by a
  recent fusion; the persistent-split count excludes daughters that re-merge within 400 t but not
  parents born by fusion. labkit's own tracker (frames 100 t apart) finds 0 persistent splits here;
  D rests on celltrack.py and the strips.
- The drive is phase_swimdiv's per-body label average (nonlocal). A label-free Gaussian-kernel
  drive (in `world_claim.py`, drive="kernel") gave swimming bands in every setting tried (see the
  sighting 20261025T0739-c07-ringswim-sighting).
- The ring is weakened by swimming (1.27-1.59 vs 1.77 static) and fails the 1.5 aggregate test on
  seed 1. Swimming is slow (0.03-0.06 px/t) and chi=0 cells swim farther than ringed cells.
- Waste was added for size control. Without it 1/3 seeds formed a band by t=20000, so waste is
  not shown to be necessary. Motion and the controls were measured at one parameter point; no dt or
  resolution check.
- The celltrack runs used the earlier copy `world.py` with key=val overrides equal to
  `world_claim.py`'s defaults (drive=label mu=1.5 waste=1 kd=0.03; chi=0, mu=0, waste=0 for controls).
