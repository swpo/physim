# Evidence pack: active-nematic-marangoni (seed 4)

- world: `../../../../../../../../../../home/user/physim/research/alife/collective/contrib/20261026T0505-c34-nematic-marangoni/world.py`, family `active-nematic`
- parent: 20261025T1141-c11-active-nematic-ringed; mutation: surfactant source restricted to rod pixels (phi>0); chis 3 -> 5; optional ring-gated CH mobility gm; cargo excluded by the ring (kappa); Marangoni stress of the ring (mar)
- run: 121 frames x 100 steps x dt 0.05 = time 600; grid [192, 192]; wall 471s; status ok
- command: `python -m labkit.run /home/user/physim/research/alife/collective/contrib/20261026T0505-c34-nematic-marangoni/world.py --out /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/rods_converge/behav/dt0.05_n192 --seeds 3 4 --frames 120 --spf 100 --dt 0.05 --size 192 192 --no-movie`
- segmentation: matter > 0.56 of robust range [-0.8449, 0.6682], min area 6 px

## Measurements
- components: final 28, mean 20.7, max 30; occupancy final 0.10
- tracks: 78; persistent (alive >= 50% of run): 14; longest 97 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 17.57 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [29, 28, 28], H1 [0, 0, 0]
- motion: 43 long-lived tracks moved >= 1 body length; max speed 0.539/time; max body lengths 5.5
- replication (lineage window K = 20 frames = time 100, default): splits 27, persistent splits 18 (0 more failed only because the siblings re-merged within K), max generation 3, merges 11, merge/split ratio 0.407, nucleations 13
- channel total drift (end/start - 1): [-0.5018, -0.2526, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 11 at frame 73: holes 0, rim-vs-core 0.93, rim-vs-outside 0.41, heterogeneity 0.24; core [0.97, 0.682, 0.277, 0.731] rim [0.754, 0.426, 0.776, 0.025]
  - track 15 at frame 75: holes 0, rim-vs-core 0.95, rim-vs-outside 0.46, heterogeneity 0.25; core [0.953, 0.835, 0.313, 0.756] rim [0.737, 0.524, 0.793, 0.033]
  - track 21 at frame 77: holes 0, rim-vs-core 0.86, rim-vs-outside 0.42, heterogeneity 0.25; core [0.963, 0.79, 0.296, 0.654] rim [0.746, 0.496, 0.765, 0.03]
  - track 53 at frame 100: holes 0, rim-vs-core 0.57, rim-vs-outside 0.50, heterogeneity 0.21; core [0.916, 0.87, 0.36, 0.48] rim [0.763, 0.63, 0.686, 0.103]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 143 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial phi (droplet): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.786, rim/outside 5.09 (aggregate of 143 individuals; 0/143 membrane-like individually; rim level 0.71)
  - radial order |Q|: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.732, rim/outside 10.1 (aggregate of 143 individuals; 11/143 membrane-like individually; rim level 0.53)
  - radial surfactant s: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.43, rim/outside 3.59 (aggregate of 143 individuals; 82/143 membrane-like individually; rim level 0.523)
  - radial cargo c: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.419, rim/outside 5.08 (aggregate of 143 individuals; 17/143 membrane-like individually; rim level 0.154)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #11 (t=365, R_eq 6.08): ['surfactant s']; #15 (t=375, R_eq 6.13): ['surfactant s']; #21 (t=385, R_eq 6.21): ['surfactant s']; #53 (t=500, R_eq 6.7): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 4 of 143 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
