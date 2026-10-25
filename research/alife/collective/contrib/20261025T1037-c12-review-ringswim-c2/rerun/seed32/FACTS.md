# Evidence pack: ringswim-waste (seed 32)

- world: `../../world_claim.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_membrane + phase_swimdiv; mutation: links adsorb to the wall (drift chi up grad of 4 phi(1-phi)); parent: unstructured initial condition: smoothed Gaussian noise phi (mean 0, sd 0.2), uniform random K in [0,0.6] and L in [0,0.1] everywhere
- run: 201 frames x 100 steps x dt 1.0 = time 20000; grid [128, 128]; wall 183s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1037-c12-review-ringswim-c2/world_claim.py --out collective/contrib/20261025T1037-c12-review-ringswim-c2/rerun/seed32 --seeds 32 --spf 100 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5524], min area 6 px

## Measurements
- components: final 2, mean 7.2, max 15; occupancy final 0.13
- tracks: 385; persistent (alive >= 50% of run): 0; longest 27 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 5.22, final 2; holes at thresholds 0.2/0.35/0.5 final [1, 3, 4]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [5, 4, 2], H1 [4, 4, 1]
- motion: 3 long-lived tracks moved >= 1 body length; max speed 0.0301/time; max body lengths 5.1
- replication (lineage window K = 20 frames = time 2000, default): splits 132, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 118, merge/split ratio 0.894, nucleations 2
- channel total drift (end/start - 1): [-0.2611, -0.8591, -0.4521, -0.6808]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 59 at frame 20: holes 0, rim-vs-core 0.72, rim-vs-outside 0.54, heterogeneity 0.21; core [0.267, 0.782, 0.86, 0.853] rim [0.413, 0.3, 0.478, 0.517]
  - track 48 at frame 17: holes 1, rim-vs-core 0.19, rim-vs-outside 0.75, heterogeneity 0.18; core [0.111, 0.619, 0.548, 0.759] rim [0.173, 0.522, 0.492, 0.621]
  - track 289 at frame 109: holes 1, rim-vs-core 0.21, rim-vs-outside 0.80, heterogeneity 0.20; core [0.073, 0.683, 0.455, 0.55] rim [0.191, 0.536, 0.509, 0.63]
  - track 345 at frame 153: holes 1, rim-vs-core 0.25, rim-vs-outside 0.82, heterogeneity 0.24; core [0.05, 0.733, 0.422, 0.434] rim [0.178, 0.607, 0.541, 0.564]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 38 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial S: peak at rho=1.95 (OUTSIDE the peak band 0.5-1.5), rim/core 7.32, rim/outside 0.791 (aggregate of 38 individuals; 0/38 membrane-like individually; rim level 0.536)
  - radial K catalyst: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.982, rim/outside 8.22 (aggregate of 38 individuals; 3/38 membrane-like individually; rim level 0.621)
  - radial L link: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.42, rim/outside 5.87 (aggregate of 38 individuals; 24/38 membrane-like individually; rim level 0.547)
  - radial membrane (wall): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 2.19, rim/outside 7.53 (aggregate of 38 individuals; 28/38 membrane-like individually; rim level 0.549)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): membrane (wall)
- membrane-like channels per top track at mid-life: #59 (t=2000, R_eq 4.62): none; #48 (t=1700, R_eq 12.82, ring): ['K catalyst', 'L link', 'membrane (wall)']; #289 (t=10900, R_eq 12.18): ['L link']; #345 (t=15300, R_eq 14.83): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 22 of 38 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
