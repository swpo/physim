# Evidence pack: fch-pchemoton-clip (seed 24)

- world: `../../../20261025T1817-c17-chemoton-honest-decay/world_clip.py`, family `fch-bilayer`
- parent: collective/contrib/20261025T0651-c02-fch-noise-sighting/world.py; mutation: add a fed precursor, a bilayer-gated Gray-Scott-like catalyst that makes amphiphile, and amphiphile decay
- run: 201 frames x 300 steps x dt 0.01 = time 600; grid [192, 192]; wall 675s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1817-c17-chemoton-honest-decay/world_clip.py --out collective/contrib/20261025T2019-c24-review-honest-decay/fed_clip/seed24 --seeds 24 --frames 200 --no-movie`
- segmentation: matter > 0.31 of robust range [-0.0207, 1.9534], min area 6 px

## Measurements
- components: final 5, mean 4.3, max 5; occupancy final 0.08
- tracks: 10; persistent (alive >= 50% of run): 5; longest 200 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 3.97 (1 = constant size)
- enclosures: components with a hole mean 1.14, final 1; holes at thresholds 0.2/0.35/0.5 final [1, 1, 1]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [7, 6, 3], H1 [3, 3, 1]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.4
- replication (lineage window K = 20 frames = time 60, default): splits 3, persistent splits 2 (0 more failed only because the siblings re-merged within K), max generation 1, merges 1, merge/split ratio 0.333, nucleations 3
- channel total drift (end/start - 1): [-0.2372, 0.5013, -0.8193]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 101: holes 0, rim-vs-core 0.33, rim-vs-outside 0.60, heterogeneity 0.18; core [0.946, 0.011, 0.757] rim [0.715, 0.038, 0.523]
  - track 6 at frame 134: holes 0, rim-vs-core 0.17, rim-vs-outside 0.42, heterogeneity 0.07; core [0.86, 0.855, 0.002] rim [0.689, 0.855, 0.004]
  - track 7 at frame 134: holes 0, rim-vs-core 0.28, rim-vs-outside 0.10, heterogeneity 0.06; core [0.779, 0.871, 0.0] rim [0.504, 0.869, 0.0]
  - track 8 at frame 143: holes 0, rim-vs-core 0.28, rim-vs-outside 0.60, heterogeneity 0.15; core [0.846, 0.009, 0.757] rim [0.697, 0.034, 0.525]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 26 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial amphiphile u+1: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.901, rim/outside 2.48 (aggregate of 26 individuals; 5/26 membrane-like individually; rim level 0.562)
  - radial precursor P: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.04, rim/outside 0.823 (aggregate of 26 individuals; 0/26 membrane-like individually; rim level 0.458)
  - radial catalyst K: peak at rho=1.15 (in the peak band 0.5-1.5), rim/core 1.51, rim/outside 1.8 (aggregate of 26 individuals; 7/26 membrane-like individually; rim level 0.209)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): catalyst K
- membrane-like channels per top track at mid-life: #0 (t=303, R_eq 11.38): none; #6 (t=402, R_eq 15.29, ring): none; #7 (t=402, R_eq 5.7): none; #8 (t=429, R_eq 19.27, ring): ['amphiphile u+1', 'catalyst K']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 14 of 26 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
