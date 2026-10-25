# Evidence pack: pcell-mwall (seed 41)

- world: `../code/world_gen.py`, family `hybrid-particle-field`
- parent: threads/autopoiesis/worlds/phase_membrane; mutation: catalyst field K -> Brownian catalyst particles with kind/lineage, reflected by a phi^2 acceptance gate
- run: 121 frames x 500 steps x dt 1.0 = time 60000; grid [192, 192]; wall 835s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/audit/pcell-mwall/replication/code/world_gen.py --out /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/audit/pcell-mwall/replication/v41_res1p5 --seeds 41 --no-movie --frames 120 --spf 500 --size 192 192`
- segmentation: matter > 0.35 of robust range [0.0, 1.5304], min area 6 px

## Measurements
- components: final 18, mean 19.5, max 23; occupancy final 0.36
- tracks: 69; persistent (alive >= 50% of run): 21; longest 119 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 22.20 (1 = constant size)
- enclosures: components with a hole mean 8.45, final 6; holes at thresholds 0.2/0.35/0.5 final [23, 6, 10]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [21, 17, 17], H1 [15, 12, 5]
- motion: 4 long-lived tracks moved >= 1 body length; max speed 0.00152/time; max body lengths 2.0
- replication (lineage window K = 20 frames = time 10000, default): splits 20, persistent splits 8 (0 more failed only because the siblings re-merged within K), max generation 2, merges 7, merge/split ratio 0.35, nucleations 4
- channel total drift (end/start - 1): [-0.6538, -0.4923, 0.5168, 0.0854, -0.3611, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 31 at frame 62: holes 0, rim-vs-core 0.36, rim-vs-outside 1.12, heterogeneity 0.21; core [0.197, 0.673, 0.742, 0.725, 0.798, 0.479] rim [0.315, 0.381, 0.593, 0.664, 0.735, 0.438]
  - track 36 at frame 61: holes 0, rim-vs-core 0.69, rim-vs-outside 1.03, heterogeneity 0.22; core [0.206, 0.742, 0.867, 0.77, 0.815, 0.541] rim [0.384, 0.179, 0.569, 0.684, 0.668, 0.481]
  - track 42 at frame 64: holes 0, rim-vs-core 0.69, rim-vs-outside 1.28, heterogeneity 0.23; core [0.154, 0.773, 0.687, 0.537, 0.864, 0.314] rim [0.356, 0.229, 0.656, 0.784, 0.762, 0.584]
  - track 60 at frame 83: holes 1, rim-vs-core 0.27, rim-vs-outside 0.91, heterogeneity 0.23; core [0.131, 0.573, 0.595, 0.514, 0.994, 0.27] rim [0.198, 0.411, 0.574, 0.573, 0.882, 0.427]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 117 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial S: peak at rho=1.65 (OUTSIDE the peak band 0.5-1.5), rim/core 5.04, rim/outside 0.921 (aggregate of 117 individuals; 0/117 membrane-like individually; rim level 0.489)
  - radial K particles: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.72, rim/outside 8.01 (aggregate of 117 individuals; 0/117 membrane-like individually; rim level 0.563)
  - radial L link: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.49, rim/outside 6.47 (aggregate of 117 individuals; 80/117 membrane-like individually; rim level 0.744)
  - radial membrane (wall): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 3.42, rim/outside 5.17 (aggregate of 117 individuals; 105/117 membrane-like individually; rim level 0.704)  MEMBRANE-LIKE
  - radial mean yield / 2: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.974, rim/outside 6.43 (aggregate of 117 individuals; 0/117 membrane-like individually; rim level 0.855)
  - radial M wall material: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 3.97, rim/outside 5.86 (aggregate of 117 individuals; 110/117 membrane-like individually; rim level 0.543)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): membrane (wall), M wall material
- membrane-like channels per top track at mid-life: #31 (t=31000, R_eq 9.61): ['L link', 'membrane (wall)', 'M wall material']; #36 (t=30500, R_eq 7.76): ['L link', 'membrane (wall)', 'M wall material']; #42 (t=32000, R_eq 10.14): ['L link', 'membrane (wall)', 'M wall material']; #60 (t=41500, R_eq 21.53, ring): ['membrane (wall)', 'M wall material']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 42 of 117 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
