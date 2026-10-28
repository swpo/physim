# Evidence pack: phase-membrane-noise (seed 1)

- world: `../../pm_noise.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_membrane; mutation: dynamics noise sd 0.03 per sqrt(t): additive on ['phi'], multiplicative (sd x value) on []
- run: 161 frames x 50 steps x dt 1.0 = time 8000; grid [128, 128]; wall 22s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/pm_noise.py --out /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/packs/phi_0.03_s1 --seeds 1 --frames 160 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5397], min area 6 px

## Measurements
- components: final 15, mean 11.0, max 26; occupancy final 0.33
- tracks: 177; persistent (alive >= 50% of run): 0; longest 65 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 5.73, final 11; holes at thresholds 0.2/0.35/0.5 final [0, 13, 13]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [18, 16, 15], H1 [14, 14, 9]
- motion: 2 long-lived tracks moved >= 1 body length; max speed 0.0111/time; max body lengths 1.2
- replication (lineage window K = 20 frames = time 1000, default): splits 52, persistent splits 16 (0 more failed only because the siblings re-merged within K), max generation 4, merges 6, merge/split ratio 0.115, nucleations 26
- channel total drift (end/start - 1): [-0.4886, -0.6894, 0.0535, 0.1764]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 120 at frame 129: holes 0, rim-vs-core 0.40, rim-vs-outside 0.77, heterogeneity 0.20; core [0.085, 0.768, 0.501, 0.594] rim [0.287, 0.432, 0.537, 0.647]
  - track 103 at frame 101: holes 1, rim-vs-core 0.21, rim-vs-outside 0.79, heterogeneity 0.19; core [0.076, 0.792, 0.492, 0.539] rim [0.155, 0.608, 0.494, 0.61]
  - track 125 at frame 133: holes 1, rim-vs-core 0.30, rim-vs-outside 0.60, heterogeneity 0.18; core [0.106, 0.709, 0.519, 0.72] rim [0.219, 0.508, 0.496, 0.524]
  - track 160 at frame 148: holes 1, rim-vs-core 0.41, rim-vs-outside 0.86, heterogeneity 0.22; core [0.106, 0.884, 0.638, 0.576] rim [0.244, 0.526, 0.514, 0.625]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 68 components >= 12 px at frames [27, 54, 81, 106, 133, 160]):
  - radial S: peak at rho=1.65 (OUTSIDE the peak band 0.5-1.5), rim/core 9.3, rim/outside 0.893 (aggregate of 68 individuals; 0/68 membrane-like individually; rim level 0.492)
  - radial K catalyst: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.04, rim/outside 4.59 (aggregate of 68 individuals; 2/68 membrane-like individually; rim level 0.706)
  - radial L link: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.66, rim/outside 3.83 (aggregate of 68 individuals; 56/68 membrane-like individually; rim level 0.564)  MEMBRANE-LIKE
  - radial membrane (wall): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.93, rim/outside 3.25 (aggregate of 68 individuals; 51/68 membrane-like individually; rim level 0.634)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): L link, membrane (wall)
- membrane-like channels per top track at mid-life: #120 (t=6450, R_eq 9.3): ['L link', 'membrane (wall)']; #103 (t=5050, R_eq 12.72, ring): ['L link', 'membrane (wall)']; #125 (t=6650, R_eq 9.24, ring): ['L link', 'membrane (wall)']; #160 (t=7400, R_eq 7.9): ['L link', 'membrane (wall)']

## Warnings
- matter fills >80% of the domain at some point: components may be one connected sea
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 30 of 68 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
