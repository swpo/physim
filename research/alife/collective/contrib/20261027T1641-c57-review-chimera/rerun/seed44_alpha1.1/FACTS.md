# Evidence pack: chimera-field (seed 44)

- world: `../../20261027T1049-c55-chimera-field-negative/world.py`, family `nonlocal-oscillators`
- parent: None; mutation: -
- run: 151 frames x 100 steps x dt 0.1 = time 1500; grid [128, 128]; wall 25s; status ok
- command: `python -m labkit.run collective/contrib/20261027T1049-c55-chimera-field-negative/world.py --out collective/contrib/c57-w16/a1.1 --seeds 44 --frames 150 --spf 100 --no-movie`
- segmentation: matter > 0.33 of robust range [0.0, 0.9153], min area 6 px

## Measurements
- components: final 0, mean 0.7, max 5; occupancy final 0.00
- tracks: 64; persistent (alive >= 50% of run): 0; longest 10 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.04, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [1, 1, 1], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 1.9
- replication (lineage window K = 20 frames = time 200, default): splits 21, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 16, merge/split ratio 0.762, nucleations 6
- channel total drift (end/start - 1): [None, -1.0, 0.0, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 13 at frame 13: holes 0, rim-vs-core 0.34, rim-vs-outside 0.19, heterogeneity 0.19; core [0.698, 0.61, 0.0, 0.481] rim [0.445, 0.434, 0.0, 0.332]
  - track 58 at frame 44: holes 0, rim-vs-core 0.09, rim-vs-outside 0.32, heterogeneity 0.17; core [0.6, 0.518, 0.0, 0.371] rim [0.506, 0.507, 0.0, 0.368]
  - track 22 at frame 13: holes 0, rim-vs-core 0.34, rim-vs-outside 0.47, heterogeneity 0.19; core [0.663, 0.232, 0.0, 0.508] rim [0.609, 0.562, 0.0, 0.457]
  - track 52 at frame 34: holes 0, rim-vs-core 0.36, rim-vs-outside 0.27, heterogeneity 0.19; core [0.771, 0.541, 0.0, 0.569] rim [0.474, 0.444, 0.0, 0.382]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 2 components >= 12 px at frames [25]):
  - radial incoherence 1-|Z|: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 0.64, rim/outside 1.04 (aggregate of 2 individuals; 0/2 membrane-like individually; rim level 0.431)
  - radial cos phase: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1.11, rim/outside 1.06 (aggregate of 2 individuals; 0/2 membrane-like individually; rim level 0.484)
  - radial fuel Y: flat profile (no radial structure; level 0; aggregate of 2 individuals)
  - radial local frequency: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 0.677, rim/outside 1.07 (aggregate of 2 individuals; 0/2 membrane-like individually; rim level 0.338)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #13 (t=130, R_eq 13.15): none; #58 (t=440, R_eq 31.14): none; #22 (t=130, R_eq 47.75): none; #52 (t=340, R_eq 15.4): none

## Warnings
- no components at the end: matter died out or fell below threshold
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
