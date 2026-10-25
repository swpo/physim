# Evidence pack: membrane-evo (seed 31)

- world: `../../../../../threads/autopoiesis/worlds/membrane_evo/world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/membrane_kinds (arm E of committee r2); identical-event design from fisim-beyond-laplacian xcell-evo2-S; mutation: kinds differ only in link yield b2; sealed catalyst channel (min face gate, fast outside decay); whole-cell flips + neutral tag + random disk deaths from a state-independent RNG
- run: 161 frames x 250 steps x dt 1.0 = time 40000; grid [128, 128]; wall 132s; status ok
- command: `python -m labkit.run threads/autopoiesis/worlds/membrane_evo/world.py --out collective/contrib/20261025T1310-c16-review-membrane-evo/rerun/membrane_evo_s31 --seeds 31 --frames 160 --spf 250 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.3034], min area 6 px

## Measurements
- components: final 0, mean 0.2, max 7; occupancy final 0.00
- tracks: 7; persistent (alive >= 50% of run): 0; longest 34 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.01, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [0, 0, 0], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.4
- replication (lineage window K = 20 frames = time 5000, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio n/a, nucleations 0
- channel total drift (end/start - 1): [-1.0, None, -1.0, -1.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 2 at frame 16: holes 0, rim-vs-core 0.33, rim-vs-outside 0.67, heterogeneity 0.08; core [0.333, 0.0, 1.0, 1.0] rim [0.0, 0.0, 1.0, 1.0]
  - track 0 at frame 0: holes 0, rim-vs-core 0.08, rim-vs-outside 0.76, heterogeneity 0.20; core [0.729, 0.0, 0.709, 1.0] rim [0.79, 0.0, 0.75, 0.964]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 1 components >= 12 px at frames [27]):
  - radial K1: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.01, rim/outside 1 (aggregate of 1 individuals; 0/1 membrane-like individually; rim level 0)
  - radial K2: flat profile (no radial structure; level 0; aggregate of 1 individuals)
  - radial L link: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 1, rim/outside 97.7 (aggregate of 1 individuals; 0/1 membrane-like individually; rim level 1)
  - radial membrane (wall): peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 1, rim/outside 1.07 (aggregate of 1 individuals; 0/1 membrane-like individually; rim level 1)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #2 (t=4000, R_eq 2.26): none; #0 (t=0, R_eq 7.14): none; #1 (t=0, R_eq 42.73, ring): none; #3 (t=0, R_eq 1.49): none

## Warnings
- no components at the end: matter died out or fell below threshold
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
