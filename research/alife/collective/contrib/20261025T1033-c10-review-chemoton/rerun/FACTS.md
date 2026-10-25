# Evidence pack: fch-pchemoton (seed 31)

- world: `../../20261025T0848-c02-fch-chemoton-claim/world.py`, family `fch-bilayer`
- parent: collective/contrib/20261025T0651-c02-fch-noise-sighting/world.py; mutation: add a fed precursor, a bilayer-gated Gray-Scott-like catalyst that makes amphiphile, and amphiphile decay
- run: 201 frames x 300 steps x dt 0.01 = time 600; grid [192, 192]; wall 483s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0848-c02-fch-chemoton-claim/world.py --out collective/contrib/20261025T1033-c10-review-chemoton/rerun --seeds 31 --frames 200 --no-movie`
- segmentation: matter > 0.32 of robust range [-0.0201, 1.9326], min area 6 px

## Measurements
- components: final 5, mean 4.5, max 5; occupancy final 0.12
- tracks: 6; persistent (alive >= 50% of run): 4; longest 200 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 5.01 (1 = constant size)
- enclosures: components with a hole mean 3.19, final 3; holes at thresholds 0.2/0.35/0.5 final [10, 10, 1]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [11, 7, 4], H1 [11, 11, 3]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.7
- replication (lineage window K = 20 frames = time 60, default): splits 1, persistent splits 1 (0 more failed only because the siblings re-merged within K), max generation 1, merges 0, merge/split ratio 0, nucleations 4
- channel total drift (end/start - 1): [0.319, 0.1722, -0.6956]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1 at frame 101: holes 1, rim-vs-core 0.27, rim-vs-outside 0.60, heterogeneity 0.17; core [0.9, 0.034, 0.602] rim [0.736, 0.058, 0.386]
  - track 2 at frame 101: holes 4, rim-vs-core 0.22, rim-vs-outside 0.55, heterogeneity 0.16; core [0.859, 0.102, 0.151] rim [0.723, 0.077, 0.326]
  - track 3 at frame 101: holes 5, rim-vs-core 0.20, rim-vs-outside 0.52, heterogeneity 0.16; core [0.868, 0.066, 0.421] rim [0.704, 0.078, 0.307]
  - track 4 at frame 153: holes 0, rim-vs-core 0.17, rim-vs-outside 0.44, heterogeneity 0.06; core [0.89, 0.924, 0.001] rim [0.719, 0.925, 0.002]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 27 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial amphiphile u+1: peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.1, rim/outside 8.22 (aggregate of 27 individuals; 5/27 membrane-like individually; rim level 0.656)
  - radial precursor P: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.31, rim/outside 0.73 (aggregate of 27 individuals; 0/27 membrane-like individually; rim level 0.494)
  - radial catalyst K: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 2.56, rim/outside 7.26 (aggregate of 27 individuals; 15/27 membrane-like individually; rim level 0.202)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): catalyst K
- membrane-like channels per top track at mid-life: #1 (t=303, R_eq 15.09, ring): ['amphiphile u+1', 'catalyst K']; #2 (t=303, R_eq 20.09): ['catalyst K']; #3 (t=303, R_eq 21.06): ['catalyst K']; #4 (t=459, R_eq 15.34, ring): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 8 of 27 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
