# Evidence pack: fch-pchemoton (seed 21)

- world: `../../../20261025T0848-c02-fch-chemoton-claim/world.py`, family `fch-bilayer`
- parent: collective/contrib/20261025T0651-c02-fch-noise-sighting/world.py; mutation: add a fed precursor, a bilayer-gated Gray-Scott-like catalyst that makes amphiphile, and amphiphile decay
- run: 201 frames x 300 steps x dt 0.01 = time 600; grid [192, 192]; wall 345s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0848-c02-fch-chemoton-claim/world.py --out collective/contrib/_c26work/rev5/rerun --seeds 21 --frames 200 --no-movie`
- segmentation: matter > 0.32 of robust range [-0.0206, 1.9419], min area 6 px

## Measurements
- components: final 5, mean 4.7, max 6; occupancy final 0.06
- tracks: 19; persistent (alive >= 50% of run): 5; longest 200 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 6.48 (1 = constant size)
- enclosures: components with a hole mean 1.32, final 1; holes at thresholds 0.2/0.35/0.5 final [1, 1, 1]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [10, 8, 4], H1 [2, 2, 1]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.6
- replication (lineage window K = 20 frames = time 60, default): splits 5, persistent splits 1 (0 more failed only because the siblings re-merged within K), max generation 1, merges 4, merge/split ratio 0.8, nucleations 4
- channel total drift (end/start - 1): [-0.4391, 0.7314, -0.9041]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 101: holes 0, rim-vs-core 0.30, rim-vs-outside 0.57, heterogeneity 0.18; core [0.874, 0.01, 0.773] rim [0.656, 0.034, 0.568]
  - track 12 at frame 108: holes 1, rim-vs-core 0.18, rim-vs-outside 0.42, heterogeneity 0.05; core [0.863, 0.975, 0.0] rim [0.681, 0.976, 0.0]
  - track 13 at frame 108: holes 0, rim-vs-core 0.29, rim-vs-outside 0.30, heterogeneity 0.06; core [0.896, 0.979, 0.0] rim [0.605, 0.979, 0.001]
  - track 17 at frame 131: holes 0, rim-vs-core 0.16, rim-vs-outside 0.41, heterogeneity 0.04; core [0.834, 0.993, 0.0] rim [0.673, 0.992, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 29 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial amphiphile u+1: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 1.01, rim/outside 3.94 (aggregate of 29 individuals; 7/29 membrane-like individually; rim level 0.567)
  - radial precursor P: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.05, rim/outside 0.956 (aggregate of 29 individuals; 0/29 membrane-like individually; rim level 0.819)
  - radial catalyst K: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.2, rim/outside 2.22 (aggregate of 29 individuals; 5/29 membrane-like individually; rim level 0.0769)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=303, R_eq 13.4): ['catalyst K']; #12 (t=324, R_eq 12.68, ring): ['amphiphile u+1']; #13 (t=324, R_eq 8.12): none; #17 (t=393, R_eq 15.12, ring): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 12 of 29 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
