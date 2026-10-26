# Evidence pack: ad5-evolve (seed 8)

- world: `../../../../threads/active-droplets/worlds/ad5-evolve/world.py`, family `phase-field`
- parent: ad2-catalysts; mutation: N catalyst alleles with different rates, rare local mutation patches, random dilution disks
- run: 201 frames x 200 steps x dt 0.5 = time 20000; grid [128, 128]; wall 303s; status ok
- command: `python -m labkit.run threads/active-droplets/worlds/ad5-evolve/world.py --out collective/contrib/wip-c33-ad5/pack8 --seeds 8 --frames 200 --no-movie`
- segmentation: matter > 0.42 of robust range [-1.0687, 1.4464], min area 6 px

## Measurements
- components: final 12, mean 8.6, max 12; occupancy final 0.12
- tracks: 20; persistent (alive >= 50% of run): 6; longest 201 frames; alive start-to-end: 3
- size of persistent tracks: max/min area ratio 8.76 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [12, 12, 12], H1 [0, 0, 0]
- motion: 2 long-lived tracks moved >= 1 body length; max speed 0.000879/time; max body lengths 1.2
- replication (lineage window K = 20 frames = time 2000, default): splits 7, persistent splits 6 (0 more failed only because the siblings re-merged within K), max generation 3, merges 0, merge/split ratio 0, nucleations 0
- channel total drift (end/start - 1): [0.101, -0.5998, -0.6896, None, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 2 at frame 101: holes 0, rim-vs-core 0.45, rim-vs-outside 0.68, heterogeneity 0.07; core [0.969, 0.126, 0.958, 0.0, 0.0, 0.0] rim [0.698, 0.218, 0.609, 0.0, 0.0, 0.0]
  - track 3 at frame 101: holes 0, rim-vs-core 0.45, rim-vs-outside 0.68, heterogeneity 0.07; core [0.969, 0.136, 0.951, 0.0, 0.0, 0.0] rim [0.699, 0.215, 0.604, 0.0, 0.0, 0.0]
  - track 4 at frame 101: holes 0, rim-vs-core 0.44, rim-vs-outside 0.69, heterogeneity 0.07; core [0.968, 0.128, 0.954, 0.0, 0.05, 0.0] rim [0.708, 0.214, 0.616, 0.0, 0.036, 0.0]
  - track 16 at frame 183: holes 0, rim-vs-core 0.46, rim-vs-outside 0.67, heterogeneity 0.07; core [0.955, 0.02, 0.0, 0.0, 0.0, 0.95] rim [0.683, 0.094, 0.0, 0.0, 0.0, 0.589]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 55 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet material): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.945, rim/outside 45.6 (aggregate of 55 individuals; 0/55 membrane-like individually; rim level 0.918)
  - radial u (fuel): peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 4.38, rim/outside 0.73 (aggregate of 55 individuals; 0/55 membrane-like individually; rim level 0.255)
  - radial a0 (k=0.10): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.909, rim/outside 35.2 (aggregate of 55 individuals; 0/55 membrane-like individually; rim level 0.399)
  - radial a1 (k=0.12): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.994, rim/outside 8.44 (aggregate of 55 individuals; 0/55 membrane-like individually; rim level 0.0761)
  - radial a2 (k=0.14): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.999, rim/outside 5.07 (aggregate of 55 individuals; 0/55 membrane-like individually; rim level 0.0448)
  - radial a3 (k=0.16): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.889, rim/outside 28 (aggregate of 55 individuals; 0/55 membrane-like individually; rim level 0.399)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #2 (t=10100, R_eq 7.84): none; #3 (t=10100, R_eq 7.09): none; #4 (t=10100, R_eq 7.53): none; #16 (t=18300, R_eq 7.33): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
