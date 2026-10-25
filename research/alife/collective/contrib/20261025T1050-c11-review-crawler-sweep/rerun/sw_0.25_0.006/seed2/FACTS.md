# Evidence pack: crawler-divide (seed 2)

- world: `../../../../home/user/physim/research/alife/collective/contrib/20261025T0908-c04-crawler-divide-confound/world.py`, family `phase-field`
- parent: None; mutation: growth by uptake, finite-range area penalty (division), food-modulated actin, shedding on retraction
- run: 241 frames x 50 steps x dt 0.05 = time 600; grid [256, 256]; wall 269s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0908-c04-crawler-divide-confound/world.py --out /tmp/claude-0/c11rev13/sw_0.25_0.006 --seeds 2 --frames 240 --no-movie`
- segmentation: matter > 0.25 of robust range [-0.0, 0.9913], min area 6 px

## Measurements
- components: final 4, mean 2.1, max 5; occupancy final 0.33
- tracks: 105; persistent (alive >= 50% of run): 0; longest 44 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.12, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [7, 6, 5], H1 [0, 0, 0]
- motion: 3 long-lived tracks moved >= 1 body length; max speed 2.91/time; max body lengths 4.4
- replication (lineage window K = 20 frames = time 50, default): splits 40, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 29, merge/split ratio 0.725, nucleations 0
- channel total drift (end/start - 1): [7.3571, 1.9055, None, -0.5627]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 22: holes 0, rim-vs-core 0.28, rim-vs-outside 0.71, heterogeneity 0.16; core [0.738, 0.327, 0.105, 0.776] rim [0.606, 0.567, 0.086, 0.823]
  - track 15 at frame 111: holes 0, rim-vs-core 0.22, rim-vs-outside 0.81, heterogeneity 0.19; core [0.673, 0.14, 0.473, 0.305] rim [0.65, 0.354, 0.457, 0.34]
  - track 73 at frame 210: holes 0, rim-vs-core 0.36, rim-vs-outside 0.43, heterogeneity 0.09; core [0.805, 0.198, 0.041, 0.054] rim [0.467, 0.32, 0.024, 0.089]
  - track 1 at frame 52: holes 0, rim-vs-core 0.21, rim-vs-outside 0.44, heterogeneity 0.12; core [0.561, 0.317, 0.155, 0.739] rim [0.409, 0.461, 0.113, 0.76]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 15 components >= 12 px at frames [40, 81, 121, 159, 200, 240]):
  - radial u (cell): peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.918, rim/outside 3.52 (aggregate of 15 individuals; 3/15 membrane-like individually; rim level 0.523)
  - radial |P| (actin polarization): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.78, rim/outside 3.07 (aggregate of 15 individuals; 11/15 membrane-like individually; rim level 0.204)  MEMBRANE-LIKE
  - radial V/V0 (body content): peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 1, rim/outside 2.05 (aggregate of 15 individuals; 3/15 membrane-like individually; rim level 0.131)
  - radial n (nutrient): peak at rho=1.85 (OUTSIDE the peak band 0.5-1.5), rim/core 1.31, rim/outside 0.96 (aggregate of 15 individuals; 0/15 membrane-like individually; rim level 0.201)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): |P| (actin polarization)
- membrane-like channels per top track at mid-life: #0 (t=55, R_eq 39.74): none; #15 (t=277.5, R_eq 86.74, ring): ['u (cell)', '|P| (actin polarization)', 'V/V0 (body content)']; #73 (t=525, R_eq 24.33): ['|P| (actin polarization)']; #1 (t=130, R_eq 17.69): ['|P| (actin polarization)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 4 of 15 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual
- radial: for 2 of 15 aggregate members less than half of the outside band (rho 1.6-2.2) was sampled (window capped on this grid, or an open boundary): their rim/outside is unreliable, and the aggregate outside level comes mostly from the smaller members

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
