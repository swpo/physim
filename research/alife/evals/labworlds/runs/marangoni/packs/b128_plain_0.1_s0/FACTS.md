# Evidence pack: active-nematic-marangoni-noise (seed 0)

- world: `../../mg_noise.py`, family `active-nematic`
- parent: collective/contrib/20261026T0505-c34-nematic-marangoni; mutation: dynamics noise sd 0.1 per sqrt(t): additive on ['phi', 'q1', 'q2', 's', 'c'], proportional on [], conserved (div of white flux) on []
- run: 101 frames x 100 steps x dt 0.05 = time 500; grid [128, 128]; wall 216s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/marangoni/mg_noise.py --out /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/marangoni/packs/b128_plain_0.1_s0 --seeds 0 --frames 100 --size 128 128 --no-movie`
- segmentation: matter > 0.59 of robust range [-0.8441, 0.5848], min area 6 px

## Measurements
- components: final 26, mean 28.9, max 43; occupancy final 0.07
- tracks: 178; persistent (alive >= 50% of run): 17; longest 95 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 9.29 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [28, 25, 21], H1 [2, 0, 0]
- motion: 41 long-lived tracks moved >= 1 body length; max speed 0.534/time; max body lengths 14.8
- replication (lineage window K = 20 frames = time 100, default): splits 35, persistent splits 2 (0 more failed only because the siblings re-merged within K), max generation 1, merges 32, merge/split ratio 0.914, nucleations 77
- channel total drift (end/start - 1): [-0.5082, 0.155, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 11 at frame 53: holes 0, rim-vs-core 0.57, rim-vs-outside 0.31, heterogeneity 0.19; core [0.904, 0.768, 0.421, 0.364] rim [0.745, 0.566, 0.797, 0.022]
  - track 27 at frame 54: holes 0, rim-vs-core 0.42, rim-vs-outside 0.22, heterogeneity 0.17; core [0.902, 0.388, 0.484, 0.212] rim [0.716, 0.246, 0.794, 0.059]
  - track 36 at frame 50: holes 0, rim-vs-core 0.67, rim-vs-outside 0.39, heterogeneity 0.23; core [0.928, 0.892, 0.45, 0.341] rim [0.741, 0.552, 0.891, 0.02]
  - track 83 at frame 64: holes 0, rim-vs-core 0.53, rim-vs-outside 0.22, heterogeneity 0.19; core [0.914, 0.437, 0.511, 0.319] rim [0.741, 0.245, 0.857, 0.021]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 178 components >= 12 px at frames [17, 33, 50, 67, 83, 100]):
  - radial phi (droplet): peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.831, rim/outside 3.98 (aggregate of 178 individuals; 3/178 membrane-like individually; rim level 0.742)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.74, rim/outside 2.95 (aggregate of 178 individuals; 12/178 membrane-like individually; rim level 0.488)
  - radial surfactant s: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.47, rim/outside 2.65 (aggregate of 178 individuals; 107/178 membrane-like individually; rim level 0.61)
  - radial cargo c: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.441, rim/outside 0.682 (aggregate of 178 individuals; 14/178 membrane-like individually; rim level 0.128)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #11 (t=265, R_eq 3.7): none; #27 (t=270, R_eq 3.61): none; #36 (t=250, R_eq 3.78): none; #83 (t=320, R_eq 3.7): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 7 of 178 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
