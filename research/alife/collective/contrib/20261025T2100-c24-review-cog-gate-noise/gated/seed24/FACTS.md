# Evidence pack: lcn-cog (seed 24)

- world: `../../../20261025T1703-c18-cog-gate-is-slow-diffusion/world.py`, family `lenia`
- parent: threads/lenia-multichannel/worlds/rf-two56-mu0.01; mutation: unmodified r-two56 kernels on a closed food-waste cycle (losses become waste that regrows into food, no refill), full-domain noise
- run: 101 frames x 50 steps x dt 0.1 = time 500; grid [192, 192]; wall 104s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1703-c18-cog-gate-is-slow-diffusion/world.py --out collective/contrib/20261025T2100-c24-review-cog-gate-noise/gated/seed24 --seeds 24 --frames 100 --spf 50 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.9996], min area 6 px

## Measurements
- components: final 1, mean 1.9, max 13; occupancy final 0.01
- tracks: 53; persistent (alive >= 50% of run): 1; longest 88 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.18 (1 = constant size)
- enclosures: components with a hole mean 1.45, final 1; holes at thresholds 0.2/0.35/0.5 final [0, 2, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [1, 1, 1], H1 [3, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.7
- replication (lineage window K = 20 frames = time 100, default): splits 13, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 3, merge/split ratio 0.231, nucleations 0
- channel total drift (end/start - 1): [-0.9951, -0.9888, 0.4961, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 38 at frame 57: holes 1, rim-vs-core 0.70, rim-vs-outside 0.56, heterogeneity 0.28; core [0.755, 0.412, 0.466, 0.073] rim [0.164, 0.784, 0.517, 0.061]
  - track 21 at frame 15: holes 6, rim-vs-core 0.51, rim-vs-outside 0.65, heterogeneity 0.31; core [0.787, 0.176, 0.014, 0.816] rim [0.466, 0.544, 0.077, 0.694]
  - track 22 at frame 14: holes 2, rim-vs-core 0.43, rim-vs-outside 0.45, heterogeneity 0.28; core [0.782, 0.751, 0.025, 0.716] rim [0.368, 0.637, 0.056, 0.691]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 11 components >= 12 px at frames [17, 33, 50, 67, 83, 100]):
  - radial A0: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 0.344, rim/outside 24.1 (aggregate of 11 individuals; 1/11 membrane-like individually; rim level 0.231)
  - radial A1: peak at rho=0.95 (in the peak band 0.5-1.5), rim/core 1.33, rim/outside 47.6 (aggregate of 11 individuals; 2/11 membrane-like individually; rim level 0.806)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 3.65, rim/outside 0.805 (aggregate of 11 individuals; 0/11 membrane-like individually; rim level 0.57)
  - radial W: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.09, rim/outside 1.46 (aggregate of 11 individuals; 0/11 membrane-like individually; rim level 0.479)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #38 (t=285, R_eq 8.81): none; #0 (t=20, R_eq 96.8): none; #21 (t=75, R_eq 15.77, ring): ['A0', 'A1']; #22 (t=70, R_eq 8.87, ring): ['A1']

## Warnings
- matter fills >80% of the domain at some point: components may be one connected sea
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 1 of 11 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
