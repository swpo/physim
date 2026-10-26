# Evidence pack: sporecell2 (seed 5)

- world: `../world_nolysis.py`, family `particle`
- parent: sporecell-gene; gate forked from autopoiesis/fisim-beyond-laplacian (gated mobility); mutation: majority-vote conformity of core kind (in-cell mutants erased, spores are the genetic bottleneck); per-kind catalysis rate; food mobility gated by membrane density D_F exp(-beta nM); short B shell
- run: 201 frames x 50 steps x dt 0.02 = time 200; grid [128, 128]; wall 62s; status ok
- command: `python -m labkit.run collective/contrib/wip-c33-ly/world_nolysis.py --out collective/contrib/wip-c33-ly/pack_nolysis --seeds 5 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 0.2671], min area 6 px

## Measurements
- components: final 0, mean 3.7, max 14; occupancy final 0.00
- tracks: 165; persistent (alive >= 50% of run): 0; longest 75 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [30, 30, 27], H1 [0, 0, 0]
- motion: 9 long-lived tracks moved >= 1 body length; max speed 0.522/time; max body lengths 2.4
- replication (lineage window K = 20 frames = time 20, default): splits 4, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 1, merge/split ratio 0.25, nucleations 156
- channel total drift (end/start - 1): [-0.0043, -1.0, None, -1.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 15 at frame 49: holes 0, rim-vs-core 0.17, rim-vs-outside 0.18, heterogeneity 0.05; core [0.214, 0.0, 0.957, 0.0] rim [0.275, 0.0, 0.794, 0.0]
  - track 13 at frame 39: holes 0, rim-vs-core 0.23, rim-vs-outside 0.30, heterogeneity 0.07; core [0.141, 0.0, 0.968, 0.0] rim [0.323, 0.0, 0.824, 0.0]
  - track 12 at frame 30: holes 0, rim-vs-core 0.17, rim-vs-outside 0.36, heterogeneity 0.06; core [0.169, 0.0, 0.993, 0.0] rim [0.273, 0.0, 0.857, 0.0]
  - track 5 at frame 24: holes 0, rim-vs-core 0.12, rim-vs-outside 0.28, heterogeneity 0.07; core [0.319, 0.0, 0.977, 0.0] rim [0.31, 0.0, 0.857, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 16 components >= 12 px at frames [34, 67, 101]):
  - radial F food: peak at rho=1.95 (OUTSIDE the peak band 0.5-1.5), rim/core 2.95, rim/outside 0.8 (aggregate of 16 individuals; 1/16 membrane-like individually; rim level 0.337)
  - radial C0 core kind 0: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.727, rim/outside 7.62 (aggregate of 16 individuals; 0/16 membrane-like individually; rim level 0.0667)
  - radial M membrane: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.937, rim/outside 6.11 (aggregate of 16 individuals; 0/16 membrane-like individually; rim level 0.928)
  - radial C1 core kind 1: flat profile (no radial structure; level 0; aggregate of 16 individuals)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #15 (t=49, R_eq 3.7): none; #13 (t=39, R_eq 4.95): none; #12 (t=30, R_eq 4.62): none; #5 (t=24, R_eq 4.03): none

## Warnings
- no components at the end: matter died out or fell below threshold
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
