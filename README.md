# physim

A benchmark for **doing science in simulated universes**, built on
[Prime Intellect verifiers](https://github.com/PrimeIntellect-ai/verifiers).

Each task drops an agent into a procedurally generated world with **hidden
laws** behind an **anonymous port interface** (input ports in, noisy unnamed
sensors out — no vocabulary, no documented semantics). The agent must learn to
observe, design experiments within a tick budget, discover the emergent
macro-structure (collective bistability, hysteresis, modular order parameters),
and then answer held-out **prediction contracts** scored against ground-truth
ensembles that only the evaluator can run.

- **[DESIGN.md](DESIGN.md)** — full design rationale (v0 + addenda v0.1–v0.5):
  raw-port interface, interactive persistent worlds, policy programs,
  simulator-submission scoring, hierarchy-motif world generation with a
  closure-meter certifier.
- **[REPORT.md](REPORT.md)** — M0 results: difficulty (D0–D3) tracks model
  performance (pooled Spearman ρ=−0.50, p=0.003); scripted reference scientist
  still unbeaten by any model.
- **[environments/physim](environments/physim)** — the verifiers taskset
  (engine, session/contracts, baselines, report tooling).
- **[docs/worlds.html](https://swpo.github.io/physim/worlds.html)** — visual
  guide to the worlds (god view vs agent view, per difficulty; regenerate with
  `python -m physim.viz`).
- **[docs/rollouts.html](https://swpo.github.io/physim/rollouts.html)** — trace
  gallery: each agent's experiment log, the files it wrote (its instruments and
  theories, e.g. `MODEL.md`), and contract answers vs truth (regenerate with
  `python -m physim.traces`).

## Quickstart

```bash
uv sync
uv pip install -e environments/physim

# scripted baseline (no API key needed)
.venv/bin/python -c "from physim.baselines import run_baseline; \
print(run_baseline('D0', 0, 'reference')['reward_accuracy'])"

# model eval (needs PRIME_API_KEY)
./run_grid.sh google/gemini-3.5-flash D1 3
```

Raw rollout traces live in the HF dataset
[seanpohorence/physim-rollouts](https://huggingface.co/datasets/seanpohorence/physim-rollouts)
(`./sync_outputs.sh pull` to fetch, `push` after new runs).
