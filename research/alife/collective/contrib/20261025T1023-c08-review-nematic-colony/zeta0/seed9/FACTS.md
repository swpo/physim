# Evidence pack: active-nematic-droplets (seed 9)

- world: `../../../../../../../home/user/physim/research/alife/collective/contrib/20261025T1014-c11-active-nematic-colony/world.py`, family `active-nematic`
- parent: None; mutation: new class: CH droplets with internal Landau-de Gennes nematic order and extensile active stress, Brinkman-Stokes flow
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 292s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1014-c11-active-nematic-colony/world.py --out /tmp/claude-0/-home-user-physim/b3c8c7c9-06fe-5142-8c86-74065d022b56/scratchpad/rev4/zeta0 --seeds 9 --no-movie`
- segmentation: matter > 0.47 of robust range [-0.8533, 0.9519], min area 6 px

## Measurements
- components: final 11, mean 10.1, max 11; occupancy final 0.07
- tracks: 11; persistent (alive >= 50% of run): 11; longest 192 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 19.71 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [12, 11, 11], H1 [0, 0, 0]
- motion: 3 long-lived tracks moved >= 1 body length; max speed 0.0125/time; max body lengths 1.4
- replication (lineage window K = 20 frames = time 100, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio n/a, nucleations 11
- channel total drift (end/start - 1): [-0.498, -0.0197, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 106: holes 0, rim-vs-core 0.47, rim-vs-outside 0.31, heterogeneity 0.18; core [0.888, 0.78, 0.451] rim [0.588, 0.423, 0.453]
  - track 1 at frame 106: holes 0, rim-vs-core 0.49, rim-vs-outside 0.32, heterogeneity 0.24; core [0.908, 0.841, 0.495] rim [0.6, 0.456, 0.486]
  - track 2 at frame 106: holes 0, rim-vs-core 0.48, rim-vs-outside 0.32, heterogeneity 0.22; core [0.907, 0.838, 0.458] rim [0.605, 0.461, 0.445]
  - track 3 at frame 108: holes 0, rim-vs-core 0.48, rim-vs-outside 0.32, heterogeneity 0.21; core [0.915, 0.857, 0.449] rim [0.615, 0.476, 0.431]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 66 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.887, rim/outside 26.1 (aggregate of 66 individuals; 0/66 membrane-like individually; rim level 0.881)
  - radial order |Q|: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.791, rim/outside 47.5 (aggregate of 66 individuals; 0/66 membrane-like individually; rim level 0.775)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=530, R_eq 4.48): none; #1 (t=530, R_eq 5.64): none; #2 (t=530, R_eq 5.47): none; #3 (t=540, R_eq 5.97): none

## Warnings
- none

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
