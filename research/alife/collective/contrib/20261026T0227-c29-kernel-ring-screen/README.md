# Kernel-drive ringswim with a ring above the gate (c29)

c28's ringswim-dl2 `world.py`, unchanged, run with the label-free local drive (`drive=kernel`: each pixel moves
with a Gaussian-weighted (sig 6) substrate gradient, no per-body labels) and three overrides:
`WORLD_P={"drive":"kernel","mu":1.0,"kd":0.08,"chi":5}` (ringtrack: `drive=kernel mu=1.0 kd=0.08 chi=5`).

`screen_table.md` (`screen_table.py`): 16 settings at 128^2, seed 0, t=10000. Raising chi lifts labkit's L rim/core
(1.36 at chi 2 to 1.66-1.72 at chi 5-6), raising kd cuts merges, and raising mu restores motion but lowers the
ring and brings merges back (mu 1.25: ring 1.28, 139 merges). chi 5, mu 1.0, kd 0.08 is the corner where all three
hold. mu 0.75 at 256^2 gives a ring (97% of frames) but only 4-12 swimmers (`data/rt_chi5kd08_*`).

256^2, seeds 0 and 1 (`pack/`, t=10000; `data/rt_chi5mu10_*`, ringtrack to t=20000):

| | seed 0 | seed 1 |
|---|---|---|
| labkit L rim/core (membrane-like individuals) | 1.64 (1148/1434) | 1.57 (987/1370) |
| labkit persistent splits / max gen / merges | 224 / 5 / 72 | 244 / 6 / 95 |
| ringtrack ring >= 1.5 (median) | 95.0% (1.67) | 95.1% (1.68) |
| ringtrack persistent splits / max gen / merges | 41 / 3 / 8 | 43 / 3 / 13 |
| tracks >= 3 BL (all ringed) | 36 | 47 |
| lineages that swim >= 3 BL ringed and divide | 1 (#78) | 3 (#333, #325, ...) |

Controls at 256^2, seed 0: mu=0 (`pack_mu0`): 6 tracks move >= 1 BL, max 1.9 BL. chi=0 (`pack_chi0`): ring
0.98 (3/97 membrane-like), 16 persistent splits vs 224.

Limit: all of it happens while the cells colonize the domain. By t~5000 the cells fill the torus and jam into a
static near-hexagonal lattice (pack/seed1/sheet.png), where nothing swims and few divide. The daughters of #333
move 3-14 px in the next 15000 steps (img/strip_s1_333.png).
