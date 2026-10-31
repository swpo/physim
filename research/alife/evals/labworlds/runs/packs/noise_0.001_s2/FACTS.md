# Evidence pack: phase-membrane-noise (seed 2)

- world: `../../pm_noise.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_membrane; mutation: additive dynamics noise sd 0.001 per sqrt(t) on ['S', 'K', 'L', 'phi']
- run: 161 frames x 50 steps x dt 1.0 = time 8000; grid [128, 128]; wall 30s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/pm_noise.py --out /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/packs/noise_0.001_s2 --seeds 2 --frames 160 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0025, 1.5353], min area 6 px

## Measurements
- components: final 14, mean 13.9, max 22; occupancy final 0.30
- tracks: 126; persistent (alive >= 50% of run): 7; longest 104 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 11.45 (1 = constant size)
- enclosures: components with a hole mean 9.60, final 11; holes at thresholds 0.2/0.35/0.5 final [1, 11, 12]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [17, 14, 14], H1 [13, 12, 10]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 0.00636/time; max body lengths 1.5
- replication (lineage window K = 20 frames = time 1000, default): splits 48, persistent splits 6 (0 more failed only because the siblings re-merged within K), max generation 3, merges 4, merge/split ratio 0.083, nucleations 0
- channel total drift (end/start - 1): [-0.5017, -0.6861, 0.1209, -0.2411]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 70 at frame 109: holes 0, rim-vs-core 0.30, rim-vs-outside 0.97, heterogeneity 0.16; core [0.07, 0.733, 0.423, 0.586] rim [0.194, 0.564, 0.548, 0.757]
  - track 66 at frame 97: holes 1, rim-vs-core 0.18, rim-vs-outside 0.80, heterogeneity 0.19; core [0.102, 0.764, 0.57, 0.659] rim [0.168, 0.617, 0.521, 0.605]
  - track 40 at frame 58: holes 1, rim-vs-core 0.20, rim-vs-outside 0.82, heterogeneity 0.19; core [0.091, 0.784, 0.536, 0.616] rim [0.168, 0.601, 0.512, 0.618]
  - track 114 at frame 149: holes 1, rim-vs-core 0.26, rim-vs-outside 0.82, heterogeneity 0.21; core [0.109, 0.843, 0.621, 0.594] rim [0.189, 0.612, 0.522, 0.604]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 85 components >= 12 px at frames [27, 54, 81, 106, 133, 160]):
  - radial S: peak at rho=1.65 (OUTSIDE the peak band 0.5-1.5), rim/core 14.2, rim/outside 0.832 (aggregate of 85 individuals; 0/85 membrane-like individually; rim level 0.456)
  - radial K catalyst: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.05, rim/outside 5.08 (aggregate of 85 individuals; 0/85 membrane-like individually; rim level 0.721)
  - radial L link: peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.74, rim/outside 3.61 (aggregate of 85 individuals; 72/85 membrane-like individually; rim level 0.549)  MEMBRANE-LIKE
  - radial membrane (wall): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 2.93, rim/outside 4.15 (aggregate of 85 individuals; 75/85 membrane-like individually; rim level 0.62)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): L link, membrane (wall)
- membrane-like channels per top track at mid-life: #70 (t=5450, R_eq 10.6): none; #66 (t=4850, R_eq 11.01, ring): ['L link', 'membrane (wall)']; #40 (t=2900, R_eq 11.06, ring): ['L link', 'membrane (wall)']; #114 (t=7450, R_eq 9.18, ring): ['L link', 'membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 59 of 85 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
