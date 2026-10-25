# Evidence pack: ringswim-waste-256 (seed 11)

- world: `../../../../../../../../../home/user/physim/research/alife/collective/contrib/20261025T0922-c07-ringswim-256/world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_membrane + phase_swimdiv; mutation: links adsorb to the wall (drift chi up grad of 4 phi(1-phi)); parent: unstructured initial condition: smoothed Gaussian noise phi (mean 0, sd 0.2), uniform random K in [0,0.6] and L in [0,0.1] everywhere
- run: 201 frames x 100 steps x dt 1.0 = time 20000; grid [256, 256]; wall 472s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0922-c07-ringswim-256/world.py --out /tmp/claude-0/-home-user-physim/ca3fe853-e88d-58ad-9551-2586c1b06c34/scratchpad/rev/rs256/claim/seed11 --seeds 11 --spf 100 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5571], min area 6 px

## Measurements
- components: final 39, mean 41.7, max 76; occupancy final 0.18
- tracks: 2257; persistent (alive >= 50% of run): 0; longest 29 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 28.14, final 28; holes at thresholds 0.2/0.35/0.5 final [4, 32, 34]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [44, 41, 38], H1 [39, 37, 9]
- motion: 14 long-lived tracks moved >= 1 body length; max speed 0.0466/time; max body lengths 5.3
- replication (lineage window K = 20 frames = time 2000, default): splits 774, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 650, merge/split ratio 0.84, nucleations 7
- channel total drift (end/start - 1): [-0.3258, -0.8222, -0.296, -0.4677]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 966 at frame 89: holes 1, rim-vs-core 0.31, rim-vs-outside 0.71, heterogeneity 0.22; core [0.14, 0.776, 0.691, 0.613] rim [0.233, 0.532, 0.524, 0.579]
  - track 438 at frame 40: holes 1, rim-vs-core 0.17, rim-vs-outside 0.80, heterogeneity 0.19; core [0.103, 0.655, 0.546, 0.72] rim [0.178, 0.553, 0.517, 0.609]
  - track 944 at frame 86: holes 0, rim-vs-core 0.63, rim-vs-outside 0.97, heterogeneity 0.24; core [0.105, 0.867, 0.652, 0.4] rim [0.373, 0.423, 0.594, 0.761]
  - track 1032 at frame 96: holes 1, rim-vs-core 0.19, rim-vs-outside 0.77, heterogeneity 0.24; core [0.094, 0.757, 0.568, 0.558] rim [0.199, 0.596, 0.557, 0.573]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 228 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial S: peak at rho=1.85 (OUTSIDE the peak band 0.5-1.5), rim/core 9.44, rim/outside 0.792 (aggregate of 228 individuals; 0/228 membrane-like individually; rim level 0.524)
  - radial K catalyst: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.06, rim/outside 8.09 (aggregate of 228 individuals; 9/228 membrane-like individually; rim level 0.644)
  - radial L link: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.52, rim/outside 6.13 (aggregate of 228 individuals; 158/228 membrane-like individually; rim level 0.552)  MEMBRANE-LIKE
  - radial membrane (wall): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 2.13, rim/outside 6.75 (aggregate of 228 individuals; 160/228 membrane-like individually; rim level 0.583)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): L link, membrane (wall)
- membrane-like channels per top track at mid-life: #966 (t=8900, R_eq 9.76, ring): ['L link', 'membrane (wall)']; #438 (t=4000, R_eq 10.65, ring): ['L link', 'membrane (wall)']; #944 (t=8600, R_eq 8.02): ['L link', 'membrane (wall)']; #1032 (t=9600, R_eq 12.07): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 128 of 228 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
