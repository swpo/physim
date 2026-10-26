# Evidence pack: condensate-food-chain (seed 1)

- world: `../../world.py`, family `active-emulsion`
- parent: threads/active-droplets/worlds/ad1-fuel; mutation: two immiscible autocatalytic condensates in a closed chain: prey made from fuel, predator made from prey material; decay -> waste -> fuel
- run: 121 frames x 200 steps x dt 0.5 = time 12000; grid [128, 128]; wall 187s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/4e890ad6-3240-5329-a5c6-2d12ecca7a99/scratchpad/cl/world.py --out /tmp/claude-0/-home-user-physim/4e890ad6-3240-5329-a5c6-2d12ecca7a99/scratchpad/cl/pack/seed1 --seeds 1 --size 128 128 --frames 120 --lineage-k 5 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0315, 1.3365], min area 6 px

## Measurements
- components: final 32, mean 37.3, max 73; occupancy final 0.18
- tracks: 420; persistent (alive >= 50% of run): 0; longest 60 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 1.64, final 1; holes at thresholds 0.2/0.35/0.5 final [0, 1, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [38, 35, 20], H1 [2, 1, 0]
- motion: 13 long-lived tracks moved >= 1 body length; max speed 0.00591/time; max body lengths 1.5
- replication (lineage window K = 5 frames = time 500, --lineage-k): splits 135, persistent splits 67 (0 more failed only because the siblings re-merged within K), max generation 7, merges 36, merge/split ratio 0.267, nucleations 51
- channel total drift (end/start - 1): [-0.441, 2.9837, -0.3465, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 63 at frame 31: holes 0, rim-vs-core 0.26, rim-vs-outside 0.41, heterogeneity 0.06; core [0.909, 0.0, 0.047, 0.899] rim [0.659, 0.0, 0.102, 0.847]
  - track 1 at frame 27: holes 0, rim-vs-core 0.33, rim-vs-outside 0.32, heterogeneity 0.06; core [0.906, 0.0, 0.048, 0.896] rim [0.586, 0.0, 0.118, 0.832]
  - track 134 at frame 31: holes 0, rim-vs-core 0.32, rim-vs-outside 0.32, heterogeneity 0.06; core [0.908, 0.0, 0.045, 0.9] rim [0.607, 0.0, 0.116, 0.834]
  - track 386 at frame 115: holes 0, rim-vs-core 0.25, rim-vs-outside 0.25, heterogeneity 0.05; core [0.003, 0.847, 0.566, 0.247] rim [0.011, 0.596, 0.559, 0.248]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 198 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial prey a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.955, rim/outside 4.37 (aggregate of 198 individuals; 14/198 membrane-like individually; rim level 0.317)
  - radial predator b: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 1, rim/outside 4.91 (aggregate of 198 individuals; 19/198 membrane-like individually; rim level 0.435)
  - radial fuel u: peak at rho=1.95 (OUTSIDE the peak band 0.5-1.5), rim/core 1.28, rim/outside 0.947 (aggregate of 198 individuals; 0/198 membrane-like individually; rim level 0.48)
  - radial waste w: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.901, rim/outside 1.27 (aggregate of 198 individuals; 0/198 membrane-like individually; rim level 0.457)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #63 (t=3100, R_eq 4.92): none; #1 (t=2700, R_eq 5.14): none; #134 (t=3100, R_eq 5.23): none; #386 (t=11500, R_eq 5.53): none
- species `prey` (channels ['prey a'], own threshold): components final 6, mean 17.7, max 59; tracks 287, persistent 0; splits 79, persistent splits 17 (K=5), max generation 6, merges 9, merge/split 0.114; moving tracks 11
- species `predator` (channels ['predator b'], own threshold): components final 28, mean 23.0, max 29; tracks 288, persistent 0; splits 66, persistent splits 34 (K=5), max generation 2, merges 18, merge/split 0.273; moving tracks 21

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 25 of 198 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
