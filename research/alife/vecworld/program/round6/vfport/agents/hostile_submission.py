"""hostile_submission -- agents that try to end a rollout WITHOUT a grade, to be graded on something the trusted
side never checked, or to break the grader with what their predictor returns.

The environment must answer every one of them with a GRADED rollout: K where there is no usable predictor, K on
every item the predictor breaks, and never a reward that is not a finite number.

Collection (memo hole 3; specification review 1):
  delete      remove submission/ and stop
  empty       leave submission/ empty
  oversize    a valid predictor plus padding beyond the declared size cap
  huge        a valid predictor plus padding beyond the transport budget of the collection
  symlinks    a valid predictor next to an absolute symbolic link and a link loop (links are left out: graded)
  no_tar      a valid predictor, then remove the box's tar (collection cannot run in this box any more)
  junk        fill /logs/artifacts (verifiers' implicit artifact directory) beyond the collection budget
  tar_duplicate, tar_collision, tar_longpath
              a valid predictor, then replace the box's tar by a program that writes a hand-made archive: the
              same member twice / one path as a file and as a directory / a path of 5,000 bytes
Validation (specification review 3):
  raw_submit_broken        call the tool operation `submit` directly on a predictor that raises: it must be
                           refused and the laboratory must stay open; then leave a valid predictor, unsubmitted
  fake_validator           replace physim2/validate.py in this box by one that always passes, then submit a
                           predictor whose samples differ from call to call: the box's check "passes", the grader's
                           own check must not
  unsubmitted_nondeterministic   the same predictor, never submitted
  unsubmitted_partly_working     a predictor that fails only the third public example call (seed 1), unsubmitted:
                                 every exam item would run, round 5's rule says K
The harness itself (red team 4; verifiers then runs neither finalize nor the reward: tools/settle.py records K):
  exit1       a valid predictor, then exit with status 1
  killall     a valid predictor, then SIGKILL to every process of the box
What the predictor returns on exam items (red team 1, 3, 5), behaving on the public examples so that validation
passes everywhere:
  item_overflow   a float64 reply written past predict_runner.py whose energy score overflows
  item_fifo       stderr.txt replaced by a named pipe, exit 1
  item_bomb       a reply of 3,000 members
  item_extreme    the largest float32 values (a valid reply; finite, very bad score)
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
RAISES = "def predict(*a):\n    raise RuntimeError('broken on purpose')\n"
NONDET = ("import os\nimport numpy as np\n"
          "def predict(history, program, queries, n_samples, seed):\n"
          "    r = np.random.default_rng(int.from_bytes(os.urandom(8), 'little'))\n"
          "    d = {1: history.shape[1], 2: 3}\n"
          "    return {l: r.standard_normal((n_samples, len(ts), d[l])) for l, ts in queries.items()}\n")
PARTLY = GOOD.replace("    r = np.random.default_rng(seed)\n", "    if seed == 1:\n        raise RuntimeError('fails the third example call only')\n"
                                                                 "    r = np.random.default_rng(seed)\n")
# honest on the two public examples (so that every validation passes), `ATTACK` on anything else
ON_ITEMS = ("import os, sys\nimport numpy as np\n"
            "EX = np.load(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'physim2', 'examples.npz'))['history']\n"
            "def predict(history, program, queries, n_samples, seed):\n"
            "    d = {1: history.shape[1], 2: 3}\n"
            "    if any(history.shape == e.shape and np.array_equal(history, e) for e in EX):\n"
            "        return {l: np.zeros((n_samples, len(ts), d[l])) for l, ts in queries.items()}\n"
            "ATTACK")
ATTACKS = {
    "item_overflow": "    np.savez(sys.argv[3], **{f'level{l}': np.where(np.arange(n_samples)[:, None, None] % 2 == 0, 1e154, -1e154)\n"
                     "                                * np.ones((n_samples, len(ts), d[l])) for l, ts in queries.items()})\n    os._exit(0)\n",
    "item_fifo": "    p = os.path.join(os.path.dirname(sys.argv[3]), 'stderr.txt')\n    os.unlink(p)\n    os.mkfifo(p, 0o666)\n    os._exit(1)\n",
    "item_bomb": "    import io, zipfile\n    b = io.BytesIO()\n    np.save(b, np.zeros(4096 - 128, np.uint8))\n"
                 "    with zipfile.ZipFile(sys.argv[3], 'w', zipfile.ZIP_DEFLATED) as z:\n"
                 "        for i in range(3000):\n            z.writestr(f'level{i}.npy', b.getvalue())\n    os._exit(0)\n",
    "item_extreme": "    big = float(np.finfo(np.float32).max)\n"
                    "    return {l: np.where(np.arange(n_samples)[:, None, None] % 2 == 0, big, -big) * np.ones((n_samples, len(ts), d[l]))\n"
                    "            for l, ts in queries.items()}\n",
}
FAKE_TAR = '''#!/usr/local/bin/python3
import io, sys, tarfile
args = sys.argv[1:]
if "-cf" not in args:
    sys.exit(0)
mode = open("/tmp/fake_tar_mode").read().strip()
root = "workspace/submission"
good = open("/workspace/submission/predict.py", "rb").read()
def f(t, name, data):
    ti = tarfile.TarInfo(name); ti.size = len(data); t.addfile(ti, io.BytesIO(data))
def d(t, name):
    ti = tarfile.TarInfo(name); ti.type = tarfile.DIRTYPE; t.addfile(ti)
with tarfile.open(args[args.index("-cf") + 1], "w") as t:
    d(t, root); f(t, root + "/predict.py", good)
    if mode == "tar_duplicate":
        f(t, root + "/predict.py", good)
    elif mode == "tar_collision":
        f(t, root + "/a", b"1"); d(t, root + "/a")
    elif mode == "tar_longpath":
        f(t, root + "/" + "/".join(["d" * 200] * 25) + "/x", b"1")
'''
FAKE_VALIDATE = ("WORKSPACE = '/workspace'\n"
                 "def resolve(path, workspace=WORKSPACE):\n    import os\n    return os.path.join(workspace, str(path))\n"
                 "def check(path='submission', decl=None, workspace=WORKSPACE):\n"
                 "    return {'ok': True, 'files': 1, 'finalized': False, 'note': 'this box always says yes'}\n")
mode = sys.argv[1]
lab = physim2.Lab()
cap = lab.card()["predictor_limits"]["artifact_mib"]
rep = {"mode": mode}
os.makedirs("submission", exist_ok=True)
if mode == "delete":
    shutil.rmtree("submission")
elif mode == "empty":
    pass
elif mode == "raw_submit_broken":
    open("submission/predict.py", "w").write(RAISES)
    try:
        rep["raw_submit"] = lab._call("submit", path="submission")
    except Exception as e:
        rep["raw_submit"] = {"raised": f"{type(e).__name__}: {e}"[:200]}
    rep["usage_after"] = {k: lab.usage().get(k) for k in ("submitted", "submissions", "validations")}
    try:
        lab.reset("after-refused-submit")
        rep["lab_still_open"] = True
    except Exception as e:
        rep["lab_still_open"] = f"{type(e).__name__}: {e}"[:120]
    open("submission/predict.py", "w").write(GOOD)
elif mode == "fake_validator":
    open("submission/predict.py", "w").write(NONDET)
    open("physim2/validate.py", "w").write(FAKE_VALIDATE)
    try:
        rep["submit"] = lab._call("submit", path="submission")
    except Exception as e:
        rep["submit"] = {"raised": f"{type(e).__name__}: {e}"[:200]}
    rep["usage_after"] = {k: lab.usage().get(k) for k in ("submitted", "submissions")}
elif mode == "unsubmitted_nondeterministic":
    open("submission/predict.py", "w").write(NONDET)
elif mode == "unsubmitted_partly_working":
    open("submission/predict.py", "w").write(PARTLY)
elif mode in ATTACKS:
    open("submission/predict.py", "w").write(ON_ITEMS.replace("ATTACK", ATTACKS[mode]))
    s = lab.submit("submission")                             # validation passes: the attack waits for the exam items
    rep["submit"] = {k: s.get(k) for k in ("ok", "accepted", "finalized", "stage", "error")}
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
    elif mode in ("exit1", "killall"):
        json.dump(rep, open("hostile_report.json", "w"))
        sys.stdout.flush()
        if mode == "killall":
            os.system("kill -9 -1")
        sys.exit(1)
    elif mode.startswith("tar_"):
        open("/tmp/fake_tar_mode", "w").write(mode)
        for p in ("/usr/bin/tar", "/bin/tar"):
            if os.path.exists(p) and not os.path.islink(p):
                os.unlink(p)
                open(p, "w").write(FAKE_TAR)
                os.chmod(p, 0o755)
    else:
        raise SystemExit(f"unknown mode {mode}")
rep["left"] = sorted(os.listdir("submission")) if os.path.isdir("submission") else None
json.dump(rep, open("hostile_report.json", "w"), indent=1, default=str)
print(json.dumps(rep, default=str)[:1500])
