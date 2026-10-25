# Evidence pack: apfc (seed 5)

- world: `../../world.py`, family `active-pfc`
- parent: new class (Menzel & Loewen 2013 active phase-field crystal); mutation: none (benchmark model)
- run: 201 frames x 50 steps x dt 0.1 = time 1000; grid [128, 128]; wall 45s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1225-c13-review-apfc-births/world.py --out collective/contrib/20261025T1225-c13-review-apfc-births/rerun --seeds 5 6 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 0.6095], min area 6 px

## Measurements
- components: final 6, mean 7.2, max 10; occupancy final 0.19
- tracks: 135; persistent (alive >= 50% of run): 0; longest 66 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.01, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [10, 6, 6], H1 [0, 0, 0]
- motion: 21 long-lived tracks moved >= 1 body length; max speed 0.299/time; max body lengths 9.6
- replication (lineage window K = 20 frames = time 100, default): splits 42, persistent splits 1 (0 more failed only because the siblings re-merged within K), max generation 1, merges 45, merge/split ratio 1.07, nucleations 9
- channel total drift (end/start - 1): [-0.6231, 0.0, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 4 at frame 35: holes 0, rim-vs-core 0.58, rim-vs-outside 0.16, heterogeneity 0.26; core [0.719, 0.431, 0.664] rim [0.442, 0.061, 0.314]
  - track 46 at frame 111: holes 0, rim-vs-core 0.61, rim-vs-outside 0.30, heterogeneity 0.27; core [0.832, 0.443, 0.685] rim [0.494, 0.085, 0.319]
  - track 8 at frame 24: holes 0, rim-vs-core 0.60, rim-vs-outside 0.30, heterogeneity 0.27; core [0.83, 0.444, 0.68] rim [0.498, 0.089, 0.333]
  - track 5 at frame 22: holes 0, rim-vs-core 0.56, rim-vs-outside 0.29, heterogeneity 0.27; core [0.818, 0.428, 0.666] rim [0.502, 0.096, 0.338]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 42 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial crystal amplitude (smoothed (phi - mean)^2): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.752, rim/outside 7.59 (aggregate of 42 individuals; 0/42 membrane-like individually; rim level 0.633)
  - radial density phi: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.648, rim/outside 1.53 (aggregate of 42 individuals; 14/42 membrane-like individually; rim level 0.284)
  - radial |P|: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.818, rim/outside 7.58 (aggregate of 42 individuals; 0/42 membrane-like individually; rim level 0.511)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #4 (t=175, R_eq 5.38): none; #46 (t=555, R_eq 7.96): ['density phi']; #8 (t=120, R_eq 7.9): ['density phi']; #5 (t=110, R_eq 8.04): ['density phi']

## Warnings
- matter fills >80% of the domain at some point: components may be one connected sea
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
