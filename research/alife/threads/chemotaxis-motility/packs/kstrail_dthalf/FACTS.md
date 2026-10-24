# Evidence pack: kstrail (seed 0)

- world: `../../../../home/user/physim/research/alife/threads/chemotaxis-motility/worlds/kstrail/world.py`, family `chemotaxis`
- parent: None; mutation: Keller-Segel with volume filling + second, slow self-secreted repellent (trail)
- run: 201 frames x 120 steps x dt 0.05 = time 1200; grid [192, 192]; wall 157s; status ok
- command: `WORLD_P='{"dt":0.025}' python -m labkit.run threads/chemotaxis-motility/worlds/kstrail/world.py --out threads/chemotaxis-motility/packs/kstrail_dthalf --frames 200 --spf 120 --size 192 192 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 0.9993], min area 6 px

## Measurements
- components: final 9, mean 9.6, max 16; occupancy final 0.05
- tracks: 84; persistent (alive >= 50% of run): 5; longest 166 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 22.40 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [9, 9, 9], H1 [0, 0, 0]
- motion: 23 long-lived tracks moved >= 1 body length; max speed 0.249/time; max body lengths 24.6
- replication: splits 20, persistent splits 2, max generation 1, merges 18, nucleations 27
- channel total drift (end/start - 1): [-0.0, -0.0, -0.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 3 at frame 118: holes 0, rim-vs-core 0.46, rim-vs-outside 0.57, heterogeneity 0.22; core [0.971, 0.869, 0.737] rim [0.63, 0.649, 0.532]
  - track 32 at frame 136: holes 0, rim-vs-core 0.37, rim-vs-outside 0.29, heterogeneity 0.13; core [0.831, 0.382, 0.27] rim [0.473, 0.312, 0.204]
  - track 46 at frame 148: holes 0, rim-vs-core 0.38, rim-vs-outside 0.55, heterogeneity 0.18; core [0.956, 0.633, 0.523] rim [0.623, 0.49, 0.395]
  - track 40 at frame 131: holes 0, rim-vs-core 0.42, rim-vs-outside 0.54, heterogeneity 0.20; core [0.96, 0.706, 0.601] rim [0.615, 0.537, 0.441]

## Warnings
- none

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
