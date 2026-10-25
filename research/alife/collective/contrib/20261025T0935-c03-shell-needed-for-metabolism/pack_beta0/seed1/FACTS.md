# Evidence pack: fch-metabolic-micelles (seed 1)

- world: `../../../20261025T0922-c03-fch-metabolic/world_beta0.py`, family `fch-bilayer`
- parent: collective/contrib/20261025T0816-c03-fch-gated-micelles/world.py; mutation: amphiphile no longer fed: made from a fed precursor by a shell-held autocatalyst, and degraded
- run: 101 frames x 400 steps x dt 0.02 = time 800; grid [128, 128]; wall 312s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0922-c03-fch-metabolic/world_beta0.py --out collective/contrib/20261025T0935-c03-shell-needed-for-metabolism/pack_beta0/seed1 --seeds 1 --frames 100 --spf 400 --no-movie`
- segmentation: matter > 0.19 of robust range [0.0058, 2.6271], min area 6 px

## Measurements
- components: final 0, mean 9.4, max 24; occupancy final 0.00
- tracks: 31; persistent (alive >= 50% of run): 2; longest 57 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 3.50 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [0, 0, 0], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.2
- replication (lineage window K = 20 frames = time 160, default): splits 6, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio 0, nucleations 18
- channel total drift (end/start - 1): [-0.9804, -0.9995, None, -0.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 2 at frame 29: holes 0, rim-vs-core 0.58, rim-vs-outside 0.62, heterogeneity 0.15; core [0.795, 0.153, 0.528, 0.589] rim [0.35, 0.151, 0.893, 0.604]
  - track 7 at frame 29: holes 0, rim-vs-core 0.51, rim-vs-outside 0.55, heterogeneity 0.15; core [0.78, 0.152, 0.582, 0.596] rim [0.328, 0.151, 0.817, 0.604]
  - track 5 at frame 22: holes 0, rim-vs-core 0.56, rim-vs-outside 0.52, heterogeneity 0.17; core [0.81, 0.257, 0.481, 0.357] rim [0.331, 0.253, 0.769, 0.382]
  - track 9 at frame 22: holes 0, rim-vs-core 0.52, rim-vs-outside 0.51, heterogeneity 0.16; core [0.783, 0.257, 0.535, 0.364] rim [0.307, 0.253, 0.737, 0.395]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 50 components >= 12 px at frames [17, 33, 50]):
  - radial amphiphile u (u + 1.6): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.607, rim/outside 16.8 (aggregate of 50 individuals; 0/50 membrane-like individually; rim level 0.597)
  - radial catalyst c: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.902, rim/outside 1.03 (aggregate of 50 individuals; 0/50 membrane-like individually; rim level 0.227)
  - radial shell q: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 7.96, rim/outside 6.84 (aggregate of 50 individuals; 50/50 membrane-like individually; rim level 1)  MEMBRANE-LIKE
  - radial precursor p: peak at rho=2.35 (OUTSIDE the peak band 0.5-1.5), rim/core 1.29, rim/outside 0.984 (aggregate of 50 individuals; 0/50 membrane-like individually; rim level 0.509)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): shell q
- membrane-like channels per top track at mid-life: #2 (t=232, R_eq 3.19): ['shell q']; #7 (t=232, R_eq 3.24): ['shell q']; #5 (t=176, R_eq 3.57): ['shell q']; #9 (t=176, R_eq 3.61): ['shell q']

## Warnings
- no components at the end: matter died out or fell below threshold
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
