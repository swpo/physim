# Evidence pack: crawler-divide (seed 1)

- world: `../cdiv.py`, family `phase-field`
- parent: None; mutation: growth by uptake, finite-range area penalty (division), food-modulated actin, shedding on retraction
- run: 241 frames x 50 steps x dt 0.05 = time 600; grid [256, 256]; wall 236s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/fba552f4-82e1-5fd3-8aee-1d1a9784fecc/scratchpad/cr/cdiv.py --out /tmp/claude-0/-home-user-physim/fba552f4-82e1-5fd3-8aee-1d1a9784fecc/scratchpad/cr/ocsk --seeds 1 --frames 240 --no-movie`
- segmentation: matter > 0.25 of robust range [-0.0, 0.9969], min area 6 px

## Measurements
- components: final 3, mean 4.5, max 15; occupancy final 0.04
- tracks: 31; persistent (alive >= 50% of run): 0; longest 109 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.20, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [3, 3, 3], H1 [0, 0, 0]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 3.52/time; max body lengths 2.3
- replication (lineage window K = 20 frames = time 50, default): splits 14, persistent splits 4 (0 more failed only because the siblings re-merged within K), max generation 2, merges 1, merge/split ratio 0.071, nucleations 0
- channel total drift (end/start - 1): [-0.0398, -0.7808, None, -0.7021]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 21 at frame 188: holes 0, rim-vs-core 0.43, rim-vs-outside 0.36, heterogeneity 0.07; core [0.888, 0.09, 0.017, 0.06] rim [0.464, 0.143, 0.009, 0.072]
  - track 26 at frame 190: holes 0, rim-vs-core 0.42, rim-vs-outside 0.31, heterogeneity 0.07; core [0.847, 0.11, 0.011, 0.077] rim [0.429, 0.15, 0.005, 0.088]
  - track 27 at frame 194: holes 0, rim-vs-core 0.43, rim-vs-outside 0.36, heterogeneity 0.08; core [0.888, 0.092, 0.019, 0.068] rim [0.46, 0.152, 0.01, 0.082]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 28 components >= 12 px at frames [40, 81, 121, 159, 200, 240]):
  - radial u (cell): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.779, rim/outside 4.81 (aggregate of 28 individuals; 0/28 membrane-like individually; rim level 0.663)
  - radial |P| (actin polarization): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 2.37, rim/outside 5.11 (aggregate of 28 individuals; 21/28 membrane-like individually; rim level 0.124)  MEMBRANE-LIKE
  - radial V/V0 (body content): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.946, rim/outside 2.53 (aggregate of 28 individuals; 0/28 membrane-like individually; rim level 0.0558)
  - radial n (nutrient): peak at rho=1.25 (in the peak band 0.5-1.5), rim/core 1.14, rim/outside 1.07 (aggregate of 28 individuals; 0/28 membrane-like individually; rim level 0.0836)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): |P| (actin polarization)
- membrane-like channels per top track at mid-life: #21 (t=470, R_eq 23.98): ['|P| (actin polarization)']; #26 (t=475, R_eq 20.3): ['|P| (actin polarization)']; #27 (t=485, R_eq 25.44): ['|P| (actin polarization)']; #3 (t=182.5, R_eq 144.43): none

## Warnings
- matter fills >80% of the domain at some point: components may be one connected sea
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 1 of 28 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual
- radial: for 3 of 28 aggregate members less than half of the outside band (rho 1.6-2.2) was sampled (window capped on this grid, or an open boundary): their rim/outside is unreliable, and the aggregate outside level comes mostly from the smaller members

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
