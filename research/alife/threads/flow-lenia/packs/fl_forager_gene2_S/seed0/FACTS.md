# Evidence pack: fl_forager_gene2 (seed 0)

- world: `../../../worlds/fl_forager_gene2/world.py`, family `flow-lenia`
- parent: flow-lenia/fl_forager_gene (committee r2 audit design; body-scale phenotype arm after autopoiesis r2 arm E); mutation: mutation timing/draws on their own RNG stream (identical-event twins), events logged with the hit body fraction; optional body-scale phenotype g_eff = blur(A g)/blur(A)
- run: 301 frames x 40 steps x dt 0.2 = time 2400; grid [128, 128]; wall 507s; status ok
- command: `python -m labkit.run threads/flow-lenia/worlds/fl_forager_gene2/world.py --out threads/flow-lenia/packs/fl_forager_gene2_S/seed0 --frames 300 --seeds 0`
- segmentation: matter > 0.07 of robust range [0.0, 2.2334], min area 6 px

## Measurements
- components: final 18, mean 12.7, max 20; occupancy final 0.13
- tracks: 1018; persistent (alive >= 50% of run): 0; longest 40 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.06, final 0; holes at thresholds 0.2/0.35/0.5 final [1, 3, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [39, 26, 18], H1 [11, 3, 0]
- motion: 9 long-lived tracks moved >= 1 body length; max speed 0.494/time; max body lengths 12.8
- replication (lineage window K = 20 frames = time 160, default): splits 378, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 340, merge/split ratio 0.899, nucleations 4
- channel total drift (end/start - 1): [-0.3376, 15.8269, -0.7396]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 2 at frame 23: holes 0, rim-vs-core 0.49, rim-vs-outside 0.36, heterogeneity 0.24; core [0.75, 0.354, 0.488] rim [0.324, 0.122, 0.578]
  - track 34 at frame 68: holes 0, rim-vs-core 0.46, rim-vs-outside 0.34, heterogeneity 0.20; core [0.732, 0.314, 0.389] rim [0.331, 0.098, 0.398]
  - track 116 at frame 116: holes 0, rim-vs-core 0.50, rim-vs-outside 0.08, heterogeneity 0.16; core [0.262, 0.513, 0.207] rim [0.032, 0.068, 0.215]
  - track 108 at frame 111: holes 0, rim-vs-core 0.63, rim-vs-outside 0.06, heterogeneity 0.20; core [0.43, 0.539, 0.197] rim [0.036, 0.046, 0.192]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 88 components >= 12 px at frames [50, 101, 151, 199, 250, 300]):
  - radial low g: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.31, rim/outside 16.4 (aggregate of 88 individuals; 37/88 membrane-like individually; rim level 0.271)
  - radial high g: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.23, rim/outside 24.6 (aggregate of 88 individuals; 41/88 membrane-like individually; rim level 0.445)
  - radial food: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.12, rim/outside 0.944 (aggregate of 88 individuals; 0/88 membrane-like individually; rim level 0.149)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #2 (t=184, R_eq 7.36): ['low g', 'high g']; #34 (t=544, R_eq 6.38): ['low g', 'high g']; #116 (t=928, R_eq 4.58): none; #108 (t=888, R_eq 4.55): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 1 of 88 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
