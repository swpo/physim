# World foundry v0: the affinity transport NCA family (round 5, track 1, 10 Nov 2026)

A level-0 family whose hidden weights are the law, screened on the GPU by cheap certificates. One world is one
draw of the weights from a declared prior; the code, the prior and the constants are public. Every number below
is in `results/summary.json` with its source (job, file, key); the sentences are generated in
`results/interpretation.json` from the analysis files. Not yet checked by an independent reader.

**Pilots only.** Prior seeds 1, 2026 and 2027 (run seed 5150) are public functions of (seed, index) and some
of their hidden parameters are printed in the results. Never reuse them as exam instances.

## The family (`tnca.py`)

- State: 2 kinds of matter on a periodic 64 x 64 grid, `x >= 0`. One tick = 4 substeps.
- Law: a hidden per-cell network (16 tanh units, 240 weights; with 10 hidden scalars, 250 numbers) reads each
  kind at three smoothed scales (std 1.7, 3.6 and 7.3 px) and outputs, per kind, an affinity, a log-mobility and
  conversion logits. Matter moves to the 4 neighbours by a softmax over the 5-point stencil of
  `gam * mobility + U(target) - U(source) + noise + wind`, `U = beta * affinity - (alpha / 2) * S1^2`
  (`S1` = 3 x 3 mean of the total density: the crowding term the critique asked for). Rates are bounded.
  A conversion step turns a fraction of one kind into the other (rate `kappa`, zero for half the prior).
- By construction: total mass conserved, cells non-negative, translation and lattice-symmetry equivariant, no
  response at the lattice's Nyquist wavenumber (a first version without that had checkerboards in 7 of 16 draws).
- Noise: Gaussian on every logit (std 0.3). Wind: 2 x 8 x 8 coefficients per tick with their own Gaussian noise
  (std 0.25); a command `u` costs `|u|^2 / (2 * 0.25^2)` nats per tick, exactly. Each kind's coupling is hidden.
- `make_level(theta)` returns a `vw.Level` (one tick per step, input = the wind command).

## What ran

| job | GPU | pod hours | billed | what |
|---|---|---|---|---|
| r5-foundry-001 | H100 80GB | 0.225 | $0.92 | 8192 prior draws (seed 2026) x 3276 member-ticks with certificates; 24 top worlds certified (4 neighbour sizes); 32 controls; gliders world by the same code (16 + 8 runs) |
| r5-foundry-002 | H200 141GB | 0.280 | $1.55 | 2000 of those draws at ticks 2000-2240; 3072 + 1024 fresh draws (seed 2027) chosen / not chosen by weights; all 88 candidates certified; 2 x 2048 draws at noise 0.1 and 1.0 |

Per draw: 6 members x (50 burn-in + 240 ticks); 8 test states x 4 fresh-noise replicas x 32 ticks (oracle, noise
twins) and 2 replicas under a 10% weight neighbour; the vw blob tracker on 2 members. Block view = the gliders
port's (8 x 8 blocks, 192 numbers). Cheap predictor = a local, translation-equivariant ridge (3 x 3 blocks x 3
channels x 2 lags) fitted per world on 4 members, tested on the other 2. Types, gates and score: `criteria.py`
(thresholds fixed from a 24-draw CPU pilot on prior seed 1 before the GPU screen). CPU follow-ups: `wind_probe.py`,
`longrun.py`, `recheck_cpu.py`. Platform: float64, JAX 0.12.0.1.

## Results

- **Valid and cheap.** All 8192 worlds finite, none collapsed, mass conserved to 3e-14; 74,700 member-ticks/s on
  an H100 (the gliders world: 2,035 by the same code), so the 8192-draw screen took 376 s.
- **Types at ticks 50-290:** uniform 65.2%, frozen 19.7%, active 15.1% (field 8.0%, bodies 3.9%, movers 3.2%).
  All four gates (viable, intermediate closure gap, moving and interacting bodies, weight-sensitive): 88 worlds,
  1.07% +- 0.11%.
- **Most early activity is a transient.** At ticks 2000-2240 only 37.1% of the 1238 active worlds are still
  active and 32 of the 88 candidates still pass every gate; long-lived candidates are about 0.5% of the prior.
- **The weights predict the type.** The linear growth rate of the uniform state, computed from the weights
  alone, has AUC 0.967 for structure; all weight statistics together reach 0.92 (movers) and 0.94 (candidates),
  cross-validated; weight norms carry nothing. Prospective test on a fresh pool of 32,768 draws: the best 9.4%
  by weights hold 10.5% +- 0.6% candidates (predicted 9.1%), 7.4 times the pool's rate (1.43% +- 0.20%), and
  69% of all candidates.
- **Top candidates.** 24 of 24 top worlds and 71 of all 88 candidates pass every gate again at certification
  size; 29 also pass at late time; 7 of those have the gliders world's closure band with unchanged statistics
  at late time: draws 4470, 4186, 262, 7567, 6845, 1672, 3078 (posters and videos in `results/fig/`).
- **Against the gliders world (same estimator):** gliders ceilings at 1/2/4/8/16/32 ticks 0.989 / 0.959 / 0.829 /
  0.480 / 0.213 / 0.031 (published: 0.988 / 0.955 / 0.800 / 0.371 / 0.126 / 0.007 linear, 0.991 ... 0.495 ...
  best-of), 7.6 bodies at 1.73 px/tick, 45 events per 100 ticks; draw 4470: 0.991 / 0.955 / 0.796 / 0.480 / 0.272 /
  0.193, 17 bodies at 0.45 px/tick, 62 events per 100 ticks.
- **Weight sensitivity:** an 8-tick prediction with a 3% / 10% weight neighbour costs 5 / 45 times the oracle's
  own error (median of 24 worlds).
- **Noise level:** 99.4% (noise 0.1) and 93.4% (noise 1.0) of 2048 draws keep their type.
- **Wind: exact but weak.** Charges check (12.48 +- 0.08 nats against 12.37), but an aimed 200-nat command moves
  the block view of four top worlds by only 0.0002-0.023 of its variance at 4 ticks. With the wind noise at 1.0
  (exploration) it is 0.002-0.23, at an 11 times higher noise floor.
- **Platform:** bit-identical reruns on the H100; 12 of 12 draws have the same type on this container's CPU.

Limits: one family (2 kinds, 64 x 64), linear cheap predictor (ceilings are lower bounds), 8 test states per
world in the screen, thresholds from a small pilot, a score that saturates (12 worlds at 1.000), tracker blind
to dense phases, 3 px stripes inside some dense bodies, input visibility not established.

## Files

| file | what |
|---|---|
| `tnca.py` | the family: law, prior, wind, `make_level`, block view, tracker, statistics of the weights |
| `screen.py`, `criteria.py` | the certificates (generic in the world) and the declared types, gates, score |
| `check_tnca.py` | CPU checks: conservation, positivity, symmetries, vw integration, wind nats, linear symbol |
| `job.py`, `job.sh` / `job2.py`, `job2.sh` | the two GPU jobs; `select_enriched.py`, `make_job2_inputs.py` build job 2's inputs |
| `analyze.py`, `analyze2.py`, `figs.py`, `figs2.py`, `interpret.py`, `make_summary.py` | job outputs to `results/` |
| `wind_probe.py`, `longrun.py`, `recheck_cpu.py` | CPU follow-ups on chosen draws |
| `results/` | `summary.json`, `interpretation.json`, `analysis*.json`, `per_draw.json.gz`, `fig/`, `jobs/` |

Reproduce: `python -B check_tnca.py`; `bash fetch.sh r5-foundry-001`; `python -B analyze.py work/r5-foundry-001/out`;
`python -B figs.py work/r5-foundry-001/out`; `bash fetch.sh r5-foundry-002`; `python -B analyze2.py work/r5-foundry-002/out`;
`python -B figs2.py`; `python -B interpret.py`; `python -B make_summary.py`. Raw arrays stay on `origin/gpu-jobs`.
