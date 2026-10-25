# Evidence pack: lcn-cog (seed 5)

- world: `../../../20261025T1703-c18-cog-gate-is-slow-diffusion/world.py`, family `lenia`
- parent: threads/lenia-multichannel/worlds/rf-two56-mu0.01; mutation: unmodified r-two56 kernels on a closed food-waste cycle (losses become waste that regrows into food, no refill), full-domain noise
- run: 101 frames x 50 steps x dt 0.1 = time 500; grid [192, 192]; wall 76s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1703-c18-cog-gate-is-slow-diffusion/world.py --out collective/contrib/20261025T1921-c19-cog-gate-from-noise/gated/seed5 --seeds 5 --frames 100 --spf 50 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.9996], min area 6 px

## Measurements
- components: final 1, mean 2.2, max 27; occupancy final 0.01
- tracks: 77; persistent (alive >= 50% of run): 1; longest 90 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.30 (1 = constant size)
- enclosures: components with a hole mean 1.55, final 1; holes at thresholds 0.2/0.35/0.5 final [0, 2, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [1, 1, 1], H1 [3, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.7
- replication (lineage window K = 20 frames = time 100, default): splits 22, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 2, merge/split ratio 0.091, nucleations 1
- channel total drift (end/start - 1): [-0.9951, -0.9886, 0.4956, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 46 at frame 56: holes 3, rim-vs-core 0.73, rim-vs-outside 0.58, heterogeneity 0.27; core [0.886, 0.473, 0.424, 0.084] rim [0.208, 0.738, 0.519, 0.062]
  - track 14 at frame 14: holes 3, rim-vs-core 0.61, rim-vs-outside 0.59, heterogeneity 0.30; core [0.868, 0.189, 0.001, 0.827] rim [0.441, 0.576, 0.079, 0.656]
  - track 34 at frame 13: holes 2, rim-vs-core 0.64, rim-vs-outside 0.50, heterogeneity 0.28; core [0.678, 0.429, 0.07, 0.651] rim [0.154, 0.801, 0.088, 0.617]
  - track 50 at frame 13: holes 0, rim-vs-core 0.73, rim-vs-outside 0.58, heterogeneity 0.29; core [0.694, 0.434, 0.046, 0.71] rim [0.099, 0.84, 0.061, 0.628]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 8 components >= 12 px at frames [17, 33, 50, 67, 83, 100]):
  - radial A0: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 0.239, rim/outside 16.5 (aggregate of 8 individuals; 1/8 membrane-like individually; rim level 0.155)
  - radial A1: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1.27, rim/outside 72.8 (aggregate of 8 individuals; 0/8 membrane-like individually; rim level 0.894)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 3.21, rim/outside 0.881 (aggregate of 8 individuals; 0/8 membrane-like individually; rim level 0.715)
  - radial W: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 1, rim/outside 1.52 (aggregate of 8 individuals; 0/8 membrane-like individually; rim level 0.324)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #46 (t=280, R_eq 8.88): none; #14 (t=70, R_eq 15.23): ['A0']; #34 (t=65, R_eq 8.52): none; #50 (t=65, R_eq 8.63): none

## Warnings
- matter fills >80% of the domain at some point: components may be one connected sea
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
