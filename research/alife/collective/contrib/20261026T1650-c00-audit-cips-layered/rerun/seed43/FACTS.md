# Evidence pack: cips-layered-divide (seed 43)

- world: `../../../../../../../../../../home/user/physim/research/alife/collective/contrib/20261026T1100-c40-cips-layered-divide-claim/world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261026T1025-c40-cips-turnover-divide-claim; mutation: c40 dividing CIPS world plus an amphiphile s made only by catalysis, adsorbing at the enzyme interface (drift up grad 4e(1-e)), decaying
- run: 181 frames x 500 steps x dt 0.1 = time 9000; grid [192, 192]; wall 747s; status ok
- command: `python -m labkit.run collective/contrib/20261026T1100-c40-cips-layered-divide-claim/world.py --out /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/audit/cips-layered/replication/runs/seed43 --seeds 43 --spf 500 --frames 180 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0208, 0.9751], min area 6 px

## Measurements
- components: final 15, mean 8.8, max 15; occupancy final 0.08
- tracks: 24; persistent (alive >= 50% of run): 6; longest 177 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 20.07 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [16, 15, 15], H1 [0, 0, 0]
- motion: 2 long-lived tracks moved >= 1 body length; max speed 0.00325/time; max body lengths 1.2
- replication (lineage window K = 20 frames = time 1000, default): splits 9, persistent splits 7 (0 more failed only because the siblings re-merged within K), max generation 2, merges 0, merge/split ratio 0, nucleations 6
- channel total drift (end/start - 1): [0.0, -0.6071, 0.6555, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 2 at frame 92: holes 0, rim-vs-core 0.54, rim-vs-outside 0.63, heterogeneity 0.16; core [0.989, 0.962, 0.047, 0.08] rim [0.79, 0.72, 0.23, 0.486]
  - track 0 at frame 76: holes 0, rim-vs-core 0.55, rim-vs-outside 0.60, heterogeneity 0.16; core [0.979, 0.933, 0.052, 0.073] rim [0.773, 0.71, 0.218, 0.503]
  - track 6 at frame 126: holes 0, rim-vs-core 0.57, rim-vs-outside 0.62, heterogeneity 0.17; core [0.981, 0.94, 0.029, 0.089] rim [0.772, 0.704, 0.21, 0.523]
  - track 14 at frame 163: holes 0, rim-vs-core 0.59, rim-vs-outside 0.64, heterogeneity 0.17; core [0.99, 0.964, 0.061, 0.078] rim [0.772, 0.713, 0.246, 0.528]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 59 components >= 12 px at frames [30, 61, 91, 119, 150, 180]):
  - radial e: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.864, rim/outside 26.4 (aggregate of 59 individuals; 0/59 membrane-like individually; rim level 0.836)
  - radial p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.865, rim/outside 11 (aggregate of 59 individuals; 0/59 membrane-like individually; rim level 0.819)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 20.7, rim/outside 0.645 (aggregate of 59 individuals; 0/59 membrane-like individually; rim level 0.482)
  - radial s: peak at rho=1.05 (in the peak band 0.5-1.5), rim/core 3.92, rim/outside 14.2 (aggregate of 59 individuals; 53/59 membrane-like individually; rim level 0.484)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): s
- membrane-like channels per top track at mid-life: #2 (t=4600, R_eq 7.65): ['s']; #0 (t=3800, R_eq 8.44): ['s']; #6 (t=6300, R_eq 8.67): ['s']; #14 (t=8150, R_eq 7.33): ['s']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
