# Evidence pack: active-nematic-marangoni-noise (seed 1)

- world: `../../mg_noise.py`, family `active-nematic`
- parent: collective/contrib/20261026T0505-c34-nematic-marangoni; mutation: dynamics noise sd 0.01 per sqrt(t): additive on ['q1', 'q2'], proportional on ['s', 'c'], conserved (div of white flux) on ['phi']
- run: 101 frames x 100 steps x dt 0.05 = time 500; grid [128, 128]; wall 217s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/marangoni/mg_noise.py --out /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/marangoni/packs/b128_phys_0.01_s1 --seeds 1 --frames 100 --size 128 128 --no-movie`
- segmentation: matter > 0.60 of robust range [-0.8142, 0.5441], min area 6 px

## Measurements
- components: final 21, mean 10.0, max 22; occupancy final 0.07
- tracks: 57; persistent (alive >= 50% of run): 0; longest 47 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [25, 22, 20], H1 [0, 0, 0]
- motion: 17 long-lived tracks moved >= 1 body length; max speed 0.248/time; max body lengths 5.2
- replication (lineage window K = 20 frames = time 100, default): splits 24, persistent splits 16 (0 more failed only because the siblings re-merged within K), max generation 4, merges 6, merge/split ratio 0.25, nucleations 3
- channel total drift (end/start - 1): [-0.4915, -0.4595, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 11 at frame 67: holes 0, rim-vs-core 0.69, rim-vs-outside 0.32, heterogeneity 0.21; core [0.938, 0.682, 0.483, 0.563] rim [0.767, 0.474, 0.838, 0.041]
  - track 6 at frame 58: holes 0, rim-vs-core 0.71, rim-vs-outside 0.32, heterogeneity 0.22; core [0.961, 0.638, 0.427, 0.563] rim [0.773, 0.43, 0.807, 0.031]
  - track 21 at frame 81: holes 0, rim-vs-core 0.74, rim-vs-outside 0.35, heterogeneity 0.22; core [0.959, 0.749, 0.461, 0.666] rim [0.796, 0.541, 0.822, 0.078]
  - track 29 at frame 86: holes 0, rim-vs-core 0.87, rim-vs-outside 0.38, heterogeneity 0.24; core [0.966, 0.895, 0.449, 0.693] rim [0.775, 0.599, 0.903, 0.034]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 72 components >= 12 px at frames [17, 33, 50, 67, 83, 100]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.783, rim/outside 4.54 (aggregate of 72 individuals; 0/72 membrane-like individually; rim level 0.718)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.77, rim/outside 8.31 (aggregate of 72 individuals; 3/72 membrane-like individually; rim level 0.614)
  - radial surfactant s: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.24, rim/outside 3.2 (aggregate of 72 individuals; 38/72 membrane-like individually; rim level 0.618)
  - radial cargo c: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.465, rim/outside 2.08 (aggregate of 72 individuals; 8/72 membrane-like individually; rim level 0.22)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #11 (t=335, R_eq 4.33): ['order |Q|', 'cargo c']; #6 (t=290, R_eq 4.3): none; #21 (t=405, R_eq 4.11): none; #29 (t=430, R_eq 4.03): none

## Warnings
- none

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
