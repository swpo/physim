# Evidence pack: cips-consumer (seed 41)

- world: `../../../../../../../home/user/physim/research/alife/collective/contrib/20261026T1700-c43-cips-consumer/world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261026T1302-c42-foodchain-both-divide-claim; mutation: c42's predator condensate replaced by a conserved CIPS enzyme whose catalysis consumes prey material
- run: 41 frames x 400 steps x dt 0.25 = time 4000; grid [128, 128]; wall 83s; status ok
- command: `python -m labkit.run collective/contrib/20261026T1700-c43-cips-consumer/world.py --out /tmp/claude-0/-home-user-physim/cb6f7f87-7e13-5a25-b6c0-c6ef3066597c/scratchpad/cips/efork --seeds 41 --frames 40 --lineage-k 5 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0396, 1.993], min area 6 px

## Measurements
- components: final 0, mean 30.9, max 81; occupancy final 0.00
- tracks: 304; persistent (alive >= 50% of run): 0; longest 18 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.15, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [1, 1, 1], H1 [0, 0, 0]
- motion: 36 long-lived tracks moved >= 1 body length; max speed 0.0205/time; max body lengths 2.9
- replication (lineage window K = 5 frames = time 500, --lineage-k): splits 102, persistent splits 16 (0 more failed only because the siblings re-merged within K), max generation 2, merges 15, merge/split ratio 0.147, nucleations 77
- channel total drift (end/start - 1): [-1.0, 0.0381, None, 0.0428]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 14 at frame 10: holes 0, rim-vs-core 0.38, rim-vs-outside 0.34, heterogeneity 0.27; core [0.749, 0.51, 0.509, 0.117] rim [0.503, 0.402, 0.242, 0.168]
  - track 109 at frame 11: holes 0, rim-vs-core 0.25, rim-vs-outside 0.64, heterogeneity 0.27; core [0.876, 0.281, 0.37, 0.063] rim [0.669, 0.408, 0.342, 0.124]
  - track 182 at frame 23: holes 0, rim-vs-core 0.16, rim-vs-outside 0.27, heterogeneity 0.03; core [0.946, 0.022, 0.002, 0.033] rim [0.794, 0.021, 0.001, 0.092]
  - track 174 at frame 21: holes 0, rim-vs-core 0.32, rim-vs-outside 0.34, heterogeneity 0.26; core [0.819, 0.37, 0.373, 0.08] rim [0.576, 0.296, 0.187, 0.151]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 147 components >= 12 px at frames [7, 13, 20, 27]):
  - radial prey a: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.903, rim/outside 7.32 (aggregate of 147 individuals; 11/147 membrane-like individually; rim level 0.67)
  - radial consumer q: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.794, rim/outside 9.93 (aggregate of 147 individuals; 23/147 membrane-like individually; rim level 0.348)
  - radial product r: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.701, rim/outside 13.8 (aggregate of 147 individuals; 14/147 membrane-like individually; rim level 0.302)
  - radial fuel u: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 2.62, rim/outside 0.766 (aggregate of 147 individuals; 0/147 membrane-like individually; rim level 0.223)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #14 (t=1000, R_eq 5.14): none; #109 (t=1100, R_eq 6.41): none; #182 (t=2300, R_eq 5.29): none; #174 (t=2100, R_eq 5.78): ['consumer q']
- species `prey` (channels ['prey a'], own threshold): components final 0, mean 28.5, max 68; tracks 317, persistent 0; splits 101, persistent splits 11 (K=5), max generation 2, merges 23, merge/split 0.228; moving tracks 29
- species `consumer` (channels ['consumer q'], own threshold): components final 0, mean 24.9, max 67; tracks 213, persistent 1; splits 48, persistent splits 6 (K=5), max generation 2, merges 3, merge/split 0.062; moving tracks 81

## Warnings
- no components at the end: matter died out or fell below threshold
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 6 of 147 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
