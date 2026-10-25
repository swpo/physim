# Evidence pack: pcell-mwall (seed 41)

- world: `../code/world_gen.py`, family `hybrid-particle-field`
- parent: threads/autopoiesis/worlds/phase_membrane; mutation: catalyst field K -> Brownian catalyst particles with kind/lineage, reflected by a phi^2 acceptance gate
- run: 201 frames x 500 steps x dt 1.0 = time 100000; grid [128, 128]; wall 608s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/audit/pcell-mwall/replication/code/world_gen.py --out /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/audit/pcell-mwall/replication/s41 --seeds 41 --no-movie --frames 200 --spf 500`
- segmentation: matter > 0.35 of robust range [0.0, 1.565], min area 6 px

## Measurements
- components: final 18, mean 20.9, max 25; occupancy final 0.41
- tracks: 67; persistent (alive >= 50% of run): 22; longest 201 frames; alive start-to-end: 1
- size of persistent tracks: max/min area ratio 14.96 (1 = constant size)
- enclosures: components with a hole mean 8.07, final 11; holes at thresholds 0.2/0.35/0.5 final [10, 12, 13]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [32, 18, 18], H1 [18, 13, 7]
- motion: 12 long-lived tracks moved >= 1 body length; max speed 0.000801/time; max body lengths 2.9
- replication (lineage window K = 20 frames = time 10000, default): splits 18, persistent splits 10 (0 more failed only because the siblings re-merged within K), max generation 2, merges 7, merge/split ratio 0.389, nucleations 3
- channel total drift (end/start - 1): [-0.641, -0.5228, 0.567, 0.0492, -0.3716, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 10 at frame 101: holes 0, rim-vs-core 0.85, rim-vs-outside 0.64, heterogeneity 0.23; core [0.235, 0.581, 0.826, 0.781, 0.83, 0.552] rim [0.405, 0.1, 0.434, 0.53, 0.356, 0.405]
  - track 23 at frame 101: holes 0, rim-vs-core 0.61, rim-vs-outside 0.82, heterogeneity 0.20; core [0.236, 0.575, 0.794, 0.751, 0.866, 0.503] rim [0.394, 0.135, 0.497, 0.604, 0.658, 0.473]
  - track 30 at frame 101: holes 0, rim-vs-core 0.64, rim-vs-outside 0.94, heterogeneity 0.20; core [0.257, 0.641, 0.944, 0.812, 0.831, 0.628] rim [0.388, 0.168, 0.601, 0.666, 0.703, 0.51]
  - track 58 at frame 136: holes 1, rim-vs-core 0.29, rim-vs-outside 0.99, heterogeneity 0.24; core [0.166, 0.593, 0.668, 0.508, 0.974, 0.315] rim [0.222, 0.398, 0.6, 0.572, 0.826, 0.433]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 125 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial S: peak at rho=1.65 (OUTSIDE the peak band 0.5-1.5), rim/core 3.93, rim/outside 0.952 (aggregate of 125 individuals; 0/125 membrane-like individually; rim level 0.474)
  - radial K particles: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.693, rim/outside 6.15 (aggregate of 125 individuals; 1/125 membrane-like individually; rim level 0.498)
  - radial L link: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.37, rim/outside 5.24 (aggregate of 125 individuals; 63/125 membrane-like individually; rim level 0.744)
  - radial membrane (wall): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 3.12, rim/outside 4.51 (aggregate of 125 individuals; 106/125 membrane-like individually; rim level 0.714)  MEMBRANE-LIKE
  - radial mean yield / 2: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.973, rim/outside 5.1 (aggregate of 125 individuals; 0/125 membrane-like individually; rim level 0.876)
  - radial M wall material: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 3.16, rim/outside 4.59 (aggregate of 125 individuals; 110/125 membrane-like individually; rim level 0.571)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): membrane (wall), M wall material
- membrane-like channels per top track at mid-life: #10 (t=50500, R_eq 5.41): ['membrane (wall)', 'M wall material']; #23 (t=50500, R_eq 5.7): ['L link', 'membrane (wall)', 'M wall material']; #30 (t=50500, R_eq 4.48): ['membrane (wall)', 'M wall material']; #58 (t=68000, R_eq 10.46, ring): ['L link', 'membrane (wall)', 'M wall material']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 51 of 125 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
