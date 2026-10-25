# Evidence pack: ringswim-dl2 (seed 3)

- world: `../../../20261025T2209-c28-ringswim-sibmd-claim/world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_membrane + phase_swimdiv; mutation: links adsorb to the wall (drift chi up grad of 4 phi(1-phi)); parent: unstructured initial condition: smoothed Gaussian noise phi (mean 0, sd 0.2), uniform random K in [0,0.6] and L in [0,0.1] everywhere
- run: 201 frames x 50 steps x dt 1.0 = time 10000; grid [256, 256]; wall 207s; status ok
- command: `python -m labkit.run collective/contrib/20261025T2209-c28-ringswim-sibmd-claim/world.py --out collective/contrib/20261025T2235-c23-review-ringswim/pack --seeds 3 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5397], min area 6 px

## Measurements
- components: final 33, mean 36.0, max 99; occupancy final 0.21
- tracks: 1052; persistent (alive >= 50% of run): 0; longest 62 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 25.57, final 26; holes at thresholds 0.2/0.35/0.5 final [11, 29, 34]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [38, 36, 33], H1 [38, 37, 26]
- motion: 72 long-lived tracks moved >= 1 body length; max speed 0.0588/time; max body lengths 4.5
- replication (lineage window K = 20 frames = time 1000, default): splits 336, persistent splits 2 (0 more failed only because the siblings re-merged within K), max generation 2, merges 260, merge/split ratio 0.774, nucleations 1
- channel total drift (end/start - 1): [-0.356, -0.7932, -0.2437, -0.4385]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 762 at frame 163: holes 1, rim-vs-core 0.20, rim-vs-outside 0.82, heterogeneity 0.22; core [0.126, 0.736, 0.625, 0.651] rim [0.215, 0.585, 0.563, 0.587]
  - track 171 at frame 32: holes 0, rim-vs-core 0.35, rim-vs-outside 0.98, heterogeneity 0.16; core [0.062, 0.634, 0.412, 0.59] rim [0.248, 0.476, 0.602, 0.753]
  - track 400 at frame 72: holes 1, rim-vs-core 0.20, rim-vs-outside 0.76, heterogeneity 0.20; core [0.098, 0.619, 0.507, 0.767] rim [0.185, 0.555, 0.518, 0.599]
  - track 928 at frame 187: holes 1, rim-vs-core 0.20, rim-vs-outside 0.82, heterogeneity 0.20; core [0.104, 0.737, 0.557, 0.6] rim [0.196, 0.561, 0.542, 0.613]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 205 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial S: peak at rho=1.85 (OUTSIDE the peak band 0.5-1.5), rim/core 9.98, rim/outside 0.768 (aggregate of 205 individuals; 0/205 membrane-like individually; rim level 0.499)
  - radial K catalyst: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.08, rim/outside 7.25 (aggregate of 205 individuals; 14/205 membrane-like individually; rim level 0.619)
  - radial L link: peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.64, rim/outside 5.45 (aggregate of 205 individuals; 159/205 membrane-like individually; rim level 0.529)  MEMBRANE-LIKE
  - radial membrane (wall): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 2.24, rim/outside 6.04 (aggregate of 205 individuals; 158/205 membrane-like individually; rim level 0.568)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): L link, membrane (wall)
- membrane-like channels per top track at mid-life: #762 (t=8150, R_eq 11, ring): ['K catalyst', 'L link', 'membrane (wall)']; #171 (t=1600, R_eq 10.09): ['L link', 'membrane (wall)']; #400 (t=3600, R_eq 11.04, ring): ['L link', 'membrane (wall)']; #928 (t=9350, R_eq 11.49, ring): ['L link', 'membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 132 of 205 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
