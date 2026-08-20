# l0-evolver — evolutionary dynamics on the L0 genome space (phase 3)

Working dir: probes/blobs/l0/evolve/. Shared format: ../lib/genome.py (l0-sampler's;
imported, never forked — operators_lib.py works directly on it).

## Deliverable status (running log; scorecard when >=3 generations done)

### Infrastructure
- engine.py: own IMEX-FFT genome simulator (written while waiting for lib/;
  now superseded by lib/genome.py run_genome for all evolution assays; kept
  for the validation-gate rows already logged + relaxed-channel seeding ref).
- metrics.py: LOCKED v1.2 (own-battery era) + A4 cross-assay convention;
  assays_x.py ports A4 to the lib stack (d0=10 T=800 L=64, dress-per-A1-variant,
  kick (90,0.5) on first act; rotor/cross_bond/repel/drift/die classes).
- operators_lib.py: mutation (log-jitter tau/D/Du, FOLD-DISTANCE k1 jitter --
  sampler's measured lesson, structural add/del W/K edges, bilin jitter,
  u0 continuation) + 3 merge modes (share_chan / cross_edge / slow_tanh).

### VALIDATION GATE (mandate: reconstruct our own history first) — ALL PASS
results.json kinds=val_gate:
- V1 EXACT: merge_share_chan(iso_A' d=.65, iso_B d=.75) == certified vvw pair
  genome up to channel permutation (own fmt) and == ref_VVW for (d=0, d=.75)
  (lib fmt). Behavior: lone areas 35.0/30.0 px^2 vs certified 36.25/30.25
  (3%/1%), A-B pair repels 12->16.5, flavor conserved. PASS.
- V1b HONEST DIRECTION: naive merge(M0,M0)+share-w FAILS exactly as M3 history
  records (sum-drive -> replication soup via w-screening du2/dw=-3.1;
  avg-drive -> island relocation, lone M0 spot dies/balloons). The iso-line is
  REQUIRED — operator reproduces both the jump and the documented dead end. PASS.
- V2 EXACT: merge_cross_edge(M4 tau=5.7, M4 tau=2.5, eta=.1) == certified xv
  rotor genome. Behavior (certified protocol kick (90,.5), d0=8): omega_late
  = -0.011064 vs certified -0.011067 (0.03%), sep 8.438+-0.004 vs 8.439,
  ncomp 1/1 at T=3000. PASS.
- V2b BONUS: cheap Gaussian pokes (no stamps) fall onto the SAME rotor
  attractor: omega -0.01106, sep 8.439 by T~300 — evolution assays are
  stamp-free. Also reproduced via lib stack A4 (assays_x): ref_XV -> cls=rotor
  omega=-0.011063.

### Evolution loop (evolve.py)
MAP-Elites: shared archive ../archive.json (sampler descriptor 8-tuple,
exemplar = most negative G0a margin) + extended archive_x.json (descriptor +
cross_sig). Population: refs (M0/M4x3/VVW/XV/BFIELD/iso x2) + alive archive
cells. Children: 50% mutate / 50% merge (mode uniform; post-merge mutation
35%). Lineage logged per child (parents + op + params). Budget caps:
n_act<=3, n_chan<=7-8.

Smoke (esmoke_9000/9001): mutate->persist|bond child (NEW cell),
merge_slow_tanh->2-species persist|persist repel child (NEW cell, A4 X:replicate).

### Comparison currency (for the research question)
n_assays per child logged (a1 panel runs + a2 + a3 + a4); yield =
new-cells-per-100-assays evolver vs sampler curves (data/yield_*.json).
