# Evidence pack: active-nematic-cargo (seed 51)

- world: `../../../../../../../../../home/user/physim/research/alife/collective/contrib/20261026T0405-c34-nematic-cargo/world.py`, family `active-nematic`
- parent: 20261025T1141-c11-active-nematic-ringed; mutation: surfactant source restricted to rod pixels (phi>0); chis 3 -> 5; optional ring-gated CH mobility gm; cargo excluded by the ring (kappa)
- run: 121 frames x 100 steps x dt 0.05 = time 600; grid [192, 192]; wall 613s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0405-c34-nematic-cargo/world.py --out /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/waudit/nematic-cargo/controls/res15_seed51 --seeds 51 --size 192 192 --frames 120 --no-movie`
- segmentation: matter > 0.57 of robust range [-0.8224, 0.6269], min area 6 px

## Measurements
- components: final 25, mean 16.0, max 27; occupancy final 0.06
- tracks: 70; persistent (alive >= 50% of run): 4; longest 63 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 28.86 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [27, 25, 25], H1 [1, 0, 0]
- motion: 30 long-lived tracks moved >= 1 body length; max speed 0.124/time; max body lengths 3.8
- replication (lineage window K = 20 frames = time 100, default): splits 29, persistent splits 17 (0 more failed only because the siblings re-merged within K), max generation 3, merges 4, merge/split ratio 0.138, nucleations 8
- channel total drift (end/start - 1): [-0.4948, -0.4118, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 27 at frame 90: holes 0, rim-vs-core 0.65, rim-vs-outside 0.24, heterogeneity 0.21; core [0.914, 0.799, 0.398, 0.445] rim [0.704, 0.525, 0.734, 0.013]
  - track 7 at frame 49: holes 0, rim-vs-core 0.51, rim-vs-outside 0.39, heterogeneity 0.16; core [0.923, 0.652, 0.425, 0.353] rim [0.748, 0.465, 0.722, 0.029]
  - track 13 at frame 59: holes 0, rim-vs-core 0.72, rim-vs-outside 0.24, heterogeneity 0.23; core [0.915, 0.868, 0.428, 0.518] rim [0.703, 0.574, 0.793, 0.012]
  - track 47 at frame 103: holes 0, rim-vs-core 0.72, rim-vs-outside 0.24, heterogeneity 0.23; core [0.923, 0.893, 0.397, 0.497] rim [0.705, 0.588, 0.772, 0.01]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 107 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.818, rim/outside 4.85 (aggregate of 107 individuals; 0/107 membrane-like individually; rim level 0.761)
  - radial order |Q|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.757, rim/outside 8.68 (aggregate of 107 individuals; 0/107 membrane-like individually; rim level 0.623)
  - radial surfactant s: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.62, rim/outside 3.2 (aggregate of 107 individuals; 76/107 membrane-like individually; rim level 0.57)  MEMBRANE-LIKE
  - radial cargo c: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.296, rim/outside 2.27 (aggregate of 107 individuals; 13/107 membrane-like individually; rim level 0.184)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): surfactant s
- membrane-like channels per top track at mid-life: #27 (t=450, R_eq 4.18): ['surfactant s']; #7 (t=245, R_eq 6.75): ['cargo c']; #13 (t=295, R_eq 5.29): ['surfactant s']; #47 (t=515, R_eq 5.08): ['surfactant s']

## Warnings
- radial: 2 of 107 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
