# Evidence pack: phase-membrane-noise (seed 0)

- world: `../../pm_noise.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_membrane; mutation: additive dynamics noise sd 0.001 per sqrt(t) on ['S', 'K', 'L', 'phi']
- run: 161 frames x 50 steps x dt 1.0 = time 8000; grid [128, 128]; wall 31s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/pm_noise.py --out /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/packs/noise_0.001_s0 --seeds 0 --frames 160 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0024, 1.5396], min area 6 px

## Measurements
- components: final 15, mean 13.7, max 26; occupancy final 0.31
- tracks: 154; persistent (alive >= 50% of run): 4; longest 91 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 10.79 (1 = constant size)
- enclosures: components with a hole mean 8.91, final 11; holes at thresholds 0.2/0.35/0.5 final [2, 12, 13]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [16, 15, 15], H1 [15, 14, 9]
- motion: 4 long-lived tracks moved >= 1 body length; max speed 0.0121/time; max body lengths 1.6
- replication (lineage window K = 20 frames = time 1000, default): splits 55, persistent splits 9 (0 more failed only because the siblings re-merged within K), max generation 3, merges 9, merge/split ratio 0.164, nucleations 0
- channel total drift (end/start - 1): [-0.4981, -0.6944, 0.0993, -0.1637]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 93 at frame 116: holes 0, rim-vs-core 0.81, rim-vs-outside 0.55, heterogeneity 0.23; core [0.245, 0.888, 0.884, 0.753] rim [0.43, 0.265, 0.432, 0.566]
  - track 95 at frame 120: holes 1, rim-vs-core 0.28, rim-vs-outside 0.76, heterogeneity 0.20; core [0.108, 0.812, 0.604, 0.624] rim [0.214, 0.572, 0.515, 0.59]
  - track 82 at frame 98: holes 1, rim-vs-core 0.15, rim-vs-outside 0.84, heterogeneity 0.18; core [0.071, 0.668, 0.427, 0.707] rim [0.159, 0.604, 0.501, 0.625]
  - track 130 at frame 138: holes 1, rim-vs-core 0.18, rim-vs-outside 0.82, heterogeneity 0.18; core [0.092, 0.743, 0.519, 0.66] rim [0.173, 0.593, 0.513, 0.614]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 84 components >= 12 px at frames [27, 54, 81, 106, 133, 160]):
  - radial S: peak at rho=1.65 (OUTSIDE the peak band 0.5-1.5), rim/core 9.04, rim/outside 0.829 (aggregate of 84 individuals; 0/84 membrane-like individually; rim level 0.444)
  - radial K catalyst: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1, rim/outside 5.41 (aggregate of 84 individuals; 0/84 membrane-like individually; rim level 0.673)
  - radial L link: peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.5, rim/outside 3.54 (aggregate of 84 individuals; 62/84 membrane-like individually; rim level 0.518)  MEMBRANE-LIKE
  - radial membrane (wall): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.82, rim/outside 4.21 (aggregate of 84 individuals; 60/84 membrane-like individually; rim level 0.563)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): L link, membrane (wall)
- membrane-like channels per top track at mid-life: #93 (t=5800, R_eq 5.11): ['membrane (wall)']; #95 (t=6000, R_eq 9.25, ring): ['L link', 'membrane (wall)']; #82 (t=4900, R_eq 10.66, ring): ['L link', 'membrane (wall)']; #130 (t=6900, R_eq 10.65, ring): ['L link', 'membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 47 of 84 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
