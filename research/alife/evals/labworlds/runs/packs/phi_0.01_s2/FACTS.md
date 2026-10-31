# Evidence pack: phase-membrane-noise (seed 2)

- world: `../../pm_noise.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_membrane; mutation: dynamics noise sd 0.01 per sqrt(t): additive on ['phi'], multiplicative (sd x value) on []
- run: 161 frames x 50 steps x dt 1.0 = time 8000; grid [128, 128]; wall 15s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/pm_noise.py --out /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/packs/phi_0.01_s2 --seeds 2 --frames 160 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5427], min area 6 px

## Measurements
- components: final 18, mean 16.2, max 40; occupancy final 0.36
- tracks: 176; persistent (alive >= 50% of run): 3; longest 93 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 9.82 (1 = constant size)
- enclosures: components with a hole mean 9.98, final 14; holes at thresholds 0.2/0.35/0.5 final [4, 14, 16]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [18, 18, 18], H1 [18, 18, 14]
- motion: 2 long-lived tracks moved >= 1 body length; max speed 0.00683/time; max body lengths 1.1
- replication (lineage window K = 20 frames = time 1000, default): splits 64, persistent splits 7 (0 more failed only because the siblings re-merged within K), max generation 1, merges 6, merge/split ratio 0.094, nucleations 8
- channel total drift (end/start - 1): [-0.5593, -0.62, 0.1914, -0.0799]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 79 at frame 65: holes 1, rim-vs-core 0.35, rim-vs-outside 0.79, heterogeneity 0.22; core [0.116, 0.866, 0.644, 0.576] rim [0.228, 0.568, 0.51, 0.583]
  - track 94 at frame 89: holes 1, rim-vs-core 0.27, rim-vs-outside 0.74, heterogeneity 0.18; core [0.105, 0.763, 0.576, 0.67] rim [0.197, 0.54, 0.492, 0.593]
  - track 86 at frame 83: holes 0, rim-vs-core 0.70, rim-vs-outside 0.47, heterogeneity 0.18; core [0.267, 0.749, 0.859, 0.898] rim [0.399, 0.322, 0.568, 0.451]
  - track 100 at frame 93: holes 1, rim-vs-core 0.20, rim-vs-outside 0.82, heterogeneity 0.20; core [0.108, 0.811, 0.606, 0.615] rim [0.176, 0.639, 0.533, 0.597]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 104 components >= 12 px at frames [27, 54, 81, 106, 133, 160]):
  - radial S: peak at rho=1.65 (OUTSIDE the peak band 0.5-1.5), rim/core 11.5, rim/outside 0.865 (aggregate of 104 individuals; 0/104 membrane-like individually; rim level 0.473)
  - radial K catalyst: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.02, rim/outside 5.53 (aggregate of 104 individuals; 0/104 membrane-like individually; rim level 0.741)
  - radial L link: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.7, rim/outside 4.42 (aggregate of 104 individuals; 87/104 membrane-like individually; rim level 0.597)  MEMBRANE-LIKE
  - radial membrane (wall): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 2.58, rim/outside 4.27 (aggregate of 104 individuals; 88/104 membrane-like individually; rim level 0.658)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): L link, membrane (wall)
- membrane-like channels per top track at mid-life: #79 (t=3250, R_eq 8.78, ring): ['L link', 'membrane (wall)']; #94 (t=4450, R_eq 9.57, ring): ['L link', 'membrane (wall)']; #86 (t=4150, R_eq 5.14): none; #100 (t=4650, R_eq 10.37, ring): ['L link', 'membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 63 of 104 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
