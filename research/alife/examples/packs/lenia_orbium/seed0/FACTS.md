# Evidence pack: lenia-orbium-ref (seed 0)

- world: `../../../lenia_orbium/world.py`, family `lenia`
- parent: None; mutation: reference
- run: 151 frames x 2 steps x dt 0.1 = time 30; grid [128, 128]; wall 0s; status ok
- command: `python -m labkit.run examples/lenia_orbium/world.py --out examples/packs/lenia_orbium --frames 150 --seeds 0 1 2`
- segmentation: matter > 0.35 of robust range [0.0, 0.9862], min area 6 px

## Measurements
- components: final 4, mean 2.6, max 5; occupancy final 0.01
- tracks: 31; persistent (alive >= 50% of run): 2; longest 105 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.58 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [8, 3, 2], H1 [1, 0, 0]
- motion: 5 long-lived tracks moved >= 1 body length; max speed 5.82/time; max body lengths 15.1
- replication (lineage window K = 20 frames = time 4, default): splits 9, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 4, merge/split ratio 0.444, nucleations 7
- channel total drift (end/start - 1): [-0.3226]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 13 at frame 97: holes 0, rim-vs-core 0.28, rim-vs-outside 0.43, heterogeneity 0.19; core [0.971] rim [0.696]
  - track 23 at frame 105: holes 0, rim-vs-core 0.29, rim-vs-outside 0.40, heterogeneity 0.20; core [0.958] rim [0.668]
  - track 0 at frame 25: holes 0, rim-vs-core 0.30, rim-vs-outside 0.40, heterogeneity 0.21; core [0.96] rim [0.664]
  - track 1 at frame 13: holes 0, rim-vs-core 0.28, rim-vs-outside 0.41, heterogeneity 0.20; core [0.979] rim [0.7]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 15 components >= 12 px at frames [25, 50, 76, 100, 125, 150]):
  - radial A: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.923, rim/outside 5.91 (aggregate of 15 individuals; 0/15 membrane-like individually; rim level 0.907)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #13 (t=19.4, R_eq 4.48): none; #23 (t=21, R_eq 4.55): none; #0 (t=5, R_eq 4.58): none; #1 (t=2.6, R_eq 4.48): none

## Warnings
- none

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
