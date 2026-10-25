# Evidence pack: cgle-solitons (seed 0)

- world: `../../world.py`, family `cgle`
- parent: None; mutation: new class: cubic-quintic complex Ginzburg-Landau (Akhmediev / Soto-Crespo dissipative solitons)
- run: 151 frames x 200 steps x dt 0.01 = time 300; grid [96, 96]; wall 28s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0841-c03-cgle-solitons/world.py --out collective/contrib/20261025T0841-c03-cgle-solitons/pack --seeds 0 1 --frames 150 --no-movie`
- segmentation: matter > 0.22 of robust range [0.0003, 2.2555], min area 6 px

## Measurements
- components: final 15, mean 18.5, max 33; occupancy final 0.07
- tracks: 95; persistent (alive >= 50% of run): 14; longest 145 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 10.17 (1 = constant size)
- enclosures: components with a hole mean 0.05, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [15, 15, 15], H1 [0, 0, 0]
- motion: 3 long-lived tracks moved >= 1 body length; max speed 0.0792/time; max body lengths 1.7
- replication (lineage window K = 20 frames = time 40, default): splits 21, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 30, merge/split ratio 1.43, nucleations 0
- channel total drift (end/start - 1): [-0.898, -1.6637]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 53 at frame 78: holes 0, rim-vs-core 0.37, rim-vs-outside 0.16, heterogeneity 0.15; core [0.703, 0.793] rim [0.359, 0.65]
  - track 60 at frame 79: holes 0, rim-vs-core 0.35, rim-vs-outside 0.14, heterogeneity 0.14; core [0.698, 0.389] rim [0.352, 0.457]
  - track 61 at frame 79: holes 0, rim-vs-core 0.39, rim-vs-outside 0.17, heterogeneity 0.16; core [0.707, 0.036] rim [0.361, 0.215]
  - track 69 at frame 79: holes 0, rim-vs-core 0.39, rim-vs-outside 0.15, heterogeneity 0.16; core [0.696, 0.08] rim [0.355, 0.265]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 107 components >= 12 px at frames [25, 50, 76, 100, 125, 150]):
  - radial |A|: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.585, rim/outside 9.71 (aggregate of 107 individuals; 0/107 membrane-like individually; rim level 0.552)
  - radial Re A: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.901, rim/outside 1.02 (aggregate of 107 individuals; 0/107 membrane-like individually; rim level 0.452)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #53 (t=156, R_eq 3.78): none; #60 (t=158, R_eq 3.78): none; #61 (t=158, R_eq 3.7): none; #69 (t=158, R_eq 3.74): none

## Warnings
- matter fills >80% of the domain at some point: components may be one connected sea
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
