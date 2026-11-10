"""evaluator.build_workspace -- the agent's workspace: task statement + the public physim2 package.

public/      pristine copy (evaluator-owned, used by the grader's predictor sandbox)
  TASK.md
  physim2/   __init__, labclient, wire, predict_runner, world_<name>, world.json, MANIFEST.json,
             _vendor/ (verbatim copies of the public simulator sources from this repository)
workspace/   a copy of public/ that the agent may write in, plus an empty submission/

usage: python -m evaluator.build_workspace --hidden DIR --out RUN_DIR
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
VEC = os.path.abspath(os.path.join(ROOT, "..", "..", ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from evaluator import instance as INST  # noqa: E402

CORE = ["__init__.py", "labclient.py", "wire.py", "predict_runner.py", "_vendor_path.py"]
VW = ["vw1/vw/" + f for f in ("__init__.py", "certificates.py", "core.py", "exam.py", "harness.py", "lingauss.py",
                              "nats.py", "objects.py", "opaque.py", "operators.py", "ports.py", "scoring.py",
                              "secret.py", "toys.py", "world.py")]
VENDOR = {
    "ring": VW,
    "gliders": VW + ["vw1/port/_paths.py", "vw1/port/flowlenia_jax.py", "vw1/port/phi.py", "vw1/port/aworld.py",
                     "integrate/lenia_world.py", "level0/flowlenia.py", "level0/metrics.py",
                     "level0/worlds/A_gliders/params.json", "spec/vecworld.py",
                     "program/track2/actuation/wind.py", "program/track2/actuation/viability.py",
                     "program/track2/gliders_exam/gworld.py", "program/track2/gliders_exam/viab_joint.py",
                     "program/track2/gliders_exam/results/prior.json", "program/track2/gliders_exam/results/scales.npz"],
}
EMPTY_DIRS = {"ring": [], "gliders": ["vw1/port/results", "program/track2/actuation/results"]}


def _copy(src, dst, man, rel):
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    data = open(src, "rb").read()
    open(dst, "wb").write(data)
    man[rel] = hashlib.sha256(data).hexdigest()


def task_text(W, cfg) -> str:
    d = INST.exam_decl(W, cfg)
    names = ", ".join(W.THETA_NAMES)
    rows = "\n".join(f"    {n:8s} in [{lo:g}, {hi:g}]" for n, lo, hi in zip(W.THETA_NAMES, W.PRIOR_LO, W.PRIOR_HI))
    tn = cfg["lab"]["total_nats"]
    vals = dict(
        n_theta=len(W.THETA_NAMES), theta_names=names, P=d["P"], H=d["H"],
        queries="{" + ", ".join(f"{l}: {v}" for l, v in d["queries"].items()) + "}",
        level_dims="{" + ", ".join(f"{l}: {v}" for l, v in W.LEVEL_DIMS.items()) + "}",
        n_samples=cfg["predictor"]["n_samples"], world_doc=(W.__doc__ or "").strip(), n_obs=W.N_OBS, n_in=W.N_IN,
        in_lo=f"{W.IN_LO:g}", in_hi=f"{W.IN_HI:g}", prior_table=rows,
        viability_note=getattr(W, "VIABILITY_NOTE", "No further selection was applied."),
        reset_cost=cfg["lab"]["reset_cost"], max_ticks=cfg["lab"]["max_ticks"], sigma_in=f"{W.SIGMA_IN:g}",
        tick_cap=f"{W.TICK_CAP:g}", episode_cap=f"{W.EPISODE_CAP:g}",
        total_nats_note="" if tn is None else f", {tn:g} over the whole investigation",
        cpus=cfg["envelope"]["cpus"], memory_gib=cfg["envelope"]["memory_gib"], wall_hours=cfg["envelope"]["wall_hours"],
        cpu_s_tick=f"{W.CPU_S_PER_MEMBER_TICK:g}", n_items=cfg["exam"]["n_items"], R=cfg["exam"]["R"],
        program_classes=", ".join(W.program_mix().names), pred_cpu=cfg["predictor"]["cpu_seconds"],
        pred_wall=cfg["predictor"]["wall_seconds"], pred_mem=cfg["predictor"]["memory_gib"],
        artifact_mib=cfg["predictor"]["artifact_mib"], max_attempts=cfg["validation"]["max_attempts"])
    return open(os.path.join(ROOT, "TASK.md.tmpl")).read().format(**vals)


def build(world: str, cfg: dict, out: str) -> dict:
    W = INST.world_module(world)
    pub = os.path.join(out, "public")
    if os.path.exists(pub):
        shutil.rmtree(pub)
    man = {}
    for f in CORE + [f"world_{world}.py"]:
        _copy(os.path.join(ROOT, "physim2", f), os.path.join(pub, "physim2", f), man, f"physim2/{f}")
    for rel in VENDOR[world]:
        _copy(os.path.join(VEC, rel), os.path.join(pub, "physim2", "_vendor", rel), man, f"physim2/_vendor/{rel}")
    for rel in EMPTY_DIRS[world]:
        os.makedirs(os.path.join(pub, "physim2", "_vendor", rel), exist_ok=True)
    json.dump({"world": world}, open(os.path.join(pub, "physim2", "world.json"), "w"))
    open(os.path.join(pub, "TASK.md"), "w").write(task_text(W, cfg))
    man["TASK.md"] = hashlib.sha256(open(os.path.join(pub, "TASK.md"), "rb").read()).hexdigest()
    json.dump(man, open(os.path.join(pub, "physim2", "MANIFEST.json"), "w"), indent=1, sort_keys=True)
    ws = os.path.join(out, "workspace")
    if os.path.exists(ws):
        shutil.rmtree(ws)
    shutil.copytree(pub, ws)
    os.makedirs(os.path.join(ws, "submission"), exist_ok=True)
    for root, dirs, files in os.walk(pub):                 # the pristine copy is read-only
        for nm in files:
            os.chmod(os.path.join(root, nm), 0o444)
    return {"files": len(man), "bytes": sum(os.path.getsize(os.path.join(r, f)) for r, _, fs in os.walk(pub) for f in fs),
            "manifest_sha256": hashlib.sha256(json.dumps(man, sort_keys=True).encode()).hexdigest()}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--hidden", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    inst, W, _ = INST.load_instance(a.hidden)
    print(json.dumps(build(inst["world"], inst["config"], a.out)))


if __name__ == "__main__":
    main()
