# Evidence pack: phase-membrane-bd-twin (seed 9)

- world: `../../../../../../../../../home/user/physim/research/alife/collective/contrib/20261025T0731-c01-phase-membrane-bd-twin/twin_pm.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_protocell_noise; mutation: links adsorb to the wall (drift chi up grad of 4 phi(1-phi)); parent: unstructured initial condition: smoothed Gaussian noise phi (mean 0, sd 0.2), uniform random K in [0,0.6] and L in [0,0.1] everywhere
- run: 161 frames x 50 steps x dt 1.0 = time 8000; grid [128, 128]; wall 9s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0731-c01-phase-membrane-bd-twin/twin_pm.py --out /tmp/claude-0/-home-user-physim/ca3fe853-e88d-58ad-9551-2586c1b06c34/scratchpad/rev/pmbd/twin/seed9 --seeds 9 --frames 160 --spf 50 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5594], min area 6 px

## Measurements
- components: final 42, mean 32.3, max 42; occupancy final 0.28
- tracks: 110; persistent (alive >= 50% of run): 33; longest 120 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.04 (1 = constant size)
- enclosures: components with a hole mean 1.70, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [46, 42, 42], H1 [42, 20, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.8
- replication (lineage window K = 20 frames = time 1000, default): splits 38, persistent splits 24 (0 more failed only because the siblings re-merged within K), max generation 3, merges 2, merge/split ratio 0.053, nucleations 0
- channel total drift (end/start - 1): [-0.4662, -0.7302, 0.1779, -0.0934]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 64 at frame 101: holes 0, rim-vs-core 0.60, rim-vs-outside 0.80, heterogeneity 0.21; core [0.08, 0.843, 0.773, 0.557] rim [0.287, 0.358, 0.541, 0.711]
  - track 66 at frame 102: holes 0, rim-vs-core 0.56, rim-vs-outside 0.81, heterogeneity 0.21; core [0.074, 0.821, 0.741, 0.55] rim [0.282, 0.37, 0.548, 0.722]
  - track 67 at frame 102: holes 0, rim-vs-core 0.62, rim-vs-outside 0.80, heterogeneity 0.21; core [0.082, 0.854, 0.786, 0.554] rim [0.291, 0.351, 0.536, 0.708]
  - track 104 at frame 132: holes 0, rim-vs-core 0.57, rim-vs-outside 0.66, heterogeneity 0.21; core [0.137, 0.828, 0.862, 0.689] rim [0.288, 0.372, 0.558, 0.678]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 205 components >= 12 px at frames [27, 54, 81, 106, 133, 160]):
  - radial S: peak at rho=1.85 (OUTSIDE the peak band 0.5-1.5), rim/core 13.3, rim/outside 0.835 (aggregate of 205 individuals; 0/205 membrane-like individually; rim level 0.497)
  - radial K catalyst: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.846, rim/outside 36 (aggregate of 205 individuals; 0/205 membrane-like individually; rim level 0.706)
  - radial L link: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.12, rim/outside 21.6 (aggregate of 205 individuals; 15/205 membrane-like individually; rim level 0.768)
  - radial membrane (wall): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 2.88, rim/outside 25.6 (aggregate of 205 individuals; 186/205 membrane-like individually; rim level 0.831)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): membrane (wall)
- membrane-like channels per top track at mid-life: #64 (t=5050, R_eq 6.21): ['membrane (wall)']; #66 (t=5100, R_eq 6.58): ['membrane (wall)']; #67 (t=5100, R_eq 6.13): ['membrane (wall)']; #104 (t=6600, R_eq 5.05): ['membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 13 of 205 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
