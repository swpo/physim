# Evidence pack: crawler (seed 0)

- world: `../crawler.py`, family `phase-field`
- parent: None; mutation: Ziebert-Aranson crawling cell, body-wise area constraint
- run: 241 frames x 50 steps x dt 0.05 = time 600; grid [256, 256]; wall 222s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/fba552f4-82e1-5fd3-8aee-1d1a9784fecc/scratchpad/cr/crawler.py --out /tmp/claude-0/-home-user-physim/fba552f4-82e1-5fd3-8aee-1d1a9784fecc/scratchpad/cr/sh0.5 --seeds 0 --frames 240 --threshold 0.25 --no-movie`
- segmentation: matter > 0.33 of robust range [-0.0, 0.7465], min area 6 px

## Measurements
- components: final 6, mean 4.0, max 6; occupancy final 0.10
- tracks: 14; persistent (alive >= 50% of run): 4; longest 217 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 9.50 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [6, 6, 6], H1 [0, 0, 0]
- motion: 8 long-lived tracks moved >= 1 body length; max speed 2.55/time; max body lengths 40.2
- replication (lineage window K = 20 frames = time 50, default): splits 6, persistent splits 4 (0 more failed only because the siblings re-merged within K), max generation 3, merges 1, merge/split ratio 0.167, nucleations 0
- channel total drift (end/start - 1): [0.8169, 0.2126, None, -0.3557]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 3 at frame 133: holes 0, rim-vs-core 0.36, rim-vs-outside 0.62, heterogeneity 0.18; core [0.797, 0.374, 0.725, 0.326] rim [0.581, 0.573, 0.527, 0.354]
  - track 5 at frame 127: holes 0, rim-vs-core 0.35, rim-vs-outside 0.64, heterogeneity 0.18; core [0.817, 0.396, 0.709, 0.318] rim [0.598, 0.592, 0.517, 0.346]
  - track 8 at frame 147: holes 0, rim-vs-core 0.35, rim-vs-outside 0.60, heterogeneity 0.17; core [0.8, 0.358, 0.692, 0.259] rim [0.58, 0.559, 0.501, 0.287]
  - track 10 at frame 210: holes 0, rim-vs-core 0.38, rim-vs-outside 0.59, heterogeneity 0.16; core [0.774, 0.3, 0.82, 0.122] rim [0.548, 0.494, 0.584, 0.153]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 27 components >= 12 px at frames [40, 81, 121, 159, 200, 240]):
  - radial u (cell): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.832, rim/outside 13.7 (aggregate of 27 individuals; 0/27 membrane-like individually; rim level 0.67)
  - radial |P| (actin polarization): peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 2.14, rim/outside 5.48 (aggregate of 27 individuals; 24/27 membrane-like individually; rim level 0.428)  MEMBRANE-LIKE
  - radial V/V0 (body content): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.834, rim/outside 39.6 (aggregate of 27 individuals; 0/27 membrane-like individually; rim level 0.627)
  - radial n (nutrient): peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.25, rim/outside 0.924 (aggregate of 27 individuals; 0/27 membrane-like individually; rim level 0.339)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): |P| (actin polarization)
- membrane-like channels per top track at mid-life: #3 (t=332.5, R_eq 18.3): ['|P| (actin polarization)']; #5 (t=317.5, R_eq 18.01): ['|P| (actin polarization)']; #8 (t=367.5, R_eq 18.02): ['|P| (actin polarization)']; #10 (t=525, R_eq 18.46): ['|P| (actin polarization)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
