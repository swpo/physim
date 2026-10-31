# Evidence pack: active-nematic-marangoni-noise (seed 1)

- world: `../../mg_noise.py`, family `active-nematic`
- parent: collective/contrib/20261026T0505-c34-nematic-marangoni; mutation: dynamics noise sd 0.0 per sqrt(t): additive on ['phi', 'q1', 'q2', 's', 'c'], proportional on [], conserved (div of white flux) on []
- run: 101 frames x 100 steps x dt 0.05 = time 500; grid [128, 128]; wall 203s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/marangoni/mg_noise.py --out /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/marangoni/packs/b128_base_0_s1 --seeds 1 --frames 100 --size 128 128 --no-movie`
- segmentation: matter > 0.60 of robust range [-0.8102, 0.5444], min area 6 px

## Measurements
- components: final 22, mean 8.7, max 23; occupancy final 0.07
- tracks: 46; persistent (alive >= 50% of run): 0; longest 48 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [25, 23, 22], H1 [1, 0, 0]
- motion: 15 long-lived tracks moved >= 1 body length; max speed 0.333/time; max body lengths 4.7
- replication (lineage window K = 20 frames = time 100, default): splits 20, persistent splits 11 (0 more failed only because the siblings re-merged within K), max generation 3, merges 2, merge/split ratio 0.1, nucleations 4
- channel total drift (end/start - 1): [-0.4915, -0.486, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 3 at frame 49: holes 0, rim-vs-core 0.86, rim-vs-outside 0.40, heterogeneity 0.23; core [0.959, 0.89, 0.484, 0.728] rim [0.772, 0.623, 0.89, 0.045]
  - track 10 at frame 79: holes 0, rim-vs-core 0.75, rim-vs-outside 0.39, heterogeneity 0.22; core [0.95, 0.874, 0.484, 0.63] rim [0.778, 0.626, 0.853, 0.049]
  - track 1 at frame 34: holes 0, rim-vs-core 0.60, rim-vs-outside 0.30, heterogeneity 0.19; core [0.947, 0.578, 0.459, 0.472] rim [0.768, 0.396, 0.78, 0.036]
  - track 22 at frame 87: holes 0, rim-vs-core 1.13, rim-vs-outside 0.44, heterogeneity 0.26; core [0.986, 0.937, 0.378, 0.959] rim [0.799, 0.656, 0.943, 0.04]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 61 components >= 12 px at frames [17, 33, 50, 67, 83, 100]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.793, rim/outside 4.44 (aggregate of 61 individuals; 0/61 membrane-like individually; rim level 0.709)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.814, rim/outside 7.83 (aggregate of 61 individuals; 3/61 membrane-like individually; rim level 0.617)
  - radial surfactant s: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.12, rim/outside 3.21 (aggregate of 61 individuals; 27/61 membrane-like individually; rim level 0.63)
  - radial cargo c: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.485, rim/outside 1.7 (aggregate of 61 individuals; 11/61 membrane-like individually; rim level 0.222)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #3 (t=245, R_eq 4.26): none; #10 (t=395, R_eq 4.44): ['cargo c']; #1 (t=170, R_eq 4.22): ['order |Q|', 'cargo c']; #22 (t=435, R_eq 3.43): ['surfactant s']

## Warnings
- radial: 2 of 61 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
