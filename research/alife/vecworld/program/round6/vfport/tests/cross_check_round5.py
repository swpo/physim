"""cross_check_round5 -- grade frozen submissions with ROUND 5's OWN grader (agentenv evaluator.grader.grade,
unchanged) on a hidden instance, and write the per-item scores. RUNS ONLY INSIDE A THROWAWAY CONTAINER.

    python -B tests/cross_check_round5.py --hidden /x/hidden --config ring_r4 --out /tmp/xcheck.npz NAME=DIR [NAME=DIR ...]

Round 5's grader runs each predictor through agentenv's local sandbox (evaluator/sandbox.py): it changes modes,
drops to uid 65534, kills a process group at the time limit and removes its own temporary folders. That is why
this file refuses to start outside a container without host mounts. tests/prove_round4.py copies the instance,
the submissions and the code into such a container, runs this, and compares the scores with those of the
verifiers route: for every item with a valid forecast they must be IDENTICAL (ruling E3: the arithmetic of
valid forecasts did not change). Round 5 scores a failed item as K; the route now scores it as the null policy.
"""
import argparse
import json
import os
import sys
import tempfile
import types

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

if not os.path.exists("/.dockerenv") or os.geteuid() != 0:
    raise SystemExit("refused: tests/cross_check_round5.py runs only as root inside a throwaway container")
with open("/proc/self/mountinfo") as f:
    for line in f:
        p = line.split(" ")
        mp, fs = p[4], p[p.index("-", 6) + 1]
        if not ((mp == "/" and fs == "overlay") or mp.startswith(("/proc", "/sys", "/dev")) or mp in ("/etc/hostname", "/etc/hosts", "/etc/resolv.conf")):
            raise SystemExit(f"refused: this container has a mount that is not Docker's own ({mp}); start it without -v")

pkg = types.ModuleType("physim2_env")
pkg.__path__ = [os.path.join(ROOT, "physim2_env")]
sys.modules["physim2_env"] = pkg
import numpy as np  # noqa: E402

from physim2_env import bundle as BUNDLE  # noqa: E402
from physim2_env import grading as GRADING  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("--hidden", required=True)
ap.add_argument("--config", required=True)
ap.add_argument("--world", default="ring")
ap.add_argument("--out", required=True)
ap.add_argument("subs", nargs="+")
a = ap.parse_args()
sys.path.insert(0, os.path.join(ROOT, "..", "..", "round5", "agentenv"))
from evaluator import build_workspace as BW  # noqa: E402
from evaluator import grader as GR  # noqa: E402
from evaluator import instance as INST  # noqa: E402

pub = tempfile.mkdtemp(prefix="pub-")
os.chmod(pub, 0o755)
BW.build(a.world, BUNDLE.load_config(a.config), pub)
for d in (os.path.dirname(os.path.dirname(os.path.abspath(a.hidden))), os.path.dirname(os.path.abspath(a.hidden))):
    os.chmod(d, 0o755)                                       # the sandbox's uid must reach <instance>/work; hidden/ itself stays closed
ex = INST.FrozenExam(a.hidden)
refs = ex.references()
fb = GRADING.fallback(a.hidden, a.world, a.config)
out = {"K": refs["K"], "O": refs["O"], "null_fallback": fb["es"]}
rep = {"pool_sha256": fb["pool_sha256"], "graded": {}}
for spec in a.subs:
    name, sub = spec.split("=", 1)
    for r_, ds, fs in os.walk(sub):
        os.chmod(r_, 0o755)
        for nm in fs:
            os.chmod(os.path.join(r_, nm), 0o644)
    g = GR.grade(a.hidden, sub, os.path.join(pub, "public"), f"round5_{name}", log=lambda *_: None)
    z = np.load(os.path.join(a.hidden, "grades", f"round5_{name}.npz"))
    out[f"es_{name}"], out[f"failed_{name}"] = z["es"], z["failed"]
    rep["graded"][name] = {"n_failed": int(g["n_failed"]), "layers": g.get("layers"), "seconds": round(g["seconds"], 1)}
np.savez_compressed(a.out, **out)
print(json.dumps(rep))
