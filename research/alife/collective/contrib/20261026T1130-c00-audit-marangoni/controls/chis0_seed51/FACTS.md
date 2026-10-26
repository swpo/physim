# Evidence pack: active-nematic-marangoni-chis0 (seed 51)

- world: `../../variants/active-nematic-marangoni-chis0.py`, family `active-nematic`
- parent: 20261025T1141-c11-active-nematic-ringed; mutation: surfactant source restricted to rod pixels (phi>0); chis 3 -> 5; optional ring-gated CH mobility gm; cargo excluded by the ring (kappa); Marangoni stress of the ring (mar)
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 497s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/waudit/nematic-marangoni/variants/active-nematic-marangoni-chis0.py --out /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/waudit/nematic-marangoni/controls/chis0_seed51 --seeds 51 --no-movie`
- segmentation: matter > 0.51 of robust range [-0.8332, 0.7878], min area 6 px

## Measurements
- components: final 32, mean 28.0, max 39; occupancy final 0.07
- tracks: 148; persistent (alive >= 50% of run): 14; longest 161 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 6.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [33, 32, 31], H1 [0, 0, 0]
- motion: 55 long-lived tracks moved >= 1 body length; max speed 0.148/time; max body lengths 4.9
- replication (lineage window K = 20 frames = time 100, default): splits 68, persistent splits 31 (0 more failed only because the siblings re-merged within K), max generation 4, merges 2, merge/split ratio 0.029, nucleations 10
- channel total drift (end/start - 1): [-0.5063, -0.343, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 30 at frame 121: holes 0, rim-vs-core 0.43, rim-vs-outside 0.39, heterogeneity 0.12; core [0.954, 0.835, 0.951, 0.102] rim [0.712, 0.511, 0.808, 0.136]
  - track 35 at frame 121: holes 0, rim-vs-core 0.52, rim-vs-outside 0.41, heterogeneity 0.13; core [0.951, 0.906, 0.975, 0.093] rim [0.669, 0.502, 0.806, 0.132]
  - track 38 at frame 123: holes 0, rim-vs-core 0.38, rim-vs-outside 0.36, heterogeneity 0.09; core [0.896, 0.801, 0.844, 0.107] rim [0.683, 0.517, 0.719, 0.142]
  - track 84 at frame 143: holes 0, rim-vs-core 0.35, rim-vs-outside 0.34, heterogeneity 0.09; core [0.854, 0.702, 0.827, 0.101] rim [0.655, 0.45, 0.699, 0.133]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 184 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.808, rim/outside 5.49 (aggregate of 184 individuals; 0/184 membrane-like individually; rim level 0.758)
  - radial order |Q|: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.718, rim/outside 9.34 (aggregate of 184 individuals; 0/184 membrane-like individually; rim level 0.581)
  - radial surfactant s: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.868, rim/outside 2.24 (aggregate of 184 individuals; 0/184 membrane-like individually; rim level 0.767)
  - radial cargo c: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 2.35, rim/outside 0.637 (aggregate of 184 individuals; 0/184 membrane-like individually; rim level 0.239)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #30 (t=605, R_eq 3.34): none; #35 (t=605, R_eq 3.91): none; #38 (t=615, R_eq 2.99): none; #84 (t=715, R_eq 3.39): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
