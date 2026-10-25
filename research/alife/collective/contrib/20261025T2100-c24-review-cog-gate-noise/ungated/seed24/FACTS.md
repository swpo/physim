# Evidence pack: lcn-cog (seed 24)

- world: `../../../20261025T1703-c18-cog-gate-is-slow-diffusion/world.py`, family `lenia`
- parent: threads/lenia-multichannel/worlds/rf-two56-mu0.01; mutation: unmodified r-two56 kernels on a closed food-waste cycle (losses become waste that regrows into food, no refill), full-domain noise
- run: 101 frames x 50 steps x dt 0.1 = time 500; grid [192, 192]; wall 109s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1703-c18-cog-gate-is-slow-diffusion/world.py --out collective/contrib/20261025T2100-c24-review-cog-gate-noise/ungated/seed24 --seeds 24 --frames 100 --spf 50 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.9996], min area 6 px

## Measurements
- components: final 8, mean 7.9, max 17; occupancy final 0.05
- tracks: 53; persistent (alive >= 50% of run): 8; longest 90 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.29 (1 = constant size)
- enclosures: components with a hole mean 5.31, final 5; holes at thresholds 0.2/0.35/0.5 final [0, 11, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [8, 8, 8], H1 [15, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.7
- replication (lineage window K = 20 frames = time 100, default): splits 11, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 4, merge/split ratio 0.364, nucleations 0
- channel total drift (end/start - 1): [-0.9609, -0.9102, 0.4646, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 27 at frame 56: holes 2, rim-vs-core 0.68, rim-vs-outside 0.49, heterogeneity 0.24; core [0.769, 0.426, 0.867, 0.048] rim [0.183, 0.772, 0.875, 0.042]
  - track 29 at frame 56: holes 0, rim-vs-core 0.71, rim-vs-outside 0.48, heterogeneity 0.24; core [0.802, 0.422, 0.905, 0.043] rim [0.177, 0.756, 0.914, 0.036]
  - track 33 at frame 56: holes 2, rim-vs-core 0.74, rim-vs-outside 0.52, heterogeneity 0.24; core [0.898, 0.463, 0.88, 0.051] rim [0.211, 0.748, 0.888, 0.042]
  - track 35 at frame 57: holes 2, rim-vs-core 0.65, rim-vs-outside 0.48, heterogeneity 0.24; core [0.903, 0.484, 0.903, 0.045] rim [0.285, 0.693, 0.912, 0.039]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 50 components >= 12 px at frames [17, 33, 50, 67, 83, 100]):
  - radial A0: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 0.123, rim/outside 9.89 (aggregate of 50 individuals; 2/50 membrane-like individually; rim level 0.0889)
  - radial A1: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1.28, rim/outside 88.3 (aggregate of 50 individuals; 2/50 membrane-like individually; rim level 0.913)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.08, rim/outside 0.94 (aggregate of 50 individuals; 0/50 membrane-like individually; rim level 0.767)
  - radial W: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.984, rim/outside 1.4 (aggregate of 50 individuals; 0/50 membrane-like individually; rim level 0.201)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #27 (t=280, R_eq 8.85): none; #29 (t=280, R_eq 8.92): none; #33 (t=280, R_eq 8.83): none; #35 (t=285, R_eq 8.88): none

## Warnings
- matter fills >80% of the domain at some point: components may be one connected sea
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 2 of 50 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
