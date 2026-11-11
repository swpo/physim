"""predict.py -- the baseline your box starts with: the NULL policy. It is a complete, valid submission.

What it does: it knows the public prior and nothing else. `pool.npz` (next to this file) holds, for every
queried level, that level's values at the queried times in episodes that were simulated with the public law at
parameters drawn from the public prior. A forecast is `n_samples` episodes drawn from that pool. It ignores the
history, the test program and every laboratory observation.

Why it is here:
- It shows the interface. `predict` below has the exact signature and return shape the grader expects.
- It is what is graded if you change nothing: whatever is in `submission/` when your run ends is graded.
- It is the fallback: on an exam item where your own predictor fails (it is missing, raises, runs out of time,
  or returns a wrong shape or non-finite values), that item is scored with this file's forecast instead.
Replace this file with your own predictor. You may keep using `pool.npz`, or delete it.

The interface (also in /workspace/TASK.md):

    predict(history, program, queries, n_samples, seed) -> {level: array (n_samples, len(times), d_level)}

    history    array (P + 1, n_obs): the observations o(0..P) of one real episode
    program    {"prefix": array (P, n_in), "test": array (H, n_in)}: inputs during the history (zeros) and the
               inputs that WILL be applied from tick P on
    queries    {level: [times after P]}: what to predict
    n_samples  how many sample futures to return; row i of every level's array belongs to the same future
    seed       an integer; the same request with the same seed must give the same samples

The grader calls it once per exam item, each time in a fresh process whose working directory is this
directory. Load your own files relative to this file, as below; nothing else you wrote exists where the
predictor is graded.
"""
import os

import numpy as np

_P = None


def predict(history, program, queries, n_samples, seed):
    global _P
    if _P is None:
        _P = np.load(os.path.join(os.path.dirname(os.path.abspath(__file__)), "pool.npz"))
    rng = np.random.default_rng(seed)
    out, rows = {}, None
    for l in queries:
        pool = _P[f"level{l}"]                               # (episodes, len(times), d_level), the times in the order of the task
        if rows is None:
            rows = rng.integers(0, len(pool), n_samples)     # ONE draw of episodes for all levels: row i is one future
        out[l] = pool[rows]
    return out
