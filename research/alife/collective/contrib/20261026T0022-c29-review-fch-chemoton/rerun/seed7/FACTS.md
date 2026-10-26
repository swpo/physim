# Evidence pack: fch-pchemoton (seed 7)

- world: `../../world.py`, family `fch-bilayer`
- parent: collective/contrib/20261025T0651-c02-fch-noise-sighting/world.py; mutation: add a fed precursor, a bilayer-gated Gray-Scott-like catalyst that makes amphiphile, and amphiphile decay
- run: 201 frames x 300 steps x dt 0.01 = time 600; grid [192, 192]; wall 472s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0022-c29-review-fch-chemoton/world.py --out collective/contrib/20261026T0022-c29-review-fch-chemoton/rerun/seed7 --seeds 7 --no-movie`
- segmentation: matter > 0.35 of robust range [-0.0204, 1.7288], min area 6 px

## Measurements
- components: final 5, mean 5.1, max 8; occupancy final 0.09
- tracks: 11; persistent (alive >= 50% of run): 5; longest 200 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 4.11 (1 = constant size)
- enclosures: components with a hole mean 2.81, final 3; holes at thresholds 0.2/0.35/0.5 final [4, 4, 3]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [13, 9, 7], H1 [4, 4, 3]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.6
- replication (lineage window K = 20 frames = time 60, default): splits 1, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 2, merge/split ratio 2, nucleations 6
- channel total drift (end/start - 1): [0.0018, 0.4456, -0.7977]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1 at frame 101: holes 1, rim-vs-core 0.19, rim-vs-outside 0.38, heterogeneity 0.06; core [0.834, 0.963, 0.0] rim [0.643, 0.962, 0.001]
  - track 3 at frame 101: holes 1, rim-vs-core 0.16, rim-vs-outside 0.46, heterogeneity 0.06; core [0.843, 0.904, 0.001] rim [0.684, 0.901, 0.002]
  - track 4 at frame 101: holes 0, rim-vs-core 0.39, rim-vs-outside 0.49, heterogeneity 0.19; core [0.872, 0.027, 0.684] rim [0.647, 0.063, 0.372]
  - track 9 at frame 106: holes 2, rim-vs-core 0.14, rim-vs-outside 0.61, heterogeneity 0.17; core [0.787, 0.076, 0.311] rim [0.696, 0.05, 0.411]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 30 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial amphiphile u+1: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.05, rim/outside 8.8 (aggregate of 30 individuals; 11/30 membrane-like individually; rim level 0.495)
  - radial precursor P: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.12, rim/outside 0.885 (aggregate of 30 individuals; 0/30 membrane-like individually; rim level 0.661)
  - radial catalyst K: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.836, rim/outside 2.89 (aggregate of 30 individuals; 5/30 membrane-like individually; rim level 0.0904)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #1 (t=303, R_eq 13.95, ring): ['amphiphile u+1']; #3 (t=303, R_eq 14.43, ring): ['amphiphile u+1']; #4 (t=303, R_eq 12.96): none; #9 (t=318, R_eq 18.71): ['catalyst K']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 13 of 30 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
