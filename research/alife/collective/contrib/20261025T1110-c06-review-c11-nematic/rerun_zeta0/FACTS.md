# Evidence pack: active-nematic-droplets (seed 5)

- world: `../../20261025T1014-c11-active-nematic-colony/world.py`, family `active-nematic`
- parent: None; mutation: new class: CH droplets with internal Landau-de Gennes nematic order and extensile active stress, Brinkman-Stokes flow
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 372s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1014-c11-active-nematic-colony/world.py --out collective/contrib/20261025T1110-c06-review-c11-nematic/rerun_zeta0 --seeds 5 --frames 200 --no-movie`
- segmentation: matter > 0.47 of robust range [-0.8414, 0.9487], min area 6 px

## Measurements
- components: final 10, mean 9.1, max 10; occupancy final 0.07
- tracks: 10; persistent (alive >= 50% of run): 10; longest 195 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 19.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [11, 10, 10], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.9
- replication (lineage window K = 20 frames = time 100, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio n/a, nucleations 10
- channel total drift (end/start - 1): [-0.5101, -0.012, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 104: holes 0, rim-vs-core 0.46, rim-vs-outside 0.57, heterogeneity 0.18; core [0.964, 0.929, 0.451] rim [0.69, 0.56, 0.463]
  - track 1 at frame 108: holes 0, rim-vs-core 0.50, rim-vs-outside 0.31, heterogeneity 0.22; core [0.907, 0.839, 0.436] rim [0.593, 0.452, 0.433]
  - track 2 at frame 108: holes 0, rim-vs-core 0.48, rim-vs-outside 0.32, heterogeneity 0.24; core [0.905, 0.828, 0.465] rim [0.602, 0.454, 0.474]
  - track 3 at frame 108: holes 0, rim-vs-core 0.28, rim-vs-outside 0.73, heterogeneity 0.16; core [0.954, 0.916, 0.436] rim [0.786, 0.694, 0.454]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 60 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.898, rim/outside 30.1 (aggregate of 60 individuals; 0/60 membrane-like individually; rim level 0.893)
  - radial order |Q|: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.807, rim/outside 53.5 (aggregate of 60 individuals; 0/60 membrane-like individually; rim level 0.779)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=520, R_eq 6.08): none; #1 (t=540, R_eq 5.84): none; #2 (t=540, R_eq 5.38): none; #3 (t=540, R_eq 6.48): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
