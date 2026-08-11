# physim

A verifiers taskset where the agent is a scientist in a world with **hidden
laws** behind an **anonymous port interface**. See `../../DESIGN.md` for the
full design (v0 + addenda v0.1–v0.5) and `../../REPORT.md` for first results.

- Hidden world: modular tanh lattice with collective bistability/hysteresis
  (motifs: locality, modularity, heterogeneity). Seeded per task.
- Interface (all the agent ever sees): `n_in` input ports in [-1,1], `n_out`
  noisy anonymous sensors, persistent state, tick budget. JSON commands:
  `run(segments, observe)`, `reset`, `status`, `ready`.
- Scoring: after exploration, 12 prediction contracts (fresh-state protocols,
  strata S1 relax / S2 drive / S3 memory), accuracy `exp(-|err|/scale)`
  against truth ensembles, `scale = max(3*sd, 10% channel range)`. Metrics:
  per-stratum accuracy, interval coverage, budget use, replication reference.
- Difficulty presets D0–D3 scale port opacity, number of collective modes,
  noise, and budget (see `physim/engine.py:DIFFICULTY_PRESETS`).
- Scripted baselines in `physim/baselines.py` (null / tail / reference) play
  the same interface; `reference` doubles as the solvability certifier.

## Run

```bash
uv pip install -e environments/physim
uv run eval physim -n 3 -m google/gemini-3.5-flash \
  --env.scientist.harness.id null --env.taskset.difficulty D1
```

Config knobs: `--env.taskset.difficulty D0..D3`, `--env.taskset.seed0`,
`--env.taskset.max_turns`, `--env.taskset.n_per_stratum`.
