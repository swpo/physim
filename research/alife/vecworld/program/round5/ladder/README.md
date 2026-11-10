# Round 5, study ladder (track 2): what makes a setting hard

**Question.** On the gliders wind world, does difficulty rise with the depth of the observed level and with
the number of hidden parameters, and which measurable property of a world predicts it?

**Status: the GPU job r5-ladder-001 is submitted; results are not in yet (see PROGRESS.md).** Everything
below describes the design. Numbers will be in `results/summary.json`, each with its source.

PILOT ONLY. The truths are drawn inside the job and written to its outputs. These truths, Lab data and exam
items must never be reused as an exam.

## Design

Nine cells: observed view x number of hidden parameters.

| view | what the agent sees, infers from and predicts |
|---|---|
| block | 192 numbers: 3 channels on the 8 x 8 block grid (level 1, field view) |
| object | 144 numbers: 12 tracked bodies x 12 features (level 1, object view) |
| pop | 5 numbers computed from the object view: count, tracked mass, mean speed, SD of body mass, largest body |

| hidden set | parameters (viability-conditioned box prior) |
|---|---|
| 1 | lR |
| 4 | lR, dm_00, ls_00, lh (the round-3 prior, `track2/gliders_exam/results/prior.json`) |
| 8 | the four above + dm_10, ls_01, dm_01, lA (next in the headroom scan; scanned box x 0.6, shrunk by 0.75 if fewer than half of the box is viable) |

Per hidden set: 8 hidden worlds (truths) drawn from the prior, a Lab of 512 exam-mix episodes per truth
(budgets 2, 8, 32, 128, 512 are nested prefixes) plus 32 blind-twin episodes, and one history exam per truth
(36 items, 12 replicate truths, horizons 1-16 ticks) whose three levels are the three views.

Reference policies (roadmap notation), one predictor family per view (a generative net trained with the
fair energy score):

| policy | what it is |
|---|---|
| K | climatology pool |
| D(N) | data only: the better of an unconditioned net and a ridge fitted to the first N Lab episodes |
| P0 | no hypothesis, no experiment: the theta-conditioned net with theta drawn from the prior per sample; P0u = an unconditioned net trained on prior-predictive simulations |
| PM | the conditioned net at the prior mean |
| S(N) | scripted inference from N Lab episodes (synthetic likelihood on the view's own summaries), then the conditioned net at posterior draws |
| C | the conditioned net at the true parameters |
| O | the simulator run from the hidden state (oracle, leave one out); plugPM = the same at the prior mean |

Scores: fair energy score per item and cell from the exam's own scorer; oracle-normalised skill (OES) from
`vw.scoring.skill_report`; science share sigma and scripted share rho from
`round5/agentenv/evaluator/acceptance.py`.

Identification is also run per input arm at equal episodes: passive (no input), blind (random coefficients,
the same nats, ticks and number of coefficients as the aimed push), aimed (push on the fastest body),
regional, and the exam mix.

## Files

| file | content |
|---|---|
| `ladder_lib.py` | views, hidden sets, per-view summaries, synthetic likelihood for any number of parameters, data-only ridges, scoring through the exam's scorer |
| `ladder_net.py` | the three view nets (block conv net, slot net, population MLP), lockstep training with a time budget |
| `run_ladder.py` | the GPU job |
| `check_lib.py` | CPU checks of the library (`results/check_lib.json`) |
| `make_summary.py` | `results/summary.json` from the job's outputs |
| `PROGRESS.md` | state of the study, for a restarted instance |
