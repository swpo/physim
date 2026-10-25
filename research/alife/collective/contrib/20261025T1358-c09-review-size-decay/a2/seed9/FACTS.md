# Evidence pack: fch-turnover-test (seed 9)

- world: `../../../20261025T1214-c03-size-decay-no-turnover/world_a2.py`, family `fch-bilayer`
- parent: collective/contrib/20261025T0816-c03-fch-gated-micelles/world.py; mutation: amphiphile no longer fed: made from a fed precursor by a shell-held autocatalyst, and degraded
- run: 121 frames x 400 steps x dt 0.02 = time 960; grid [128, 128]; wall 391s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1214-c03-size-decay-no-turnover/world_a2.py --out collective/contrib/20261025T1358-c09-review-size-decay/a2/seed9 --seeds 9 --frames 120 --spf 400 --no-movie`
- segmentation: matter > 0.15 of robust range [0.0749, 2.9741], min area 6 px

## Measurements
- components: final 47, mean 35.5, max 47; occupancy final 0.24
- tracks: 76; persistent (alive >= 50% of run): 31; longest 120 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.82 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [47, 47, 47], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.6
- replication (lineage window K = 20 frames = time 160, default): splits 24, persistent splits 23 (0 more failed only because the siblings re-merged within K), max generation 2, merges 0, merge/split ratio 0, nucleations 21
- channel total drift (end/start - 1): [0.562, 1.3707, None, -0.6478]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 8 at frame 61: holes 0, rim-vs-core 0.30, rim-vs-outside 0.48, heterogeneity 0.24; core [0.583, 0.568, 0.257, 0.086] rim [0.409, 0.321, 0.269, 0.116]
  - track 10 at frame 61: holes 0, rim-vs-core 0.62, rim-vs-outside 0.30, heterogeneity 0.24; core [0.644, 0.611, 0.24, 0.056] rim [0.254, 0.138, 0.315, 0.107]
  - track 15 at frame 61: holes 0, rim-vs-core 0.80, rim-vs-outside 0.21, heterogeneity 0.25; core [0.631, 0.66, 0.223, 0.063] rim [0.181, 0.005, 0.296, 0.156]
  - track 58 at frame 100: holes 0, rim-vs-core 0.52, rim-vs-outside 0.31, heterogeneity 0.21; core [0.618, 0.255, 0.382, 0.126] rim [0.174, 0.006, 0.481, 0.168]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 219 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial amphiphile u (u + 1.6): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.527, rim/outside 10.3 (aggregate of 219 individuals; 3/219 membrane-like individually; rim level 0.492)
  - radial catalyst c: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.344, rim/outside 13.5 (aggregate of 219 individuals; 0/219 membrane-like individually; rim level 0.219)
  - radial shell q: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 11.1, rim/outside 5.11 (aggregate of 219 individuals; 215/219 membrane-like individually; rim level 0.697)  MEMBRANE-LIKE
  - radial precursor p: peak at rho=2.15 (OUTSIDE the peak band 0.5-1.5), rim/core 2.2, rim/outside 0.89 (aggregate of 219 individuals; 0/219 membrane-like individually; rim level 0.234)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): shell q
- membrane-like channels per top track at mid-life: #8 (t=488, R_eq 4.79): ['shell q']; #10 (t=488, R_eq 4.95): ['shell q']; #15 (t=488, R_eq 4.92): ['shell q']; #58 (t=800, R_eq 4.98): ['shell q']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
