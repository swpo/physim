# Evidence pack: condensate-food-chain (seed 7)

- world: `../../world_claim.py`, family `active-emulsion`
- parent: threads/active-droplets/worlds/ad1-fuel; mutation: two immiscible autocatalytic condensates in a closed chain: prey made from fuel, predator made from prey material; decay -> waste -> fuel
- run: 121 frames x 200 steps x dt 0.5 = time 12000; grid [128, 128]; wall 113s; status ok
- command: `python -m labkit.run world_claim.py --out rerun_nopred/seed7 --seeds 7 --size 128 128 --frames 120 --lineage-k 5 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0258, 1.1623], min area 6 px

## Measurements
- components: final 75, mean 74.3, max 78; occupancy final 0.30
- tracks: 136; persistent (alive >= 50% of run): 75; longest 121 frames; alive start-to-end: 3
- size of persistent tracks: max/min area ratio 18.50 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [75, 75, 75], H1 [0, 0, 0]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 0.000689/time; max body lengths 1.1
- replication (lineage window K = 5 frames = time 500, --lineage-k): splits 20, persistent splits 2 (0 more failed only because the siblings re-merged within K), max generation 1, merges 8, merge/split ratio 0.4, nucleations 9
- channel total drift (end/start - 1): [0.2458, None, -0.7049, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 14 at frame 61: holes 0, rim-vs-core 0.44, rim-vs-outside 0.31, heterogeneity 0.09; core [0.883, 0.0, 0.04, 0.884] rim [0.48, 0.0, 0.101, 0.718]
  - track 18 at frame 61: holes 0, rim-vs-core 0.39, rim-vs-outside 0.32, heterogeneity 0.08; core [0.889, 0.0, 0.047, 0.854] rim [0.519, 0.0, 0.096, 0.73]
  - track 29 at frame 61: holes 0, rim-vs-core 0.44, rim-vs-outside 0.30, heterogeneity 0.09; core [0.877, 0.0, 0.042, 0.874] rim [0.472, 0.0, 0.1, 0.72]
  - track 130 at frame 63: holes 0, rim-vs-core 0.43, rim-vs-outside 0.32, heterogeneity 0.09; core [0.889, 0.0, 0.039, 0.883] rim [0.498, 0.0, 0.099, 0.725]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 450 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial prey a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.858, rim/outside 24.8 (aggregate of 450 individuals; 0/450 membrane-like individually; rim level 0.849)
  - radial predator b: flat profile (no radial structure; level 0; aggregate of 450 individuals)
  - radial fuel u: peak at rho=1.85 (OUTSIDE the peak band 0.5-1.5), rim/core 7.55, rim/outside 0.863 (aggregate of 450 individuals; 0/450 membrane-like individually; rim level 0.146)
  - radial waste w: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.876, rim/outside 1.65 (aggregate of 450 individuals; 0/450 membrane-like individually; rim level 0.837)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #14 (t=6100, R_eq 4.85): none; #18 (t=6100, R_eq 4.18): none; #29 (t=6100, R_eq 4.69): none; #130 (t=6300, R_eq 4.72): none
- species `prey` (channels ['prey a'], own threshold): components final 75, mean 74.3, max 78; tracks 136, persistent 75; splits 20, persistent splits 2 (K=5), max generation 1, merges 8, merge/split 0.4; moving tracks 1
- species `predator` (channels ['predator b'], own threshold): components final 0, mean 0.0, max 0; tracks 0, persistent 0; splits 0, persistent splits 0 (K=5), max generation 0, merges 0, merge/split n/a; moving tracks 0

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
