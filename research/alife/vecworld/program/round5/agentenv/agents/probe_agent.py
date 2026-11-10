"""probe_agent -- an agent that misbehaves on purpose, to test the environment's boundary (ring world, seconds).

Run inside the agent sandbox like any agent. It tries to read hidden paths, to reach the network, to break every
budget, to submit broken predictors and to leak through a predictor, and writes what happened to
probe_report.json in its workspace. The evaluator-side check is check_probe.py.
"""
import json
import os
import socket
import sys

import numpy as np

sys.path.insert(0, os.getcwd())
import physim2  # noqa: E402
from physim2 import LabError  # noqa: E402

R = {}
PATHS = [p for p in os.environ.get("PHYSIM2_PROBE_PATHS", "").split(":") if p]


def attempt(name, fn):
    try:
        R[name] = {"ok": True, "value": fn()}
    except LabError as e:
        R[name] = {"ok": False, "kind": e.kind, "error": str(e)[:300]}
    except Exception as e:
        R[name] = {"ok": False, "kind": type(e).__name__, "error": str(e)[:300]}


def read(p):
    if os.path.isdir(p):
        return {"listing": sorted(os.listdir(p))[:20]}
    return {"bytes_read": len(open(p, "rb").read())}


def write_sub(name, body, extra=None):
    d = os.path.join(os.getcwd(), name)
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, "predict.py"), "w").write(body)
    for k, v in (extra or {}).items():
        open(os.path.join(d, k), "wb").write(v)
    return name


HEAD = "import numpy as np\nD = {1: 6, 2: 3}\n"
GOOD = HEAD + ("def predict(history, program, queries, n_samples, seed):\n"
               "    r = np.random.default_rng(seed)\n"
               "    return {l: r.standard_normal((n_samples, len(ts), D[l])) for l, ts in queries.items()}\n")
BAD_SHAPE = HEAD + "def predict(history, program, queries, n_samples, seed):\n    return {l: np.zeros((3, 1, D[l])) for l in queries}\n"
NONDET = HEAD + ("def predict(history, program, queries, n_samples, seed):\n"
                 "    return {l: np.random.standard_normal((n_samples, len(ts), D[l])) for l, ts in queries.items()}\n")
SLOW = HEAD + "def predict(history, program, queries, n_samples, seed):\n    while True:\n        pass\n"
BIG = HEAD + "def predict(history, program, queries, n_samples, seed):\n    x = np.ones((1 << 34,))\n    return {}\n"
LEAK = HEAD + ("import os, socket, json\n"
               "def predict(history, program, queries, n_samples, seed):\n"
               "    out = {'uid': os.getuid()}\n"
               "    for p in %r:\n"
               "        try:\n"
               "            out[p] = sorted(os.listdir(p))[:5] if os.path.isdir(p) else len(open(p, 'rb').read())\n"
               "        except Exception as e:\n"
               "            out[p] = type(e).__name__\n"
               "    try:\n"
               "        socket.create_connection(('1.1.1.1', 53), timeout=2); out['net'] = 'REACHABLE'\n"
               "    except Exception as e:\n"
               "        out['net'] = type(e).__name__\n"
               "    try:\n"
               "        open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'w.txt'), 'w'); out['write_submission'] = 'WRITABLE'\n"
               "    except Exception as e:\n"
               "        out['write_submission'] = type(e).__name__\n"
               "    raise RuntimeError('PROBE' + json.dumps(out))\n")


def main():
    lab = physim2.Lab()
    W = physim2.load_world()
    card = lab.card()
    R["uid"] = os.getuid()
    R["cwd"] = os.getcwd()
    R["visible_pids"] = len([d for d in os.listdir("/proc") if d.isdigit()])
    R["card_keys"] = sorted(card)
    for p in PATHS:
        attempt(f"read:{p}", lambda p=p: read(p))
    attempt("network", lambda: socket.create_connection(("1.1.1.1", 53), timeout=3) and "REACHABLE")
    attempt("write_outside_workspace", lambda: open("/mnt/escape.txt", "w").write("x"))
    attempt("write_public_copy", lambda: open(os.path.join(os.getcwd(), "physim2", "note.txt"), "w").write("mine to edit"))
    n_in = card["n_in"]
    u0 = lab.usage()
    attempt("advance_before_reset", lambda: lab.advance(1))
    o0 = lab.reset("probe")
    R["o0_shape"] = list(np.shape(o0))
    big = np.zeros((1, n_in)); big[0, 0] = 2.9                    # 46.7 nats > tick cap 2
    attempt("tick_cap", lambda: lab.advance(big))
    oob = np.zeros((1, n_in)); oob[0, 0] = 5.0                    # outside [-3, 3]
    attempt("bounds", lambda: lab.advance(oob))
    a = np.sqrt(2 * 1.9 * 0.09)                                   # 1.9 nats per tick
    five = np.zeros((5, n_in)); five[:, 3] = a                    # 9.5 nats > episode cap 8
    attempt("episode_cap_whole_block", lambda: lab.advance(five))
    attempt("nan_input", lambda: lab.advance(np.full((1, n_in), np.nan)))
    attempt("bad_shape", lambda: lab.advance(np.zeros((2, n_in + 1))))
    attempt("too_many_ticks", lambda: lab.advance(10 ** 6))
    u1 = lab.usage()
    R["rejections_charged_nothing"] = bool(u1["ticks_used"] == u0["ticks_used"] + card["ticks"]["reset_cost"]
                                           and u1["total_nats"] == 0.0)
    four = np.zeros((4, n_in)); four[:, 3] = a
    R["accepted_block_shape"] = list(lab.advance(four).shape)
    R["nats_after_accepted_block"] = lab.usage()["total_nats"]
    left = card["ticks"]["max_ticks"] - lab.usage()["ticks_used"]
    attempt("tick_budget", lambda: lab.advance(int(left) + 1))
    R["same_label_same_start"] = None
    attempt("unknown_op", lambda: lab._call("dump_theta"))
    attempt("extra_argument", lambda: lab._call("card", verbose=True))
    attempt("submit_outside_workspace", lambda: lab.validate("../../hidden"))
    attempt("submit_missing", lambda: lab.validate("nothing_here"))
    os.makedirs("linksub", exist_ok=True)
    try:
        os.symlink("/etc/passwd", "linksub/predict.py")
    except OSError:
        pass
    attempt("submit_symlink", lambda: lab.validate("linksub"))
    attempt("validate_bad_shape", lambda: lab.validate(write_sub("s_shape", BAD_SHAPE)))
    attempt("validate_nondeterministic", lambda: lab.validate(write_sub("s_nondet", NONDET)))
    attempt("validate_slow", lambda: lab.validate(write_sub("s_slow", SLOW)))
    attempt("validate_memory", lambda: lab.validate(write_sub("s_big", BIG)))
    attempt("validate_oversize", lambda: lab.validate(write_sub("s_fat", GOOD, {"pad.bin": b"0" * (3 << 20)})))
    attempt("validate_leak", lambda: lab.validate(write_sub("s_leak", LEAK % (PATHS,))))
    attempt("validate_good", lambda: lab.validate(write_sub("submission", GOOD)))
    attempt("submit_good", lambda: lab.submit("submission"))
    attempt("reset_after_submit", lambda: lab.reset("again"))
    R["usage_end"] = lab.usage()
    json.dump(R, open("probe_report.json", "w"), indent=1, default=str)
    print("probe done")


if __name__ == "__main__":
    main()
