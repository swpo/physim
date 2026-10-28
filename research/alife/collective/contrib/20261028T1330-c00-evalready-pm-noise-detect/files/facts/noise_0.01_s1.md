# Evidence pack: phase-membrane-noise (seed 1)

- world: `../../pm_noise.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_membrane; mutation: additive dynamics noise sd 0.01 per sqrt(t) on ['S', 'K', 'L', 'phi']
- run: 161 frames x 50 steps x dt 1.0 = time 8000; grid [128, 128]; wall 24s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/pm_noise.py --out /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/packs/noise_0.01_s1 --seeds 1 --frames 160 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0133, 1.479], min area 6 px

## Measurements
- components: final 0, mean 2.1, max 55; occupancy final 0.00
- tracks: 110; persistent (alive >= 50% of run): 0; longest 58 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.98, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [265, 88, 6], H1 [237, 42, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.9
- replication (lineage window K = 20 frames = time 1000, default): splits 24, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 16, merge/split ratio 0.667, nucleations 27
- channel total drift (end/start - 1): [-0.2363, -0.8791, 0.5797, -0.9062]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 84 at frame 31: holes 1, rim-vs-core 0.25, rim-vs-outside 0.68, heterogeneity 0.20; core [0.088, 0.833, 0.544, 0.679] rim [0.163, 0.627, 0.461, 0.597]
  - track 109 at frame 78: holes 1, rim-vs-core 0.24, rim-vs-outside 0.68, heterogeneity 0.21; core [0.091, 0.841, 0.562, 0.679] rim [0.155, 0.64, 0.482, 0.605]
  - track 97 at frame 30: holes 1, rim-vs-core 0.27, rim-vs-outside 0.68, heterogeneity 0.21; core [0.092, 0.88, 0.587, 0.649] rim [0.162, 0.656, 0.479, 0.588]
  - track 76 at frame 7: holes 1, rim-vs-core 0.21, rim-vs-outside 0.76, heterogeneity 0.18; core [0.061, 0.812, 0.441, 0.688] rim [0.151, 0.627, 0.463, 0.642]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 6 components >= 12 px at frames [27, 54, 81]):
  - radial S: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 15.8, rim/outside 0.707 (aggregate of 6 individuals; 0/6 membrane-like individually; rim level 0.439)
  - radial K catalyst: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.05, rim/outside 6.52 (aggregate of 6 individuals; 0/6 membrane-like individually; rim level 0.774)
  - radial L link: peak at rho=0.95 (in the peak band 0.5-1.5), rim/core 1.85, rim/outside 1.96 (aggregate of 6 individuals; 6/6 membrane-like individually; rim level 0.546)  MEMBRANE-LIKE
  - radial membrane (wall): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 2.42, rim/outside 23.2 (aggregate of 6 individuals; 5/6 membrane-like individually; rim level 0.702)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): L link, membrane (wall)
- membrane-like channels per top track at mid-life: #84 (t=1550, R_eq 11.26, ring): ['L link', 'membrane (wall)']; #109 (t=3900, R_eq 11.64, ring): ['L link', 'membrane (wall)']; #97 (t=1500, R_eq 11.41, ring): ['L link', 'membrane (wall)']; #76 (t=350, R_eq 10.2, ring): ['L link', 'membrane (wall)']

## Warnings
- no components at the end: matter died out or fell below threshold
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 4 of 6 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
