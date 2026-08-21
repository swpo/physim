# l0-evolver — merge-and-mutate evolution on the L0 genome space (SCORECARD)

Sibling of l0-sampler (phase 3). Shared format/battery: ../lib/ (sampler's,
imported not forked). All rows in evolve/results.json (lineage-logged);
archive contributions in ../archive.json (shared 8-tuple descriptor) and
evolve/archive_x.json (descriptor + cross-encounter signature).

## 1. Operators (operators_lib.py)
MUTATE: log-normal tau/D/Du (sigma .15), FOLD-DISTANCE log-jitter on k1
(adopts sampler's measured lesson: refs sit ~0.03 from the cubic fold),
small lam moves, tanh thr/sc jitter, bilin coeff jitter, u0 continuation
(nearest root), structural micro-moves p=.15 (add/del one W/K edge,
|w|~logU[.02,.2]; never orphans an act's K row or a chan's W row).
MERGE: block direct-sum then ONE coupling move:
  share_chan (vvw-class) / cross_edge (xv-class, eta~logU[.03,.3]) /
  slow_tanh (bfield-class: new shared saturating channel, thr>0 =>
  linearly dead, vacuum-exact). Post-merge mutation p=.35.

## 2. VALIDATION GATE — reconstruct our own history first (ALL PASS)
- V1 vvw: merge_share_chan(iso_A' d=.65, iso_B d=.75) == certified vvw pair
  EXACTLY (up to channel permutation), and behaves: lone areas 35.0/30.0 px^2
  (cert 36.25/30.25 => 3%/1%), A'-B pair repels 12->16.5px, flavor conserved.
  Also lib-format: merge(iso_0, iso_.75) == ref_VVW exact.
- V1b honest inverse: merge(M0,M0)+share-w FAILS both drive conventions
  exactly as M3 history says it must (sum-drive -> replication soup via
  w-screening; avg-drive -> island relocation, spot dies). The operator
  reproduces the jump AND the documented dead end.
- V2 xv: merge_cross_edge(M4 t5.7, M4 t2.5, eta=.1) == certified rotor
  genome EXACTLY; behavior omega=-0.011064 (cert -0.011067, 0.03%),
  sep 8.438+-0.004 (cert 8.439). Lib-format exactness too. BONUS: cheap
  Gaussian pokes (no stamps) land on the same rotor attractor by T~300
  => stamp-free evolution assays (V2b row).

## 3. Evolution runs (this machine, shared with sibling load)
- e1: 3 workers x 18 children = 54 (+2 smoke), 3 generations (REFRESH=6/worker,
  pool re-read from disk; 14/54 children have evolver parents = true lineage).
  50% mutate / 50% merge (mode uniform), parents: refs .3 / alive archive
  cells .55 / any .15. 45/54 assayed, 5 fail_g0a (all share_chan or
  post-mutated merges), 0 blowups, 0 errors.
- rh1 rotor-hunt: 10 targeted cross_edge merges of M4-family refs ONLY
  (taus {4.5,5,5.7,5.9}; certified rotor tau2=2.5 NOT in pool).

## 4. THE ANSWER: does merge-and-mutate find things jitter-sampling does not?
Currency: first-touch shared-archive cells per 100 assay runs (n_assays
logged per child; identical accounting applied to sampler rows).

| strategy         |   n | funnel% | assays | cells | /100a | ALIVE | /100a |
|------------------|----:|--------:|-------:|------:|------:|------:|------:|
| sampler_uniform  | 147 |     85% |    211 |    49 | 23.2  |     4 |  1.9  |
| sampler_jitter   | 143 |     80% |    524 |    42 |  8.0  |    28 |  5.3  |
| evolver_mutate   |  28 |    100% |    189 |     7 |  3.7  |     6 |  3.2  |
| evolver_merge    |  38 |     87% |    246 |    23 |  9.4  |    19 |  7.7  |

(uniform's 23/100a is mostly cheap DEAD cells — die/na descriptors are
diverse; its ALIVE yield is worst. Snapshot at sampler n=290, evolver n=66.)

HEADLINE SPLITS:
- Cells with >=2 COEXISTING alive species (first touch):
  merge 13, jitter 4, uniform 0, mutate 0. Per 100 assays: merge 5.3 vs
  jitter 0.76 — ~7x. EVERY multi-coexist family beyond 2|3 and 2|4 plain
  (i.e. all 3-act worlds, all tanh-channel coexist worlds) is merge-only.
- Cross-encounter physics (A4 assay, archive_x): 5 cross_bond cells,
  2 rotor cells, 5 drift, 3 repel — ALL evolver-discovered (sampler has no
  A4; but note these phenotypes require >=2 coexisting species, which
  jitter found in only 4 cells of 2 plain families).
- ROTOR REDISCOVERY (rh1): child #1 already a NEW rotor point — eta12-only
  =0.202 (asymmetric!), taus (5.9, 5.0), omega=-0.0324, sep 8.72 (certified
  M7 point was symmetric eta=.1, taus (5.7, 2.5), omega -0.0111, sep 8.44).
  10 children: 1 rotor, 2 cross_bond, 4 replicate, 1 drift, 2 dead-ish.
  The general loop ALSO surfaced a rotor without targeting (e1_9513:
  merge_slow_tanh(M0, XV-mutant) + heavy post-mutation -> 3-act world w/
  omega=-0.0323 rotor pair INSIDE a 6-channel genome).
- Triple-persist world (3 coexisting species): e1_9508
  (cross_edge(BFIELD-jitter, VVW) + mutation) — first 3-species world in
  the program.
- HONEST NEGATIVES: (a) plain mutate UNDERPERFORMS sampler-jitter on alive
  yield (3.2 vs 5.3/100a) — same neighborhoods, no recombination gain;
  the value is merge, not mutation. (b) share_chan merges fail G0a 50%
  (5/10) — random pairs don't share a background; the iso-line lesson is
  structural (only same-vacuum parents survive sharing; e.g. M4+M4 or
  iso+iso). (c) cross_edge at eta>~0.15 mostly replicates (rh1 4/10) —
  the certified eta window [.05,.125] generalizes.

VERDICT: merge-and-mutate finds a qualitatively different part of genome
space: multi-species coexistence + cross-species interaction physics
(bonds, rotors) at ~7x jitter's per-assay rate for coexistence cells, and
rediscovers the program's hand-designed jumps (vvw, xv rotor) from raw
parts — while pure parameter mutation is NOT better than the sampler's
jitter. Composition, not perturbation, is where evolution pays.

## 5. Costs (this box, heavily shared: load ~15-28 on 10 cores)
funnel ~0s (median .003s); A1 panel 30-300s; full battery 200-1300s/child;
n_assays/child median 7 (range 2-13). rotorhunt child ~40-190s (A1+A4 only).

## 6. Files
engine.py (own sim, val-gate era), metrics.py (LOCKED v1.3 + amendments),
operators_lib.py, evolve.py (MAP-Elites loop), rotorhunt.py, assays_x.py
(A4 cross assay on lib stack), compare_yield.py, val_history.py /
val_gates_fix.py / val_gates_lib.py (gates), results.json (78 rows),
archive_x.json (48 cells), data/compare_yield.json.
