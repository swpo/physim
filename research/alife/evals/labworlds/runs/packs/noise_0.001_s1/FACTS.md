# Evidence pack: phase-membrane-noise (seed 1)

- world: `../../pm_noise.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_membrane; mutation: additive dynamics noise sd 0.001 per sqrt(t) on ['S', 'K', 'L', 'phi']
- run: 161 frames x 50 steps x dt 1.0 = time 8000; grid [128, 128]; wall 32s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/pm_noise.py --out /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/packs/noise_0.001_s1 --seeds 1 --frames 160 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0026, 1.5413], min area 6 px

## Measurements
- components: final 20, mean 16.9, max 27; occupancy final 0.29
- tracks: 142; persistent (alive >= 50% of run): 2; longest 113 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 32.68 (1 = constant size)
- enclosures: components with a hole mean 10.53, final 7; holes at thresholds 0.2/0.35/0.5 final [1, 7, 12]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [21, 20, 20], H1 [14, 12, 6]
- motion: 6 long-lived tracks moved >= 1 body length; max speed 0.0135/time; max body lengths 1.3
- replication (lineage window K = 20 frames = time 1000, default): splits 53, persistent splits 9 (0 more failed only because the siblings re-merged within K), max generation 2, merges 10, merge/split ratio 0.189, nucleations 0
- channel total drift (end/start - 1): [-0.4742, -0.718, 0.071, -0.0263]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 15 at frame 56: holes 1, rim-vs-core 0.17, rim-vs-outside 0.75, heterogeneity 0.17; core [0.085, 0.708, 0.483, 0.676] rim [0.156, 0.566, 0.488, 0.624]
  - track 83 at frame 109: holes 1, rim-vs-core 0.18, rim-vs-outside 0.83, heterogeneity 0.18; core [0.075, 0.725, 0.451, 0.633] rim [0.171, 0.589, 0.513, 0.63]
  - track 60 at frame 46: holes 1, rim-vs-core 0.32, rim-vs-outside 0.72, heterogeneity 0.21; core [0.119, 0.817, 0.634, 0.637] rim [0.213, 0.557, 0.49, 0.568]
  - track 107 at frame 125: holes 1, rim-vs-core 0.21, rim-vs-outside 0.84, heterogeneity 0.22; core [0.104, 0.833, 0.599, 0.57] rim [0.194, 0.645, 0.544, 0.575]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 103 components >= 12 px at frames [27, 54, 81, 106, 133, 160]):
  - radial S: peak at rho=1.65 (OUTSIDE the peak band 0.5-1.5), rim/core 12.1, rim/outside 0.887 (aggregate of 103 individuals; 0/103 membrane-like individually; rim level 0.455)
  - radial K catalyst: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.04, rim/outside 4.74 (aggregate of 103 individuals; 0/103 membrane-like individually; rim level 0.712)
  - radial L link: peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.72, rim/outside 3.47 (aggregate of 103 individuals; 86/103 membrane-like individually; rim level 0.565)  MEMBRANE-LIKE
  - radial membrane (wall): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 2.75, rim/outside 3.86 (aggregate of 103 individuals; 86/103 membrane-like individually; rim level 0.652)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): L link, membrane (wall)
- membrane-like channels per top track at mid-life: #15 (t=2800, R_eq 13.15, ring): ['L link', 'membrane (wall)']; #83 (t=5450, R_eq 11.21): ['L link']; #60 (t=2300, R_eq 9.29, ring): ['L link', 'membrane (wall)']; #107 (t=6250, R_eq 10.12, ring): ['L link', 'membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 66 of 103 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
