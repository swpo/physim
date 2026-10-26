# Evidence pack: sporecell2 (seed 5)

- world: `../world_lysis.py`, family `particle`
- parent: sporecell-gene; gate forked from autopoiesis/fisim-beyond-laplacian (gated mobility); mutation: majority-vote conformity of core kind (in-cell mutants erased, spores are the genetic bottleneck); per-kind catalysis rate; food mobility gated by membrane density D_F exp(-beta nM); short B shell
- run: 201 frames x 50 steps x dt 0.02 = time 200; grid [128, 128]; wall 63s; status ok
- command: `python -m labkit.run collective/contrib/wip-c33-ly/world_lysis.py --out collective/contrib/wip-c33-ly/pack_lysis --seeds 5 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 0.9842], min area 6 px

## Measurements
- components: final 2, mean 2.9, max 5; occupancy final 0.01
- tracks: 37; persistent (alive >= 50% of run): 2; longest 149 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 20.71 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [2, 2, 1], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 1.0
- replication (lineage window K = 20 frames = time 20, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 1, merge/split ratio n/a, nucleations 36
- channel total drift (end/start - 1): [-0.0321, -1.0, None, 4.7778]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 28 at frame 126: holes 0, rim-vs-core 0.01, rim-vs-outside 0.45, heterogeneity 0.02; core [0.0, 0.0, 0.98, 1.0] rim [0.009, 0.0, 0.972, 0.992]
  - track 5 at frame 66: holes 0, rim-vs-core 0.09, rim-vs-outside 0.40, heterogeneity 0.03; core [0.002, 1.0, 0.991, 0.0] rim [0.064, 1.0, 0.922, 0.0]
  - track 14 at frame 72: holes 0, rim-vs-core 0.22, rim-vs-outside 0.39, heterogeneity 0.06; core [0.0, 0.0, 1.0, 0.979] rim [0.0, 0.0, 0.991, 0.757]
  - track 31 at frame 161: holes 0, rim-vs-core 0.07, rim-vs-outside 0.54, heterogeneity 0.03; core [0.001, 0.0, 1.0, 1.0] rim [0.024, 0.0, 0.935, 0.977]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 17 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial F food: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 17.3, rim/outside 0.453 (aggregate of 17 individuals; 0/17 membrane-like individually; rim level 0.179)
  - radial C0 core kind 0: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.973, rim/outside 5.59 (aggregate of 17 individuals; 0/17 membrane-like individually; rim level 0.398)
  - radial M membrane: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.03, rim/outside 9.8 (aggregate of 17 individuals; 0/17 membrane-like individually; rim level 0.988)
  - radial C1 core kind 1: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.981, rim/outside 27.3 (aggregate of 17 individuals; 0/17 membrane-like individually; rim level 0.756)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #28 (t=126, R_eq 3.7): none; #5 (t=66, R_eq 4.37): none; #14 (t=72, R_eq 3.09): none; #31 (t=161, R_eq 4.37): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
