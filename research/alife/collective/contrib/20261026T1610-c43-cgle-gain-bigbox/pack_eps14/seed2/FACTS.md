# Evidence pack: cgle-gain (seed 2)

- world: `../../world.py`, family `cgle`
- parent: collective/contrib/20261025T0841-c03-cgle-solitons; mutation: the CGLE linear gain becomes a local gain medium g, depleted by |A|^2 and regrowing toward g0
- run: 201 frames x 500 steps x dt 0.01 = time 1000; grid [192, 192]; wall 1400s; status ok
- command: `python -m labkit.run collective/contrib/20261026T1610-c43-cgle-gain-bigbox/world.py --out collective/contrib/20261026T1610-c43-cgle-gain-bigbox/pack_eps14/seed2 --seeds 2 --size 192 192 --frames 200 --no-movie`
- segmentation: matter > 0.21 of robust range [0.0, 2.3506], min area 6 px

## Measurements
- components: final 6, mean 10.6, max 16; occupancy final 0.02
- tracks: 45; persistent (alive >= 50% of run): 8; longest 197 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 8.47 (1 = constant size)
- enclosures: components with a hole mean 0.03, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [6, 6, 6], H1 [0, 0, 0]
- motion: 12 long-lived tracks moved >= 1 body length; max speed 0.0967/time; max body lengths 2.2
- replication (lineage window K = 20 frames = time 100, default): splits 10, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 15, merge/split ratio 1.5, nucleations 0
- channel total drift (end/start - 1): [-0.9758, -1.0758, -0.0574]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 8 at frame 103: holes 0, rim-vs-core 0.49, rim-vs-outside 0.15, heterogeneity 0.20; core [0.727, 0.112, 0.514] rim [0.282, 0.284, 0.607]
  - track 21 at frame 104: holes 0, rim-vs-core 0.51, rim-vs-outside 0.15, heterogeneity 0.20; core [0.733, 0.08, 0.532] rim [0.278, 0.277, 0.633]
  - track 31 at frame 136: holes 0, rim-vs-core 0.49, rim-vs-outside 0.15, heterogeneity 0.19; core [0.728, 0.109, 0.473] rim [0.294, 0.315, 0.575]
  - track 13 at frame 69: holes 0, rim-vs-core 0.47, rim-vs-outside 0.14, heterogeneity 0.21; core [0.728, 0.207, 0.425] rim [0.292, 0.368, 0.513]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 62 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial |A|: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.613, rim/outside 19.9 (aggregate of 62 individuals; 0/62 membrane-like individually; rim level 0.569)
  - radial Re A: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.983, rim/outside 1.02 (aggregate of 62 individuals; 2/62 membrane-like individually; rim level 0.396)
  - radial g: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.81, rim/outside 0.858 (aggregate of 62 individuals; 0/62 membrane-like individually; rim level 0.604)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #8 (t=515, R_eq 5.7): none; #21 (t=520, R_eq 5.86): none; #31 (t=680, R_eq 5.29): none; #13 (t=345, R_eq 5.47): none

## Warnings
- matter fills >80% of the domain at some point: components may be one connected sea
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
