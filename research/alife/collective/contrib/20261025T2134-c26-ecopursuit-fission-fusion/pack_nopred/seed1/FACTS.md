# Evidence pack: eco-pursuit (seed 1)

- world: `../../world.py`, family `chemotaxis`
- parent: threads/chemotaxis-motility/worlds/evopursuit; mutation: all prey B (B0=1, m=0), species tracking, food- and prey-removal forks
- run: 201 frames x 240 steps x dt 0.05 = time 2400; grid [160, 160]; wall 333s; status ok
- command: `python -m labkit.run collective/contrib/_c26work/ep/world.py --out collective/contrib/_c26work/ep/pack_nopred --seeds 0 1 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 0.9937], min area 6 px

## Measurements
- components: final 6, mean 10.6, max 28; occupancy final 0.02
- tracks: 166; persistent (alive >= 50% of run): 0; longest 78 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [6, 6, 6], H1 [0, 0, 0]
- motion: 37 long-lived tracks moved >= 1 body length; max speed 0.268/time; max body lengths 24.1
- replication (lineage window K = 20 frames = time 240, default): splits 32, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 54, merge/split ratio 1.69, nucleations 50
- channel total drift (end/start - 1): [None, -0.6802, None, -0.0194]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 147 at frame 161: holes 0, rim-vs-core 0.62, rim-vs-outside 0.65, heterogeneity 0.16; core [0.99, 0.949, 0.0, 0.101] rim [0.645, 0.501, 0.0, 0.354]
  - track 146 at frame 156: holes 0, rim-vs-core 0.64, rim-vs-outside 0.61, heterogeneity 0.16; core [0.929, 0.954, 0.0, 0.1] rim [0.546, 0.513, 0.0, 0.352]
  - track 87 at frame 71: holes 0, rim-vs-core 0.60, rim-vs-outside 0.52, heterogeneity 0.17; core [0.725, 0.951, 0.0, 0.095] rim [0.394, 0.51, 0.0, 0.344]
  - track 95 at frame 76: holes 0, rim-vs-core 0.37, rim-vs-outside 0.75, heterogeneity 0.16; core [0.733, 0.945, 0.0, 0.11] rim [0.524, 0.671, 0.0, 0.25]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 58 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial preyA: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.872, rim/outside 25.5 (aggregate of 58 individuals; 0/58 membrane-like individually; rim level 0.421)
  - radial preyB: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.81, rim/outside 47.8 (aggregate of 58 individuals; 0/58 membrane-like individually; rim level 0.793)
  - radial predator: flat profile (no radial structure; level 0; aggregate of 58 individuals)
  - radial n: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 16.6, rim/outside 0.716 (aggregate of 58 individuals; 0/58 membrane-like individually; rim level 0.605)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #147 (t=1932, R_eq 5.05): none; #146 (t=1872, R_eq 5.08): none; #87 (t=852, R_eq 5.08): none; #95 (t=912, R_eq 5.11): none
- species `prey` (channels ['preyA', 'preyB'], own threshold): components final 6, mean 10.6, max 28; tracks 166, persistent 0; splits 32, persistent splits 0 (K=20), max generation 0, merges 54, merge/split 1.69; moving tracks 37
- species `predator` (channels ['predator'], own threshold): components final 0, mean 0.0, max 0; tracks 0, persistent 0; splits 0, persistent splits 0 (K=20), max generation 0, merges 0, merge/split n/a; moving tracks 0

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
