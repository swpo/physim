# Evidence pack: fch-metabolic-micelles (seed 23)

- world: `../world_ctl.py`, family `fch-bilayer`
- parent: collective/contrib/20261025T0816-c03-fch-gated-micelles/world.py; mutation: amphiphile no longer fed: made from a fed precursor by a shell-held autocatalyst, and degraded
- run: 151 frames x 400 steps x dt 0.02 = time 1200; grid [128, 128]; wall 663s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0945-c10-review-fch-metabolic/world_ctl.py --out collective/contrib/20261025T0945-c10-review-fch-metabolic/lowD001 --seeds 23 --frames 150 --spf 400 --no-movie`
- segmentation: matter > 0.14 of robust range [0.108, 2.9963], min area 6 px

## Measurements
- components: final 48, mean 40.5, max 48; occupancy final 0.24
- tracks: 79; persistent (alive >= 50% of run): 40; longest 151 frames; alive start-to-end: 1
- size of persistent tracks: max/min area ratio 14.67 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [48, 48, 48], H1 [0, 0, 0]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 0.0102/time; max body lengths 1.2
- replication (lineage window K = 20 frames = time 160, default): splits 28, persistent splits 22 (0 more failed only because the siblings re-merged within K), max generation 3, merges 0, merge/split ratio 0, nucleations 19
- channel total drift (end/start - 1): [0.5854, 2.9512, None, -0.6293]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 3 at frame 76: holes 0, rim-vs-core 0.60, rim-vs-outside 0.26, heterogeneity 0.21; core [0.621, 0.561, 0.276, 0.043] rim [0.166, 0.19, 0.375, 0.101]
  - track 7 at frame 76: holes 0, rim-vs-core 0.60, rim-vs-outside 0.28, heterogeneity 0.21; core [0.633, 0.535, 0.272, 0.04] rim [0.173, 0.179, 0.408, 0.095]
  - track 9 at frame 76: holes 0, rim-vs-core 0.64, rim-vs-outside 0.27, heterogeneity 0.21; core [0.631, 0.653, 0.245, 0.051] rim [0.176, 0.227, 0.376, 0.124]
  - track 73 at frame 131: holes 0, rim-vs-core 0.50, rim-vs-outside 0.34, heterogeneity 0.19; core [0.619, 0.213, 0.382, 0.086] rim [0.168, 0.077, 0.54, 0.11]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 259 components >= 12 px at frames [25, 50, 76, 100, 125, 150]):
  - radial amphiphile u (u + 1.6): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.515, rim/outside 10.5 (aggregate of 259 individuals; 0/259 membrane-like individually; rim level 0.489)
  - radial catalyst c: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.436, rim/outside 5.07 (aggregate of 259 individuals; 0/259 membrane-like individually; rim level 0.323)
  - radial shell q: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 13, rim/outside 4.93 (aggregate of 259 individuals; 259/259 membrane-like individually; rim level 0.709)  MEMBRANE-LIKE
  - radial precursor p: peak at rho=1.95 (OUTSIDE the peak band 0.5-1.5), rim/core 2.98, rim/outside 0.901 (aggregate of 259 individuals; 0/259 membrane-like individually; rim level 0.176)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): shell q
- membrane-like channels per top track at mid-life: #3 (t=608, R_eq 5.2): ['shell q']; #7 (t=608, R_eq 5.17): ['shell q']; #9 (t=608, R_eq 5.17): ['shell q']; #73 (t=1048, R_eq 5.11): ['shell q']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
