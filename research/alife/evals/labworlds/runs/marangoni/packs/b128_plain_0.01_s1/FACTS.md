# Evidence pack: active-nematic-marangoni-noise (seed 1)

- world: `../../mg_noise.py`, family `active-nematic`
- parent: collective/contrib/20261026T0505-c34-nematic-marangoni; mutation: dynamics noise sd 0.01 per sqrt(t): additive on ['phi', 'q1', 'q2', 's', 'c'], proportional on [], conserved (div of white flux) on []
- run: 101 frames x 100 steps x dt 0.05 = time 500; grid [128, 128]; wall 209s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/marangoni/mg_noise.py --out /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/marangoni/packs/b128_plain_0.01_s1 --seeds 1 --frames 100 --size 128 128 --no-movie`
- segmentation: matter > 0.60 of robust range [-0.8168, 0.5487], min area 6 px

## Measurements
- components: final 24, mean 11.5, max 24; occupancy final 0.09
- tracks: 43; persistent (alive >= 50% of run): 3; longest 55 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 3.12 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [28, 24, 24], H1 [0, 0, 0]
- motion: 26 long-lived tracks moved >= 1 body length; max speed 0.301/time; max body lengths 7.3
- replication (lineage window K = 20 frames = time 100, default): splits 19, persistent splits 15 (0 more failed only because the siblings re-merged within K), max generation 4, merges 0, merge/split ratio 0, nucleations 5
- channel total drift (end/start - 1): [-0.4939, -0.3954, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 13 at frame 73: holes 0, rim-vs-core 0.83, rim-vs-outside 0.41, heterogeneity 0.24; core [0.969, 0.929, 0.37, 0.643] rim [0.78, 0.629, 0.815, 0.036]
  - track 14 at frame 73: holes 0, rim-vs-core 0.79, rim-vs-outside 0.37, heterogeneity 0.23; core [0.968, 0.788, 0.409, 0.606] rim [0.775, 0.535, 0.842, 0.03]
  - track 16 at frame 74: holes 0, rim-vs-core 0.77, rim-vs-outside 0.34, heterogeneity 0.25; core [0.971, 0.723, 0.46, 0.498] rim [0.764, 0.459, 0.95, 0.015]
  - track 31 at frame 87: holes 0, rim-vs-core 0.81, rim-vs-outside 0.43, heterogeneity 0.23; core [0.976, 0.935, 0.356, 0.633] rim [0.774, 0.656, 0.774, 0.027]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 80 components >= 12 px at frames [17, 33, 50, 67, 83, 100]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.791, rim/outside 4.41 (aggregate of 80 individuals; 0/80 membrane-like individually; rim level 0.708)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.788, rim/outside 7.52 (aggregate of 80 individuals; 5/80 membrane-like individually; rim level 0.573)
  - radial surfactant s: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.19, rim/outside 3.12 (aggregate of 80 individuals; 38/80 membrane-like individually; rim level 0.606)
  - radial cargo c: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.447, rim/outside 1.83 (aggregate of 80 individuals; 12/80 membrane-like individually; rim level 0.185)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #13 (t=365, R_eq 3.19): ['surfactant s']; #14 (t=365, R_eq 4.37): none; #16 (t=370, R_eq 4.85): none; #31 (t=435, R_eq 3.78): ['surfactant s']

## Warnings
- radial: 2 of 80 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
