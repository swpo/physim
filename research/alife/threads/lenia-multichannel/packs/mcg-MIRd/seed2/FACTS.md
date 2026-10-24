# Evidence pack: mcg-MIRd (seed 2)

- world: `../../../worlds/mcg-MIRd/world.py`, family `lenia`
- parent: mcfd-MIRd + heredity mechanism forked from active-droplets (ad5-evolve: body-confined alleles, droplet-scale mutation events); mutation: heritable trait field g carried by matter: new matter copies the local g of existing matter; rare cell-scale mutation events; g sets food yield Y*exp(SEL*g) (SEL=0: neutral control)
- run: 501 frames x 20 steps x dt 0.1 = time 1000; grid [160, 160]; wall 143s; status ok
- command: `python -m labkit.run threads/lenia-multichannel/worlds/mcg-MIRd/world.py --out threads/lenia-multichannel/packs/mcg-MIRd --seeds 0 1 2 --frames 500 --size 160 160 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 0.997], min area 6 px

## Measurements
- components: final 8, mean 14.8, max 37; occupancy final 0.05
- tracks: 1758; persistent (alive >= 50% of run): 0; longest 86 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.63, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [26, 10, 7], H1 [4, 0, 0]
- motion: 3 long-lived tracks moved >= 1 body length; max speed 0.18/time; max body lengths 2.5
- replication: splits 443, persistent splits 0, max generation 0, merges 353, nucleations 544
- channel total drift (end/start - 1): [4.2507, 3.1985, 2.7744, -0.4942, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 142 at frame 126: holes 0, rim-vs-core 0.43, rim-vs-outside 0.86, heterogeneity 0.17; core [1.0, 0.91, 0.448, 0.052, 0.136, 0.0] rim [0.783, 0.761, 0.116, 0.126, 0.132, 0.0]
  - track 535 at frame 189: holes 0, rim-vs-core 0.34, rim-vs-outside 0.65, heterogeneity 0.13; core [0.781, 0.069, 0.033, 0.005, 0.0, 0.075] rim [0.693, 0.385, 0.128, 0.045, 0.0, 0.074]
  - track 1001 at frame 361: holes 0, rim-vs-core 0.57, rim-vs-outside 0.92, heterogeneity 0.18; core [1.0, 0.635, 0.525, 0.191, 0.31, 0.0] rim [0.817, 0.998, 0.133, 0.249, 0.31, 0.0]
  - track 806 at frame 319: holes 0, rim-vs-core 0.31, rim-vs-outside 0.94, heterogeneity 0.19; core [1.0, 0.817, 0.44, 0.112, 0.742, 0.0] rim [0.801, 0.793, 0.21, 0.182, 0.716, 0.0]

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
