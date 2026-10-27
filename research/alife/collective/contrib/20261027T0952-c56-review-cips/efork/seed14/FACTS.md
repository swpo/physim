# Evidence pack: cips-consumer (seed 14)

- world: `../../../collective/contrib/20261026T1700-c43-cips-consumer/world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261026T1302-c42-foodchain-both-divide-claim; mutation: c42's predator condensate replaced by a conserved CIPS enzyme whose catalysis consumes prey material
- run: 41 frames x 400 steps x dt 0.25 = time 4000; grid [128, 128]; wall 80s; status ok
- command: `python -m labkit.run collective/contrib/20261026T1700-c43-cips-consumer/world.py --out c56work/cr/efork_s14 --seeds 14 --frames 40 --lineage-k 5 --no-movie`
- segmentation: matter > 0.35 of robust range [0.041, 1.9834], min area 6 px

## Measurements
- components: final 0, mean 31.4, max 84; occupancy final 0.00
- tracks: 275; persistent (alive >= 50% of run): 2; longest 27 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 16.50 (1 = constant size)
- enclosures: components with a hole mean 0.15, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [2, 2, 1], H1 [0, 0, 0]
- motion: 38 long-lived tracks moved >= 1 body length; max speed 0.025/time; max body lengths 4.7
- replication (lineage window K = 5 frames = time 500, --lineage-k): splits 98, persistent splits 16 (0 more failed only because the siblings re-merged within K), max generation 2, merges 4, merge/split ratio 0.041, nucleations 62
- channel total drift (end/start - 1): [-1.0, 0.0348, None, 0.0487]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 69 at frame 15: holes 0, rim-vs-core 0.40, rim-vs-outside 0.34, heterogeneity 0.28; core [0.774, 0.509, 0.539, 0.122] rim [0.526, 0.401, 0.248, 0.178]
  - track 112 at frame 14: holes 0, rim-vs-core 0.19, rim-vs-outside 0.53, heterogeneity 0.24; core [0.889, 0.263, 0.29, 0.057] rim [0.718, 0.25, 0.242, 0.122]
  - track 137 at frame 17: holes 0, rim-vs-core 0.34, rim-vs-outside 0.56, heterogeneity 0.29; core [0.857, 0.41, 0.495, 0.085] rim [0.587, 0.452, 0.316, 0.167]
  - track 208 at frame 23: holes 0, rim-vs-core 0.17, rim-vs-outside 0.29, heterogeneity 0.03; core [0.928, 0.021, 0.002, 0.028] rim [0.774, 0.019, 0.001, 0.1]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 149 components >= 12 px at frames [7, 13, 20, 27]):
  - radial prey a: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.94, rim/outside 8.64 (aggregate of 149 individuals; 14/149 membrane-like individually; rim level 0.7)
  - radial consumer q: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.79, rim/outside 8.66 (aggregate of 149 individuals; 15/149 membrane-like individually; rim level 0.319)
  - radial product r: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.704, rim/outside 13.2 (aggregate of 149 individuals; 11/149 membrane-like individually; rim level 0.274)
  - radial fuel u: peak at rho=2.25 (OUTSIDE the peak band 0.5-1.5), rim/core 2.66, rim/outside 0.763 (aggregate of 149 individuals; 0/149 membrane-like individually; rim level 0.218)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #69 (t=1500, R_eq 5.17): none; #112 (t=1400, R_eq 7, ring): ['consumer q', 'product r']; #137 (t=1700, R_eq 6.56): none; #208 (t=2300, R_eq 5.86): none
- species `prey` (channels ['prey a'], own threshold): components final 0, mean 29.4, max 70; tracks 285, persistent 2; splits 92, persistent splits 11 (K=5), max generation 2, merges 14, merge/split 0.152; moving tracks 29
- species `consumer` (channels ['consumer q'], own threshold): components final 0, mean 22.9, max 61; tracks 218, persistent 1; splits 42, persistent splits 6 (K=5), max generation 2, merges 5, merge/split 0.119; moving tracks 64

## Warnings
- no components at the end: matter died out or fell below threshold
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 9 of 149 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
