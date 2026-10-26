# Evidence pack: condensate-food-chain (seed 11)

- world: `../../20261026T1302-c42-foodchain-both-divide-claim/world.py`, family `active-emulsion`
- parent: threads/active-droplets/worlds/ad1-fuel; mutation: two immiscible autocatalytic condensates in a closed chain: prey made from fuel, predator made from prey material; decay -> waste -> fuel
- run: 121 frames x 200 steps x dt 0.5 = time 12000; grid [96, 96]; wall 99s; status ok
- command: `python -m labkit.run collective/contrib/20261026T1302-c42-foodchain-both-divide-claim/world.py --out collective/contrib/20261026T1646-c41-review-arena-size/L96_s11 --seeds 11 --size 96 96 --frames 120 --lineage-k 5 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0341, 1.3568], min area 6 px

## Measurements
- components: final 17, mean 20.1, max 42; occupancy final 0.19
- tracks: 253; persistent (alive >= 50% of run): 0; longest 43 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.99, final 2; holes at thresholds 0.2/0.35/0.5 final [3, 2, 1]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [21, 18, 11], H1 [4, 3, 1]
- motion: 2 long-lived tracks moved >= 1 body length; max speed 0.00452/time; max body lengths 1.3
- replication (lineage window K = 5 frames = time 500, --lineage-k): splits 74, persistent splits 26 (0 more failed only because the siblings re-merged within K), max generation 3, merges 21, merge/split ratio 0.284, nucleations 45
- channel total drift (end/start - 1): [-0.4811, 3.4385, -0.3433, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 37 at frame 22: holes 0, rim-vs-core 0.29, rim-vs-outside 0.53, heterogeneity 0.08; core [0.901, 0.028, 0.025, 0.781] rim [0.66, 0.032, 0.137, 0.663]
  - track 36 at frame 22: holes 0, rim-vs-core 0.32, rim-vs-outside 0.33, heterogeneity 0.07; core [0.918, 0.0, 0.044, 0.741] rim [0.616, 0.0, 0.117, 0.677]
  - track 46 at frame 20: holes 0, rim-vs-core 0.25, rim-vs-outside 0.27, heterogeneity 0.05; core [0.005, 0.844, 0.726, 0.113] rim [0.015, 0.598, 0.718, 0.117]
  - track 129 at frame 53: holes 0, rim-vs-core 0.25, rim-vs-outside 0.26, heterogeneity 0.04; core [0.005, 0.865, 0.715, 0.047] rim [0.017, 0.611, 0.712, 0.047]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 107 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial prey a: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.17, rim/outside 3.62 (aggregate of 107 individuals; 16/107 membrane-like individually; rim level 0.259)
  - radial predator b: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.978, rim/outside 5.08 (aggregate of 107 individuals; 9/107 membrane-like individually; rim level 0.496)
  - radial fuel u: peak at rho=1.95 (OUTSIDE the peak band 0.5-1.5), rim/core 1.21, rim/outside 0.947 (aggregate of 107 individuals; 0/107 membrane-like individually; rim level 0.493)
  - radial waste w: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.918, rim/outside 1.23 (aggregate of 107 individuals; 0/107 membrane-like individually; rim level 0.429)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #37 (t=2200, R_eq 7.23): none; #36 (t=2200, R_eq 5.2): none; #46 (t=2000, R_eq 5.64): none; #129 (t=5300, R_eq 3.78): none
- species `prey` (channels ['prey a'], own threshold): components final 2, mean 7.7, max 34; tracks 154, persistent 0; splits 33, persistent splits 3 (K=5), max generation 1, merges 8, merge/split 0.242; moving tracks 1
- species `predator` (channels ['predator b'], own threshold): components final 16, mean 14.2, max 19; tracks 186, persistent 0; splits 46, persistent splits 15 (K=5), max generation 2, merges 12, merge/split 0.261; moving tracks 12

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 16 of 107 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
