# Evidence pack: rdtrail_slow5 (seed 22)

- world: `../../world_slow5_dt2.py`, family `reaction-diffusion`
- parent: kstrail; mutation: kstrail with both taxis terms replaced by local threshold kinetics (Laplacian-only twin)
- run: 201 frames x 120 steps x dt 0.025 = time 600; grid [192, 192]; wall 49s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0935-c10-review-kstrail-twin/world_slow5_dt2.py --out collective/contrib/20261025T0935-c10-review-kstrail-twin/twin_kh01_dt2 --seeds 21 22 --spf 120 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 0.9939], min area 6 px

## Measurements
- components: final 8, mean 7.9, max 14; occupancy final 0.16
- tracks: 72; persistent (alive >= 50% of run): 0; longest 87 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [8, 8, 8], H1 [0, 0, 0]
- motion: 11 long-lived tracks moved >= 1 body length; max speed 0.284/time; max body lengths 2.0
- replication (lineage window K = 20 frames = time 60, default): splits 30, persistent splits 9 (0 more failed only because the siblings re-merged within K), max generation 4, merges 6, merge/split ratio 0.2, nucleations 0
- channel total drift (end/start - 1): [3.1502, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 19 at frame 79: holes 0, rim-vs-core 0.39, rim-vs-outside 0.40, heterogeneity 0.19; core [0.865, 0.712, 0.625] rim [0.543, 0.538, 0.497]
  - track 49 at frame 158: holes 0, rim-vs-core 0.20, rim-vs-outside 0.48, heterogeneity 0.18; core [0.812, 0.577, 0.605] rim [0.635, 0.507, 0.56]
  - track 54 at frame 163: holes 0, rim-vs-core 0.38, rim-vs-outside 0.30, heterogeneity 0.17; core [0.8, 0.587, 0.722] rim [0.491, 0.439, 0.561]
  - track 57 at frame 163: holes 0, rim-vs-core 0.35, rim-vs-outside 0.51, heterogeneity 0.19; core [0.904, 0.685, 0.594] rim [0.607, 0.509, 0.516]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 46 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial u: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.784, rim/outside 8.86 (aggregate of 46 individuals; 2/46 membrane-like individually; rim level 0.631)
  - radial a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.799, rim/outside 3.98 (aggregate of 46 individuals; 0/46 membrane-like individually; rim level 0.566)
  - radial h: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.797, rim/outside 2.79 (aggregate of 46 individuals; 0/46 membrane-like individually; rim level 0.624)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #19 (t=237, R_eq 15.65): none; #49 (t=474, R_eq 11.37): none; #54 (t=489, R_eq 11.64): none; #57 (t=489, R_eq 15.01): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 3 of 46 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
