# Evidence pack: condensate-food-chain (seed 0)

- world: `../world.py`, family `active-emulsion`
- parent: threads/active-droplets/worlds/ad1-fuel; mutation: two immiscible autocatalytic condensates in a closed chain: prey made from fuel, predator made from prey material; decay -> waste -> fuel
- run: 81 frames x 200 steps x dt 0.5 = time 8000; grid [256, 256]; wall 574s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/60e094ad-5b43-583e-8321-7611b63df58f/scratchpad/fc/world.py --out /tmp/claude-0/-home-user-physim/60e094ad-5b43-583e-8321-7611b63df58f/scratchpad/fc/pack --seeds 0 --frames 80 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.3728], min area 6 px

## Measurements
- components: final 147, mean 137.4, max 203; occupancy final 0.31
- tracks: 916; persistent (alive >= 50% of run): 97; longest 81 frames; alive start-to-end: 4
- size of persistent tracks: max/min area ratio 24.50 (1 = constant size)
- enclosures: components with a hole mean 0.96, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [160, 151, 147], H1 [0, 0, 0]
- motion: 24 long-lived tracks moved >= 1 body length; max speed 0.00832/time; max body lengths 1.6
- replication (lineage window K = 20 frames = time 2000, default): splits 256, persistent splits 35 (0 more failed only because the siblings re-merged within K), max generation 3, merges 115, merge/split ratio 0.449, nucleations 34
- channel total drift (end/start - 1): [0.2713, -0.9029, -0.718, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 4 at frame 40: holes 0, rim-vs-core 0.23, rim-vs-outside 0.57, heterogeneity 0.06; core [0.932, 0.0, 0.031, 0.959] rim [0.713, 0.0, 0.074, 0.922]
  - track 51 at frame 40: holes 0, rim-vs-core 0.27, rim-vs-outside 0.51, heterogeneity 0.06; core [0.914, 0.0, 0.034, 0.958] rim [0.657, 0.0, 0.088, 0.909]
  - track 133 at frame 40: holes 0, rim-vs-core 0.35, rim-vs-outside 0.31, heterogeneity 0.06; core [0.879, 0.0, 0.048, 0.941] rim [0.539, 0.0, 0.098, 0.898]
  - track 821 at frame 69: holes 0, rim-vs-core 0.34, rim-vs-outside 0.32, heterogeneity 0.06; core [0.884, 0.0, 0.049, 0.929] rim [0.553, 0.0, 0.097, 0.888]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 793 components >= 12 px at frames [13, 27, 40, 53, 67, 80]):
  - radial prey a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.913, rim/outside 13.2 (aggregate of 793 individuals; 13/793 membrane-like individually; rim level 0.811)
  - radial predator b: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.05, rim/outside 1.51 (aggregate of 793 individuals; 13/793 membrane-like individually; rim level 0.0256)
  - radial fuel u: peak at rho=1.85 (OUTSIDE the peak band 0.5-1.5), rim/core 4.1, rim/outside 0.868 (aggregate of 793 individuals; 0/793 membrane-like individually; rim level 0.16)
  - radial waste w: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.961, rim/outside 1.14 (aggregate of 793 individuals; 0/793 membrane-like individually; rim level 0.919)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #4 (t=4000, R_eq 6.05): none; #51 (t=4000, R_eq 6.51): none; #133 (t=4000, R_eq 6): none; #821 (t=6900, R_eq 5.81): none
- species `prey` (channels ['prey a'], own threshold): components final 146, mean 128.9, max 193; tracks 607, persistent 99; splits 155, persistent splits 34 (K=20), max generation 3, merges 38, merge/split 0.245; moving tracks 21
- species `predator` (channels ['predator b'], own threshold): components final 1, mean 15.5, max 72; tracks 334, persistent 0; splits 98, persistent splits 0 (K=20), max generation 0, merges 18, merge/split 0.184; moving tracks 0

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 13 of 793 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
