# Evidence pack: phase-membrane-chi0 (seed 2)

- world: `../../../worlds/phase_membrane_chi0/world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_membrane; mutation: CONTROL: chi=0 (no link adsorption to the wall); is the ring load-bearing?
- run: 161 frames x 50 steps x dt 1.0 = time 8000; grid [128, 128]; wall 9s; status ok
- command: `python -m labkit.run threads/autopoiesis/worlds/phase_membrane_chi0/world.py --out threads/autopoiesis/packs/phase_membrane_chi0 --seeds 0 1 2 --frames 160`
- segmentation: matter > 0.35 of robust range [0.0, 1.529], min area 6 px

## Measurements
- components: final 43, mean 27.4, max 43; occupancy final 0.37
- tracks: 108; persistent (alive >= 50% of run): 15; longest 116 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.04 (1 = constant size)
- enclosures: components with a hole mean 2.02, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 12]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [43, 43, 43], H1 [45, 37, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.8
- replication (lineage window K = 20 frames = time 1000, default): splits 37, persistent splits 32 (0 more failed only because the siblings re-merged within K), max generation 4, merges 1, merge/split ratio 0.027, nucleations 0
- channel total drift (end/start - 1): [-0.535, -0.6822, 0.2975, -0.0278]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 51 at frame 104: holes 0, rim-vs-core 0.43, rim-vs-outside 0.98, heterogeneity 0.18; core [0.094, 0.852, 0.738, 0.657] rim [0.273, 0.479, 0.658, 0.716]
  - track 52 at frame 104: holes 0, rim-vs-core 0.46, rim-vs-outside 0.97, heterogeneity 0.19; core [0.087, 0.859, 0.728, 0.586] rim [0.29, 0.467, 0.659, 0.692]
  - track 55 at frame 105: holes 0, rim-vs-core 0.46, rim-vs-outside 0.96, heterogeneity 0.19; core [0.086, 0.849, 0.716, 0.585] rim [0.291, 0.46, 0.653, 0.685]
  - track 86 at frame 126: holes 0, rim-vs-core 0.46, rim-vs-outside 0.98, heterogeneity 0.19; core [0.101, 0.885, 0.782, 0.637] rim [0.283, 0.478, 0.672, 0.699]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 183 components >= 12 px at frames [27, 54, 81, 106, 133, 160]):
  - radial S: peak at rho=1.65 (OUTSIDE the peak band 0.5-1.5), rim/core 11.4, rim/outside 0.909 (aggregate of 183 individuals; 0/183 membrane-like individually; rim level 0.486)
  - radial K catalyst: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.901, rim/outside 11.7 (aggregate of 183 individuals; 0/183 membrane-like individually; rim level 0.783)
  - radial L link: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.12, rim/outside 8.64 (aggregate of 183 individuals; 7/183 membrane-like individually; rim level 0.756)
  - radial membrane (wall): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 2.88, rim/outside 8.05 (aggregate of 183 individuals; 163/183 membrane-like individually; rim level 0.817)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): membrane (wall)
- membrane-like channels per top track at mid-life: #51 (t=5200, R_eq 7.86): none; #52 (t=5200, R_eq 7.36): ['membrane (wall)']; #55 (t=5250, R_eq 7.53): ['membrane (wall)']; #86 (t=6300, R_eq 6.46): ['membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 13 of 183 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
