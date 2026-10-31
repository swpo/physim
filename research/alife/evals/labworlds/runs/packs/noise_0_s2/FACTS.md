# Evidence pack: phase-membrane-noise (seed 2)

- world: `../../pm_noise.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_membrane; mutation: additive dynamics noise sd 0.0 per sqrt(t) on ['S', 'K', 'L', 'phi']
- run: 161 frames x 50 steps x dt 1.0 = time 8000; grid [128, 128]; wall 17s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/pm_noise.py --out /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/packs/noise_0_s2 --seeds 2 --frames 160 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5463], min area 6 px

## Measurements
- components: final 15, mean 15.9, max 22; occupancy final 0.28
- tracks: 140; persistent (alive >= 50% of run): 7; longest 120 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 13.77 (1 = constant size)
- enclosures: components with a hole mean 10.16, final 8; holes at thresholds 0.2/0.35/0.5 final [2, 9, 12]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [17, 15, 15], H1 [13, 12, 6]
- motion: 4 long-lived tracks moved >= 1 body length; max speed 0.00743/time; max body lengths 1.6
- replication (lineage window K = 20 frames = time 1000, default): splits 53, persistent splits 9 (0 more failed only because the siblings re-merged within K), max generation 2, merges 7, merge/split ratio 0.132, nucleations 0
- channel total drift (end/start - 1): [-0.4558, -0.7234, -0.0327, -0.3153]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 65 at frame 101: holes 1, rim-vs-core 0.26, rim-vs-outside 0.69, heterogeneity 0.19; core [0.103, 0.739, 0.554, 0.689] rim [0.191, 0.535, 0.476, 0.568]
  - track 85 at frame 106: holes 0, rim-vs-core 0.36, rim-vs-outside 0.85, heterogeneity 0.18; core [0.097, 0.764, 0.527, 0.649] rim [0.277, 0.454, 0.572, 0.693]
  - track 73 at frame 87: holes 1, rim-vs-core 0.15, rim-vs-outside 0.76, heterogeneity 0.16; core [0.078, 0.655, 0.431, 0.726] rim [0.149, 0.574, 0.478, 0.627]
  - track 94 at frame 117: holes 1, rim-vs-core 0.17, rim-vs-outside 0.76, heterogeneity 0.18; core [0.098, 0.726, 0.539, 0.685] rim [0.153, 0.595, 0.492, 0.614]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 99 components >= 12 px at frames [27, 54, 81, 106, 133, 160]):
  - radial S: peak at rho=1.65 (OUTSIDE the peak band 0.5-1.5), rim/core 11.9, rim/outside 0.854 (aggregate of 99 individuals; 0/99 membrane-like individually; rim level 0.466)
  - radial K catalyst: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.04, rim/outside 5.24 (aggregate of 99 individuals; 1/99 membrane-like individually; rim level 0.718)
  - radial L link: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.71, rim/outside 4.19 (aggregate of 99 individuals; 84/99 membrane-like individually; rim level 0.569)  MEMBRANE-LIKE
  - radial membrane (wall): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 2.57, rim/outside 4.27 (aggregate of 99 individuals; 82/99 membrane-like individually; rim level 0.635)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): L link, membrane (wall)
- membrane-like channels per top track at mid-life: #65 (t=5050, R_eq 9.69, ring): ['L link', 'membrane (wall)']; #85 (t=5300, R_eq 7.92): ['L link', 'membrane (wall)']; #73 (t=4350, R_eq 12.8, ring): ['L link', 'membrane (wall)']; #94 (t=5850, R_eq 12.74, ring): ['L link', 'membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 60 of 99 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
