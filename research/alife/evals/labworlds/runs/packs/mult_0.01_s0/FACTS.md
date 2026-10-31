# Evidence pack: phase-membrane-noise (seed 0)

- world: `../../pm_noise.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_membrane; mutation: dynamics noise sd 0.01 per sqrt(t): additive on ['phi'], multiplicative (sd x value) on ['S', 'K', 'L']
- run: 161 frames x 50 steps x dt 1.0 = time 8000; grid [128, 128]; wall 33s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/pm_noise.py --out /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/packs/mult_0.01_s0 --seeds 0 --frames 160 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5452], min area 6 px

## Measurements
- components: final 15, mean 13.6, max 45; occupancy final 0.27
- tracks: 172; persistent (alive >= 50% of run): 1; longest 82 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 4.11 (1 = constant size)
- enclosures: components with a hole mean 8.70, final 11; holes at thresholds 0.2/0.35/0.5 final [0, 11, 12]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [16, 15, 15], H1 [15, 13, 9]
- motion: 3 long-lived tracks moved >= 1 body length; max speed 0.00924/time; max body lengths 1.4
- replication (lineage window K = 20 frames = time 1000, default): splits 58, persistent splits 8 (0 more failed only because the siblings re-merged within K), max generation 2, merges 7, merge/split ratio 0.121, nucleations 18
- channel total drift (end/start - 1): [-0.4443, -0.7229, -0.0541, -0.2455]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 97 at frame 93: holes 1, rim-vs-core 0.19, rim-vs-outside 0.82, heterogeneity 0.18; core [0.096, 0.757, 0.53, 0.646] rim [0.173, 0.593, 0.506, 0.617]
  - track 124 at frame 120: holes 0, rim-vs-core 0.61, rim-vs-outside 0.42, heterogeneity 0.16; core [0.189, 0.73, 0.681, 0.874] rim [0.323, 0.367, 0.528, 0.434]
  - track 91 at frame 73: holes 1, rim-vs-core 0.17, rim-vs-outside 0.74, heterogeneity 0.18; core [0.087, 0.702, 0.487, 0.705] rim [0.157, 0.591, 0.487, 0.597]
  - track 94 at frame 78: holes 1, rim-vs-core 0.27, rim-vs-outside 0.76, heterogeneity 0.22; core [0.113, 0.832, 0.626, 0.599] rim [0.208, 0.604, 0.515, 0.571]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 81 components >= 12 px at frames [27, 54, 81, 106, 133, 160]):
  - radial S: peak at rho=1.65 (OUTSIDE the peak band 0.5-1.5), rim/core 11.6, rim/outside 0.832 (aggregate of 81 individuals; 0/81 membrane-like individually; rim level 0.463)
  - radial K catalyst: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.08, rim/outside 4.9 (aggregate of 81 individuals; 1/81 membrane-like individually; rim level 0.712)
  - radial L link: peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.74, rim/outside 3.94 (aggregate of 81 individuals; 67/81 membrane-like individually; rim level 0.555)  MEMBRANE-LIKE
  - radial membrane (wall): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 2.9, rim/outside 3.75 (aggregate of 81 individuals; 68/81 membrane-like individually; rim level 0.61)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): L link, membrane (wall)
- membrane-like channels per top track at mid-life: #97 (t=4650, R_eq 10.76, ring): ['L link', 'membrane (wall)']; #124 (t=6000, R_eq 5.94): none; #91 (t=3650, R_eq 12.79, ring): ['L link', 'membrane (wall)']; #94 (t=3900, R_eq 9.64, ring): ['L link', 'membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 58 of 81 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
