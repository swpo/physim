# Evidence pack: fch-metabolic-micelles (seed 5)

- world: `../../../../../../../home/user/physim/research/alife/collective/contrib/20261025T0922-c03-fch-metabolic/world.py`, family `fch-bilayer`
- parent: collective/contrib/20261025T0816-c03-fch-gated-micelles/world.py; mutation: amphiphile no longer fed: made from a fed precursor by a shell-held autocatalyst, and degraded
- run: 151 frames x 400 steps x dt 0.02 = time 1200; grid [128, 128]; wall 466s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0922-c03-fch-metabolic/world.py --out /tmp/claude-0/-home-user-physim/b3c8c7c9-06fe-5142-8c86-74065d022b56/scratchpad/rev2/rerun --seeds 5 --frames 150 --spf 400 --no-movie`
- segmentation: matter > 0.14 of robust range [0.0807, 2.9922], min area 6 px

## Measurements
- components: final 63, mean 44.9, max 63; occupancy final 0.31
- tracks: 106; persistent (alive >= 50% of run): 38; longest 150 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.78 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [64, 64, 64], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.8
- replication (lineage window K = 20 frames = time 160, default): splits 41, persistent splits 34 (0 more failed only because the siblings re-merged within K), max generation 3, merges 0, merge/split ratio 0, nucleations 20
- channel total drift (end/start - 1): [0.8541, 3.7787, None, -0.7619]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 7 at frame 76: holes 0, rim-vs-core 0.69, rim-vs-outside 0.24, heterogeneity 0.23; core [0.632, 0.528, 0.247, 0.033] rim [0.18, 0.022, 0.357, 0.081]
  - track 10 at frame 76: holes 0, rim-vs-core 0.79, rim-vs-outside 0.24, heterogeneity 0.25; core [0.638, 0.636, 0.232, 0.035] rim [0.182, 0.006, 0.352, 0.092]
  - track 16 at frame 76: holes 0, rim-vs-core 0.72, rim-vs-outside 0.25, heterogeneity 0.23; core [0.636, 0.553, 0.235, 0.039] rim [0.183, 0.016, 0.362, 0.088]
  - track 78 at frame 116: holes 0, rim-vs-core 0.53, rim-vs-outside 0.30, heterogeneity 0.20; core [0.622, 0.257, 0.361, 0.047] rim [0.172, 0.004, 0.472, 0.071]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 288 components >= 12 px at frames [25, 50, 76, 100, 125, 150]):
  - radial amphiphile u (u + 1.6): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.519, rim/outside 7.76 (aggregate of 288 individuals; 2/288 membrane-like individually; rim level 0.489)
  - radial catalyst c: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.323, rim/outside 8.92 (aggregate of 288 individuals; 7/288 membrane-like individually; rim level 0.215)
  - radial shell q: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 12.5, rim/outside 4.55 (aggregate of 288 individuals; 286/288 membrane-like individually; rim level 0.7)  MEMBRANE-LIKE
  - radial precursor p: peak at rho=2.05 (OUTSIDE the peak band 0.5-1.5), rim/core 2.45, rim/outside 0.919 (aggregate of 288 individuals; 0/288 membrane-like individually; rim level 0.177)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): shell q
- membrane-like channels per top track at mid-life: #7 (t=608, R_eq 5.14): ['shell q']; #10 (t=608, R_eq 5.17): ['shell q']; #16 (t=608, R_eq 5.14): ['shell q']; #78 (t=928, R_eq 5.08): ['shell q']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
