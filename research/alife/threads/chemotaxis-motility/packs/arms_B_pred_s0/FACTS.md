# Evidence pack: evopursuit (seed 0)

- world: `../../../../home/user/physim/research/alife/threads/chemotaxis-motility/worlds/evopursuit/world.py`, family `chemotaxis`
- parent: ecology + swimevo (alleles: active-droplets/ad5-evolve); mutation: prey carry a heritable evasion allele (chi_x x (1+e) at growth cost), prey divide (Da_p 2)
- run: 126 frames x 240 steps x dt 0.05 = time 1500; grid [160, 160]; wall 307s; status ok
- command: `WORLD_P='{"m":0,"B0":1}' python -m labkit.run threads/chemotaxis-motility/worlds/evopursuit/world.py --out threads/chemotaxis-motility/packs/arms_B_pred_s0 --seeds 0 --frames 125 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.9037], min area 6 px

## Measurements
- components: final 35, mean 29.2, max 40; occupancy final 0.06
- tracks: 1661; persistent (alive >= 50% of run): 0; longest 16 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [42, 36, 28], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 8.9
- replication (lineage window K = 20 frames = time 240, default): splits 37, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 35, merge/split ratio 0.946, nucleations 1552
- channel total drift (end/start - 1): [None, 0.2753, 0.7467, -0.0861]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 936 at frame 77: holes 0, rim-vs-core 0.51, rim-vs-outside 0.64, heterogeneity 0.26; core [0.047, 0.441, 0.908, 0.245] rim [0.118, 0.662, 0.459, 0.26]
  - track 725 at frame 61: holes 0, rim-vs-core 0.25, rim-vs-outside 0.51, heterogeneity 0.31; core [0.206, 0.584, 0.7, 0.054] rim [0.168, 0.458, 0.546, 0.197]
  - track 836 at frame 69: holes 0, rim-vs-core 0.47, rim-vs-outside 0.43, heterogeneity 0.18; core [0.168, 0.916, 0.641, 0.136] rim [0.125, 0.693, 0.263, 0.298]
  - track 472 at frame 44: holes 0, rim-vs-core 0.30, rim-vs-outside 0.46, heterogeneity 0.26; core [0.022, 0.692, 0.591, 0.147] rim [0.023, 0.584, 0.358, 0.296]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 191 components >= 12 px at frames [21, 42, 63, 83, 104, 125]):
  - radial preyA: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.9, rim/outside 4.85 (aggregate of 191 individuals; 15/191 membrane-like individually; rim level 0.167)
  - radial preyB: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.877, rim/outside 6.73 (aggregate of 191 individuals; 23/191 membrane-like individually; rim level 0.614)
  - radial predator: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.578, rim/outside 10.2 (aggregate of 191 individuals; 1/191 membrane-like individually; rim level 0.422)
  - radial n: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 3.2, rim/outside 0.751 (aggregate of 191 individuals; 0/191 membrane-like individually; rim level 0.541)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #936 (t=924, R_eq 7): ['preyB']; #725 (t=732, R_eq 6.38): none; #836 (t=828, R_eq 3.66): none; #472 (t=528, R_eq 6.05): none
- species `prey` (channels ['preyA', 'preyB'], own threshold): components final 37, mean 31.2, max 40; tracks 1502, persistent 0; splits 50, persistent splits 0 (K=20), max generation 0, merges 58, merge/split 1.16; moving tracks 1
- species `predator` (channels ['predator'], own threshold): components final 30, mean 22.6, max 32; tracks 1653, persistent 0; splits 3, persistent splits 0 (K=20), max generation 0, merges 15, merge/split 5; moving tracks 0

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 1 of 191 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
