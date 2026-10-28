# Evidence pack: flow-lenia-digestion-ecology (seed 1)

- world: `../../c62work/world_fleco.py`, family `flow-lenia`
- parent: collective/contrib/20261025T1932-c18-fl-drive-bg-sighting; mutation: a second conserved Flow-Lenia matter (predator) whose growth gain is set by a product of digesting prey matter; digested prey matter recycled as dilute prey matter
- run: 401 frames x 25 steps x dt 0.2 = time 2000; grid [160, 160]; wall 215s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/6de1d515-b157-56c9-97ab-8aa81df695be/scratchpad/c62work/world_fleco.py --out /tmp/claude-0/-home-user-physim/6de1d515-b157-56c9-97ab-8aa81df695be/scratchpad/fl2/twin --seeds 1 --size 160 160 --frames 400 --no-movie`
- segmentation: matter > 0.08 of robust range [0.0003, 1.8092], min area 6 px

## Measurements
- components: final 13, mean 15.9, max 21; occupancy final 0.08
- tracks: 1002; persistent (alive >= 50% of run): 0; longest 67 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.01, final 0; holes at thresholds 0.2/0.35/0.5 final [1, 10, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [26, 16, 13], H1 [11, 5, 0]
- motion: 63 long-lived tracks moved >= 1 body length; max speed 0.945/time; max body lengths 36.3
- replication (lineage window K = 20 frames = time 100, default): splits 344, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 335, merge/split ratio 0.974, nucleations 4
- channel total drift (end/start - 1): [0.0, None, -0.0775, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 253 at frame 141: holes 0, rim-vs-core 0.55, rim-vs-outside 0.09, heterogeneity 0.12; core [0.568, 0.0, 0.418, 0.0] rim [0.056, 0.0, 0.611, 0.0]
  - track 865 at frame 366: holes 0, rim-vs-core 0.58, rim-vs-outside 0.10, heterogeneity 0.14; core [0.574, 0.0, 0.362, 0.0] rim [0.046, 0.0, 0.592, 0.0]
  - track 323 at frame 155: holes 0, rim-vs-core 0.55, rim-vs-outside 0.11, heterogeneity 0.13; core [0.59, 0.0, 0.349, 0.0] rim [0.074, 0.0, 0.551, 0.0]
  - track 305 at frame 151: holes 0, rim-vs-core 0.54, rim-vs-outside 0.12, heterogeneity 0.14; core [0.547, 0.0, 0.25, 0.0] rim [0.062, 0.0, 0.491, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 103 components >= 12 px at frames [67, 134, 202, 266, 333, 400]):
  - radial prey A: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.12, rim/outside 23.6 (aggregate of 103 individuals; 25/103 membrane-like individually; rim level 0.533)
  - radial predator B: flat profile (no radial structure; level 0; aggregate of 103 individuals)
  - radial food: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 3.21, rim/outside 0.835 (aggregate of 103 individuals; 0/103 membrane-like individually; rim level 0.638)
  - radial digestion q: flat profile (no radial structure; level 0; aggregate of 103 individuals)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #253 (t=705, R_eq 4.72): none; #865 (t=1830, R_eq 5.17): ['prey A']; #323 (t=775, R_eq 4.85): ['prey A']; #305 (t=755, R_eq 6): ['prey A']
- species `prey` (channels ['prey A'], own threshold): components final 13, mean 16.9, max 21; tracks 928, persistent 0; splits 324, persistent splits 1 (K=20), max generation 1, merges 289, merge/split 0.892; moving tracks 88
- species `predator` (channels ['predator B'], own threshold): components final 0, mean 0.0, max 0; tracks 0, persistent 0; splits 0, persistent splits 0 (K=20), max generation 0, merges 0, merge/split n/a; moving tracks 0

## Warnings
- none

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
