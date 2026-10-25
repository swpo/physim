# Evidence pack: crawler-divide (seed 1)

- world: `../../cdiv2.py`, family `phase-field`
- parent: None; mutation: growth by uptake, finite-range area penalty (division), food-modulated actin, shedding on retraction
- run: 241 frames x 50 steps x dt 0.05 = time 600; grid [256, 256]; wall 232s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/fba552f4-82e1-5fd3-8aee-1d1a9784fecc/scratchpad/cr/cdiv2.py --out /tmp/claude-0/-home-user-physim/fba552f4-82e1-5fd3-8aee-1d1a9784fecc/scratchpad/cr/v2r0.008 --seeds 1 2 --frames 240 --no-movie`
- segmentation: matter > 0.26 of robust range [-0.0, 0.9792], min area 6 px

## Measurements
- components: final 1, mean 1.5, max 6; occupancy final 0.96
- tracks: 78; persistent (alive >= 50% of run): 1; longest 133 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.17 (1 = constant size)
- enclosures: components with a hole mean 0.73, final 1; holes at thresholds 0.2/0.35/0.5 final [24, 36, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [28, 28, 25], H1 [47, 19, 0]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 0.916/time; max body lengths 1.2
- replication (lineage window K = 20 frames = time 50, default): splits 27, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 23, merge/split ratio 0.852, nucleations 0
- channel total drift (end/start - 1): [21.7407, 3.9298, None, -0.4199]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 12: holes 0, rim-vs-core 0.32, rim-vs-outside 0.71, heterogeneity 0.12; core [0.922, 0.182, 0.044, 0.404] rim [0.677, 0.381, 0.032, 0.474]
  - track 3 at frame 34: holes 0, rim-vs-core 0.33, rim-vs-outside 0.40, heterogeneity 0.08; core [0.662, 0.276, 0.01, 0.557] rim [0.382, 0.437, 0.006, 0.621]
  - track 5 at frame 38: holes 0, rim-vs-core 0.25, rim-vs-outside 0.75, heterogeneity 0.16; core [0.763, 0.13, 0.161, 0.628] rim [0.709, 0.37, 0.15, 0.658]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 8 components >= 12 px at frames [40, 81, 121, 159, 200, 240]):
  - radial u (cell): peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.06, rim/outside 2.98 (aggregate of 8 individuals; 1/8 membrane-like individually; rim level 0.608)
  - radial |P| (actin polarization): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.5, rim/outside 1.87 (aggregate of 8 individuals; 3/8 membrane-like individually; rim level 0.275)  MEMBRANE-LIKE
  - radial V/V0 (body content): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 1.04, rim/outside 5.3 (aggregate of 8 individuals; 1/8 membrane-like individually; rim level 0.412)
  - radial n (nutrient): peak at rho=2.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.98, rim/outside 0.509 (aggregate of 8 individuals; 0/8 membrane-like individually; rim level 0.297)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): |P| (actin polarization)
- membrane-like channels per top track at mid-life: #76 (t=437.5, R_eq 141.55): none; #0 (t=30, R_eq 43.98, ring): ['u (cell)', '|P| (actin polarization)', 'V/V0 (body content)']; #3 (t=85, R_eq 21.83): ['|P| (actin polarization)']; #5 (t=95, R_eq 85, ring): ['u (cell)', '|P| (actin polarization)', 'V/V0 (body content)']

## Warnings
- matter fills >80% of the domain at some point: components may be one connected sea
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 1 of 8 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual
- radial: for 6 of 8 aggregate members less than half of the outside band (rho 1.6-2.2) was sampled (window capped on this grid, or an open boundary): their rim/outside is unreliable, and the aggregate outside level comes mostly from the smaller members

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
