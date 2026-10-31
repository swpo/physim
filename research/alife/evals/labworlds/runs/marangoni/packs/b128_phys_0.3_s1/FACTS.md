# Evidence pack: active-nematic-marangoni-noise (seed 1)

- world: `../../mg_noise.py`, family `active-nematic`
- parent: collective/contrib/20261026T0505-c34-nematic-marangoni; mutation: dynamics noise sd 0.3 per sqrt(t): additive on ['q1', 'q2'], proportional on ['s', 'c'], conserved (div of white flux) on ['phi']
- run: 101 frames x 100 steps x dt 0.05 = time 500; grid [128, 128]; wall 207s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/marangoni/mg_noise.py --out /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/marangoni/packs/b128_phys_0.3_s1 --seeds 1 --frames 100 --size 128 128 --no-movie`
- segmentation: matter > 0.56 of robust range [-0.8876, 0.7109], min area 6 px

## Measurements
- components: final 28, mean 30.4, max 40; occupancy final 0.06
- tracks: 220; persistent (alive >= 50% of run): 11; longest 91 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 7.14 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [34, 28, 26], H1 [23, 0, 0]
- motion: 52 long-lived tracks moved >= 1 body length; max speed 0.384/time; max body lengths 10.0
- replication (lineage window K = 20 frames = time 100, default): splits 55, persistent splits 3 (0 more failed only because the siblings re-merged within K), max generation 1, merges 40, merge/split ratio 0.727, nucleations 75
- channel total drift (end/start - 1): [-0.4915, 1.9288, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 22 at frame 53: holes 0, rim-vs-core 0.53, rim-vs-outside 0.24, heterogeneity 0.21; core [0.866, 0.552, 0.369, 0.498] rim [0.732, 0.518, 0.659, 0.08]
  - track 5 at frame 48: holes 0, rim-vs-core 0.59, rim-vs-outside 0.27, heterogeneity 0.22; core [0.863, 0.486, 0.33, 0.644] rim [0.731, 0.396, 0.565, 0.133]
  - track 11 at frame 49: holes 0, rim-vs-core 0.72, rim-vs-outside 0.30, heterogeneity 0.26; core [0.942, 0.581, 0.416, 0.56] rim [0.744, 0.382, 0.877, 0.089]
  - track 106 at frame 78: holes 0, rim-vs-core 0.50, rim-vs-outside 0.29, heterogeneity 0.20; core [0.906, 0.722, 0.271, 0.324] rim [0.707, 0.523, 0.564, 0.026]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 185 components >= 12 px at frames [17, 33, 50, 67, 83, 100]):
  - radial phi (droplet): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.821, rim/outside 3.83 (aggregate of 185 individuals; 0/185 membrane-like individually; rim level 0.752)
  - radial order |Q|: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.834, rim/outside 1.59 (aggregate of 185 individuals; 26/185 membrane-like individually; rim level 0.494)
  - radial surfactant s: peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.93, rim/outside 3.28 (aggregate of 185 individuals; 148/185 membrane-like individually; rim level 0.491)  MEMBRANE-LIKE
  - radial cargo c: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.323, rim/outside 0.767 (aggregate of 185 individuals; 4/185 membrane-like individually; rim level 0.164)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): surfactant s
- membrane-like channels per top track at mid-life: #22 (t=265, R_eq 3.09): ['order |Q|', 'surfactant s']; #5 (t=240, R_eq 3.39): ['surfactant s']; #11 (t=245, R_eq 3.48): ['surfactant s']; #106 (t=390, R_eq 3.29): ['surfactant s']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 1 of 185 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
