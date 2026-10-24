# Evidence pack: evopursuit (seed 0)

- world: `../../../../home/user/physim/research/alife/threads/chemotaxis-motility/worlds/evopursuit/world.py`, family `chemotaxis`
- parent: ecology + swimevo (alleles: active-droplets/ad5-evolve); mutation: prey carry a heritable evasion allele (chi_x x (1+e) at growth cost), prey divide (Da_p 2)
- run: 126 frames x 240 steps x dt 0.05 = time 1500; grid [160, 160]; wall 318s; status ok
- command: `WORLD_P='{"m":0,"B0":0}' python -m labkit.run threads/chemotaxis-motility/worlds/evopursuit/world.py --out threads/chemotaxis-motility/packs/arms_A_pred_s0 --seeds 0 --frames 125 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0003, 1.7179], min area 6 px

## Measurements
- components: final 5, mean 9.6, max 28; occupancy final 0.01
- tracks: 221; persistent (alive >= 50% of run): 3; longest 75 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.45 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [5, 5, 5], H1 [0, 0, 0]
- motion: 11 long-lived tracks moved >= 1 body length; max speed 0.458/time; max body lengths 54.1
- replication (lineage window K = 20 frames = time 240, default): splits 1, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 4, merge/split ratio 4, nucleations 215
- channel total drift (end/start - 1): [-0.854, None, -0.6789, -0.0085]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 141 at frame 79: holes 0, rim-vs-core 0.40, rim-vs-outside 0.43, heterogeneity 0.21; core [0.613, 0.0, 0.919, 0.0] rim [0.473, 0.0, 0.551, 0.055]
  - track 144 at frame 82: holes 0, rim-vs-core 0.40, rim-vs-outside 0.44, heterogeneity 0.22; core [0.591, 0.0, 0.894, 0.006] rim [0.461, 0.0, 0.561, 0.18]
  - track 161 at frame 93: holes 0, rim-vs-core 0.38, rim-vs-outside 0.40, heterogeneity 0.23; core [0.677, 0.0, 0.869, 0.025] rim [0.49, 0.0, 0.564, 0.158]
  - track 170 at frame 96: holes 0, rim-vs-core 0.43, rim-vs-outside 0.42, heterogeneity 0.23; core [0.67, 0.0, 0.863, 0.01] rim [0.45, 0.0, 0.563, 0.222]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 53 components >= 12 px at frames [21, 42, 63, 83, 104, 125]):
  - radial preyA: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.721, rim/outside 13.9 (aggregate of 53 individuals; 1/53 membrane-like individually; rim level 0.568)
  - radial preyB: flat profile (no radial structure; level 0; aggregate of 53 individuals)
  - radial predator: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.726, rim/outside 17.3 (aggregate of 53 individuals; 1/53 membrane-like individually; rim level 0.672)
  - radial n: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 19.6, rim/outside 0.627 (aggregate of 53 individuals; 0/53 membrane-like individually; rim level 0.463)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #141 (t=948, R_eq 4.44): none; #144 (t=984, R_eq 3.78): none; #161 (t=1116, R_eq 3.57): none; #170 (t=1152, R_eq 3.66): none
- species `prey` (channels ['preyA', 'preyB'], own threshold): components final 5, mean 9.8, max 29; tracks 272, persistent 0; splits 1, persistent splits 0 (K=20), max generation 0, merges 3, merge/split 3; moving tracks 12
- species `predator` (channels ['predator'], own threshold): components final 5, mean 8.9, max 22; tracks 275, persistent 0; splits 2, persistent splits 0 (K=20), max generation 0, merges 2, merge/split 1; moving tracks 9

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
