# Evidence pack: ad5-evolve (seed 12)

- world: `../../world.py`, family `phase-field`
- parent: ad2-catalysts; mutation: N catalyst alleles with different rates, rare local mutation patches, random dilution disks
- run: 201 frames x 200 steps x dt 0.5 = time 20000; grid [128, 128]; wall 203s; status ok
- command: `python -m labkit.run collective/contrib/wip-c27g/world.py --out collective/contrib/wip-c27g/rerun --seeds 11 12 --frames 200`
- segmentation: matter > 0.42 of robust range [-1.0687, 1.4491], min area 6 px

## Measurements
- components: final 12, mean 8.2, max 12; occupancy final 0.12
- tracks: 19; persistent (alive >= 50% of run): 5; longest 201 frames; alive start-to-end: 1
- size of persistent tracks: max/min area ratio 2.95 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [12, 12, 12], H1 [0, 0, 0]
- motion: 2 long-lived tracks moved >= 1 body length; max speed 0.00232/time; max body lengths 1.3
- replication (lineage window K = 20 frames = time 2000, default): splits 7, persistent splits 6 (0 more failed only because the siblings re-merged within K), max generation 2, merges 0, merge/split ratio 0, nucleations 0
- channel total drift (end/start - 1): [0.1049, -0.6063, -0.6978, None, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 3 at frame 101: holes 0, rim-vs-core 0.43, rim-vs-outside 0.68, heterogeneity 0.07; core [0.968, 0.111, 0.96, 0.0, 0.0, 0.0] rim [0.713, 0.206, 0.625, 0.0, 0.0, 0.0]
  - track 5 at frame 104: holes 0, rim-vs-core 0.43, rim-vs-outside 0.69, heterogeneity 0.07; core [0.972, 0.12, 0.958, 0.0, 0.0, 0.0] rim [0.713, 0.204, 0.621, 0.0, 0.0, 0.0]
  - track 6 at frame 104: holes 0, rim-vs-core 0.30, rim-vs-outside 0.81, heterogeneity 0.07; core [0.97, 0.12, 0.954, 0.0, 0.0, 0.0] rim [0.79, 0.18, 0.722, 0.0, 0.0, 0.0]
  - track 11 at frame 166: holes 0, rim-vs-core 0.28, rim-vs-outside 0.83, heterogeneity 0.07; core [0.948, 0.014, 0.0, 0.0, 0.0, 0.959] rim [0.782, 0.056, 0.0, 0.0, 0.0, 0.74]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 52 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet material): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.937, rim/outside 52.4 (aggregate of 52 individuals; 0/52 membrane-like individually; rim level 0.902)
  - radial u (fuel): peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 5.32, rim/outside 0.713 (aggregate of 52 individuals; 0/52 membrane-like individually; rim level 0.244)
  - radial a0 (k=0.10): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.898, rim/outside 34.9 (aggregate of 52 individuals; 0/52 membrane-like individually; rim level 0.372)
  - radial a1 (k=0.12): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.929, rim/outside 11.8 (aggregate of 52 individuals; 0/52 membrane-like individually; rim level 0.113)
  - radial a2 (k=0.14): peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1, rim/outside 14.7 (aggregate of 52 individuals; 1/52 membrane-like individually; rim level 0.151)
  - radial a3 (k=0.16): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.899, rim/outside 30.7 (aggregate of 52 individuals; 1/52 membrane-like individually; rim level 0.365)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #3 (t=10100, R_eq 8): none; #5 (t=10400, R_eq 7.4): none; #6 (t=10400, R_eq 7.36): none; #11 (t=16600, R_eq 7.8): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
