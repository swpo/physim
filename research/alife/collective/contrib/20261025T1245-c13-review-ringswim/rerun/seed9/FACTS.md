# Evidence pack: ringswim-waste (seed 9)

- world: `../../world_claim.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_membrane + phase_swimdiv; mutation: links adsorb to the wall (drift chi up grad of 4 phi(1-phi)); parent: unstructured initial condition: smoothed Gaussian noise phi (mean 0, sd 0.2), uniform random K in [0,0.6] and L in [0,0.1] everywhere
- run: 201 frames x 100 steps x dt 1.0 = time 20000; grid [128, 128]; wall 120s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1245-c13-review-ringswim/world_claim.py --out collective/contrib/20261025T1245-c13-review-ringswim/rerun --seeds 9 10 --spf 100 --frames 200 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5555], min area 6 px

## Measurements
- components: final 9, mean 11.0, max 20; occupancy final 0.21
- tracks: 572; persistent (alive >= 50% of run): 0; longest 23 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 7.43, final 6; holes at thresholds 0.2/0.35/0.5 final [2, 7, 8]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [12, 10, 8], H1 [9, 9, 3]
- motion: 3 long-lived tracks moved >= 1 body length; max speed 0.0237/time; max body lengths 3.4
- replication (lineage window K = 20 frames = time 2000, default): splits 197, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 166, merge/split ratio 0.843, nucleations 3
- channel total drift (end/start - 1): [-0.3623, -0.789, -0.2165, -0.39]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 486 at frame 161: holes 0, rim-vs-core 0.31, rim-vs-outside 0.75, heterogeneity 0.18; core [0.087, 0.65, 0.47, 0.645] rim [0.269, 0.406, 0.524, 0.675]
  - track 383 at frame 124: holes 1, rim-vs-core 0.36, rim-vs-outside 0.73, heterogeneity 0.24; core [0.145, 0.799, 0.717, 0.6] rim [0.264, 0.526, 0.52, 0.55]
  - track 202 at frame 66: holes 1, rim-vs-core 0.21, rim-vs-outside 0.77, heterogeneity 0.22; core [0.113, 0.735, 0.587, 0.622] rim [0.195, 0.559, 0.52, 0.605]
  - track 22 at frame 10: holes 0, rim-vs-core 0.23, rim-vs-outside 0.91, heterogeneity 0.19; core [0.11, 0.72, 0.602, 0.682] rim [0.209, 0.533, 0.531, 0.636]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 64 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial S: peak at rho=1.85 (OUTSIDE the peak band 0.5-1.5), rim/core 10.2, rim/outside 0.782 (aggregate of 64 individuals; 0/64 membrane-like individually; rim level 0.523)
  - radial K catalyst: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.05, rim/outside 8.51 (aggregate of 64 individuals; 3/64 membrane-like individually; rim level 0.651)
  - radial L link: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.49, rim/outside 6.39 (aggregate of 64 individuals; 45/64 membrane-like individually; rim level 0.567)
  - radial membrane (wall): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 2.27, rim/outside 6.91 (aggregate of 64 individuals; 48/64 membrane-like individually; rim level 0.574)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): membrane (wall)
- membrane-like channels per top track at mid-life: #486 (t=16100, R_eq 9.51): ['membrane (wall)']; #383 (t=12400, R_eq 9.13, ring): ['L link', 'membrane (wall)']; #202 (t=6600, R_eq 10.48, ring): ['L link', 'membrane (wall)']; #22 (t=1000, R_eq 8.65): ['membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 39 of 64 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
