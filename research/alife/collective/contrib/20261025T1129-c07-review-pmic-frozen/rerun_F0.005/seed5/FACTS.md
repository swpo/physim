# Evidence pack: pmic-F0.005 (seed 5)

- world: `../../world_F005.py`, family `hybrid-particle-field`
- parent: collective/contrib/20261025T0752-c03-fch-cargo-fission/world.py; mutation: uniform amphiphile feed -> local synthesis by gated catalyst particles from a fed precursor, plus amphiphile decay
- run: 201 frames x 250 steps x dt 0.02 = time 1000; grid [128, 128]; wall 400s; status ok
- command: `python -m labkit.run collective/contrib/_c07rev21/world_F005.py --out collective/contrib/_c07rev21/rerun_F0.005/seed5 --seeds 5 --frames 200 --no-movie`
- segmentation: matter > 0.13 of robust range [0.122, 2.9857], min area 6 px

## Measurements
- components: final 66, mean 62.7, max 66; occupancy final 0.31
- tracks: 120; persistent (alive >= 50% of run): 66; longest 200 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.34 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [66, 66, 66], H1 [0, 0, 0]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 0.00937/time; max body lengths 1.0
- replication (lineage window K = 20 frames = time 100, default): splits 46, persistent splits 20 (0 more failed only because the siblings re-merged within K), max generation 3, merges 3, merge/split ratio 0.065, nucleations 20
- channel total drift (end/start - 1): [0.8117, -0.2918, -0.6435]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 5 at frame 101: holes 0, rim-vs-core 0.59, rim-vs-outside 0.14, heterogeneity 0.18; core [0.628, 0.507, 0.037] rim [0.177, 0.122, 0.049]
  - track 7 at frame 101: holes 0, rim-vs-core 0.58, rim-vs-outside 0.11, heterogeneity 0.19; core [0.608, 0.434, 0.023] rim [0.159, 0.073, 0.04]
  - track 9 at frame 101: holes 0, rim-vs-core 0.57, rim-vs-outside 0.14, heterogeneity 0.18; core [0.632, 0.46, 0.022] rim [0.183, 0.116, 0.035]
  - track 110 at frame 114: holes 0, rim-vs-core 0.59, rim-vs-outside 0.12, heterogeneity 0.19; core [0.613, 0.474, 0.019] rim [0.166, 0.091, 0.029]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 394 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial amphiphile u (u + 1.6): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.502, rim/outside 9.84 (aggregate of 394 individuals; 0/394 membrane-like individually; rim level 0.474)
  - radial K particles: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.414, rim/outside 9.73 (aggregate of 394 individuals; 0/394 membrane-like individually; rim level 0.341)
  - radial precursor S: peak at rho=1.85 (OUTSIDE the peak band 0.5-1.5), rim/core 1.57, rim/outside 0.958 (aggregate of 394 individuals; 0/394 membrane-like individually; rim level 0.0778)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #5 (t=505, R_eq 4.98): none; #7 (t=505, R_eq 5.05): none; #9 (t=505, R_eq 4.95): none; #110 (t=570, R_eq 4.98): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
