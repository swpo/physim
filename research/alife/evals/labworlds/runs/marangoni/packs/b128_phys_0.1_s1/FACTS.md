# Evidence pack: active-nematic-marangoni-noise (seed 1)

- world: `../../mg_noise.py`, family `active-nematic`
- parent: collective/contrib/20261026T0505-c34-nematic-marangoni; mutation: dynamics noise sd 0.1 per sqrt(t): additive on ['q1', 'q2'], proportional on ['s', 'c'], conserved (div of white flux) on ['phi']
- run: 101 frames x 100 steps x dt 0.05 = time 500; grid [128, 128]; wall 215s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/marangoni/mg_noise.py --out /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/marangoni/packs/b128_phys_0.1_s1 --seeds 1 --frames 100 --size 128 128 --no-movie`
- segmentation: matter > 0.59 of robust range [-0.8348, 0.5842], min area 6 px

## Measurements
- components: final 29, mean 17.8, max 30; occupancy final 0.09
- tracks: 93; persistent (alive >= 50% of run): 5; longest 66 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 4.87 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [32, 30, 28], H1 [0, 0, 0]
- motion: 35 long-lived tracks moved >= 1 body length; max speed 0.319/time; max body lengths 8.2
- replication (lineage window K = 20 frames = time 100, default): splits 34, persistent splits 12 (0 more failed only because the siblings re-merged within K), max generation 3, merges 14, merge/split ratio 0.412, nucleations 10
- channel total drift (end/start - 1): [-0.4915, 0.3185, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 19 at frame 68: holes 0, rim-vs-core 0.67, rim-vs-outside 0.38, heterogeneity 0.22; core [0.923, 0.844, 0.402, 0.505] rim [0.733, 0.552, 0.729, 0.031]
  - track 25 at frame 70: holes 0, rim-vs-core 0.76, rim-vs-outside 0.39, heterogeneity 0.25; core [0.961, 0.893, 0.359, 0.565] rim [0.772, 0.552, 0.795, 0.079]
  - track 20 at frame 66: holes 0, rim-vs-core 0.65, rim-vs-outside 0.28, heterogeneity 0.21; core [0.908, 0.66, 0.46, 0.498] rim [0.732, 0.428, 0.812, 0.032]
  - track 79 at frame 90: holes 0, rim-vs-core 0.71, rim-vs-outside 0.38, heterogeneity 0.23; core [0.975, 0.859, 0.29, 0.467] rim [0.754, 0.58, 0.713, 0.024]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 120 components >= 12 px at frames [17, 33, 50, 67, 83, 100]):
  - radial phi (droplet): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.82, rim/outside 4.5 (aggregate of 120 individuals; 0/120 membrane-like individually; rim level 0.74)
  - radial order |Q|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.766, rim/outside 3.78 (aggregate of 120 individuals; 7/120 membrane-like individually; rim level 0.574)
  - radial surfactant s: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.37, rim/outside 3.31 (aggregate of 120 individuals; 73/120 membrane-like individually; rim level 0.601)
  - radial cargo c: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.406, rim/outside 1.62 (aggregate of 120 individuals; 14/120 membrane-like individually; rim level 0.176)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #19 (t=340, R_eq 3.99): none; #25 (t=350, R_eq 3.19): ['surfactant s']; #20 (t=330, R_eq 4.37): none; #79 (t=450, R_eq 3.43): ['surfactant s']

## Warnings
- radial: 3 of 120 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
