# Evidence pack: active-nematic-marangoni-noise (seed 1)

- world: `../../mg_noise.py`, family `active-nematic`
- parent: collective/contrib/20261026T0505-c34-nematic-marangoni; mutation: dynamics noise sd 0.003 per sqrt(t): additive on ['phi', 'q1', 'q2', 's', 'c'], proportional on [], conserved (div of white flux) on []
- run: 101 frames x 100 steps x dt 0.05 = time 500; grid [128, 128]; wall 209s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/marangoni/mg_noise.py --out /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/marangoni/packs/b128_plain_0.003_s1 --seeds 1 --frames 100 --size 128 128 --no-movie`
- segmentation: matter > 0.60 of robust range [-0.8186, 0.5471], min area 6 px

## Measurements
- components: final 27, mean 11.0, max 27; occupancy final 0.08
- tracks: 56; persistent (alive >= 50% of run): 0; longest 48 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [28, 28, 26], H1 [0, 0, 0]
- motion: 20 long-lived tracks moved >= 1 body length; max speed 0.357/time; max body lengths 4.8
- replication (lineage window K = 20 frames = time 100, default): splits 25, persistent splits 14 (0 more failed only because the siblings re-merged within K), max generation 3, merges 2, merge/split ratio 0.08, nucleations 4
- channel total drift (end/start - 1): [-0.4923, -0.4502, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 13 at frame 69: holes 0, rim-vs-core 0.69, rim-vs-outside 0.48, heterogeneity 0.24; core [0.97, 0.869, 0.417, 0.621] rim [0.804, 0.579, 0.807, 0.157]
  - track 16 at frame 78: holes 0, rim-vs-core 0.80, rim-vs-outside 0.34, heterogeneity 0.22; core [0.942, 0.765, 0.463, 0.659] rim [0.759, 0.507, 0.843, 0.027]
  - track 19 at frame 78: holes 0, rim-vs-core 0.63, rim-vs-outside 0.41, heterogeneity 0.23; core [0.94, 0.786, 0.486, 0.573] rim [0.793, 0.576, 0.832, 0.113]
  - track 20 at frame 81: holes 0, rim-vs-core 0.81, rim-vs-outside 0.53, heterogeneity 0.26; core [0.97, 0.895, 0.373, 0.841] rim [0.825, 0.688, 0.776, 0.184]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 81 components >= 12 px at frames [17, 33, 50, 67, 83, 100]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.801, rim/outside 4.63 (aggregate of 81 individuals; 0/81 membrane-like individually; rim level 0.738)
  - radial order |Q|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.763, rim/outside 8.83 (aggregate of 81 individuals; 3/81 membrane-like individually; rim level 0.625)
  - radial surfactant s: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.4, rim/outside 3.25 (aggregate of 81 individuals; 47/81 membrane-like individually; rim level 0.65)
  - radial cargo c: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.39, rim/outside 1.77 (aggregate of 81 individuals; 5/81 membrane-like individually; rim level 0.2)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #13 (t=345, R_eq 3.95): none; #16 (t=390, R_eq 4.37): ['cargo c']; #19 (t=390, R_eq 4.51): ['cargo c']; #20 (t=405, R_eq 3.39): ['surfactant s']

## Warnings
- radial: 2 of 81 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
