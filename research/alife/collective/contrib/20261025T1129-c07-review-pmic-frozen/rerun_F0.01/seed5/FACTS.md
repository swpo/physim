# Evidence pack: pmic (seed 5)

- world: `../../../20261025T1013-c06-pmic-frozen/world.py`, family `hybrid-particle-field`
- parent: collective/contrib/20261025T0752-c03-fch-cargo-fission/world.py; mutation: uniform amphiphile feed -> local synthesis by gated catalyst particles from a fed precursor, plus amphiphile decay
- run: 201 frames x 250 steps x dt 0.02 = time 1000; grid [128, 128]; wall 535s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1013-c06-pmic-frozen/world.py --out collective/contrib/_c07rev21/rerun_F0.01/seed5 --seeds 5 --frames 200 --no-movie`
- segmentation: matter > 0.13 of robust range [0.1219, 2.9984], min area 6 px

## Measurements
- components: final 83, mean 88.7, max 114; occupancy final 0.68
- tracks: 559; persistent (alive >= 50% of run): 66; longest 200 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.41 (1 = constant size)
- enclosures: components with a hole mean 0.16, final 1; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [131, 130, 128], H1 [7, 0, 0]
- motion: 6 long-lived tracks moved >= 1 body length; max speed 0.0178/time; max body lengths 1.4
- replication (lineage window K = 20 frames = time 100, default): splits 201, persistent splits 41 (0 more failed only because the siblings re-merged within K), max generation 4, merges 117, merge/split ratio 0.582, nucleations 20
- channel total drift (end/start - 1): [2.3721, 0.4786, -0.6606]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 5 at frame 101: holes 0, rim-vs-core 0.57, rim-vs-outside 0.13, heterogeneity 0.17; core [0.612, 0.467, 0.078] rim [0.163, 0.121, 0.089]
  - track 38 at frame 103: holes 0, rim-vs-core 0.59, rim-vs-outside 0.11, heterogeneity 0.19; core [0.603, 0.475, 0.071] rim [0.156, 0.094, 0.082]
  - track 7 at frame 99: holes 0, rim-vs-core 0.59, rim-vs-outside 0.11, heterogeneity 0.18; core [0.61, 0.46, 0.074] rim [0.155, 0.084, 0.087]
  - track 231 at frame 148: holes 0, rim-vs-core 0.55, rim-vs-outside 0.11, heterogeneity 0.18; core [0.589, 0.429, 0.043] rim [0.149, 0.099, 0.054]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 555 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial amphiphile u (u + 1.6): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.504, rim/outside 1.81 (aggregate of 555 individuals; 0/555 membrane-like individually; rim level 0.464)
  - radial K particles: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.421, rim/outside 1.82 (aggregate of 555 individuals; 1/555 membrane-like individually; rim level 0.332)
  - radial precursor S: peak at rho=1.35 (in the peak band 0.5-1.5), rim/core 1.34, rim/outside 1.05 (aggregate of 555 individuals; 4/555 membrane-like individually; rim level 0.11)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #5 (t=505, R_eq 5.08): none; #38 (t=515, R_eq 5.11): none; #7 (t=495, R_eq 5.08): none; #231 (t=740, R_eq 5.14): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 2 of 555 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
