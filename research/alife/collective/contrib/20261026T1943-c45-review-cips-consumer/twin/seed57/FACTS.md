# Evidence pack: cips-consumer (seed 57)

- world: `../../../../../home/user/physim/research/alife/collective/contrib/20261026T1700-c43-cips-consumer/world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261026T1302-c42-foodchain-both-divide-claim; mutation: c42's predator condensate replaced by a conserved CIPS enzyme whose catalysis consumes prey material
- run: 121 frames x 400 steps x dt 0.25 = time 12000; grid [128, 128]; wall 153s; status ok
- command: `python -m labkit.run collective/contrib/20261026T1700-c43-cips-consumer/world.py --out /tmp/claude-0/cc/twin/seed57 --seeds 57 --frames 120 --lineage-k 5 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0256, 1.1627], min area 6 px

## Measurements
- components: final 75, mean 74.4, max 78; occupancy final 0.30
- tracks: 150; persistent (alive >= 50% of run): 75; longest 121 frames; alive start-to-end: 3
- size of persistent tracks: max/min area ratio 9.90 (1 = constant size)
- enclosures: components with a hole mean 0.01, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [75, 75, 75], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.9
- replication (lineage window K = 5 frames = time 500, --lineage-k): splits 21, persistent splits 1 (0 more failed only because the siblings re-merged within K), max generation 1, merges 10, merge/split ratio 0.476, nucleations 10
- channel total drift (end/start - 1): [0.2025, None, None, -0.7064]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 5 at frame 61: holes 0, rim-vs-core 0.18, rim-vs-outside 0.47, heterogeneity 0.06; core [0.857, 0.0, 0.0, 0.052] rim [0.675, 0.0, 0.0, 0.072]
  - track 43 at frame 61: holes 0, rim-vs-core 0.38, rim-vs-outside 0.31, heterogeneity 0.06; core [0.89, 0.0, 0.0, 0.04] rim [0.517, 0.0, 0.0, 0.095]
  - track 45 at frame 61: holes 0, rim-vs-core 0.40, rim-vs-outside 0.30, heterogeneity 0.06; core [0.883, 0.0, 0.0, 0.041] rim [0.491, 0.0, 0.0, 0.098]
  - track 148 at frame 64: holes 0, rim-vs-core 0.37, rim-vs-outside 0.32, heterogeneity 0.06; core [0.898, 0.0, 0.0, 0.037] rim [0.538, 0.0, 0.0, 0.094]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 450 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial prey a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.861, rim/outside 28.3 (aggregate of 450 individuals; 0/450 membrane-like individually; rim level 0.851)
  - radial consumer q: flat profile (no radial structure; level 0; aggregate of 450 individuals)
  - radial product r: flat profile (no radial structure; level 0; aggregate of 450 individuals)
  - radial fuel u: peak at rho=1.85 (OUTSIDE the peak band 0.5-1.5), rim/core 8.17, rim/outside 0.867 (aggregate of 450 individuals; 0/450 membrane-like individually; rim level 0.146)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #5 (t=6100, R_eq 4.3): none; #43 (t=6100, R_eq 4.55): none; #45 (t=6100, R_eq 4.65): none; #148 (t=6400, R_eq 4.65): none
- species `prey` (channels ['prey a'], own threshold): components final 75, mean 74.4, max 78; tracks 150, persistent 75; splits 21, persistent splits 1 (K=5), max generation 1, merges 10, merge/split 0.476; moving tracks 0
- species `consumer` (channels ['consumer q'], own threshold): components final 0, mean 0.0, max 0; tracks 0, persistent 0; splits 0, persistent splits 0 (K=5), max generation 0, merges 0, merge/split n/a; moving tracks 0

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
