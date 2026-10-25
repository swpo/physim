# Evidence pack: ringswim-waste (seed 5)

- world: `../../../../../../../home/user/physim/research/alife/collective/contrib/20261025T0949-c07-wall-tilt-drive-negative/world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_membrane + phase_swimdiv; mutation: links adsorb to the wall (drift chi up grad of 4 phi(1-phi)); parent: unstructured initial condition: smoothed Gaussian noise phi (mean 0, sd 0.2), uniform random K in [0,0.6] and L in [0,0.1] everywhere
- run: 201 frames x 50 steps x dt 1.0 = time 10000; grid [128, 128]; wall 61s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0949-c07-wall-tilt-drive-negative/world.py --out /tmp/claude-0/-home-user-physim/fba552f4-82e1-5fd3-8aee-1d1a9784fecc/scratchpad/rev12/a7 --seeds 5 --frames 200 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5907], min area 6 px

## Measurements
- components: final 0, mean 4.1, max 33; occupancy final 0.00
- tracks: 139; persistent (alive >= 50% of run): 0; longest 27 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.28, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [0, 0, 0], H1 [0, 0, 0]
- motion: 3 long-lived tracks moved >= 1 body length; max speed 0.0139/time; max body lengths 1.5
- replication (lineage window K = 20 frames = time 1000, default): splits 46, persistent splits 1 (0 more failed only because the siblings re-merged within K), max generation 1, merges 8, merge/split ratio 0.174, nucleations 1
- channel total drift (end/start - 1): [0.0, -1.0, -1.0, -1.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 32 at frame 18: holes 1, rim-vs-core 0.38, rim-vs-outside 0.80, heterogeneity 0.23; core [0.04, 0.863, 0.727, 0.548] rim [0.194, 0.57, 0.547, 0.616]
  - track 23 at frame 15: holes 0, rim-vs-core 0.70, rim-vs-outside 0.55, heterogeneity 0.21; core [0.086, 0.826, 0.803, 0.825] rim [0.283, 0.308, 0.462, 0.562]
  - track 120 at frame 87: holes 0, rim-vs-core 0.62, rim-vs-outside 0.55, heterogeneity 0.18; core [0.283, 0.739, 0.982, 0.893] rim [0.391, 0.361, 0.743, 0.472]
  - track 57 at frame 17: holes 0, rim-vs-core 0.60, rim-vs-outside 0.51, heterogeneity 0.17; core [0.361, 0.597, 0.908, 0.967] rim [0.445, 0.238, 0.533, 0.676]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 11 components >= 12 px at frames [34, 67, 101]):
  - radial S: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 13.8, rim/outside 0.827 (aggregate of 11 individuals; 0/11 membrane-like individually; rim level 0.564)
  - radial K catalyst: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.936, rim/outside 10.7 (aggregate of 11 individuals; 0/11 membrane-like individually; rim level 0.849)
  - radial L link: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.34, rim/outside 9.6 (aggregate of 11 individuals; 6/11 membrane-like individually; rim level 0.885)
  - radial membrane (wall): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.81, rim/outside 8.7 (aggregate of 11 individuals; 7/11 membrane-like individually; rim level 0.845)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): membrane (wall)
- membrane-like channels per top track at mid-life: #32 (t=900, R_eq 9.13, ring): ['L link', 'membrane (wall)']; #23 (t=750, R_eq 5.81): ['L link', 'membrane (wall)']; #120 (t=4350, R_eq 3.57): none; #57 (t=850, R_eq 2.99): none

## Warnings
- no components at the end: matter died out or fell below threshold
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 1 of 11 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
