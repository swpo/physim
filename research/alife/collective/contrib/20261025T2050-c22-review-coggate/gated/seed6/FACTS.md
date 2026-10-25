# Evidence pack: lcn-cog (seed 6)

- world: `../../../../20261025T1703-c18-cog-gate-is-slow-diffusion/world.py`, family `lenia`
- parent: threads/lenia-multichannel/worlds/rf-two56-mu0.01; mutation: unmodified r-two56 kernels on a closed food-waste cycle (losses become waste that regrows into food, no refill), full-domain noise
- run: 101 frames x 50 steps x dt 0.1 = time 500; grid [192, 192]; wall 55s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1703-c18-cog-gate-is-slow-diffusion/world.py --out collective/contrib/wip-c22/rev_cog/gated/seed6 --seeds 6 --frames 100 --spf 50 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.9996], min area 6 px

## Measurements
- components: final 3, mean 4.2, max 23; occupancy final 0.02
- tracks: 90; persistent (alive >= 50% of run): 3; longest 92 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.21 (1 = constant size)
- enclosures: components with a hole mean 3.16, final 3; holes at thresholds 0.2/0.35/0.5 final [0, 10, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [3, 3, 3], H1 [9, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.9
- replication (lineage window K = 20 frames = time 100, default): splits 21, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 13, merge/split ratio 0.619, nucleations 6
- channel total drift (end/start - 1): [-0.9856, -0.9667, 0.4865, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 16 at frame 55: holes 2, rim-vs-core 0.81, rim-vs-outside 0.59, heterogeneity 0.27; core [0.929, 0.429, 0.44, 0.076] rim [0.193, 0.757, 0.555, 0.06]
  - track 78 at frame 58: holes 1, rim-vs-core 0.78, rim-vs-outside 0.60, heterogeneity 0.28; core [0.833, 0.386, 0.493, 0.09] rim [0.169, 0.796, 0.532, 0.068]
  - track 80 at frame 58: holes 5, rim-vs-core 0.72, rim-vs-outside 0.59, heterogeneity 0.27; core [0.828, 0.444, 0.474, 0.089] rim [0.197, 0.78, 0.538, 0.067]
  - track 66 at frame 20: holes 4, rim-vs-core 0.55, rim-vs-outside 0.57, heterogeneity 0.32; core [0.837, 0.273, 0.021, 0.666] rim [0.41, 0.602, 0.126, 0.624]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 21 components >= 12 px at frames [17, 33, 50, 67, 83, 100]):
  - radial A0: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 0.19, rim/outside 13.6 (aggregate of 21 individuals; 3/21 membrane-like individually; rim level 0.126)
  - radial A1: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1.23, rim/outside 26.9 (aggregate of 21 individuals; 2/21 membrane-like individually; rim level 0.848)
  - radial F: peak at rho=2.15 (OUTSIDE the peak band 0.5-1.5), rim/core 2.89, rim/outside 0.93 (aggregate of 21 individuals; 0/21 membrane-like individually; rim level 0.767)
  - radial W: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.953, rim/outside 1.53 (aggregate of 21 individuals; 0/21 membrane-like individually; rim level 0.285)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #16 (t=275, R_eq 8.79): none; #78 (t=290, R_eq 8.7): none; #80 (t=290, R_eq 8.69): none; #66 (t=100, R_eq 14.74, ring): ['A0']

## Warnings
- matter fills >80% of the domain at some point: components may be one connected sea
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 1 of 21 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
