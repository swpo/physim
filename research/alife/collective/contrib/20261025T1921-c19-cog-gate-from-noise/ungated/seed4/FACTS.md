# Evidence pack: lcn-cog (seed 4)

- world: `../../../20261025T1703-c18-cog-gate-is-slow-diffusion/world.py`, family `lenia`
- parent: threads/lenia-multichannel/worlds/rf-two56-mu0.01; mutation: unmodified r-two56 kernels on a closed food-waste cycle (losses become waste that regrows into food, no refill), full-domain noise
- run: 101 frames x 50 steps x dt 0.1 = time 500; grid [192, 192]; wall 82s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1703-c18-cog-gate-is-slow-diffusion/world.py --out collective/contrib/20261025T1921-c19-cog-gate-from-noise/ungated/seed4 --seeds 4 --frames 100 --spf 50 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.9996], min area 6 px

## Measurements
- components: final 13, mean 13.1, max 20; occupancy final 0.08
- tracks: 114; persistent (alive >= 50% of run): 13; longest 92 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.13 (1 = constant size)
- enclosures: components with a hole mean 9.56, final 11; holes at thresholds 0.2/0.35/0.5 final [0, 24, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [16, 13, 13], H1 [39, 0, 0]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 0.336/time; max body lengths 2.0
- replication (lineage window K = 20 frames = time 100, default): splits 28, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 20, merge/split ratio 0.714, nucleations 5
- channel total drift (end/start - 1): [-0.936, -0.8521, 0.4408, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 18 at frame 55: holes 3, rim-vs-core 0.79, rim-vs-outside 0.46, heterogeneity 0.24; core [0.906, 0.407, 0.891, 0.054] rim [0.199, 0.753, 0.899, 0.048]
  - track 20 at frame 55: holes 2, rim-vs-core 0.78, rim-vs-outside 0.49, heterogeneity 0.24; core [0.921, 0.426, 0.871, 0.06] rim [0.209, 0.741, 0.881, 0.054]
  - track 31 at frame 55: holes 1, rim-vs-core 0.72, rim-vs-outside 0.52, heterogeneity 0.24; core [0.799, 0.425, 0.905, 0.043] rim [0.174, 0.772, 0.912, 0.036]
  - track 38 at frame 56: holes 2, rim-vs-core 0.69, rim-vs-outside 0.50, heterogeneity 0.24; core [0.847, 0.475, 0.853, 0.055] rim [0.21, 0.745, 0.862, 0.049]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 83 components >= 12 px at frames [17, 33, 50, 67, 83, 100]):
  - radial A0: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 0.27, rim/outside 9.47 (aggregate of 83 individuals; 7/83 membrane-like individually; rim level 0.197)
  - radial A1: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1.3, rim/outside 12.8 (aggregate of 83 individuals; 7/83 membrane-like individually; rim level 0.891)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.09, rim/outside 0.943 (aggregate of 83 individuals; 0/83 membrane-like individually; rim level 0.735)
  - radial W: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.947, rim/outside 1.35 (aggregate of 83 individuals; 0/83 membrane-like individually; rim level 0.221)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #18 (t=275, R_eq 8.61): none; #20 (t=275, R_eq 8.79): none; #31 (t=275, R_eq 8.97): none; #38 (t=280, R_eq 8.87): none

## Warnings
- matter fills >80% of the domain at some point: components may be one connected sea
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 7 of 83 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
