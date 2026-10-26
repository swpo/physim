# Evidence pack: condensate-food-chain (seed 7)

- world: `../world.py`, family `active-emulsion`
- parent: threads/active-droplets/worlds/ad1-fuel; mutation: two immiscible autocatalytic condensates in a closed chain: prey made from fuel, predator made from prey material; decay -> waste -> fuel
- run: 101 frames x 200 steps x dt 0.5 = time 10000; grid [256, 256]; wall 567s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0507-c29-review-foodchain/world.py --out collective/contrib/20261026T0507-c29-review-foodchain/rerun --seeds 7 --frames 100 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0091, 1.2446], min area 6 px

## Measurements
- components: final 181, mean 169.9, max 213; occupancy final 0.32
- tracks: 706; persistent (alive >= 50% of run): 170; longest 101 frames; alive start-to-end: 8
- size of persistent tracks: max/min area ratio 20.86 (1 = constant size)
- enclosures: components with a hole mean 0.11, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [183, 182, 181], H1 [0, 0, 0]
- motion: 4 long-lived tracks moved >= 1 body length; max speed 0.00309/time; max body lengths 1.3
- replication (lineage window K = 20 frames = time 2000, default): splits 157, persistent splits 61 (0 more failed only because the siblings re-merged within K), max generation 3, merges 61, merge/split ratio 0.389, nucleations 20
- channel total drift (end/start - 1): [0.311, -0.9997, -0.7338, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 10 at frame 50: holes 0, rim-vs-core 0.33, rim-vs-outside 0.52, heterogeneity 0.07; core [0.955, 0.0, 0.024, 0.959] rim [0.644, 0.0, 0.076, 0.879]
  - track 23 at frame 50: holes 0, rim-vs-core 0.34, rim-vs-outside 0.51, heterogeneity 0.07; core [0.953, 0.0, 0.024, 0.958] rim [0.629, 0.0, 0.078, 0.873]
  - track 28 at frame 50: holes 0, rim-vs-core 0.35, rim-vs-outside 0.33, heterogeneity 0.06; core [0.907, 0.0, 0.043, 0.926] rim [0.559, 0.0, 0.082, 0.868]
  - track 662 at frame 65: holes 0, rim-vs-core 0.38, rim-vs-outside 0.31, heterogeneity 0.06; core [0.904, 0.0, 0.039, 0.935] rim [0.534, 0.0, 0.084, 0.866]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 1012 components >= 12 px at frames [17, 33, 50, 67, 83, 100]):
  - radial prey a: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.905, rim/outside 17.5 (aggregate of 1012 individuals; 2/1012 membrane-like individually; rim level 0.874)
  - radial predator b: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.03, rim/outside 1.09 (aggregate of 1012 individuals; 0/1012 membrane-like individually; rim level 0.0063)
  - radial fuel u: peak at rho=1.75 (OUTSIDE the peak band 0.5-1.5), rim/core 6.74, rim/outside 0.876 (aggregate of 1012 individuals; 0/1012 membrane-like individually; rim level 0.131)
  - radial waste w: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.939, rim/outside 1.23 (aggregate of 1012 individuals; 0/1012 membrane-like individually; rim level 0.918)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #10 (t=5000, R_eq 6.15): none; #23 (t=5000, R_eq 6.31): none; #28 (t=5000, R_eq 5.29): none; #662 (t=6500, R_eq 5.75): none
- species `prey` (channels ['prey a'], own threshold): components final 181, mean 166.1, max 195; tracks 566, persistent 170; splits 127, persistent splits 61 (K=20), max generation 3, merges 41, merge/split 0.323; moving tracks 4
- species `predator` (channels ['predator b'], own threshold): components final 0, mean 7.5, max 71; tracks 164, persistent 0; splits 35, persistent splits 0 (K=20), max generation 0, merges 14, merge/split 0.4; moving tracks 1

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 3 of 1012 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
