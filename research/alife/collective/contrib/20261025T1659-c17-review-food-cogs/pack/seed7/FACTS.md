# Evidence pack: lcn-cog (seed 7)

- world: `../../world.py`, family `lenia`
- parent: threads/lenia-multichannel/worlds/rf-two56-mu0.01; mutation: unmodified r-two56 kernels on a closed food-waste cycle (losses become waste that regrows into food, no refill), full-domain noise
- run: 201 frames x 50 steps x dt 0.1 = time 1000; grid [192, 192]; wall 105s; status ok
- command: `python -m labkit.run world.py --out pack --seeds 6 7 --frames 200 --spf 50 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.9996], min area 6 px

## Measurements
- components: final 19, mean 17.8, max 29; occupancy final 0.12
- tracks: 107; persistent (alive >= 50% of run): 18; longest 193 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.75 (1 = constant size)
- enclosures: components with a hole mean 15.02, final 16; holes at thresholds 0.2/0.35/0.5 final [2, 34, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [23, 18, 18], H1 [47, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.7
- replication (lineage window K = 20 frames = time 100, default): splits 22, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 16, merge/split ratio 0.727, nucleations 11
- channel total drift (end/start - 1): [-0.9112, -0.7954, 0.4183, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 12 at frame 104: holes 3, rim-vs-core 0.68, rim-vs-outside 0.49, heterogeneity 0.24; core [0.868, 0.509, 0.906, 0.036] rim [0.221, 0.732, 0.915, 0.027]
  - track 24 at frame 106: holes 1, rim-vs-core 0.80, rim-vs-outside 0.53, heterogeneity 0.25; core [0.785, 0.327, 0.859, 0.062] rim [0.152, 0.821, 0.865, 0.052]
  - track 29 at frame 106: holes 1, rim-vs-core 0.67, rim-vs-outside 0.47, heterogeneity 0.24; core [0.744, 0.418, 0.898, 0.044] rim [0.173, 0.767, 0.905, 0.036]
  - track 31 at frame 106: holes 2, rim-vs-core 0.75, rim-vs-outside 0.49, heterogeneity 0.24; core [0.89, 0.441, 0.898, 0.038] rim [0.205, 0.74, 0.907, 0.03]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 109 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial A0: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 0.247, rim/outside 7.35 (aggregate of 109 individuals; 1/109 membrane-like individually; rim level 0.187)
  - radial A1: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1.28, rim/outside 12.3 (aggregate of 109 individuals; 1/109 membrane-like individually; rim level 0.947)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.03, rim/outside 0.984 (aggregate of 109 individuals; 0/109 membrane-like individually; rim level 0.859)
  - radial W: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.907, rim/outside 1.46 (aggregate of 109 individuals; 0/109 membrane-like individually; rim level 0.0695)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #12 (t=520, R_eq 8.79): none; #24 (t=530, R_eq 8.57): none; #29 (t=530, R_eq 8.85): none; #31 (t=530, R_eq 8.74): none

## Warnings
- matter fills >80% of the domain at some point: components may be one connected sea
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 1 of 109 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
