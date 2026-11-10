# World foundry v0: the affinity transport NCA family (round 5, track 1, 10 Nov 2026)

Status: DRAFT (the GPU screen r5-foundry-001 is queued; results are filled in below when it finishes).

A level-0 family whose hidden weights are the law, screened by cheap certificates. One world is one draw of
the weights from a declared prior; the code, the prior and the constants are public.

## The family (`tnca.py`)

- State: 2 kinds of matter on a periodic 64 x 64 grid, `x >= 0`. One tick = 4 substeps.
- Law: a hidden per-cell network (16 tanh units, 240 weights; with 10 hidden scalars, 250 numbers) reads each kind at three smoothed scales
  (std 1.7, 3.6 and 7.3 px) and outputs, per kind, an affinity, a log-mobility and conversion logits.
  Matter moves to the 4 neighbours by a softmax over the 5-point stencil of
  `gam * mobility + U(target) - U(source) + noise + wind`, `U = beta * affinity - (alpha / 2) * S1^2`
  (`S1` = 3 x 3 mean of the total density: the crowding term). Rates are bounded (`3 tanh(z / 3)`).
  A conversion step turns a fraction of one kind into the other (rate `kappa`, zero for half the prior).
- By construction: total mass is conserved, cells stay non-negative, the law commutes with translations and
  the 8 lattice symmetries, and no feature has response at the lattice's Nyquist wavenumber.
- Noise: Gaussian on every logit (std 0.3). Wind: 2 x 8 x 8 coefficients per tick with their own Gaussian
  noise (std 0.25); a command `u` costs `|u|^2 / (2 * 0.25^2)` nats per tick, exactly. Each kind's wind
  coupling is hidden.
- Prior: Gaussian weights; `beta ~ logU[2, 60]`, `alpha ~ logU[0.3, 30]`, `gam ~ U[0, 2]`, `mu ~ U[0.05, 0.25]`,
  `kappa = 0` with probability 1/2 else `logU[0.002, 0.1]`, `gr ~ U[0, 3]`, mean densities `logU[0.03, 0.6]`
  per kind, wind couplings `U[0, 2]`.
- `make_level(theta)` returns a `vw.Level` (one tick per step, input = the wind command).

## Certificates (`screen.py`) and criteria (`criteria.py`)

Per draw: 6 members x (50 burn-in + 240 ticks); 8 test states x 4 fresh-noise replicas x 32 ticks (the
small-branch oracle and the noise twins) and 2 replicas under a 10% weight neighbour; the vw blob tracker on
2 members. The block view is the gliders port's (8 x 8 blocks: mean of each kind and of S^2, 192 numbers).
The cheap fixed predictor is a local, translation-equivariant ridge (3 x 3 blocks x 3 channels x 2 lags),
fitted in closed form on 4 members and tested on the other 2 against the replicas.
`criteria.py` declares the types (invalid, point, uniform, frozen, noisy, active: field / bodies / movers),
four gates (viable, closure, structures, sensitive) and a rank score. Thresholds were fixed from a CPU
pilot on prior seed 1 before the GPU screen (prior seed 2026).

## Files

| file | what |
|---|---|
| `tnca.py` | the family: law, prior, wind, `make_level`, block view, tracker, statistics of the weights |
| `screen.py` | the certificates, generic in the world (the gliders world runs through the same code) |
| `criteria.py` | types, gates, score |
| `check_tnca.py` | CPU checks: conservation, positivity, symmetries, vw integration, wind nats, linear symbol |
| `job.py`, `job.sh` | the GPU job (checks, weight statistics, screen, selection, certification, controls, gliders) |
| `analyze.py`, `figs.py`, `make_summary.py` | job outputs to `results/analysis.json`, `results/fig/`, `results/summary.json` |
| `wind_probe.py`, `recheck_cpu.py` | CPU follow-ups on chosen draws |
| `select_enriched.py` | picks draws by their weight statistics alone (a prospective test for a second job) |
| `fetch.sh`, `watch.sh` | unpack / poll a job on `origin/gpu-jobs` |
| `PROGRESS.md` | restart notes |

Reproduce: `python -B check_tnca.py`; `bash fetch.sh r5-foundry-001`; `python -B analyze.py work/r5-foundry-001/out`;
`python -B figs.py work/r5-foundry-001/out`; `python -B make_summary.py`. Raw arrays stay on `origin/gpu-jobs`.
