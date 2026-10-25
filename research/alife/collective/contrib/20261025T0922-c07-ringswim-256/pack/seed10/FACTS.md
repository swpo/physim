# Evidence pack: ringswim-waste (seed 10)

- world: `../../../../../home/user/physim/research/alife/collective/contrib/20261025T0806-c07-ringswim-claim/world_claim.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_membrane + phase_swimdiv; mutation: links adsorb to the wall (drift chi up grad of 4 phi(1-phi)); parent: unstructured initial condition: smoothed Gaussian noise phi (mean 0, sd 0.2), uniform random K in [0,0.6] and L in [0,0.1] everywhere
- run: 201 frames x 100 steps x dt 1.0 = time 20000; grid [256, 256]; wall 603s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0806-c07-ringswim-claim/world_claim.py --out /tmp/claude-0/c07/big/s10 --seeds 10 --size 256 256 --spf 100 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.555], min area 6 px

## Measurements
- components: final 31, mean 38.9, max 84; occupancy final 0.19
- tracks: 2001; persistent (alive >= 50% of run): 0; longest 36 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 26.26, final 22; holes at thresholds 0.2/0.35/0.5 final [6, 24, 32]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [41, 36, 32], H1 [35, 32, 13]
- motion: 27 long-lived tracks moved >= 1 body length; max speed 0.0362/time; max body lengths 5.6
- replication (lineage window K = 20 frames = time 2000, default): splits 666, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 572, merge/split ratio 0.859, nucleations 7
- channel total drift (end/start - 1): [-0.316, -0.8183, -0.3091, -0.4319]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1566 at frame 161: holes 0, rim-vs-core 0.48, rim-vs-outside 0.91, heterogeneity 0.22; core [0.114, 0.827, 0.63, 0.536] rim [0.337, 0.447, 0.599, 0.733]
  - track 48 at frame 17: holes 1, rim-vs-core 0.26, rim-vs-outside 0.73, heterogeneity 0.18; core [0.104, 0.685, 0.572, 0.679] rim [0.204, 0.476, 0.493, 0.603]
  - track 131 at frame 18: holes 0, rim-vs-core 0.43, rim-vs-outside 0.95, heterogeneity 0.22; core [0.102, 0.8, 0.606, 0.485] rim [0.29, 0.483, 0.571, 0.701]
  - track 117 at frame 18: holes 1, rim-vs-core 0.27, rim-vs-outside 0.63, heterogeneity 0.18; core [0.103, 0.63, 0.512, 0.744] rim [0.198, 0.465, 0.465, 0.562]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 214 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial S: peak at rho=1.95 (OUTSIDE the peak band 0.5-1.5), rim/core 9, rim/outside 0.784 (aggregate of 214 individuals; 0/214 membrane-like individually; rim level 0.53)
  - radial K catalyst: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.05, rim/outside 8.24 (aggregate of 214 individuals; 15/214 membrane-like individually; rim level 0.635)
  - radial L link: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.47, rim/outside 6.15 (aggregate of 214 individuals; 141/214 membrane-like individually; rim level 0.541)
  - radial membrane (wall): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.89, rim/outside 6.66 (aggregate of 214 individuals; 148/214 membrane-like individually; rim level 0.549)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): membrane (wall)
- membrane-like channels per top track at mid-life: #1566 (t=16100, R_eq 7.23): ['L link', 'membrane (wall)']; #48 (t=1700, R_eq 8.79, ring): ['L link', 'membrane (wall)']; #131 (t=1800, R_eq 8, ring): ['L link', 'membrane (wall)']; #117 (t=1800, R_eq 9.36, ring): ['L link', 'membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 106 of 214 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
