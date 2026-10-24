# Evidence pack: evopursuit (seed 1)

- world: `../../../../home/user/physim/research/alife/threads/chemotaxis-motility/worlds/evopursuit/world.py`, family `chemotaxis`
- parent: ecology + swimevo (alleles: active-droplets/ad5-evolve); mutation: prey carry a heritable evasion allele (chi_x x (1+e) at growth cost), prey divide (Da_p 2)
- run: 126 frames x 240 steps x dt 0.05 = time 1500; grid [160, 160]; wall 302s; status ok
- command: `WORLD_P='{"m":0,"B0":1,"k":0,"qdeath":0}' python -m labkit.run threads/chemotaxis-motility/worlds/evopursuit/world.py --out threads/chemotaxis-motility/packs/arms_B_esc_s1 --seeds 1 --frames 125 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.9154], min area 6 px

## Measurements
- components: final 39, mean 30.9, max 44; occupancy final 0.10
- tracks: 1010; persistent (alive >= 50% of run): 0; longest 36 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [42, 37, 32], H1 [0, 0, 0]
- motion: 13 long-lived tracks moved >= 1 body length; max speed 0.296/time; max body lengths 13.4
- replication (lineage window K = 20 frames = time 240, default): splits 199, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 155, merge/split ratio 0.779, nucleations 483
- channel total drift (end/start - 1): [None, 1.5415, 0.0, -0.1515]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 366 at frame 64: holes 0, rim-vs-core 0.42, rim-vs-outside 0.73, heterogeneity 0.19; core [0.825, 0.974, 0.557, 0.008] rim [0.826, 0.88, 0.158, 0.094]
  - track 384 at frame 66: holes 0, rim-vs-core 0.35, rim-vs-outside 0.41, heterogeneity 0.11; core [0.114, 0.968, 0.398, 0.153] rim [0.102, 0.859, 0.09, 0.29]
  - track 160 at frame 32: holes 0, rim-vs-core 0.28, rim-vs-outside 0.37, heterogeneity 0.10; core [0.14, 0.971, 0.323, 0.092] rim [0.128, 0.86, 0.096, 0.221]
  - track 188 at frame 35: holes 0, rim-vs-core 0.25, rim-vs-outside 0.34, heterogeneity 0.12; core [0.25, 0.981, 0.244, 0.108] rim [0.268, 0.915, 0.032, 0.225]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 198 components >= 12 px at frames [21, 42, 63, 83, 104, 125]):
  - radial preyA: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.924, rim/outside 7.37 (aggregate of 198 individuals; 6/198 membrane-like individually; rim level 0.25)
  - radial preyB: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.881, rim/outside 10.3 (aggregate of 198 individuals; 3/198 membrane-like individually; rim level 0.809)
  - radial predator: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.46, rim/outside 16.5 (aggregate of 198 individuals; 6/198 membrane-like individually; rim level 0.248)
  - radial n: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 3.99, rim/outside 0.713 (aggregate of 198 individuals; 0/198 membrane-like individually; rim level 0.521)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #366 (t=768, R_eq 6.86): none; #384 (t=792, R_eq 4.62): none; #160 (t=384, R_eq 5.67): none; #188 (t=420, R_eq 4.69): none
- species `prey` (channels ['preyA', 'preyB'], own threshold): components final 37, mean 30.3, max 42; tracks 1241, persistent 0; splits 286, persistent splits 0 (K=20), max generation 0, merges 319, merge/split 1.11; moving tracks 5
- species `predator` (channels ['predator'], own threshold): components final 20, mean 19.3, max 26; tracks 883, persistent 0; splits 11, persistent splits 0 (K=20), max generation 0, merges 5, merge/split 0.455; moving tracks 6

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 5 of 198 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
