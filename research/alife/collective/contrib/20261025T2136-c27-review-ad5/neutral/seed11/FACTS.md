# Evidence pack: ad5-evolve-neutral (seed 11)

- world: `../../world_neutral.py`, family `phase-field`
- parent: ad2-catalysts; mutation: N catalyst alleles with different rates, rare local mutation patches, random dilution disks
- run: 201 frames x 200 steps x dt 0.5 = time 20000; grid [128, 128]; wall 205s; status ok
- command: `python -m labkit.run collective/contrib/wip-c27g/world_neutral.py --out collective/contrib/wip-c27g/neutral --seeds 11 12 --frames 200`
- segmentation: matter > 0.43 of robust range [-1.063, 1.43], min area 6 px

## Measurements
- components: final 11, mean 9.3, max 11; occupancy final 0.11
- tracks: 16; persistent (alive >= 50% of run): 10; longest 201 frames; alive start-to-end: 1
- size of persistent tracks: max/min area ratio 3.80 (1 = constant size)
- enclosures: components with a hole mean 0.07, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [11, 11, 11], H1 [0, 0, 0]
- motion: 3 long-lived tracks moved >= 1 body length; max speed 0.00148/time; max body lengths 1.5
- replication (lineage window K = 20 frames = time 2000, default): splits 5, persistent splits 5 (0 more failed only because the siblings re-merged within K), max generation 1, merges 0, merge/split ratio 0, nucleations 0
- channel total drift (end/start - 1): [0.0947, -0.5841, 0.457, None, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 3 at frame 101: holes 0, rim-vs-core 0.40, rim-vs-outside 0.71, heterogeneity 0.06; core [0.953, 0.026, 0.0, 0.994, 0.0, 0.0] rim [0.703, 0.116, 0.0, 0.689, 0.0, 0.0]
  - track 6 at frame 116: holes 0, rim-vs-core 0.30, rim-vs-outside 0.77, heterogeneity 0.05; core [0.963, 0.033, 0.029, 0.0, 1.0, 0.0] rim [0.695, 0.121, 0.02, 0.0, 0.886, 0.0]
  - track 7 at frame 116: holes 0, rim-vs-core 0.39, rim-vs-outside 0.65, heterogeneity 0.08; core [0.968, 0.042, 0.72, 0.0, 0.344, 0.0] rim [0.711, 0.121, 0.461, 0.0, 0.226, 0.0]
  - track 8 at frame 119: holes 0, rim-vs-core 0.42, rim-vs-outside 0.64, heterogeneity 0.15; core [0.964, 0.031, 0.0, 0.797, 0.0, 0.24] rim [0.691, 0.113, 0.0, 0.489, 0.0, 0.226]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 58 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet material): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.935, rim/outside 55.4 (aggregate of 58 individuals; 0/58 membrane-like individually; rim level 0.91)
  - radial u (fuel): peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 13.9, rim/outside 0.693 (aggregate of 58 individuals; 0/58 membrane-like individually; rim level 0.215)
  - radial a0 (k=0.10): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.887, rim/outside 39.3 (aggregate of 58 individuals; 0/58 membrane-like individually; rim level 0.537)
  - radial a1 (k=0.12): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.957, rim/outside 14.9 (aggregate of 58 individuals; 0/58 membrane-like individually; rim level 0.143)
  - radial a2 (k=0.14): peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.97, rim/outside 9.04 (aggregate of 58 individuals; 0/58 membrane-like individually; rim level 0.0845)
  - radial a3 (k=0.16): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.983, rim/outside 17 (aggregate of 58 individuals; 0/58 membrane-like individually; rim level 0.164)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #3 (t=10100, R_eq 8.18): none; #6 (t=11600, R_eq 7.76): none; #7 (t=11600, R_eq 7.14): none; #8 (t=11900, R_eq 7.46): ['a3 (k=0.16)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
