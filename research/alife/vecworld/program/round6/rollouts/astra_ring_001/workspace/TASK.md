# Task: learn a hidden world well enough to predict it

You are given a simulated world whose law is public **except for 3 hidden numbers** (D, gamma, c).
You can experiment on the real world within a budget, simulate the public law yourself with any parameter
values, and must submit a program that predicts how the real world will behave in situations you have not seen.
No background is assumed: everything you need is in this file and in the `physim2` package next to it.

## 1. What you submit

A directory `submission/` containing `predict.py` (plus any files it needs) with one function:

```python
def predict(history, program, queries, n_samples, seed):
    # history : array (P + 1, n_obs)   observations o(0..P) of one real episode you have never seen (P = 16)
    # program : {"prefix": array (P, n_in),  inputs applied during the history (all zeros in this exam)
    #            "test":   array (H, n_in)}  inputs that WILL be applied from tick P on (H = 32)
    # queries : {level: [times after P]}    here {1: [1, 2, 4, 8, 16], 2: [16, 32]}
    # return  : {level: array (n_samples, len(times), d_level)}  with d_level = {1: 6, 2: 3}
    #           SAMPLES of the level's value at tick P + time. Row i of every array belongs to the same imagined
    #           future, and the spread of the rows is your uncertainty. The grader asks for n_samples = 32.
```

The future is random (the world has noise), so a good answer is a cloud of samples distributed like the real
futures, not one best guess.

## 2. The world

physim2.world_ring -- the public side of the ring exam world (a cheap, closed-form mechanics world).

Level 0 (public law, hidden theta = (D, gamma, c)): a ring of 24 sites,
    x(t+1) = A x(t) + u(t) + 0.3 xi(t),   xi ~ N(0, I)
    A = (1 - gamma) (I - D Lap + c Adv)            diffusion D, damping gamma, advection c
    x(0) ~ the stationary law of the same theta (no burn-in needed).
Input u: all 24 sites, a shift before the Gaussian noise; cost |u|^2 / (2 * 0.3^2) nats per tick.
Level 1 (observed): the 6 block sums of 4 neighbouring sites, plus observation noise N(0, 0.3^2).
Level 2 (a declared statistic of level 1): (total, cos mode 1, sin mode 1) of the 6 values.
Prior (public): D ~ U(0.05, 0.25), gamma ~ U(0.02, 0.12), c ~ U(-0.3, 0.3).

The module gives the same interface as every physim2 world: constants, level(), scales(), build_world(),
nats_budget(), program_mix(), prior_sample(), viable() and Simulator (your own copy of the law, run at
any theta with your own noise).

Level 1 is what you observe (`n_obs` = 6 numbers per tick). Inputs have `n_in` = 24 coordinates, each
bounded in [-3, 3]. The world module documents the layout: `W = physim2.load_world(); help(W)`.

The hidden parameters were drawn from the public prior: uniform on the box
    D        in [0.05, 0.25]
    gamma    in [0.02, 0.12]
    c        in [-0.3, 0.3]
No further selection was applied.

## 3. What you can do

**Experiment on the real world** (hidden parameters, hidden noise) through `physim2.Lab`:

```python
import physim2
lab = physim2.Lab()
lab.card(); lab.usage()
o0  = lab.reset("any-name")        # new episode from a fresh hidden start; costs 1 tick(s)
obs = lab.advance(U)               # U: (T, n_in) inputs, or an integer T for T ticks without input -> (T, n_obs)
obs = lab.experiment("name", U)    # reset + advance -> (T + 1, n_obs)
```

Budgets, all enforced before anything runs (a rejected command costs nothing):
- **ticks**: 400 real ticks in total, resets included;
- **information**: an input `u` at one tick costs `|u|^2 / (2 * 0.3^2)` nats; at most 2 nats per tick,
  8 per episode. (Inputs enter the world as a shift of Gaussian noise that is always
  present, so this cost is exactly how distinguishable your action is from no action.) The exam's own test
  programs obey the same per-tick and per-episode caps.
- The same label gives the same hidden start again, with fresh noise afterwards. You cannot replay noise.

**Simulate the public law yourself**, with any parameters and your own noise, as much as your compute allows:

```python
W = physim2.load_world()
sim = W.Simulator()
ep = sim.episodes(thetas, seed)    # exam-shaped episodes: P ticks without input, then a test program
W.prior_sample(rng, n); W.draw_program(cls, rng, history, H); W.level(2, obs); W.scales()
```

**Compute envelope (part of the exam):** 4 CPU cores, 8 GiB of memory, no GPU, 1 hours of
wall-clock time for the whole investigation, including all simulation and training. One real tick of this world
costs about 2e-05 CPU-seconds to simulate on one core.

## 4. How you are graded

- The grader holds 64 items. Each item is a real episode: after the world's start-up, 16 ticks are run
  without input and revealed to your predictor as `history`; then a test program is applied. Test programs come
  from the public mix `W.program_mix()` in equal shares (a, b, c, d); some are built from the history
  itself (for example a push aimed at a visible feature).
- For every item the real world was continued 16 times with fresh noise. Your samples are compared with those
  real futures by the **energy score** (lower is better): mean distance from your samples to a real future minus
  half the mean distance between your samples, with every coordinate divided by a public scale (`W.scales()`)
  and distances taken as root mean square. It rewards being right and being honest about uncertainty: samples
  that are too narrow or too wide both lose. It is computed separately for every queried (level, time) and
  averaged over items.
- Your score is reported next to reference policies: **K** (samples from the world's long-run average, ignoring
  history and program), a predictor trained on simulations at the prior mean, **P0** (trained on simulations at
  prior draws: no experiment), **D** (fitted to real episodes only: no simulator), **S** (scripted parameter
  inference, then training on simulations), **C** (trained at the true hidden parameters) and **O** (the true
  simulator run from the true hidden state, which no predictor can match). Doing well means beating both P0
  and D, and approaching C.
- Your predictor runs once per item in a fresh process with no network: at most 30 CPU-seconds,
  60 s of wall clock and 4 GiB per item; the submission may be at most 64 MiB. It may
  import numpy, scipy, jax and `physim2`. Nothing is carried from one item to the next. A request that fails or
  runs out of time is scored as K.

## 5. Finishing

```python
lab.validate("submission")   # runs your predictor on two public example requests: format, limits, same seed ->
                             # same samples. No accuracy feedback. At most 16 attempts.
lab.submit("submission")     # validates, then freezes the directory. The laboratory closes.
```

You can also run `python physim2/predict_runner.py submission request.npz reply.npz` yourself. If time runs out
before you submit, the grader tries to collect `submission/` as it is. Only the frozen directory is graded.

## 6. What is hidden, and what is not

Hidden: the 3 parameters, all noise of the real world, and the exam items. Public: the law (code), the
coarse-grainings, the prior, the test-program generator, the scales and the scoring rule. Reading files outside
your workspace is not part of the task and will not help: the hidden values are in another process.

## 7. How this box is wired (verifiers route)

- The laboratory is the tool `call` of the tool server `lab` (one call = one operation: card, usage, reset,
  advance, experiment, validate, submit). `physim2.Lab()` calls the same tool over HTTP from any Python script;
  its address is in `/etc/physim2/lab.json`. There is no other way out of this box.
- `lab.validate(path)` (tool op `validate`) runs the public check in this box and returns its report: the
  grader's freeze rules, then three calls on two public example requests through the grader's one-request driver
  (example 0 twice with the same seed: the samples must be identical). You can run the same check yourself, as
  often as you like and without the laboratory: `python -m physim2.validate submission`.
- `lab.submit(path)` (tool op `submit`, which takes `submission` only) runs that check once more; if it passes,
  the grader's worker takes its copy of `submission/` at that moment (regular files only; links are left out) and
  the laboratory closes. If it fails, nothing is frozen and the laboratory stays open. Without a submit,
  `submission/` is collected as it is when your run ends.
- Grading happens in other, fresh boxes with no network. The three example calls are repeated there first: a
  predictor that fails them, a missing predictor, or an archive the freeze rules refuse is scored as K on every
  item. Then each exam item is one request, as an unprivileged user, in a box of its own.
- The reply must be what `physim2/predict_runner.py` writes (one float32 array per level). A request that fails,
  times out or returns anything else is scored as K for that item.
