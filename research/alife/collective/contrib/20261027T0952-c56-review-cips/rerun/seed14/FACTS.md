# Evidence pack: cips-consumer (seed 14)

- world: `../../../collective/contrib/20261026T1700-c43-cips-consumer/world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261026T1302-c42-foodchain-both-divide-claim; mutation: c42's predator condensate replaced by a conserved CIPS enzyme whose catalysis consumes prey material
- run: 121 frames x 400 steps x dt 0.25 = time 12000; grid [128, 128]; wall 232s; status ok
- command: `python -m labkit.run collective/contrib/20261026T1700-c43-cips-consumer/world.py --out c56work/cr/pack_s14 --seeds 14 --frames 120 --lineage-k 5 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0377, 1.9964], min area 6 px

## Measurements
- components: final 43, mean 39.9, max 84; occupancy final 0.20
- tracks: 916; persistent (alive >= 50% of run): 0; longest 41 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.16, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [48, 43, 38], H1 [0, 0, 0]
- motion: 143 long-lived tracks moved >= 1 body length; max speed 0.025/time; max body lengths 4.7
- replication (lineage window K = 5 frames = time 500, --lineage-k): splits 408, persistent splits 92 (0 more failed only because the siblings re-merged within K), max generation 10, merges 11, merge/split ratio 0.027, nucleations 71
- channel total drift (end/start - 1): [-0.0211, 0.0348, None, -0.5981]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 303 at frame 55: holes 0, rim-vs-core 0.26, rim-vs-outside 0.46, heterogeneity 0.25; core [0.842, 0.186, 0.134, 0.054] rim [0.634, 0.294, 0.151, 0.171]
  - track 278 at frame 45: holes 0, rim-vs-core 0.42, rim-vs-outside 0.37, heterogeneity 0.28; core [0.78, 0.49, 0.519, 0.117] rim [0.544, 0.326, 0.222, 0.187]
  - track 329 at frame 52: holes 0, rim-vs-core 0.22, rim-vs-outside 0.46, heterogeneity 0.26; core [0.774, 0.42, 0.407, 0.105] rim [0.593, 0.391, 0.309, 0.16]
  - track 840 at frame 114: holes 0, rim-vs-core 0.29, rim-vs-outside 0.30, heterogeneity 0.22; core [0.9, 0.259, 0.303, 0.062] rim [0.699, 0.141, 0.136, 0.122]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 224 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial prey a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.905, rim/outside 10.3 (aggregate of 224 individuals; 18/224 membrane-like individually; rim level 0.658)
  - radial consumer q: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.798, rim/outside 9.08 (aggregate of 224 individuals; 20/224 membrane-like individually; rim level 0.342)
  - radial product r: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.679, rim/outside 12.3 (aggregate of 224 individuals; 18/224 membrane-like individually; rim level 0.28)
  - radial fuel u: peak at rho=2.35 (OUTSIDE the peak band 0.5-1.5), rim/core 2.47, rim/outside 0.766 (aggregate of 224 individuals; 0/224 membrane-like individually; rim level 0.234)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #303 (t=5500, R_eq 7.11): ['product r']; #278 (t=4500, R_eq 5.38): none; #329 (t=5200, R_eq 5.2): none; #840 (t=11400, R_eq 4.55): ['consumer q']
- species `prey` (channels ['prey a'], own threshold): components final 39, mean 37.4, max 69; tracks 912, persistent 0; splits 400, persistent splits 71 (K=5), max generation 8, merges 20, merge/split 0.05; moving tracks 111
- species `consumer` (channels ['consumer q'], own threshold): components final 36, mean 30.5, max 61; tracks 742, persistent 0; splits 220, persistent splits 32 (K=5), max generation 4, merges 21, merge/split 0.095; moving tracks 296

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 13 of 224 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
