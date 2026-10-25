# Evidence pack: pmic (seed 3)

- world: `../../20261025T1013-c06-pmic-frozen/world.py`, family `hybrid-particle-field`
- parent: collective/contrib/20261025T0752-c03-fch-cargo-fission/world.py; mutation: uniform amphiphile feed -> local synthesis by gated catalyst particles from a fed precursor, plus amphiphile decay
- run: 201 frames x 250 steps x dt 0.02 = time 1000; grid [128, 128]; wall 402s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1013-c06-pmic-frozen/world.py --out collective/contrib/20261025T1121-c01-review-pmic/F0005 --seeds 3 --frames 200 --no-movie`
- segmentation: matter > 0.13 of robust range [0.1221, 2.9973], min area 6 px

## Measurements
- components: final 114, mean 93.4, max 120; occupancy final 0.67
- tracks: 500; persistent (alive >= 50% of run): 65; longest 200 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.45 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [129, 129, 129], H1 [1, 0, 0]
- motion: 9 long-lived tracks moved >= 1 body length; max speed 0.0185/time; max body lengths 1.5
- replication (lineage window K = 20 frames = time 100, default): splits 185, persistent splits 29 (0 more failed only because the siblings re-merged within K), max generation 4, merges 85, merge/split ratio 0.459, nucleations 20
- channel total drift (end/start - 1): [2.3939, 0.4704, -0.6599]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 9 at frame 101: holes 0, rim-vs-core 0.57, rim-vs-outside 0.11, heterogeneity 0.18; core [0.606, 0.436, 0.081] rim [0.157, 0.089, 0.088]
  - track 33 at frame 103: holes 0, rim-vs-core 0.58, rim-vs-outside 0.11, heterogeneity 0.18; core [0.596, 0.462, 0.088] rim [0.151, 0.097, 0.095]
  - track 51 at frame 104: holes 0, rim-vs-core 0.59, rim-vs-outside 0.12, heterogeneity 0.19; core [0.602, 0.496, 0.076] rim [0.159, 0.11, 0.089]
  - track 184 at frame 129: holes 0, rim-vs-core 0.59, rim-vs-outside 0.11, heterogeneity 0.19; core [0.599, 0.473, 0.046] rim [0.157, 0.086, 0.058]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 605 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial amphiphile u (u + 1.6): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.499, rim/outside 1.72 (aggregate of 605 individuals; 1/605 membrane-like individually; rim level 0.464)
  - radial K particles: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.417, rim/outside 1.72 (aggregate of 605 individuals; 2/605 membrane-like individually; rim level 0.33)
  - radial precursor S: peak at rho=1.35 (in the peak band 0.5-1.5), rim/core 1.35, rim/outside 1.05 (aggregate of 605 individuals; 8/605 membrane-like individually; rim level 0.103)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #9 (t=505, R_eq 5.08): none; #33 (t=515, R_eq 5.17): none; #51 (t=520, R_eq 5.01): none; #184 (t=645, R_eq 5.08): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 2 of 605 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
