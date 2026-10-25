# Evidence pack: lcn-cog (seed 25)

- world: `../../../20261025T1703-c18-cog-gate-is-slow-diffusion/world.py`, family `lenia`
- parent: threads/lenia-multichannel/worlds/rf-two56-mu0.01; mutation: unmodified r-two56 kernels on a closed food-waste cycle (losses become waste that regrows into food, no refill), full-domain noise
- run: 101 frames x 50 steps x dt 0.1 = time 500; grid [192, 192]; wall 104s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1703-c18-cog-gate-is-slow-diffusion/world.py --out collective/contrib/20261025T2100-c24-review-cog-gate-noise/gated4/seed25 --seeds 25 --frames 100 --spf 50 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.9996], min area 6 px

## Measurements
- components: final 3, mean 4.6, max 29; occupancy final 0.02
- tracks: 89; persistent (alive >= 50% of run): 3; longest 90 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.20 (1 = constant size)
- enclosures: components with a hole mean 3.61, final 3; holes at thresholds 0.2/0.35/0.5 final [0, 4, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [3, 3, 3], H1 [8, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.6
- replication (lineage window K = 20 frames = time 100, default): splits 24, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 7, merge/split ratio 0.292, nucleations 2
- channel total drift (end/start - 1): [-0.9852, -0.966, 0.4843, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 38 at frame 56: holes 2, rim-vs-core 0.70, rim-vs-outside 0.53, heterogeneity 0.26; core [0.828, 0.469, 0.585, 0.069] rim [0.199, 0.751, 0.71, 0.054]
  - track 45 at frame 56: holes 1, rim-vs-core 0.71, rim-vs-outside 0.54, heterogeneity 0.27; core [0.778, 0.434, 0.56, 0.076] rim [0.174, 0.773, 0.702, 0.058]
  - track 67 at frame 57: holes 3, rim-vs-core 0.68, rim-vs-outside 0.53, heterogeneity 0.27; core [0.785, 0.456, 0.568, 0.076] rim [0.195, 0.765, 0.706, 0.06]
  - track 4 at frame 22: holes 1, rim-vs-core 0.46, rim-vs-outside 0.54, heterogeneity 0.27; core [0.602, 0.446, 0.319, 0.267] rim [0.276, 0.761, 0.422, 0.269]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 25 components >= 12 px at frames [17, 33, 50, 67, 83, 100]):
  - radial A0: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.149, rim/outside 12.1 (aggregate of 25 individuals; 0/25 membrane-like individually; rim level 0.116)
  - radial A1: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 1.29, rim/outside 52 (aggregate of 25 individuals; 0/25 membrane-like individually; rim level 0.935)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 2.08, rim/outside 0.954 (aggregate of 25 individuals; 0/25 membrane-like individually; rim level 0.758)
  - radial W: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.976, rim/outside 1.32 (aggregate of 25 individuals; 0/25 membrane-like individually; rim level 0.247)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #38 (t=280, R_eq 8.83): none; #45 (t=280, R_eq 8.92): none; #67 (t=285, R_eq 8.78): none; #4 (t=110, R_eq 8.48): none

## Warnings
- matter fills >80% of the domain at some point: components may be one connected sea
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
