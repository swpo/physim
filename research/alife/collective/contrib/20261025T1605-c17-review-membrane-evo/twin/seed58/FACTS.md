# Evidence pack: membrane-evo (seed 58)

- world: `../../world_twin.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/membrane_kinds (arm E of committee r2); identical-event design from fisim-beyond-laplacian xcell-evo2-S; mutation: kinds differ only in link yield b2; sealed catalyst channel (min face gate, fast outside decay); whole-cell flips + neutral tag + random disk deaths from a state-independent RNG
- run: 161 frames x 250 steps x dt 1.0 = time 40000; grid [128, 128]; wall 92s; status ok
- command: `python -m labkit.run collective/contrib/c17-mevo-wip/world_twin.py --out collective/contrib/c17-mevo-wip/twin/seed58 --seeds 58 --frames 160 --spf 250 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.7274], min area 6 px

## Measurements
- components: final 11, mean 11.3, max 18; occupancy final 0.23
- tracks: 96; persistent (alive >= 50% of run): 1; longest 84 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.94 (1 = constant size)
- enclosures: components with a hole mean 10.55, final 10; holes at thresholds 0.2/0.35/0.5 final [6, 10, 10]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [12, 11, 11], H1 [11, 10, 7]
- motion: 5 long-lived tracks moved >= 1 body length; max speed 0.00308/time; max body lengths 1.6
- replication (lineage window K = 20 frames = time 5000, default): splits 38, persistent splits 9 (0 more failed only because the siblings re-merged within K), max generation 3, merges 3, merge/split ratio 0.079, nucleations 0
- channel total drift (end/start - 1): [-0.7147, None, 0.0035, -0.3568]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 52 at frame 118: holes 1, rim-vs-core 0.41, rim-vs-outside 0.70, heterogeneity 0.22; core [0.853, 0.0, 0.742, 0.522] rim [0.485, 0.0, 0.584, 0.6]
  - track 39 at frame 93: holes 1, rim-vs-core 0.35, rim-vs-outside 0.71, heterogeneity 0.20; core [0.824, 0.0, 0.649, 0.529] rim [0.502, 0.0, 0.569, 0.644]
  - track 66 at frame 130: holes 1, rim-vs-core 0.41, rim-vs-outside 0.66, heterogeneity 0.21; core [0.825, 0.0, 0.696, 0.587] rim [0.445, 0.0, 0.545, 0.609]
  - track 72 at frame 140: holes 1, rim-vs-core 0.36, rim-vs-outside 0.68, heterogeneity 0.20; core [0.813, 0.0, 0.683, 0.57] rim [0.478, 0.0, 0.554, 0.62]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 71 components >= 12 px at frames [27, 54, 81, 106, 133, 160]):
  - radial K1: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.15, rim/outside 8.72 (aggregate of 71 individuals; 17/71 membrane-like individually; rim level 0.561)
  - radial K2: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.19, rim/outside 3.68 (aggregate of 71 individuals; 1/71 membrane-like individually; rim level 0.0446)
  - radial L link: peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.41, rim/outside 5.66 (aggregate of 71 individuals; 49/71 membrane-like individually; rim level 0.48)
  - radial membrane (wall): peak at rho=0.95 (in the peak band 0.5-1.5), rim/core 5.11, rim/outside 4 (aggregate of 71 individuals; 62/71 membrane-like individually; rim level 0.472)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): membrane (wall)
- membrane-like channels per top track at mid-life: #52 (t=29500, R_eq 8.57, ring): ['L link', 'membrane (wall)']; #39 (t=23250, R_eq 9.25, ring): ['K1', 'L link', 'membrane (wall)']; #66 (t=32500, R_eq 8.74, ring): ['K1', 'L link', 'membrane (wall)']; #72 (t=35000, R_eq 9.97, ring): ['K1', 'L link', 'membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 64 of 71 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
