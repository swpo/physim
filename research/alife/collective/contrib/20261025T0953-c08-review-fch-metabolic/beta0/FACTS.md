# Evidence pack: fch-metabolic-micelles (seed 5)

- world: `../../../../../../../home/user/physim/research/alife/collective/contrib/20261025T0922-c03-fch-metabolic/world_beta0.py`, family `fch-bilayer`
- parent: collective/contrib/20261025T0816-c03-fch-gated-micelles/world.py; mutation: amphiphile no longer fed: made from a fed precursor by a shell-held autocatalyst, and degraded
- run: 101 frames x 400 steps x dt 0.02 = time 800; grid [128, 128]; wall 304s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0922-c03-fch-metabolic/world_beta0.py --out /tmp/claude-0/-home-user-physim/b3c8c7c9-06fe-5142-8c86-74065d022b56/scratchpad/rev2/beta0 --seeds 5 --frames 100 --spf 400 --no-movie`
- segmentation: matter > 0.19 of robust range [0.006, 2.6385], min area 6 px

## Measurements
- components: final 0, mean 10.1, max 25; occupancy final 0.00
- tracks: 30; persistent (alive >= 50% of run): 5; longest 59 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 3.25 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [0, 0, 0], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.8
- replication (lineage window K = 20 frames = time 160, default): splits 3, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio 0, nucleations 20
- channel total drift (end/start - 1): [-0.9803, -0.9994, None, -0.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 7 at frame 30: holes 0, rim-vs-core 0.52, rim-vs-outside 0.60, heterogeneity 0.14; core [0.767, 0.147, 0.586, 0.6] rim [0.33, 0.145, 0.874, 0.604]
  - track 5 at frame 27: holes 0, rim-vs-core 0.57, rim-vs-outside 0.58, heterogeneity 0.15; core [0.792, 0.182, 0.499, 0.52] rim [0.342, 0.18, 0.843, 0.533]
  - track 11 at frame 27: holes 0, rim-vs-core 0.65, rim-vs-outside 0.64, heterogeneity 0.15; core [0.813, 0.184, 0.468, 0.507] rim [0.368, 0.182, 0.943, 0.521]
  - track 16 at frame 27: holes 0, rim-vs-core 0.66, rim-vs-outside 0.65, heterogeneity 0.15; core [0.814, 0.183, 0.456, 0.515] rim [0.368, 0.181, 0.942, 0.529]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 55 components >= 12 px at frames [17, 33, 50]):
  - radial amphiphile u (u + 1.6): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.591, rim/outside 16.8 (aggregate of 55 individuals; 0/55 membrane-like individually; rim level 0.579)
  - radial catalyst c: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.898, rim/outside 1.03 (aggregate of 55 individuals; 0/55 membrane-like individually; rim level 0.222)
  - radial shell q: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 7.99, rim/outside 6.99 (aggregate of 55 individuals; 55/55 membrane-like individually; rim level 0.998)  MEMBRANE-LIKE
  - radial precursor p: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.28, rim/outside 0.986 (aggregate of 55 individuals; 0/55 membrane-like individually; rim level 0.527)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): shell q
- membrane-like channels per top track at mid-life: #7 (t=240, R_eq 3.19): ['shell q']; #5 (t=216, R_eq 3.29): ['shell q']; #11 (t=216, R_eq 3.19): ['shell q']; #16 (t=216, R_eq 3.19): ['shell q']

## Warnings
- no components at the end: matter died out or fell below threshold
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
