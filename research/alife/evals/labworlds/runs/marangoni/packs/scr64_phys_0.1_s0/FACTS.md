# Evidence pack: active-nematic-marangoni-noise (seed 0)

- world: `../../mg_noise.py`, family `active-nematic`
- parent: collective/contrib/20261026T0505-c34-nematic-marangoni; mutation: dynamics noise sd 0.1 per sqrt(t): additive on ['q1', 'q2'], proportional on ['s', 'c'], conserved (div of white flux) on ['phi']
- run: 101 frames x 100 steps x dt 0.05 = time 500; grid [64, 64]; wall 59s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/marangoni/mg_noise.py --out /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/marangoni/packs/scr64_phys_0.1_s0 --seeds 0 --frames 100 --size 64 64 --no-movie`
- segmentation: matter > 0.59 of robust range [-0.8444, 0.5951], min area 6 px

## Measurements
- components: final 7, mean 5.9, max 9; occupancy final 0.09
- tracks: 21; persistent (alive >= 50% of run): 4; longest 75 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 7.67 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [7, 7, 7], H1 [0, 0, 0]
- motion: 9 long-lived tracks moved >= 1 body length; max speed 0.348/time; max body lengths 6.7
- replication (lineage window K = 20 frames = time 100, default): splits 7, persistent splits 3 (0 more failed only because the siblings re-merged within K), max generation 1, merges 3, merge/split ratio 0.429, nucleations 4
- channel total drift (end/start - 1): [-0.4868, 0.3837, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 5 at frame 63: holes 0, rim-vs-core 0.71, rim-vs-outside 0.34, heterogeneity 0.23; core [0.935, 0.798, 0.389, 0.511] rim [0.75, 0.503, 0.761, 0.022]
  - track 3 at frame 61: holes 0, rim-vs-core 0.76, rim-vs-outside 0.29, heterogeneity 0.25; core [0.947, 0.607, 0.382, 0.488] rim [0.734, 0.329, 0.862, 0.018]
  - track 7 at frame 63: holes 0, rim-vs-core 0.60, rim-vs-outside 0.41, heterogeneity 0.24; core [0.93, 0.801, 0.385, 0.517] rim [0.775, 0.55, 0.71, 0.101]
  - track 4 at frame 52: holes 0, rim-vs-core 0.69, rim-vs-outside 0.33, heterogeneity 0.24; core [0.948, 0.676, 0.373, 0.486] rim [0.751, 0.465, 0.821, 0.044]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 40 components >= 12 px at frames [17, 33, 50, 67, 83, 100]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.796, rim/outside 4.63 (aggregate of 40 individuals; 0/40 membrane-like individually; rim level 0.74)
  - radial order |Q|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.716, rim/outside 3.99 (aggregate of 40 individuals; 0/40 membrane-like individually; rim level 0.564)
  - radial surfactant s: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.59, rim/outside 3.48 (aggregate of 40 individuals; 30/40 membrane-like individually; rim level 0.597)  MEMBRANE-LIKE
  - radial cargo c: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.35, rim/outside 1.49 (aggregate of 40 individuals; 1/40 membrane-like individually; rim level 0.139)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): surfactant s
- membrane-like channels per top track at mid-life: #5 (t=315, R_eq 3.78): ['surfactant s']; #3 (t=305, R_eq 4.03): ['order |Q|']; #7 (t=315, R_eq 3.74): ['surfactant s']; #4 (t=260, R_eq 4.41): ['surfactant s']

## Warnings
- radial: 1 of 40 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
