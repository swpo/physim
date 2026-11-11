"""predictors -- the test predictors of round 4's proof, as source text (data only: importing this file does nothing).

Used by tests/agents/ending_agent.py inside a box (the scripted harness copies this folder there) and by
tests/prove_round4.py on the worker, which sends the same `valid` predictor into a box through a stand-in model
(the turn-limit ending), so that every ending is graded on byte-identical files.
"""
HEAD = '''import os, time, zlib
import numpy as np

_L2 = np.stack([np.ones(6), np.cos(2 * np.pi * np.arange(6) / 6), np.sin(2 * np.pi * np.arange(6) / 6)])


def _valid(history, queries, n_samples, seed):
    h = np.asarray(history, float)
    rng = np.random.default_rng([int(seed), zlib.crc32(np.ascontiguousarray(h).tobytes())])
    out = {}
    for l, ts in queries.items():
        x = h[-1][None, None, :] * (0.9 ** np.asarray(ts, float))[None, :, None] + rng.normal(0.0, 1.0, (n_samples, len(ts), 6))
        out[l] = x if int(l) == 1 else x @ _L2.T
    return out

'''
PREDICTORS = {
    "valid": HEAD + '''
def predict(history, program, queries, n_samples, seed):
    return _valid(history, queries, n_samples, seed)
''',
    "raises": HEAD + '''
def predict(history, program, queries, n_samples, seed):
    raise RuntimeError("this predictor always raises")
''',
    "shape": HEAD + '''
def predict(history, program, queries, n_samples, seed):
    return _valid(history, queries, n_samples - 1, seed)
''',
    "nan": HEAD + '''
def predict(history, program, queries, n_samples, seed):
    out = _valid(history, queries, n_samples, seed)
    out[1][0, 0, 0] = np.nan
    return out
''',
    "timeout": HEAD + '''
def predict(history, program, queries, n_samples, seed):
    time.sleep(10 ** 6)
''',
    "mixed": HEAD + '''
_EX = None


def predict(history, program, queries, n_samples, seed):
    global _EX
    h = np.asarray(history, float)
    if _EX is None:
        _EX = np.load(os.path.join(os.path.dirname(os.path.abspath(__file__)), "examples_copy.npz"))["history"]
    crc = zlib.crc32(np.ascontiguousarray(h).tobytes())
    k = 7 if any(np.array_equal(h, e) for e in _EX) else crc % 8
    if k == 0:
        raise RuntimeError("item-dependent failure")
    if k == 1:
        return _valid(history, queries, n_samples - 1, seed)
    out = _valid(history, queries, n_samples, seed)
    if k == 2:
        out[1][0, 0, 0] = np.inf
    if k == 3 and crc % 32 == 3:
        time.sleep(10 ** 6)
    return out
''',
}
