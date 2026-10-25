# Evidence pack: pcell-mwall-b42-starve (seed 0)

- world: `../../world_m42_starve.py`, family `hybrid-particle-field`
- parent: threads/autopoiesis/worlds/phase_membrane; mutation: catalyst field K -> Brownian catalyst particles with kind/lineage, reflected by a phi^2 acceptance gate
- run: 201 frames x 500 steps x dt 1.0 = time 100000; grid [128, 128]; wall 718s; status ok
- command: `python -m labkit.run scratch/c14/world_m42_starve.py --out scratch/c14/m42starve/seed0 --seeds 0 --frames 200 --spf 500 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5836], min area 6 px

## Measurements
- components: final 0, mean 13.2, max 27; occupancy final 0.00
- tracks: 55; persistent (alive >= 50% of run): 12; longest 121 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 21.11 (1 = constant size)
- enclosures: components with a hole mean 2.21, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [0, 0, 0], H1 [0, 0, 0]
- motion: 12 long-lived tracks moved >= 1 body length; max speed 0.000594/time; max body lengths 3.3
- replication (lineage window K = 20 frames = time 10000, default): splits 13, persistent splits 9 (0 more failed only because the siblings re-merged within K), max generation 3, merges 1, merge/split ratio 0.077, nucleations 0
- channel total drift (end/start - 1): [-0.6329, -1.0, -1.0, -1.0, -1.0, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 11 at frame 61: holes 0, rim-vs-core 0.62, rim-vs-outside 0.90, heterogeneity 0.21; core [0.19, 0.64, 0.806, 0.733, 0.792, 0.638] rim [0.412, 0.154, 0.529, 0.62, 0.687, 0.588]
  - track 14 at frame 61: holes 0, rim-vs-core 0.74, rim-vs-outside 1.37, heterogeneity 0.23; core [0.114, 0.779, 0.736, 0.496, 0.833, 0.423] rim [0.371, 0.242, 0.695, 0.792, 0.757, 0.737]
  - track 16 at frame 61: holes 0, rim-vs-core 0.69, rim-vs-outside 1.29, heterogeneity 0.23; core [0.085, 0.771, 0.729, 0.547, 0.844, 0.428] rim [0.353, 0.242, 0.652, 0.747, 0.772, 0.691]
  - track 47 at frame 108: holes 1, rim-vs-core 0.46, rim-vs-outside 1.10, heterogeneity 0.24; core [0.096, 0.563, 0.643, 0.476, 0.957, 0.358] rim [0.263, 0.272, 0.581, 0.619, 0.775, 0.568]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 66 components >= 12 px at frames [34, 67, 101]):
  - radial S: peak at rho=1.95 (OUTSIDE the peak band 0.5-1.5), rim/core 11.2, rim/outside 0.827 (aggregate of 66 individuals; 0/66 membrane-like individually; rim level 0.589)
  - radial K particles: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.668, rim/outside 31.4 (aggregate of 66 individuals; 0/66 membrane-like individually; rim level 0.548)
  - radial L link: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.53, rim/outside 31.3 (aggregate of 66 individuals; 48/66 membrane-like individually; rim level 0.838)  MEMBRANE-LIKE
  - radial membrane (wall): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 3.44, rim/outside 27.9 (aggregate of 66 individuals; 63/66 membrane-like individually; rim level 0.855)  MEMBRANE-LIKE
  - radial mean yield / 2: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.974, rim/outside 30.7 (aggregate of 66 individuals; 0/66 membrane-like individually; rim level 0.841)
  - radial M wall material: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 4, rim/outside 29 (aggregate of 66 individuals; 63/66 membrane-like individually; rim level 0.798)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): L link, membrane (wall), M wall material
- membrane-like channels per top track at mid-life: #11 (t=30500, R_eq 5.89): ['L link', 'membrane (wall)', 'M wall material']; #14 (t=30500, R_eq 6.63): ['L link', 'membrane (wall)', 'M wall material']; #16 (t=30500, R_eq 6.82): ['L link', 'membrane (wall)', 'M wall material']; #47 (t=54000, R_eq 9.61, ring): ['L link', 'membrane (wall)', 'M wall material']

## Warnings
- no components at the end: matter died out or fell below threshold
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 6 of 66 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
