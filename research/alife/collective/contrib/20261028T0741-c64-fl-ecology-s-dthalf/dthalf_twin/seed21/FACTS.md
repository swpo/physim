# Evidence pack: flow-lenia-digestion-ecology-dt (seed 21)

- world: `../../../../../home/user/physim/research/alife/collective/contrib/20261028T0326-c62-flow-lenia-ecology-robustness/world_dt.py`, family `flow-lenia`
- parent: collective/contrib/20261025T1932-c18-fl-drive-bg-sighting; mutation: a second conserved Flow-Lenia matter (predator) whose growth gain is set by a product of digesting prey matter; digested prey matter recycled as dilute prey matter
- run: 601 frames x 50 steps x dt 0.1 (--dt; world META dt 0.2) = time 3000; grid [160, 160]; wall 671s; status ok
- command: `python -m labkit.run collective/contrib/20261028T0326-c62-flow-lenia-ecology-robustness/world_dt.py --out /tmp/claude-0/dt/dthalf_twin/seed21 --seeds 21 --size 160 160 --frames 600 --spf 50 --dt 0.1 --no-movie`
- segmentation: matter > 0.09 of robust range [0.001, 1.6826], min area 6 px

## Measurements
- components: final 20, mean 20.5, max 28; occupancy final 0.08
- tracks: 2885; persistent (alive >= 50% of run): 0; longest 38 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 5, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [38, 24, 20], H1 [9, 2, 0]
- motion: 44 long-lived tracks moved >= 1 body length; max speed 1.14/time; max body lengths 25.3
- replication (lineage window K = 20 frames = time 100, default): splits 998, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 1000, merge/split ratio 1, nucleations 31
- channel total drift (end/start - 1): [0.0, None, -0.0931, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 2229 at frame 494: holes 0, rim-vs-core 0.57, rim-vs-outside 0.10, heterogeneity 0.12; core [0.612, 0.0, 0.211, 0.0] rim [0.077, 0.0, 0.402, 0.0]
  - track 1164 at frame 277: holes 0, rim-vs-core 0.60, rim-vs-outside 0.11, heterogeneity 0.14; core [0.627, 0.0, 0.364, 0.0] rim [0.066, 0.0, 0.586, 0.0]
  - track 10 at frame 25: holes 0, rim-vs-core 0.62, rim-vs-outside 0.10, heterogeneity 0.14; core [0.628, 0.0, 0.311, 0.0] rim [0.051, 0.0, 0.526, 0.0]
  - track 853 at frame 207: holes 0, rim-vs-core 0.56, rim-vs-outside 0.10, heterogeneity 0.14; core [0.569, 0.0, 0.273, 0.0] rim [0.057, 0.0, 0.499, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 119 components >= 12 px at frames [101, 202, 303, 398, 499, 600]):
  - radial prey A: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.21, rim/outside 26.4 (aggregate of 119 individuals; 42/119 membrane-like individually; rim level 0.55)
  - radial predator B: flat profile (no radial structure; level 0; aggregate of 119 individuals)
  - radial food: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 2.99, rim/outside 0.857 (aggregate of 119 individuals; 0/119 membrane-like individually; rim level 0.597)
  - radial digestion q: flat profile (no radial structure; level 0; aggregate of 119 individuals)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #2229 (t=2470, R_eq 4.65): none; #1164 (t=1385, R_eq 4.58): none; #10 (t=125, R_eq 4.44): none; #853 (t=1035, R_eq 5.84): ['prey A']
- species `prey` (channels ['prey A'], own threshold): components final 20, mean 22.1, max 27; tracks 2035, persistent 0; splits 730, persistent splits 2 (K=20), max generation 1, merges 373, merge/split 0.511; moving tracks 95
- species `predator` (channels ['predator B'], own threshold): components final 0, mean 0.0, max 0; tracks 0, persistent 0; splits 0, persistent splits 0 (K=20), max generation 0, merges 0, merge/split n/a; moving tracks 0

## Warnings
- --dt 0.1 only relabels time (world META dt 0.2): the world's integration step is unchanged, so this run is NOT a dt/2 (or any time-step) test; change the world's own step for that
- radial: 2 of 119 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
