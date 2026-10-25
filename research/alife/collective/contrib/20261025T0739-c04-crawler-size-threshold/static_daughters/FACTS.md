# Evidence pack: crawler (seed 0)

- world: `../crawler.py`, family `phase-field`
- parent: None; mutation: Ziebert-Aranson crawling cell, body-wise area constraint
- run: 161 frames x 100 steps x dt 0.05 = time 800; grid [256, 256]; wall 283s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/fba552f4-82e1-5fd3-8aee-1d1a9784fecc/scratchpad/cr/crawler.py --out /tmp/claude-0/-home-user-physim/fba552f4-82e1-5fd3-8aee-1d1a9784fecc/scratchpad/cr/e14a --seeds 0 --frames 160 --no-movie`
- segmentation: matter > 0.70 of robust range [-0.0, 0.7107], min area 6 px

## Measurements
- components: final 4, mean 3.4, max 4; occupancy final 0.05
- tracks: 7; persistent (alive >= 50% of run): 4; longest 114 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 3.64 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [4, 4, 4], H1 [0, 0, 0]
- motion: 6 long-lived tracks moved >= 1 body length; max speed 0.157/time; max body lengths 1.9
- replication (lineage window K = 20 frames = time 100, default): splits 3, persistent splits 2 (0 more failed only because the siblings re-merged within K), max generation 1, merges 0, merge/split ratio 0, nucleations 0
- channel total drift (end/start - 1): [1.0174, 0.0508, None, -0.2157]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 3 at frame 104: holes 0, rim-vs-core 0.40, rim-vs-outside 0.29, heterogeneity 0.10; core [0.964, 0.434, 0.797, 0.043] rim [0.813, 0.781, 0.667, 0.103]
  - track 4 at frame 104: holes 0, rim-vs-core 0.40, rim-vs-outside 0.28, heterogeneity 0.10; core [0.963, 0.428, 0.833, 0.019] rim [0.813, 0.77, 0.698, 0.076]
  - track 5 at frame 105: holes 0, rim-vs-core 0.40, rim-vs-outside 0.29, heterogeneity 0.10; core [0.962, 0.431, 0.832, 0.03] rim [0.812, 0.774, 0.696, 0.09]
  - track 6 at frame 105: holes 0, rim-vs-core 0.40, rim-vs-outside 0.29, heterogeneity 0.10; core [0.964, 0.441, 0.76, 0.037] rim [0.814, 0.79, 0.636, 0.095]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 22 components >= 12 px at frames [27, 54, 81, 106, 133, 160]):
  - radial u (cell): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.923, rim/outside 9.99 (aggregate of 22 individuals; 0/22 membrane-like individually; rim level 0.919)
  - radial |P| (actin polarization): peak at rho=1.25 (in the peak band 0.5-1.5), rim/core 5.1, rim/outside 2.69 (aggregate of 22 individuals; 22/22 membrane-like individually; rim level 0.939)  MEMBRANE-LIKE
  - radial V/V0 (body content): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.922, rim/outside 71.6 (aggregate of 22 individuals; 0/22 membrane-like individually; rim level 0.75)
  - radial n (nutrient): peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 2.58, rim/outside 0.587 (aggregate of 22 individuals; 0/22 membrane-like individually; rim level 0.201)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): |P| (actin polarization)
- membrane-like channels per top track at mid-life: #3 (t=520, R_eq 14.71): ['|P| (actin polarization)']; #4 (t=520, R_eq 14.88): ['|P| (actin polarization)']; #5 (t=525, R_eq 14.93): ['|P| (actin polarization)']; #6 (t=525, R_eq 14.51): ['|P| (actin polarization)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
