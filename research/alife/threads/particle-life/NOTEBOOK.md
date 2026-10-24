# particle-life notebook

Sprint 1 started 2026-10-24 14:28 UTC. Engine: `plcore.py` (numba cell lists, periodic box);
quick looks via `screen.py`. Screens in `screens/`.

## S1. Periodic multi-cell Particle Lenia from uniform noise
Reference PL kernel (mu_k=4, sigma_k=1, w=0.022, mu_g=0.6, sigma_g=0.15), periodic L=60.
- N=1000: breaks into a lattice of tiny 4-6 particle clumps, no cells. N=2000: foam/labyrinth
  of ring-like walls with one void; no discrete cells. `screens/s01_pl_N*_L60.png`.
- Reading: the PL cell is a bulk phase with a free surface; G regulates the *local* U, not the
  particle count, so nothing sets a cell size from uniform init. L1 only. Negative result.

## S2. Asymmetric particle life (Ventrella/Mohr force), random matrices
- At ~1 particle per r_max^2 (N=2000, L=40): everything collapses to tiny point clumps. Too
  dilute. `screens/s02_plife_random.png`.
- At ~20 particles per r_max^2 (N=3000, L=12): many matrices spontaneously form persistent
  cell-like clusters with core/shell type layering (m2: white shell around green+orange core;
  m11: concentric yellow shells around orange/pink core). `screens/s02b_plife_random_dense.png`,
  `screens/s03_m2_time.png`, `screens/s03_m11_time.png`. Known result (Ventrella "clusters").

## S3. One-type SALR (second force shell B on [1, R2])
- Uniform start: fixed-size clusters even with B=0 (kinetic arrest: clusters > r_max apart stop
  interacting). B<0 just makes a crystal of clusters. `screens/s04_salr.png`.
- Planted oversized clusters (n=300) shed sub-clusters; n=100 stable unless B<=-1.
  So there is a maximum stable cluster size, lowered by B<0. `screens/s05_bigcluster.png`.

## S4. eatbud: closed particle chemistry (F food gas -> C core, catalysed by C; C -> F decay)
- v0 (5% C seeds, k_dec=0.02): ~70 clusters nucleate, food equilibrates at ~10%, count frozen.
  `screens/e0.png`.
- 0.5% seeds: ~20 clusters reach a bounded size with plenty of food left (surface uptake balances
  bulk decay, a food-depletion halo around each). No division. `screens/e1.png`, `e2.png`.
- Lower decay (0.002-0.005) + B_CC=-1 (to R2=2-2.5) + D_F=0.2: food runs out and the cluster
  count roughly doubles (~20 -> ~35, e6). Mechanism from the sheet: clusters near max size shed
  small streams of C, which catalyse food into new clusters ("spores"), not binary fission.
  labkit pack (scratch/p_eatbud1) under-segments small clusters: 0 splits, 15 nucleations.
