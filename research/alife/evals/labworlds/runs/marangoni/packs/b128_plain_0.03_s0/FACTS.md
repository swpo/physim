# Evidence pack: active-nematic-marangoni-noise (seed 0)

- world: `../../mg_noise.py`, family `active-nematic`
- parent: collective/contrib/20261026T0505-c34-nematic-marangoni; mutation: dynamics noise sd 0.03 per sqrt(t): additive on ['phi', 'q1', 'q2', 's', 'c'], proportional on [], conserved (div of white flux) on []
- run: 101 frames x 100 steps x dt 0.05 = time 500; grid [128, 128]; wall 204s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/marangoni/mg_noise.py --out /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/marangoni/packs/b128_plain_0.03_s0 --seeds 0 --frames 100 --size 128 128 --no-movie`
- segmentation: matter > 0.59 of robust range [-0.8382, 0.576], min area 6 px

## Measurements
- components: final 29, mean 22.1, max 29; occupancy final 0.09
- tracks: 56; persistent (alive >= 50% of run): 18; longest 89 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 12.43 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [30, 29, 29], H1 [0, 0, 0]
- motion: 35 long-lived tracks moved >= 1 body length; max speed 0.287/time; max body lengths 10.1
- replication (lineage window K = 20 frames = time 100, default): splits 16, persistent splits 10 (0 more failed only because the siblings re-merged within K), max generation 2, merges 5, merge/split ratio 0.312, nucleations 19
- channel total drift (end/start - 1): [-0.5046, -0.319, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 9 at frame 56: holes 0, rim-vs-core 0.67, rim-vs-outside 0.30, heterogeneity 0.24; core [0.949, 0.523, 0.45, 0.457] rim [0.758, 0.351, 0.89, 0.021]
  - track 10 at frame 58: holes 0, rim-vs-core 0.67, rim-vs-outside 0.42, heterogeneity 0.29; core [0.968, 0.672, 0.355, 0.418] rim [0.775, 0.564, 0.87, 0.048]
  - track 13 at frame 58: holes 0, rim-vs-core 0.76, rim-vs-outside 0.35, heterogeneity 0.27; core [0.968, 0.659, 0.43, 0.427] rim [0.743, 0.391, 0.965, 0.024]
  - track 49 at frame 87: holes 0, rim-vs-core 0.63, rim-vs-outside 0.29, heterogeneity 0.20; core [0.938, 0.562, 0.441, 0.372] rim [0.765, 0.359, 0.887, 0.012]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 146 components >= 12 px at frames [17, 33, 50, 67, 83, 100]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.82, rim/outside 4.34 (aggregate of 146 individuals; 2/146 membrane-like individually; rim level 0.714)
  - radial order |Q|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.779, rim/outside 6.33 (aggregate of 146 individuals; 20/146 membrane-like individually; rim level 0.492)
  - radial surfactant s: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.22, rim/outside 3.01 (aggregate of 146 individuals; 69/146 membrane-like individually; rim level 0.561)
  - radial cargo c: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.46, rim/outside 1.53 (aggregate of 146 individuals; 34/146 membrane-like individually; rim level 0.125)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #9 (t=280, R_eq 4.75): ['order |Q|', 'cargo c']; #10 (t=290, R_eq 5.08): ['surfactant s']; #13 (t=290, R_eq 4.18): none; #49 (t=435, R_eq 4.44, ring): ['order |Q|', 'cargo c']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 6 of 146 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
