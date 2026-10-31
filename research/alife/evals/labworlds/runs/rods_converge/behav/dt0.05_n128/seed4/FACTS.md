# Evidence pack: active-nematic-marangoni (seed 4)

- world: `../../../../../../../../../../home/user/physim/research/alife/collective/contrib/20261026T0505-c34-nematic-marangoni/world.py`, family `active-nematic`
- parent: 20261025T1141-c11-active-nematic-ringed; mutation: surfactant source restricted to rod pixels (phi>0); chis 3 -> 5; optional ring-gated CH mobility gm; cargo excluded by the ring (kappa); Marangoni stress of the ring (mar)
- run: 121 frames x 100 steps x dt 0.05 = time 600; grid [128, 128]; wall 203s; status ok
- command: `python -m labkit.run /home/user/physim/research/alife/collective/contrib/20261026T0505-c34-nematic-marangoni/world.py --out /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/rods_converge/behav/dt0.05_n128 --seeds 3 4 --frames 120 --spf 100 --dt 0.05 --size 128 128 --no-movie`
- segmentation: matter > 0.59 of robust range [-0.8356, 0.5735], min area 6 px

## Measurements
- components: final 34, mean 22.5, max 34; occupancy final 0.09
- tracks: 77; persistent (alive >= 50% of run): 16; longest 105 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 7.56 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [34, 34, 32], H1 [0, 0, 0]
- motion: 40 long-lived tracks moved >= 1 body length; max speed 0.327/time; max body lengths 8.7
- replication (lineage window K = 20 frames = time 100, default): splits 30, persistent splits 22 (0 more failed only because the siblings re-merged within K), max generation 3, merges 6, merge/split ratio 0.2, nucleations 11
- channel total drift (end/start - 1): [-0.5081, -0.3979, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 8 at frame 69: holes 0, rim-vs-core 0.73, rim-vs-outside 0.35, heterogeneity 0.23; core [0.955, 0.748, 0.419, 0.464] rim [0.751, 0.482, 0.894, 0.018]
  - track 14 at frame 72: holes 0, rim-vs-core 0.76, rim-vs-outside 0.35, heterogeneity 0.24; core [0.944, 0.793, 0.46, 0.462] rim [0.747, 0.5, 0.956, 0.012]
  - track 18 at frame 75: holes 0, rim-vs-core 0.53, rim-vs-outside 0.42, heterogeneity 0.22; core [0.936, 0.797, 0.43, 0.35] rim [0.751, 0.534, 0.77, 0.101]
  - track 39 at frame 88: holes 0, rim-vs-core 0.76, rim-vs-outside 0.32, heterogeneity 0.24; core [0.957, 0.63, 0.417, 0.501] rim [0.759, 0.404, 0.923, 0.018]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 154 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.8, rim/outside 4.68 (aggregate of 154 individuals; 0/154 membrane-like individually; rim level 0.732)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.741, rim/outside 8.9 (aggregate of 154 individuals; 5/154 membrane-like individually; rim level 0.55)
  - radial surfactant s: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.39, rim/outside 3.25 (aggregate of 154 individuals; 92/154 membrane-like individually; rim level 0.582)
  - radial cargo c: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.36, rim/outside 2.07 (aggregate of 154 individuals; 16/154 membrane-like individually; rim level 0.133)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #8 (t=345, R_eq 4.41): none; #14 (t=360, R_eq 4.82): none; #18 (t=375, R_eq 3.99): none; #39 (t=440, R_eq 4.41): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 3 of 154 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
