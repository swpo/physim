# Evidence pack: lcn-cog (seed 7)

- world: `../../../../20261025T1703-c18-cog-gate-is-slow-diffusion/world.py`, family `lenia`
- parent: threads/lenia-multichannel/worlds/rf-two56-mu0.01; mutation: unmodified r-two56 kernels on a closed food-waste cycle (losses become waste that regrows into food, no refill), full-domain noise
- run: 101 frames x 50 steps x dt 0.1 = time 500; grid [192, 192]; wall 56s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1703-c18-cog-gate-is-slow-diffusion/world.py --out collective/contrib/wip-c22/rev_cog/ungated/seed7 --seeds 7 --frames 100 --spf 50 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.9996], min area 6 px

## Measurements
- components: final 18, mean 17.6, max 29; occupancy final 0.12
- tracks: 105; persistent (alive >= 50% of run): 18; longest 93 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.75 (1 = constant size)
- enclosures: components with a hole mean 13.49, final 17; holes at thresholds 0.2/0.35/0.5 final [1, 33, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [24, 18, 18], H1 [40, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.7
- replication (lineage window K = 20 frames = time 100, default): splits 22, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 16, merge/split ratio 0.727, nucleations 9
- channel total drift (end/start - 1): [-0.9114, -0.7959, 0.4178, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 12 at frame 54: holes 3, rim-vs-core 0.69, rim-vs-outside 0.50, heterogeneity 0.24; core [0.868, 0.509, 0.891, 0.044] rim [0.22, 0.733, 0.901, 0.036]
  - track 24 at frame 55: holes 1, rim-vs-core 0.84, rim-vs-outside 0.55, heterogeneity 0.25; core [0.9, 0.343, 0.848, 0.064] rim [0.179, 0.781, 0.86, 0.053]
  - track 29 at frame 55: holes 0, rim-vs-core 0.69, rim-vs-outside 0.45, heterogeneity 0.24; core [0.777, 0.42, 0.869, 0.053] rim [0.17, 0.754, 0.876, 0.045]
  - track 31 at frame 55: holes 2, rim-vs-core 0.71, rim-vs-outside 0.50, heterogeneity 0.24; core [0.828, 0.424, 0.874, 0.048] rim [0.2, 0.757, 0.886, 0.041]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 113 components >= 12 px at frames [17, 33, 50, 67, 83, 100]):
  - radial A0: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 0.262, rim/outside 7.67 (aggregate of 113 individuals; 3/113 membrane-like individually; rim level 0.196)
  - radial A1: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1.28, rim/outside 11.8 (aggregate of 113 individuals; 3/113 membrane-like individually; rim level 0.925)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.06, rim/outside 0.962 (aggregate of 113 individuals; 0/113 membrane-like individually; rim level 0.748)
  - radial W: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.971, rim/outside 1.25 (aggregate of 113 individuals; 0/113 membrane-like individually; rim level 0.184)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #12 (t=270, R_eq 8.81): none; #24 (t=275, R_eq 8.59): none; #29 (t=275, R_eq 8.85): none; #31 (t=275, R_eq 8.78): none

## Warnings
- matter fills >80% of the domain at some point: components may be one connected sea
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 3 of 113 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
