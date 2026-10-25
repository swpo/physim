# Evidence pack: cgle-solitons (seed 1)

- world: `../../world.py`, family `cgle`
- parent: None; mutation: new class: cubic-quintic complex Ginzburg-Landau (Akhmediev / Soto-Crespo dissipative solitons)
- run: 151 frames x 200 steps x dt 0.01 = time 300; grid [96, 96]; wall 25s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0841-c03-cgle-solitons/world.py --out collective/contrib/20261025T0841-c03-cgle-solitons/pack --seeds 0 1 --frames 150 --no-movie`
- segmentation: matter > 0.22 of robust range [0.0005, 2.2743], min area 6 px

## Measurements
- components: final 17, mean 17.7, max 27; occupancy final 0.08
- tracks: 103; persistent (alive >= 50% of run): 17; longest 148 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 6.66 (1 = constant size)
- enclosures: components with a hole mean 0.03, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [17, 17, 17], H1 [0, 0, 0]
- motion: 2 long-lived tracks moved >= 1 body length; max speed 0.0416/time; max body lengths 1.7
- replication (lineage window K = 20 frames = time 40, default): splits 29, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 34, merge/split ratio 1.17, nucleations 0
- channel total drift (end/start - 1): [-0.886, 1.6348]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 17 at frame 77: holes 0, rim-vs-core 0.35, rim-vs-outside 0.15, heterogeneity 0.12; core [0.703, 0.572] rim [0.358, 0.547]
  - track 36 at frame 77: holes 0, rim-vs-core 0.38, rim-vs-outside 0.18, heterogeneity 0.15; core [0.703, 0.018] rim [0.359, 0.175]
  - track 38 at frame 77: holes 0, rim-vs-core 0.39, rim-vs-outside 0.16, heterogeneity 0.15; core [0.679, 0.024] rim [0.33, 0.192]
  - track 48 at frame 78: holes 0, rim-vs-core 0.41, rim-vs-outside 0.18, heterogeneity 0.17; core [0.704, 0.927] rim [0.36, 0.708]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 107 components >= 12 px at frames [25, 50, 76, 100, 125, 150]):
  - radial |A|: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.585, rim/outside 9.96 (aggregate of 107 individuals; 0/107 membrane-like individually; rim level 0.552)
  - radial Re A: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1.01, rim/outside 0.988 (aggregate of 107 individuals; 0/107 membrane-like individually; rim level 0.434)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #17 (t=154, R_eq 3.78): none; #36 (t=154, R_eq 3.78): none; #38 (t=154, R_eq 3.91): none; #48 (t=156, R_eq 3.78): none

## Warnings
- matter fills >80% of the domain at some point: components may be one connected sea
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
