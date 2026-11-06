# VW-0: the first two-level supervenient vector world (6 Nov 2026)

A PhySim world as a hierarchy of hidden vectors. Level 0 is a hidden state h0 under a fixed law F0. Level 1 is a
fixed many-to-one coarse-graining h1 = Phi(h0, m), with optional tracking memory m that depends only on the
level-0 history, so level 1 never has independent state. The agent sees only the level-1 vector through a hidden
permutation, and acts blindly by adding constrained vectors to h0 in a hidden permuted basis. Its scored task is
predicting level-1 vectors under held-out input programs. The coarse-graining replaces the hand-built apparatus,
and a few declared input and observation constraints replace the device choices.

## Contents

- `spec/DESIGN.md`: the VW-0 contract (levels, anonymisation, input and observation constraints, the exam,
  designer-side certificates, composition). `spec/vecworld.py`: the generic `VectorWorld` with an agent API and a
  designer API. `spec/lingauss.py` and `spec/calibrate.py`: a linear-Gaussian family with closed-form certificates;
  the estimators match the exact values on seven toy worlds (`spec/calibration/summary.md`); 37 tests pass.
- `level0/flowlenia.py`: Flow-Lenia (Plantec et al. 2023), checked against a transliteration of the authors' code
  to 1e-13 per step; mass drift about 1e-14 over 10^4 steps at 128^2; about 5 ms per step on one core.
  `level0/worlds/`: three worlds found in a search of 450 rules (A_gliders, B_swarm, C_cells).
- `integrate/lenia_world.py`: the two-level example. A_gliders at level 0 (n0 = 32768, one tick = 20 steps) with
  `Phi_objects` (12 tracked slots x 12 features: presence, mass, composition, centroid, size, shape, velocity) and
  `Phi_coarse` (8x8 block means of both channels plus a second moment, n1 = 192). Blind inputs: per-cell matter
  moves, k = 8 non-zero coordinates, values in [-1, 1], total at most 4 per tick, zero sum (mass conserved; A >= 0).
- `integrate/results/`: certificates for A_gliders and B_swarm, learning curves, exam and composition demos.
- `reports/`: the four agents' reports; `reports/check.md` is the independent check, whose corrections are
  applied in the summary below. `review/`: the checker's scripts and results.

Large data (base runs, branches, videos) is not committed; `integrate/run_base.py` regenerates it bit for bit.
Scripts use absolute paths under `/home/user/evalwork/vecworld/` from the build session.

## Results (with the checker's corrections)

- **Closure ceiling** c = (V0 - Vbest)/(V0 - Voracle), best level-1-only predictor against the true simulator from
  the true state, A_gliders:

  | tau (ticks) | 1 | 2 | 4 | 8 | 16 | 32 |
  |---|---|---|---|---|---|---|
  | coarse | 0.99 | 0.95 | 0.79 | 0.34 | 0.04 | 0.01 |
  | objects | 0.81 | 0.63 | 0.51 | 0.26 | 0.13 | 0.04 |

  Coarse is close to closed for tau <= 2. The objects gap at tau = 1 is about three quarters tracker identity events
  (fusions and fissions that h0 foresees but the slots do not); slots with an event at t+1 are 16% of slot-ticks and
  75% of the error. The coarse gap is an upper bound: its learning curve had not saturated.
- **Blind inputs are nearly invisible.** Within the default constraint, the median shift of the level-1 mean is at
  most 0.07 of the oracle spread at every horizon (one state of 12 reaches 1 at tau = 16). Random placement mostly
  lands on empty cells. Designer-chosen inputs placed on bodies can steer a glider: 32 of 36 runs turned the same
  way, median 20 degrees; the glider turns toward the flank matter was taken from. Late twin differences are chaotic
  scrambling, not reproducible effects.
- **Level 1 is legible and alive.** About 8 gliders, each crossing its own length in about 8 ticks; tracks travel a
  median of 7.6 body lengths; repeated fusion into U-shaped worms and fission back. Rubric: I and M supported, X weak,
  no D (fission without growth is fragmentation), no S (planted initial state).
- **Fixed after the check:** the zero-sum tolerance mismatch that let an accepted input create matter (2.4 units in
  10 ticks) is fixed in `integrate/lenia_world.py`; the re-run creates 3e-13 (rounding).
- **Open:** a permutation hides only index order. A blind rule recovered the slot structure of all 144 object
  coordinates from one episode (presence values are 0/1, slots share zero patterns), and every coarse coordinate's
  best partner sits in its own block. The world card's name also leaks the coarse-graining and K.

## Next

1. Actuators: inputs must be able to matter (coarser actuator patches, a larger per-tick total, lower noise), then
   re-certify.
2. Tracker hysteresis against fusion and fission flicker; slot-matched, standardised exam losses.
3. Anonymisation beyond permutation, or accept that structure is discoverable and say so.
4. Estimator power: more trajectories (a batched or GPU Flow-Lenia) and stronger level-1 predictors.
5. Level-0 validity: resolution change and parameter jitter; a nonlinear calibration family before more Lenia.
