# Evidence pack: crawler (seed 1)

- world: `../crawler.py`, family `phase-field`
- parent: None; mutation: Ziebert-Aranson crawling cell, body-wise area constraint
- run: 241 frames x 50 steps x dt 0.05 = time 600; grid [256, 256]; wall 225s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/fba552f4-82e1-5fd3-8aee-1d1a9784fecc/scratchpad/cr/crawler.py --out /tmp/claude-0/-home-user-physim/fba552f4-82e1-5fd3-8aee-1d1a9784fecc/scratchpad/cr/K_chi0 --seeds 1 --frames 240 --threshold 0.25 --no-movie`
- segmentation: matter > 0.33 of robust range [-0.0, 0.7468], min area 6 px

## Measurements
- components: final 22, mean 17.0, max 22; occupancy final 0.21
- tracks: 46; persistent (alive >= 50% of run): 20; longest 203 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 76.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [22, 22, 22], H1 [0, 0, 0]
- motion: 12 long-lived tracks moved >= 1 body length; max speed 1.65/time; max body lengths 2.6
- replication (lineage window K = 20 frames = time 50, default): splits 21, persistent splits 17 (0 more failed only because the siblings re-merged within K), max generation 6, merges 1, merge/split ratio 0.048, nucleations 1
- channel total drift (end/start - 1): [3.1779, 1.7531, None, -0.6985]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 13 at frame 139: holes 0, rim-vs-core 0.37, rim-vs-outside 0.30, heterogeneity 0.09; core [0.787, 0.372, 0.296, 0.063] rim [0.513, 0.592, 0.193, 0.075]
  - track 15 at frame 143: holes 0, rim-vs-core 0.38, rim-vs-outside 0.31, heterogeneity 0.10; core [0.799, 0.383, 0.339, 0.042] rim [0.515, 0.603, 0.219, 0.055]
  - track 17 at frame 145: holes 0, rim-vs-core 0.39, rim-vs-outside 0.34, heterogeneity 0.10; core [0.781, 0.333, 0.473, 0.026] rim [0.508, 0.557, 0.308, 0.041]
  - track 40 at frame 167: holes 0, rim-vs-core 0.28, rim-vs-outside 0.17, heterogeneity 0.07; core [0.675, 0.37, 0.0, 0.022] rim [0.481, 0.567, 0.0, 0.028]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 112 components >= 12 px at frames [40, 81, 121, 159, 200, 240]):
  - radial u (cell): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.808, rim/outside 10.2 (aggregate of 112 individuals; 0/112 membrane-like individually; rim level 0.676)
  - radial |P| (actin polarization): peak at rho=0.95 (in the peak band 0.5-1.5), rim/core 3.63, rim/outside 4.69 (aggregate of 112 individuals; 111/112 membrane-like individually; rim level 0.6)  MEMBRANE-LIKE
  - radial V/V0 (body content): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.82, rim/outside 8.19 (aggregate of 112 individuals; 0/112 membrane-like individually; rim level 0.166)
  - radial n (nutrient): peak at rho=1.85 (OUTSIDE the peak band 0.5-1.5), rim/core 1.21, rim/outside 0.955 (aggregate of 112 individuals; 0/112 membrane-like individually; rim level 0.166)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): |P| (actin polarization)
- membrane-like channels per top track at mid-life: #13 (t=347.5, R_eq 18.64): ['|P| (actin polarization)']; #15 (t=357.5, R_eq 18.97): ['|P| (actin polarization)']; #17 (t=362.5, R_eq 20.92): ['|P| (actin polarization)']; #40 (t=417.5, R_eq 13.82): ['|P| (actin polarization)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
