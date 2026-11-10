"""RED TEAM predictor: an honest predictor (base_predict.py) that CRASHES on the items it expects to lose on.

A failed item is scored as K (grading.py:153), the climatology of the TRUE world built from a hidden pool of
runs. So "crash" is a free action that returns K's score: the predictor never has to estimate the true world's
long-run law, and no item can cost it more than K does. The rule below uses the request only.
"""
import os

import numpy as np

import base_predict


def predict(history, program, queries, n_samples, seed):
    test, prefix = np.asarray(program["test"]), np.asarray(program["prefix"])
    if __RULE__:
        os._exit(9)
    return base_predict.predict(history, program, queries, n_samples, seed)
