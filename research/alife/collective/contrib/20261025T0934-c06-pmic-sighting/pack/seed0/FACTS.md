# Evidence pack: pmic-kf0.03 (seed 0)

- world: `../world_kf0.03.py`, family `hybrid-particle-field`
- parent: collective/contrib/20261025T0752-c03-fch-cargo-fission/world.py; mutation: uniform amphiphile feed -> local synthesis by gated catalyst particles from a fed precursor, plus amphiphile decay
- run: 81 frames x 250 steps x dt 0.02 = time 400; grid [128, 128]; wall 197s; status ok
- command: `python -m labkit.run collective/work/pmic/world_kf0.03.py --out collective/work/pmic/pack_kf0.03 --seeds 0 --frames 80 --no-movie`
- segmentation: matter > 0.13 of robust range [0.1164, 2.9967], min area 6 px

## Measurements
- components: final 94, mean 69.8, max 96; occupancy final 0.49
- tracks: 185; persistent (alive >= 50% of run): 66; longest 80 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.35 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [100, 100, 100], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 1.0
- replication (lineage window K = 20 frames = time 100, default): splits 75, persistent splits 45 (0 more failed only because the siblings re-merged within K), max generation 4, merges 6, merge/split ratio 0.08, nucleations 23
- channel total drift (end/start - 1): [1.6964, 0.24, -0.5793]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 6 at frame 41: holes 0, rim-vs-core 0.60, rim-vs-outside 0.13, heterogeneity 0.19; core [0.629, 0.5, 0.18] rim [0.178, 0.112, 0.201]
  - track 17 at frame 41: holes 0, rim-vs-core 0.58, rim-vs-outside 0.13, heterogeneity 0.19; core [0.619, 0.479, 0.133] rim [0.172, 0.116, 0.163]
  - track 23 at frame 41: holes 0, rim-vs-core 0.62, rim-vs-outside 0.13, heterogeneity 0.20; core [0.619, 0.541, 0.128] rim [0.167, 0.117, 0.152]
  - track 138 at frame 63: holes 0, rim-vs-core 0.59, rim-vs-outside 0.12, heterogeneity 0.19; core [0.615, 0.471, 0.025] rim [0.168, 0.089, 0.039]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 457 components >= 12 px at frames [13, 27, 40, 53, 67, 80]):
  - radial amphiphile u (u + 1.6): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.513, rim/outside 3.59 (aggregate of 457 individuals; 6/457 membrane-like individually; rim level 0.476)
  - radial K particles: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.429, rim/outside 3.69 (aggregate of 457 individuals; 0/457 membrane-like individually; rim level 0.348)
  - radial precursor S: peak at rho=1.55 (OUTSIDE the peak band 0.5-1.5), rim/core 1.33, rim/outside 0.991 (aggregate of 457 individuals; 0/457 membrane-like individually; rim level 0.169)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #6 (t=205, R_eq 5.01): none; #17 (t=205, R_eq 5.08): none; #23 (t=205, R_eq 5.05): none; #138 (t=315, R_eq 5.05): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 1 of 457 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
