# Evidence pack: membrane-evo (seed 57)

- world: `../../world_twin.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/membrane_kinds (arm E of committee r2); identical-event design from fisim-beyond-laplacian xcell-evo2-S; mutation: kinds differ only in link yield b2; sealed catalyst channel (min face gate, fast outside decay); whole-cell flips + neutral tag + random disk deaths from a state-independent RNG
- run: 161 frames x 250 steps x dt 1.0 = time 40000; grid [128, 128]; wall 90s; status ok
- command: `python -m labkit.run collective/contrib/c17-mevo-wip/world_twin.py --out collective/contrib/c17-mevo-wip/twin/seed57 --seeds 57 --frames 160 --spf 250 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.7233], min area 6 px

## Measurements
- components: final 16, mean 11.1, max 17; occupancy final 0.28
- tracks: 86; persistent (alive >= 50% of run): 1; longest 121 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 6.36 (1 = constant size)
- enclosures: components with a hole mean 10.32, final 14; holes at thresholds 0.2/0.35/0.5 final [5, 14, 16]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [21, 16, 16], H1 [17, 16, 11]
- motion: 5 long-lived tracks moved >= 1 body length; max speed 0.00366/time; max body lengths 1.5
- replication (lineage window K = 20 frames = time 5000, default): splits 34, persistent splits 11 (0 more failed only because the siblings re-merged within K), max generation 3, merges 2, merge/split ratio 0.059, nucleations 0
- channel total drift (end/start - 1): [-0.7691, None, 0.0892, -0.1849]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 21 at frame 101: holes 1, rim-vs-core 0.37, rim-vs-outside 0.74, heterogeneity 0.20; core [0.861, 0.0, 0.618, 0.44] rim [0.538, 0.0, 0.56, 0.62]
  - track 45 at frame 102: holes 1, rim-vs-core 0.34, rim-vs-outside 0.75, heterogeneity 0.21; core [0.841, 0.0, 0.708, 0.462] rim [0.549, 0.0, 0.585, 0.592]
  - track 59 at frame 117: holes 1, rim-vs-core 0.45, rim-vs-outside 0.67, heterogeneity 0.22; core [0.868, 0.0, 0.737, 0.549] rim [0.453, 0.0, 0.556, 0.596]
  - track 48 at frame 99: holes 1, rim-vs-core 0.38, rim-vs-outside 0.67, heterogeneity 0.21; core [0.834, 0.0, 0.681, 0.586] rim [0.48, 0.0, 0.55, 0.62]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 76 components >= 12 px at frames [27, 54, 81, 106, 133, 160]):
  - radial K1: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.07, rim/outside 8.6 (aggregate of 76 individuals; 11/76 membrane-like individually; rim level 0.462)
  - radial K2: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 1.03, rim/outside 5.51 (aggregate of 76 individuals; 4/76 membrane-like individually; rim level 0.125)
  - radial L link: peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.37, rim/outside 5.89 (aggregate of 76 individuals; 52/76 membrane-like individually; rim level 0.485)
  - radial membrane (wall): peak at rho=0.95 (in the peak band 0.5-1.5), rim/core 3.97, rim/outside 4.2 (aggregate of 76 individuals; 66/76 membrane-like individually; rim level 0.475)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): membrane (wall)
- membrane-like channels per top track at mid-life: #21 (t=25250, R_eq 11.64, ring): ['membrane (wall)']; #45 (t=25500, R_eq 11.1, ring): ['K1', 'L link', 'membrane (wall)']; #59 (t=29250, R_eq 9.22, ring): ['K1', 'L link', 'membrane (wall)']; #48 (t=24750, R_eq 9.76, ring): ['K1', 'L link', 'membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 63 of 76 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
