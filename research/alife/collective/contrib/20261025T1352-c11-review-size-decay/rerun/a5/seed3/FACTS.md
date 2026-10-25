# Evidence pack: fch-turnover-test (seed 3)

- world: `../../../../home/user/physim/research/alife/collective/contrib/20261025T1214-c03-size-decay-no-turnover/world_a5.py`, family `fch-bilayer`
- parent: collective/contrib/20261025T0816-c03-fch-gated-micelles/world.py; mutation: amphiphile no longer fed: made from a fed precursor by a shell-held autocatalyst, and degraded
- run: 121 frames x 400 steps x dt 0.02 = time 960; grid [128, 128]; wall 427s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1214-c03-size-decay-no-turnover/world_a5.py --out /tmp/claude-0/c11rev27/a5 --seeds 3 --frames 120 --spf 400 --no-movie`
- segmentation: matter > 0.15 of robust range [0.0634, 2.9709], min area 6 px

## Measurements
- components: final 24, mean 23.8, max 24; occupancy final 0.12
- tracks: 30; persistent (alive >= 50% of run): 24; longest 121 frames; alive start-to-end: 1
- size of persistent tracks: max/min area ratio 12.14 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [24, 24, 24], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.5
- replication (lineage window K = 20 frames = time 160, default): splits 3, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio 0, nucleations 20
- channel total drift (end/start - 1): [0.0214, -0.1103, None, -0.4137]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 61: holes 0, rim-vs-core 0.67, rim-vs-outside 0.26, heterogeneity 0.24; core [0.655, 0.467, 0.301, 0.028] rim [0.188, 0.0, 0.392, 0.097]
  - track 4 at frame 61: holes 0, rim-vs-core 0.23, rim-vs-outside 0.49, heterogeneity 0.24; core [0.601, 0.454, 0.321, 0.057] rim [0.449, 0.28, 0.303, 0.078]
  - track 5 at frame 61: holes 0, rim-vs-core 0.26, rim-vs-outside 0.42, heterogeneity 0.24; core [0.581, 0.39, 0.362, 0.034] rim [0.409, 0.214, 0.299, 0.063]
  - track 6 at frame 61: holes 0, rim-vs-core 0.28, rim-vs-outside 0.41, heterogeneity 0.23; core [0.6, 0.377, 0.346, 0.029] rim [0.383, 0.209, 0.306, 0.062]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 144 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial amphiphile u (u + 1.6): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.513, rim/outside 13.6 (aggregate of 144 individuals; 0/144 membrane-like individually; rim level 0.489)
  - radial catalyst c: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.292, rim/outside 16.4 (aggregate of 144 individuals; 0/144 membrane-like individually; rim level 0.196)
  - radial shell q: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 12, rim/outside 6.14 (aggregate of 144 individuals; 144/144 membrane-like individually; rim level 0.719)  MEMBRANE-LIKE
  - radial precursor p: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 2.13, rim/outside 0.844 (aggregate of 144 individuals; 0/144 membrane-like individually; rim level 0.312)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): shell q
- membrane-like channels per top track at mid-life: #0 (t=488, R_eq 5.01): ['shell q']; #4 (t=488, R_eq 5.01): ['shell q']; #5 (t=488, R_eq 5.05): ['shell q']; #6 (t=488, R_eq 5.08): ['shell q']

## Warnings
- none

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
