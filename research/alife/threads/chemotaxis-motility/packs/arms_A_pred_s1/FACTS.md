# Evidence pack: evopursuit (seed 1)

- world: `../../../../home/user/physim/research/alife/threads/chemotaxis-motility/worlds/evopursuit/world.py`, family `chemotaxis`
- parent: ecology + swimevo (alleles: active-droplets/ad5-evolve); mutation: prey carry a heritable evasion allele (chi_x x (1+e) at growth cost), prey divide (Da_p 2)
- run: 126 frames x 240 steps x dt 0.05 = time 1500; grid [160, 160]; wall 318s; status ok
- command: `WORLD_P='{"m":0,"B0":0}' python -m labkit.run threads/chemotaxis-motility/worlds/evopursuit/world.py --out threads/chemotaxis-motility/packs/arms_A_pred_s1 --seeds 1 --frames 125 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0003, 1.6951], min area 6 px

## Measurements
- components: final 3, mean 7.5, max 26; occupancy final 0.01
- tracks: 147; persistent (alive >= 50% of run): 2; longest 95 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.47 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [3, 3, 3], H1 [0, 0, 0]
- motion: 11 long-lived tracks moved >= 1 body length; max speed 0.524/time; max body lengths 53.9
- replication (lineage window K = 20 frames = time 240, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 5, merge/split ratio n/a, nucleations 142
- channel total drift (end/start - 1): [-0.8824, None, -0.7685, -0.0059]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 73 at frame 65: holes 0, rim-vs-core 0.44, rim-vs-outside 0.47, heterogeneity 0.22; core [0.639, 0.0, 0.932, 0.02] rim [0.519, 0.0, 0.531, 0.148]
  - track 140 at frame 93: holes 0, rim-vs-core 0.41, rim-vs-outside 0.46, heterogeneity 0.22; core [0.691, 0.0, 0.894, 0.006] rim [0.473, 0.0, 0.573, 0.149]
  - track 42 at frame 41: holes 0, rim-vs-core 0.35, rim-vs-outside 0.44, heterogeneity 0.21; core [0.612, 0.0, 0.917, 0.0] rim [0.478, 0.0, 0.601, 0.077]
  - track 133 at frame 69: holes 0, rim-vs-core 0.39, rim-vs-outside 0.44, heterogeneity 0.22; core [0.672, 0.0, 0.879, 0.014] rim [0.505, 0.0, 0.546, 0.13]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 40 components >= 12 px at frames [21, 42, 63, 83, 104, 125]):
  - radial preyA: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.721, rim/outside 12 (aggregate of 40 individuals; 0/40 membrane-like individually; rim level 0.59)
  - radial preyB: flat profile (no radial structure; level 0; aggregate of 40 individuals)
  - radial predator: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.748, rim/outside 15.5 (aggregate of 40 individuals; 1/40 membrane-like individually; rim level 0.707)
  - radial n: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 30.8, rim/outside 0.589 (aggregate of 40 individuals; 0/40 membrane-like individually; rim level 0.407)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #73 (t=780, R_eq 3.7): none; #140 (t=1116, R_eq 3.74): none; #42 (t=492, R_eq 3.83): none; #133 (t=828, R_eq 3.66): none
- species `prey` (channels ['preyA', 'preyB'], own threshold): components final 3, mean 7.6, max 27; tracks 213, persistent 0; splits 2, persistent splits 0 (K=20), max generation 0, merges 2, merge/split 1; moving tracks 14
- species `predator` (channels ['predator'], own threshold): components final 3, mean 7.1, max 23; tracks 186, persistent 2; splits 0, persistent splits 0 (K=20), max generation 0, merges 4, merge/split n/a; moving tracks 9

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
