# Evidence pack: fl_forager_gene (seed 3)

- world: `../../../worlds/fl_forager_gene/world.py`, family `flow-lenia`
- parent: flow-lenia/fl_forager + fork of the heritable-rate-allele protocol of active-droplets/ad5-evolve and autopoiesis/phase_trait (gene carried by matter, mutation during the run, neutral control); mutation: every parcel carries a heritable uptake gene log g (eat *= g) and a genotype id, both moved with the matter by stochastic sampling; body-scale mutations log g += N(0, mut_size); gene_active=False is the neutral-marker control
- run: 301 frames x 40 steps x dt 0.2 = time 2400; grid [128, 128]; wall 438s; status ok
- command: `python -m labkit.run threads/flow-lenia/worlds/fl_forager_gene/world.py --out threads/flow-lenia/packs/fl_forager_gene/seed3 --frames 300 --seeds 3`
- segmentation: matter > 0.08 of robust range [0.0, 1.8036], min area 6 px

## Measurements
- components: final 1, mean 3.0, max 6; occupancy final 0.14
- tracks: 29; persistent (alive >= 50% of run): 1; longest 203 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.86 (1 = constant size)
- enclosures: components with a hole mean 0.91, final 1; holes at thresholds 0.2/0.35/0.5 final [6, 4, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [17, 3, 2], H1 [17, 7, 1]
- motion: 6 long-lived tracks moved >= 1 body length; max speed 0.493/time; max body lengths 21.9
- replication: splits 8, persistent splits 0, max generation 0, merges 10, nucleations 0
- channel total drift (end/start - 1): [-0.3364, 16.5611, -0.7323]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 24 at frame 184: holes 0, rim-vs-core 0.24, rim-vs-outside 0.32, heterogeneity 0.16; core [0.151, 0.54, 0.125] rim [0.09, 0.308, 0.144]
  - track 27 at frame 237: holes 10, rim-vs-core 0.23, rim-vs-outside 0.42, heterogeneity 0.20; core [0.014, 0.487, 0.004] rim [0.197, 0.374, 0.079]
  - track 25 at frame 144: holes 3, rim-vs-core 0.11, rim-vs-outside 0.43, heterogeneity 0.18; core [0.207, 0.48, 0.111] rim [0.129, 0.403, 0.094]
  - track 26 at frame 154: holes 0, rim-vs-core 0.04, rim-vs-outside 0.44, heterogeneity 0.12; core [0.008, 0.442, 0.007] rim [0.008, 0.433, 0.043]

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
