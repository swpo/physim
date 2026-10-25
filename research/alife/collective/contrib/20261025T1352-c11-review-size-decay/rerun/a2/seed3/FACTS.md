# Evidence pack: fch-turnover-test (seed 3)

- world: `../../../../home/user/physim/research/alife/collective/contrib/20261025T1214-c03-size-decay-no-turnover/world_a2.py`, family `fch-bilayer`
- parent: collective/contrib/20261025T0816-c03-fch-gated-micelles/world.py; mutation: amphiphile no longer fed: made from a fed precursor by a shell-held autocatalyst, and degraded
- run: 121 frames x 400 steps x dt 0.02 = time 960; grid [128, 128]; wall 420s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1214-c03-size-decay-no-turnover/world_a2.py --out /tmp/claude-0/c11rev27/a2 --seeds 3 --frames 120 --spf 400 --no-movie`
- segmentation: matter > 0.15 of robust range [0.0759, 2.9826], min area 6 px

## Measurements
- components: final 48, mean 34.0, max 48; occupancy final 0.23
- tracks: 78; persistent (alive >= 50% of run): 35; longest 121 frames; alive start-to-end: 1
- size of persistent tracks: max/min area ratio 12.71 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [48, 48, 48], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.8
- replication (lineage window K = 20 frames = time 160, default): splits 27, persistent splits 18 (0 more failed only because the siblings re-merged within K), max generation 2, merges 0, merge/split ratio 0, nucleations 20
- channel total drift (end/start - 1): [0.4536, 1.1033, None, -0.5876]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 61: holes 0, rim-vs-core 0.77, rim-vs-outside 0.25, heterogeneity 0.25; core [0.629, 0.639, 0.229, 0.055] rim [0.19, 0.027, 0.349, 0.129]
  - track 4 at frame 61: holes 0, rim-vs-core 0.35, rim-vs-outside 0.45, heterogeneity 0.24; core [0.591, 0.571, 0.249, 0.093] rim [0.371, 0.306, 0.252, 0.125]
  - track 5 at frame 61: holes 0, rim-vs-core 0.33, rim-vs-outside 0.45, heterogeneity 0.25; core [0.579, 0.556, 0.277, 0.054] rim [0.383, 0.298, 0.264, 0.091]
  - track 60 at frame 101: holes 0, rim-vs-core 0.52, rim-vs-outside 0.32, heterogeneity 0.21; core [0.629, 0.217, 0.383, 0.128] rim [0.178, 0.006, 0.51, 0.166]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 214 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial amphiphile u (u + 1.6): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.517, rim/outside 10.6 (aggregate of 214 individuals; 0/214 membrane-like individually; rim level 0.49)
  - radial catalyst c: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.347, rim/outside 13 (aggregate of 214 individuals; 0/214 membrane-like individually; rim level 0.218)
  - radial shell q: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 12.4, rim/outside 5.24 (aggregate of 214 individuals; 214/214 membrane-like individually; rim level 0.701)  MEMBRANE-LIKE
  - radial precursor p: peak at rho=2.35 (OUTSIDE the peak band 0.5-1.5), rim/core 2.15, rim/outside 0.903 (aggregate of 214 individuals; 0/214 membrane-like individually; rim level 0.247)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): shell q
- membrane-like channels per top track at mid-life: #0 (t=488, R_eq 4.82): ['shell q']; #4 (t=488, R_eq 4.92): ['shell q']; #5 (t=488, R_eq 4.85): ['shell q']; #60 (t=808, R_eq 5.11): ['shell q']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
