# Evidence pack: membrane-evo (seed 23)

- world: `../../../../../../../../../home/user/physim/research/alife/threads/autopoiesis/worlds/membrane_evo/world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/membrane_kinds (arm E of committee r2); identical-event design from fisim-beyond-laplacian xcell-evo2-S; mutation: kinds differ only in link yield b2; sealed catalyst channel (min face gate, fast outside decay); whole-cell flips + neutral tag + random disk deaths from a state-independent RNG
- run: 161 frames x 250 steps x dt 1.0 = time 40000; grid [128, 128]; wall 140s; status ok
- command: `python -m labkit.run threads/autopoiesis/worlds/membrane_evo/world.py --out /tmp/claude-0/-home-user-physim/ca3fe853-e88d-58ad-9551-2586c1b06c34/scratchpad/rev/evo/twin/seed23 --seeds 23 --frames 160 --spf 250 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.7275], min area 6 px

## Measurements
- components: final 13, mean 11.3, max 29; occupancy final 0.26
- tracks: 107; persistent (alive >= 50% of run): 0; longest 79 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 10.35, final 12; holes at thresholds 0.2/0.35/0.5 final [7, 12, 12]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [13, 13, 13], H1 [12, 12, 9]
- motion: 7 long-lived tracks moved >= 1 body length; max speed 0.00236/time; max body lengths 2.3
- replication (lineage window K = 20 frames = time 5000, default): splits 39, persistent splits 10 (0 more failed only because the siblings re-merged within K), max generation 4, merges 0, merge/split ratio 0, nucleations 0
- channel total drift (end/start - 1): [-0.6553, None, 0.0836, -0.0161]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 67 at frame 120: holes 1, rim-vs-core 0.34, rim-vs-outside 0.71, heterogeneity 0.20; core [0.806, 0.0, 0.66, 0.584] rim [0.493, 0.0, 0.552, 0.636]
  - track 70 at frame 125: holes 1, rim-vs-core 0.43, rim-vs-outside 0.72, heterogeneity 0.23; core [0.0, 0.998, 0.675, 0.556] rim [0.0, 0.584, 0.564, 0.624]
  - track 52 at frame 97: holes 1, rim-vs-core 0.29, rim-vs-outside 0.73, heterogeneity 0.21; core [0.8, 0.0, 0.668, 0.596] rim [0.528, 0.0, 0.567, 0.603]
  - track 97 at frame 148: holes 1, rim-vs-core 0.50, rim-vs-outside 0.75, heterogeneity 0.21; core [0.943, 0.0, 0.695, 0.294] rim [0.551, 0.0, 0.587, 0.576]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 69 components >= 12 px at frames [27, 54, 81, 106, 133, 160]):
  - radial K1: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.12, rim/outside 8.14 (aggregate of 69 individuals; 6/69 membrane-like individually; rim level 0.563)
  - radial K2: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1.07, rim/outside 3.42 (aggregate of 69 individuals; 1/69 membrane-like individually; rim level 0.0309)
  - radial L link: peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.4, rim/outside 5.66 (aggregate of 69 individuals; 47/69 membrane-like individually; rim level 0.491)
  - radial membrane (wall): peak at rho=0.95 (in the peak band 0.5-1.5), rim/core 3.83, rim/outside 4.01 (aggregate of 69 individuals; 56/69 membrane-like individually; rim level 0.471)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): membrane (wall)
- membrane-like channels per top track at mid-life: #67 (t=30000, R_eq 8.88, ring): ['L link', 'membrane (wall)']; #70 (t=31250, R_eq 8.61, ring): ['L link', 'membrane (wall)']; #52 (t=24250, R_eq 10.91, ring): ['K1', 'L link', 'membrane (wall)']; #97 (t=37000, R_eq 12.21, ring): ['membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 59 of 69 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
