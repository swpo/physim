# Evidence pack: crawler-divide (seed 1)

- world: `../cdiv.py`, family `phase-field`
- parent: None; mutation: growth by uptake, finite-range area penalty (division), food-modulated actin, shedding on retraction
- run: 241 frames x 50 steps x dt 0.05 = time 600; grid [256, 256]; wall 237s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/fba552f4-82e1-5fd3-8aee-1d1a9784fecc/scratchpad/cr/cdiv.py --out /tmp/claude-0/-home-user-physim/fba552f4-82e1-5fd3-8aee-1d1a9784fecc/scratchpad/cr/ocs0.1 --seeds 1 --frames 240 --no-movie`
- segmentation: matter > 0.25 of robust range [-0.0, 0.9899], min area 6 px

## Measurements
- components: final 0, mean 4.1, max 11; occupancy final 0.00
- tracks: 51; persistent (alive >= 50% of run): 0; longest 90 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.06, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [1, 1, 1], H1 [0, 0, 0]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 3.09/time; max body lengths 5.0
- replication (lineage window K = 20 frames = time 50, default): splits 22, persistent splits 1 (0 more failed only because the siblings re-merged within K), max generation 1, merges 6, merge/split ratio 0.273, nucleations 0
- channel total drift (end/start - 1): [-0.9997, -0.9993, None, -0.631]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 25 at frame 161: holes 0, rim-vs-core 0.25, rim-vs-outside 0.46, heterogeneity 0.08; core [0.83, 0.141, 0.035, 0.007] rim [0.583, 0.166, 0.025, 0.014]
  - track 48 at frame 194: holes 0, rim-vs-core 0.39, rim-vs-outside 0.33, heterogeneity 0.07; core [0.819, 0.147, 0.03, 0.041] rim [0.431, 0.209, 0.016, 0.059]
  - track 27 at frame 157: holes 0, rim-vs-core 0.41, rim-vs-outside 0.33, heterogeneity 0.07; core [0.843, 0.133, 0.034, 0.004] rim [0.437, 0.188, 0.018, 0.017]
  - track 0 at frame 38: holes 0, rim-vs-core 0.28, rim-vs-outside 0.77, heterogeneity 0.18; core [0.752, 0.237, 0.295, 0.757] rim [0.659, 0.497, 0.259, 0.761]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 24 components >= 12 px at frames [40, 81, 121, 159, 200]):
  - radial u (cell): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.786, rim/outside 5.12 (aggregate of 24 individuals; 1/24 membrane-like individually; rim level 0.64)
  - radial |P| (actin polarization): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 2.9, rim/outside 4.98 (aggregate of 24 individuals; 22/24 membrane-like individually; rim level 0.189)  MEMBRANE-LIKE
  - radial V/V0 (body content): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.702, rim/outside 2 (aggregate of 24 individuals; 1/24 membrane-like individually; rim level 0.0649)
  - radial n (nutrient): peak at rho=1.75 (OUTSIDE the peak band 0.5-1.5), rim/core 1.28, rim/outside 0.99 (aggregate of 24 individuals; 0/24 membrane-like individually; rim level 0.098)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): |P| (actin polarization)
- membrane-like channels per top track at mid-life: #25 (t=402.5, R_eq 20.88): ['|P| (actin polarization)']; #48 (t=485, R_eq 19.72): ['|P| (actin polarization)']; #27 (t=392.5, R_eq 20.46): ['|P| (actin polarization)']; #0 (t=95, R_eq 61.26, ring): ['u (cell)', '|P| (actin polarization)', 'V/V0 (body content)']

## Warnings
- no components at the end: matter died out or fell below threshold
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 1 of 24 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual
- radial: for 1 of 24 aggregate members less than half of the outside band (rho 1.6-2.2) was sampled (window capped on this grid, or an open boundary): their rim/outside is unreliable, and the aggregate outside level comes mostly from the smaller members

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
