# Evidence pack: membrane-evo (seed 21)

- world: `../../../../home/user/physim/research/alife/threads/autopoiesis/worlds/membrane_evo/world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/membrane_kinds (arm E of committee r2); identical-event design from fisim-beyond-laplacian xcell-evo2-S; mutation: kinds differ only in link yield b2; sealed catalyst channel (min face gate, fast outside decay); whole-cell flips + neutral tag + random disk deaths from a state-independent RNG
- run: 161 frames x 250 steps x dt 1.0 = time 40000; grid [128, 128]; wall 92s; status ok
- command: `python -m labkit.run threads/autopoiesis/worlds/membrane_evo/world.py --out /tmp/claude-0/c11rev5/membrane_evo_s21 --seeds 21 --frames 160 --spf 250 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.7262], min area 6 px

## Measurements
- components: final 13, mean 12.5, max 19; occupancy final 0.23
- tracks: 96; persistent (alive >= 50% of run): 1; longest 102 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 9.02 (1 = constant size)
- enclosures: components with a hole mean 11.52, final 12; holes at thresholds 0.2/0.35/0.5 final [7, 12, 12]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [15, 13, 13], H1 [12, 12, 11]
- motion: 8 long-lived tracks moved >= 1 body length; max speed 0.00763/time; max body lengths 2.0
- replication (lineage window K = 20 frames = time 5000, default): splits 38, persistent splits 14 (0 more failed only because the siblings re-merged within K), max generation 2, merges 1, merge/split ratio 0.026, nucleations 1
- channel total drift (end/start - 1): [-0.8373, None, -0.0719, -0.3153]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 37 at frame 95: holes 1, rim-vs-core 0.24, rim-vs-outside 0.75, heterogeneity 0.21; core [0.772, 0.0, 0.616, 0.566] rim [0.534, 0.0, 0.573, 0.608]
  - track 38 at frame 93: holes 1, rim-vs-core 0.37, rim-vs-outside 0.69, heterogeneity 0.22; core [0.827, 0.0, 0.723, 0.526] rim [0.495, 0.0, 0.583, 0.606]
  - track 54 at frame 120: holes 1, rim-vs-core 0.46, rim-vs-outside 0.74, heterogeneity 0.22; core [0.877, 0.0, 0.68, 0.497] rim [0.45, 0.0, 0.573, 0.627]
  - track 45 at frame 110: holes 1, rim-vs-core 0.48, rim-vs-outside 0.70, heterogeneity 0.22; core [0.0, 0.928, 0.641, 0.618] rim [0.0, 0.467, 0.526, 0.653]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 78 components >= 12 px at frames [27, 54, 81, 106, 133, 160]):
  - radial K1: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.14, rim/outside 7.82 (aggregate of 78 individuals; 14/78 membrane-like individually; rim level 0.514)
  - radial K2: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.25, rim/outside 6.49 (aggregate of 78 individuals; 4/78 membrane-like individually; rim level 0.108)
  - radial L link: peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.51, rim/outside 5.63 (aggregate of 78 individuals; 57/78 membrane-like individually; rim level 0.509)  MEMBRANE-LIKE
  - radial membrane (wall): peak at rho=0.95 (in the peak band 0.5-1.5), rim/core 4.81, rim/outside 4.21 (aggregate of 78 individuals; 69/78 membrane-like individually; rim level 0.519)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): L link, membrane (wall)
- membrane-like channels per top track at mid-life: #37 (t=23750, R_eq 10.39, ring): ['L link', 'membrane (wall)']; #38 (t=23250, R_eq 9.11, ring): ['K1', 'L link', 'membrane (wall)']; #54 (t=30000, R_eq 7.76, ring): ['L link', 'membrane (wall)']; #45 (t=27500, R_eq 9.2, ring): ['L link', 'membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 69 of 78 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
