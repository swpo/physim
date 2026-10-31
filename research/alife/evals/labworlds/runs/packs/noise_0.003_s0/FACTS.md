# Evidence pack: phase-membrane-noise (seed 0)

- world: `../../pm_noise.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_membrane; mutation: additive dynamics noise sd 0.003 per sqrt(t) on ['S', 'K', 'L', 'phi']
- run: 161 frames x 50 steps x dt 1.0 = time 8000; grid [128, 128]; wall 31s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/pm_noise.py --out /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/packs/noise_0.003_s0 --seeds 0 --frames 160 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0057, 1.5298], min area 6 px

## Measurements
- components: final 15, mean 10.0, max 26; occupancy final 0.28
- tracks: 128; persistent (alive >= 50% of run): 1; longest 85 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 19.55 (1 = constant size)
- enclosures: components with a hole mean 6.39, final 10; holes at thresholds 0.2/0.35/0.5 final [3, 10, 12]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [15, 15, 15], H1 [15, 14, 8]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 0.00685/time; max body lengths 1.3
- replication (lineage window K = 20 frames = time 1000, default): splits 44, persistent splits 7 (0 more failed only because the siblings re-merged within K), max generation 2, merges 9, merge/split ratio 0.205, nucleations 0
- channel total drift (end/start - 1): [-0.4703, -0.6916, 0.1984, -0.2309]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 23 at frame 43: holes 1, rim-vs-core 0.20, rim-vs-outside 0.75, heterogeneity 0.19; core [0.114, 0.798, 0.614, 0.661] rim [0.163, 0.638, 0.518, 0.594]
  - track 82 at frame 95: holes 0, rim-vs-core 0.49, rim-vs-outside 1.05, heterogeneity 0.21; core [0.07, 0.837, 0.495, 0.449] rim [0.27, 0.564, 0.645, 0.768]
  - track 60 at frame 40: holes 1, rim-vs-core 0.21, rim-vs-outside 0.75, heterogeneity 0.21; core [0.106, 0.793, 0.596, 0.651] rim [0.178, 0.627, 0.518, 0.583]
  - track 98 at frame 132: holes 1, rim-vs-core 0.18, rim-vs-outside 0.78, heterogeneity 0.19; core [0.095, 0.754, 0.529, 0.68] rim [0.174, 0.615, 0.522, 0.605]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 59 components >= 12 px at frames [27, 54, 81, 106, 133, 160]):
  - radial S: peak at rho=1.85 (OUTSIDE the peak band 0.5-1.5), rim/core 11.2, rim/outside 0.756 (aggregate of 59 individuals; 0/59 membrane-like individually; rim level 0.464)
  - radial K catalyst: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.04, rim/outside 7.27 (aggregate of 59 individuals; 1/59 membrane-like individually; rim level 0.712)
  - radial L link: peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.6, rim/outside 3.46 (aggregate of 59 individuals; 47/59 membrane-like individually; rim level 0.524)  MEMBRANE-LIKE
  - radial membrane (wall): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 2.5, rim/outside 6.26 (aggregate of 59 individuals; 50/59 membrane-like individually; rim level 0.575)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): L link, membrane (wall)
- membrane-like channels per top track at mid-life: #23 (t=2150, R_eq 12.72, ring): ['L link', 'membrane (wall)']; #82 (t=4750, R_eq 10.05): none; #60 (t=2000, R_eq 11.9, ring): ['L link', 'membrane (wall)']; #98 (t=6600, R_eq 10.85, ring): ['L link', 'membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 40 of 59 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
