# Evidence pack: crawler-divide (seed 2)

- world: `../../../../../../../home/user/physim/research/alife/collective/contrib/20261025T0908-c04-crawler-divide-confound/world.py`, family `phase-field`
- parent: None; mutation: growth by uptake, finite-range area penalty (division), food-modulated actin, shedding on retraction
- run: 241 frames x 50 steps x dt 0.05 = time 600; grid [256, 256]; wall 281s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0908-c04-crawler-divide-confound/world.py --out /tmp/claude-0/-home-user-physim/b3c8c7c9-06fe-5142-8c86-74065d022b56/scratchpad/rev7/shed0.1 --seeds 2 --frames 240 --no-movie`
- segmentation: matter > 0.25 of robust range [-0.0, 0.9826], min area 6 px

## Measurements
- components: final 1, mean 4.0, max 13; occupancy final 0.01
- tracks: 53; persistent (alive >= 50% of run): 0; longest 103 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.06, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [1, 1, 1], H1 [0, 0, 0]
- motion: 2 long-lived tracks moved >= 1 body length; max speed 3.48/time; max body lengths 4.6
- replication (lineage window K = 20 frames = time 50, default): splits 22, persistent splits 1 (0 more failed only because the siblings re-merged within K), max generation 1, merges 7, merge/split ratio 0.318, nucleations 0
- channel total drift (end/start - 1): [-0.7179, -0.9183, None, -0.6172]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 49 at frame 190: holes 0, rim-vs-core 0.42, rim-vs-outside 0.39, heterogeneity 0.08; core [0.877, 0.138, 0.052, 0.024] rim [0.468, 0.225, 0.027, 0.049]
  - track 46 at frame 186: holes 0, rim-vs-core 0.41, rim-vs-outside 0.34, heterogeneity 0.08; core [0.833, 0.151, 0.036, 0.031] rim [0.432, 0.215, 0.019, 0.051]
  - track 52 at frame 182: holes 0, rim-vs-core 0.40, rim-vs-outside 0.34, heterogeneity 0.08; core [0.841, 0.144, 0.036, 0.014] rim [0.442, 0.205, 0.019, 0.032]
  - track 51 at frame 169: holes 0, rim-vs-core 0.37, rim-vs-outside 0.34, heterogeneity 0.07; core [0.822, 0.138, 0.026, 0.015] rim [0.459, 0.197, 0.014, 0.03]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 22 components >= 12 px at frames [40, 81, 121, 159, 200, 240]):
  - radial u (cell): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.815, rim/outside 9.73 (aggregate of 22 individuals; 1/22 membrane-like individually; rim level 0.659)
  - radial |P| (actin polarization): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 3.03, rim/outside 7.48 (aggregate of 22 individuals; 20/22 membrane-like individually; rim level 0.215)  MEMBRANE-LIKE
  - radial V/V0 (body content): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.885, rim/outside 3.03 (aggregate of 22 individuals; 1/22 membrane-like individually; rim level 0.107)
  - radial n (nutrient): peak at rho=2.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1.28, rim/outside 0.918 (aggregate of 22 individuals; 0/22 membrane-like individually; rim level 0.123)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): |P| (actin polarization)
- membrane-like channels per top track at mid-life: #49 (t=475, R_eq 23.17): ['|P| (actin polarization)']; #46 (t=465, R_eq 20.55): ['|P| (actin polarization)']; #52 (t=455, R_eq 20.23): ['|P| (actin polarization)']; #51 (t=422.5, R_eq 18.01): ['|P| (actin polarization)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 2 of 22 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual
- radial: for 1 of 22 aggregate members less than half of the outside band (rho 1.6-2.2) was sampled (window capped on this grid, or an open boundary): their rim/outside is unreliable, and the aggregate outside level comes mostly from the smaller members

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
