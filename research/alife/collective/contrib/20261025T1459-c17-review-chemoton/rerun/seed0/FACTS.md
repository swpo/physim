# Evidence pack: fch-pchemoton (seed 0)

- world: `../../world.py`, family `fch-bilayer`
- parent: collective/contrib/20261025T0651-c02-fch-noise-sighting/world.py; mutation: add a fed precursor, a bilayer-gated Gray-Scott-like catalyst that makes amphiphile, and amphiphile decay
- run: 201 frames x 300 steps x dt 0.01 = time 600; grid [192, 192]; wall 365s; status ok
- command: `python -m labkit.run collective/contrib/c17-chemoton-wip/world.py --out collective/contrib/c17-chemoton-wip/rerun/seed0 --seeds 0 --no-movie`
- segmentation: matter > 0.32 of robust range [-0.0203, 1.8952], min area 6 px

## Measurements
- components: final 4, mean 3.3, max 6; occupancy final 0.11
- tracks: 12; persistent (alive >= 50% of run): 3; longest 200 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 3.37 (1 = constant size)
- enclosures: components with a hole mean 2.78, final 3; holes at thresholds 0.2/0.35/0.5 final [2, 4, 2]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [7, 5, 3], H1 [5, 3, 2]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.7
- replication (lineage window K = 20 frames = time 60, default): splits 2, persistent splits 1 (0 more failed only because the siblings re-merged within K), max generation 1, merges 3, merge/split ratio 1.5, nucleations 4
- channel total drift (end/start - 1): [0.0848, 0.3413, -0.758]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 101: holes 1, rim-vs-core 0.21, rim-vs-outside 0.43, heterogeneity 0.06; core [0.909, 0.909, 0.001] rim [0.7, 0.903, 0.002]
  - track 3 at frame 101: holes 1, rim-vs-core 0.19, rim-vs-outside 0.58, heterogeneity 0.18; core [0.876, 0.044, 0.509] rim [0.725, 0.053, 0.401]
  - track 9 at frame 87: holes 5, rim-vs-core 0.23, rim-vs-outside 0.53, heterogeneity 0.17; core [0.614, 0.124, 0.056] rim [0.686, 0.115, 0.275]
  - track 10 at frame 180: holes 0, rim-vs-core 0.24, rim-vs-outside 0.56, heterogeneity 0.15; core [0.823, 0.083, 0.24] rim [0.707, 0.047, 0.449]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 20 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial amphiphile u+1: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.98, rim/outside 8.58 (aggregate of 20 individuals; 11/20 membrane-like individually; rim level 0.717)  MEMBRANE-LIKE
  - radial precursor P: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.18, rim/outside 0.766 (aggregate of 20 individuals; 0/20 membrane-like individually; rim level 0.457)
  - radial catalyst K: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 2.2, rim/outside 3.02 (aggregate of 20 individuals; 8/20 membrane-like individually; rim level 0.183)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): amphiphile u+1, catalyst K
- membrane-like channels per top track at mid-life: #0 (t=303, R_eq 12.93, ring): ['amphiphile u+1']; #3 (t=303, R_eq 15.58, ring): ['amphiphile u+1', 'catalyst K']; #9 (t=261, R_eq 28.43): ['catalyst K']; #10 (t=540, R_eq 22.33, ring): ['catalyst K']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 14 of 20 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
