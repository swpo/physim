# Evidence pack: pcell-mwall-b42-starve (seed 2)

- world: `../../world_starve.py`, family `hybrid-particle-field`
- parent: threads/autopoiesis/worlds/phase_membrane; mutation: catalyst field K -> Brownian catalyst particles with kind/lineage, reflected by a phi^2 acceptance gate
- run: 141 frames x 500 steps x dt 1.0 = time 70000; grid [128, 128]; wall 284s; status ok
- command: `python -m labkit.run collective/contrib/c17-b42-wip/world_starve.py --out collective/contrib/c17-b42-wip/starve/seed2 --seeds 2 --frames 140 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.6247], min area 6 px

## Measurements
- components: final 0, mean 22.4, max 29; occupancy final 0.00
- tracks: 47; persistent (alive >= 50% of run): 25; longest 121 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 36.29 (1 = constant size)
- enclosures: components with a hole mean 3.56, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [0, 0, 0], H1 [0, 0, 0]
- motion: 16 long-lived tracks moved >= 1 body length; max speed 0.00116/time; max body lengths 3.2
- replication (lineage window K = 20 frames = time 10000, default): splits 10, persistent splits 6 (0 more failed only because the siblings re-merged within K), max generation 2, merges 0, merge/split ratio 0, nucleations 1
- channel total drift (end/start - 1): [-0.6335, -1.0, -1.0, -1.0, -1.0, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 3 at frame 60: holes 0, rim-vs-core 0.67, rim-vs-outside 0.85, heterogeneity 0.22; core [0.203, 0.591, 0.82, 0.714, 0.831, 0.598] rim [0.415, 0.108, 0.511, 0.639, 0.582, 0.562]
  - track 4 at frame 60: holes 0, rim-vs-core 0.70, rim-vs-outside 0.96, heterogeneity 0.20; core [0.242, 0.669, 0.931, 0.823, 0.757, 0.803] rim [0.404, 0.18, 0.564, 0.62, 0.694, 0.589]
  - track 5 at frame 60: holes 0, rim-vs-core 0.71, rim-vs-outside 0.76, heterogeneity 0.21; core [0.213, 0.591, 0.824, 0.775, 0.77, 0.7] rim [0.41, 0.126, 0.462, 0.548, 0.579, 0.524]
  - track 41 at frame 108: holes 1, rim-vs-core 0.24, rim-vs-outside 1.06, heterogeneity 0.23; core [0.118, 0.473, 0.64, 0.524, 0.987, 0.369] rim [0.2, 0.352, 0.569, 0.556, 0.842, 0.459]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 133 components >= 12 px at frames [24, 47, 71, 93, 116]):
  - radial S: peak at rho=1.95 (OUTSIDE the peak band 0.5-1.5), rim/core 8.52, rim/outside 0.841 (aggregate of 133 individuals; 0/133 membrane-like individually; rim level 0.577)
  - radial K particles: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.648, rim/outside 32.5 (aggregate of 133 individuals; 0/133 membrane-like individually; rim level 0.513)
  - radial L link: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.51, rim/outside 34.1 (aggregate of 133 individuals; 105/133 membrane-like individually; rim level 0.832)  MEMBRANE-LIKE
  - radial membrane (wall): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 3.2, rim/outside 29.9 (aggregate of 133 individuals; 124/133 membrane-like individually; rim level 0.874)  MEMBRANE-LIKE
  - radial mean yield / 2: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.987, rim/outside 34.6 (aggregate of 133 individuals; 0/133 membrane-like individually; rim level 0.853)
  - radial M wall material: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 3.81, rim/outside 30.8 (aggregate of 133 individuals; 126/133 membrane-like individually; rim level 0.797)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): L link, membrane (wall), M wall material
- membrane-like channels per top track at mid-life: #3 (t=30000, R_eq 5.81): ['L link', 'membrane (wall)', 'M wall material']; #4 (t=30000, R_eq 4.44): ['membrane (wall)', 'M wall material']; #5 (t=30000, R_eq 5.5): ['L link', 'membrane (wall)', 'M wall material']; #41 (t=54000, R_eq 9.51, ring): ['L link', 'membrane (wall)', 'M wall material']

## Warnings
- no components at the end: matter died out or fell below threshold
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 20 of 133 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
