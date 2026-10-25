# Evidence pack: fch-pchemoton-kablate (seed 0)

- world: `../../world_kablate.py`, family `fch-bilayer`
- parent: collective/contrib/20261025T0651-c02-fch-noise-sighting/world.py; mutation: add a fed precursor, a bilayer-gated Gray-Scott-like catalyst that makes amphiphile, and amphiphile decay
- run: 201 frames x 300 steps x dt 0.01 = time 600; grid [192, 192]; wall 371s; status ok
- command: `python -m labkit.run collective/contrib/c17-chemoton-wip/world_kablate.py --out collective/contrib/c17-chemoton-wip/rerun_kablate_small/seed0 --seeds 0 --no-movie`
- segmentation: matter > 0.32 of robust range [-0.0203, 1.8952], min area 6 px

## Measurements
- components: final 3, mean 3.1, max 6; occupancy final 0.08
- tracks: 10; persistent (alive >= 50% of run): 3; longest 200 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 3.37 (1 = constant size)
- enclosures: components with a hole mean 2.78, final 3; holes at thresholds 0.2/0.35/0.5 final [2, 4, 3]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [4, 4, 3], H1 [8, 4, 3]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.6
- replication (lineage window K = 20 frames = time 60, default): splits 1, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 3, merge/split ratio 3, nucleations 4
- channel total drift (end/start - 1): [-0.2205, 0.6094, -0.8596]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 101: holes 1, rim-vs-core 0.21, rim-vs-outside 0.44, heterogeneity 0.06; core [0.927, 0.897, 0.001] rim [0.715, 0.891, 0.002]
  - track 3 at frame 101: holes 1, rim-vs-core 0.15, rim-vs-outside 0.49, heterogeneity 0.07; core [0.887, 0.289, 0.0] rim [0.739, 0.299, 0.001]
  - track 9 at frame 109: holes 4, rim-vs-core 0.33, rim-vs-outside 0.55, heterogeneity 0.17; core [0.611, 0.152, 0.023] rim [0.696, 0.08, 0.33]
  - track 1 at frame 8: holes 0, rim-vs-core 0.18, rim-vs-outside 0.59, heterogeneity 0.06; core [1.0, 0.131, 0.149] rim [0.821, 0.133, 0.148]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 18 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial amphiphile u+1: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 2.21, rim/outside 15.5 (aggregate of 18 individuals; 11/18 membrane-like individually; rim level 0.762)  MEMBRANE-LIKE
  - radial precursor P: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.15, rim/outside 0.847 (aggregate of 18 individuals; 0/18 membrane-like individually; rim level 0.633)
  - radial catalyst K: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.88, rim/outside 4.44 (aggregate of 18 individuals; 4/18 membrane-like individually; rim level 0.133)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): amphiphile u+1, catalyst K
- membrane-like channels per top track at mid-life: #0 (t=303, R_eq 12.91, ring): ['amphiphile u+1']; #3 (t=303, R_eq 15.47, ring): ['amphiphile u+1']; #9 (t=327, R_eq 28.2): ['catalyst K']; #1 (t=24, R_eq 14.64): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 12 of 18 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
