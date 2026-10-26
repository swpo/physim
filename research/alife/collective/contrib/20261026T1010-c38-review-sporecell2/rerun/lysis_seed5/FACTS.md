# Evidence pack: sporecell2-lysis (seed 5)

- world: `../../world_lysis.py`, family `particle`
- parent: sporecell-gene; gate forked from autopoiesis/fisim-beyond-laplacian (gated mobility); mutation: majority-vote conformity of core kind (in-cell mutants erased, spores are the genetic bottleneck); per-kind catalysis rate; food mobility gated by membrane density D_F exp(-beta nM); short B shell
- run: 301 frames x 50 steps x dt 0.02 = time 300; grid [128, 128]; wall 104s; status ok
- command: `python -m labkit.run collective/contrib/20261026T1010-c38-review-sporecell2/world_lysis.py --out collective/contrib/20261026T1010-c38-review-sporecell2/rerun/lysis_seed5 --seeds 5 --frames 300 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.8635], min area 6 px

## Measurements
- components: final 5, mean 1.8, max 7; occupancy final 0.03
- tracks: 57; persistent (alive >= 50% of run): 1; longest 223 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 15.44 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [5, 4, 2], H1 [0, 0, 0]
- motion: 2 long-lived tracks moved >= 1 body length; max speed 0.16/time; max body lengths 2.4
- replication (lineage window K = 20 frames = time 20, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 3, merge/split ratio n/a, nucleations 54
- channel total drift (end/start - 1): [-0.2923, -1.0, None, 119.4444]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 3 at frame 151: holes 0, rim-vs-core 0.06, rim-vs-outside 0.47, heterogeneity 0.01; core [0.0, 0.0, 1.0, 1.0] rim [0.0, 0.0, 1.0, 0.945]
  - track 28 at frame 275: holes 0, rim-vs-core 0.05, rim-vs-outside 0.25, heterogeneity 0.02; core [0.0, 0.0, 0.927, 1.0] rim [0.012, 0.0, 0.978, 1.0]
  - track 30 at frame 275: holes 0, rim-vs-core 0.38, rim-vs-outside 0.20, heterogeneity 0.08; core [0.0, 0.0, 0.625, 1.0] rim [0.013, 0.0, 0.245, 1.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 10 components >= 12 px at frames [50, 101, 151, 199, 250, 300]):
  - radial F food: peak at rho=2.35 (OUTSIDE the peak band 0.5-1.5), rim/core 9.93, rim/outside 0.313 (aggregate of 10 individuals; 0/10 membrane-like individually; rim level 0.0906)
  - radial C0 core kind 0: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 1.23, rim/outside 1.96 (aggregate of 10 individuals; 0/10 membrane-like individually; rim level 0.2)
  - radial M membrane: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.976, rim/outside 5.12 (aggregate of 10 individuals; 1/10 membrane-like individually; rim level 0.613)
  - radial C1 core kind 1: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.954, rim/outside 9.76 (aggregate of 10 individuals; 0/10 membrane-like individually; rim level 0.8)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #3 (t=151, R_eq 2.99): none; #28 (t=275, R_eq 2.82): none; #30 (t=275, R_eq 7.33): none; #26 (t=232, R_eq 1.87): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
