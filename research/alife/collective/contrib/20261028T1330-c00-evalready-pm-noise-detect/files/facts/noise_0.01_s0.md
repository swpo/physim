# Evidence pack: phase-membrane-noise (seed 0)

- world: `../../pm_noise.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_membrane; mutation: additive dynamics noise sd 0.01 per sqrt(t) on ['S', 'K', 'L', 'phi']
- run: 161 frames x 50 steps x dt 1.0 = time 8000; grid [128, 128]; wall 23s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/pm_noise.py --out /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/packs/noise_0.01_s0 --seeds 0 --frames 160 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0134, 1.469], min area 6 px

## Measurements
- components: final 0, mean 1.3, max 35; occupancy final 0.00
- tracks: 75; persistent (alive >= 50% of run): 0; longest 49 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.57, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [255, 74, 1], H1 [231, 44, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 1.0
- replication (lineage window K = 20 frames = time 1000, default): splits 17, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 5, merge/split ratio 0.294, nucleations 16
- channel total drift (end/start - 1): [-0.2376, -0.8778, 0.5774, -0.9224]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 52 at frame 27: holes 1, rim-vs-core 0.26, rim-vs-outside 0.72, heterogeneity 0.21; core [0.08, 0.884, 0.521, 0.637] rim [0.17, 0.646, 0.479, 0.608]
  - track 63 at frame 32: holes 1, rim-vs-core 0.24, rim-vs-outside 0.72, heterogeneity 0.21; core [0.082, 0.898, 0.557, 0.617] rim [0.154, 0.684, 0.492, 0.601]
  - track 48 at frame 7: holes 1, rim-vs-core 0.22, rim-vs-outside 0.73, heterogeneity 0.18; core [0.045, 0.783, 0.425, 0.634] rim [0.138, 0.589, 0.461, 0.646]
  - track 55 at frame 9: holes 0, rim-vs-core 0.34, rim-vs-outside 0.62, heterogeneity 0.18; core [0.061, 0.773, 0.41, 0.702] rim [0.231, 0.502, 0.482, 0.632]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 3 components >= 12 px at frames [27, 54]):
  - radial S: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 34.6, rim/outside 0.72 (aggregate of 3 individuals; 0/3 membrane-like individually; rim level 0.469)
  - radial K catalyst: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.09, rim/outside 6.74 (aggregate of 3 individuals; 0/3 membrane-like individually; rim level 0.808)
  - radial L link: peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 2.31, rim/outside 2.1 (aggregate of 3 individuals; 3/3 membrane-like individually; rim level 0.587)  MEMBRANE-LIKE
  - radial membrane (wall): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 4.12, rim/outside 24.2 (aggregate of 3 individuals; 3/3 membrane-like individually; rim level 0.758)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): L link, membrane (wall)
- membrane-like channels per top track at mid-life: #52 (t=1350, R_eq 10.75, ring): ['L link', 'membrane (wall)']; #63 (t=1600, R_eq 11.16, ring): ['L link', 'membrane (wall)']; #48 (t=350, R_eq 11.9, ring): ['membrane (wall)']; #55 (t=450, R_eq 9.44): ['L link', 'membrane (wall)']

## Warnings
- no components at the end: matter died out or fell below threshold
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 2 of 3 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
