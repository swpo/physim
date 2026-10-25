# Evidence pack: fch-pchemoton-res15 (seed 31)

- world: `../../20261025T1048-c02-chemoton-res15/world_res15.py`, family `fch-bilayer`
- parent: collective/contrib/20261025T0651-c02-fch-noise-sighting/world.py; mutation: add a fed precursor, a bilayer-gated Gray-Scott-like catalyst that makes amphiphile, and amphiphile decay
- run: 201 frames x 600 steps x dt 0.005 = time 600; grid [288, 288]; wall 2605s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1048-c02-chemoton-res15/world_res15.py --out collective/contrib/20261025T1143-c10-review-chemoton-res15/res15_s31 --seeds 31 --frames 200 --no-movie`
- segmentation: matter > 0.32 of robust range [-0.022, 1.9043], min area 6 px

## Measurements
- components: final 5, mean 5.2, max 8; occupancy final 0.05
- tracks: 25; persistent (alive >= 50% of run): 6; longest 190 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 3.31 (1 = constant size)
- enclosures: components with a hole mean 1.60, final 2; holes at thresholds 0.2/0.35/0.5 final [2, 3, 2]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [7, 7, 6], H1 [3, 3, 2]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.8
- replication (lineage window K = 20 frames = time 60, default): splits 7, persistent splits 2 (0 more failed only because the siblings re-merged within K), max generation 1, merges 6, merge/split ratio 0.857, nucleations 4
- channel total drift (end/start - 1): [-0.5103, 0.8194, -0.9365]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 13 at frame 106: holes 1, rim-vs-core 0.21, rim-vs-outside 0.45, heterogeneity 0.05; core [0.929, 0.973, 0.0] rim [0.719, 0.973, 0.001]
  - track 16 at frame 108: holes 0, rim-vs-core 0.20, rim-vs-outside 0.62, heterogeneity 0.18; core [0.918, 0.02, 0.704] rim [0.731, 0.04, 0.627]
  - track 17 at frame 124: holes 0, rim-vs-core 0.17, rim-vs-outside 0.43, heterogeneity 0.05; core [0.888, 0.985, 0.0] rim [0.723, 0.984, 0.0]
  - track 18 at frame 124: holes 0, rim-vs-core 0.24, rim-vs-outside 0.16, heterogeneity 0.05; core [0.833, 0.986, 0.0] rim [0.596, 0.985, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 32 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial amphiphile u+1: peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.11, rim/outside 3.98 (aggregate of 32 individuals; 9/32 membrane-like individually; rim level 0.693)
  - radial precursor P: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.03, rim/outside 0.952 (aggregate of 32 individuals; 0/32 membrane-like individually; rim level 0.823)
  - radial catalyst K: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.66, rim/outside 2.88 (aggregate of 32 individuals; 4/32 membrane-like individually; rim level 0.101)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): catalyst K
- membrane-like channels per top track at mid-life: #13 (t=318, R_eq 18.12, ring): ['amphiphile u+1']; #16 (t=324, R_eq 19.99): ['catalyst K']; #17 (t=372, R_eq 22.13, ring): none; #18 (t=372, R_eq 8.06): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 17 of 32 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
