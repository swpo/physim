# Evidence pack: lenia-orbium-ref (seed 1)

- world: `../../../lenia_orbium/world.py`, family `lenia`
- parent: None; mutation: reference
- run: 151 frames x 2 steps x dt 0.1 = time 30; grid [128, 128]; wall 0s; status ok
- command: `python -m labkit.run examples/lenia_orbium/world.py --out examples/packs/lenia_orbium --frames 150 --seeds 0 1 2`
- segmentation: matter > 0.35 of robust range [0.0, 1.0], min area 6 px

## Measurements
- components: final 10, mean 3.7, max 10; occupancy final 0.03
- tracks: 50; persistent (alive >= 50% of run): 3; longest 126 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.55 (1 = constant size)
- enclosures: components with a hole mean 0.09, final 1; holes at thresholds 0.2/0.35/0.5 final [0, 1, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [14, 11, 7], H1 [4, 1, 0]
- motion: 3 long-lived tracks moved >= 1 body length; max speed 5.86/time; max body lengths 18.2
- replication (lineage window K = 20 frames = time 4, default): splits 18, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 8, merge/split ratio 0.444, nucleations 3
- channel total drift (end/start - 1): [1.3064]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1 at frame 63: holes 0, rim-vs-core 0.30, rim-vs-outside 0.39, heterogeneity 0.20; core [0.936] rim [0.632]
  - track 0 at frame 55: holes 0, rim-vs-core 0.19, rim-vs-outside 0.48, heterogeneity 0.20; core [0.93] rim [0.735]
  - track 2 at frame 55: holes 0, rim-vs-core 0.29, rim-vs-outside 0.39, heterogeneity 0.20; core [0.933] rim [0.644]
  - track 23 at frame 142: holes 0, rim-vs-core 0.25, rim-vs-outside 0.39, heterogeneity 0.20; core [0.923] rim [0.672]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 25 components >= 12 px at frames [25, 50, 76, 100, 125, 150]):
  - radial A: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.879, rim/outside 6.08 (aggregate of 25 individuals; 4/25 membrane-like individually; rim level 0.717)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #1 (t=12.6, R_eq 4.41): none; #0 (t=11, R_eq 4.41): none; #2 (t=11, R_eq 4.41): none; #23 (t=28.4, R_eq 4.48): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 3 of 25 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
