# Evidence pack: evopursuit (seed 0)

- world: `../../../../home/user/physim/research/alife/threads/chemotaxis-motility/worlds/evopursuit/world.py`, family `chemotaxis`
- parent: ecology + swimevo (alleles: active-droplets/ad5-evolve); mutation: prey carry a heritable evasion allele (chi_x x (1+e) at growth cost), prey divide (Da_p 2)
- run: 126 frames x 240 steps x dt 0.05 = time 1500; grid [160, 160]; wall 318s; status ok
- command: `WORLD_P='{"m":0,"B0":0,"k":0,"qdeath":0}' python -m labkit.run threads/chemotaxis-motility/worlds/evopursuit/world.py --out threads/chemotaxis-motility/packs/arms_A_esc_s0 --seeds 0 --frames 125 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.9629], min area 6 px

## Measurements
- components: final 23, mean 20.2, max 27; occupancy final 0.07
- tracks: 455; persistent (alive >= 50% of run): 0; longest 47 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [27, 23, 22], H1 [0, 0, 0]
- motion: 25 long-lived tracks moved >= 1 body length; max speed 0.301/time; max body lengths 16.9
- replication (lineage window K = 20 frames = time 240, default): splits 103, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 114, merge/split ratio 1.11, nucleations 144
- channel total drift (end/start - 1): [0.6237, None, 0.0089, -0.1027]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 86 at frame 45: holes 0, rim-vs-core 0.47, rim-vs-outside 0.41, heterogeneity 0.17; core [0.961, 0.0, 0.609, 0.135] rim [0.766, 0.0, 0.218, 0.301]
  - track 225 at frame 81: holes 0, rim-vs-core 0.34, rim-vs-outside 0.43, heterogeneity 0.11; core [0.986, 0.0, 0.397, 0.088] rim [0.877, 0.0, 0.112, 0.244]
  - track 298 at frame 102: holes 0, rim-vs-core 0.25, rim-vs-outside 0.54, heterogeneity 0.17; core [0.979, 0.0, 0.509, 0.056] rim [0.825, 0.0, 0.415, 0.229]
  - track 14 at frame 19: holes 0, rim-vs-core 0.46, rim-vs-outside 0.41, heterogeneity 0.17; core [0.935, 0.0, 0.652, 0.185] rim [0.732, 0.0, 0.275, 0.351]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 123 components >= 12 px at frames [21, 42, 63, 83, 104, 125]):
  - radial preyA: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.853, rim/outside 13.5 (aggregate of 123 individuals; 2/123 membrane-like individually; rim level 0.799)
  - radial preyB: flat profile (no radial structure; level 0; aggregate of 123 individuals)
  - radial predator: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.535, rim/outside 24.1 (aggregate of 123 individuals; 1/123 membrane-like individually; rim level 0.314)
  - radial n: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 5.79, rim/outside 0.694 (aggregate of 123 individuals; 0/123 membrane-like individually; rim level 0.53)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #86 (t=540, R_eq 4.89): none; #225 (t=972, R_eq 4.58): none; #298 (t=1224, R_eq 5.7): none; #14 (t=228, R_eq 4.92): none
- species `prey` (channels ['preyA', 'preyB'], own threshold): components final 22, mean 20.2, max 29; tracks 548, persistent 0; splits 145, persistent splits 0 (K=20), max generation 0, merges 160, merge/split 1.1; moving tracks 17
- species `predator` (channels ['predator'], own threshold): components final 18, mean 14.8, max 21; tracks 312, persistent 0; splits 25, persistent splits 0 (K=20), max generation 0, merges 10, merge/split 0.4; moving tracks 25

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
