# Evidence pack: driven-condensate-prey-predator (seed 4)

- world: `../../world_claim.py`, family `active-emulsion`
- parent: collective/contrib/20261026T1302-c42-foodchain-both-divide-claim; mutation: prey condensate whose miscibility gap is opened only by its own fuel-driven catalysis product (active chi); prey matter recycled from predator waste, not made from fuel
- run: 71 frames x 500 steps x dt 0.2 = time 7000; grid [128, 128]; wall 165s; status ok
- command: `python -m labkit.run world_claim.py --out rerun/fork_nopred_seed4 --seeds 4 --frames 70 --no-movie`
- segmentation: matter > 0.50 of robust range [0.126, 0.8799], min area 6 px

## Measurements
- components: final 0, mean 14.5, max 19; occupancy final 0.00
- tracks: 19; persistent (alive >= 50% of run): 18; longest 61 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 23.12 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [3, 1, 1], H1 [3, 1, 1]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.6
- replication (lineage window K = 20 frames = time 2000, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio n/a, nucleations 19
- channel total drift (end/start - 1): [0.0, None, -1.0, -1.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 32: holes 0, rim-vs-core 0.29, rim-vs-outside 0.52, heterogeneity 0.07; core [0.947, 0.0, 0.203, 0.879] rim [0.717, 0.0, 0.268, 0.709]
  - track 1 at frame 33: holes 0, rim-vs-core 0.29, rim-vs-outside 0.52, heterogeneity 0.07; core [0.947, 0.0, 0.206, 0.89] rim [0.716, 0.0, 0.275, 0.723]
  - track 2 at frame 32: holes 0, rim-vs-core 0.27, rim-vs-outside 0.51, heterogeneity 0.07; core [0.926, 0.0, 0.202, 0.853] rim [0.707, 0.0, 0.271, 0.706]
  - track 3 at frame 33: holes 0, rim-vs-core 0.38, rim-vs-outside 0.29, heterogeneity 0.08; core [0.912, 0.0, 0.231, 0.892] rim [0.626, 0.0, 0.293, 0.647]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 90 components >= 12 px at frames [12, 23, 35, 47, 58]):
  - radial prey a: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.896, rim/outside 21.4 (aggregate of 90 individuals; 0/90 membrane-like individually; rim level 0.868)
  - radial predator b: flat profile (no radial structure; level 0; aggregate of 90 individuals)
  - radial fuel F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.81, rim/outside 0.811 (aggregate of 90 individuals; 0/90 membrane-like individually; rim level 0.37)
  - radial product p: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.947, rim/outside 8.11 (aggregate of 90 individuals; 0/90 membrane-like individually; rim level 0.867)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=3200, R_eq 6.26): none; #1 (t=3300, R_eq 6.46): none; #2 (t=3200, R_eq 7.02): none; #3 (t=3300, R_eq 5.73): none
- species `prey` (channels ['prey a'], own threshold): components final 0, mean 15.5, max 19; tracks 19, persistent 19; splits 0, persistent splits 0 (K=20), max generation 0, merges 0, merge/split n/a; moving tracks 0
- species `predator` (channels ['predator b'], own threshold): components final 0, mean 0.0, max 0; tracks 0, persistent 0; splits 0, persistent splits 0 (K=20), max generation 0, merges 0, merge/split n/a; moving tracks 0

## Warnings
- no components at the end: matter died out or fell below threshold
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
