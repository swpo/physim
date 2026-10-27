# Evidence pack: cips-consumer (seed 41)

- world: `../../../../../../../home/user/physim/research/alife/collective/contrib/20261026T1700-c43-cips-consumer/world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261026T1302-c42-foodchain-both-divide-claim; mutation: c42's predator condensate replaced by a conserved CIPS enzyme whose catalysis consumes prey material
- run: 121 frames x 400 steps x dt 0.25 = time 12000; grid [128, 128]; wall 242s; status ok
- command: `python -m labkit.run collective/contrib/20261026T1700-c43-cips-consumer/world.py --out /tmp/claude-0/-home-user-physim/cb6f7f87-7e13-5a25-b6c0-c6ef3066597c/scratchpad/cips/pack --seeds 41 --frames 120 --lineage-k 5 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0374, 2.0038], min area 6 px

## Measurements
- components: final 39, mean 39.2, max 81; occupancy final 0.20
- tracks: 872; persistent (alive >= 50% of run): 0; longest 36 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.09, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [43, 41, 37], H1 [0, 0, 0]
- motion: 160 long-lived tracks moved >= 1 body length; max speed 0.0214/time; max body lengths 5.7
- replication (lineage window K = 5 frames = time 500, --lineage-k): splits 373, persistent splits 101 (0 more failed only because the siblings re-merged within K), max generation 11, merges 27, merge/split ratio 0.072, nucleations 86
- channel total drift (end/start - 1): [0.005, 0.0381, None, -0.5982]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 214 at frame 36: holes 0, rim-vs-core 0.48, rim-vs-outside 0.39, heterogeneity 0.28; core [0.771, 0.605, 0.641, 0.143] rim [0.523, 0.413, 0.281, 0.211]
  - track 658 at frame 99: holes 0, rim-vs-core 0.22, rim-vs-outside 0.61, heterogeneity 0.27; core [0.878, 0.338, 0.397, 0.064] rim [0.702, 0.354, 0.283, 0.109]
  - track 633 at frame 92: holes 0, rim-vs-core 0.37, rim-vs-outside 0.35, heterogeneity 0.27; core [0.826, 0.417, 0.457, 0.104] rim [0.546, 0.37, 0.233, 0.178]
  - track 837 at frame 117: holes 0, rim-vs-core 0.14, rim-vs-outside 0.26, heterogeneity 0.03; core [0.886, 0.032, 0.003, 0.026] rim [0.767, 0.03, 0.002, 0.094]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 240 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial prey a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.885, rim/outside 10.1 (aggregate of 240 individuals; 17/240 membrane-like individually; rim level 0.661)
  - radial consumer q: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.793, rim/outside 10.9 (aggregate of 240 individuals; 20/240 membrane-like individually; rim level 0.363)
  - radial product r: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.676, rim/outside 14.2 (aggregate of 240 individuals; 12/240 membrane-like individually; rim level 0.297)
  - radial fuel u: peak at rho=2.25 (OUTSIDE the peak band 0.5-1.5), rim/core 2.41, rim/outside 0.782 (aggregate of 240 individuals; 0/240 membrane-like individually; rim level 0.24)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #214 (t=3600, R_eq 4.89): none; #658 (t=9900, R_eq 6.33): ['consumer q']; #633 (t=9200, R_eq 5.61): none; #837 (t=11700, R_eq 5.97): none
- species `prey` (channels ['prey a'], own threshold): components final 39, mean 36.6, max 65; tracks 869, persistent 0; splits 369, persistent splits 87 (K=5), max generation 9, merges 37, merge/split 0.1; moving tracks 127
- species `consumer` (channels ['consumer q'], own threshold): components final 32, mean 30.1, max 67; tracks 679, persistent 0; splits 215, persistent splits 36 (K=5), max generation 5, merges 16, merge/split 0.074; moving tracks 286

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 7 of 240 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
