# Evidence pack: sporecell (seed 0)

- world: `../../worlds/sporecell/world.py`, family `particle`
- parent: eatbud-m2; mutation: promoted settings: membrane induced by food contact (mrule=food), turnover k_dec=0.01
- run: 161 frames x 50 steps x dt 0.02 = time 160; grid [128, 128]; wall 208s; status ok
- command: `python -m labkit.run threads/particle-life/worlds/sporecell/world.py --out threads/particle-life/packs/sporecell_damage --frames 160 --damage 100:0.5`
- segmentation: matter > 0.35 of robust range [0.0, 1.3197], min area 6 px

## Measurements
- components: final 17, mean 3.6, max 17; occupancy final 0.04
- tracks: 44; persistent (alive >= 50% of run): 1; longest 90 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 6.07 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [23, 16, 5], H1 [0, 0, 0]
- motion: 4 long-lived tracks moved >= 1 body length; max speed 0.27/time; max body lengths 3.2
- replication: splits 0, persistent splits 0, max generation 0, merges 0, nucleations 44
- channel total drift (end/start - 1): [-0.2577, 33.9333, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 9 at frame 116: holes 0, rim-vs-core 0.45, rim-vs-outside 0.51, heterogeneity 0.13; core [0.021, 0.99, 0.985] rim [0.156, 0.566, 0.975]
  - track 15 at frame 130: holes 0, rim-vs-core 0.39, rim-vs-outside 0.46, heterogeneity 0.10; core [0.005, 0.993, 0.992] rim [0.074, 0.612, 0.994]
  - track 4 at frame 71: holes 0, rim-vs-core 0.50, rim-vs-outside 0.43, heterogeneity 0.11; core [0.001, 0.987, 0.99] rim [0.059, 0.495, 1.0]
  - track 20 at frame 134: holes 0, rim-vs-core 0.20, rim-vs-outside 0.46, heterogeneity 0.10; core [0.009, 1.0, 0.685] rim [0.064, 0.863, 0.82]
- damage applied at frame 100: erased 32 px of a 64 px component

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, particles.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
