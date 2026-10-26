# Evidence pack: eco-pursuit (seed 1)

- world: `../../world.py`, family `chemotaxis`
- parent: threads/chemotaxis-motility/worlds/evopursuit; mutation: all prey B (B0=1, m=0), species tracking, food- and prey-removal forks
- run: 201 frames x 240 steps x dt 0.05 = time 2400; grid [160, 160]; wall 321s; status ok
- command: `python -m labkit.run collective/contrib/_c26work/ep/world.py --out collective/contrib/_c26work/ep/pack_preyrm --seeds 0 1 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.8555], min area 6 px

## Measurements
- components: final 0, mean 19.0, max 39; occupancy final 0.00
- tracks: 1817; persistent (alive >= 50% of run): 0; longest 19 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [1, 1, 1], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 7.1
- replication (lineage window K = 20 frames = time 240, default): splits 37, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 58, merge/split ratio 1.57, nucleations 1684
- channel total drift (end/start - 1): [None, -0.9877, -0.7626, 0.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 358 at frame 35: holes 0, rim-vs-core 0.60, rim-vs-outside 0.60, heterogeneity 0.29; core [0.139, 0.61, 0.902, 0.086] rim [0.235, 0.724, 0.332, 0.177]
  - track 876 at frame 69: holes 0, rim-vs-core 0.39, rim-vs-outside 0.33, heterogeneity 0.26; core [0.156, 0.775, 0.569, 0.009] rim [0.084, 0.419, 0.519, 0.141]
  - track 856 at frame 66: holes 0, rim-vs-core 0.46, rim-vs-outside 0.55, heterogeneity 0.28; core [0.095, 0.509, 0.867, 0.049] rim [0.099, 0.572, 0.432, 0.192]
  - track 1463 at frame 109: holes 0, rim-vs-core 0.70, rim-vs-outside 0.61, heterogeneity 0.29; core [0.104, 0.28, 0.893, 0.163] rim [0.275, 0.704, 0.364, 0.16]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 93 components >= 12 px at frames [34, 67, 101, 133]):
  - radial preyA: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.833, rim/outside 3.88 (aggregate of 93 individuals; 14/93 membrane-like individually; rim level 0.133)
  - radial preyB: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.879, rim/outside 6.5 (aggregate of 93 individuals; 14/93 membrane-like individually; rim level 0.574)
  - radial predator: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.6, rim/outside 10.1 (aggregate of 93 individuals; 3/93 membrane-like individually; rim level 0.432)
  - radial n: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 4, rim/outside 0.735 (aggregate of 93 individuals; 0/93 membrane-like individually; rim level 0.526)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #358 (t=420, R_eq 6.86): none; #876 (t=828, R_eq 5.61): none; #856 (t=792, R_eq 6.1): none; #1463 (t=1308, R_eq 6.13): ['preyA', 'preyB']
- species `prey` (channels ['preyA', 'preyB'], own threshold): components final 0, mean 20.0, max 41; tracks 1574, persistent 0; splits 42, persistent splits 0 (K=20), max generation 0, merges 54, merge/split 1.29; moving tracks 0
- species `predator` (channels ['predator'], own threshold): components final 0, mean 15.4, max 32; tracks 1824, persistent 0; splits 6, persistent splits 0 (K=20), max generation 0, merges 17, merge/split 2.83; moving tracks 4

## Warnings
- no components at the end: matter died out or fell below threshold
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
