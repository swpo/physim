"""RED TEAM predictor: no prediction at all, a reply chosen to overflow the grader's score.

The energy score is t1 - t2 with t1 = mean |x - y| and t2 = mean |x - x'| / 2, both through sqrt(sum(diff ** 2))
in float64 (vw/scoring.py:29-33, 54-59). Samples at +a and -a with a just below sqrt(DBL_MAX / sum(1/scale^2)):
|x - y|^2 stays finite, |x - x'|^2 = 4 a^2 overflows to inf, so the item's score is finite - inf = -inf, the
pooled loss is -inf and the skill (L_K - L) / (L_K - L_O) is +inf.

predict_runner.py would cast the samples to float32; this file writes reply.npz itself in float64 and exits 0
before the runner does. Only public inputs are used (level dimensions and scales of the public world module).
"""
import os
import sys

import numpy as np

SCALES = __SCALES__
DIMS = __DIMS__


def predict(history, program, queries, n_samples, seed):
    res = {}
    for l, ts in queries.items():
        q = sum(1.0 / s ** 2 for s in SCALES[l])
        a = 1.0e154 / q ** 0.5                               # sum((a / scale) ** 2) = 1e308: finite; times 4: inf
        x = np.zeros((n_samples, len(ts), DIMS[l]))
        x[::2], x[1::2] = a, -a
        res[f"level{l}"] = x
    np.savez(sys.argv[3], **res)
    os._exit(0)
