# Evidence pack: fch-allee-micelles (seed 5)

- world: `../../../20261025T1050-c03-allee-no-turnover/world_wb1.py`, family `fch-bilayer`
- parent: collective/contrib/20261025T0816-c03-fch-gated-micelles/world.py; mutation: amphiphile no longer fed: made from a fed precursor by a shell-held autocatalyst, and degraded
- run: 151 frames x 400 steps x dt 0.02 = time 1200; grid [128, 128]; wall 661s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1050-c03-allee-no-turnover/world_wb1.py --out collective/contrib/_c07rev24/wb1/seed5 --seeds 5 --frames 150 --spf 400 --no-movie`
- segmentation: matter > 0.14 of robust range [0.1118, 2.9375], min area 6 px

## Measurements
- components: final 48, mean 46.0, max 48; occupancy final 0.20
- tracks: 76; persistent (alive >= 50% of run): 48; longest 150 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.38 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [48, 48, 48], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.6
- replication (lineage window K = 20 frames = time 160, default): splits 26, persistent splits 16 (0 more failed only because the siblings re-merged within K), max generation 1, merges 0, merge/split ratio 0, nucleations 20
- channel total drift (end/start - 1): [0.3001, -0.6106, None, -0.7791]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 5 at frame 76: holes 0, rim-vs-core 0.66, rim-vs-outside 0.26, heterogeneity 0.25; core [0.602, 0.487, 0.351, 0.041] rim [0.158, 0.001, 0.401, 0.092]
  - track 7 at frame 76: holes 0, rim-vs-core 0.63, rim-vs-outside 0.26, heterogeneity 0.24; core [0.601, 0.448, 0.355, 0.041] rim [0.162, 0.001, 0.411, 0.088]
  - track 9 at frame 76: holes 0, rim-vs-core 0.62, rim-vs-outside 0.30, heterogeneity 0.23; core [0.614, 0.415, 0.339, 0.038] rim [0.17, 0.002, 0.452, 0.079]
  - track 44 at frame 82: holes 0, rim-vs-core 0.64, rim-vs-outside 0.30, heterogeneity 0.24; core [0.616, 0.443, 0.334, 0.038] rim [0.171, 0.0, 0.453, 0.085]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 288 components >= 12 px at frames [25, 50, 76, 100, 125, 150]):
  - radial amphiphile u (u + 1.6): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.507, rim/outside 23.3 (aggregate of 288 individuals; 0/288 membrane-like individually; rim level 0.478)
  - radial catalyst c: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.209, rim/outside 9.38 (aggregate of 288 individuals; 0/288 membrane-like individually; rim level 0.153)
  - radial shell q: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 13.9, rim/outside 6.71 (aggregate of 288 individuals; 288/288 membrane-like individually; rim level 0.774)  MEMBRANE-LIKE
  - radial precursor p: peak at rho=2.15 (OUTSIDE the peak band 0.5-1.5), rim/core 5.3, rim/outside 0.868 (aggregate of 288 individuals; 0/288 membrane-like individually; rim level 0.13)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): shell q
- membrane-like channels per top track at mid-life: #5 (t=608, R_eq 4.82): ['shell q']; #7 (t=608, R_eq 4.79): ['shell q']; #9 (t=608, R_eq 4.75): ['shell q']; #44 (t=656, R_eq 4.75): ['shell q']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
