# Evidence pack: lcn-cog (seed 5)

- world: `../world.py`, family `lenia`
- parent: threads/lenia-multichannel/worlds/rf-two56-mu0.01; mutation: unmodified r-two56 kernels on a closed food-waste cycle (losses become waste that regrows into food, no refill), full-domain noise
- run: 201 frames x 50 steps x dt 0.1 = time 1000; grid [192, 192]; wall 148s; status ok
- command: `python -m labkit.run scratch/c14/rev_cnf/world.py --out scratch/c14/rev_cnf/k1m095 --seeds 5 --frames 200 --spf 50 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.9996], min area 6 px

## Measurements
- components: final 28, mean 29.4, max 41; occupancy final 0.30
- tracks: 2770; persistent (alive >= 50% of run): 0; longest 22 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 12.28, final 9; holes at thresholds 0.2/0.35/0.5 final [31, 21, 2]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [102, 50, 17], H1 [63, 14, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 1.4
- replication (lineage window K = 20 frames = time 100, default): splits 850, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 913, merge/split ratio 1.07, nucleations 395
- channel total drift (end/start - 1): [-0.6758, -0.5065, -0.5083, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1793 at frame 141: holes 1, rim-vs-core 0.67, rim-vs-outside 0.39, heterogeneity 0.26; core [0.747, 0.345, 0.523, 0.439] rim [0.211, 0.74, 0.582, 0.398]
  - track 1463 at frame 118: holes 0, rim-vs-core 1.06, rim-vs-outside 0.58, heterogeneity 0.25; core [0.789, 0.282, 0.792, 0.208] rim [0.0, 0.992, 0.811, 0.195]
  - track 123 at frame 24: holes 0, rim-vs-core 1.10, rim-vs-outside 0.57, heterogeneity 0.25; core [0.851, 0.24, 0.671, 0.289] rim [0.041, 0.982, 0.701, 0.283]
  - track 1337 at frame 111: holes 2, rim-vs-core 0.76, rim-vs-outside 0.55, heterogeneity 0.26; core [0.958, 0.138, 0.654, 0.222] rim [0.408, 0.662, 0.66, 0.215]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 162 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial A0: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 1.05, rim/outside 6.89 (aggregate of 162 individuals; 46/162 membrane-like individually; rim level 0.557)
  - radial A1: peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.76, rim/outside 2.94 (aggregate of 162 individuals; 92/162 membrane-like individually; rim level 0.635)  MEMBRANE-LIKE
  - radial F: peak at rho=1.85 (OUTSIDE the peak band 0.5-1.5), rim/core 1.4, rim/outside 0.907 (aggregate of 162 individuals; 2/162 membrane-like individually; rim level 0.425)
  - radial W: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.934, rim/outside 1.11 (aggregate of 162 individuals; 0/162 membrane-like individually; rim level 0.547)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): A1
- membrane-like channels per top track at mid-life: #1793 (t=705, R_eq 8.63): none; #1463 (t=590, R_eq 8.59): ['A1']; #123 (t=120, R_eq 8.16): ['A1']; #1337 (t=555, R_eq 10.76, ring): ['A1']

## Warnings
- matter fills >80% of the domain at some point: components may be one connected sea
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 59 of 162 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
