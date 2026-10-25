# Evidence pack: crawler (seed 1)

- world: `../../crawler.py`, family `phase-field`
- parent: None; mutation: Ziebert-Aranson crawling cell, body-wise area constraint
- run: 121 frames x 100 steps x dt 0.05 = time 600; grid [256, 256]; wall 215s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/fba552f4-82e1-5fd3-8aee-1d1a9784fecc/scratchpad/cr/crawler.py --out /tmp/claude-0/-home-user-physim/fba552f4-82e1-5fd3-8aee-1d1a9784fecc/scratchpad/cr/okg --seeds 0 1 --frames 120 --no-movie`
- segmentation: matter > 0.59 of robust range [-0.0, 0.8413], min area 6 px

## Measurements
- components: final 21, mean 14.4, max 21; occupancy final 0.27
- tracks: 63; persistent (alive >= 50% of run): 10; longest 84 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 83.29 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [21, 21, 21], H1 [0, 0, 0]
- motion: 12 long-lived tracks moved >= 1 body length; max speed 0.655/time; max body lengths 3.8
- replication (lineage window K = 20 frames = time 100, default): splits 21, persistent splits 10 (0 more failed only because the siblings re-merged within K), max generation 4, merges 0, merge/split ratio 0, nucleations 19
- channel total drift (end/start - 1): [9.3494, 4.5747, None, -0.4592]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 20 at frame 79: holes 0, rim-vs-core 0.20, rim-vs-outside 0.15, heterogeneity 0.05; core [0.74, 0.172, 0.682, 0.082] rim [0.66, 0.334, 0.609, 0.099]
  - track 22 at frame 82: holes 0, rim-vs-core 0.30, rim-vs-outside 0.40, heterogeneity 0.11; core [0.901, 0.37, 0.845, 0.067] rim [0.774, 0.618, 0.726, 0.093]
  - track 23 at frame 82: holes 0, rim-vs-core 0.16, rim-vs-outside 0.10, heterogeneity 0.04; core [0.713, 0.193, 0.669, 0.108] rim [0.648, 0.322, 0.608, 0.115]
  - track 58 at frame 108: holes 0, rim-vs-core 0.48, rim-vs-outside 0.37, heterogeneity 0.12; core [0.941, 0.48, 0.964, 0.015] rim [0.732, 0.858, 0.76, 0.044]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 99 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial u (cell): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.909, rim/outside 5.05 (aggregate of 99 individuals; 0/99 membrane-like individually; rim level 0.798)
  - radial |P| (actin polarization): peak at rho=1.05 (in the peak band 0.5-1.5), rim/core 4.83, rim/outside 2.53 (aggregate of 99 individuals; 82/99 membrane-like individually; rim level 0.644)  MEMBRANE-LIKE
  - radial V/V0 (body content): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.911, rim/outside 5.08 (aggregate of 99 individuals; 0/99 membrane-like individually; rim level 0.682)
  - radial n (nutrient): peak at rho=2.15 (OUTSIDE the peak band 0.5-1.5), rim/core 1.43, rim/outside 0.865 (aggregate of 99 individuals; 0/99 membrane-like individually; rim level 0.201)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): |P| (actin polarization)
- membrane-like channels per top track at mid-life: #20 (t=395, R_eq 13.7): none; #22 (t=410, R_eq 16.95): ['|P| (actin polarization)']; #23 (t=410, R_eq 8.12): none; #58 (t=540, R_eq 17.62): ['|P| (actin polarization)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
