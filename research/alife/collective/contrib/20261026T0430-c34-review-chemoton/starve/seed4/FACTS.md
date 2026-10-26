# Evidence pack: fch-pchemoton-starve (seed 4)

- world: `../../../20261025T0848-c02-fch-chemoton-claim/world_starve.py`, family `fch-bilayer`
- parent: collective/contrib/20261025T0651-c02-fch-noise-sighting/world.py; mutation: add a fed precursor, a bilayer-gated Gray-Scott-like catalyst that makes amphiphile, and amphiphile decay
- run: 201 frames x 300 steps x dt 0.01 = time 600; grid [192, 192]; wall 398s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0848-c02-fch-chemoton-claim/world_starve.py --out collective/contrib/20261026T0430-c34-review-chemoton/starve/seed4 --seeds 4 --no-movie`
- segmentation: matter > 0.34 of robust range [-0.0251, 1.8384], min area 6 px

## Measurements
- components: final 4, mean 4.2, max 9; occupancy final 0.02
- tracks: 17; persistent (alive >= 50% of run): 4; longest 200 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 9.07 (1 = constant size)
- enclosures: components with a hole mean 1.61, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [10, 10, 4], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.6
- replication (lineage window K = 20 frames = time 60, default): splits 3, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 4, merge/split ratio 1.33, nucleations 5
- channel total drift (end/start - 1): [-0.9125, -0.0008, -0.9852]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 101: holes 0, rim-vs-core 0.29, rim-vs-outside 0.60, heterogeneity 0.16; core [0.914, 0.001, 0.904] rim [0.696, 0.011, 0.709]
  - track 1 at frame 101: holes 0, rim-vs-core 0.29, rim-vs-outside 0.31, heterogeneity 0.06; core [0.913, 0.968, 0.001] rim [0.621, 0.967, 0.002]
  - track 13 at frame 106: holes 1, rim-vs-core 0.20, rim-vs-outside 0.40, heterogeneity 0.05; core [0.877, 0.962, 0.0] rim [0.676, 0.961, 0.001]
  - track 12 at frame 64: holes 3, rim-vs-core 0.08, rim-vs-outside 0.47, heterogeneity 0.05; core [0.782, 0.995, 0.0] rim [0.698, 0.997, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 25 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial amphiphile u+1: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.07, rim/outside 8.08 (aggregate of 25 individuals; 5/25 membrane-like individually; rim level 0.624)
  - radial precursor P: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.06, rim/outside 0.949 (aggregate of 25 individuals; 0/25 membrane-like individually; rim level 0.653)
  - radial catalyst K: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.964, rim/outside 2.92 (aggregate of 25 individuals; 3/25 membrane-like individually; rim level 0.0912)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=303, R_eq 12.93): none; #1 (t=303, R_eq 8.04): none; #13 (t=318, R_eq 12.15, ring): ['amphiphile u+1']; #12 (t=192, R_eq 21.94): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 7 of 25 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
