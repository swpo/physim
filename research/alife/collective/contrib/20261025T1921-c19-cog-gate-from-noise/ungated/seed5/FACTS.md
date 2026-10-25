# Evidence pack: lcn-cog (seed 5)

- world: `../../../20261025T1703-c18-cog-gate-is-slow-diffusion/world.py`, family `lenia`
- parent: threads/lenia-multichannel/worlds/rf-two56-mu0.01; mutation: unmodified r-two56 kernels on a closed food-waste cycle (losses become waste that regrows into food, no refill), full-domain noise
- run: 101 frames x 50 steps x dt 0.1 = time 500; grid [192, 192]; wall 77s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1703-c18-cog-gate-is-slow-diffusion/world.py --out collective/contrib/20261025T1921-c19-cog-gate-from-noise/ungated/seed5 --seeds 5 --frames 100 --spf 50 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.9996], min area 6 px

## Measurements
- components: final 12, mean 11.6, max 25; occupancy final 0.08
- tracks: 108; persistent (alive >= 50% of run): 9; longest 92 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.54 (1 = constant size)
- enclosures: components with a hole mean 9.77, final 10; holes at thresholds 0.2/0.35/0.5 final [0, 28, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [13, 12, 12], H1 [42, 0, 0]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 0.268/time; max body lengths 1.1
- replication (lineage window K = 20 frames = time 100, default): splits 31, persistent splits 1 (0 more failed only because the siblings re-merged within K), max generation 1, merges 15, merge/split ratio 0.484, nucleations 6
- channel total drift (end/start - 1): [-0.9415, -0.8658, 0.4403, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 18 at frame 55: holes 4, rim-vs-core 0.80, rim-vs-outside 0.54, heterogeneity 0.24; core [0.97, 0.467, 0.886, 0.046] rim [0.224, 0.75, 0.894, 0.037]
  - track 22 at frame 55: holes 1, rim-vs-core 0.68, rim-vs-outside 0.49, heterogeneity 0.24; core [0.699, 0.416, 0.9, 0.048] rim [0.142, 0.8, 0.906, 0.039]
  - track 26 at frame 55: holes 1, rim-vs-core 0.66, rim-vs-outside 0.46, heterogeneity 0.24; core [0.754, 0.432, 0.887, 0.052] rim [0.178, 0.751, 0.895, 0.045]
  - track 106 at frame 87: holes 1, rim-vs-core 0.72, rim-vs-outside 0.46, heterogeneity 0.25; core [0.795, 0.398, 0.653, 0.278] rim [0.173, 0.756, 0.682, 0.263]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 74 components >= 12 px at frames [17, 33, 50, 67, 83, 100]):
  - radial A0: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 0.166, rim/outside 9.18 (aggregate of 74 individuals; 4/74 membrane-like individually; rim level 0.123)
  - radial A1: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1.24, rim/outside 28 (aggregate of 74 individuals; 2/74 membrane-like individually; rim level 0.883)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.1, rim/outside 0.936 (aggregate of 74 individuals; 0/74 membrane-like individually; rim level 0.744)
  - radial W: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.953, rim/outside 1.4 (aggregate of 74 individuals; 0/74 membrane-like individually; rim level 0.225)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #18 (t=275, R_eq 8.78): none; #22 (t=275, R_eq 8.96): none; #26 (t=275, R_eq 8.85): none; #106 (t=435, R_eq 8.94): none

## Warnings
- matter fills >80% of the domain at some point: components may be one connected sea
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 2 of 74 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
