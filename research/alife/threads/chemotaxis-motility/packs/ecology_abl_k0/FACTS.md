# Evidence pack: ecology (seed 0)

- world: `../../../../home/user/physim/research/alife/threads/chemotaxis-motility/worlds/ecology/world.py`, family `chemotaxis`
- parent: pursuit; mutation: pursuit + toxforage kinetics: nutrient-limited prey growth, predation, self-toxic trails for both species
- run: 161 frames x 100 steps x dt 0.05 = time 800; grid [160, 160]; wall 153s; status ok
- command: `WORLD_P='{"k":0.0}' python -m labkit.run threads/chemotaxis-motility/worlds/ecology/world.py --out threads/chemotaxis-motility/packs/ecology_abl_k0 --frames 160 --spf 100 --size 160 160 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.4605], min area 6 px

## Measurements
- components: final 13, mean 11.4, max 19; occupancy final 0.04
- tracks: 148; persistent (alive >= 50% of run): 3; longest 124 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.81 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [13, 13, 13], H1 [0, 0, 0]
- motion: 32 long-lived tracks moved >= 1 body length; max speed 0.519/time; max body lengths 28.0
- replication: splits 38, persistent splits 2, max generation 1, merges 36, nucleations 37
- channel total drift (end/start - 1): [0.0071, -0.9545, -0.2767]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 23 at frame 99: holes 0, rim-vs-core 0.43, rim-vs-outside 0.37, heterogeneity 0.19; core [0.958, 0.421, 0.138] rim [0.75, 0.061, 0.248]
  - track 41 at frame 102: holes 0, rim-vs-core 0.36, rim-vs-outside 0.45, heterogeneity 0.19; core [0.969, 0.32, 0.118] rim [0.789, 0.034, 0.233]
  - track 107 at frame 121: holes 0, rim-vs-core 0.39, rim-vs-outside 0.39, heterogeneity 0.19; core [0.955, 0.322, 0.161] rim [0.727, 0.036, 0.291]
  - track 139 at frame 147: holes 0, rim-vs-core 0.26, rim-vs-outside 0.38, heterogeneity 0.13; core [0.967, 0.088, 0.148] rim [0.758, 0.012, 0.278]

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
