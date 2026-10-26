# Evidence pack: membrane-kinds (seed 4)

- world: `../../world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_membrane + phase_kinds; mutation: two heritable catalyst kinds with K1->K2 point mutation; catalyst mobility phi^kexp and optional autocatalysis mask (vertical vs horizontal transmission test)
- run: 201 frames x 50 steps x dt 1.0 = time 10000; grid [128, 128]; wall 16s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0318-c32-review-membrane-kinds/world.py --out collective/contrib/20261026T0318-c32-review-membrane-kinds/pack --seeds 3 4 --frames 200 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5419], min area 6 px

## Measurements
- components: final 19, mean 15.4, max 22; occupancy final 0.34
- tracks: 160; persistent (alive >= 50% of run): 1; longest 105 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 5.58 (1 = constant size)
- enclosures: components with a hole mean 10.03, final 8; holes at thresholds 0.2/0.35/0.5 final [0, 8, 16]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [21, 20, 20], H1 [23, 17, 7]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 0.00633/time; max body lengths 1.0
- replication (lineage window K = 20 frames = time 1000, default): splits 64, persistent splits 15 (0 more failed only because the siblings re-merged within K), max generation 3, merges 7, merge/split ratio 0.109, nucleations 0
- channel total drift (end/start - 1): [-0.5141, -0.6824, None, 0.11, -0.1304]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 100 at frame 148: holes 0, rim-vs-core 0.35, rim-vs-outside 0.79, heterogeneity 0.15; core [0.094, 0.725, 0.0, 0.519, 0.665] rim [0.286, 0.439, 0.0, 0.585, 0.643]
  - track 82 at frame 97: holes 1, rim-vs-core 0.31, rim-vs-outside 0.77, heterogeneity 0.18; core [0.126, 0.829, 0.0, 0.695, 0.627] rim [0.214, 0.591, 0.0, 0.532, 0.559]
  - track 76 at frame 92: holes 1, rim-vs-core 0.20, rim-vs-outside 0.81, heterogeneity 0.16; core [0.106, 0.809, 0.0, 0.626, 0.6] rim [0.167, 0.63, 0.0, 0.552, 0.597]
  - track 153 at frame 190: holes 1, rim-vs-core 0.18, rim-vs-outside 0.84, heterogeneity 0.16; core [0.087, 0.768, 0.0, 0.552, 0.615] rim [0.164, 0.602, 0.0, 0.541, 0.611]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 99 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial S: peak at rho=1.65 (OUTSIDE the peak band 0.5-1.5), rim/core 10.4, rim/outside 0.855 (aggregate of 99 individuals; 0/99 membrane-like individually; rim level 0.467)
  - radial K1: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.01, rim/outside 5.22 (aggregate of 99 individuals; 0/99 membrane-like individually; rim level 0.713)
  - radial K2: flat profile (no radial structure; level 0; aggregate of 99 individuals)
  - radial L link: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.59, rim/outside 4.11 (aggregate of 99 individuals; 77/99 membrane-like individually; rim level 0.593)  MEMBRANE-LIKE
  - radial membrane (wall): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 2.19, rim/outside 4.05 (aggregate of 99 individuals; 77/99 membrane-like individually; rim level 0.615)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): L link, membrane (wall)
- membrane-like channels per top track at mid-life: #100 (t=7400, R_eq 9.25): ['L link', 'membrane (wall)']; #82 (t=4850, R_eq 9.62, ring): ['L link', 'membrane (wall)']; #76 (t=4600, R_eq 11.98, ring): ['L link', 'membrane (wall)']; #153 (t=9500, R_eq 10.46, ring): ['L link', 'membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 56 of 99 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
