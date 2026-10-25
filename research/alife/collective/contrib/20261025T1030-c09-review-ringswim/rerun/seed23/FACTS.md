# Evidence pack: ringswim-waste (seed 23)

- world: `../../../20261025T0806-c07-ringswim-claim/world_claim.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_membrane + phase_swimdiv; mutation: links adsorb to the wall (drift chi up grad of 4 phi(1-phi)); parent: unstructured initial condition: smoothed Gaussian noise phi (mean 0, sd 0.2), uniform random K in [0,0.6] and L in [0,0.1] everywhere
- run: 201 frames x 100 steps x dt 1.0 = time 20000; grid [128, 128]; wall 116s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0806-c07-ringswim-claim/world_claim.py --out collective/contrib/20261025T1030-c09-review-ringswim/rerun/seed23 --seeds 23 --spf 100 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5606], min area 6 px

## Measurements
- components: final 5, mean 11.3, max 23; occupancy final 0.19
- tracks: 595; persistent (alive >= 50% of run): 0; longest 25 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 7.45, final 5; holes at thresholds 0.2/0.35/0.5 final [0, 7, 6]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [9, 5, 5], H1 [7, 6, 2]
- motion: 7 long-lived tracks moved >= 1 body length; max speed 0.0352/time; max body lengths 4.2
- replication (lineage window K = 20 frames = time 2000, default): splits 190, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 176, merge/split ratio 0.926, nucleations 4
- channel total drift (end/start - 1): [-0.3297, -0.811, -0.2955, -0.3884]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 75 at frame 24: holes 1, rim-vs-core 0.20, rim-vs-outside 0.81, heterogeneity 0.19; core [0.103, 0.736, 0.567, 0.58] rim [0.174, 0.556, 0.523, 0.624]
  - track 42 at frame 13: holes 1, rim-vs-core 0.33, rim-vs-outside 0.73, heterogeneity 0.22; core [0.137, 0.777, 0.679, 0.601] rim [0.254, 0.517, 0.516, 0.569]
  - track 522 at frame 170: holes 1, rim-vs-core 0.21, rim-vs-outside 0.84, heterogeneity 0.23; core [0.083, 0.733, 0.518, 0.55] rim [0.208, 0.575, 0.546, 0.6]
  - track 181 at frame 52: holes 0, rim-vs-core 0.45, rim-vs-outside 0.84, heterogeneity 0.22; core [0.086, 0.756, 0.559, 0.525] rim [0.295, 0.407, 0.543, 0.717]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 58 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial S: peak at rho=1.85 (OUTSIDE the peak band 0.5-1.5), rim/core 7.33, rim/outside 0.798 (aggregate of 58 individuals; 0/58 membrane-like individually; rim level 0.501)
  - radial K catalyst: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.02, rim/outside 6.6 (aggregate of 58 individuals; 2/58 membrane-like individually; rim level 0.618)
  - radial L link: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.47, rim/outside 5.24 (aggregate of 58 individuals; 35/58 membrane-like individually; rim level 0.543)
  - radial membrane (wall): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.78, rim/outside 5.48 (aggregate of 58 individuals; 37/58 membrane-like individually; rim level 0.581)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): membrane (wall)
- membrane-like channels per top track at mid-life: #75 (t=2400, R_eq 10.06, ring): ['L link', 'membrane (wall)']; #42 (t=1300, R_eq 9.03, ring): ['L link', 'membrane (wall)']; #522 (t=17000, R_eq 10.46): ['L link', 'membrane (wall)']; #181 (t=5200, R_eq 8.27): ['L link', 'membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 25 of 58 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
