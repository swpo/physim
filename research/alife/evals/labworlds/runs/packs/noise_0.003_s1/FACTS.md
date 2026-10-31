# Evidence pack: phase-membrane-noise (seed 1)

- world: `../../pm_noise.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_membrane; mutation: additive dynamics noise sd 0.003 per sqrt(t) on ['S', 'K', 'L', 'phi']
- run: 161 frames x 50 steps x dt 1.0 = time 8000; grid [128, 128]; wall 29s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/pm_noise.py --out /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/packs/noise_0.003_s1 --seeds 1 --frames 160 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0063, 1.5314], min area 6 px

## Measurements
- components: final 12, mean 15.2, max 32; occupancy final 0.30
- tracks: 129; persistent (alive >= 50% of run): 4; longest 132 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 29.05 (1 = constant size)
- enclosures: components with a hole mean 10.09, final 10; holes at thresholds 0.2/0.35/0.5 final [3, 10, 10]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [13, 12, 12], H1 [11, 11, 9]
- motion: 5 long-lived tracks moved >= 1 body length; max speed 0.0064/time; max body lengths 1.4
- replication (lineage window K = 20 frames = time 1000, default): splits 43, persistent splits 10 (0 more failed only because the siblings re-merged within K), max generation 2, merges 9, merge/split ratio 0.209, nucleations 2
- channel total drift (end/start - 1): [-0.5061, -0.676, 0.2168, -0.0087]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 51 at frame 69: holes 1, rim-vs-core 0.20, rim-vs-outside 0.69, heterogeneity 0.18; core [0.087, 0.688, 0.475, 0.758] rim [0.153, 0.574, 0.482, 0.603]
  - track 12 at frame 63: holes 1, rim-vs-core 0.18, rim-vs-outside 0.80, heterogeneity 0.19; core [0.097, 0.771, 0.557, 0.643] rim [0.174, 0.613, 0.531, 0.614]
  - track 86 at frame 108: holes 0, rim-vs-core 0.85, rim-vs-outside 0.47, heterogeneity 0.23; core [0.294, 0.854, 0.935, 0.82] rim [0.455, 0.239, 0.453, 0.518]
  - track 101 at frame 134: holes 1, rim-vs-core 0.31, rim-vs-outside 0.80, heterogeneity 0.22; core [0.112, 0.84, 0.624, 0.586] rim [0.223, 0.573, 0.519, 0.581]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 90 components >= 12 px at frames [27, 54, 81, 106, 133, 160]):
  - radial S: peak at rho=1.75 (OUTSIDE the peak band 0.5-1.5), rim/core 10.7, rim/outside 0.838 (aggregate of 90 individuals; 0/90 membrane-like individually; rim level 0.466)
  - radial K catalyst: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.02, rim/outside 5.9 (aggregate of 90 individuals; 0/90 membrane-like individually; rim level 0.714)
  - radial L link: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.59, rim/outside 3.21 (aggregate of 90 individuals; 72/90 membrane-like individually; rim level 0.557)  MEMBRANE-LIKE
  - radial membrane (wall): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 2.2, rim/outside 5.21 (aggregate of 90 individuals; 69/90 membrane-like individually; rim level 0.61)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): L link, membrane (wall)
- membrane-like channels per top track at mid-life: #51 (t=3450, R_eq 12.21, ring): ['L link', 'membrane (wall)']; #12 (t=3150, R_eq 10.48, ring): ['L link', 'membrane (wall)']; #86 (t=5400, R_eq 4.58): ['membrane (wall)']; #101 (t=6700, R_eq 9.47, ring): ['L link', 'membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 55 of 90 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
