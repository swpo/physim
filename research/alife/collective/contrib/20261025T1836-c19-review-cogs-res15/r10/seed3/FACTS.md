# Evidence pack: lcn-cog (seed 3)

- world: `../../../20261025T1621-c18-rtwo56-food-cogs-res15/world.py`, family `lenia`
- parent: threads/lenia-multichannel/worlds/rf-two56-mu0.01; mutation: unmodified r-two56 kernels on a closed food-waste cycle (losses become waste that regrows into food, no refill), full-domain noise
- run: 201 frames x 50 steps x dt 0.1 = time 1000; grid [192, 192]; wall 162s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1621-c18-rtwo56-food-cogs-res15/world.py --out collective/contrib/20261025T1836-c19-review-cogs-res15/r10/seed3 --seeds 3 --frames 200 --spf 50 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.9996], min area 6 px

## Measurements
- components: final 9, mean 9.7, max 21; occupancy final 0.06
- tracks: 76; persistent (alive >= 50% of run): 9; longest 193 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.57 (1 = constant size)
- enclosures: components with a hole mean 7.54, final 8; holes at thresholds 0.2/0.35/0.5 final [0, 19, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [9, 9, 9], H1 [23, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.5
- replication (lineage window K = 20 frames = time 100, default): splits 20, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 9, merge/split ratio 0.45, nucleations 3
- channel total drift (end/start - 1): [-0.9559, -0.8976, 0.4581, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 12 at frame 104: holes 0, rim-vs-core 0.71, rim-vs-outside 0.49, heterogeneity 0.24; core [0.797, 0.417, 0.921, 0.037] rim [0.174, 0.766, 0.929, 0.028]
  - track 22 at frame 106: holes 3, rim-vs-core 0.66, rim-vs-outside 0.52, heterogeneity 0.24; core [0.806, 0.468, 0.864, 0.051] rim [0.209, 0.753, 0.872, 0.048]
  - track 31 at frame 106: holes 2, rim-vs-core 0.70, rim-vs-outside 0.51, heterogeneity 0.24; core [0.761, 0.412, 0.88, 0.039] rim [0.173, 0.785, 0.887, 0.03]
  - track 32 at frame 106: holes 1, rim-vs-core 0.69, rim-vs-outside 0.48, heterogeneity 0.24; core [0.814, 0.42, 0.846, 0.044] rim [0.202, 0.742, 0.854, 0.037]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 56 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial A0: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.101, rim/outside 7.84 (aggregate of 56 individuals; 0/56 membrane-like individually; rim level 0.0711)
  - radial A1: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1.29, rim/outside 24.3 (aggregate of 56 individuals; 0/56 membrane-like individually; rim level 0.961)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.03, rim/outside 0.984 (aggregate of 56 individuals; 0/56 membrane-like individually; rim level 0.88)
  - radial W: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.894, rim/outside 1.5 (aggregate of 56 individuals; 0/56 membrane-like individually; rim level 0.0571)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #12 (t=520, R_eq 8.96): none; #22 (t=530, R_eq 8.87): none; #31 (t=530, R_eq 8.88): none; #32 (t=530, R_eq 8.74): none

## Warnings
- matter fills >80% of the domain at some point: components may be one connected sea
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
