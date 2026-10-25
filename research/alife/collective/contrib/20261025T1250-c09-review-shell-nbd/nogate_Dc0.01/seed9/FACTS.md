# Evidence pack: fch-metabolic-micelles (seed 9)

- world: `../../../20261025T1131-c03-shell-not-beyond-diffusion/world_nogate_Dc0.01.py`, family `fch-bilayer`
- parent: collective/contrib/20261025T0816-c03-fch-gated-micelles/world.py; mutation: amphiphile no longer fed: made from a fed precursor by a shell-held autocatalyst, and degraded
- run: 101 frames x 400 steps x dt 0.02 = time 800; grid [128, 128]; wall 304s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1131-c03-shell-not-beyond-diffusion/world_nogate_Dc0.01.py --out collective/contrib/20261025T1250-c09-review-shell-nbd/nogate_Dc0.01/seed9 --seeds 9 --frames 100 --spf 400 --no-movie`
- segmentation: matter > 0.14 of robust range [0.1063, 2.9916], min area 6 px

## Measurements
- components: final 49, mean 39.9, max 49; occupancy final 0.24
- tracks: 80; persistent (alive >= 50% of run): 36; longest 100 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.13 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [49, 49, 49], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.7
- replication (lineage window K = 20 frames = time 160, default): splits 26, persistent splits 22 (0 more failed only because the siblings re-merged within K), max generation 2, merges 0, merge/split ratio 0, nucleations 21
- channel total drift (end/start - 1): [0.5724, 2.9963, None, -0.6391]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 8 at frame 51: holes 0, rim-vs-core 0.28, rim-vs-outside 0.43, heterogeneity 0.21; core [0.58, 0.569, 0.288, 0.04] rim [0.367, 0.396, 0.273, 0.068]
  - track 13 at frame 51: holes 0, rim-vs-core 0.60, rim-vs-outside 0.24, heterogeneity 0.21; core [0.623, 0.559, 0.258, 0.038] rim [0.167, 0.187, 0.347, 0.096]
  - track 16 at frame 51: holes 0, rim-vs-core 0.64, rim-vs-outside 0.25, heterogeneity 0.21; core [0.634, 0.653, 0.238, 0.034] rim [0.173, 0.228, 0.345, 0.101]
  - track 64 at frame 78: holes 0, rim-vs-core 0.54, rim-vs-outside 0.33, heterogeneity 0.20; core [0.633, 0.336, 0.352, 0.093] rim [0.172, 0.1, 0.5, 0.137]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 249 components >= 12 px at frames [17, 33, 50, 67, 83, 100]):
  - radial amphiphile u (u + 1.6): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.532, rim/outside 10.3 (aggregate of 249 individuals; 5/249 membrane-like individually; rim level 0.485)
  - radial catalyst c: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.421, rim/outside 5.44 (aggregate of 249 individuals; 4/249 membrane-like individually; rim level 0.314)
  - radial shell q: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 11.3, rim/outside 4.94 (aggregate of 249 individuals; 237/249 membrane-like individually; rim level 0.692)  MEMBRANE-LIKE
  - radial precursor p: peak at rho=2.25 (OUTSIDE the peak band 0.5-1.5), rim/core 2.98, rim/outside 0.889 (aggregate of 249 individuals; 0/249 membrane-like individually; rim level 0.184)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): shell q
- membrane-like channels per top track at mid-life: #8 (t=408, R_eq 5.2): ['shell q']; #13 (t=408, R_eq 5.17): ['shell q']; #16 (t=408, R_eq 5.17): ['shell q']; #64 (t=624, R_eq 5.08): ['shell q']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
