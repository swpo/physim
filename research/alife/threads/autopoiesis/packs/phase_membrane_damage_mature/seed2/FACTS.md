# Evidence pack: phase-membrane (seed 2)

- world: `../../../worlds/phase_membrane/world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_protocell_noise; mutation: links adsorb to the wall (drift chi up grad of 4 phi(1-phi)); parent: unstructured initial condition: smoothed Gaussian noise phi (mean 0, sd 0.2), uniform random K in [0,0.6] and L in [0,0.1] everywhere
- run: 161 frames x 50 steps x dt 1.0 = time 8000; grid [128, 128]; wall 12s; status ok
- command: `python -m labkit.run threads/autopoiesis/worlds/phase_membrane/world.py --out threads/autopoiesis/packs/phase_membrane_damage_mature/seed2 --seeds 2 --frames 160 --damage 120:0.3 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.548], min area 6 px

## Measurements
- components: final 16, mean 16.0, max 22; occupancy final 0.25
- tracks: 140; persistent (alive >= 50% of run): 7; longest 120 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 13.74 (1 = constant size)
- enclosures: components with a hole mean 10.11, final 8; holes at thresholds 0.2/0.35/0.5 final [2, 8, 11]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [19, 16, 16], H1 [13, 12, 6]
- motion: 4 long-lived tracks moved >= 1 body length; max speed 0.0075/time; max body lengths 1.6
- replication (lineage window K = 20 frames = time 1000, default): splits 53, persistent splits 9 (0 more failed only because the siblings re-merged within K), max generation 2, merges 7, merge/split ratio 0.132, nucleations 0
- channel total drift (end/start - 1): [-0.4368, -0.7333, -0.0582, -0.375]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 65 at frame 101: holes 1, rim-vs-core 0.26, rim-vs-outside 0.69, heterogeneity 0.19; core [0.103, 0.739, 0.553, 0.689] rim [0.191, 0.535, 0.474, 0.568]
  - track 85 at frame 104: holes 0, rim-vs-core 0.38, rim-vs-outside 0.86, heterogeneity 0.18; core [0.091, 0.76, 0.513, 0.612] rim [0.274, 0.44, 0.551, 0.692]
  - track 73 at frame 87: holes 1, rim-vs-core 0.15, rim-vs-outside 0.76, heterogeneity 0.16; core [0.078, 0.655, 0.43, 0.726] rim [0.149, 0.574, 0.477, 0.627]
  - track 94 at frame 117: holes 1, rim-vs-core 0.17, rim-vs-outside 0.76, heterogeneity 0.18; core [0.098, 0.726, 0.538, 0.685] rim [0.153, 0.594, 0.491, 0.614]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 97 components >= 12 px at frames [27, 54, 81, 106, 133, 160]; 3 components of the damaged lineage after the cut left out):
  - radial S: peak at rho=1.65 (OUTSIDE the peak band 0.5-1.5), rim/core 12.6, rim/outside 0.855 (aggregate of 97 individuals; 0/97 membrane-like individually; rim level 0.467)
  - radial K catalyst: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.04, rim/outside 5.21 (aggregate of 97 individuals; 0/97 membrane-like individually; rim level 0.721)
  - radial L link: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.73, rim/outside 4.22 (aggregate of 97 individuals; 85/97 membrane-like individually; rim level 0.569)  MEMBRANE-LIKE
  - radial membrane (wall): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 2.71, rim/outside 4.23 (aggregate of 97 individuals; 82/97 membrane-like individually; rim level 0.642)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): L link, membrane (wall)
- membrane-like channels per top track at mid-life: #65 (t=5050, R_eq 9.69, ring): ['L link', 'membrane (wall)']; #85 (t=5200, R_eq 8.29): ['L link', 'membrane (wall)']; #73 (t=4350, R_eq 12.8, ring): ['L link', 'membrane (wall)']; #94 (t=5850, R_eq 12.74, ring): ['L link', 'membrane (wall)']
- damage `core` (requested 0.30 of the area) at frame 120 (t=6000): target track #85 (rule mature-compact: track age 69 frames vs K=20, area 263 px = 0.86x median, aspect 1.04); mask 78 px (56 inside the component)
- damage MEASURED: the target lost 31.8% of its matter (85 of 263 px lost > half their matter); matter lost outside it = 3.03% of its matter; share of all lost matter that was under labkit's mask 0.22
- after damage, area of the individual's largest piece / area before the cut at t=[6000.0, 6400.0, 6800.0, 7200.0, 7600.0, 8000.0]: target #85 [0.656, 1.035, 1.429, 1.807, 2.467, 0.934]; comparator #105 [1.011, 0.382, 0.7, 1.112, None, None] (followed through its own splits and re-merges; None = died or merged with another individual); target lineage tracks [132, 133, 134, 135]; baseline recorded frame 119 (damage.png)

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 60 of 97 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual
- the world's damage() hook did not erase where labkit's mask was (only 22% of the lost matter was under it): the MEASURED loss is what counts

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, damage.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
