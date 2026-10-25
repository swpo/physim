# Evidence pack: fch-turnover-test (seed 9)

- world: `../../../20261025T1214-c03-size-decay-no-turnover/world_a5.py`, family `fch-bilayer`
- parent: collective/contrib/20261025T0816-c03-fch-gated-micelles/world.py; mutation: amphiphile no longer fed: made from a fed precursor by a shell-held autocatalyst, and degraded
- run: 121 frames x 400 steps x dt 0.02 = time 960; grid [128, 128]; wall 389s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1214-c03-size-decay-no-turnover/world_a5.py --out collective/contrib/20261025T1358-c09-review-size-decay/a5/seed9 --seeds 9 --frames 120 --spf 400 --no-movie`
- segmentation: matter > 0.15 of robust range [0.0624, 2.9745], min area 6 px

## Measurements
- components: final 26, mean 23.9, max 26; occupancy final 0.13
- tracks: 34; persistent (alive >= 50% of run): 24; longest 121 frames; alive start-to-end: 2
- size of persistent tracks: max/min area ratio 14.17 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [26, 26, 26], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.5
- replication (lineage window K = 20 frames = time 160, default): splits 3, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio 0, nucleations 21
- channel total drift (end/start - 1): [0.0314, -0.1185, None, -0.4112]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 61: holes 0, rim-vs-core 0.64, rim-vs-outside 0.30, heterogeneity 0.22; core [0.668, 0.437, 0.272, 0.01] rim [0.221, 0.002, 0.425, 0.063]
  - track 4 at frame 61: holes 0, rim-vs-core 0.65, rim-vs-outside 0.27, heterogeneity 0.22; core [0.652, 0.436, 0.281, 0.03] rim [0.194, 0.001, 0.4, 0.093]
  - track 7 at frame 61: holes 0, rim-vs-core 0.62, rim-vs-outside 0.33, heterogeneity 0.24; core [0.695, 0.516, 0.247, 0.021] rim [0.278, 0.086, 0.386, 0.078]
  - track 8 at frame 61: holes 0, rim-vs-core 0.30, rim-vs-outside 0.43, heterogeneity 0.24; core [0.607, 0.442, 0.318, 0.036] rim [0.409, 0.223, 0.303, 0.072]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 146 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial amphiphile u (u + 1.6): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.517, rim/outside 13.6 (aggregate of 146 individuals; 0/146 membrane-like individually; rim level 0.492)
  - radial catalyst c: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.334, rim/outside 17.8 (aggregate of 146 individuals; 0/146 membrane-like individually; rim level 0.215)
  - radial shell q: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 11.8, rim/outside 6.15 (aggregate of 146 individuals; 146/146 membrane-like individually; rim level 0.711)  MEMBRANE-LIKE
  - radial precursor p: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 2.02, rim/outside 0.852 (aggregate of 146 individuals; 0/146 membrane-like individually; rim level 0.321)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): shell q
- membrane-like channels per top track at mid-life: #0 (t=488, R_eq 5.05): ['shell q']; #4 (t=488, R_eq 5.01): ['shell q']; #7 (t=488, R_eq 5.05): ['shell q']; #8 (t=488, R_eq 5.05): ['shell q']

## Warnings
- none

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
