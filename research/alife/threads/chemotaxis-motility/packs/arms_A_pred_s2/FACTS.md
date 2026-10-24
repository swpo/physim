# Evidence pack: evopursuit (seed 2)

- world: `../../../../home/user/physim/research/alife/threads/chemotaxis-motility/worlds/evopursuit/world.py`, family `chemotaxis`
- parent: ecology + swimevo (alleles: active-droplets/ad5-evolve); mutation: prey carry a heritable evasion allele (chi_x x (1+e) at growth cost), prey divide (Da_p 2)
- run: 126 frames x 240 steps x dt 0.05 = time 1500; grid [160, 160]; wall 317s; status ok
- command: `WORLD_P='{"m":0,"B0":0}' python -m labkit.run threads/chemotaxis-motility/worlds/evopursuit/world.py --out threads/chemotaxis-motility/packs/arms_A_pred_s2 --seeds 2 --frames 125 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0003, 1.7092], min area 6 px

## Measurements
- components: final 3, mean 7.9, max 25; occupancy final 0.01
- tracks: 178; persistent (alive >= 50% of run): 1; longest 76 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.54 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [3, 3, 3], H1 [0, 0, 0]
- motion: 11 long-lived tracks moved >= 1 body length; max speed 0.533/time; max body lengths 44.2
- replication (lineage window K = 20 frames = time 240, default): splits 6, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 7, merge/split ratio 1.17, nucleations 160
- channel total drift (end/start - 1): [-0.8885, None, -0.8027, -0.0055]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 145 at frame 88: holes 0, rim-vs-core 0.35, rim-vs-outside 0.46, heterogeneity 0.22; core [0.552, 0.0, 0.89, 0.002] rim [0.47, 0.0, 0.577, 0.125]
  - track 142 at frame 74: holes 0, rim-vs-core 0.39, rim-vs-outside 0.45, heterogeneity 0.22; core [0.632, 0.0, 0.903, 0.005] rim [0.459, 0.0, 0.581, 0.147]
  - track 153 at frame 77: holes 0, rim-vs-core 0.38, rim-vs-outside 0.43, heterogeneity 0.24; core [0.646, 0.0, 0.874, 0.036] rim [0.508, 0.0, 0.553, 0.177]
  - track 134 at frame 60: holes 0, rim-vs-core 0.37, rim-vs-outside 0.42, heterogeneity 0.25; core [0.664, 0.0, 0.812, 0.024] rim [0.383, 0.0, 0.609, 0.152]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 43 components >= 12 px at frames [21, 42, 63, 83, 104, 125]):
  - radial preyA: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.734, rim/outside 14.9 (aggregate of 43 individuals; 2/43 membrane-like individually; rim level 0.584)
  - radial preyB: flat profile (no radial structure; level 0; aggregate of 43 individuals)
  - radial predator: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.688, rim/outside 16.6 (aggregate of 43 individuals; 0/43 membrane-like individually; rim level 0.664)
  - radial n: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 28.3, rim/outside 0.598 (aggregate of 43 individuals; 0/43 membrane-like individually; rim level 0.439)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #145 (t=1056, R_eq 3.95): none; #142 (t=888, R_eq 3.78): none; #153 (t=924, R_eq 3.61): none; #134 (t=720, R_eq 4.92): none
- species `prey` (channels ['preyA', 'preyB'], own threshold): components final 3, mean 7.9, max 28; tracks 208, persistent 1; splits 2, persistent splits 0 (K=20), max generation 0, merges 1, merge/split 0.5; moving tracks 8
- species `predator` (channels ['predator'], own threshold): components final 3, mean 7.4, max 22; tracks 248, persistent 0; splits 0, persistent splits 0 (K=20), max generation 0, merges 6, merge/split n/a; moving tracks 9

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
