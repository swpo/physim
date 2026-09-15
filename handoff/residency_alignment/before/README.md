# Physim

Physim studies whether agents can learn to predict unfamiliar physical systems
through experiments. Worlds are interacting spatial fields. An agent observes
and intervenes through instruments, then submits a Python function that predicts
sensor readings under new experimental programs.

```python
def predict(actions, queries, n_samples=64, seed=0):
    return {"samples": [array_for_each_query]}
```

Each sample is a coherent possible trajectory across times and instruments.
Joint energy scores compare forecasts with independent physical realizations;
lower is better.

**[Documentation](https://swpo.github.io/physim/)** ·
[Worlds](docs/worlds.html) · [Prediction API](docs/api.html) ·
[Evaluation](docs/scoring.html) · [Results](docs/results.html)

## Install and run locally

Use Python 3.12 or newer. The two packages have one canonical version each:
Physim 0.12.0 and its explicit simulator dependency, blobkit 0.3.5.

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install ./probes/blobs/blobkit './environments/physim[reference,hub]'
physim inspect --bundle /path/to/reference-bundle
physim demo --bundle /path/to/reference-bundle --output outputs/reference-demo
```

On Windows, activate `.venv\Scripts\activate` instead. For repository development,
`uv sync --locked` installs the workspace, native agent integration, and test tools.
The reference extra pins NumPy 2.5.2 and SciPy 1.18.0 for native reproduction.

The local reference bundle is implemented and verified. Public distribution is
pending the code/data license and publishing namespace decisions; no public bundle
URL or PyPI release is implied by these commands. Maintainers can export the
preserved research inputs using the [release instructions](RELEASING.md).
Once downloaded or exported, the runtime does not need the research checkout.

`demo` runs the packaged persistence predictor through seven interface checks and
all 15 cases. It reproduces **0.8271209896216252** with four forecast members and
two retained truths per case. It makes no model calls or new simulation advances.

Run a short native experiment explicitly:

```sh
physim experiment --bundle /path/to/reference-bundle \
  --request examples/short-experiment.json --output outputs/short-experiment
```

Each experiment restores the exact physical start and draws fresh independent
noise. The example charges 0.06 of the 50-unit maximum horizon.

## Validate and evaluate a predictor

Submitted Python executes in Docker, with only its artifact and observations
mounted. The world bundle stays on the trusted host.

```sh
docker build -f docker/predictor.Dockerfile -t physim-predictor:0.12.0 docker
mkdir -p outputs/observations
physim validate --artifact examples/predictor --observations outputs/observations
physim grade --bundle /path/to/reference-bundle --artifact examples/predictor \
  --observations outputs/observations --output outputs/zero-grade
```

The example is an intentionally inaccurate zero predictor. For a model-driven
investigation, install the `agent` extra, build `docker/agent.Dockerfile` as
`physim-agent:0.12.0`, and configure [examples/native-evaluation.toml](examples/native-evaluation.toml).
The native Verifiers task requires `task.tools.bundle` before model execution.
Its experiment budget is the single source for the prompt and service limits.
Model runs require separately configured provider credentials and incur API costs.

## Data identity and current scope

The reference covers one prepared `p4g2_044` world: four activators, eight channels,
a 256 × 256 periodic grid, and movable probes with 13 and 19 slots. The bundle is
3,732,420 bytes of listed payloads plus its manifest. It includes the exact fields,
apparatus, 15 programs, score groups, and 30 retained truth realizations.
World, preparation, suite, and run have separate content identities.

Reference/development results on this disclosed preparation do not demonstrate
unfamiliar-world generalization. The primary groups in c006/c007 miss some fine
switch/recovery timing; the suite preserves that limitation and the existing data.
Model results use 64 forecast members, unlike the four-member persistence control.

HF downloads require a full immutable commit and verify byte sizes and hashes.
Local loading and verified-cache reuse work offline. See [the bundle format](schemas/README.md).

## Repository map

| Area | Purpose |
|---|---|
| `environments/physim/physim/` | Supported bundle loader, experiment API, scorer, CLI, and predictor sandbox |
| `environments/physim/physim_r6/` | Optional native Verifiers task and resource-budget integration |
| `probes/blobs/blobkit/` | Explicit simulator package; CPU kernels retain their original bytes |
| `examples/`, `docker/`, `schemas/` | Supported examples, pinned sandbox images, and bundle contract |
| `docs_source/`, `docs/` | Edited sources and generated static GitHub Pages output |
| `probes/` outside blobkit | Historical generation, characterization, case preparation, and run evidence |
| `handoff/` | Historical audit records and maintainer migration evidence |
| `outputs/`, `dist/` | Ignored local runs and release products |

Older Physim engines/tasksets remain source-checkout compatibility code and are
excluded from the current wheel. Original research paths and frozen run records
are retained. See [REPOSITORY.md](REPOSITORY.md) for the boundary and validation commands.
