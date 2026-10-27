# Evidence pack: cips-consumer (seed 55)

- world: `../../../20261026T1700-c43-cips-consumer/world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261026T1302-c42-foodchain-both-divide-claim; mutation: c42's predator condensate replaced by a conserved CIPS enzyme whose catalysis consumes prey material
- run: 121 frames x 400 steps x dt 0.25 = time 12000; grid [128, 128]; wall 258s; status ok
- command: `python -m labkit.run collective/contrib/20261026T1700-c43-cips-consumer/world.py --out collective/contrib/20261027T0900-c54-review-cips-consumer/rerun/seed55 --seeds 55 --frames 120 --lineage-k 5 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0375, 2.0023], min area 6 px

## Measurements
- components: final 35, mean 38.4, max 80; occupancy final 0.20
- tracks: 845; persistent (alive >= 50% of run): 0; longest 36 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.12, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [42, 35, 32], H1 [0, 0, 0]
- motion: 147 long-lived tracks moved >= 1 body length; max speed 0.0238/time; max body lengths 4.6
- replication (lineage window K = 5 frames = time 500, --lineage-k): splits 374, persistent splits 88 (0 more failed only because the siblings re-merged within K), max generation 9, merges 15, merge/split ratio 0.04, nucleations 70
- channel total drift (end/start - 1): [0.02, 0.0141, None, -0.5894]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 646 at frame 103: holes 0, rim-vs-core 0.39, rim-vs-outside 0.36, heterogeneity 0.28; core [0.767, 0.48, 0.479, 0.121] rim [0.509, 0.374, 0.209, 0.193]
  - track 148 at frame 25: holes 0, rim-vs-core 0.27, rim-vs-outside 0.63, heterogeneity 0.28; core [0.853, 0.347, 0.39, 0.073] rim [0.62, 0.45, 0.348, 0.148]
  - track 529 at frame 81: holes 0, rim-vs-core 0.22, rim-vs-outside 0.62, heterogeneity 0.26; core [0.831, 0.363, 0.402, 0.092] rim [0.638, 0.43, 0.344, 0.15]
  - track 803 at frame 117: holes 0, rim-vs-core 0.42, rim-vs-outside 0.26, heterogeneity 0.17; core [0.843, 0.289, 0.352, 0.053] rim [0.75, 0.008, 0.062, 0.094]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 218 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial prey a: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.886, rim/outside 10.8 (aggregate of 218 individuals; 13/218 membrane-like individually; rim level 0.669)
  - radial consumer q: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.852, rim/outside 8.22 (aggregate of 218 individuals; 23/218 membrane-like individually; rim level 0.336)
  - radial product r: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.712, rim/outside 12.7 (aggregate of 218 individuals; 13/218 membrane-like individually; rim level 0.268)
  - radial fuel u: peak at rho=2.25 (OUTSIDE the peak band 0.5-1.5), rim/core 2.66, rim/outside 0.768 (aggregate of 218 individuals; 0/218 membrane-like individually; rim level 0.241)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #646 (t=10300, R_eq 5.5): none; #148 (t=2500, R_eq 6.18): none; #529 (t=8100, R_eq 7.09): none; #803 (t=11700, R_eq 4.3): none
- species `prey` (channels ['prey a'], own threshold): components final 35, mean 36.3, max 72; tracks 859, persistent 0; splits 374, persistent splits 70 (K=5), max generation 7, merges 21, merge/split 0.056; moving tracks 117
- species `consumer` (channels ['consumer q'], own threshold): components final 22, mean 28.6, max 65; tracks 669, persistent 0; splits 200, persistent splits 24 (K=5), max generation 3, merges 19, merge/split 0.095; moving tracks 269

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 6 of 218 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
