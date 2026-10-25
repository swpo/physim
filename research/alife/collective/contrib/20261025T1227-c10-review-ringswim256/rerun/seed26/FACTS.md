# Evidence pack: ringswim-waste-256 (seed 26)

- world: `../../../20261025T0922-c07-ringswim-256/world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_membrane + phase_swimdiv; mutation: links adsorb to the wall (drift chi up grad of 4 phi(1-phi)); parent: unstructured initial condition: smoothed Gaussian noise phi (mean 0, sd 0.2), uniform random K in [0,0.6] and L in [0,0.1] everywhere
- run: 201 frames x 100 steps x dt 1.0 = time 20000; grid [256, 256]; wall 608s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0922-c07-ringswim-256/world.py --out collective/contrib/20261025T1227-c10-review-ringswim256/rerun/seed26 --seeds 26 --spf 100 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5546], min area 6 px

## Measurements
- components: final 27, mean 36.6, max 88; occupancy final 0.17
- tracks: 1875; persistent (alive >= 50% of run): 0; longest 36 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 25.14, final 16; holes at thresholds 0.2/0.35/0.5 final [4, 20, 23]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [34, 27, 24], H1 [29, 24, 5]
- motion: 25 long-lived tracks moved >= 1 body length; max speed 0.0658/time; max body lengths 6.5
- replication (lineage window K = 20 frames = time 2000, default): splits 611, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 537, merge/split ratio 0.879, nucleations 14
- channel total drift (end/start - 1): [-0.3058, -0.8309, -0.3557, -0.5152]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 804 at frame 82: holes 1, rim-vs-core 0.19, rim-vs-outside 0.79, heterogeneity 0.22; core [0.103, 0.65, 0.542, 0.712] rim [0.214, 0.566, 0.54, 0.582]
  - track 102 at frame 17: holes 1, rim-vs-core 0.33, rim-vs-outside 0.71, heterogeneity 0.23; core [0.149, 0.778, 0.705, 0.612] rim [0.249, 0.533, 0.519, 0.557]
  - track 1565 at frame 168: holes 1, rim-vs-core 0.18, rim-vs-outside 0.84, heterogeneity 0.23; core [0.093, 0.739, 0.563, 0.58] rim [0.202, 0.602, 0.565, 0.576]
  - track 138 at frame 17: holes 1, rim-vs-core 0.15, rim-vs-outside 0.82, heterogeneity 0.18; core [0.104, 0.694, 0.568, 0.629] rim [0.172, 0.564, 0.527, 0.625]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 200 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial S: peak at rho=1.95 (OUTSIDE the peak band 0.5-1.5), rim/core 8.92, rim/outside 0.787 (aggregate of 200 individuals; 0/200 membrane-like individually; rim level 0.528)
  - radial K catalyst: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.01, rim/outside 8.56 (aggregate of 200 individuals; 9/200 membrane-like individually; rim level 0.616)
  - radial L link: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.42, rim/outside 6.2 (aggregate of 200 individuals; 118/200 membrane-like individually; rim level 0.536)
  - radial membrane (wall): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.76, rim/outside 6.81 (aggregate of 200 individuals; 129/200 membrane-like individually; rim level 0.548)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): membrane (wall)
- membrane-like channels per top track at mid-life: #804 (t=8200, R_eq 10.65, ring): ['L link', 'membrane (wall)']; #102 (t=1700, R_eq 9.69, ring): ['L link', 'membrane (wall)']; #1565 (t=16800, R_eq 10.63, ring): ['L link', 'membrane (wall)']; #138 (t=1700, R_eq 10.23, ring): ['L link', 'membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 94 of 200 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
