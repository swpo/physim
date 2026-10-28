# Evidence pack: flow-lenia-digestion-ecology (seed 2)

- world: `../../c62work/world_fleco.py`, family `flow-lenia`
- parent: collective/contrib/20261025T1932-c18-fl-drive-bg-sighting; mutation: a second conserved Flow-Lenia matter (predator) whose growth gain is set by a product of digesting prey matter; digested prey matter recycled as dilute prey matter
- run: 401 frames x 25 steps x dt 0.2 = time 2000; grid [160, 160]; wall 495s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/6de1d515-b157-56c9-97ab-8aa81df695be/scratchpad/c62work/world_fleco.py --out /tmp/claude-0/-home-user-physim/6de1d515-b157-56c9-97ab-8aa81df695be/scratchpad/fl2/fork2 --seeds 2 --size 160 160 --frames 400 --no-movie`
- segmentation: matter > 0.08 of robust range [0.0042, 1.8672], min area 6 px

## Measurements
- components: final 13, mean 16.2, max 30; occupancy final 0.07
- tracks: 1241; persistent (alive >= 50% of run): 0; longest 60 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.42, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 2, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [26, 17, 13], H1 [6, 2, 0]
- motion: 41 long-lived tracks moved >= 1 body length; max speed 0.896/time; max body lengths 18.1
- replication (lineage window K = 20 frames = time 100, default): splits 434, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 388, merge/split ratio 0.894, nucleations 44
- channel total drift (end/start - 1): [-0.1071, None, -0.0778, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 983 at frame 303: holes 0, rim-vs-core 0.52, rim-vs-outside 0.27, heterogeneity 0.13; core [0.636, 0.055, 0.214, 0.0] rim [0.173, 0.057, 0.441, 0.0]
  - track 938 at frame 272: holes 0, rim-vs-core 0.46, rim-vs-outside 0.28, heterogeneity 0.14; core [0.597, 0.024, 0.183, 0.0] rim [0.203, 0.024, 0.427, 0.0]
  - track 907 at frame 255: holes 0, rim-vs-core 0.05, rim-vs-outside 0.03, heterogeneity 0.05; core [0.037, 0.174, 0.82, 0.0] rim [0.016, 0.149, 0.855, 0.0]
  - track 1154 at frame 373: holes 0, rim-vs-core 0.47, rim-vs-outside 0.21, heterogeneity 0.14; core [0.529, 0.068, 0.19, 0.0] rim [0.126, 0.067, 0.435, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 96 components >= 12 px at frames [67, 134, 202, 266, 333, 400]):
  - radial prey A: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 0.825, rim/outside 11.9 (aggregate of 96 individuals; 19/96 membrane-like individually; rim level 0.321)
  - radial predator B: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 0.986, rim/outside 2.78 (aggregate of 96 individuals; 11/96 membrane-like individually; rim level 0.158)
  - radial food: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 2.17, rim/outside 0.896 (aggregate of 96 individuals; 0/96 membrane-like individually; rim level 0.693)
  - radial digestion q: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.801, rim/outside 2.35 (aggregate of 96 individuals; 0/96 membrane-like individually; rim level 0.0574)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #983 (t=1515, R_eq 6.08): none; #938 (t=1360, R_eq 6.08): ['prey A']; #907 (t=1275, R_eq 15.8): ['prey A']; #1154 (t=1865, R_eq 7.33): none
- species `prey` (channels ['prey A'], own threshold): components final 14, mean 15.1, max 19; tracks 689, persistent 0; splits 224, persistent splits 0 (K=20), max generation 0, merges 201, merge/split 0.897; moving tracks 85
- species `predator` (channels ['predator B'], own threshold): components final 0, mean 3.9, max 12; tracks 93, persistent 0; splits 24, persistent splits 1 (K=20), max generation 1, merges 22, merge/split 0.917; moving tracks 19

## Warnings
- radial: 2 of 96 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
