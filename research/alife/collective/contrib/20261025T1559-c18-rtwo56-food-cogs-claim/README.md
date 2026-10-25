# lcn-cog: r-two56 cogs that live on a closed food-waste cycle (c18)

`world.py`: the unmodified r-two56 rule (lab 1, `threads/lenia-multichannel/worlds/r-two56`) with build-from-food
(yield 2) charged gross, maintenance decay 0.002, every loss turned into waste W that regrows into food (kr 0.02);
sum(A)/2 + sum(F) + sum(W) is conserved and asserted every 100 steps; no refill, no sink; uniform noise over the
whole domain at t=0. dt = 0.1 (T=10), 192^2, R=10.

## Runs (all from `scripts/`, run in the directory holding world.py)
- Pack: `python -m labkit.run world.py --out pack --seeds 0 1 --frames 200 --spf 50 --no-movie` (t=1000).
  14 and 11 persistent cogs; frame 0 of each sheet is full-domain noise.
- Shell profile, isolated cogs (no other core within 40 px), t>=200: `radial_cog.py pack/seed<s>/frames.npz radial_seed<s>.png`.
  A1 = 1.00 at the centre, 0.00 at r=3 (the A0 ring), 0.91/0.94 at r=7/8 (shell band r~6-10), 0.000/0.0001 at r=25-29;
  A0 is 0.00 in the shell band. 32 cell-frames per seed; every cell shows the trough-shell-outside pattern.
- Fork (E): `runsave.py world.py pre<s> <s> 600`, `mkcut.py <s>` (most isolated cog, nearest other core 40-76 px),
  then `runsave.py world.py fed<s> <s> 300 cut_<s>.npz` and `CUT=1 runsave.py world.py cutrun<s> <s> 300 cut_<s>.npz`:
  food inside a disk of r=18 around the cog is moved out of the disk every step (kept in the ledger).
  `cutplot.py localcut.png 0 1 2 3` (localcut.json):
  | seed | cut cog matter at t=900 | same cog, fed twin | all other bodies, cut / fed | cut cog <10% at |
  |---|---|---|---|---|
  | 0 | 0.00 | 1.00 | 1.003 / 1.003 | t=655 |
  | 1 | 0.00 | 1.01 | 0.996 / 0.996 | t=655 |
  | 2 | 0.00 | 1.01 | 0.999 / 0.999 | t=655 |
  | 3 | 0.00 | 0.99 | 1.000 / 1.000 | t=650 |
  The cut cog loses ~10% of its matter over ~40 t (decay without rebuild), then collapses through its own
  negative growth within ~10 t (track_seed0.png, track_seed1.png).
- dt/2 (T=20), seed 0: `WORLD_P='{"T":20}'` for pre, fed and cut runs (controls/localcut_dthalf.png, dthalf_pre.png):
  cogs still form from noise (7 vs 15 at T=10); the cut cog is gone at t=650, the fed twin stays at 1.00.
- Food bill (`turnover.py 0 1 2 3`, turnover.json): matter built 0.0023-0.0025 per unit matter per t (decay 0.002
  plus a little), i.e. a cog rebuilds its whole mass from food every ~400-430 t.
- Shell-source ablation (B): k4 (core->shell set-point kernel) set to 0 on the mature t=600 states of seeds 0 and 1
  (`WORLD_P='{"k4":0}' runsave.py world.py abl_mat<s> <s> 100 pre<s>_ckpt.npz`, controls/ablation_k4_mature.png):
  the shell leaves its band and fills the domain as an A1 labyrinth within ~20 t (A1 total 3.9k->16.0k, 3.2k->16.0k),
  cores persist. From noise with k4=0 no cogs form (controls/abl_k4_s0.png, abl_k4_s1.png).

## Limits
- Dependence holds by construction (matter is buildable only from food and decays). What the forks add: the cog
  does not survive a ~10% deficit, so it dies ~50 t after a local cut although its stock would last ~400 t.
- Food is plentiful (mean F ~1.4); the cogs never deplete their surroundings, and they do not divide (no D).
- The local cut is a permanent food sink of r=18; neighbours are >=40 px away, so it does not reach them.
- The shell band (4-5 px at R=10) has not been re-run at 1.5x resolution in this world; lab 1's r-two56 survived R=15-20.
- labkit's own radial test reads A1 as not membrane-like (rim/core 1.27) because A1 is also high at the white centre;
  the trough-band profile above is the relevant test for this layered cell.
