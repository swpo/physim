# Evidence pack: fch-pchemoton-kablate (seed 0)

- world: `../../world_kablate.py`, family `fch-bilayer`
- parent: collective/contrib/20261025T0651-c02-fch-noise-sighting/world.py; mutation: add a fed precursor, a bilayer-gated Gray-Scott-like catalyst that makes amphiphile, and amphiphile decay
- run: 201 frames x 300 steps x dt 0.01 = time 600; grid [192, 192]; wall 371s; status ok
- command: `python -m labkit.run collective/contrib/c17-chemoton-wip/world_kablate.py --out collective/contrib/c17-chemoton-wip/rerun_kablate_big/seed0 --seeds 0 --no-movie`
- segmentation: matter > 0.32 of robust range [-0.0208, 1.8952], min area 6 px

## Measurements
- components: final 4, mean 3.3, max 6; occupancy final 0.06
- tracks: 15; persistent (alive >= 50% of run): 3; longest 200 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 3.37 (1 = constant size)
- enclosures: components with a hole mean 2.59, final 2; holes at thresholds 0.2/0.35/0.5 final [2, 2, 2]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [7, 5, 3], H1 [3, 3, 2]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.8
- replication (lineage window K = 20 frames = time 60, default): splits 3, persistent splits 2 (0 more failed only because the siblings re-merged within K), max generation 2, merges 4, merge/split ratio 1.33, nucleations 4
- channel total drift (end/start - 1): [-0.4369, 0.7208, -0.8985]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 101: holes 1, rim-vs-core 0.21, rim-vs-outside 0.43, heterogeneity 0.06; core [0.908, 0.887, 0.001] rim [0.699, 0.881, 0.002]
  - track 3 at frame 101: holes 1, rim-vs-core 0.18, rim-vs-outside 0.60, heterogeneity 0.18; core [0.876, 0.035, 0.537] rim [0.725, 0.042, 0.442]
  - track 9 at frame 77: holes 6, rim-vs-core 0.16, rim-vs-outside 0.53, heterogeneity 0.20; core [0.664, 0.053, 0.169] rim [0.683, 0.173, 0.272]
  - track 13 at frame 188: holes 0, rim-vs-core 0.18, rim-vs-outside 0.43, heterogeneity 0.06; core [0.885, 0.926, 0.001] rim [0.708, 0.926, 0.002]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 20 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial amphiphile u+1: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.71, rim/outside 6.27 (aggregate of 20 individuals; 11/20 membrane-like individually; rim level 0.716)  MEMBRANE-LIKE
  - radial precursor P: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.16, rim/outside 0.898 (aggregate of 20 individuals; 0/20 membrane-like individually; rim level 0.668)
  - radial catalyst K: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.73, rim/outside 4.09 (aggregate of 20 individuals; 4/20 membrane-like individually; rim level 0.16)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): amphiphile u+1, catalyst K
- membrane-like channels per top track at mid-life: #0 (t=303, R_eq 12.91, ring): ['amphiphile u+1']; #3 (t=303, R_eq 15.54, ring): ['amphiphile u+1', 'catalyst K']; #9 (t=231, R_eq 28.56): ['catalyst K']; #13 (t=564, R_eq 15.44, ring): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 15 of 20 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
