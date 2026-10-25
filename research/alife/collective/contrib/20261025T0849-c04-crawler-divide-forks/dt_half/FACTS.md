# Evidence pack: crawler-divide (seed 1)

- world: `../cdiv.py`, family `phase-field`
- parent: None; mutation: growth by uptake, finite-range area penalty (division), food-modulated actin, shedding on retraction
- run: 241 frames x 100 steps x dt 0.025 = time 600; grid [256, 256]; wall 457s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/fba552f4-82e1-5fd3-8aee-1d1a9784fecc/scratchpad/cr/cdiv.py --out /tmp/claude-0/-home-user-physim/fba552f4-82e1-5fd3-8aee-1d1a9784fecc/scratchpad/cr/dt2 --seeds 1 --frames 240 --no-movie`
- segmentation: matter > 0.35 of robust range [-0.0, 0.7236], min area 6 px

## Measurements
- components: final 16, mean 9.4, max 16; occupancy final 0.22
- tracks: 39; persistent (alive >= 50% of run): 2; longest 188 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.46 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [16, 16, 16], H1 [0, 0, 0]
- motion: 18 long-lived tracks moved >= 1 body length; max speed 2.53/time; max body lengths 10.7
- replication (lineage window K = 20 frames = time 50, default): splits 17, persistent splits 15 (0 more failed only because the siblings re-merged within K), max generation 5, merges 2, merge/split ratio 0.118, nucleations 2
- channel total drift (end/start - 1): [3.4261, 1.1794, None, -0.6076]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 11 at frame 147: holes 0, rim-vs-core 0.17, rim-vs-outside 0.39, heterogeneity 0.08; core [0.654, 0.178, 0.405, 0.34] rim [0.558, 0.304, 0.346, 0.355]
  - track 24 at frame 177: holes 0, rim-vs-core 0.33, rim-vs-outside 0.45, heterogeneity 0.09; core [0.712, 0.157, 0.707, 0.194] rim [0.501, 0.298, 0.498, 0.217]
  - track 25 at frame 184: holes 0, rim-vs-core 0.38, rim-vs-outside 0.47, heterogeneity 0.10; core [0.762, 0.187, 0.755, 0.148] rim [0.513, 0.323, 0.508, 0.171]
  - track 26 at frame 184: holes 0, rim-vs-core 0.14, rim-vs-outside 0.59, heterogeneity 0.09; core [0.711, 0.208, 0.677, 0.169] rim [0.612, 0.245, 0.583, 0.178]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 64 components >= 12 px at frames [40, 81, 121, 159, 200, 240]):
  - radial u (cell): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.817, rim/outside 15.9 (aggregate of 64 individuals; 0/64 membrane-like individually; rim level 0.681)
  - radial |P| (actin polarization): peak at rho=0.95 (in the peak band 0.5-1.5), rim/core 3.03, rim/outside 5.64 (aggregate of 64 individuals; 63/64 membrane-like individually; rim level 0.358)  MEMBRANE-LIKE
  - radial V/V0 (body content): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.815, rim/outside 27.2 (aggregate of 64 individuals; 0/64 membrane-like individually; rim level 0.468)
  - radial n (nutrient): peak at rho=2.15 (OUTSIDE the peak band 0.5-1.5), rim/core 1.15, rim/outside 0.942 (aggregate of 64 individuals; 0/64 membrane-like individually; rim level 0.29)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): |P| (actin polarization)
- membrane-like channels per top track at mid-life: #11 (t=367.5, R_eq 18.12): ['|P| (actin polarization)']; #24 (t=442.5, R_eq 19.56): ['|P| (actin polarization)']; #25 (t=460, R_eq 19.32): ['|P| (actin polarization)']; #26 (t=460, R_eq 19.23): ['|P| (actin polarization)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
