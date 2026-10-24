# Evidence pack: evopursuit (seed 0)

- world: `../../../../home/user/physim/research/alife/threads/chemotaxis-motility/worlds/evopursuit/world.py`, family `chemotaxis`
- parent: ecology + swimevo (alleles: active-droplets/ad5-evolve); mutation: prey carry a heritable evasion allele (chi_x x (1+e) at growth cost), prey divide (Da_p 2)
- run: 85 frames x 240 steps x dt 0.05 = time 1008; grid [160, 160]; wall 208s; status ok
- command: `WORLD_P='{"m":0,"B0":1,"k":0,"qdeath":0,"pdeath":0}' python -m labkit.run threads/chemotaxis-motility/worlds/evopursuit/world.py --out threads/chemotaxis-motility/packs/arms_tox0_Besc_s0 --seeds 0 --frames 84 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.9904], min area 6 px

## Measurements
- components: final 1, mean 4.1, max 30; occupancy final 1.00
- tracks: 151; persistent (alive >= 50% of run): 1; longest 60 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.63 (1 = constant size)
- enclosures: components with a hole mean 0.22, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [6, 5, 5], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 3.1
- replication (lineage window K = 20 frames = time 240, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 20, merge/split ratio n/a, nucleations 131
- channel total drift (end/start - 1): [None, 18.9609, -0.0002, -0.7222]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 90 at frame 16: holes 0, rim-vs-core 0.31, rim-vs-outside 0.63, heterogeneity 0.08; core [0.0, 1.0, 0.272, 0.099] rim [0.0, 0.957, 0.029, 0.282]
  - track 37 at frame 13: holes 0, rim-vs-core 0.55, rim-vs-outside 0.35, heterogeneity 0.14; core [0.0, 0.954, 0.656, 0.406] rim [0.0, 0.814, 0.144, 0.557]
  - track 107 at frame 17: holes 0, rim-vs-core 0.20, rim-vs-outside 0.86, heterogeneity 0.09; core [0.0, 1.0, 0.286, 0.046] rim [0.004, 0.991, 0.116, 0.144]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 32 components >= 12 px at frames [14, 28, 42, 56, 70, 84]):
  - radial preyA: peak at rho=1.35 (in the peak band 0.5-1.5), rim/core 1.11, rim/outside 2.44 (aggregate of 32 individuals; 1/32 membrane-like individually; rim level 0.0145)
  - radial preyB: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.913, rim/outside 14.6 (aggregate of 32 individuals; 0/32 membrane-like individually; rim level 0.881)
  - radial predator: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.49, rim/outside 14.3 (aggregate of 32 individuals; 1/32 membrane-like individually; rim level 0.212)
  - radial n: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 2.48, rim/outside 0.659 (aggregate of 32 individuals; 0/32 membrane-like individually; rim level 0.59)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #150 (t=660, R_eq 90.27): none; #90 (t=192, R_eq 7.57): none; #37 (t=156, R_eq 4.3): none; #107 (t=204, R_eq 11.18): ['preyA']
- species `prey` (channels ['preyA', 'preyB'], own threshold): components final 1, mean 5.0, max 38; tracks 190, persistent 1; splits 2, persistent splits 0 (K=20), max generation 0, merges 26, merge/split 13; moving tracks 0
- species `predator` (channels ['predator'], own threshold): components final 5, mean 7.2, max 19; tracks 187, persistent 0; splits 10, persistent splits 0 (K=20), max generation 0, merges 11, merge/split 1.1; moving tracks 3

## Warnings
- matter fills >80% of the domain at some point: components may be one connected sea
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: for 5 of 32 aggregate members less than half of the outside band (rho 1.6-2.2) was sampled (window capped on this grid, or an open boundary): their rim/outside is unreliable, and the aggregate outside level comes mostly from the smaller members

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
