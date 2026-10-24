# Evidence pack: evopursuit (seed 0)

- world: `../../../../home/user/physim/research/alife/threads/chemotaxis-motility/worlds/evopursuit/world.py`, family `chemotaxis`
- parent: ecology + swimevo (alleles: active-droplets/ad5-evolve); mutation: prey carry a heritable evasion allele (chi_x x (1+e) at growth cost), prey divide (Da_p 2)
- run: 85 frames x 240 steps x dt 0.05 = time 1008; grid [160, 160]; wall 207s; status ok
- command: `WORLD_P='{"m":0,"B0":1,"pred":0,"pdeath":0}' python -m labkit.run threads/chemotaxis-motility/worlds/evopursuit/world.py --out threads/chemotaxis-motility/packs/arms_tox0_Bnone_s0 --seeds 0 --frames 84 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.0], min area 6 px

## Measurements
- components: final 1, mean 4.3, max 27; occupancy final 1.00
- tracks: 44; persistent (alive >= 50% of run): 1; longest 56 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.70 (1 = constant size)
- enclosures: components with a hole mean 0.20, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [0, 0, 0], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 4.5
- replication (lineage window K = 20 frames = time 240, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 16, merge/split ratio n/a, nucleations 28
- channel total drift (end/start - 1): [None, 18.9609, None, -0.7222]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 6 at frame 14: holes 0, rim-vs-core 0.32, rim-vs-outside 0.77, heterogeneity 0.09; core [0.0, 0.996, 0.0, 0.203] rim [0.0, 0.77, 0.0, 0.437]
  - track 17 at frame 13: holes 0, rim-vs-core 0.50, rim-vs-outside 0.44, heterogeneity 0.09; core [0.0, 0.964, 0.0, 0.43] rim [0.0, 0.546, 0.0, 0.695]
  - track 32 at frame 21: holes 0, rim-vs-core 0.29, rim-vs-outside 1.16, heterogeneity 0.15; core [0.346, 1.0, 0.0, 0.023] rim [0.533, 0.894, 0.0, 0.216]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 19 components >= 12 px at frames [14, 28, 42, 56, 70, 84]):
  - radial preyA: peak at rho=1.85 (OUTSIDE the peak band 0.5-1.5), rim/core 1.24, rim/outside 1.17 (aggregate of 19 individuals; 1/19 membrane-like individually; rim level 0.0786)
  - radial preyB: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.899, rim/outside 6.41 (aggregate of 19 individuals; 0/19 membrane-like individually; rim level 0.888)
  - radial predator: flat profile (no radial structure; level 0; aggregate of 19 individuals)
  - radial n: peak at rho=1.55 (OUTSIDE the peak band 0.5-1.5), rim/core 6.97, rim/outside 0.828 (aggregate of 19 individuals; 3/19 membrane-like individually; rim level 0.709)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #43 (t=684, R_eq 90.27): none; #6 (t=168, R_eq 6.02): none; #17 (t=156, R_eq 6): none; #32 (t=252, R_eq 14.99): ['preyA']
- species `prey` (channels ['preyA', 'preyB'], own threshold): components final 1, mean 4.3, max 27; tracks 44, persistent 1; splits 0, persistent splits 0 (K=20), max generation 0, merges 16, merge/split n/a; moving tracks 0
- species `predator` (channels ['predator'], own threshold): components final 0, mean 0.0, max 0; tracks 0, persistent 0; splits 0, persistent splits 0 (K=20), max generation 0, merges 0, merge/split n/a; moving tracks 0

## Warnings
- matter fills >80% of the domain at some point: components may be one connected sea
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: for 5 of 19 aggregate members less than half of the outside band (rho 1.6-2.2) was sampled (window capped on this grid, or an open boundary): their rim/outside is unreliable, and the aggregate outside level comes mostly from the smaller members

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
