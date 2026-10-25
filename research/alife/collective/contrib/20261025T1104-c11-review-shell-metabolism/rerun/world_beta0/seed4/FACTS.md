# Evidence pack: fch-metabolic-micelles (seed 4)

- world: `../../../../home/user/physim/research/alife/collective/contrib/20261025T0922-c03-fch-metabolic/world_beta0.py`, family `fch-bilayer`
- parent: collective/contrib/20261025T0816-c03-fch-gated-micelles/world.py; mutation: amphiphile no longer fed: made from a fed precursor by a shell-held autocatalyst, and degraded
- run: 101 frames x 400 steps x dt 0.02 = time 800; grid [128, 128]; wall 315s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0922-c03-fch-metabolic/world_beta0.py --out /tmp/claude-0/c11rev15/world_beta0 --seeds 4 --frames 100 --spf 400 --no-movie`
- segmentation: matter > 0.19 of robust range [0.006, 2.6316], min area 6 px

## Measurements
- components: final 0, mean 10.0, max 25; occupancy final 0.00
- tracks: 38; persistent (alive >= 50% of run): 4; longest 53 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 3.74 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [0, 0, 0], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.7
- replication (lineage window K = 20 frames = time 160, default): splits 8, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio 0, nucleations 16
- channel total drift (end/start - 1): [-0.9803, -0.9994, None, -0.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 8 at frame 27: holes 0, rim-vs-core 0.50, rim-vs-outside 0.53, heterogeneity 0.15; core [0.766, 0.186, 0.586, 0.521] rim [0.308, 0.184, 0.791, 0.534]
  - track 11 at frame 27: holes 0, rim-vs-core 0.16, rim-vs-outside 0.55, heterogeneity 0.15; core [0.717, 0.183, 0.683, 0.545] rim [0.552, 0.182, 0.695, 0.544]
  - track 15 at frame 27: holes 0, rim-vs-core 0.58, rim-vs-outside 0.59, heterogeneity 0.15; core [0.797, 0.179, 0.486, 0.566] rim [0.344, 0.177, 0.84, 0.579]
  - track 17 at frame 27: holes 0, rim-vs-core 0.53, rim-vs-outside 0.55, heterogeneity 0.15; core [0.783, 0.179, 0.533, 0.565] rim [0.325, 0.177, 0.798, 0.577]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 55 components >= 12 px at frames [17, 33, 50]):
  - radial amphiphile u (u + 1.6): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.596, rim/outside 16.8 (aggregate of 55 individuals; 0/55 membrane-like individually; rim level 0.584)
  - radial catalyst c: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.887, rim/outside 1.03 (aggregate of 55 individuals; 0/55 membrane-like individually; rim level 0.222)
  - radial shell q: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 8.06, rim/outside 6.97 (aggregate of 55 individuals; 55/55 membrane-like individually; rim level 0.997)  MEMBRANE-LIKE
  - radial precursor p: peak at rho=1.25 (in the peak band 0.5-1.5), rim/core 1.31, rim/outside 1.02 (aggregate of 55 individuals; 0/55 membrane-like individually; rim level 0.564)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): shell q
- membrane-like channels per top track at mid-life: #8 (t=216, R_eq 3.39): ['shell q']; #11 (t=216, R_eq 3.19): ['shell q']; #15 (t=216, R_eq 3.29): ['shell q']; #17 (t=216, R_eq 3.34): ['shell q']

## Warnings
- no components at the end: matter died out or fell below threshold
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
