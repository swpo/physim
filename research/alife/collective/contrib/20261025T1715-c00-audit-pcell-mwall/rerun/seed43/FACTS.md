# Evidence pack: pcell-mwall (seed 43)

- world: `../code/world_gen.py`, family `hybrid-particle-field`
- parent: threads/autopoiesis/worlds/phase_membrane; mutation: catalyst field K -> Brownian catalyst particles with kind/lineage, reflected by a phi^2 acceptance gate
- run: 201 frames x 500 steps x dt 1.0 = time 100000; grid [128, 128]; wall 594s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/audit/pcell-mwall/replication/code/world_gen.py --out /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/audit/pcell-mwall/replication/s43 --seeds 43 --no-movie --frames 200 --spf 500`
- segmentation: matter > 0.35 of robust range [0.0, 1.5639], min area 6 px

## Measurements
- components: final 22, mean 22.3, max 25; occupancy final 0.40
- tracks: 72; persistent (alive >= 50% of run): 22; longest 201 frames; alive start-to-end: 1
- size of persistent tracks: max/min area ratio 15.18 (1 = constant size)
- enclosures: components with a hole mean 9.16, final 13; holes at thresholds 0.2/0.35/0.5 final [12, 13, 14]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [27, 22, 22], H1 [18, 13, 0]
- motion: 9 long-lived tracks moved >= 1 body length; max speed 0.000394/time; max body lengths 3.1
- replication (lineage window K = 20 frames = time 10000, default): splits 22, persistent splits 11 (0 more failed only because the siblings re-merged within K), max generation 3, merges 4, merge/split ratio 0.182, nucleations 5
- channel total drift (end/start - 1): [-0.6386, -0.5332, 0.5636, 0.2215, -0.3799, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 12 at frame 101: holes 0, rim-vs-core 0.60, rim-vs-outside 0.87, heterogeneity 0.21; core [0.227, 0.545, 0.824, 0.748, 0.88, 0.533] rim [0.391, 0.147, 0.497, 0.619, 0.662, 0.476]
  - track 31 at frame 101: holes 0, rim-vs-core 0.72, rim-vs-outside 1.26, heterogeneity 0.23; core [0.139, 0.763, 0.757, 0.549, 0.885, 0.36] rim [0.346, 0.2, 0.676, 0.778, 0.743, 0.649]
  - track 32 at frame 101: holes 0, rim-vs-core 0.41, rim-vs-outside 0.98, heterogeneity 0.21; core [0.249, 0.509, 0.836, 0.834, 0.876, 0.554] rim [0.312, 0.367, 0.604, 0.617, 0.689, 0.477]
  - track 61 at frame 148: holes 0, rim-vs-core 0.79, rim-vs-outside 0.77, heterogeneity 0.23; core [0.221, 0.578, 0.888, 0.811, 0.887, 0.613] rim [0.378, 0.122, 0.466, 0.534, 0.546, 0.447]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 136 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial S: peak at rho=1.65 (OUTSIDE the peak band 0.5-1.5), rim/core 5.62, rim/outside 0.956 (aggregate of 136 individuals; 0/136 membrane-like individually; rim level 0.483)
  - radial K particles: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.739, rim/outside 6.88 (aggregate of 136 individuals; 0/136 membrane-like individually; rim level 0.524)
  - radial L link: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.45, rim/outside 5.28 (aggregate of 136 individuals; 82/136 membrane-like individually; rim level 0.748)
  - radial membrane (wall): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 3.93, rim/outside 4.4 (aggregate of 136 individuals; 126/136 membrane-like individually; rim level 0.711)  MEMBRANE-LIKE
  - radial mean yield / 2: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.989, rim/outside 5.47 (aggregate of 136 individuals; 0/136 membrane-like individually; rim level 0.894)
  - radial M wall material: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 3.5, rim/outside 4.55 (aggregate of 136 individuals; 128/136 membrane-like individually; rim level 0.581)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): membrane (wall), M wall material
- membrane-like channels per top track at mid-life: #12 (t=50500, R_eq 5.41): ['L link', 'membrane (wall)', 'M wall material']; #31 (t=50500, R_eq 6.23): ['L link', 'membrane (wall)', 'M wall material']; #32 (t=50500, R_eq 5.41): ['membrane (wall)', 'M wall material']; #61 (t=74000, R_eq 4.92): ['membrane (wall)', 'M wall material']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 57 of 136 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
