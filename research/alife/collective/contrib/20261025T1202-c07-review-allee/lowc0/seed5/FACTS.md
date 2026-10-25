# Evidence pack: fch-allee-micelles (seed 5)

- world: `../../../20261025T1050-c03-allee-no-turnover/world_lowc0.py`, family `fch-bilayer`
- parent: collective/contrib/20261025T0816-c03-fch-gated-micelles/world.py; mutation: amphiphile no longer fed: made from a fed precursor by a shell-held autocatalyst, and degraded
- run: 76 frames x 400 steps x dt 0.02 = time 600; grid [128, 128]; wall 331s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1050-c03-allee-no-turnover/world_lowc0.py --out collective/contrib/_c07rev24/lowc0/seed5 --seeds 5 --frames 75 --spf 400 --no-movie`
- segmentation: matter > 0.18 of robust range [0.0161, 2.7084], min area 6 px

## Measurements
- components: final 0, mean 13.4, max 25; occupancy final 0.00
- tracks: 30; persistent (alive >= 50% of run): 13; longest 59 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 3.50 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [0, 0, 0], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.8
- replication (lineage window K = 20 frames = time 160, default): splits 3, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio 0, nucleations 20
- channel total drift (end/start - 1): [-0.9469, -0.9974, None, -0.0001]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 7 at frame 30: holes 0, rim-vs-core 0.49, rim-vs-outside 0.57, heterogeneity 0.15; core [0.713, 0.12, 0.562, 0.619] rim [0.298, 0.087, 0.82, 0.625]
  - track 5 at frame 27: holes 0, rim-vs-core 0.54, rim-vs-outside 0.56, heterogeneity 0.15; core [0.742, 0.133, 0.476, 0.571] rim [0.31, 0.107, 0.797, 0.571]
  - track 11 at frame 27: holes 0, rim-vs-core 0.63, rim-vs-outside 0.63, heterogeneity 0.16; core [0.765, 0.156, 0.45, 0.53] rim [0.333, 0.112, 0.903, 0.565]
  - track 16 at frame 27: holes 0, rim-vs-core 0.63, rim-vs-outside 0.63, heterogeneity 0.16; core [0.765, 0.144, 0.44, 0.563] rim [0.333, 0.107, 0.892, 0.571]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 68 components >= 12 px at frames [12, 25, 38, 50]):
  - radial amphiphile u (u + 1.6): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.574, rim/outside 17.7 (aggregate of 68 individuals; 0/68 membrane-like individually; rim level 0.561)
  - radial catalyst c: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.805, rim/outside 1.18 (aggregate of 68 individuals; 0/68 membrane-like individually; rim level 0.196)
  - radial shell q: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 10.3, rim/outside 7.74 (aggregate of 68 individuals; 68/68 membrane-like individually; rim level 0.961)  MEMBRANE-LIKE
  - radial precursor p: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.42, rim/outside 0.954 (aggregate of 68 individuals; 0/68 membrane-like individually; rim level 0.478)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): shell q
- membrane-like channels per top track at mid-life: #7 (t=240, R_eq 3.19): ['shell q']; #5 (t=216, R_eq 3.29): ['shell q']; #11 (t=216, R_eq 3.19): ['shell q']; #16 (t=216, R_eq 3.19): ['shell q']

## Warnings
- no components at the end: matter died out or fell below threshold
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
