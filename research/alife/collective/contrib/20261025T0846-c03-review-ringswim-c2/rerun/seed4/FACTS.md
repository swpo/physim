# Evidence pack: ringswim-waste (seed 4)

- world: `../../../../../../../../../home/user/physim/research/alife/collective/contrib/20261025T0806-c07-ringswim-claim/world_claim.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_membrane + phase_swimdiv; mutation: links adsorb to the wall (drift chi up grad of 4 phi(1-phi)); parent: unstructured initial condition: smoothed Gaussian noise phi (mean 0, sd 0.2), uniform random K in [0,0.6] and L in [0,0.1] everywhere
- run: 201 frames x 100 steps x dt 1.0 = time 20000; grid [128, 128]; wall 113s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0806-c07-ringswim-claim/world_claim.py --out /tmp/claude-0/-home-user-physim/ca3fe853-e88d-58ad-9551-2586c1b06c34/scratchpad/rev/rsw/claim/seed4 --seeds 4 --spf 100 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.556], min area 6 px

## Measurements
- components: final 14, mean 9.4, max 18; occupancy final 0.19
- tracks: 474; persistent (alive >= 50% of run): 0; longest 26 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 6.41, final 6; holes at thresholds 0.2/0.35/0.5 final [0, 6, 11]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [15, 14, 14], H1 [13, 13, 4]
- motion: 7 long-lived tracks moved >= 1 body length; max speed 0.0584/time; max body lengths 5.7
- replication (lineage window K = 20 frames = time 2000, default): splits 151, persistent splits 1 (0 more failed only because the siblings re-merged within K), max generation 1, merges 130, merge/split ratio 0.861, nucleations 4
- channel total drift (end/start - 1): [-0.3181, -0.821, -0.2798, -0.5383]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 398 at frame 168: holes 2, rim-vs-core 0.31, rim-vs-outside 0.88, heterogeneity 0.21; core [0.036, 0.679, 0.386, 0.381] rim [0.174, 0.574, 0.522, 0.595]
  - track 411 at frame 173: holes 1, rim-vs-core 0.23, rim-vs-outside 0.71, heterogeneity 0.18; core [0.085, 0.541, 0.443, 0.827] rim [0.163, 0.527, 0.496, 0.615]
  - track 87 at frame 45: holes 1, rim-vs-core 0.19, rim-vs-outside 0.70, heterogeneity 0.18; core [0.094, 0.602, 0.477, 0.772] rim [0.156, 0.494, 0.461, 0.63]
  - track 199 at frame 96: holes 1, rim-vs-core 0.16, rim-vs-outside 0.82, heterogeneity 0.21; core [0.087, 0.692, 0.514, 0.638] rim [0.187, 0.577, 0.545, 0.599]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 60 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial S: peak at rho=1.85 (OUTSIDE the peak band 0.5-1.5), rim/core 8.06, rim/outside 0.807 (aggregate of 60 individuals; 0/60 membrane-like individually; rim level 0.528)
  - radial K catalyst: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.02, rim/outside 8.18 (aggregate of 60 individuals; 4/60 membrane-like individually; rim level 0.65)
  - radial L link: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.5, rim/outside 6.15 (aggregate of 60 individuals; 38/60 membrane-like individually; rim level 0.594)
  - radial membrane (wall): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.93, rim/outside 7.09 (aggregate of 60 individuals; 39/60 membrane-like individually; rim level 0.593)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): membrane (wall)
- membrane-like channels per top track at mid-life: #398 (t=16800, R_eq 15.51): none; #411 (t=17300, R_eq 11.82, ring): ['L link', 'membrane (wall)']; #87 (t=4500, R_eq 12.33, ring): ['L link', 'membrane (wall)']; #199 (t=9600, R_eq 10.65): ['L link', 'membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 30 of 60 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
