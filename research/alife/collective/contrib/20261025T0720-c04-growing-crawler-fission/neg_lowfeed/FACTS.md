# Evidence pack: crawler (seed 0)

- world: `../crawler.py`, family `phase-field`
- parent: None; mutation: Ziebert-Aranson crawling cell, body-wise area constraint
- run: 161 frames x 100 steps x dt 0.05 = time 800; grid [256, 256]; wall 292s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/fba552f4-82e1-5fd3-8aee-1d1a9784fecc/scratchpad/cr/crawler.py --out /tmp/claude-0/-home-user-physim/fba552f4-82e1-5fd3-8aee-1d1a9784fecc/scratchpad/cr/okr0.003 --seeds 0 --frames 160 --no-movie`
- segmentation: matter > 0.64 of robust range [-0.0, 0.787], min area 6 px

## Measurements
- components: final 16, mean 13.0, max 16; occupancy final 0.15
- tracks: 38; persistent (alive >= 50% of run): 16; longest 138 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 137.67 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [16, 16, 16], H1 [0, 0, 0]
- motion: 16 long-lived tracks moved >= 1 body length; max speed 0.63/time; max body lengths 4.0
- replication (lineage window K = 20 frames = time 100, default): splits 5, persistent splits 4 (0 more failed only because the siblings re-merged within K), max generation 2, merges 0, merge/split ratio 0, nucleations 26
- channel total drift (end/start - 1): [5.5584, 2.7978, None, -0.646]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 10 at frame 91: holes 0, rim-vs-core 0.23, rim-vs-outside 0.15, heterogeneity 0.05; core [0.854, 0.288, 0.102, 0.069] rim [0.738, 0.487, 0.088, 0.077]
  - track 13 at frame 94: holes 0, rim-vs-core 0.30, rim-vs-outside 0.21, heterogeneity 0.06; core [0.896, 0.312, 0.113, 0.055] rim [0.756, 0.573, 0.095, 0.067]
  - track 17 at frame 104: holes 0, rim-vs-core 0.29, rim-vs-outside 0.25, heterogeneity 0.07; core [0.907, 0.315, 0.114, 0.026] rim [0.775, 0.573, 0.098, 0.036]
  - track 5 at frame 38: holes 0, rim-vs-core 0.32, rim-vs-outside 0.21, heterogeneity 0.09; core [0.868, 0.35, 0.946, 0.519] rim [0.741, 0.612, 0.81, 0.533]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 86 components >= 12 px at frames [27, 54, 81, 106, 133, 160]):
  - radial u (cell): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.911, rim/outside 6.8 (aggregate of 86 individuals; 0/86 membrane-like individually; rim level 0.854)
  - radial |P| (actin polarization): peak at rho=1.15 (in the peak band 0.5-1.5), rim/core 5.01, rim/outside 2.55 (aggregate of 86 individuals; 77/86 membrane-like individually; rim level 0.72)  MEMBRANE-LIKE
  - radial V/V0 (body content): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.914, rim/outside 4.66 (aggregate of 86 individuals; 0/86 membrane-like individually; rim level 0.147)
  - radial n (nutrient): peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.26, rim/outside 0.867 (aggregate of 86 individuals; 0/86 membrane-like individually; rim level 0.153)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): |P| (actin polarization)
- membrane-like channels per top track at mid-life: #10 (t=455, R_eq 11.53): ['|P| (actin polarization)']; #13 (t=470, R_eq 14.28): ['|P| (actin polarization)']; #17 (t=520, R_eq 14.55): ['|P| (actin polarization)']; #5 (t=190, R_eq 13.11): ['|P| (actin polarization)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
