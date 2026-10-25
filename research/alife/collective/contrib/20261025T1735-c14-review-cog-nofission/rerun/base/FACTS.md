# Evidence pack: lcn-cog (seed 5)

- world: `../world.py`, family `lenia`
- parent: threads/lenia-multichannel/worlds/rf-two56-mu0.01; mutation: unmodified r-two56 kernels on a closed food-waste cycle (losses become waste that regrows into food, no refill), full-domain noise
- run: 201 frames x 50 steps x dt 0.1 = time 1000; grid [192, 192]; wall 153s; status ok
- command: `python -m labkit.run scratch/c14/rev_cnf/world.py --out scratch/c14/rev_cnf/base --seeds 5 --frames 200 --spf 50 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.9996], min area 6 px

## Measurements
- components: final 11, mean 11.4, max 25; occupancy final 0.07
- tracks: 108; persistent (alive >= 50% of run): 11; longest 192 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.18 (1 = constant size)
- enclosures: components with a hole mean 10.19, final 11; holes at thresholds 0.2/0.35/0.5 final [0, 34, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [12, 11, 11], H1 [36, 0, 0]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 0.268/time; max body lengths 1.1
- replication (lineage window K = 20 frames = time 100, default): splits 31, persistent splits 1 (0 more failed only because the siblings re-merged within K), max generation 1, merges 15, merge/split ratio 0.484, nucleations 6
- channel total drift (end/start - 1): [-0.9461, -0.876, 0.4508, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 18 at frame 106: holes 3, rim-vs-core 0.80, rim-vs-outside 0.54, heterogeneity 0.24; core [0.972, 0.467, 0.885, 0.037] rim [0.222, 0.75, 0.893, 0.027]
  - track 22 at frame 106: holes 1, rim-vs-core 0.68, rim-vs-outside 0.49, heterogeneity 0.24; core [0.74, 0.414, 0.916, 0.037] rim [0.17, 0.78, 0.922, 0.029]
  - track 26 at frame 106: holes 1, rim-vs-core 0.75, rim-vs-outside 0.50, heterogeneity 0.24; core [0.895, 0.456, 0.891, 0.036] rim [0.207, 0.748, 0.898, 0.028]
  - track 106 at frame 138: holes 3, rim-vs-core 0.69, rim-vs-outside 0.48, heterogeneity 0.24; core [0.836, 0.455, 0.918, 0.041] rim [0.205, 0.742, 0.929, 0.033]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 67 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial A0: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.139, rim/outside 8.05 (aggregate of 67 individuals; 1/67 membrane-like individually; rim level 0.102)
  - radial A1: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1.27, rim/outside 30.4 (aggregate of 67 individuals; 0/67 membrane-like individually; rim level 0.927)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.03, rim/outside 0.976 (aggregate of 67 individuals; 0/67 membrane-like individually; rim level 0.873)
  - radial W: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.906, rim/outside 1.76 (aggregate of 67 individuals; 0/67 membrane-like individually; rim level 0.075)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #18 (t=530, R_eq 8.79): none; #22 (t=530, R_eq 8.97): none; #26 (t=530, R_eq 8.79): none; #106 (t=690, R_eq 8.81): none

## Warnings
- matter fills >80% of the domain at some point: components may be one connected sea
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 1 of 67 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
