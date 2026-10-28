# Evidence pack: phase-membrane-noise (seed 1)

- world: `../../pm_noise.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_membrane; mutation: additive dynamics noise sd 0.0 per sqrt(t) on ['S', 'K', 'L', 'phi']
- run: 161 frames x 50 steps x dt 1.0 = time 8000; grid [128, 128]; wall 18s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/pm_noise.py --out /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/packs/noise_0_s1 --seeds 1 --frames 160 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5365], min area 6 px

## Measurements
- components: final 15, mean 16.2, max 27; occupancy final 0.28
- tracks: 163; persistent (alive >= 50% of run): 2; longest 90 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 9.61 (1 = constant size)
- enclosures: components with a hole mean 10.82, final 4; holes at thresholds 0.2/0.35/0.5 final [3, 4, 8]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [15, 15, 15], H1 [17, 10, 4]
- motion: 6 long-lived tracks moved >= 1 body length; max speed 0.0248/time; max body lengths 1.2
- replication (lineage window K = 20 frames = time 1000, default): splits 62, persistent splits 7 (0 more failed only because the siblings re-merged within K), max generation 2, merges 12, merge/split ratio 0.194, nucleations 0
- channel total drift (end/start - 1): [-0.4553, -0.733, -0.045, -0.0397]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 53 at frame 47: holes 1, rim-vs-core 0.18, rim-vs-outside 0.75, heterogeneity 0.18; core [0.097, 0.746, 0.553, 0.684] rim [0.147, 0.602, 0.494, 0.612]
  - track 88 at frame 94: holes 0, rim-vs-core 0.54, rim-vs-outside 0.99, heterogeneity 0.22; core [0.095, 0.869, 0.58, 0.474] rim [0.319, 0.467, 0.593, 0.755]
  - track 77 at frame 62: holes 1, rim-vs-core 0.18, rim-vs-outside 0.82, heterogeneity 0.19; core [0.098, 0.778, 0.558, 0.632] rim [0.164, 0.618, 0.519, 0.609]
  - track 81 at frame 56: holes 1, rim-vs-core 0.19, rim-vs-outside 0.82, heterogeneity 0.19; core [0.095, 0.769, 0.541, 0.628] rim [0.168, 0.602, 0.512, 0.61]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 100 components >= 12 px at frames [27, 54, 81, 106, 133, 160]):
  - radial S: peak at rho=1.65 (OUTSIDE the peak band 0.5-1.5), rim/core 11.1, rim/outside 0.874 (aggregate of 100 individuals; 0/100 membrane-like individually; rim level 0.459)
  - radial K catalyst: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.03, rim/outside 5.02 (aggregate of 100 individuals; 0/100 membrane-like individually; rim level 0.71)
  - radial L link: peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.65, rim/outside 3.91 (aggregate of 100 individuals; 81/100 membrane-like individually; rim level 0.558)  MEMBRANE-LIKE
  - radial membrane (wall): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 2.47, rim/outside 3.99 (aggregate of 100 individuals; 80/100 membrane-like individually; rim level 0.638)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): L link, membrane (wall)
- membrane-like channels per top track at mid-life: #53 (t=2350, R_eq 13.91, ring): ['L link', 'membrane (wall)']; #88 (t=4700, R_eq 8.12): ['L link', 'membrane (wall)']; #77 (t=3100, R_eq 10.97, ring): ['L link', 'membrane (wall)']; #81 (t=2800, R_eq 11.23, ring): ['L link', 'membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 63 of 100 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
