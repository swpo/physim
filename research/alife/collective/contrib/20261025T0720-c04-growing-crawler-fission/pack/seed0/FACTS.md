# Evidence pack: crawler (seed 0)

- world: `../../crawler.py`, family `phase-field`
- parent: None; mutation: Ziebert-Aranson crawling cell, body-wise area constraint
- run: 121 frames x 100 steps x dt 0.05 = time 600; grid [256, 256]; wall 219s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/fba552f4-82e1-5fd3-8aee-1d1a9784fecc/scratchpad/cr/crawler.py --out /tmp/claude-0/-home-user-physim/fba552f4-82e1-5fd3-8aee-1d1a9784fecc/scratchpad/cr/okg --seeds 0 1 --frames 120 --no-movie`
- segmentation: matter > 0.59 of robust range [-0.0, 0.8422], min area 6 px

## Measurements
- components: final 21, mean 14.2, max 21; occupancy final 0.27
- tracks: 57; persistent (alive >= 50% of run): 9; longest 115 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 254.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [21, 21, 21], H1 [0, 0, 0]
- motion: 13 long-lived tracks moved >= 1 body length; max speed 0.643/time; max body lengths 3.5
- replication (lineage window K = 20 frames = time 100, default): splits 18, persistent splits 10 (0 more failed only because the siblings re-merged within K), max generation 4, merges 0, merge/split ratio 0, nucleations 19
- channel total drift (end/start - 1): [9.3009, 4.5613, None, -0.4571]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 2 at frame 64: holes 0, rim-vs-core 0.32, rim-vs-outside 0.21, heterogeneity 0.08; core [0.851, 0.388, 0.683, 0.216] rim [0.694, 0.634, 0.557, 0.235]
  - track 6 at frame 67: holes 0, rim-vs-core 0.14, rim-vs-outside 0.08, heterogeneity 0.04; core [0.712, 0.174, 0.588, 0.165] rim [0.649, 0.287, 0.536, 0.176]
  - track 17 at frame 77: holes 0, rim-vs-core 0.33, rim-vs-outside 0.26, heterogeneity 0.09; core [0.864, 0.317, 0.779, 0.093] rim [0.705, 0.566, 0.635, 0.117]
  - track 31 at frame 90: holes 0, rim-vs-core 0.25, rim-vs-outside 0.22, heterogeneity 0.07; core [0.747, 0.179, 0.726, 0.044] rim [0.67, 0.406, 0.651, 0.07]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 98 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial u (cell): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.91, rim/outside 5.42 (aggregate of 98 individuals; 0/98 membrane-like individually; rim level 0.808)
  - radial |P| (actin polarization): peak at rho=1.05 (in the peak band 0.5-1.5), rim/core 4.81, rim/outside 2.61 (aggregate of 98 individuals; 80/98 membrane-like individually; rim level 0.661)  MEMBRANE-LIKE
  - radial V/V0 (body content): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.915, rim/outside 5.4 (aggregate of 98 individuals; 0/98 membrane-like individually; rim level 0.664)
  - radial n (nutrient): peak at rho=2.15 (OUTSIDE the peak band 0.5-1.5), rim/core 1.42, rim/outside 0.865 (aggregate of 98 individuals; 0/98 membrane-like individually; rim level 0.212)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): |P| (actin polarization)
- membrane-like channels per top track at mid-life: #2 (t=320, R_eq 12.23): ['|P| (actin polarization)']; #6 (t=335, R_eq 9.79): none; #17 (t=385, R_eq 14.76): ['|P| (actin polarization)']; #31 (t=450, R_eq 17.36): ['|P| (actin polarization)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
