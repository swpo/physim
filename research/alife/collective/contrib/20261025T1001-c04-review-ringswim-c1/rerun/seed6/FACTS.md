# Evidence pack: ringswim-waste (seed 6)

- world: `../../../../../../../../home/user/physim/research/alife/collective/contrib/20261025T0806-c07-ringswim-claim/world_claim.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_membrane + phase_swimdiv; mutation: links adsorb to the wall (drift chi up grad of 4 phi(1-phi)); parent: unstructured initial condition: smoothed Gaussian noise phi (mean 0, sd 0.2), uniform random K in [0,0.6] and L in [0,0.1] everywhere
- run: 201 frames x 100 steps x dt 1.0 = time 20000; grid [128, 128]; wall 125s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0806-c07-ringswim-claim/world_claim.py --out /tmp/claude-0/-home-user-physim/fba552f4-82e1-5fd3-8aee-1d1a9784fecc/scratchpad/rev4/claim --seeds 5 6 --spf 100 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5527], min area 6 px

## Measurements
- components: final 4, mean 9.0, max 20; occupancy final 0.14
- tracks: 431; persistent (alive >= 50% of run): 0; longest 29 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 6.33, final 3; holes at thresholds 0.2/0.35/0.5 final [0, 5, 5]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [8, 6, 5], H1 [6, 5, 2]
- motion: 5 long-lived tracks moved >= 1 body length; max speed 0.0425/time; max body lengths 4.0
- replication (lineage window K = 20 frames = time 2000, default): splits 147, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 119, merge/split ratio 0.81, nucleations 1
- channel total drift (end/start - 1): [-0.2723, -0.8538, -0.4102, -0.618]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 4 at frame 13: holes 1, rim-vs-core 0.29, rim-vs-outside 0.73, heterogeneity 0.21; core [0.126, 0.746, 0.644, 0.645] rim [0.232, 0.513, 0.511, 0.584]
  - track 252 at frame 109: holes 0, rim-vs-core 0.42, rim-vs-outside 0.84, heterogeneity 0.19; core [0.157, 0.824, 0.681, 0.761] rim [0.329, 0.463, 0.597, 0.682]
  - track 316 at frame 143: holes 1, rim-vs-core 0.28, rim-vs-outside 0.62, heterogeneity 0.18; core [0.11, 0.643, 0.534, 0.731] rim [0.215, 0.459, 0.466, 0.556]
  - track 394 at frame 188: holes 1, rim-vs-core 0.42, rim-vs-outside 0.99, heterogeneity 0.20; core [0.034, 0.687, 0.38, 0.35] rim [0.189, 0.55, 0.544, 0.681]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 43 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial S: peak at rho=1.95 (OUTSIDE the peak band 0.5-1.5), rim/core 8.85, rim/outside 0.796 (aggregate of 43 individuals; 0/43 membrane-like individually; rim level 0.552)
  - radial K catalyst: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 0.999, rim/outside 9.09 (aggregate of 43 individuals; 0/43 membrane-like individually; rim level 0.627)
  - radial L link: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.4, rim/outside 6.53 (aggregate of 43 individuals; 24/43 membrane-like individually; rim level 0.538)
  - radial membrane (wall): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.74, rim/outside 7.2 (aggregate of 43 individuals; 23/43 membrane-like individually; rim level 0.542)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): membrane (wall)
- membrane-like channels per top track at mid-life: #4 (t=1300, R_eq 8.76, ring): ['L link', 'membrane (wall)']; #252 (t=10900, R_eq 6.46): none; #316 (t=14300, R_eq 10, ring): ['L link', 'membrane (wall)']; #394 (t=18800, R_eq 15.86, ring): ['K catalyst', 'L link']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 13 of 43 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
