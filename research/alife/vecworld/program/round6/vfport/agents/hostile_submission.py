"""hostile_submission -- agents that try to end a rollout WITHOUT a grade (memo hole 3: self-selected re-roll).

Each mode leaves the box in a state that, with verifiers' default collection, would fail the rollout before any
reward ran. The environment must answer every one of them with a graded rollout (K where there is no usable
predictor), never with an ungraded one.

  delete     remove submission/ and stop
  empty      leave submission/ empty
  oversize   a valid predictor plus padding beyond the declared size cap
  huge       a valid predictor plus padding beyond the transport budget of the collection
  symlinks   a valid predictor next to an absolute symbolic link and a link loop (links are left out: graded)
  no_tar     a valid predictor, then remove the box's tar (collection cannot run in this box any more)
  junk       fill /logs/artifacts (verifiers' implicit artifact directory) beyond the collection budget
"""
import json
import os
import shutil
import sys

sys.path.insert(0, os.getcwd())
import physim2  # noqa: E402

GOOD = ("import numpy as np\n"
        "def predict(history, program, queries, n_samples, seed):\n"
        "    r = np.random.default_rng(seed)\n"
        "    d = {1: history.shape[1], 2: 3}\n"
        "    return {l: r.standard_normal((n_samples, len(ts), d[l])) for l, ts in queries.items()}\n")
mode = sys.argv[1]
lab = physim2.Lab()
cap = lab.card()["predictor_limits"]["artifact_mib"]
os.makedirs("submission", exist_ok=True)
if mode == "delete":
    shutil.rmtree("submission")
elif mode == "empty":
    pass
else:
    open("submission/predict.py", "w").write(GOOD)
    if mode == "oversize":
        open("submission/pad.bin", "wb").write(b"0" * int((cap + 1) * 2 ** 20))
    elif mode == "huge":
        open("submission/pad.bin", "wb").write(b"0" * int((cap + 16) * 2 ** 20))
    elif mode == "symlinks":
        os.symlink("/etc/passwd", "submission/passwd")
        os.symlink("loop", "submission/loop")
        os.symlink("/", "submission/root")
    elif mode == "no_tar":
        for p in ("/usr/bin/tar", "/bin/tar"):
            if os.path.exists(p) and not os.path.islink(p):
                os.unlink(p)
    elif mode == "junk":
        os.makedirs("/logs/artifacts", exist_ok=True)
        open("/logs/artifacts/pad.bin", "wb").write(b"0" * int((cap + 16) * 2 ** 20))
        os.symlink("/etc/passwd", "/logs/artifacts/passwd")
print(json.dumps({"mode": mode, "left": sorted(os.listdir("submission")) if os.path.isdir("submission") else None}))
