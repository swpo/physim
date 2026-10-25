# Evidence pack: crawler-divide (seed 1)

- world: `../cdiv.py`, family `phase-field`
- parent: None; mutation: growth by uptake, finite-range area penalty (division), food-modulated actin, shedding on retraction
- run: 241 frames x 50 steps x dt 0.05 = time 600; grid [256, 256]; wall 235s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/fba552f4-82e1-5fd3-8aee-1d1a9784fecc/scratchpad/cr/cdiv.py --out /tmp/claude-0/-home-user-physim/fba552f4-82e1-5fd3-8aee-1d1a9784fecc/scratchpad/cr/ocs0.2 --seeds 1 --frames 240 --no-movie`
- segmentation: matter > 0.26 of robust range [-0.0, 0.9478], min area 6 px

## Measurements
- components: final 2, mean 2.1, max 3; occupancy final 0.04
- tracks: 8; persistent (alive >= 50% of run): 1; longest 166 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.16 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [2, 2, 2], H1 [0, 0, 0]
- motion: 6 long-lived tracks moved >= 1 body length; max speed 2.77/time; max body lengths 16.3
- replication (lineage window K = 20 frames = time 50, default): splits 3, persistent splits 2 (0 more failed only because the siblings re-merged within K), max generation 2, merges 1, merge/split ratio 0.333, nucleations 0
- channel total drift (end/start - 1): [0.0374, -0.5575, None, -0.4027]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 4 at frame 157: holes 0, rim-vs-core 0.36, rim-vs-outside 0.57, heterogeneity 0.15; core [0.87, 0.32, 0.431, 0.031] rim [0.551, 0.385, 0.273, 0.052]
  - track 2 at frame 113: holes 0, rim-vs-core 0.33, rim-vs-outside 0.63, heterogeneity 0.17; core [0.789, 0.341, 0.37, 0.261] rim [0.542, 0.515, 0.254, 0.314]
  - track 3 at frame 119: holes 0, rim-vs-core 0.35, rim-vs-outside 0.58, heterogeneity 0.15; core [0.805, 0.298, 0.353, 0.131] rim [0.531, 0.462, 0.233, 0.184]
  - track 0 at frame 30: holes 0, rim-vs-core 0.29, rim-vs-outside 0.94, heterogeneity 0.22; core [0.792, 0.402, 0.817, 0.722] rim [0.634, 0.574, 0.65, 0.776]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 14 components >= 12 px at frames [40, 81, 121, 159, 200, 240]):
  - radial u (cell): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.738, rim/outside 12 (aggregate of 14 individuals; 0/14 membrane-like individually; rim level 0.644)
  - radial |P| (actin polarization): peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.52, rim/outside 10.8 (aggregate of 14 individuals; 8/14 membrane-like individually; rim level 0.376)  MEMBRANE-LIKE
  - radial V/V0 (body content): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.694, rim/outside 11.2 (aggregate of 14 individuals; 0/14 membrane-like individually; rim level 0.292)
  - radial n (nutrient): peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.47, rim/outside 0.884 (aggregate of 14 individuals; 0/14 membrane-like individually; rim level 0.31)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): |P| (actin polarization)
- membrane-like channels per top track at mid-life: #4 (t=392.5, R_eq 25.93): ['|P| (actin polarization)']; #2 (t=282.5, R_eq 25.69): none; #3 (t=297.5, R_eq 24.91): ['|P| (actin polarization)']; #0 (t=75, R_eq 36.77): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
