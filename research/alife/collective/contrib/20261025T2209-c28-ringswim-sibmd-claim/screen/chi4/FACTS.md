# Evidence pack: ringswim-waste-256 (seed 0)

- world: `../../../../home/user/physim/research/alife/collective/contrib/20261025T0922-c07-ringswim-256/world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_membrane + phase_swimdiv; mutation: links adsorb to the wall (drift chi up grad of 4 phi(1-phi)); parent: unstructured initial condition: smoothed Gaussian noise phi (mean 0, sd 0.2), uniform random K in [0,0.6] and L in [0,0.1] everywhere
- run: 201 frames x 60 steps x dt 1.0 = time 12000; grid [128, 128]; wall 69s; status ok
- command: `python -m labkit.run /home/user/physim/research/alife/collective/contrib/20261025T0922-c07-ringswim-256/world.py --out /tmp/claude-0/c28sd/chi4 --seeds 0 --size 128 128 --spf 60 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5456], min area 6 px

## Measurements
- components: final 3, mean 4.6, max 25; occupancy final 0.13
- tracks: 231; persistent (alive >= 50% of run): 0; longest 33 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 3.14, final 3; holes at thresholds 0.2/0.35/0.5 final [2, 3, 3]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [4, 3, 3], H1 [3, 3, 2]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 0.0239/time; max body lengths 1.8
- replication (lineage window K = 20 frames = time 1200, default): splits 67, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 65, merge/split ratio 0.97, nucleations 0
- channel total drift (end/start - 1): [-0.2789, -0.8467, -0.4605, -0.6528]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 54 at frame 25: holes 1, rim-vs-core 0.18, rim-vs-outside 0.77, heterogeneity 0.22; core [0.136, 0.755, 0.56, 0.58] rim [0.206, 0.596, 0.503, 0.578]
  - track 61 at frame 24: holes 1, rim-vs-core 0.22, rim-vs-outside 0.79, heterogeneity 0.23; core [0.137, 0.805, 0.55, 0.512] rim [0.212, 0.609, 0.519, 0.575]
  - track 67 at frame 32: holes 1, rim-vs-core 0.16, rim-vs-outside 0.75, heterogeneity 0.22; core [0.107, 0.702, 0.476, 0.583] rim [0.198, 0.577, 0.492, 0.585]
  - track 168 at frame 131: holes 1, rim-vs-core 0.16, rim-vs-outside 0.76, heterogeneity 0.23; core [0.111, 0.69, 0.495, 0.642] rim [0.211, 0.585, 0.493, 0.576]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 24 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial S: peak at rho=2.15 (OUTSIDE the peak band 0.5-1.5), rim/core 5.21, rim/outside 0.679 (aggregate of 24 individuals; 0/24 membrane-like individually; rim level 0.443)
  - radial K catalyst: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.997, rim/outside 4.67 (aggregate of 24 individuals; 7/24 membrane-like individually; rim level 0.504)
  - radial L link: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.23, rim/outside 3.36 (aggregate of 24 individuals; 14/24 membrane-like individually; rim level 0.343)
  - radial membrane (wall): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.33, rim/outside 3.32 (aggregate of 24 individuals; 13/24 membrane-like individually; rim level 0.357)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #54 (t=1500, R_eq 12.11, ring): ['K catalyst', 'L link', 'membrane (wall)']; #61 (t=1440, R_eq 11.7, ring): ['K catalyst', 'L link', 'membrane (wall)']; #67 (t=1920, R_eq 12.57, ring): ['K catalyst', 'L link', 'membrane (wall)']; #168 (t=7860, R_eq 11.34, ring): ['K catalyst', 'L link', 'membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 14 of 24 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
