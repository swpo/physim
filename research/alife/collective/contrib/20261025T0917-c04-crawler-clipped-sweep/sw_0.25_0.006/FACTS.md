# Evidence pack: crawler-divide (seed 1)

- world: `../cdiv.py`, family `phase-field`
- parent: None; mutation: growth by uptake, finite-range area penalty (division), food-modulated actin, shedding on retraction
- run: 241 frames x 50 steps x dt 0.05 = time 600; grid [256, 256]; wall 229s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/fba552f4-82e1-5fd3-8aee-1d1a9784fecc/scratchpad/cr/cdiv.py --out /tmp/claude-0/-home-user-physim/fba552f4-82e1-5fd3-8aee-1d1a9784fecc/scratchpad/cr/sw_0.25_0.006 --seeds 1 --frames 240 --no-movie`
- segmentation: matter > 0.25 of robust range [-0.0, 0.9917], min area 6 px

## Measurements
- components: final 2, mean 2.0, max 7; occupancy final 0.31
- tracks: 127; persistent (alive >= 50% of run): 0; longest 65 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.19, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [7, 6, 4], H1 [0, 0, 0]
- motion: 2 long-lived tracks moved >= 1 body length; max speed 3.11/time; max body lengths 6.1
- replication (lineage window K = 20 frames = time 50, default): splits 47, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 35, merge/split ratio 0.745, nucleations 0
- channel total drift (end/start - 1): [6.7536, 1.7214, None, -0.5621]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 32: holes 0, rim-vs-core 0.25, rim-vs-outside 0.70, heterogeneity 0.16; core [0.733, 0.306, 0.128, 0.776] rim [0.621, 0.523, 0.108, 0.802]
  - track 3 at frame 101: holes 0, rim-vs-core 0.23, rim-vs-outside 0.78, heterogeneity 0.19; core [0.712, 0.157, 0.429, 0.357] rim [0.658, 0.375, 0.396, 0.392]
  - track 5 at frame 131: holes 1, rim-vs-core 0.17, rim-vs-outside 0.88, heterogeneity 0.20; core [0.584, 0.093, 0.579, 0.167] rim [0.639, 0.241, 0.634, 0.178]
  - track 88 at frame 204: holes 0, rim-vs-core 0.21, rim-vs-outside 0.59, heterogeneity 0.10; core [0.763, 0.107, 0.05, 0.009] rim [0.655, 0.283, 0.043, 0.046]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 12 components >= 12 px at frames [40, 81, 121, 159, 200, 240]):
  - radial u (cell): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.849, rim/outside 2.39 (aggregate of 12 individuals; 2/12 membrane-like individually; rim level 0.442)
  - radial |P| (actin polarization): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.67, rim/outside 2.62 (aggregate of 12 individuals; 8/12 membrane-like individually; rim level 0.193)  MEMBRANE-LIKE
  - radial V/V0 (body content): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.936, rim/outside 2.25 (aggregate of 12 individuals; 4/12 membrane-like individually; rim level 0.176)
  - radial n (nutrient): peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.12, rim/outside 0.965 (aggregate of 12 individuals; 0/12 membrane-like individually; rim level 0.244)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): |P| (actin polarization)
- membrane-like channels per top track at mid-life: #0 (t=80, R_eq 44.98): none; #3 (t=252.5, R_eq 81.27, ring): ['u (cell)', '|P| (actin polarization)', 'V/V0 (body content)']; #5 (t=327.5, R_eq 108.22): none; #88 (t=510, R_eq 27.81): ['|P| (actin polarization)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 3 of 12 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual
- radial: for 4 of 12 aggregate members less than half of the outside band (rho 1.6-2.2) was sampled (window capped on this grid, or an open boundary): their rim/outside is unreliable, and the aggregate outside level comes mostly from the smaller members

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
