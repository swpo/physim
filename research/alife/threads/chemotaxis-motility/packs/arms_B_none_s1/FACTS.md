# Evidence pack: evopursuit (seed 1)

- world: `../../../../home/user/physim/research/alife/threads/chemotaxis-motility/worlds/evopursuit/world.py`, family `chemotaxis`
- parent: ecology + swimevo (alleles: active-droplets/ad5-evolve); mutation: prey carry a heritable evasion allele (chi_x x (1+e) at growth cost), prey divide (Da_p 2)
- run: 126 frames x 240 steps x dt 0.05 = time 1500; grid [160, 160]; wall 303s; status ok
- command: `WORLD_P='{"m":0,"B0":1,"pred":0}' python -m labkit.run threads/chemotaxis-motility/worlds/evopursuit/world.py --out threads/chemotaxis-motility/packs/arms_B_none_s1 --seeds 1 --frames 125 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 0.9938], min area 6 px

## Measurements
- components: final 9, mean 13.1, max 28; occupancy final 0.03
- tracks: 148; persistent (alive >= 50% of run): 1; longest 66 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 3.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [9, 9, 9], H1 [0, 0, 0]
- motion: 27 long-lived tracks moved >= 1 body length; max speed 0.268/time; max body lengths 21.6
- replication (lineage window K = 20 frames = time 240, default): splits 28, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 46, merge/split ratio 1.64, nucleations 48
- channel total drift (end/start - 1): [None, -0.5382, None, -0.0279]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 87 at frame 70: holes 0, rim-vs-core 0.50, rim-vs-outside 0.51, heterogeneity 0.15; core [0.455, 0.959, 0.0, 0.1] rim [0.277, 0.567, 0.0, 0.346]
  - track 95 at frame 75: holes 0, rim-vs-core 0.42, rim-vs-outside 0.80, heterogeneity 0.17; core [0.934, 0.953, 0.0, 0.094] rim [0.702, 0.661, 0.0, 0.279]
  - track 41 at frame 39: holes 0, rim-vs-core 0.31, rim-vs-outside 0.61, heterogeneity 0.10; core [0.004, 0.948, 0.0, 0.112] rim [0.004, 0.678, 0.0, 0.265]
  - track 114 at frame 90: holes 0, rim-vs-core 0.38, rim-vs-outside 0.56, heterogeneity 0.11; core [0.037, 0.958, 0.0, 0.12] rim [0.024, 0.623, 0.0, 0.294]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 78 components >= 12 px at frames [21, 42, 63, 83, 104, 125]):
  - radial preyA: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.869, rim/outside 20.7 (aggregate of 78 individuals; 0/78 membrane-like individually; rim level 0.423)
  - radial preyB: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.811, rim/outside 37.5 (aggregate of 78 individuals; 0/78 membrane-like individually; rim level 0.805)
  - radial predator: flat profile (no radial structure; level 0; aggregate of 78 individuals)
  - radial n: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 17, rim/outside 0.739 (aggregate of 78 individuals; 0/78 membrane-like individually; rim level 0.625)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #87 (t=840, R_eq 4.98): none; #95 (t=900, R_eq 5.05): none; #41 (t=468, R_eq 5.01): none; #114 (t=1080, R_eq 5.05): none
- species `prey` (channels ['preyA', 'preyB'], own threshold): components final 9, mean 13.1, max 28; tracks 148, persistent 1; splits 28, persistent splits 0 (K=20), max generation 0, merges 46, merge/split 1.64; moving tracks 27
- species `predator` (channels ['predator'], own threshold): components final 0, mean 0.0, max 0; tracks 0, persistent 0; splits 0, persistent splits 0 (K=20), max generation 0, merges 0, merge/split n/a; moving tracks 0

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
