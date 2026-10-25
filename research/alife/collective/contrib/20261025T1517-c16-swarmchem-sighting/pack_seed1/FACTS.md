# Evidence pack: swarmchem-23 (seed 1)

- world: `../world.py`, family `swarm-chemistry`
- parent: new class (Sayama 2009 Swarm Chemistry); mutation: none; recipe from a random screen
- run: 201 frames x 20 steps x dt 1.0 = time 4000; grid [128, 128]; wall 169s; status ok
- command: `python -m labkit.run /tmp/claude-0/swarm/w/world.py --out /tmp/claude-0/swarm/w/pack --seeds 1 --frames 200 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 0.2306], min area 6 px

## Measurements
- components: final 11, mean 12.4, max 31; occupancy final 0.08
- tracks: 70; persistent (alive >= 50% of run): 11; longest 201 frames; alive start-to-end: 1
- size of persistent tracks: max/min area ratio 5.06 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [12, 11, 11], H1 [0, 0, 0]
- motion: 15 long-lived tracks moved >= 1 body length; max speed 0.086/time; max body lengths 7.5
- replication (lineage window K = 20 frames = time 400, default): splits 1, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 12, merge/split ratio 12, nucleations 49
- channel total drift (end/start - 1): [0.0, 0.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 6 at frame 101: holes 0, rim-vs-core 0.14, rim-vs-outside 0.32, heterogeneity 0.11; core [0.719, 0.012] rim [0.587, 0.041]
  - track 21 at frame 101: holes 0, rim-vs-core 0.29, rim-vs-outside 0.23, heterogeneity 0.11; core [0.809, 0.01] rim [0.517, 0.052]
  - track 25 at frame 101: holes 0, rim-vs-core 0.33, rim-vs-outside 0.24, heterogeneity 0.11; core [0.809, 0.008] rim [0.484, 0.044]
  - track 37 at frame 101: holes 0, rim-vs-core 0.36, rim-vs-outside 0.23, heterogeneity 0.12; core [0.834, 0.008] rim [0.478, 0.062]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 72 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial red density (core species): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.852, rim/outside 42.8 (aggregate of 72 individuals; 0/72 membrane-like individually; rim level 0.771)
  - radial blue density (halo species): peak at rho=1.65 (OUTSIDE the peak band 0.5-1.5), rim/core 25.8, rim/outside 0.746 (aggregate of 72 individuals; 5/72 membrane-like individually; rim level 0.268)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #6 (t=2020, R_eq 4.95): none; #21 (t=2020, R_eq 5.29): none; #25 (t=2020, R_eq 4.72): none; #37 (t=2020, R_eq 5.94): none

## Warnings
- none

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
