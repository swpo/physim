# Evidence pack: phase-membrane-noise (seed 0)

- world: `../../pm_noise.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_membrane; mutation: dynamics noise sd 0.01 per sqrt(t): additive on ['phi'], multiplicative (sd x value) on []
- run: 161 frames x 50 steps x dt 1.0 = time 8000; grid [128, 128]; wall 15s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/pm_noise.py --out /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/packs/phi_0.01_s0 --seeds 0 --frames 160 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5412], min area 6 px

## Measurements
- components: final 19, mean 13.6, max 42; occupancy final 0.37
- tracks: 175; persistent (alive >= 50% of run): 1; longest 81 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 4.13 (1 = constant size)
- enclosures: components with a hole mean 8.31, final 13; holes at thresholds 0.2/0.35/0.5 final [6, 13, 18]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [21, 19, 19], H1 [19, 19, 12]
- motion: 2 long-lived tracks moved >= 1 body length; max speed 0.00721/time; max body lengths 1.2
- replication (lineage window K = 20 frames = time 1000, default): splits 56, persistent splits 8 (0 more failed only because the siblings re-merged within K), max generation 2, merges 11, merge/split ratio 0.196, nucleations 14
- channel total drift (end/start - 1): [-0.5446, -0.6256, 0.1954, -0.0084]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 117 at frame 108: holes 1, rim-vs-core 0.22, rim-vs-outside 0.71, heterogeneity 0.19; core [0.1, 0.687, 0.515, 0.767] rim [0.162, 0.592, 0.485, 0.584]
  - track 124 at frame 122: holes 1, rim-vs-core 0.24, rim-vs-outside 0.87, heterogeneity 0.19; core [0.08, 0.781, 0.49, 0.525] rim [0.18, 0.593, 0.521, 0.634]
  - track 100 at frame 89: holes 1, rim-vs-core 0.16, rim-vs-outside 0.85, heterogeneity 0.19; core [0.087, 0.748, 0.504, 0.645] rim [0.167, 0.613, 0.518, 0.617]
  - track 131 at frame 122: holes 1, rim-vs-core 0.17, rim-vs-outside 0.78, heterogeneity 0.18; core [0.095, 0.749, 0.529, 0.641] rim [0.165, 0.594, 0.506, 0.617]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 81 components >= 12 px at frames [27, 54, 81, 106, 133, 160]):
  - radial S: peak at rho=1.65 (OUTSIDE the peak band 0.5-1.5), rim/core 14.1, rim/outside 0.842 (aggregate of 81 individuals; 0/81 membrane-like individually; rim level 0.448)
  - radial K catalyst: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.06, rim/outside 4.51 (aggregate of 81 individuals; 0/81 membrane-like individually; rim level 0.698)
  - radial L link: peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.73, rim/outside 3.61 (aggregate of 81 individuals; 67/81 membrane-like individually; rim level 0.524)  MEMBRANE-LIKE
  - radial membrane (wall): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 2.59, rim/outside 3.2 (aggregate of 81 individuals; 68/81 membrane-like individually; rim level 0.585)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): L link, membrane (wall)
- membrane-like channels per top track at mid-life: #117 (t=5400, R_eq 13.3, ring): ['L link', 'membrane (wall)']; #124 (t=6100, R_eq 10.54, ring): ['L link', 'membrane (wall)']; #100 (t=4450, R_eq 10.56, ring): ['L link', 'membrane (wall)']; #131 (t=6100, R_eq 12.51, ring): ['L link', 'membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 55 of 81 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
