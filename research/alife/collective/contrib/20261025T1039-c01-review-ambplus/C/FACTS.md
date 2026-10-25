# Evidence pack: ambplus-ab (seed 3)

- world: `../../20261025T0811-c08-ambplus-reaction-morphology/world.py`, family `active-emulsion`
- parent: None; mutation: reference: Active Model B+ (zeta, lambda) with an optional Model-A birth/death reaction
- run: 101 frames x 1000 steps x dt 0.03 = time 3000; grid [128, 128]; wall 271s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0811-c08-ambplus-reaction-morphology/world.py --out collective/contrib/20261025T1039-c01-review-ambplus/C --seeds 3 --frames 100 --no-movie`
- segmentation: matter > 0.54 of robust range [-0.8898, 0.7635], min area 6 px

## Measurements
- components: final 2, mean 6.0, max 33; occupancy final 0.36
- tracks: 66; persistent (alive >= 50% of run): 0; longest 40 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.54, final 1; holes at thresholds 0.2/0.35/0.5 final [3, 2, 2]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [14, 2, 2], H1 [9, 2, 2]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.7
- replication (lineage window K = 20 frames = time 600, default): splits 2, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 29, merge/split ratio 14.5, nucleations 33
- channel total drift (end/start - 1): [0.4237]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 11 at frame 39: holes 0, rim-vs-core 0.09, rim-vs-outside 0.34, heterogeneity 0.13; core [0.85] rim [0.762]
  - track 4 at frame 38: holes 0, rim-vs-core 0.23, rim-vs-outside 0.24, heterogeneity 0.13; core [0.896] rim [0.662]
  - track 65 at frame 84: holes 0, rim-vs-core 0.18, rim-vs-outside 0.55, heterogeneity 0.13; core [0.992] rim [0.814]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 32 components >= 12 px at frames [33, 50, 67, 83, 100]):
  - radial phi: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.798, rim/outside 1.84 (aggregate of 32 individuals; 1/32 membrane-like individually; rim level 0.569)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #63 (t=2430, R_eq 38.46, ring): none; #11 (t=1170, R_eq 8.35): none; #4 (t=1140, R_eq 6.93): none; #65 (t=2520, R_eq 20.1): none

## Warnings
- radial: 7 of 32 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual
- radial: for 3 of 32 aggregate members less than half of the outside band (rho 1.6-2.2) was sampled (window capped on this grid, or an open boundary): their rim/outside is unreliable, and the aggregate outside level comes mostly from the smaller members

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
