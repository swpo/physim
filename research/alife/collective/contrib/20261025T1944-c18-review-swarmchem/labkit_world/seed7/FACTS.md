# Evidence pack: swarmchem-23 (seed 7)

- world: `../world2.py`, family `swarm-chemistry`
- parent: new class (Sayama 2009 Swarm Chemistry); mutation: none; recipe from a random screen
- run: 201 frames x 20 steps x dt 1.0 = time 4000; grid [128, 128]; wall 127s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/3b801bf0-17d3-5f80-b419-db17577ce992/scratchpad/rev15/world2.py --out /tmp/claude-0/-home-user-physim/3b801bf0-17d3-5f80-b419-db17577ce992/scratchpad/rev15/labkit_world --seeds 7 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 0.2319], min area 6 px

## Measurements
- components: final 10, mean 12.5, max 23; occupancy final 0.08
- tracks: 61; persistent (alive >= 50% of run): 10; longest 201 frames; alive start-to-end: 1
- size of persistent tracks: max/min area ratio 6.38 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [10, 10, 10], H1 [0, 0, 0]
- motion: 22 long-lived tracks moved >= 1 body length; max speed 0.0981/time; max body lengths 7.9
- replication (lineage window K = 20 frames = time 400, default): splits 1, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 8, merge/split ratio 8, nucleations 41
- channel total drift (end/start - 1): [0.0, 0.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1 at frame 101: holes 0, rim-vs-core 0.32, rim-vs-outside 0.44, heterogeneity 0.12; core [0.906, 0.001] rim [0.588, 0.041]
  - track 18 at frame 101: holes 0, rim-vs-core 0.35, rim-vs-outside 0.25, heterogeneity 0.12; core [0.87, 0.012] rim [0.522, 0.072]
  - track 20 at frame 101: holes 0, rim-vs-core 0.35, rim-vs-outside 0.23, heterogeneity 0.12; core [0.832, 0.007] rim [0.488, 0.058]
  - track 31 at frame 101: holes 0, rim-vs-core 0.12, rim-vs-outside 0.29, heterogeneity 0.13; core [0.69, 0.041] rim [0.578, 0.085]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 72 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial red density (core species): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.848, rim/outside 59.3 (aggregate of 72 individuals; 0/72 membrane-like individually; rim level 0.779)
  - radial blue density (halo species): peak at rho=1.65 (OUTSIDE the peak band 0.5-1.5), rim/core 26.2, rim/outside 0.781 (aggregate of 72 individuals; 4/72 membrane-like individually; rim level 0.268)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #1 (t=2020, R_eq 7.02): none; #18 (t=2020, R_eq 5.17): none; #20 (t=2020, R_eq 5.81): none; #31 (t=2020, R_eq 4.62): none

## Warnings
- none

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
