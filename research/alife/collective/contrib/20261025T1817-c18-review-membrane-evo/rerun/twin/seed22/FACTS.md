# Evidence pack: membrane-evo (seed 22)

- world: `../../../../../../../../home/user/physim/research/alife/threads/autopoiesis/worlds/membrane_evo/world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/membrane_kinds (arm E of committee r2); identical-event design from fisim-beyond-laplacian xcell-evo2-S; mutation: kinds differ only in link yield b2; sealed catalyst channel (min face gate, fast outside decay); whole-cell flips + neutral tag + random disk deaths from a state-independent RNG
- run: 161 frames x 250 steps x dt 1.0 = time 40000; grid [128, 128]; wall 87s; status ok
- command: `python -m labkit.run threads/autopoiesis/worlds/membrane_evo/world.py --out /tmp/claude-0/-home-user-physim/3b801bf0-17d3-5f80-b419-db17577ce992/scratchpad/rev6/twin --seeds 21 22 --frames 160 --spf 250 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.7304], min area 6 px

## Measurements
- components: final 15, mean 11.8, max 19; occupancy final 0.27
- tracks: 98; persistent (alive >= 50% of run): 5; longest 103 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 9.51 (1 = constant size)
- enclosures: components with a hole mean 10.81, final 12; holes at thresholds 0.2/0.35/0.5 final [6, 14, 13]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [18, 15, 15], H1 [14, 13, 4]
- motion: 5 long-lived tracks moved >= 1 body length; max speed 0.00379/time; max body lengths 1.7
- replication (lineage window K = 20 frames = time 5000, default): splits 39, persistent splits 11 (0 more failed only because the siblings re-merged within K), max generation 4, merges 4, merge/split ratio 0.103, nucleations 0
- channel total drift (end/start - 1): [-0.7593, None, 0.0838, -0.244]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 55 at frame 113: holes 1, rim-vs-core 0.40, rim-vs-outside 0.77, heterogeneity 0.20; core [0.0, 0.949, 0.629, 0.446] rim [0.0, 0.593, 0.562, 0.625]
  - track 54 at frame 110: holes 1, rim-vs-core 0.40, rim-vs-outside 0.70, heterogeneity 0.22; core [0.0, 0.898, 0.716, 0.559] rim [0.0, 0.529, 0.572, 0.614]
  - track 75 at frame 126: holes 1, rim-vs-core 0.36, rim-vs-outside 0.75, heterogeneity 0.21; core [0.864, 0.0, 0.64, 0.45] rim [0.547, 0.0, 0.577, 0.612]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 80 components >= 12 px at frames [27, 54, 81, 106, 133, 160]):
  - radial K1: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.16, rim/outside 8.03 (aggregate of 80 individuals; 7/80 membrane-like individually; rim level 0.439)
  - radial K2: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.21, rim/outside 7.59 (aggregate of 80 individuals; 7/80 membrane-like individually; rim level 0.191)
  - radial L link: peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.54, rim/outside 5.78 (aggregate of 80 individuals; 63/80 membrane-like individually; rim level 0.512)  MEMBRANE-LIKE
  - radial membrane (wall): peak at rho=0.95 (in the peak band 0.5-1.5), rim/core 5.73, rim/outside 4.06 (aggregate of 80 individuals; 74/80 membrane-like individually; rim level 0.507)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): L link, membrane (wall)
- membrane-like channels per top track at mid-life: #48 (t=27250, R_eq 10.05, ring): ['L link', 'membrane (wall)']; #55 (t=28250, R_eq 10.52, ring): ['K2', 'L link', 'membrane (wall)']; #54 (t=27500, R_eq 8.97, ring): ['L link', 'membrane (wall)']; #75 (t=31500, R_eq 11, ring): ['membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 73 of 80 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
