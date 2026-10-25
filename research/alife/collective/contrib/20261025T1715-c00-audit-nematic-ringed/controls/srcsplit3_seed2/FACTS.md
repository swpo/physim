# Evidence pack: active-nematic-droplets-audit-source-split3 (seed 2)

- world: `../worlds/world_srcsplit3.py`, family `active-nematic`
- parent: None; mutation: new class: CH droplets with internal Landau-de Gennes nematic order and extensile active stress, Brinkman-Stokes flow
- run: 121 frames x 100 steps x dt 0.05 = time 600; grid [128, 128]; wall 327s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/audit/nematic-ringed/construction/worlds/world_srcsplit3.py --out /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/audit/nematic-ringed/construction/r6_srcsplit3_seed2 --seeds 2 --frames 120 --no-movie`
- segmentation: matter > 0.57 of robust range [-0.8165, 0.6113], min area 6 px

## Measurements
- components: final 25, mean 14.7, max 25; occupancy final 0.06
- tracks: 66; persistent (alive >= 50% of run): 5; longest 72 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 5.29 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [27, 26, 22], H1 [0, 0, 0]
- motion: 21 long-lived tracks moved >= 1 body length; max speed 0.0712/time; max body lengths 3.7
- replication (lineage window K = 20 frames = time 100, default): splits 26, persistent splits 12 (0 more failed only because the siblings re-merged within K), max generation 2, merges 6, merge/split ratio 0.231, nucleations 8
- channel total drift (end/start - 1): [-0.5102, -0.4675, None, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 21 at frame 74: holes 0, rim-vs-core 0.58, rim-vs-outside 0.38, heterogeneity 0.15; core [0.95, 0.914, 0.556, 0.303, 0.417] rim [0.735, 0.602, 0.772, 0.539, 0.727]
  - track 12 at frame 61: holes 0, rim-vs-core 0.62, rim-vs-outside 0.37, heterogeneity 0.16; core [0.954, 0.923, 0.507, 0.285, 0.44] rim [0.748, 0.633, 0.754, 0.532, 0.802]
  - track 24 at frame 87: holes 0, rim-vs-core 0.52, rim-vs-outside 0.28, heterogeneity 0.12; core [0.938, 0.528, 0.508, 0.393, 0.561] rim [0.759, 0.371, 0.695, 0.635, 0.901]
  - track 7 at frame 56: holes 0, rim-vs-core 0.59, rim-vs-outside 0.38, heterogeneity 0.16; core [0.959, 0.914, 0.604, 0.291, 0.384] rim [0.768, 0.643, 0.888, 0.536, 0.689]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 99 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.815, rim/outside 4.82 (aggregate of 99 individuals; 0/99 membrane-like individually; rim level 0.754)
  - radial order |Q|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.78, rim/outside 7.82 (aggregate of 99 individuals; 1/99 membrane-like individually; rim level 0.631)
  - radial s rod-made (phi>0): peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.26, rim/outside 2.87 (aggregate of 99 individuals; 60/99 membrane-like individually; rim level 0.701)
  - radial s interface-made (-0.5<phi<=0): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.62, rim/outside 1.98 (aggregate of 99 individuals; 74/99 membrane-like individually; rim level 0.484)  MEMBRANE-LIKE
  - radial s far-bath-made (phi<=-0.5): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.7, rim/outside 1.45 (aggregate of 99 individuals; 60/99 membrane-like individually; rim level 0.639)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): s interface-made (-0.5<phi<=0)
- membrane-like channels per top track at mid-life: #21 (t=370, R_eq 3.29): ['s interface-made (-0.5<phi<=0)', 's far-bath-made (phi<=-0.5)']; #12 (t=305, R_eq 3.09): ['s rod-made (phi>0)', 's interface-made (-0.5<phi<=0)', 's far-bath-made (phi<=-0.5)']; #24 (t=435, R_eq 2.33): ['s rod-made (phi>0)', 's interface-made (-0.5<phi<=0)', 's far-bath-made (phi<=-0.5)']; #7 (t=280, R_eq 3.57): ['s interface-made (-0.5<phi<=0)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 2 of 99 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
