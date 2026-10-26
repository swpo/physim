# Evidence pack: sporecell2-nolysis (seed 5)

- world: `../../world_lysis.py`, family `particle`
- parent: sporecell-gene; gate forked from autopoiesis/fisim-beyond-laplacian (gated mobility); mutation: majority-vote conformity of core kind (in-cell mutants erased, spores are the genetic bottleneck); per-kind catalysis rate; food mobility gated by membrane density D_F exp(-beta nM); short B shell
- run: 301 frames x 50 steps x dt 0.02 = time 300; grid [128, 128]; wall 98s; status ok
- command: `python -m labkit.run collective/contrib/20261026T1010-c38-review-sporecell2/world_lysis.py --out collective/contrib/20261026T1010-c38-review-sporecell2/rerun/nolysis_seed5 --seeds 5 --frames 300 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 0.2521], min area 6 px

## Measurements
- components: final 0, mean 2.7, max 14; occupancy final 0.00
- tracks: 205; persistent (alive >= 50% of run): 0; longest 75 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [7, 7, 7], H1 [0, 0, 0]
- motion: 7 long-lived tracks moved >= 1 body length; max speed 0.473/time; max body lengths 2.6
- replication (lineage window K = 20 frames = time 20, default): splits 5, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 4, merge/split ratio 0.8, nucleations 191
- channel total drift (end/start - 1): [0.002, -1.0, None, -1.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 17 at frame 50: holes 0, rim-vs-core 0.13, rim-vs-outside 0.31, heterogeneity 0.05; core [0.198, 0.0, 1.0, 0.0] rim [0.313, 0.0, 0.933, 0.0]
  - track 15 at frame 38: holes 0, rim-vs-core 0.15, rim-vs-outside 0.29, heterogeneity 0.06; core [0.217, 0.0, 0.999, 0.0] rim [0.338, 0.0, 0.914, 0.0]
  - track 14 at frame 30: holes 0, rim-vs-core 0.12, rim-vs-outside 0.37, heterogeneity 0.05; core [0.171, 0.0, 0.997, 0.0] rim [0.268, 0.0, 0.927, 0.0]
  - track 170 at frame 108: holes 0, rim-vs-core 0.16, rim-vs-outside 0.56, heterogeneity 0.07; core [0.059, 1.0, 1.0, 1.0] rim [0.184, 1.0, 0.917, 0.949]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 6 components >= 12 px at frames [50, 101]):
  - radial F food: peak at rho=1.95 (OUTSIDE the peak band 0.5-1.5), rim/core 3.05, rim/outside 0.777 (aggregate of 6 individuals; 0/6 membrane-like individually; rim level 0.309)
  - radial C0 core kind 0: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.658, rim/outside 12.4 (aggregate of 6 individuals; 0/6 membrane-like individually; rim level 0.167)
  - radial M membrane: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.979, rim/outside 5.18 (aggregate of 6 individuals; 0/6 membrane-like individually; rim level 0.973)
  - radial C1 core kind 1: flat profile (no radial structure; level 0; aggregate of 6 individuals)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #17 (t=50, R_eq 4.03): none; #15 (t=38, R_eq 4.98): none; #14 (t=30, R_eq 4.75): none; #170 (t=108, R_eq 5.05): none

## Warnings
- no components at the end: matter died out or fell below threshold
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
