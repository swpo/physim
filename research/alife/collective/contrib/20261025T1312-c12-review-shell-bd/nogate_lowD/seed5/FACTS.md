# Evidence pack: fch-metabolic-micelles (seed 5)

- world: `../../world_nogate_lowD.py`, family `fch-bilayer`
- parent: collective/contrib/20261025T0816-c03-fch-gated-micelles/world.py; mutation: amphiphile no longer fed: made from a fed precursor by a shell-held autocatalyst, and degraded
- run: 101 frames x 400 steps x dt 0.02 = time 800; grid [128, 128]; wall 520s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1312-c12-review-shell-bd/world_nogate_lowD.py --out collective/contrib/20261025T1312-c12-review-shell-bd/nogate_lowD/seed5 --seeds 5 --frames 100 --spf 400 --no-movie`
- segmentation: matter > 0.14 of robust range [0.1061, 2.9902], min area 6 px

## Measurements
- components: final 49, mean 39.8, max 49; occupancy final 0.24
- tracks: 78; persistent (alive >= 50% of run): 39; longest 100 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.28 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [49, 49, 49], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.6
- replication (lineage window K = 20 frames = time 160, default): splits 27, persistent splits 20 (0 more failed only because the siblings re-merged within K), max generation 2, merges 0, merge/split ratio 0, nucleations 20
- channel total drift (end/start - 1): [0.5265, 2.9259, None, -0.6259]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 5 at frame 51: holes 0, rim-vs-core 0.62, rim-vs-outside 0.28, heterogeneity 0.21; core [0.644, 0.593, 0.237, 0.039] rim [0.197, 0.194, 0.368, 0.104]
  - track 10 at frame 51: holes 0, rim-vs-core 0.60, rim-vs-outside 0.25, heterogeneity 0.21; core [0.619, 0.582, 0.262, 0.038] rim [0.168, 0.201, 0.349, 0.097]
  - track 16 at frame 51: holes 0, rim-vs-core 0.58, rim-vs-outside 0.26, heterogeneity 0.20; core [0.625, 0.521, 0.259, 0.035] rim [0.172, 0.179, 0.369, 0.087]
  - track 64 at frame 82: holes 0, rim-vs-core 0.52, rim-vs-outside 0.33, heterogeneity 0.20; core [0.62, 0.272, 0.353, 0.111] rim [0.17, 0.083, 0.514, 0.149]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 248 components >= 12 px at frames [17, 33, 50, 67, 83, 100]):
  - radial amphiphile u (u + 1.6): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.519, rim/outside 11.2 (aggregate of 248 individuals; 0/248 membrane-like individually; rim level 0.483)
  - radial catalyst c: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.415, rim/outside 5.72 (aggregate of 248 individuals; 0/248 membrane-like individually; rim level 0.315)
  - radial shell q: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 12, rim/outside 5.06 (aggregate of 248 individuals; 243/248 membrane-like individually; rim level 0.697)  MEMBRANE-LIKE
  - radial precursor p: peak at rho=2.05 (OUTSIDE the peak band 0.5-1.5), rim/core 3.42, rim/outside 0.889 (aggregate of 248 individuals; 0/248 membrane-like individually; rim level 0.184)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): shell q
- membrane-like channels per top track at mid-life: #5 (t=408, R_eq 5.11): ['shell q']; #10 (t=408, R_eq 5.08): ['shell q']; #16 (t=408, R_eq 5.08): ['shell q']; #64 (t=656, R_eq 5.17): ['shell q']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
