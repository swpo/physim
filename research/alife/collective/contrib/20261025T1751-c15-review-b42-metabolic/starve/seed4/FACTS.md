# Evidence pack: pcell-mwall-b42-starve (seed 4)

- world: `../../world_starve.py`, family `hybrid-particle-field`
- parent: threads/autopoiesis/worlds/phase_membrane; mutation: catalyst field K -> Brownian catalyst particles with kind/lineage, reflected by a phi^2 acceptance gate
- run: 201 frames x 500 steps x dt 1.0 = time 100000; grid [128, 128]; wall 717s; status ok
- command: `python -m labkit.run /root/rev7/world_starve.py --out /root/rev7/starve/seed4 --seeds 4 --frames 200 --spf 500 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5602], min area 6 px

## Measurements
- components: final 0, mean 12.0, max 29; occupancy final 0.00
- tracks: 51; persistent (alive >= 50% of run): 11; longest 121 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 16.66 (1 = constant size)
- enclosures: components with a hole mean 2.47, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [0, 0, 0], H1 [0, 0, 0]
- motion: 9 long-lived tracks moved >= 1 body length; max speed 0.000554/time; max body lengths 3.0
- replication (lineage window K = 20 frames = time 10000, default): splits 16, persistent splits 8 (0 more failed only because the siblings re-merged within K), max generation 3, merges 0, merge/split ratio 0, nucleations 0
- channel total drift (end/start - 1): [-0.6705, -1.0, -1.0, -1.0, -1.0, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1 at frame 61: holes 0, rim-vs-core 0.58, rim-vs-outside 1.31, heterogeneity 0.23; core [0.08, 0.719, 0.636, 0.439, 0.889, 0.323] rim [0.271, 0.353, 0.662, 0.701, 0.794, 0.622]
  - track 3 at frame 61: holes 0, rim-vs-core 0.59, rim-vs-outside 1.27, heterogeneity 0.22; core [0.117, 0.657, 0.703, 0.559, 0.853, 0.433] rim [0.363, 0.25, 0.658, 0.743, 0.768, 0.715]
  - track 5 at frame 61: holes 0, rim-vs-core 0.73, rim-vs-outside 1.35, heterogeneity 0.23; core [0.108, 0.75, 0.693, 0.483, 0.834, 0.392] rim [0.369, 0.235, 0.669, 0.782, 0.768, 0.722]
  - track 39 at frame 103: holes 1, rim-vs-core 0.41, rim-vs-outside 1.07, heterogeneity 0.24; core [0.119, 0.592, 0.685, 0.531, 0.974, 0.39] rim [0.252, 0.303, 0.572, 0.583, 0.803, 0.53]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 59 components >= 12 px at frames [34, 67, 101]):
  - radial S: peak at rho=1.85 (OUTSIDE the peak band 0.5-1.5), rim/core 11.1, rim/outside 0.838 (aggregate of 59 individuals; 0/59 membrane-like individually; rim level 0.58)
  - radial K particles: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.702, rim/outside 22.2 (aggregate of 59 individuals; 0/59 membrane-like individually; rim level 0.549)
  - radial L link: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.48, rim/outside 19.9 (aggregate of 59 individuals; 38/59 membrane-like individually; rim level 0.792)
  - radial membrane (wall): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 3.32, rim/outside 17.9 (aggregate of 59 individuals; 54/59 membrane-like individually; rim level 0.794)  MEMBRANE-LIKE
  - radial mean yield / 2: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.95, rim/outside 20.3 (aggregate of 59 individuals; 0/59 membrane-like individually; rim level 0.845)
  - radial M wall material: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 3.86, rim/outside 18.5 (aggregate of 59 individuals; 54/59 membrane-like individually; rim level 0.726)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): membrane (wall), M wall material
- membrane-like channels per top track at mid-life: #1 (t=30500, R_eq 8.18): ['L link', 'membrane (wall)', 'M wall material']; #3 (t=30500, R_eq 7.18): ['L link', 'membrane (wall)', 'M wall material']; #5 (t=30500, R_eq 7.42): ['L link', 'membrane (wall)', 'M wall material']; #39 (t=51500, R_eq 9.29, ring): ['L link', 'membrane (wall)', 'M wall material']

## Warnings
- no components at the end: matter died out or fell below threshold
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 11 of 59 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
