# Review of 20261027T0712-c53-fed-vortex-claim#c1 (c54), fresh seeds 54 and 55

Re-runs (world defaults, --frames 1000 --spf 150, T = 3000, default window K = 20 frames = 60 t): rerun/seed54, rerun/seed55;
the fuel fork at t = 2000 (fork/, seed 54, WORLD_P fork_t 2000); the no-advection twin (noadv/, seed 54, WORLD_P adv 0).
strips.py draws four random persistent splits of seed 55 (|omega| > 0.06, render frames ~25 t apart).

| | seed 54 | seed 55 | claim seeds 0-2 |
|---|---|---|---|
| persistent splits / max generation / merge-split | 52 / 10 / 0.85 | 38 / 10 / 0.87 | 34, 39, 42 / 10, 9, 10 / 0.91-1.02 |
| no-advection twin (seed 54) | 13 / 3 / 0 merges | | gen 1-2 |
| bodies (|omega| > 0.06) around the fork, fed vs forked (seed 54) | t 1965-2118: 27-31 fed; forked 27, 29 (t 2004), 19 (2043), **0** (2079), 0 | | 0 by t 2070 |

- **S**: band-passed random vorticity on uniform fuel (sheet t = 0); ~30 vortices of both signs by t = 126.
- **I**: discrete vortices of both signs, 25-31 at a time, each persisting between collisions (sheet.png).
- **D**: 52 and 38 persistent splits, generation 10 on both seeds, splits continue to the end (sheet t 2346-2472: a cyan rod
  stretches and pinches). Strips rows 2 and 4 (t 1689-1791, 2673-2850) show rods pinching into two vortices; rows 1 and 3 are
  less clear at 25 t spacing. Merge/split 0.85-0.87, so the genealogy is reticulate (confidence medium, RUBRIC L6).
- **E**: fork replicates: every vortex goes out within ~80 t of emptying the fuel, the fed twin keeps 27-31. By construction:
  vorticity grows only by eating fuel and decays at mu (the claim says so).
- Twin: with advection off the same reaction-diffusion still splits, but less (13 persistent splits, generation 3 on seed 54,
  against generation 1-2 in the claim). The flow raises division 4x and the depth from 3 to 10 generations; it does not create it.

Verdict **Supported** for S, I, D; E seen and by construction.
