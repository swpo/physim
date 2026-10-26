# Evidence pack: condensate-food-chain (seed 13)

- world: `../../20261026T1302-c42-foodchain-both-divide-claim/world.py`, family `active-emulsion`
- parent: threads/active-droplets/worlds/ad1-fuel; mutation: two immiscible autocatalytic condensates in a closed chain: prey made from fuel, predator made from prey material; decay -> waste -> fuel
- run: 121 frames x 200 steps x dt 0.5 = time 12000; grid [80, 80]; wall 68s; status ok
- command: `python -m labkit.run collective/contrib/20261026T1302-c42-foodchain-both-divide-claim/world.py --out collective/contrib/20261026T1648-c41-review-arena-heldout/L80_s13 --seeds 13 --size 80 80 --frames 120 --lineage-k 5 --no-movie`
- segmentation: matter > 0.35 of robust range [0.044, 1.3454], min area 6 px

## Measurements
- components: final 12, mean 13.2, max 26; occupancy final 0.19
- tracks: 189; persistent (alive >= 50% of run): 0; longest 35 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.85, final 2; holes at thresholds 0.2/0.35/0.5 final [2, 2, 2]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [18, 14, 9], H1 [3, 3, 1]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 1.0
- replication (lineage window K = 5 frames = time 500, --lineage-k): splits 55, persistent splits 17 (0 more failed only because the siblings re-merged within K), max generation 2, merges 15, merge/split ratio 0.273, nucleations 32
- channel total drift (end/start - 1): [-0.4549, 2.8229, -0.33, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 110 at frame 77: holes 0, rim-vs-core 0.13, rim-vs-outside 0.45, heterogeneity 0.03; core [0.003, 0.843, 0.748, 0.108] rim [0.01, 0.714, 0.741, 0.112]
  - track 61 at frame 25: holes 0, rim-vs-core 0.15, rim-vs-outside 0.30, heterogeneity 0.05; core [0.006, 0.823, 0.679, 0.22] rim [0.012, 0.676, 0.661, 0.237]
  - track 41 at frame 16: holes 1, rim-vs-core 0.25, rim-vs-outside 0.40, heterogeneity 0.23; core [0.599, 0.423, 0.118, 0.633] rim [0.442, 0.27, 0.208, 0.553]
  - track 149 at frame 92: holes 0, rim-vs-core 0.23, rim-vs-outside 0.27, heterogeneity 0.05; core [0.003, 0.851, 0.563, 0.284] rim [0.011, 0.625, 0.564, 0.283]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 78 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial prey a: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.21, rim/outside 2.91 (aggregate of 78 individuals; 6/78 membrane-like individually; rim level 0.219)
  - radial predator b: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.03, rim/outside 4.49 (aggregate of 78 individuals; 13/78 membrane-like individually; rim level 0.488)
  - radial fuel u: peak at rho=2.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1.15, rim/outside 0.964 (aggregate of 78 individuals; 0/78 membrane-like individually; rim level 0.564)
  - radial waste w: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.917, rim/outside 1.24 (aggregate of 78 individuals; 0/78 membrane-like individually; rim level 0.355)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #110 (t=7700, R_eq 6.1): none; #61 (t=2500, R_eq 4.33): none; #41 (t=1600, R_eq 9.04): ['predator b']; #149 (t=9200, R_eq 2.93): none
- species `prey` (channels ['prey a'], own threshold): components final 2, mean 3.8, max 22; tracks 99, persistent 0; splits 17, persistent splits 0 (K=5), max generation 0, merges 4, merge/split 0.235; moving tracks 4
- species `predator` (channels ['predator b'], own threshold): components final 12, mean 10.8, max 20; tracks 150, persistent 0; splits 40, persistent splits 12 (K=5), max generation 2, merges 9, merge/split 0.225; moving tracks 7

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 18 of 78 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
