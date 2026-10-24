# Evidence pack: evopursuit (seed 0)

- world: `../../../../home/user/physim/research/alife/threads/chemotaxis-motility/worlds/evopursuit/world.py`, family `chemotaxis`
- parent: ecology + swimevo (alleles: active-droplets/ad5-evolve); mutation: prey carry a heritable evasion allele (chi_x x (1+e) at growth cost), prey divide (Da_p 2)
- run: 126 frames x 240 steps x dt 0.05 = time 1500; grid [160, 160]; wall 305s; status ok
- command: `WORLD_P='{"m":0,"B0":0,"pred":0}' python -m labkit.run threads/chemotaxis-motility/worlds/evopursuit/world.py --out threads/chemotaxis-motility/packs/arms_A_none_s0 --seeds 0 --frames 125 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 0.9942], min area 6 px

## Measurements
- components: final 7, mean 10.9, max 27; occupancy final 0.02
- tracks: 137; persistent (alive >= 50% of run): 0; longest 60 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [7, 7, 7], H1 [0, 0, 0]
- motion: 22 long-lived tracks moved >= 1 body length; max speed 0.263/time; max body lengths 18.5
- replication (lineage window K = 20 frames = time 240, default): splits 23, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 48, merge/split ratio 2.09, nucleations 47
- channel total drift (end/start - 1): [-0.5938, None, None, -0.0262]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 86 at frame 74: holes 0, rim-vs-core 0.47, rim-vs-outside 0.46, heterogeneity 0.10; core [0.96, 0.0, 0.0, 0.091] rim [0.56, 0.0, 0.0, 0.343]
  - track 107 at frame 87: holes 0, rim-vs-core 0.46, rim-vs-outside 0.47, heterogeneity 0.10; core [0.963, 0.0, 0.0, 0.086] rim [0.568, 0.0, 0.0, 0.329]
  - track 115 at frame 99: holes 0, rim-vs-core 0.47, rim-vs-outside 0.47, heterogeneity 0.10; core [0.963, 0.0, 0.0, 0.089] rim [0.564, 0.0, 0.0, 0.331]
  - track 17 at frame 29: holes 0, rim-vs-core 0.48, rim-vs-outside 0.46, heterogeneity 0.10; core [0.961, 0.0, 0.0, 0.095] rim [0.545, 0.0, 0.0, 0.338]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 61 components >= 12 px at frames [21, 42, 63, 83, 104, 125]):
  - radial preyA: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.819, rim/outside 48.4 (aggregate of 61 individuals; 1/61 membrane-like individually; rim level 0.797)
  - radial preyB: flat profile (no radial structure; level 0; aggregate of 61 individuals)
  - radial predator: flat profile (no radial structure; level 0; aggregate of 61 individuals)
  - radial n: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 11.6, rim/outside 0.726 (aggregate of 61 individuals; 0/61 membrane-like individually; rim level 0.623)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #86 (t=888, R_eq 5.23): none; #107 (t=1044, R_eq 5.2): none; #115 (t=1188, R_eq 5.23): none; #17 (t=348, R_eq 5.26): none
- species `prey` (channels ['preyA', 'preyB'], own threshold): components final 7, mean 10.9, max 27; tracks 137, persistent 0; splits 23, persistent splits 0 (K=20), max generation 0, merges 48, merge/split 2.09; moving tracks 22
- species `predator` (channels ['predator'], own threshold): components final 0, mean 0.0, max 0; tracks 0, persistent 0; splits 0, persistent splits 0 (K=20), max generation 0, merges 0, merge/split n/a; moving tracks 0

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 1 of 61 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
