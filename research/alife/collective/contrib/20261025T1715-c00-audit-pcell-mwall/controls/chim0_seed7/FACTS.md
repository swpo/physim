# Evidence pack: pcell-mwall (seed 7)

- world: `../code/world_chim0.py`, family `hybrid-particle-field`
- parent: threads/autopoiesis/worlds/phase_membrane; mutation: catalyst field K -> Brownian catalyst particles with kind/lineage, reflected by a phi^2 acceptance gate
- run: 41 frames x 500 steps x dt 1.0 = time 20000; grid [128, 128]; wall 103s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/audit/pcell-mwall/construction/code/world_chim0.py --out /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/audit/pcell-mwall/construction/chim0_s7 --seeds 7 --frames 40 --spf 500 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.539], min area 6 px

## Measurements
- components: final 23, mean 20.0, max 23; occupancy final 0.31
- tracks: 43; persistent (alive >= 50% of run): 22; longest 41 frames; alive start-to-end: 3
- size of persistent tracks: max/min area ratio 24.83 (1 = constant size)
- enclosures: components with a hole mean 5.71, final 6; holes at thresholds 0.2/0.35/0.5 final [4, 6, 17]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [30, 23, 23], H1 [22, 16, 0]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 0.000963/time; max body lengths 1.2
- replication (lineage window K = 20 frames = time 10000, default): splits 13, persistent splits 6 (0 more failed only because the siblings re-merged within K), max generation 1, merges 3, merge/split ratio 0.231, nucleations 0
- channel total drift (end/start - 1): [-0.4649, -0.6876, 0.0439, -0.0736, -0.6659, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1 at frame 20: holes 1, rim-vs-core 0.30, rim-vs-outside 1.12, heterogeneity 0.20; core [0.093, 0.594, 0.595, 0.407, 0.898, 0.791] rim [0.21, 0.411, 0.617, 0.579, 0.815, 0.719]
  - track 7 at frame 20: holes 0, rim-vs-core 0.64, rim-vs-outside 1.25, heterogeneity 0.20; core [0.091, 0.677, 0.641, 0.446, 0.86, 0.861] rim [0.34, 0.213, 0.649, 0.768, 0.721, 0.751]
  - track 10 at frame 20: holes 0, rim-vs-core 0.71, rim-vs-outside 1.19, heterogeneity 0.21; core [0.108, 0.695, 0.653, 0.441, 0.867, 0.865] rim [0.346, 0.17, 0.646, 0.778, 0.635, 0.76]
  - track 29 at frame 24: holes 0, rim-vs-core 0.50, rim-vs-outside 1.31, heterogeneity 0.19; core [0.104, 0.685, 0.63, 0.486, 0.822, 0.958] rim [0.294, 0.323, 0.669, 0.731, 0.721, 0.86]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 125 components >= 12 px at frames [7, 13, 20, 27, 33, 40]):
  - radial S: peak at rho=1.75 (OUTSIDE the peak band 0.5-1.5), rim/core 12.2, rim/outside 0.86 (aggregate of 125 individuals; 0/125 membrane-like individually; rim level 0.587)
  - radial K particles: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.77, rim/outside 30.9 (aggregate of 125 individuals; 0/125 membrane-like individually; rim level 0.558)
  - radial L link: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.67, rim/outside 24.1 (aggregate of 125 individuals; 110/125 membrane-like individually; rim level 0.802)  MEMBRANE-LIKE
  - radial membrane (wall): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 5.24, rim/outside 19.2 (aggregate of 125 individuals; 121/125 membrane-like individually; rim level 0.795)  MEMBRANE-LIKE
  - radial mean yield / 2: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.978, rim/outside 26.8 (aggregate of 125 individuals; 0/125 membrane-like individually; rim level 0.838)
  - radial M wall material: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.98, rim/outside 17.3 (aggregate of 125 individuals; 0/125 membrane-like individually; rim level 0.856)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): L link, membrane (wall)
- membrane-like channels per top track at mid-life: #1 (t=10000, R_eq 10.2, ring): ['L link', 'membrane (wall)']; #7 (t=10000, R_eq 9.24): ['membrane (wall)']; #10 (t=10000, R_eq 8.23): ['L link', 'membrane (wall)']; #29 (t=12000, R_eq 7.27): ['L link', 'membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 31 of 125 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
