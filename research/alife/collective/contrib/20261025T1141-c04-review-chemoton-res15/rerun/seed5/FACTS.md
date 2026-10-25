# Evidence pack: fch-pchemoton-res15 (seed 5)

- world: `../../../../../../../home/user/physim/research/alife/collective/contrib/20261025T1048-c02-chemoton-res15/world_res15.py`, family `fch-bilayer`
- parent: collective/contrib/20261025T0651-c02-fch-noise-sighting/world.py; mutation: add a fed precursor, a bilayer-gated Gray-Scott-like catalyst that makes amphiphile, and amphiphile decay
- run: 101 frames x 600 steps x dt 0.005 = time 300; grid [288, 288]; wall 932s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1048-c02-chemoton-res15/world_res15.py --out /tmp/claude-0/-home-user-physim/fba552f4-82e1-5fd3-8aee-1d1a9784fecc/scratchpad/rev15/r15 --seeds 5 --frames 100 --no-movie`
- segmentation: matter > 0.31 of robust range [-0.0203, 1.9764], min area 6 px

## Measurements
- components: final 5, mean 3.8, max 7; occupancy final 0.10
- tracks: 22; persistent (alive >= 50% of run): 2; longest 90 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.04 (1 = constant size)
- enclosures: components with a hole mean 2.39, final 2; holes at thresholds 0.2/0.35/0.5 final [5, 5, 1]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [8, 7, 4], H1 [7, 7, 3]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.1
- replication (lineage window K = 20 frames = time 60, default): splits 6, persistent splits 2 (0 more failed only because the siblings re-merged within K), max generation 1, merges 4, merge/split ratio 0.667, nucleations 3
- channel total drift (end/start - 1): [0.0892, 0.3727, -0.77]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 14 at frame 56: holes 4, rim-vs-core 0.16, rim-vs-outside 0.53, heterogeneity 0.16; core [0.783, 0.05, 0.504] rim [0.647, 0.062, 0.414]
  - track 13 at frame 43: holes 4, rim-vs-core 0.10, rim-vs-outside 0.43, heterogeneity 0.04; core [0.746, 0.991, 0.0] rim [0.646, 0.991, 0.0]
  - track 17 at frame 35: holes 6, rim-vs-core 0.30, rim-vs-outside 0.56, heterogeneity 0.22; core [0.6, 0.04, 0.458] rim [0.633, 0.279, 0.275]
  - track 18 at frame 79: holes 0, rim-vs-core 0.29, rim-vs-outside 0.55, heterogeneity 0.15; core [0.79, 0.022, 0.758] rim [0.649, 0.053, 0.502]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 23 components >= 12 px at frames [17, 33, 50, 67, 83, 100]):
  - radial amphiphile u+1: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1.02, rim/outside 4.35 (aggregate of 23 individuals; 3/23 membrane-like individually; rim level 0.563)
  - radial precursor P: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.23, rim/outside 0.759 (aggregate of 23 individuals; 0/23 membrane-like individually; rim level 0.481)
  - radial catalyst K: peak at rho=1.15 (in the peak band 0.5-1.5), rim/core 2.04, rim/outside 2.58 (aggregate of 23 individuals; 8/23 membrane-like individually; rim level 0.213)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): catalyst K
- membrane-like channels per top track at mid-life: #14 (t=168, R_eq 29.98): ['catalyst K']; #13 (t=129, R_eq 31.94): none; #17 (t=105, R_eq 38.46): none; #18 (t=237, R_eq 28.91, ring): ['amphiphile u+1', 'catalyst K']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 9 of 23 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
