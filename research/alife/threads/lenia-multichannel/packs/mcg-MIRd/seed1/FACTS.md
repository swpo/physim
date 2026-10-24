# Evidence pack: mcg-MIRd (seed 1)

- world: `../../../worlds/mcg-MIRd/world.py`, family `lenia`
- parent: mcfd-MIRd + heredity mechanism forked from active-droplets (ad5-evolve: body-confined alleles, droplet-scale mutation events); mutation: heritable trait field g carried by matter: new matter copies the local g of existing matter; rare cell-scale mutation events; g sets food yield Y*exp(SEL*g) (SEL=0: neutral control)
- run: 501 frames x 20 steps x dt 0.1 = time 1000; grid [160, 160]; wall 142s; status ok
- command: `python -m labkit.run threads/lenia-multichannel/worlds/mcg-MIRd/world.py --out threads/lenia-multichannel/packs/mcg-MIRd --seeds 0 1 2 --frames 500 --size 160 160 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 0.997], min area 6 px

## Measurements
- components: final 14, mean 12.1, max 34; occupancy final 0.08
- tracks: 1446; persistent (alive >= 50% of run): 0; longest 53 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.72, final 0; holes at thresholds 0.2/0.35/0.5 final [1, 0, 2]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [37, 20, 13], H1 [8, 2, 0]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 0.458/time; max body lengths 3.6
- replication: splits 405, persistent splits 0, max generation 0, merges 248, nucleations 405
- channel total drift (end/start - 1): [8.1628, 6.4695, 5.4068, -0.4935, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 787 at frame 298: holes 0, rim-vs-core 0.37, rim-vs-outside 0.66, heterogeneity 0.14; core [0.899, 0.254, 0.072, 0.006, 0.0, 0.115] rim [0.699, 0.5, 0.261, 0.048, 0.0, 0.116]
  - track 272 at frame 130: holes 0, rim-vs-core 0.20, rim-vs-outside 0.65, heterogeneity 0.13; core [0.678, 0.322, 0.062, 0.001, 0.0, 0.992] rim [0.672, 0.497, 0.15, 0.017, 0.0, 0.989]
  - track 216 at frame 118: holes 0, rim-vs-core 0.54, rim-vs-outside 0.92, heterogeneity 0.18; core [1.0, 0.604, 0.431, 0.123, 0.669, 0.0] rim [0.851, 1.0, 0.098, 0.162, 0.668, 0.0]
  - track 186 at frame 113: holes 0, rim-vs-core 0.44, rim-vs-outside 0.81, heterogeneity 0.20; core [0.948, 0.705, 0.552, 0.019, 0.296, 0.0] rim [0.77, 0.715, 0.151, 0.084, 0.314, 0.0]

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
