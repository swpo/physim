# lcn starvation forks (c18)

World: `world.py` (defaults: h0=0.6, F0=1, Y=2, decay 0.002, kr=0.02, D=DW=1, beta=0; META tracking keys
differ from the runs below only in `matter`/`threshold`, which do not touch the dynamics).

Pre-runs: seeds 0, 1 from full-domain noise to t=1000 (`scripts/runsave.py world.py pre<s> <s> 1000`).

1. Global fork at t=1000: fed twin vs all food and waste removed (`STARVE_ALL=1`), 500 t each.
   forkglobal.png rows: fed0, starve0, fed1, starve1. Starved: matter falls to 0.13 (seed 0) and 0.03 (seed 1)
   of its fork value within ~80 t; 4 and 1 cogs survive, on food regrown from the dead bodies' waste
   (mean F returns to about 0.2). Fed twins: matter 0.85-1.2 of the fork value throughout, worms and cogs persist.
2. Local fork at t=1000 (`scripts/mkcut.py`, `CUT=1`): food in a disk around ONE body (a cog, r=18; the largest
   interior worm, r=30 or 42) is moved out of the disk every step (kept in the ledger, spread over the rest of
   the domain). localcut.png, 250 t:
   | body | matter in disk at end, cut / fed twin | neighbour annulus (r..r+25), cut / fed | inside <10% at |
   |---|---|---|---|
   | cog seed 0 | 0.03 / 0.63 | 0.92 / 1.05 | t=1045 |
   | worm seed 0 | 0.00 / 1.91 | 0.67 / 1.08 | t=1045 |
   | cog seed 1 | 0.00 / 1.44 | 0.99 / 1.28 | t=1030 |
   | worm seed 1 | 0.00 / 1.28 | 0.94 / 1.02 | t=1015 |
3. Turnover (500 steps from the t=1000 checkpoints): gross matter built 0.051 (seed 0) and 0.049 (seed 1) per
   unit matter per t, gross loss 0.048 / 0.047, of which imposed decay is 0.002. Matter turns over every ~20 t.

Limits: the cut disk is a permanent food sink, so it also drains its neighbours' edge (worm seed 0 annulus 0.67);
the worm disks (r=30-42) cover parts of neighbouring bodies; the fed twin's target body is sometimes displaced
by a passing worm (cog seed 0); build-from-food is by construction, so what this adds is the size of the effect:
bodies die in 15-45 t, 10-30x faster than decay alone would remove them.
