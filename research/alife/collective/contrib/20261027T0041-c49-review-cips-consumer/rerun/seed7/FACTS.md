# Evidence pack: cips-consumer (seed 7)

- world: `../../../20261026T1700-c43-cips-consumer/world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261026T1302-c42-foodchain-both-divide-claim; mutation: c42's predator condensate replaced by a conserved CIPS enzyme whose catalysis consumes prey material
- run: 121 frames x 400 steps x dt 0.25 = time 12000; grid [128, 128]; wall 221s; status ok
- command: `python -m labkit.run collective/contrib/20261026T1700-c43-cips-consumer/world.py --out collective/contrib/c49rev2/rerun/seed7 --seeds 7 --frames 120 --lineage-k 5 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0379, 1.9942], min area 6 px

## Measurements
- components: final 42, mean 39.6, max 81; occupancy final 0.19
- tracks: 918; persistent (alive >= 50% of run): 0; longest 37 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.05, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [49, 44, 36], H1 [0, 0, 0]
- motion: 144 long-lived tracks moved >= 1 body length; max speed 0.0247/time; max body lengths 4.8
- replication (lineage window K = 5 frames = time 500, --lineage-k): splits 405, persistent splits 89 (0 more failed only because the siblings re-merged within K), max generation 8, merges 16, merge/split ratio 0.04, nucleations 83
- channel total drift (end/start - 1): [0.0287, 0.0191, None, -0.5944]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 627 at frame 97: holes 0, rim-vs-core 0.42, rim-vs-outside 0.55, heterogeneity 0.29; core [0.769, 0.557, 0.592, 0.129] rim [0.514, 0.46, 0.279, 0.198]
  - track 672 at frame 101: holes 0, rim-vs-core 0.34, rim-vs-outside 0.43, heterogeneity 0.26; core [0.684, 0.609, 0.581, 0.164] rim [0.513, 0.466, 0.326, 0.212]
  - track 87 at frame 16: holes 0, rim-vs-core 0.36, rim-vs-outside 0.37, heterogeneity 0.27; core [0.73, 0.53, 0.489, 0.142] rim [0.491, 0.387, 0.267, 0.206]
  - track 685 at frame 93: holes 0, rim-vs-core 0.48, rim-vs-outside 0.38, heterogeneity 0.28; core [0.732, 0.591, 0.599, 0.141] rim [0.497, 0.394, 0.242, 0.202]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 234 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial prey a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.904, rim/outside 10.7 (aggregate of 234 individuals; 16/234 membrane-like individually; rim level 0.68)
  - radial consumer q: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.776, rim/outside 8.85 (aggregate of 234 individuals; 19/234 membrane-like individually; rim level 0.33)
  - radial product r: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.676, rim/outside 13.1 (aggregate of 234 individuals; 14/234 membrane-like individually; rim level 0.281)
  - radial fuel u: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 2.66, rim/outside 0.768 (aggregate of 234 individuals; 0/234 membrane-like individually; rim level 0.228)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #627 (t=9700, R_eq 6.1): none; #672 (t=10100, R_eq 5.01): none; #87 (t=1600, R_eq 5.84): none; #685 (t=9300, R_eq 4.82): none
- species `prey` (channels ['prey a'], own threshold): components final 39, mean 37.3, max 70; tracks 897, persistent 0; splits 391, persistent splits 83 (K=5), max generation 8, merges 25, merge/split 0.064; moving tracks 109
- species `consumer` (channels ['consumer q'], own threshold): components final 35, mean 30.2, max 66; tracks 732, persistent 0; splits 228, persistent splits 30 (K=5), max generation 4, merges 12, merge/split 0.053; moving tracks 284

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 9 of 234 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
