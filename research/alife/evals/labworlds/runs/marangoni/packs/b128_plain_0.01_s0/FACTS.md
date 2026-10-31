# Evidence pack: active-nematic-marangoni-noise (seed 0)

- world: `../../mg_noise.py`, family `active-nematic`
- parent: collective/contrib/20261026T0505-c34-nematic-marangoni; mutation: dynamics noise sd 0.01 per sqrt(t): additive on ['phi', 'q1', 'q2', 's', 'c'], proportional on [], conserved (div of white flux) on []
- run: 101 frames x 100 steps x dt 0.05 = time 500; grid [128, 128]; wall 212s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/marangoni/mg_noise.py --out /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/marangoni/packs/b128_plain_0.01_s0 --seeds 0 --frames 100 --size 128 128 --no-movie`
- segmentation: matter > 0.59 of robust range [-0.8355, 0.5744], min area 6 px

## Measurements
- components: final 28, mean 19.8, max 30; occupancy final 0.09
- tracks: 64; persistent (alive >= 50% of run): 14; longest 79 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 13.50 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [30, 30, 28], H1 [0, 0, 0]
- motion: 36 long-lived tracks moved >= 1 body length; max speed 0.271/time; max body lengths 6.1
- replication (lineage window K = 20 frames = time 100, default): splits 23, persistent splits 14 (0 more failed only because the siblings re-merged within K), max generation 2, merges 6, merge/split ratio 0.261, nucleations 13
- channel total drift (end/start - 1): [-0.5036, -0.3993, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 12 at frame 61: holes 0, rim-vs-core 0.75, rim-vs-outside 0.32, heterogeneity 0.24; core [0.954, 0.63, 0.43, 0.497] rim [0.751, 0.41, 0.914, 0.011]
  - track 14 at frame 63: holes 0, rim-vs-core 0.74, rim-vs-outside 0.35, heterogeneity 0.24; core [0.955, 0.69, 0.402, 0.5] rim [0.748, 0.437, 0.873, 0.025]
  - track 15 at frame 63: holes 0, rim-vs-core 0.87, rim-vs-outside 0.39, heterogeneity 0.24; core [0.969, 0.879, 0.354, 0.63] rim [0.772, 0.546, 0.846, 0.029]
  - track 37 at frame 74: holes 0, rim-vs-core 0.87, rim-vs-outside 0.40, heterogeneity 0.24; core [0.964, 0.873, 0.349, 0.61] rim [0.761, 0.548, 0.852, 0.015]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 132 components >= 12 px at frames [17, 33, 50, 67, 83, 100]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.798, rim/outside 4.6 (aggregate of 132 individuals; 0/132 membrane-like individually; rim level 0.714)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.768, rim/outside 8.18 (aggregate of 132 individuals; 8/132 membrane-like individually; rim level 0.508)
  - radial surfactant s: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.26, rim/outside 3.27 (aggregate of 132 individuals; 63/132 membrane-like individually; rim level 0.573)
  - radial cargo c: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.374, rim/outside 1.87 (aggregate of 132 individuals; 20/132 membrane-like individually; rim level 0.126)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #12 (t=305, R_eq 4.22): ['order |Q|', 'cargo c']; #14 (t=315, R_eq 4.33): none; #15 (t=315, R_eq 3.52): ['surfactant s']; #37 (t=370, R_eq 3.43): ['surfactant s']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 5 of 132 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
