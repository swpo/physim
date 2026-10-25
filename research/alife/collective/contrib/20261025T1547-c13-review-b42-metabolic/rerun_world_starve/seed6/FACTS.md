# Evidence pack: pcell-mwall-b42-starve (seed 6)

- world: `../../world_starve.py`, family `hybrid-particle-field`
- parent: threads/autopoiesis/worlds/phase_membrane; mutation: catalyst field K -> Brownian catalyst particles with kind/lineage, reflected by a phi^2 acceptance gate
- run: 201 frames x 500 steps x dt 1.0 = time 100000; grid [128, 128]; wall 408s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1547-c13-review-b42-metabolic/world_starve.py --out collective/contrib/20261025T1547-c13-review-b42-metabolic/rerun_world_starve/seed6 --seeds 6 --spf 500 --frames 200 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.607], min area 6 px

## Measurements
- components: final 0, mean 15.1, max 29; occupancy final 0.00
- tracks: 49; persistent (alive >= 50% of run): 19; longest 121 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 14.33 (1 = constant size)
- enclosures: components with a hole mean 1.47, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [0, 0, 0], H1 [0, 0, 0]
- motion: 14 long-lived tracks moved >= 1 body length; max speed 0.000527/time; max body lengths 2.5
- replication (lineage window K = 20 frames = time 10000, default): splits 12, persistent splits 4 (0 more failed only because the siblings re-merged within K), max generation 1, merges 0, merge/split ratio 0, nucleations 2
- channel total drift (end/start - 1): [-0.6351, -1.0, -1.0, -1.0, -1.0, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1 at frame 61: holes 0, rim-vs-core 0.67, rim-vs-outside 1.29, heterogeneity 0.22; core [0.134, 0.719, 0.743, 0.541, 0.834, 0.422] rim [0.355, 0.223, 0.682, 0.785, 0.74, 0.701]
  - track 7 at frame 61: holes 0, rim-vs-core 0.77, rim-vs-outside 1.30, heterogeneity 0.24; core [0.087, 0.715, 0.654, 0.457, 0.868, 0.328] rim [0.35, 0.202, 0.644, 0.783, 0.742, 0.71]
  - track 9 at frame 61: holes 0, rim-vs-core 0.69, rim-vs-outside 1.27, heterogeneity 0.23; core [0.106, 0.715, 0.693, 0.559, 0.833, 0.416] rim [0.361, 0.226, 0.654, 0.77, 0.709, 0.741]
  - track 33 at frame 108: holes 1, rim-vs-core 0.35, rim-vs-outside 1.12, heterogeneity 0.23; core [0.085, 0.565, 0.598, 0.431, 0.987, 0.269] rim [0.183, 0.378, 0.599, 0.576, 0.89, 0.483]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 76 components >= 12 px at frames [34, 67, 101]):
  - radial S: peak at rho=1.95 (OUTSIDE the peak band 0.5-1.5), rim/core 10.9, rim/outside 0.824 (aggregate of 76 individuals; 0/76 membrane-like individually; rim level 0.589)
  - radial K particles: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.647, rim/outside 36.1 (aggregate of 76 individuals; 0/76 membrane-like individually; rim level 0.547)
  - radial L link: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.58, rim/outside 43.1 (aggregate of 76 individuals; 57/76 membrane-like individually; rim level 0.881)  MEMBRANE-LIKE
  - radial membrane (wall): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 3.5, rim/outside 39.9 (aggregate of 76 individuals; 72/76 membrane-like individually; rim level 0.912)  MEMBRANE-LIKE
  - radial mean yield / 2: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.987, rim/outside 39.5 (aggregate of 76 individuals; 0/76 membrane-like individually; rim level 0.834)
  - radial M wall material: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 4.17, rim/outside 41.7 (aggregate of 76 individuals; 71/76 membrane-like individually; rim level 0.857)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): L link, membrane (wall), M wall material
- membrane-like channels per top track at mid-life: #1 (t=30500, R_eq 6.46): ['L link', 'membrane (wall)', 'M wall material']; #7 (t=30500, R_eq 7.8): ['L link', 'membrane (wall)', 'M wall material']; #9 (t=30500, R_eq 6.6): ['L link', 'membrane (wall)', 'M wall material']; #33 (t=54000, R_eq 10.33, ring): ['L link', 'membrane (wall)', 'M wall material']

## Warnings
- no components at the end: matter died out or fell below threshold
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 5 of 76 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
