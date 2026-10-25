# Evidence pack: active-nematic-droplets (seed 0)

- world: `../world.py`, family `active-nematic`
- parent: None; mutation: new class: CH droplets with internal Landau-de Gennes nematic order and extensile active stress, Brinkman-Stokes flow
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 288s; status ok
- command: `python -m labkit.run /tmp/claude-0/c11ex/world.py --out /tmp/claude-0/c11ex/p_d00 --seeds 0 --no-movie`
- segmentation: matter > 0.48 of robust range [-0.9689, 1.029], min area 6 px

## Measurements
- components: final 10, mean 6.2, max 10; occupancy final 0.20
- tracks: 10; persistent (alive >= 50% of run): 8; longest 153 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 69.78 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [10, 10, 10], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.5
- replication (lineage window K = 20 frames = time 100, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio n/a, nucleations 10
- channel total drift (end/start - 1): [0.0, 2.0274, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 124: holes 0, rim-vs-core 0.39, rim-vs-outside 0.77, heterogeneity 0.19; core [0.987, 0.978, 0.443] rim [0.769, 0.657, 0.444]
  - track 1 at frame 129: holes 0, rim-vs-core 0.45, rim-vs-outside 0.59, heterogeneity 0.17; core [0.976, 0.952, 0.44] rim [0.715, 0.584, 0.438]
  - track 2 at frame 129: holes 0, rim-vs-core 0.38, rim-vs-outside 0.77, heterogeneity 0.21; core [0.987, 0.977, 0.437] rim [0.775, 0.662, 0.454]
  - track 3 at frame 129: holes 0, rim-vs-core 0.48, rim-vs-outside 0.58, heterogeneity 0.21; core [0.973, 0.946, 0.45] rim [0.691, 0.556, 0.467]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 42 components >= 12 px at frames [67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.956, rim/outside 20 (aggregate of 42 individuals; 0/42 membrane-like individually; rim level 0.949)
  - radial order |Q|: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.912, rim/outside 50.5 (aggregate of 42 individuals; 0/42 membrane-like individually; rim level 0.881)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=620, R_eq 12.24): none; #1 (t=645, R_eq 9.92): none; #2 (t=645, R_eq 10.94): none; #3 (t=645, R_eq 10): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
