# Evidence pack: evopursuit (seed 2)

- world: `../../../../home/user/physim/research/alife/threads/chemotaxis-motility/worlds/evopursuit/world.py`, family `chemotaxis`
- parent: ecology + swimevo (alleles: active-droplets/ad5-evolve); mutation: prey carry a heritable evasion allele (chi_x x (1+e) at growth cost), prey divide (Da_p 2)
- run: 126 frames x 240 steps x dt 0.05 = time 1500; grid [160, 160]; wall 312s; status ok
- command: `WORLD_P='{"m":0,"B0":0,"pred":0}' python -m labkit.run threads/chemotaxis-motility/worlds/evopursuit/world.py --out threads/chemotaxis-motility/packs/arms_A_none_s2 --seeds 2 --frames 125 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 0.9955], min area 6 px

## Measurements
- components: final 13, mean 14.4, max 28; occupancy final 0.04
- tracks: 152; persistent (alive >= 50% of run): 3; longest 102 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 3.84 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [13, 13, 13], H1 [0, 0, 0]
- motion: 25 long-lived tracks moved >= 1 body length; max speed 0.29/time; max body lengths 29.6
- replication (lineage window K = 20 frames = time 240, default): splits 32, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 48, merge/split ratio 1.5, nucleations 43
- channel total drift (end/start - 1): [-0.243, None, None, -0.0489]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 64 at frame 75: holes 0, rim-vs-core 0.49, rim-vs-outside 0.45, heterogeneity 0.10; core [0.958, 0.0, 0.0, 0.106] rim [0.537, 0.0, 0.0, 0.355]
  - track 50 at frame 58: holes 0, rim-vs-core 0.46, rim-vs-outside 0.47, heterogeneity 0.10; core [0.962, 0.0, 0.0, 0.097] rim [0.573, 0.0, 0.0, 0.343]
  - track 43 at frame 56: holes 0, rim-vs-core 0.48, rim-vs-outside 0.45, heterogeneity 0.10; core [0.958, 0.0, 0.0, 0.114] rim [0.543, 0.0, 0.0, 0.359]
  - track 97 at frame 77: holes 0, rim-vs-core 0.47, rim-vs-outside 0.48, heterogeneity 0.10; core [0.966, 0.0, 0.0, 0.096] rim [0.574, 0.0, 0.0, 0.357]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 83 components >= 12 px at frames [21, 42, 63, 83, 104, 125]):
  - radial preyA: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.807, rim/outside 46.5 (aggregate of 83 individuals; 0/83 membrane-like individually; rim level 0.789)
  - radial preyB: flat profile (no radial structure; level 0; aggregate of 83 individuals)
  - radial predator: flat profile (no radial structure; level 0; aggregate of 83 individuals)
  - radial n: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 12.9, rim/outside 0.737 (aggregate of 83 individuals; 0/83 membrane-like individually; rim level 0.627)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #64 (t=900, R_eq 5.38): none; #50 (t=696, R_eq 5.17): none; #43 (t=672, R_eq 5.26): none; #97 (t=924, R_eq 5.14): none
- species `prey` (channels ['preyA', 'preyB'], own threshold): components final 13, mean 14.4, max 28; tracks 152, persistent 3; splits 32, persistent splits 0 (K=20), max generation 0, merges 48, merge/split 1.5; moving tracks 25
- species `predator` (channels ['predator'], own threshold): components final 0, mean 0.0, max 0; tracks 0, persistent 0; splits 0, persistent splits 0 (K=20), max generation 0, merges 0, merge/split n/a; moving tracks 0

## Warnings
- none

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
