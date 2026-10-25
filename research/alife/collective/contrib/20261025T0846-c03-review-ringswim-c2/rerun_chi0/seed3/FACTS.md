# Evidence pack: ringswim-waste-chi0 (seed 3)

- world: `../../../../../../../../../home/user/physim/research/alife/collective/contrib/20261025T0806-c07-ringswim-claim/world_chi0.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_membrane + phase_swimdiv; mutation: links adsorb to the wall (drift chi up grad of 4 phi(1-phi)); parent: unstructured initial condition: smoothed Gaussian noise phi (mean 0, sd 0.2), uniform random K in [0,0.6] and L in [0,0.1] everywhere
- run: 201 frames x 100 steps x dt 1.0 = time 20000; grid [128, 128]; wall 104s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0806-c07-ringswim-claim/world_chi0.py --out /tmp/claude-0/-home-user-physim/ca3fe853-e88d-58ad-9551-2586c1b06c34/scratchpad/rev/rsw/chi0/seed3 --seeds 3 --spf 100 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5591], min area 6 px

## Measurements
- components: final 18, mean 21.4, max 28; occupancy final 0.21
- tracks: 251; persistent (alive >= 50% of run): 5; longest 134 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 5.20 (1 = constant size)
- enclosures: components with a hole mean 2.33, final 2; holes at thresholds 0.2/0.35/0.5 final [0, 2, 15]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [19, 18, 18], H1 [20, 18, 1]
- motion: 49 long-lived tracks moved >= 1 body length; max speed 0.0134/time; max body lengths 4.8
- replication (lineage window K = 20 frames = time 2000, default): splits 86, persistent splits 6 (0 more failed only because the siblings re-merged within K), max generation 2, merges 57, merge/split ratio 0.663, nucleations 1
- channel total drift (end/start - 1): [-0.3369, -0.8148, -0.2085, -0.4204]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 97 at frame 133: holes 0, rim-vs-core 0.39, rim-vs-outside 0.92, heterogeneity 0.18; core [0.077, 0.76, 0.713, 0.582] rim [0.269, 0.454, 0.65, 0.712]
  - track 53 at frame 84: holes 0, rim-vs-core 0.46, rim-vs-outside 0.87, heterogeneity 0.20; core [0.098, 0.789, 0.755, 0.588] rim [0.321, 0.417, 0.633, 0.669]
  - track 130 at frame 143: holes 0, rim-vs-core 0.56, rim-vs-outside 0.94, heterogeneity 0.22; core [0.095, 0.856, 0.841, 0.513] rim [0.329, 0.436, 0.628, 0.713]
  - track 163 at frame 150: holes 0, rim-vs-core 0.35, rim-vs-outside 0.89, heterogeneity 0.16; core [0.072, 0.731, 0.678, 0.596] rim [0.252, 0.456, 0.65, 0.714]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 131 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial S: peak at rho=1.85 (OUTSIDE the peak band 0.5-1.5), rim/core 17.3, rim/outside 0.854 (aggregate of 131 individuals; 0/131 membrane-like individually; rim level 0.533)
  - radial K catalyst: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 0.953, rim/outside 10.9 (aggregate of 131 individuals; 0/131 membrane-like individually; rim level 0.734)
  - radial L link: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.13, rim/outside 8.92 (aggregate of 131 individuals; 0/131 membrane-like individually; rim level 0.762)
  - radial membrane (wall): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 3.71, rim/outside 9.83 (aggregate of 131 individuals; 123/131 membrane-like individually; rim level 0.824)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): membrane (wall)
- membrane-like channels per top track at mid-life: #97 (t=13300, R_eq 7): ['membrane (wall)']; #53 (t=8400, R_eq 7.2): ['membrane (wall)']; #130 (t=14300, R_eq 6.93): ['membrane (wall)']; #163 (t=15000, R_eq 7.16): ['membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 16 of 131 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
