# Evidence pack: phase-membrane-noise (seed 2)

- world: `../../pm_noise.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_membrane; mutation: dynamics noise sd 0.01 per sqrt(t): additive on ['phi'], multiplicative (sd x value) on ['S', 'K', 'L']
- run: 161 frames x 50 steps x dt 1.0 = time 8000; grid [128, 128]; wall 34s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/pm_noise.py --out /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/packs/mult_0.01_s2 --seeds 2 --frames 160 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5446], min area 6 px

## Measurements
- components: final 15, mean 15.3, max 37; occupancy final 0.30
- tracks: 156; persistent (alive >= 50% of run): 4; longest 106 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 9.75 (1 = constant size)
- enclosures: components with a hole mean 9.87, final 12; holes at thresholds 0.2/0.35/0.5 final [1, 12, 14]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [15, 15, 15], H1 [16, 16, 10]
- motion: 3 long-lived tracks moved >= 1 body length; max speed 0.00723/time; max body lengths 1.4
- replication (lineage window K = 20 frames = time 1000, default): splits 57, persistent splits 8 (0 more failed only because the siblings re-merged within K), max generation 2, merges 6, merge/split ratio 0.105, nucleations 11
- channel total drift (end/start - 1): [-0.4487, -0.69, -0.0231, -0.2493]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 64 at frame 65: holes 1, rim-vs-core 0.15, rim-vs-outside 0.79, heterogeneity 0.18; core [0.088, 0.716, 0.492, 0.678] rim [0.16, 0.598, 0.498, 0.62]
  - track 63 at frame 62: holes 0, rim-vs-core 0.48, rim-vs-outside 0.88, heterogeneity 0.21; core [0.099, 0.829, 0.572, 0.542] rim [0.325, 0.439, 0.567, 0.715]
  - track 92 at frame 106: holes 1, rim-vs-core 0.31, rim-vs-outside 0.80, heterogeneity 0.22; core [0.125, 0.84, 0.652, 0.621] rim [0.214, 0.581, 0.509, 0.576]
  - track 124 at frame 134: holes 1, rim-vs-core 0.31, rim-vs-outside 0.72, heterogeneity 0.21; core [0.118, 0.813, 0.631, 0.627] rim [0.206, 0.563, 0.488, 0.57]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 93 components >= 12 px at frames [27, 54, 81, 106, 133, 160]):
  - radial S: peak at rho=1.65 (OUTSIDE the peak band 0.5-1.5), rim/core 15.7, rim/outside 0.857 (aggregate of 93 individuals; 0/93 membrane-like individually; rim level 0.47)
  - radial K catalyst: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.05, rim/outside 4.72 (aggregate of 93 individuals; 0/93 membrane-like individually; rim level 0.728)
  - radial L link: peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.77, rim/outside 3.88 (aggregate of 93 individuals; 85/93 membrane-like individually; rim level 0.567)  MEMBRANE-LIKE
  - radial membrane (wall): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 2.92, rim/outside 3.58 (aggregate of 93 individuals; 83/93 membrane-like individually; rim level 0.632)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): L link, membrane (wall)
- membrane-like channels per top track at mid-life: #64 (t=3250, R_eq 11.41, ring): ['L link', 'membrane (wall)']; #63 (t=3100, R_eq 8.74): ['L link', 'membrane (wall)']; #92 (t=5300, R_eq 8.94, ring): ['L link', 'membrane (wall)']; #124 (t=6700, R_eq 9.89, ring): ['L link', 'membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 65 of 93 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
