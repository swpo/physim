# Evidence pack: condensate-food-chain (seed 2)

- world: `../../world.py`, family `active-emulsion`
- parent: threads/active-droplets/worlds/ad1-fuel; mutation: two immiscible autocatalytic condensates in a closed chain: prey made from fuel, predator made from prey material; decay -> waste -> fuel
- run: 101 frames x 200 steps x dt 0.5 = time 10000; grid [256, 256]; wall 689s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/60e094ad-5b43-583e-8321-7611b63df58f/scratchpad/fc/world.py --out /tmp/claude-0/-home-user-physim/60e094ad-5b43-583e-8321-7611b63df58f/scratchpad/fc/packK/s2 --seeds 2 --frames 100 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0091, 1.2519], min area 6 px

## Measurements
- components: final 180, mean 167.1, max 205; occupancy final 0.31
- tracks: 718; persistent (alive >= 50% of run): 161; longest 101 frames; alive start-to-end: 3
- size of persistent tracks: max/min area ratio 28.43 (1 = constant size)
- enclosures: components with a hole mean 0.14, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [180, 180, 180], H1 [0, 0, 0]
- motion: 6 long-lived tracks moved >= 1 body length; max speed 0.00816/time; max body lengths 1.4
- replication (lineage window K = 20 frames = time 2000, default): splits 173, persistent splits 61 (0 more failed only because the siblings re-merged within K), max generation 3, merges 68, merge/split ratio 0.393, nucleations 35
- channel total drift (end/start - 1): [0.3112, -0.9997, -0.7333, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 14 at frame 50: holes 0, rim-vs-core 0.32, rim-vs-outside 0.52, heterogeneity 0.07; core [0.946, 0.0, 0.025, 0.959] rim [0.641, 0.0, 0.078, 0.876]
  - track 114 at frame 50: holes 0, rim-vs-core 0.31, rim-vs-outside 0.53, heterogeneity 0.06; core [0.953, 0.0, 0.024, 0.961] rim [0.663, 0.0, 0.075, 0.881]
  - track 159 at frame 50: holes 0, rim-vs-core 0.32, rim-vs-outside 0.52, heterogeneity 0.07; core [0.955, 0.0, 0.026, 0.955] rim [0.644, 0.0, 0.077, 0.878]
  - track 682 at frame 73: holes 0, rim-vs-core 0.33, rim-vs-outside 0.51, heterogeneity 0.07; core [0.953, 0.0, 0.026, 0.957] rim [0.635, 0.0, 0.078, 0.878]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 993 components >= 12 px at frames [17, 33, 50, 67, 83, 100]):
  - radial prey a: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.906, rim/outside 17.2 (aggregate of 993 individuals; 3/993 membrane-like individually; rim level 0.874)
  - radial predator b: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 1.04, rim/outside 1.12 (aggregate of 993 individuals; 2/993 membrane-like individually; rim level 0.0062)
  - radial fuel u: peak at rho=1.75 (OUTSIDE the peak band 0.5-1.5), rim/core 6.74, rim/outside 0.871 (aggregate of 993 individuals; 0/993 membrane-like individually; rim level 0.132)
  - radial waste w: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.939, rim/outside 1.23 (aggregate of 993 individuals; 0/993 membrane-like individually; rim level 0.918)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #14 (t=5000, R_eq 6.48): none; #114 (t=5000, R_eq 6.21): none; #159 (t=5000, R_eq 6.08): none; #682 (t=7300, R_eq 6.18): none
- species `prey` (channels ['prey a'], own threshold): components final 180, mean 162.5, max 203; tracks 567, persistent 162; splits 132, persistent splits 62 (K=20), max generation 3, merges 40, merge/split 0.303; moving tracks 4
- species `predator` (channels ['predator b'], own threshold): components final 0, mean 8.9, max 82; tracks 176, persistent 0; splits 36, persistent splits 0 (K=20), max generation 0, merges 9, merge/split 0.25; moving tracks 0

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 2 of 993 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
