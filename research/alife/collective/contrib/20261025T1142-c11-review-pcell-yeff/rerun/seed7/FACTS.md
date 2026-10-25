# Evidence pack: pcell-yeff (seed 7)

- world: `../../../../home/user/physim/research/alife/collective/contrib/20261025T1037-c06-pcell-yeff-response/world.py`, family `hybrid-particle-field`
- parent: threads/autopoiesis/worlds/phase_membrane; mutation: catalyst field K -> Brownian catalyst particles with kind/lineage, reflected by a phi^2 acceptance gate
- run: 121 frames x 50 steps x dt 1.0 = time 6000; grid [128, 128]; wall 26s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1037-c06-pcell-yeff-response/world.py --out /tmp/claude-0/c11rev18/rerun --seeds 7 --frames 120 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.53], min area 6 px

## Measurements
- components: final 20, mean 16.3, max 35; occupancy final 0.36
- tracks: 90; persistent (alive >= 50% of run): 16; longest 111 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 7.62 (1 = constant size)
- enclosures: components with a hole mean 10.17, final 14; holes at thresholds 0.2/0.35/0.5 final [0, 15, 20]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [28, 20, 20], H1 [20, 20, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.6
- replication (lineage window K = 20 frames = time 1000, default): splits 27, persistent splits 2 (0 more failed only because the siblings re-merged within K), max generation 1, merges 3, merge/split ratio 0.111, nucleations 3
- channel total drift (end/start - 1): [-0.4838, -0.6624, 0.0899, -0.0007]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 49 at frame 66: holes 0, rim-vs-core 0.65, rim-vs-outside 0.85, heterogeneity 0.23; core [0.11, 0.673, 0.568, 0.404] rim [0.353, 0.2, 0.567, 0.767]
  - track 51 at frame 66: holes 0, rim-vs-core 0.63, rim-vs-outside 0.80, heterogeneity 0.22; core [0.127, 0.647, 0.579, 0.453] rim [0.359, 0.152, 0.538, 0.76]
  - track 62 at frame 68: holes 1, rim-vs-core 0.30, rim-vs-outside 0.79, heterogeneity 0.21; core [0.106, 0.677, 0.542, 0.425] rim [0.207, 0.433, 0.544, 0.577]
  - track 84 at frame 95: holes 0, rim-vs-core 0.69, rim-vs-outside 0.83, heterogeneity 0.23; core [0.096, 0.703, 0.566, 0.372] rim [0.359, 0.197, 0.552, 0.751]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 107 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial S: peak at rho=1.65 (OUTSIDE the peak band 0.5-1.5), rim/core 9.64, rim/outside 0.893 (aggregate of 107 individuals; 0/107 membrane-like individually; rim level 0.58)
  - radial K particles: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.826, rim/outside 17.4 (aggregate of 107 individuals; 0/107 membrane-like individually; rim level 0.547)
  - radial L link: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.5, rim/outside 10.6 (aggregate of 107 individuals; 73/107 membrane-like individually; rim level 0.616)
  - radial membrane (wall): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 5.37, rim/outside 8.6 (aggregate of 107 individuals; 101/107 membrane-like individually; rim level 0.669)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): membrane (wall)
- membrane-like channels per top track at mid-life: #49 (t=3300, R_eq 8.88): ['L link', 'membrane (wall)']; #51 (t=3300, R_eq 8.23): ['L link', 'membrane (wall)']; #62 (t=3400, R_eq 10.46, ring): ['membrane (wall)']; #84 (t=4750, R_eq 9.87): ['L link', 'membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 56 of 107 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
