# Evidence pack: driven-condensate-prey-predator (seed 11)

- world: `../../../collective/contrib/20261026T2103-c46-hunting-ecology-claim/world.py`, family `active-emulsion`
- parent: collective/contrib/20261026T1302-c42-foodchain-both-divide-claim; mutation: prey condensate whose miscibility gap is opened only by its own fuel-driven catalysis product (active chi); prey matter recycled from predator waste, not made from fuel
- run: 81 frames x 500 steps x dt 0.2 = time 8000; grid [128, 128]; wall 285s; status ok
- command: `python -m labkit.run collective/contrib/20261026T2103-c46-hunting-ecology-claim/world.py --out c56work/rv/efork128 --seeds 11 --size 128 128 --frames 80 --lineage-k 5 --no-movie`
- segmentation: matter > 0.34 of robust range [0.1431, 1.2008], min area 6 px

## Measurements
- components: final 14, mean 15.7, max 31; occupancy final 0.05
- tracks: 34; persistent (alive >= 50% of run): 13; longest 80 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 22.67 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [15, 14, 14], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.5
- replication (lineage window K = 5 frames = time 500, --lineage-k): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio n/a, nucleations 34
- channel total drift (end/start - 1): [-0.1343, None, -1.0, -1.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 41: holes 0, rim-vs-core 0.30, rim-vs-outside 0.27, heterogeneity 0.05; core [0.005, 0.869, 0.596, 0.072] rim [0.018, 0.566, 0.593, 0.081]
  - track 1 at frame 41: holes 0, rim-vs-core 0.35, rim-vs-outside 0.27, heterogeneity 0.05; core [0.001, 0.875, 0.639, 0.071] rim [0.013, 0.527, 0.636, 0.081]
  - track 6 at frame 43: holes 0, rim-vs-core 0.33, rim-vs-outside 0.25, heterogeneity 0.05; core [0.007, 0.848, 0.608, 0.076] rim [0.021, 0.517, 0.605, 0.085]
  - track 8 at frame 43: holes 0, rim-vs-core 0.27, rim-vs-outside 0.22, heterogeneity 0.04; core [0.004, 0.809, 0.615, 0.072] rim [0.015, 0.537, 0.613, 0.08]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 97 components >= 12 px at frames [13, 27, 40, 53, 67, 80]):
  - radial prey a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.814, rim/outside 2.97 (aggregate of 97 individuals; 2/97 membrane-like individually; rim level 0.271)
  - radial predator b: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.88, rim/outside 17.7 (aggregate of 97 individuals; 0/97 membrane-like individually; rim level 0.566)
  - radial fuel F: peak at rho=2.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1.15, rim/outside 0.955 (aggregate of 97 individuals; 0/97 membrane-like individually; rim level 0.364)
  - radial product p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.869, rim/outside 2.85 (aggregate of 97 individuals; 2/97 membrane-like individually; rim level 0.304)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=4100, R_eq 2.88): none; #1 (t=4100, R_eq 3.19): none; #6 (t=4300, R_eq 2.93): none; #8 (t=4300, R_eq 2.99): none
- species `prey` (channels ['prey a'], own threshold): components final 0, mean 7.4, max 18; tracks 44, persistent 1; splits 4, persistent splits 0 (K=5), max generation 0, merges 1, merge/split 0.25; moving tracks 4
- species `predator` (channels ['predator b'], own threshold): components final 14, mean 10.3, max 17; tracks 25, persistent 3; splits 0, persistent splits 0 (K=5), max generation 0, merges 0, merge/split n/a; moving tracks 0

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
