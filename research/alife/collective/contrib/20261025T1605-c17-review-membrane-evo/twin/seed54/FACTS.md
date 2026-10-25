# Evidence pack: membrane-evo (seed 54)

- world: `../../world_twin.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/membrane_kinds (arm E of committee r2); identical-event design from fisim-beyond-laplacian xcell-evo2-S; mutation: kinds differ only in link yield b2; sealed catalyst channel (min face gate, fast outside decay); whole-cell flips + neutral tag + random disk deaths from a state-independent RNG
- run: 161 frames x 250 steps x dt 1.0 = time 40000; grid [128, 128]; wall 95s; status ok
- command: `python -m labkit.run collective/contrib/c17-mevo-wip/world_twin.py --out collective/contrib/c17-mevo-wip/twin/seed54 --seeds 54 --frames 160 --spf 250 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.7282], min area 6 px

## Measurements
- components: final 15, mean 12.2, max 26; occupancy final 0.26
- tracks: 120; persistent (alive >= 50% of run): 1; longest 92 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 4.43 (1 = constant size)
- enclosures: components with a hole mean 10.93, final 14; holes at thresholds 0.2/0.35/0.5 final [6, 15, 15]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [15, 15, 15], H1 [16, 16, 12]
- motion: 3 long-lived tracks moved >= 1 body length; max speed 0.00353/time; max body lengths 1.6
- replication (lineage window K = 20 frames = time 5000, default): splits 44, persistent splits 13 (0 more failed only because the siblings re-merged within K), max generation 3, merges 2, merge/split ratio 0.045, nucleations 0
- channel total drift (end/start - 1): [-0.7008, None, 0.0416, -0.0943]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 70 at frame 110: holes 1, rim-vs-core 0.45, rim-vs-outside 0.69, heterogeneity 0.22; core [0.874, 0.0, 0.772, 0.507] rim [0.48, 0.0, 0.579, 0.599]
  - track 60 at frame 87: holes 0, rim-vs-core 0.75, rim-vs-outside 0.92, heterogeneity 0.24; core [0.893, 0.0, 0.694, 0.383] rim [0.279, 0.0, 0.611, 0.809]
  - track 65 at frame 94: holes 1, rim-vs-core 0.32, rim-vs-outside 0.75, heterogeneity 0.20; core [0.82, 0.0, 0.63, 0.567] rim [0.513, 0.0, 0.543, 0.62]
  - track 99 at frame 136: holes 1, rim-vs-core 0.36, rim-vs-outside 0.74, heterogeneity 0.21; core [0.822, 0.0, 0.643, 0.53] rim [0.491, 0.0, 0.571, 0.65]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 79 components >= 12 px at frames [27, 54, 81, 106, 133, 160]):
  - radial K1: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.23, rim/outside 9.01 (aggregate of 79 individuals; 17/79 membrane-like individually; rim level 0.566)
  - radial K2: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.02, rim/outside 4.62 (aggregate of 79 individuals; 1/79 membrane-like individually; rim level 0.0692)
  - radial L link: peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.56, rim/outside 5.86 (aggregate of 79 individuals; 65/79 membrane-like individually; rim level 0.513)  MEMBRANE-LIKE
  - radial membrane (wall): peak at rho=0.95 (in the peak band 0.5-1.5), rim/core 5.92, rim/outside 4.07 (aggregate of 79 individuals; 75/79 membrane-like individually; rim level 0.502)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): L link, membrane (wall)
- membrane-like channels per top track at mid-life: #70 (t=27500, R_eq 9.29, ring): ['L link', 'membrane (wall)']; #60 (t=21750, R_eq 7.11): ['membrane (wall)']; #65 (t=23500, R_eq 10.2, ring): ['L link', 'membrane (wall)']; #99 (t=34000, R_eq 8.06, ring): ['L link', 'membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 72 of 79 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
