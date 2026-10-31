# Evidence pack: phase-membrane-noise (seed 1)

- world: `../../pm_noise.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_membrane; mutation: dynamics noise sd 0.01 per sqrt(t): additive on ['phi'], multiplicative (sd x value) on ['S', 'K', 'L']
- run: 161 frames x 50 steps x dt 1.0 = time 8000; grid [128, 128]; wall 32s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/pm_noise.py --out /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/packs/mult_0.01_s1 --seeds 1 --frames 160 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5412], min area 6 px

## Measurements
- components: final 16, mean 16.3, max 65; occupancy final 0.30
- tracks: 204; persistent (alive >= 50% of run): 5; longest 124 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 6.34 (1 = constant size)
- enclosures: components with a hole mean 10.27, final 11; holes at thresholds 0.2/0.35/0.5 final [0, 11, 15]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [17, 16, 16], H1 [17, 15, 9]
- motion: 5 long-lived tracks moved >= 1 body length; max speed 0.0103/time; max body lengths 1.3
- replication (lineage window K = 20 frames = time 1000, default): splits 66, persistent splits 10 (0 more failed only because the siblings re-merged within K), max generation 3, merges 12, merge/split ratio 0.182, nucleations 26
- channel total drift (end/start - 1): [-0.4464, -0.7053, -0.0053, -0.0108]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 26 at frame 63: holes 1, rim-vs-core 0.17, rim-vs-outside 0.78, heterogeneity 0.18; core [0.09, 0.718, 0.509, 0.713] rim [0.154, 0.612, 0.504, 0.604]
  - track 136 at frame 109: holes 1, rim-vs-core 0.28, rim-vs-outside 0.75, heterogeneity 0.19; core [0.114, 0.784, 0.598, 0.674] rim [0.196, 0.555, 0.493, 0.596]
  - track 119 at frame 89: holes 1, rim-vs-core 0.34, rim-vs-outside 0.78, heterogeneity 0.22; core [0.116, 0.864, 0.641, 0.571] rim [0.229, 0.569, 0.508, 0.583]
  - track 170 at frame 138: holes 1, rim-vs-core 0.19, rim-vs-outside 0.78, heterogeneity 0.19; core [0.105, 0.793, 0.594, 0.628] rim [0.164, 0.63, 0.526, 0.604]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 93 components >= 12 px at frames [27, 54, 81, 106, 133, 160]):
  - radial S: peak at rho=1.65 (OUTSIDE the peak band 0.5-1.5), rim/core 11.6, rim/outside 0.858 (aggregate of 93 individuals; 0/93 membrane-like individually; rim level 0.489)
  - radial K catalyst: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.04, rim/outside 5.84 (aggregate of 93 individuals; 1/93 membrane-like individually; rim level 0.728)
  - radial L link: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.65, rim/outside 4.56 (aggregate of 93 individuals; 70/93 membrane-like individually; rim level 0.572)  MEMBRANE-LIKE
  - radial membrane (wall): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 2.52, rim/outside 4.2 (aggregate of 93 individuals; 76/93 membrane-like individually; rim level 0.63)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): L link, membrane (wall)
- membrane-like channels per top track at mid-life: #26 (t=3150, R_eq 12.18, ring): ['L link', 'membrane (wall)']; #136 (t=5450, R_eq 9.66, ring): ['L link', 'membrane (wall)']; #119 (t=4450, R_eq 9.44, ring): ['L link', 'membrane (wall)']; #170 (t=6900, R_eq 11.3, ring): ['L link', 'membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 61 of 93 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
