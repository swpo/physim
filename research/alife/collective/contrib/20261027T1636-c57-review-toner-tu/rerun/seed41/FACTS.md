# Evidence pack: eating-flocks (seed 41)

- world: `../../20261027T0210-c51-toner-tu-eaters-fronts/world.py`, family `polar-active-fluid`
- parent: None; mutation: -
- run: 151 frames x 80 steps x dt 0.25 = time 3000; grid [128, 128]; wall 27s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0210-c51-toner-tu-eaters-fronts/world.py --out collective/contrib/c57-w13/rerun --seeds 41 --frames 150 --spf 80 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0001, 0.8602], min area 6 px

## Measurements
- components: final 5, mean 6.2, max 30; occupancy final 0.26
- tracks: 508; persistent (alive >= 50% of run): 0; longest 16 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.05, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [10, 7, 4], H1 [1, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 3.0
- replication (lineage window K = 20 frames = time 400, default): splits 8, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 3, merge/split ratio 0.375, nucleations 445
- channel total drift (end/start - 1): [0.8134, -0.528, -0.295, 20.065]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 378 at frame 110: holes 0, rim-vs-core 0.39, rim-vs-outside 0.78, heterogeneity 0.14; core [0.902, 0.0, 0.942, 0.893] rim [0.636, 0.139, 0.829, 0.665]
  - track 74 at frame 13: holes 0, rim-vs-core 0.38, rim-vs-outside 0.66, heterogeneity 0.22; core [0.931, 0.01, 0.936, 0.432] rim [0.623, 0.133, 0.773, 0.364]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 39 components >= 12 px at frames [25, 50, 76, 100, 125, 150]):
  - radial density rho: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.622, rim/outside 1.41 (aggregate of 39 individuals; 2/39 membrane-like individually; rim level 0.298)
  - radial food c: peak at rho=1.45 (in the peak band 0.5-1.5), rim/core 1.75, rim/outside 0.982 (aggregate of 39 individuals; 0/39 membrane-like individually; rim level 0.429)
  - radial |p|: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.682, rim/outside 1.43 (aggregate of 39 individuals; 3/39 membrane-like individually; rim level 0.413)
  - radial p_x: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.88, rim/outside 1.07 (aggregate of 39 individuals; 0/39 membrane-like individually; rim level 0.479)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #255 (t=1340, R_eq 18.81, ring): ['density rho']; #338 (t=1900, R_eq 22.84, ring): none; #378 (t=2200, R_eq 16.93, ring): ['density rho', '|p|']; #74 (t=260, R_eq 12.48, ring): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 15 of 39 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
