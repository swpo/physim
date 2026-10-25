# Evidence pack: ad5-evolve-neutral (seed 12)

- world: `../../world_neutral.py`, family `phase-field`
- parent: ad2-catalysts; mutation: N catalyst alleles with different rates, rare local mutation patches, random dilution disks
- run: 201 frames x 200 steps x dt 0.5 = time 20000; grid [128, 128]; wall 198s; status ok
- command: `python -m labkit.run collective/contrib/wip-c27g/world_neutral.py --out collective/contrib/wip-c27g/neutral --seeds 11 12 --frames 200`
- segmentation: matter > 0.43 of robust range [-1.0634, 1.4243], min area 6 px

## Measurements
- components: final 10, mean 9.2, max 10; occupancy final 0.11
- tracks: 15; persistent (alive >= 50% of run): 10; longest 195 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.92 (1 = constant size)
- enclosures: components with a hole mean 0.04, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [10, 10, 10], H1 [0, 0, 0]
- motion: 2 long-lived tracks moved >= 1 body length; max speed 0.000993/time; max body lengths 1.2
- replication (lineage window K = 20 frames = time 2000, default): splits 5, persistent splits 5 (0 more failed only because the siblings re-merged within K), max generation 1, merges 0, merge/split ratio 0, nucleations 0
- channel total drift (end/start - 1): [0.0884, -0.5732, -0.0926, None, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 5 at frame 104: holes 0, rim-vs-core 0.46, rim-vs-outside 0.68, heterogeneity 0.07; core [0.962, 0.034, 0.0, 0.0, 0.967, 0.0] rim [0.689, 0.12, 0.0, 0.0, 0.611, 0.0]
  - track 6 at frame 104: holes 0, rim-vs-core 0.35, rim-vs-outside 0.78, heterogeneity 0.07; core [0.971, 0.033, 0.953, 0.0, 0.0, 0.0] rim [0.764, 0.1, 0.685, 0.0, 0.0, 0.0]
  - track 7 at frame 116: holes 0, rim-vs-core 0.44, rim-vs-outside 0.69, heterogeneity 0.07; core [0.964, 0.031, 0.0, 0.0, 0.971, 0.0] rim [0.705, 0.119, 0.0, 0.0, 0.628, 0.0]
  - track 8 at frame 116: holes 0, rim-vs-core 0.38, rim-vs-outside 0.73, heterogeneity 0.06; core [0.961, 0.03, 0.002, 1.0, 0.0, 0.0] rim [0.711, 0.12, 0.001, 0.722, 0.0, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 58 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet material): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.944, rim/outside 61.9 (aggregate of 58 individuals; 0/58 membrane-like individually; rim level 0.932)
  - radial u (fuel): peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 16.6, rim/outside 0.696 (aggregate of 58 individuals; 0/58 membrane-like individually; rim level 0.221)
  - radial a0 (k=0.10): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.908, rim/outside 35.3 (aggregate of 58 individuals; 1/58 membrane-like individually; rim level 0.405)
  - radial a1 (k=0.12): peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.941, rim/outside 13.5 (aggregate of 58 individuals; 0/58 membrane-like individually; rim level 0.131)
  - radial a2 (k=0.14): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.922, rim/outside 22.4 (aggregate of 58 individuals; 0/58 membrane-like individually; rim level 0.236)
  - radial a3 (k=0.16): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.967, rim/outside 16.6 (aggregate of 58 individuals; 0/58 membrane-like individually; rim level 0.16)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #5 (t=10400, R_eq 7.72): none; #6 (t=10400, R_eq 7.44): none; #7 (t=11600, R_eq 7.86): none; #8 (t=11600, R_eq 7.94): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
