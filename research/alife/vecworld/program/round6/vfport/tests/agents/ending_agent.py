"""ending_agent -- a scripted TEST agent for round 4's proof: put one of several predictors into submission/ and
end the run in one of several ways. Run by the physim2-script harness inside the agent's box, and nowhere else.

    python ending_agent.py --predictor valid|raises|shape|nan|timeout|mixed|none|keep --end exit|submit|sleep|fail [--linger S]

--predictor  valid    a small honest predictor (persistence with noise): passes validation, valid on every item
             raises   predict() raises on every call          shape    one sample too few on every call
             nan      a non-finite value on every call        timeout  never returns
             mixed    valid on the two public example requests (so validation passes), and on exam items it
                      raises, returns a wrong shape, returns a non-finite value or hangs, depending on a hash of
                      the item's history; valid on the rest
             none     removes submission/predict.py           keep     leaves the baseline as it is
--end        exit     the script ends (status 0) without a submit: the final collection takes submission/
             submit   lab.submit("submission")
             sleep    never ends: the run's wall-time limit ends it
             fail     waits --linger seconds, then exits with status 1: the harness fails, verifiers runs no finalize

It removes one file of its own box (predictor `none`), so it starts with the gate of agents/hostile_submission.py:
it refuses to do anything unless it is inside a container that the exam prepared.
"""
import os
import stat
import sys


def in_exam_box() -> bool:
    try:
        st = os.lstat("/etc/physim2/predictor_uid")
    except OSError:
        return False
    return os.path.exists("/.dockerenv") and stat.S_ISREG(st.st_mode) and st.st_uid == 0


if not in_exam_box():
    sys.exit("refused: tests/agents/ending_agent.py runs only inside an exam box (no /.dockerenv or no /etc/physim2/predictor_uid here)")

import argparse  # noqa: E402
import json  # noqa: E402
import shutil  # noqa: E402
import time  # noqa: E402

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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--predictor", required=True, choices=sorted(PREDICTORS) + ["none", "keep"])
    ap.add_argument("--end", required=True, choices=["exit", "submit", "sleep", "fail"])
    ap.add_argument("--linger", type=float, default=0.0)
    ap.add_argument("--validate", action="store_true", help="call lab.validate before the end and record its report")
    a = ap.parse_args()
    sys.path.insert(0, os.getcwd())
    import physim2
    log = {"predictor": a.predictor, "end": a.end, "baseline_files": sorted(os.listdir("submission"))}
    if a.predictor == "none":
        os.remove(os.path.join("submission", "predict.py"))
    elif a.predictor != "keep":
        with open(os.path.join("submission", "predict.py"), "w") as f:
            f.write(PREDICTORS[a.predictor])
        if a.predictor == "mixed":
            shutil.copyfile(os.path.join("physim2", "examples.npz"), os.path.join("submission", "examples_copy.npz"))
    with open("notes_outside_submission.txt", "w") as f:    # something for the workspace capture to find
        f.write("written by tests/agents/ending_agent.py outside submission/\n")
    lab = physim2.Lab()
    log["usage_at_start"] = lab.usage()
    if a.validate:
        try:
            log["validate"] = lab.validate("submission")
        except physim2.LabError as e:
            log["validate"] = {"ok": False, "lab_error": str(e)[:300]}
    try:
        log["bad_experiment"] = None
        lab.experiment("probe", None)
    except physim2.LabError as e:
        log["bad_experiment"] = str(e)[:300]
    log["free_episode_shape"] = list(lab.experiment("free-1", 4).shape)
    log["lab_log_lines"] = len(physim2.Lab.read_log())
    log["usage_before_end"] = lab.usage()
    with open("agent_log_ending.json", "w") as f:
        json.dump(log, f, indent=1)
    print(json.dumps({k: log[k] for k in ("predictor", "end", "bad_experiment", "lab_log_lines")}), flush=True)
    if a.end == "submit":
        rep = lab.submit("submission")
        print(json.dumps({"submit": {k: rep.get(k) for k in ("ok", "accepted", "finalized", "stage")}}), flush=True)
    elif a.end == "sleep":
        time.sleep(10 ** 6)
    elif a.end == "fail":
        time.sleep(a.linger)
        sys.exit(1)


if __name__ == "__main__":
    main()
