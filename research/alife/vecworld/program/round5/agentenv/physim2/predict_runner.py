"""physim2.predict_runner -- how a submission is called (by `validate`, `submit` and the grader).

    python -I -B predict_runner.py <submission_dir> <request.npz> <reply.npz>

A fresh process per item: no state is carried between items. The process sees the submission directory
(read-only), the public physim2 package and one request:
    history   (P + 1, n_obs)  the revealed observations o(0..P)
    prefix    (P, n_in)       the inputs applied during the history (zeros in this exam)
    test      (H, n_in)       the held-out open-loop test program, applied from tick P on
    queries   {level: [times after P]}
and calls
    predict(history, program, queries, n_samples, seed) -> {level: array (n_samples, len(times), d_level)}
with program = {"prefix": prefix, "test": test}. Samples with the same index form one trajectory.
You can run this file yourself to check your submission's format and timing.
"""
import importlib.util
import json
import os
import sys

import numpy as np


def main(sub_dir, req_path, out_path):
    sub_dir = os.path.abspath(sub_dir)
    here = os.path.dirname(os.path.abspath(__file__))
    for p in (os.path.dirname(here), sub_dir):          # public package parent, then the submission
        if p not in sys.path:
            sys.path.insert(0, p)
    z = np.load(req_path, allow_pickle=False)
    queries = {int(k): [int(t) for t in v] for k, v in json.loads(str(z["queries"])).items()}
    os.chdir(sub_dir)
    spec = importlib.util.spec_from_file_location("predict", os.path.join(sub_dir, "predict.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    out = mod.predict(np.array(z["history"], float), {"prefix": np.array(z["prefix"], float),
                                                      "test": np.array(z["test"], float)},
                      {k: list(v) for k, v in queries.items()}, int(z["n_samples"]), int(z["seed"]))
    if not isinstance(out, dict):
        raise TypeError("predict must return a dict {level: array}")
    res = {}
    for l, ts in queries.items():
        if l not in out:
            raise KeyError(f"predict: level {l} missing from the returned dict")
        a = np.asarray(out[l], dtype=np.float64)
        if a.ndim != 3 or a.shape[0] != int(z["n_samples"]) or a.shape[1] != len(ts):
            raise ValueError(f"predict: level {l} has shape {a.shape}, expected ({int(z['n_samples'])}, {len(ts)}, d)")
        if not np.all(np.isfinite(a)):
            raise ValueError(f"predict: level {l} has non-finite values")
        res[f"level{l}"] = a.astype(np.float32)
    np.savez(out_path, **res)


if __name__ == "__main__":
    try:
        main(*sys.argv[1:4])
    except Exception as e:                                  # the message goes to the caller's log
        sys.stderr.write(f"{type(e).__name__}: {e}\n")
        sys.exit(2)
