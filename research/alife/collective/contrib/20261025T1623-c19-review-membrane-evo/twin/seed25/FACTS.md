# Evidence pack: membrane-evo (seed 25)

- world: `../../../../../threads/autopoiesis/worlds/membrane_evo/world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/membrane_kinds (arm E of committee r2); identical-event design from fisim-beyond-laplacian xcell-evo2-S; mutation: kinds differ only in link yield b2; sealed catalyst channel (min face gate, fast outside decay); whole-cell flips + neutral tag + random disk deaths from a state-independent RNG
- run: 161 frames x 250 steps x dt 1.0 = time 40000; grid [128, 128]; wall 103s; status ok
- command: `python -m labkit.run threads/autopoiesis/worlds/membrane_evo/world.py --out collective/contrib/20261025T1623-c19-review-membrane-evo/twin/seed25 --seeds 25 --frames 160 --spf 250 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.7248], min area 6 px

## Measurements
- components: final 13, mean 11.1, max 17; occupancy final 0.28
- tracks: 87; persistent (alive >= 50% of run): 3; longest 108 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 12.58 (1 = constant size)
- enclosures: components with a hole mean 10.42, final 13; holes at thresholds 0.2/0.35/0.5 final [6, 15, 14]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [14, 13, 13], H1 [15, 14, 8]
- motion: 11 long-lived tracks moved >= 1 body length; max speed 0.00304/time; max body lengths 1.2
- replication (lineage window K = 20 frames = time 5000, default): splits 32, persistent splits 12 (0 more failed only because the siblings re-merged within K), max generation 3, merges 1, merge/split ratio 0.031, nucleations 0
- channel total drift (end/start - 1): [-0.7401, None, 0.1178, -0.1233]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 43 at frame 108: holes 1, rim-vs-core 0.38, rim-vs-outside 0.67, heterogeneity 0.21; core [0.823, 0.0, 0.677, 0.591] rim [0.464, 0.0, 0.545, 0.624]
  - track 32 at frame 89: holes 1, rim-vs-core 0.35, rim-vs-outside 0.73, heterogeneity 0.21; core [0.006, 0.936, 0.66, 0.585] rim [0.004, 0.599, 0.558, 0.631]
  - track 44 at frame 102: holes 1, rim-vs-core 0.40, rim-vs-outside 0.67, heterogeneity 0.22; core [0.094, 0.857, 0.644, 0.56] rim [0.053, 0.486, 0.505, 0.625]
  - track 52 at frame 122: holes 1, rim-vs-core 0.34, rim-vs-outside 0.74, heterogeneity 0.20; core [0.847, 0.0, 0.652, 0.516] rim [0.533, 0.0, 0.565, 0.614]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 74 components >= 12 px at frames [27, 54, 81, 106, 133, 160]):
  - radial K1: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.13, rim/outside 8.55 (aggregate of 74 individuals; 18/74 membrane-like individually; rim level 0.468)
  - radial K2: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.17, rim/outside 5.94 (aggregate of 74 individuals; 4/74 membrane-like individually; rim level 0.124)
  - radial L link: peak at rho=0.95 (in the peak band 0.5-1.5), rim/core 1.43, rim/outside 5.72 (aggregate of 74 individuals; 50/74 membrane-like individually; rim level 0.472)
  - radial membrane (wall): peak at rho=1.05 (in the peak band 0.5-1.5), rim/core 4.3, rim/outside 4.12 (aggregate of 74 individuals; 64/74 membrane-like individually; rim level 0.472)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): membrane (wall)
- membrane-like channels per top track at mid-life: #43 (t=27000, R_eq 9.85, ring): ['K1', 'L link', 'membrane (wall)']; #32 (t=22250, R_eq 9.49, ring): ['K2', 'L link', 'membrane (wall)']; #44 (t=25500, R_eq 9.64, ring): ['L link', 'membrane (wall)']; #52 (t=30500, R_eq 10.6, ring): ['L link', 'membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 63 of 74 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
