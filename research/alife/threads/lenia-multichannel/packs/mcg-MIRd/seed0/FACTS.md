# Evidence pack: mcg-MIRd (seed 0)

- world: `../../../worlds/mcg-MIRd/world.py`, family `lenia`
- parent: mcfd-MIRd + heredity mechanism forked from active-droplets (ad5-evolve: body-confined alleles, droplet-scale mutation events); mutation: heritable trait field g carried by matter: new matter copies the local g of existing matter; rare cell-scale mutation events; g sets food yield Y*exp(SEL*g) (SEL=0: neutral control)
- run: 501 frames x 20 steps x dt 0.1 = time 1000; grid [160, 160]; wall 179s; status ok
- command: `python -m labkit.run threads/lenia-multichannel/worlds/mcg-MIRd/world.py --out threads/lenia-multichannel/packs/mcg-MIRd --seeds 0 1 2 --frames 500 --size 160 160 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 0.997], min area 6 px

## Measurements
- components: final 14, mean 14.9, max 37; occupancy final 0.07
- tracks: 1775; persistent (alive >= 50% of run): 0; longest 75 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.73, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 1]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [46, 23, 12], H1 [4, 0, 0]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 0.0983/time; max body lengths 2.2
- replication: splits 443, persistent splits 0, max generation 0, merges 329, nucleations 571
- channel total drift (end/start - 1): [6.8459, 6.2595, 5.12, -0.5515, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 135 at frame 122: holes 0, rim-vs-core 0.30, rim-vs-outside 0.90, heterogeneity 0.24; core [0.963, 0.85, 0.348, 0.02, 0.007, 0.481] rim [0.762, 0.761, 0.159, 0.073, 0.015, 0.515]
  - track 947 at frame 357: holes 0, rim-vs-core 0.20, rim-vs-outside 0.90, heterogeneity 0.16; core [1.0, 0.837, 0.261, 0.139, 0.265, 0.0] rim [0.847, 0.882, 0.147, 0.18, 0.266, 0.0]
  - track 197 at frame 134: holes 0, rim-vs-core 0.43, rim-vs-outside 0.95, heterogeneity 0.18; core [1.0, 0.663, 0.376, 0.217, 0.6, 0.0] rim [0.826, 0.983, 0.147, 0.262, 0.604, 0.0]
  - track 150 at frame 122: holes 0, rim-vs-core 0.24, rim-vs-outside 0.95, heterogeneity 0.18; core [0.996, 0.853, 0.148, 0.046, 0.897, 0.0] rim [0.774, 0.838, 0.128, 0.106, 0.849, 0.0]

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
