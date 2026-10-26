# Evidence pack: condensate-food-chain (seed 1)

- world: `../../world.py`, family `active-emulsion`
- parent: threads/active-droplets/worlds/ad1-fuel; mutation: two immiscible autocatalytic condensates in a closed chain: prey made from fuel, predator made from prey material; decay -> waste -> fuel
- run: 101 frames x 200 steps x dt 0.5 = time 10000; grid [256, 256]; wall 696s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/60e094ad-5b43-583e-8321-7611b63df58f/scratchpad/fc/world.py --out /tmp/claude-0/-home-user-physim/60e094ad-5b43-583e-8321-7611b63df58f/scratchpad/fc/packK/s1 --seeds 1 --frames 100 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0091, 1.2416], min area 6 px

## Measurements
- components: final 181, mean 167.2, max 226; occupancy final 0.31
- tracks: 725; persistent (alive >= 50% of run): 174; longest 101 frames; alive start-to-end: 3
- size of persistent tracks: max/min area ratio 13.33 (1 = constant size)
- enclosures: components with a hole mean 0.09, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [181, 181, 181], H1 [0, 0, 0]
- motion: 5 long-lived tracks moved >= 1 body length; max speed 0.00501/time; max body lengths 1.3
- replication (lineage window K = 20 frames = time 2000, default): splits 172, persistent splits 63 (0 more failed only because the siblings re-merged within K), max generation 2, merges 79, merge/split ratio 0.459, nucleations 15
- channel total drift (end/start - 1): [0.3365, -0.9997, -0.7332, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 120 at frame 50: holes 0, rim-vs-core 0.40, rim-vs-outside 0.31, heterogeneity 0.07; core [0.899, 0.0, 0.04, 0.925] rim [0.505, 0.0, 0.087, 0.847]
  - track 128 at frame 50: holes 0, rim-vs-core 0.31, rim-vs-outside 0.52, heterogeneity 0.07; core [0.93, 0.0, 0.035, 0.937] rim [0.629, 0.0, 0.078, 0.864]
  - track 189 at frame 50: holes 0, rim-vs-core 0.33, rim-vs-outside 0.52, heterogeneity 0.07; core [0.949, 0.0, 0.024, 0.956] rim [0.634, 0.0, 0.078, 0.86]
  - track 621 at frame 60: holes 0, rim-vs-core 0.32, rim-vs-outside 0.53, heterogeneity 0.07; core [0.944, 0.0, 0.024, 0.956] rim [0.641, 0.0, 0.078, 0.861]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 1006 components >= 12 px at frames [17, 33, 50, 67, 83, 100]):
  - radial prey a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.903, rim/outside 17.6 (aggregate of 1006 individuals; 5/1006 membrane-like individually; rim level 0.874)
  - radial predator b: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.15, rim/outside 1.09 (aggregate of 1006 individuals; 2/1006 membrane-like individually; rim level 0.0064)
  - radial fuel u: peak at rho=1.75 (OUTSIDE the peak band 0.5-1.5), rim/core 6.98, rim/outside 0.874 (aggregate of 1006 individuals; 0/1006 membrane-like individually; rim level 0.131)
  - radial waste w: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.931, rim/outside 1.26 (aggregate of 1006 individuals; 0/1006 membrane-like individually; rim level 0.909)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #120 (t=5000, R_eq 5.84): none; #128 (t=5000, R_eq 6.56): none; #189 (t=5000, R_eq 6.46): none; #621 (t=6000, R_eq 6.68): none
- species `prey` (channels ['prey a'], own threshold): components final 181, mean 163.0, max 181; tracks 560, persistent 174; splits 132, persistent splits 64 (K=20), max generation 2, merges 44, merge/split 0.333; moving tracks 5
- species `predator` (channels ['predator b'], own threshold): components final 0, mean 8.0, max 82; tracks 165, persistent 0; splits 26, persistent splits 0 (K=20), max generation 0, merges 13, merge/split 0.5; moving tracks 0

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 4 of 1006 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
