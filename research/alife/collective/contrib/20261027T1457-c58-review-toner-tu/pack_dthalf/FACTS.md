# Evidence pack: eating-flocks (seed 5)

- world: `../../20261027T0210-c51-toner-tu-eaters-fronts/world.py`, family `polar-active-fluid`
- parent: None; mutation: -
- run: 151 frames x 160 steps x dt 0.25 = time 6000; grid [128, 128]; wall 68s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0210-c51-toner-tu-eaters-fronts/world.py --out collective/contrib/20261027T1457-c58-review-toner-tu/pack_dthalf --seeds 5 --frames 150 --spf 160 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0001, 0.8567], min area 6 px

## Measurements
- components: final 3, mean 5.3, max 28; occupancy final 0.26
- tracks: 323; persistent (alive >= 50% of run): 0; longest 28 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.05, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [9, 4, 3], H1 [2, 0, 0]
- motion: 4 long-lived tracks moved >= 1 body length; max speed 0.1/time; max body lengths 3.7
- replication (lineage window K = 20 frames = time 800, default): splits 9, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 2, merge/split ratio 0.222, nucleations 264
- channel total drift (end/start - 1): [0.5678, -0.5145, -0.3068, -13.3671]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 251 at frame 81: holes 0, rim-vs-core 0.30, rim-vs-outside 0.82, heterogeneity 0.12; core [0.878, 0.0, 0.939, 0.143] rim [0.63, 0.137, 0.834, 0.148]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 29 components >= 12 px at frames [25, 50, 76, 100, 125, 150]):
  - radial density rho: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.794, rim/outside 1.33 (aggregate of 29 individuals; 7/29 membrane-like individually; rim level 0.271)
  - radial food c: peak at rho=1.65 (OUTSIDE the peak band 0.5-1.5), rim/core 1.24, rim/outside 0.939 (aggregate of 29 individuals; 0/29 membrane-like individually; rim level 0.422)
  - radial |p|: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.808, rim/outside 1.34 (aggregate of 29 individuals; 6/29 membrane-like individually; rim level 0.376)
  - radial p_x: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.11, rim/outside 1.03 (aggregate of 29 individuals; 0/29 membrane-like individually; rim level 0.482)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #271 (t=4000, R_eq 21.26, ring): none; #293 (t=5080, R_eq 21.28, ring): ['density rho']; #251 (t=3240, R_eq 17.38, ring): ['density rho', '|p|']; #278 (t=4200, R_eq 15.87, ring): ['density rho', '|p|']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 17 of 29 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
