# Evidence pack: cips-layered-divide (seed 14)

- world: `../../../../../home/user/physim/research/alife/collective/contrib/20261026T1100-c40-cips-layered-divide-claim/world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261026T1025-c40-cips-turnover-divide-claim; mutation: c40 dividing CIPS world plus an amphiphile s made only by catalysis, adsorbing at the enzyme interface (drift up grad 4e(1-e)), decaying
- run: 151 frames x 1000 steps x dt 0.1 = time 15000; grid [128, 128]; wall 354s; status ok
- command: `python -m labkit.run collective/contrib/20261026T1100-c40-cips-layered-divide-claim/world.py --out /tmp/claude-0/cl/kF008/seed14 --seeds 14 --size 128 128 --frames 150 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0545, 0.9371], min area 6 px

## Measurements
- components: final 13, mean 12.5, max 13; occupancy final 0.12
- tracks: 13; persistent (alive >= 50% of run): 13; longest 148 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 10.10 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [13, 13, 13], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.7
- replication (lineage window K = 20 frames = time 2000, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio n/a, nucleations 13
- channel total drift (end/start - 1): [0.0, -0.3472, 1.4661, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 77: holes 0, rim-vs-core 0.64, rim-vs-outside 0.50, heterogeneity 0.17; core [0.955, 0.913, 0.06, 0.109] rim [0.713, 0.673, 0.249, 0.623]
  - track 1 at frame 77: holes 0, rim-vs-core 0.64, rim-vs-outside 0.51, heterogeneity 0.17; core [0.962, 0.924, 0.072, 0.1] rim [0.719, 0.678, 0.255, 0.605]
  - track 2 at frame 77: holes 0, rim-vs-core 0.39, rim-vs-outside 0.68, heterogeneity 0.17; core [0.952, 0.908, 0.074, 0.112] rim [0.808, 0.768, 0.181, 0.426]
  - track 3 at frame 78: holes 0, rim-vs-core 0.66, rim-vs-outside 0.50, heterogeneity 0.18; core [0.961, 0.922, 0.088, 0.099] rim [0.709, 0.67, 0.263, 0.621]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 78 components >= 12 px at frames [25, 50, 76, 100, 125, 150]):
  - radial e: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.931, rim/outside 40.7 (aggregate of 78 individuals; 0/78 membrane-like individually; rim level 0.928)
  - radial p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.872, rim/outside 12.6 (aggregate of 78 individuals; 0/78 membrane-like individually; rim level 0.864)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 29.7, rim/outside 0.66 (aggregate of 78 individuals; 0/78 membrane-like individually; rim level 0.499)
  - radial s: peak at rho=1.05 (in the peak band 0.5-1.5), rim/core 10.8, rim/outside 41.4 (aggregate of 78 individuals; 78/78 membrane-like individually; rim level 0.892)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): s
- membrane-like channels per top track at mid-life: #0 (t=7700, R_eq 7.53): ['s']; #1 (t=7700, R_eq 7.07): ['s']; #2 (t=7700, R_eq 7.27): ['s']; #3 (t=7800, R_eq 6.75): ['s']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
