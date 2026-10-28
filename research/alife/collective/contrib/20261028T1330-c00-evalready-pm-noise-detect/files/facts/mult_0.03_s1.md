# Evidence pack: phase-membrane-noise (seed 1)

- world: `../../pm_noise.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_membrane; mutation: dynamics noise sd 0.03 per sqrt(t): additive on ['phi'], multiplicative (sd x value) on ['S', 'K', 'L']
- run: 161 frames x 50 steps x dt 1.0 = time 8000; grid [128, 128]; wall 31s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/pm_noise.py --out /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/packs/mult_0.03_s1 --seeds 1 --frames 160 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5443], min area 6 px

## Measurements
- components: final 16, mean 7.4, max 26; occupancy final 0.38
- tracks: 344; persistent (alive >= 50% of run): 0; longest 47 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 2.99, final 10; holes at thresholds 0.2/0.35/0.5 final [0, 13, 15]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [22, 17, 16], H1 [19, 16, 6]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 1.2
- replication (lineage window K = 20 frames = time 1000, default): splits 44, persistent splits 2 (0 more failed only because the siblings re-merged within K), max generation 1, merges 11, merge/split ratio 0.25, nucleations 209
- channel total drift (end/start - 1): [-0.5134, -0.6623, 0.1371, 0.3515]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 297 at frame 137: holes 0, rim-vs-core 0.57, rim-vs-outside 0.82, heterogeneity 0.24; core [0.273, 0.893, 0.926, 0.773] rim [0.364, 0.499, 0.573, 0.581]
  - track 310 at frame 144: holes 1, rim-vs-core 0.30, rim-vs-outside 0.90, heterogeneity 0.21; core [0.067, 0.823, 0.487, 0.416] rim [0.167, 0.623, 0.525, 0.611]
  - track 311 at frame 144: holes 1, rim-vs-core 0.27, rim-vs-outside 0.74, heterogeneity 0.18; core [0.098, 0.744, 0.544, 0.704] rim [0.195, 0.521, 0.489, 0.59]
  - track 286 at frame 124: holes 1, rim-vs-core 0.22, rim-vs-outside 0.75, heterogeneity 0.21; core [0.09, 0.84, 0.564, 0.498] rim [0.166, 0.65, 0.516, 0.563]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 44 components >= 12 px at frames [27, 54, 81, 106, 133, 160]):
  - radial S: peak at rho=1.75 (OUTSIDE the peak band 0.5-1.5), rim/core 6.22, rim/outside 0.791 (aggregate of 44 individuals; 0/44 membrane-like individually; rim level 0.404)
  - radial K catalyst: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.04, rim/outside 3.9 (aggregate of 44 individuals; 3/44 membrane-like individually; rim level 0.654)
  - radial L link: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.43, rim/outside 3.78 (aggregate of 44 individuals; 25/44 membrane-like individually; rim level 0.501)
  - radial membrane (wall): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.55, rim/outside 3.36 (aggregate of 44 individuals; 28/44 membrane-like individually; rim level 0.537)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): membrane (wall)
- membrane-like channels per top track at mid-life: #297 (t=6850, R_eq 4.92): ['membrane (wall)']; #310 (t=7200, R_eq 10.6, ring): ['L link', 'membrane (wall)']; #311 (t=7200, R_eq 9.74, ring): ['L link', 'membrane (wall)']; #286 (t=6200, R_eq 13.63, ring): ['L link', 'membrane (wall)']

## Warnings
- matter fills >80% of the domain at some point: components may be one connected sea
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 17 of 44 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
