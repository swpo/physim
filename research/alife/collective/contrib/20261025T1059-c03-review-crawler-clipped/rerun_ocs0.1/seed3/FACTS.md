# Evidence pack: crawler-divide (seed 3)

- world: `../../../../../../../../../home/user/physim/research/alife/collective/contrib/20261025T0908-c04-crawler-divide-confound/world.py`, family `phase-field`
- parent: None; mutation: growth by uptake, finite-range area penalty (division), food-modulated actin, shedding on retraction
- run: 241 frames x 50 steps x dt 0.05 = time 600; grid [256, 256]; wall 260s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0908-c04-crawler-divide-confound/world.py --out /tmp/claude-0/-home-user-physim/ca3fe853-e88d-58ad-9551-2586c1b06c34/scratchpad/rev/ccs/ocs0.1/seed3 --seeds 3 --frames 240 --no-movie`
- segmentation: matter > 0.25 of robust range [-0.0, 0.9807], min area 6 px

## Measurements
- components: final 0, mean 4.0, max 10; occupancy final 0.00
- tracks: 54; persistent (alive >= 50% of run): 0; longest 90 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.03, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [2, 1, 1], H1 [0, 0, 0]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 3.47/time; max body lengths 4.4
- replication (lineage window K = 20 frames = time 50, default): splits 21, persistent splits 2 (0 more failed only because the siblings re-merged within K), max generation 1, merges 10, merge/split ratio 0.476, nucleations 0
- channel total drift (end/start - 1): [-1.0, -1.0, None, -0.6571]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 45 at frame 182: holes 0, rim-vs-core 0.41, rim-vs-outside 0.33, heterogeneity 0.08; core [0.845, 0.142, 0.037, 0.011] rim [0.436, 0.2, 0.019, 0.028]
  - track 35 at frame 161: holes 0, rim-vs-core 0.42, rim-vs-outside 0.33, heterogeneity 0.08; core [0.858, 0.135, 0.041, 0.001] rim [0.441, 0.192, 0.021, 0.01]
  - track 47 at frame 179: holes 0, rim-vs-core 0.21, rim-vs-outside 0.48, heterogeneity 0.08; core [0.808, 0.162, 0.033, 0.011] rim [0.6, 0.166, 0.025, 0.019]
  - track 51 at frame 186: holes 0, rim-vs-core 0.40, rim-vs-outside 0.33, heterogeneity 0.07; core [0.826, 0.148, 0.032, 0.029] rim [0.431, 0.206, 0.016, 0.046]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 24 components >= 12 px at frames [40, 81, 121, 159, 200]):
  - radial u (cell): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.83, rim/outside 9.07 (aggregate of 24 individuals; 2/24 membrane-like individually; rim level 0.658)
  - radial |P| (actin polarization): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 3.32, rim/outside 6.74 (aggregate of 24 individuals; 23/24 membrane-like individually; rim level 0.21)  MEMBRANE-LIKE
  - radial V/V0 (body content): peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.06, rim/outside 2.17 (aggregate of 24 individuals; 2/24 membrane-like individually; rim level 0.0537)
  - radial n (nutrient): peak at rho=1.95 (OUTSIDE the peak band 0.5-1.5), rim/core 1.23, rim/outside 0.923 (aggregate of 24 individuals; 0/24 membrane-like individually; rim level 0.116)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): |P| (actin polarization)
- membrane-like channels per top track at mid-life: #45 (t=455, R_eq 20.36): ['|P| (actin polarization)']; #35 (t=402.5, R_eq 21.03): ['|P| (actin polarization)']; #47 (t=447.5, R_eq 19.9): ['|P| (actin polarization)']; #51 (t=465, R_eq 19.48): ['|P| (actin polarization)']

## Warnings
- no components at the end: matter died out or fell below threshold
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 2 of 24 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual
- radial: for 2 of 24 aggregate members less than half of the outside band (rho 1.6-2.2) was sampled (window capped on this grid, or an open boundary): their rim/outside is unreliable, and the aggregate outside level comes mostly from the smaller members

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
