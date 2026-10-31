# Evidence pack: active-nematic-marangoni-noise (seed 0)

- world: `../../mg_noise.py`, family `active-nematic`
- parent: collective/contrib/20261026T0505-c34-nematic-marangoni; mutation: dynamics noise sd 0.003 per sqrt(t): additive on ['q1', 'q2'], proportional on ['s', 'c'], conserved (div of white flux) on ['phi']
- run: 101 frames x 100 steps x dt 0.05 = time 500; grid [128, 128]; wall 223s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/marangoni/mg_noise.py --out /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/marangoni/packs/b128_phys_0.003_s0 --seeds 0 --frames 100 --size 128 128 --no-movie`
- segmentation: matter > 0.59 of robust range [-0.8299, 0.5684], min area 6 px

## Measurements
- components: final 29, mean 16.5, max 29; occupancy final 0.09
- tracks: 67; persistent (alive >= 50% of run): 11; longest 73 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 3.29 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [33, 29, 29], H1 [0, 0, 0]
- motion: 30 long-lived tracks moved >= 1 body length; max speed 0.274/time; max body lengths 5.5
- replication (lineage window K = 20 frames = time 100, default): splits 26, persistent splits 14 (0 more failed only because the siblings re-merged within K), max generation 3, merges 6, merge/split ratio 0.231, nucleations 9
- channel total drift (end/start - 1): [-0.5031, -0.4219, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 11 at frame 64: holes 0, rim-vs-core 0.81, rim-vs-outside 0.38, heterogeneity 0.24; core [0.955, 0.913, 0.392, 0.536] rim [0.743, 0.554, 0.857, 0.02]
  - track 12 at frame 64: holes 0, rim-vs-core 0.73, rim-vs-outside 0.32, heterogeneity 0.24; core [0.951, 0.679, 0.432, 0.498] rim [0.749, 0.429, 0.885, 0.02]
  - track 14 at frame 65: holes 0, rim-vs-core 0.76, rim-vs-outside 0.39, heterogeneity 0.24; core [0.948, 0.887, 0.414, 0.463] rim [0.731, 0.562, 0.889, 0.012]
  - track 31 at frame 79: holes 0, rim-vs-core 0.62, rim-vs-outside 0.36, heterogeneity 0.20; core [0.934, 0.815, 0.405, 0.455] rim [0.764, 0.579, 0.744, 0.019]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 117 components >= 12 px at frames [17, 33, 50, 67, 83, 100]):
  - radial phi (droplet): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.807, rim/outside 4.63 (aggregate of 117 individuals; 0/117 membrane-like individually; rim level 0.737)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.749, rim/outside 9.22 (aggregate of 117 individuals; 8/117 membrane-like individually; rim level 0.572)
  - radial surfactant s: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.36, rim/outside 3.3 (aggregate of 117 individuals; 70/117 membrane-like individually; rim level 0.577)
  - radial cargo c: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.378, rim/outside 2.14 (aggregate of 117 individuals; 12/117 membrane-like individually; rim level 0.157)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #11 (t=320, R_eq 3.66): ['surfactant s']; #12 (t=320, R_eq 4.15): ['surfactant s']; #14 (t=325, R_eq 3.74): ['surfactant s']; #31 (t=395, R_eq 4.33): ['cargo c']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 4 of 117 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
