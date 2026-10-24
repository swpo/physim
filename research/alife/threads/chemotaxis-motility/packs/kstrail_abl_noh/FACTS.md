# Evidence pack: kstrail (seed 0)

- world: `../../../../home/user/physim/research/alife/threads/chemotaxis-motility/worlds/kstrail/world.py`, family `chemotaxis`
- parent: None; mutation: Keller-Segel with volume filling + second, slow self-secreted repellent (trail)
- run: 201 frames x 60 steps x dt 0.05 = time 600; grid [192, 192]; wall 81s; status ok
- command: `WORLD_P='{"chi_h":0.0}' python -m labkit.run threads/chemotaxis-motility/worlds/kstrail/world.py --out threads/chemotaxis-motility/packs/kstrail_abl_noh --frames 200 --spf 60 --size 192 192 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 0.9999], min area 6 px

## Measurements
- components: final 29, mean 41.3, max 68; occupancy final 0.06
- tracks: 102; persistent (alive >= 50% of run): 38; longest 194 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 8.33 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [29, 29, 29], H1 [0, 0, 0]
- motion: 25 long-lived tracks moved >= 1 body length; max speed 0.0811/time; max body lengths 2.5
- replication: splits 0, persistent splits 0, max generation 0, merges 32, nucleations 70
- channel total drift (end/start - 1): [0.0, -0.0, -0.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 104: holes 0, rim-vs-core 0.51, rim-vs-outside 0.51, heterogeneity 0.16; core [0.967, 0.713, 0.818] rim [0.572, 0.562, 0.542]
  - track 3 at frame 106: holes 0, rim-vs-core 0.52, rim-vs-outside 0.50, heterogeneity 0.16; core [0.964, 0.718, 0.816] rim [0.55, 0.564, 0.533]
  - track 14 at frame 106: holes 0, rim-vs-core 0.45, rim-vs-outside 0.54, heterogeneity 0.14; core [0.965, 0.634, 0.771] rim [0.608, 0.509, 0.525]
  - track 15 at frame 106: holes 0, rim-vs-core 0.47, rim-vs-outside 0.53, heterogeneity 0.16; core [0.962, 0.675, 0.796] rim [0.592, 0.539, 0.539]

## Warnings
- none

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
