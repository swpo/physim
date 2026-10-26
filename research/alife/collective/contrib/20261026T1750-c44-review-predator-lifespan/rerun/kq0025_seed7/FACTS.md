# Evidence pack: condensate-food-chain (seed 7)

- world: `../../world_claim.py`, family `active-emulsion`
- parent: threads/active-droplets/worlds/ad1-fuel; mutation: two immiscible autocatalytic condensates in a closed chain: prey made from fuel, predator made from prey material; decay -> waste -> fuel
- run: 121 frames x 200 steps x dt 0.5 = time 12000; grid [128, 128]; wall 220s; status ok
- command: `python -m labkit.run world_claim.py --out rerun/kq0025_seed7 --seeds 7 --size 128 128 --frames 120 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0404, 1.3144], min area 6 px

## Measurements
- components: final 37, mean 38.5, max 64; occupancy final 0.22
- tracks: 315; persistent (alive >= 50% of run): 8; longest 74 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 40.57 (1 = constant size)
- enclosures: components with a hole mean 3.38, final 8; holes at thresholds 0.2/0.35/0.5 final [10, 8, 7]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [43, 38, 27], H1 [11, 9, 7]
- motion: 2 long-lived tracks moved >= 1 body length; max speed 0.00228/time; max body lengths 2.0
- replication (lineage window K = 20 frames = time 2000, default): splits 73, persistent splits 7 (0 more failed only because the siblings re-merged within K), max generation 2, merges 55, merge/split ratio 0.753, nucleations 50
- channel total drift (end/start - 1): [-0.543, 4.2299, -0.3172, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 46 at frame 37: holes 0, rim-vs-core 0.29, rim-vs-outside 0.29, heterogeneity 0.04; core [0.004, 0.916, 0.703, 0.044] rim [0.017, 0.631, 0.702, 0.044]
  - track 183 at frame 70: holes 0, rim-vs-core 0.28, rim-vs-outside 0.27, heterogeneity 0.06; core [0.003, 0.899, 0.613, 0.245] rim [0.014, 0.624, 0.599, 0.254]
  - track 77 at frame 37: holes 0, rim-vs-core 0.29, rim-vs-outside 0.29, heterogeneity 0.04; core [0.005, 0.906, 0.712, 0.028] rim [0.019, 0.615, 0.711, 0.027]
  - track 232 at frame 82: holes 0, rim-vs-core 0.27, rim-vs-outside 0.28, heterogeneity 0.05; core [0.004, 0.91, 0.637, 0.177] rim [0.016, 0.637, 0.632, 0.18]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 204 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial prey a: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.12, rim/outside 1.2 (aggregate of 204 individuals; 7/204 membrane-like individually; rim level 0.091)
  - radial predator b: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.04, rim/outside 6.98 (aggregate of 204 individuals; 38/204 membrane-like individually; rim level 0.663)
  - radial fuel u: peak at rho=1.65 (OUTSIDE the peak band 0.5-1.5), rim/core 1.04, rim/outside 0.995 (aggregate of 204 individuals; 0/204 membrane-like individually; rim level 0.635)
  - radial waste w: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.907, rim/outside 1.16 (aggregate of 204 individuals; 0/204 membrane-like individually; rim level 0.15)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #46 (t=3700, R_eq 4.15): none; #183 (t=7000, R_eq 4.69): none; #77 (t=3700, R_eq 3.57): none; #232 (t=8200, R_eq 3.34): none
- species `prey` (channels ['prey a'], own threshold): components final 4, mean 7.8, max 59; tracks 187, persistent 0; splits 36, persistent splits 0 (K=20), max generation 0, merges 9, merge/split 0.25; moving tracks 0
- species `predator` (channels ['predator b'], own threshold): components final 32, mean 32.4, max 40; tracks 209, persistent 6; splits 46, persistent splits 7 (K=20), max generation 1, merges 30, merge/split 0.652; moving tracks 9

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 43 of 204 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
