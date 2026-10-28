# Evidence pack: flow-lenia-digestion-ecology (seed 1)

- world: `../../c62work/world_fleco.py`, family `flow-lenia`
- parent: collective/contrib/20261025T1932-c18-fl-drive-bg-sighting; mutation: a second conserved Flow-Lenia matter (predator) whose growth gain is set by a product of digesting prey matter; digested prey matter recycled as dilute prey matter
- run: 401 frames x 25 steps x dt 0.2 = time 2000; grid [160, 160]; wall 421s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/6de1d515-b157-56c9-97ab-8aa81df695be/scratchpad/c62work/world_fleco.py --out /tmp/claude-0/-home-user-physim/6de1d515-b157-56c9-97ab-8aa81df695be/scratchpad/fl2/fork --seeds 1 --size 160 160 --frames 400 --no-movie`
- segmentation: matter > 0.08 of robust range [0.004, 1.8956], min area 6 px

## Measurements
- components: final 16, mean 16.6, max 31; occupancy final 0.08
- tracks: 1271; persistent (alive >= 50% of run): 0; longest 65 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.37, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 2, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [25, 18, 16], H1 [4, 0, 0]
- motion: 59 long-lived tracks moved >= 1 body length; max speed 0.939/time; max body lengths 22.4
- replication (lineage window K = 20 frames = time 100, default): splits 453, persistent splits 1 (0 more failed only because the siblings re-merged within K), max generation 1, merges 395, merge/split ratio 0.872, nucleations 41
- channel total drift (end/start - 1): [-0.1032, None, -0.0781, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1025 at frame 296: holes 0, rim-vs-core 0.50, rim-vs-outside 0.09, heterogeneity 0.13; core [0.473, 0.047, 0.349, 0.0] rim [0.036, 0.047, 0.582, 0.0]
  - track 52 at frame 54: holes 0, rim-vs-core 0.56, rim-vs-outside 0.15, heterogeneity 0.12; core [0.606, 0.001, 0.277, 0.018] rim [0.092, 0.008, 0.506, 0.014]
  - track 1016 at frame 286: holes 0, rim-vs-core 0.48, rim-vs-outside 0.09, heterogeneity 0.13; core [0.458, 0.062, 0.348, 0.0] rim [0.035, 0.063, 0.582, 0.0]
  - track 1232 at frame 390: holes 0, rim-vs-core 0.53, rim-vs-outside 0.07, heterogeneity 0.14; core [0.537, 0.058, 0.349, 0.0] rim [0.053, 0.058, 0.575, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 98 components >= 12 px at frames [67, 134, 202, 266, 333, 400]):
  - radial prey A: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 0.922, rim/outside 12.4 (aggregate of 98 individuals; 25/98 membrane-like individually; rim level 0.341)
  - radial predator B: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.13, rim/outside 3.03 (aggregate of 98 individuals; 10/98 membrane-like individually; rim level 0.172)
  - radial food: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 2.12, rim/outside 0.894 (aggregate of 98 individuals; 0/98 membrane-like individually; rim level 0.687)
  - radial digestion q: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.857, rim/outside 2.76 (aggregate of 98 individuals; 0/98 membrane-like individually; rim level 0.0762)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #1025 (t=1480, R_eq 4.79): none; #52 (t=270, R_eq 3.74): none; #1016 (t=1430, R_eq 5.53): none; #1232 (t=1950, R_eq 4.85): none
- species `prey` (channels ['prey A'], own threshold): components final 16, mean 15.4, max 20; tracks 633, persistent 0; splits 208, persistent splits 2 (K=20), max generation 2, merges 190, merge/split 0.913; moving tracks 89
- species `predator` (channels ['predator B'], own threshold): components final 0, mean 4.1, max 13; tracks 125, persistent 0; splits 33, persistent splits 0 (K=20), max generation 0, merges 35, merge/split 1.06; moving tracks 19

## Warnings
- none

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
