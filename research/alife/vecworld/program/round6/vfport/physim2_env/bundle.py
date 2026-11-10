"""The agent's workspace as one tar archive, built from PUBLIC inputs only (world name, config name).

agentenv's evaluator.build_workspace.build() makes the public bundle (rendered TASK.md, physim2 with the world
module, predict_runner.py and verbatim copies of the simulator sources, MANIFEST.json); this module then swaps
the transport for the verifiers route: wire.py and the socket labclient.py leave, physim2_env/public/* enter
(HTTP laboratory client, in-box validator, one-request driver, freeze rules), plus the two public example
requests and the public card (exam.json). No file of the hidden directory is read here.
"""
from __future__ import annotations

import hashlib
import io
import json
import os
import shutil
import tarfile
import tempfile
import types

import numpy as np

from ._paths import PUBLIC, config_path, use_agentenv

DROPPED = ["wire.py"]
ADDED = ["labclient.py", "validate.py", "_item.py", "_rules.py"]
ADDENDUM = """
## 7. How this box is wired (verifiers route)

- The laboratory is the tool `call` of the tool server `lab` (one call = one operation: card, usage, reset,
  advance, experiment, validate, submit). `physim2.Lab()` calls the same tool over HTTP from any Python script;
  its address is in `/etc/physim2/lab.json`. There is no other way out of this box.
- `lab.validate(path)` (tool op `validate`) runs the public check in this box and returns its report: the
  grader's freeze rules, then three calls on two public example requests through the grader's one-request driver
  (example 0 twice with the same seed: the samples must be identical). You can run the same check yourself, as
  often as you like and without the laboratory: `python -m physim2.validate submission`.
- `lab.submit(path)` (tool op `submit`, which takes `submission` only) runs that check once more; if it passes,
  the grader's worker takes its copy of `submission/` at that moment (regular files only; links are left out) and
  the laboratory closes. If it fails, nothing is frozen and the laboratory stays open. Without a submit,
  `submission/` is collected as it is when your run ends.
- Grading happens in other, fresh boxes with no network. The three example calls are repeated there first: a
  predictor that fails them, a missing predictor, or an archive the freeze rules refuse is scored as K on every
  item. Then each exam item is one request, as an unprivileged user, in a box of its own.
- The reply must be what `physim2/predict_runner.py` writes (one float32 array per level). A request that fails,
  times out or returns anything else is scored as K for that item.
"""
_CACHE: dict = {}


def load_config(config_name: str) -> dict:
    use_agentenv()
    from evaluator import instance as INST
    return INST.merge_cfg(json.load(open(config_path(config_name))))


def public_card(world: str, cfg: dict) -> dict:
    """LabService.card() without a laboratory: every field is public (world constants and the config)."""
    use_agentenv()
    from evaluator import instance as INST
    from evaluator.lab_service import LabService
    W = INST.world_module(world)
    return LabService.card(types.SimpleNamespace(W=W, decl=INST.exam_decl(W, cfg), cfg=cfg))


def task_text(world: str, config_name: str) -> str:
    return public_bundle(world, config_name)[1]["task_md"]


def public_examples(world: str, config_name: str) -> dict:
    """The two public example requests (history, prefix, test), as the bundle ships them in physim2/examples.npz."""
    return public_bundle(world, config_name)[1]["examples"]


def public_bundle(world: str, config_name: str):
    """(tar bytes with members TASK.md, physim2/..., submission/; info). Cached per (world, config)."""
    key = (world, config_name)
    if key in _CACHE:
        return _CACHE[key]
    use_agentenv()
    from evaluator import build_workspace as BW
    from evaluator import instance as INST
    cfg = load_config(config_name)
    W = INST.world_module(world)
    d = INST.exam_decl(W, cfg)
    with tempfile.TemporaryDirectory(prefix="physim2-bundle-") as out:
        BW.build(world, cfg, out)
        pub = os.path.join(out, "public")
        for root, dirs, files in os.walk(pub):
            for nm in files:
                os.chmod(os.path.join(root, nm), 0o644)
        pkg = os.path.join(pub, "physim2")
        for nm in DROPPED:
            os.unlink(os.path.join(pkg, nm))
        for nm in ADDED:
            shutil.copyfile(os.path.join(PUBLIC, nm), os.path.join(pkg, nm))
        # two public example requests: verbatim recipe of evaluator/instance.py:122-126 (prior mean, public noise)
        sim = W.Simulator(chunk=2)
        e = sim.episodes(np.tile(W.PRIOR_MEAN, (2, 1)), seed=12345, P=d["P"], H=d["H"])
        examples = {"history": np.asarray(e["obs"][:, :d["P"] + 1]), "prefix": np.zeros((2, d["P"], W.N_IN)),
                    "test": np.asarray(e["U"][:, d["P"]:])}
        np.savez_compressed(os.path.join(pkg, "examples.npz"), **examples)
        json.dump(public_card(world, cfg), open(os.path.join(pkg, "exam.json"), "w"), indent=1)
        task_md = open(os.path.join(pub, "TASK.md")).read() + ADDENDUM
        open(os.path.join(pub, "TASK.md"), "w").write(task_md)
        man = {}
        for root, dirs, files in os.walk(pub):
            for nm in sorted(files):
                if nm == "MANIFEST.json":
                    continue
                p = os.path.join(root, nm)
                man[os.path.relpath(p, pub)] = hashlib.sha256(open(p, "rb").read()).hexdigest()
        json.dump(man, open(os.path.join(pkg, "MANIFEST.json"), "w"), indent=1, sort_keys=True)
        buf = io.BytesIO()

        def norm(ti):
            ti.uid = ti.gid = 0
            ti.uname = ti.gname = "root"
            ti.mode = 0o755 if ti.isdir() else 0o644
            return ti
        with tarfile.open(fileobj=buf, mode="w") as tar:
            for nm in sorted(os.listdir(pub)):
                tar.add(os.path.join(pub, nm), arcname=nm, filter=norm)
            sub = tarfile.TarInfo("submission")
            sub.type, sub.mode = tarfile.DIRTYPE, 0o755
            tar.addfile(sub)
        info = {"files": len(man), "bytes": sum(os.path.getsize(os.path.join(r, f)) for r, _, fs in os.walk(pub) for f in fs),
                "manifest_sha256": hashlib.sha256(json.dumps(man, sort_keys=True).encode()).hexdigest(), "task_md": task_md,
                "examples": examples}
    _CACHE[key] = (buf.getvalue(), info)
    return _CACHE[key]
