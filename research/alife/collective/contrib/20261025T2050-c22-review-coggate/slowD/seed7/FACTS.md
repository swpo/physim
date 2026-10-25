# Evidence pack: lcn-cog (seed 7)

- world: `../../../../20261025T1703-c18-cog-gate-is-slow-diffusion/world.py`, family `lenia`
- parent: threads/lenia-multichannel/worlds/rf-two56-mu0.01; mutation: unmodified r-two56 kernels on a closed food-waste cycle (losses become waste that regrows into food, no refill), full-domain noise
- run: 101 frames x 50 steps x dt 0.1 = time 500; grid [192, 192]; wall 56s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1703-c18-cog-gate-is-slow-diffusion/world.py --out collective/contrib/wip-c22/rev_cog/slowD/seed7 --seeds 7 --frames 100 --spf 50 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.9996], min area 6 px

## Measurements
- components: final 1, mean 2.8, max 32; occupancy final 0.01
- tracks: 90; persistent (alive >= 50% of run): 1; longest 91 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.14 (1 = constant size)
- enclosures: components with a hole mean 1.93, final 1; holes at thresholds 0.2/0.35/0.5 final [0, 1, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [1, 1, 1], H1 [3, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.7
- replication (lineage window K = 20 frames = time 100, default): splits 21, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 9, merge/split ratio 0.429, nucleations 4
- channel total drift (end/start - 1): [-0.9951, -0.9886, 0.4957, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 33 at frame 55: holes 1, rim-vs-core 0.72, rim-vs-outside 0.55, heterogeneity 0.27; core [0.824, 0.438, 0.345, 0.07] rim [0.194, 0.758, 0.475, 0.054]
  - track 63 at frame 24: holes 0, rim-vs-core 0.67, rim-vs-outside 0.55, heterogeneity 0.29; core [0.774, 0.456, 0.236, 0.256] rim [0.188, 0.764, 0.334, 0.236]
  - track 86 at frame 32: holes 4, rim-vs-core 0.50, rim-vs-outside 0.55, heterogeneity 0.33; core [0.867, 0.36, 0.131, 0.412] rim [0.432, 0.584, 0.224, 0.377]
  - track 38 at frame 14: holes 2, rim-vs-core 0.67, rim-vs-outside 0.52, heterogeneity 0.31; core [0.787, 0.481, 0.175, 0.314] rim [0.188, 0.762, 0.232, 0.37]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 14 components >= 12 px at frames [17, 33, 50, 67, 83, 100]):
  - radial A0: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.228, rim/outside 9.42 (aggregate of 14 individuals; 2/14 membrane-like individually; rim level 0.14)
  - radial A1: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1.24, rim/outside 14.1 (aggregate of 14 individuals; 3/14 membrane-like individually; rim level 0.779)
  - radial F: peak at rho=2.05 (OUTSIDE the peak band 0.5-1.5), rim/core 3.57, rim/outside 0.795 (aggregate of 14 individuals; 0/14 membrane-like individually; rim level 0.502)
  - radial W: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1.08, rim/outside 1.63 (aggregate of 14 individuals; 1/14 membrane-like individually; rim level 0.416)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #33 (t=275, R_eq 8.88): none; #63 (t=120, R_eq 8.97): none; #86 (t=160, R_eq 14.25, ring): ['A1']; #38 (t=70, R_eq 8.54): none

## Warnings
- matter fills >80% of the domain at some point: components may be one connected sea
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 3 of 14 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
