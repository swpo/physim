# Evidence pack: lcn-cog (seed 5)

- world: `../world.py`, family `lenia`
- parent: threads/lenia-multichannel/worlds/rf-two56-mu0.01; mutation: unmodified r-two56 kernels on a closed food-waste cycle (losses become waste that regrows into food, no refill), full-domain noise
- run: 201 frames x 50 steps x dt 0.1 = time 1000; grid [192, 192]; wall 150s; status ok
- command: `python -m labkit.run scratch/c14/rev_cnf/world.py --out scratch/c14/rev_cnf/k0h075 --seeds 5 --frames 200 --spf 50 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.9996], min area 6 px

## Measurements
- components: final 32, mean 20.8, max 37; occupancy final 0.21
- tracks: 353; persistent (alive >= 50% of run): 9; longest 193 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 3.06 (1 = constant size)
- enclosures: components with a hole mean 5.63, final 9; holes at thresholds 0.2/0.35/0.5 final [14, 14, 1]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [54, 34, 30], H1 [47, 2, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 1.3
- replication (lineage window K = 20 frames = time 100, default): splits 102, persistent splits 2 (0 more failed only because the siblings re-merged within K), max generation 2, merges 74, merge/split ratio 0.725, nucleations 60
- channel total drift (end/start - 1): [-0.8269, -0.6216, 0.2829, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 16 at frame 104: holes 0, rim-vs-core 1.02, rim-vs-outside 0.53, heterogeneity 0.25; core [0.779, 0.283, 0.88, 0.058] rim [0.01, 0.958, 0.884, 0.048]
  - track 20 at frame 104: holes 0, rim-vs-core 0.98, rim-vs-outside 0.56, heterogeneity 0.28; core [0.807, 0.283, 0.779, 0.116] rim [0.054, 0.905, 0.762, 0.126]
  - track 61 at frame 118: holes 0, rim-vs-core 0.78, rim-vs-outside 0.49, heterogeneity 0.25; core [0.744, 0.356, 0.783, 0.086] rim [0.122, 0.831, 0.795, 0.079]
  - track 36 at frame 92: holes 0, rim-vs-core 0.97, rim-vs-outside 0.64, heterogeneity 0.28; core [0.698, 0.319, 0.844, 0.078] rim [0.0, 0.998, 0.816, 0.097]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 131 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial A0: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 0.708, rim/outside 13.7 (aggregate of 131 individuals; 18/131 membrane-like individually; rim level 0.475)
  - radial A1: peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.47, rim/outside 7.31 (aggregate of 131 individuals; 51/131 membrane-like individually; rim level 0.859)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.07, rim/outside 0.963 (aggregate of 131 individuals; 0/131 membrane-like individually; rim level 0.717)
  - radial W: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.941, rim/outside 1.3 (aggregate of 131 individuals; 0/131 membrane-like individually; rim level 0.215)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #16 (t=520, R_eq 8.72): ['A1']; #20 (t=520, R_eq 8.16): none; #61 (t=590, R_eq 8.74): none; #36 (t=460, R_eq 8.78): none

## Warnings
- matter fills >80% of the domain at some point: components may be one connected sea
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 23 of 131 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
