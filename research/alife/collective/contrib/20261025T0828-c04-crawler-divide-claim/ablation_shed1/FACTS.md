# Evidence pack: crawler (seed 0)

- world: `../crawler.py`, family `phase-field`
- parent: None; mutation: Ziebert-Aranson crawling cell, body-wise area constraint
- run: 241 frames x 50 steps x dt 0.05 = time 600; grid [256, 256]; wall 225s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/fba552f4-82e1-5fd3-8aee-1d1a9784fecc/scratchpad/cr/crawler.py --out /tmp/claude-0/-home-user-physim/fba552f4-82e1-5fd3-8aee-1d1a9784fecc/scratchpad/cr/sh1.0 --seeds 0 --frames 240 --threshold 0.25 --no-movie`
- segmentation: matter > 0.37 of robust range [-0.0, 0.6697], min area 6 px

## Measurements
- components: final 1, mean 1.0, max 1; occupancy final 0.01
- tracks: 1; persistent (alive >= 50% of run): 1; longest 241 frames; alive start-to-end: 1
- size of persistent tracks: max/min area ratio 3.05 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [1, 1, 1], H1 [0, 0, 0]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 2.77/time; max body lengths 54.1
- replication (lineage window K = 20 frames = time 50, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio n/a, nucleations 0
- channel total drift (end/start - 1): [-0.6825, -0.6843, None, -0.1011]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 121: holes 0, rim-vs-core 0.34, rim-vs-outside 0.70, heterogeneity 0.20; core [0.912, 0.573, 0.901, 0.224] rim [0.703, 0.722, 0.69, 0.291]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 6 components >= 12 px at frames [40, 81, 121, 159, 200, 240]):
  - radial u (cell): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.823, rim/outside 10.7 (aggregate of 6 individuals; 0/6 membrane-like individually; rim level 0.789)
  - radial |P| (actin polarization): peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.64, rim/outside 4.78 (aggregate of 6 individuals; 6/6 membrane-like individually; rim level 0.647)  MEMBRANE-LIKE
  - radial V/V0 (body content): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.814, rim/outside 72.8 (aggregate of 6 individuals; 0/6 membrane-like individually; rim level 0.772)
  - radial n (nutrient): peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 2.11, rim/outside 0.816 (aggregate of 6 individuals; 0/6 membrane-like individually; rim level 0.334)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): |P| (actin polarization)
- membrane-like channels per top track at mid-life: #0 (t=302.5, R_eq 17.09): ['|P| (actin polarization)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
