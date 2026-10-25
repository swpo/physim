# Evidence pack: crawler-divide (seed 1)

- world: `../cdiv.py`, family `phase-field`
- parent: None; mutation: growth by uptake, finite-range area penalty (division), food-modulated actin, shedding on retraction
- run: 401 frames x 100 steps x dt 0.05 = time 2000; grid [256, 256]; wall 715s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/fba552f4-82e1-5fd3-8aee-1d1a9784fecc/scratchpad/cr/cdiv.py --out /tmp/claude-0/-home-user-physim/fba552f4-82e1-5fd3-8aee-1d1a9784fecc/scratchpad/cr/long_b --seeds 1 --frames 400 --no-movie`
- segmentation: matter > 0.25 of robust range [-0.0, 0.9938], min area 6 px

## Measurements
- components: final 0, mean 1.4, max 16; occupancy final 0.00
- tracks: 30; persistent (alive >= 50% of run): 0; longest 59 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.08, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [0, 0, 0], H1 [0, 0, 0]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 2.28/time; max body lengths 3.1
- replication (lineage window K = 20 frames = time 100, default): splits 14, persistent splits 2 (0 more failed only because the siblings re-merged within K), max generation 2, merges 0, merge/split ratio 0, nucleations 0
- channel total drift (end/start - 1): [-1.0, -1.0, None, -0.6608]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 11 at frame 94: holes 0, rim-vs-core 0.44, rim-vs-outside 0.33, heterogeneity 0.08; core [0.871, 0.134, 0.012, 0.075] rim [0.437, 0.173, 0.006, 0.086]
  - track 22 at frame 97: holes 0, rim-vs-core 0.43, rim-vs-outside 0.33, heterogeneity 0.08; core [0.873, 0.133, 0.012, 0.075] rim [0.441, 0.174, 0.006, 0.086]
  - track 23 at frame 84: holes 0, rim-vs-core 0.38, rim-vs-outside 0.27, heterogeneity 0.07; core [0.783, 0.144, 0.006, 0.059] rim [0.398, 0.158, 0.003, 0.064]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 9 components >= 12 px at frames [67]):
  - radial u (cell): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.711, rim/outside 1.74 (aggregate of 9 individuals; 0/9 membrane-like individually; rim level 0.562)
  - radial |P| (actin polarization): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.57, rim/outside 1.57 (aggregate of 9 individuals; 4/9 membrane-like individually; rim level 0.118)  MEMBRANE-LIKE
  - radial V/V0 (body content): peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.801, rim/outside 1.05 (aggregate of 9 individuals; 1/9 membrane-like individually; rim level 0.0174)
  - radial n (nutrient): peak at rho=1.65 (OUTSIDE the peak band 0.5-1.5), rim/core 1.27, rim/outside 1 (aggregate of 9 individuals; 0/9 membrane-like individually; rim level 0.0238)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): |P| (actin polarization)
- membrane-like channels per top track at mid-life: #0 (t=150, R_eq 144.43): none; #11 (t=470, R_eq 20.65): ['|P| (actin polarization)']; #22 (t=485, R_eq 20.64): ['|P| (actin polarization)']; #23 (t=420, R_eq 15.77): ['|P| (actin polarization)']

## Warnings
- matter fills >80% of the domain at some point: components may be one connected sea
- no components at the end: matter died out or fell below threshold
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 1 of 9 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
