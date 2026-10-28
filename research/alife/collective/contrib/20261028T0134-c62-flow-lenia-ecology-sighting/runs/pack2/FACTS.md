# Evidence pack: flow-lenia-digestion-ecology (seed 2)

- world: `../../c62work/world_fleco.py`, family `flow-lenia`
- parent: collective/contrib/20261025T1932-c18-fl-drive-bg-sighting; mutation: a second conserved Flow-Lenia matter (predator) whose growth gain is set by a product of digesting prey matter; digested prey matter recycled as dilute prey matter
- run: 401 frames x 25 steps x dt 0.2 = time 2000; grid [160, 160]; wall 415s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/6de1d515-b157-56c9-97ab-8aa81df695be/scratchpad/c62work/world_fleco.py --out /tmp/claude-0/-home-user-physim/6de1d515-b157-56c9-97ab-8aa81df695be/scratchpad/fl2/pack --seeds 2 --size 160 160 --frames 400 --no-movie`
- segmentation: matter > 0.08 of robust range [0.0033, 1.9316], min area 6 px

## Measurements
- components: final 16, mean 17.8, max 30; occupancy final 0.14
- tracks: 1596; persistent (alive >= 50% of run): 0; longest 48 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 1.26, final 1; holes at thresholds 0.2/0.35/0.5 final [5, 7, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [28, 16, 12], H1 [12, 2, 0]
- motion: 28 long-lived tracks moved >= 1 body length; max speed 0.896/time; max body lengths 20.5
- replication (lineage window K = 20 frames = time 100, default): splits 552, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 472, merge/split ratio 0.855, nucleations 69
- channel total drift (end/start - 1): [-0.0625, None, -0.0773, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 787 at frame 215: holes 0, rim-vs-core 0.37, rim-vs-outside 0.29, heterogeneity 0.14; core [0.585, 0.001, 0.352, 0.006] rim [0.241, 0.004, 0.493, 0.005]
  - track 1152 at frame 313: holes 0, rim-vs-core 0.55, rim-vs-outside 0.14, heterogeneity 0.13; core [0.581, 0.001, 0.293, 0.006] rim [0.079, 0.006, 0.517, 0.004]
  - track 1200 at frame 323: holes 0, rim-vs-core 0.33, rim-vs-outside 0.18, heterogeneity 0.10; core [0.007, 0.519, 0.854, 0.061] rim [0.009, 0.186, 0.851, 0.047]
  - track 715 at frame 188: holes 0, rim-vs-core 0.20, rim-vs-outside 0.10, heterogeneity 0.07; core [0.275, 0.001, 0.383, 0.008] rim [0.145, 0.002, 0.534, 0.008]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 107 components >= 12 px at frames [67, 134, 202, 266, 333, 400]):
  - radial prey A: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 0.937, rim/outside 11.1 (aggregate of 107 individuals; 26/107 membrane-like individually; rim level 0.299)
  - radial predator B: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.13, rim/outside 4.03 (aggregate of 107 individuals; 29/107 membrane-like individually; rim level 0.156)
  - radial food: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.68, rim/outside 0.912 (aggregate of 107 individuals; 0/107 membrane-like individually; rim level 0.72)
  - radial digestion q: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.771, rim/outside 3.04 (aggregate of 107 individuals; 2/107 membrane-like individually; rim level 0.0709)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #787 (t=1075, R_eq 5.44): ['prey A']; #1152 (t=1565, R_eq 4.15): none; #1200 (t=1615, R_eq 5.29): ['predator B']; #715 (t=940, R_eq 4.82): none
- species `prey` (channels ['prey A'], own threshold): components final 14, mean 15.5, max 20; tracks 759, persistent 0; splits 250, persistent splits 1 (K=20), max generation 1, merges 221, merge/split 0.884; moving tracks 81
- species `predator` (channels ['predator B'], own threshold): components final 3, mean 7.6, max 14; tracks 241, persistent 1; splits 72, persistent splits 3 (K=20), max generation 2, merges 70, merge/split 0.972; moving tracks 33

## Warnings
- radial: 4 of 107 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
