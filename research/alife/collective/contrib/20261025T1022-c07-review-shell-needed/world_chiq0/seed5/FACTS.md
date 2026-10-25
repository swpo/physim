# Evidence pack: fch-metabolic-micelles (seed 5)

- world: `../../../20261025T0922-c03-fch-metabolic/world_chiq0.py`, family `fch-bilayer`
- parent: collective/contrib/20261025T0816-c03-fch-gated-micelles/world.py; mutation: amphiphile no longer fed: made from a fed precursor by a shell-held autocatalyst, and degraded
- run: 101 frames x 400 steps x dt 0.02 = time 800; grid [128, 128]; wall 443s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0922-c03-fch-metabolic/world_chiq0.py --out collective/contrib/_c07rev18/world_chiq0/seed5 --seeds 5 --frames 100 --spf 400 --no-movie`
- segmentation: matter > 0.19 of robust range [0.006, 2.6405], min area 6 px

## Measurements
- components: final 0, mean 10.2, max 25; occupancy final 0.00
- tracks: 30; persistent (alive >= 50% of run): 5; longest 59 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 3.12 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [0, 0, 0], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.8
- replication (lineage window K = 20 frames = time 160, default): splits 3, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio 0, nucleations 20
- channel total drift (end/start - 1): [-0.9801, -0.9994, None, -0.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 7 at frame 30: holes 0, rim-vs-core 0.44, rim-vs-outside 0.20, heterogeneity 0.07; core [0.769, 0.183, 1.0, 0.574] rim [0.331, 0.175, 1.0, 0.588]
  - track 5 at frame 27: holes 0, rim-vs-core 0.46, rim-vs-outside 0.18, heterogeneity 0.08; core [0.764, 0.216, 0.998, 0.496] rim [0.309, 0.205, 0.974, 0.514]
  - track 11 at frame 27: holes 0, rim-vs-core 0.44, rim-vs-outside 0.22, heterogeneity 0.07; core [0.814, 0.233, 1.0, 0.474] rim [0.37, 0.221, 1.0, 0.49]
  - track 16 at frame 27: holes 0, rim-vs-core 0.45, rim-vs-outside 0.22, heterogeneity 0.07; core [0.815, 0.223, 1.0, 0.491] rim [0.37, 0.212, 0.999, 0.503]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 55 components >= 12 px at frames [17, 33, 50]):
  - radial amphiphile u (u + 1.6): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.589, rim/outside 16.8 (aggregate of 55 individuals; 0/55 membrane-like individually; rim level 0.577)
  - radial catalyst c: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.837, rim/outside 1.09 (aggregate of 55 individuals; 0/55 membrane-like individually; rim level 0.246)
  - radial shell q: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.942, rim/outside 1.14 (aggregate of 55 individuals; 0/55 membrane-like individually; rim level 0.908)
  - radial precursor p: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.29, rim/outside 0.983 (aggregate of 55 individuals; 0/55 membrane-like individually; rim level 0.514)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #7 (t=240, R_eq 3.19): none; #5 (t=216, R_eq 3.39): none; #11 (t=216, R_eq 3.19): none; #16 (t=216, R_eq 3.19): none

## Warnings
- no components at the end: matter died out or fell below threshold
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
