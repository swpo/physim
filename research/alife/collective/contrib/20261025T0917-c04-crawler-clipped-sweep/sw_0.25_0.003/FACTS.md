# Evidence pack: crawler-divide (seed 1)

- world: `../cdiv.py`, family `phase-field`
- parent: None; mutation: growth by uptake, finite-range area penalty (division), food-modulated actin, shedding on retraction
- run: 241 frames x 50 steps x dt 0.05 = time 600; grid [256, 256]; wall 230s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/fba552f4-82e1-5fd3-8aee-1d1a9784fecc/scratchpad/cr/cdiv.py --out /tmp/claude-0/-home-user-physim/fba552f4-82e1-5fd3-8aee-1d1a9784fecc/scratchpad/cr/sw_0.25_0.003 --seeds 1 --frames 240 --no-movie`
- segmentation: matter > 0.26 of robust range [-0.0, 0.9607], min area 6 px

## Measurements
- components: final 3, mean 1.7, max 5; occupancy final 0.12
- tracks: 41; persistent (alive >= 50% of run): 0; longest 75 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [3, 3, 3], H1 [0, 0, 0]
- motion: 4 long-lived tracks moved >= 1 body length; max speed 2.97/time; max body lengths 5.6
- replication (lineage window K = 20 frames = time 50, default): splits 15, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 8, merge/split ratio 0.533, nucleations 0
- channel total drift (end/start - 1): [2.0581, 0.148, None, -0.5224]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 14 at frame 143: holes 0, rim-vs-core 0.28, rim-vs-outside 0.95, heterogeneity 0.18; core [0.815, 0.11, 0.795, 0.077] rim [0.694, 0.33, 0.677, 0.095]
  - track 0 at frame 30: holes 0, rim-vs-core 0.26, rim-vs-outside 0.76, heterogeneity 0.18; core [0.759, 0.315, 0.296, 0.758] rim [0.65, 0.54, 0.254, 0.786]
  - track 35 at frame 230: holes 0, rim-vs-core 0.23, rim-vs-outside 0.62, heterogeneity 0.13; core [0.838, 0.236, 0.155, 0.038] rim [0.644, 0.345, 0.119, 0.06]
  - track 38 at frame 230: holes 0, rim-vs-core 0.35, rim-vs-outside 0.45, heterogeneity 0.10; core [0.811, 0.213, 0.072, 0.022] rim [0.482, 0.334, 0.043, 0.057]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 13 components >= 12 px at frames [40, 81, 121, 159, 200, 240]):
  - radial u (cell): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.704, rim/outside 5.96 (aggregate of 13 individuals; 2/13 membrane-like individually; rim level 0.434)
  - radial |P| (actin polarization): peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.25, rim/outside 5.44 (aggregate of 13 individuals; 9/13 membrane-like individually; rim level 0.216)
  - radial V/V0 (body content): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.521, rim/outside 2.77 (aggregate of 13 individuals; 2/13 membrane-like individually; rim level 0.0993)
  - radial n (nutrient): peak at rho=2.35 (OUTSIDE the peak band 0.5-1.5), rim/core 1.19, rim/outside 0.933 (aggregate of 13 individuals; 0/13 membrane-like individually; rim level 0.25)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #14 (t=357.5, R_eq 66.72, ring): ['u (cell)', '|P| (actin polarization)', 'V/V0 (body content)']; #0 (t=75, R_eq 43.77): none; #35 (t=575, R_eq 30.08): ['|P| (actin polarization)']; #38 (t=575, R_eq 22.2): ['|P| (actin polarization)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 2 of 13 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
