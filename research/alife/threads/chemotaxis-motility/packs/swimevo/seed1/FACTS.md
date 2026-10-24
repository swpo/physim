# Evidence pack: swimevo (seed 1)

- world: `../../../worlds/swimevo/world.py`, family `chemotaxis`
- parent: swimfission + active-droplets/ad5-evolve (confined alleles); mutation: split rho into two heritable alleles with own-density cooperative growth (body purification), symmetric patch mutations, allele B grows (1+s) faster
- run: 151 frames x 240 steps x dt 0.05 = time 1800; grid [160, 160]; wall 205s; status ok
- command: `python -m labkit.run threads/chemotaxis-motility/worlds/swimevo/world.py --out threads/chemotaxis-motility/packs/swimevo --seeds 0 1 2 --frames 150 --spf 240`
- segmentation: matter > 0.35 of robust range [0.0, 0.9957], min area 6 px

## Measurements
- components: final 11, mean 13.3, max 32; occupancy final 0.04
- tracks: 181; persistent (alive >= 50% of run): 3; longest 148 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 7.27 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [11, 11, 11], H1 [0, 0, 0]
- motion: 39 long-lived tracks moved >= 1 body length; max speed 0.271/time; max body lengths 50.1
- replication: splits 40, persistent splits 0, max generation 0, merges 55, nucleations 51
- channel total drift (end/start - 1): [-0.9482, None, -0.364, -0.0445]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 8 at frame 77: holes 0, rim-vs-core 0.58, rim-vs-outside 0.46, heterogeneity 0.17; core [0.959, 0.0, 0.748, 0.101] rim [0.48, 0.0, 0.539, 0.353]
  - track 10 at frame 73: holes 0, rim-vs-core 0.30, rim-vs-outside 0.65, heterogeneity 0.17; core [0.938, 0.0, 0.622, 0.162] rim [0.682, 0.0, 0.551, 0.292]
  - track 52 at frame 79: holes 0, rim-vs-core 0.55, rim-vs-outside 0.47, heterogeneity 0.17; core [0.959, 0.0, 0.722, 0.11] rim [0.526, 0.0, 0.503, 0.368]
  - track 98 at frame 57: holes 0, rim-vs-core 0.51, rim-vs-outside 0.49, heterogeneity 0.16; core [0.961, 0.0, 0.76, 0.097] rim [0.571, 0.0, 0.545, 0.337]

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
