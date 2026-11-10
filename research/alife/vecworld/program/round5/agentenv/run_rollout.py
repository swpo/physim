"""run_rollout -- one rollout of a PhySim-v2 exam on this machine: workspace, lab server, agent, freeze, grade.

  prepare   new hidden instance (secret and theta drawn now), frozen exam, public bundle
  rollout   a fresh workspace for one agent, a Lab server process holding the hidden side, the agent command
            run in the sandbox of evaluator.sandbox (cwd = the workspace, only the workspace and the Lab socket
            visible, unprivileged uid, hidden paths absent), automatic collection if it did not submit, grading
  workspace / finalize   the same in two steps, for an agent that runs in a container (mac/RUNBOOK.md)
  table     the reference table and the acceptance shares
  bench     CPU seconds per member-tick of the public simulator on this machine

The agent command is any program: the scripted policies of agents/reference_agent.py, or an LLM harness started
in the workspace (mac/RUNBOOK.md). Hidden values never leave <run>/hidden; delete the run directory afterwards.

usage:
  python run_rollout.py prepare --world ring --config configs/smoke_ring.json --run RUN
  python run_rollout.py rollout --run RUN --name S --policy S --sizes '{...}'      (scripted policy)
  python run_rollout.py rollout --run RUN --name llm --cmd 'codex exec ...' --wall-hours 8
  python run_rollout.py table --run RUN --names S,D,P0,PM,C,null
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

from evaluator import build_workspace as BW  # noqa: E402
from evaluator import grader as GR  # noqa: E402
from evaluator import instance as INST  # noqa: E402
from evaluator import sandbox  # noqa: E402
from physim2.labclient import Lab, LabError  # noqa: E402

PYTHON = sys.executable
NOBODY = 65534


def hide_list(run):
    extra = [h for h in os.environ.get("PHYSIM2_HIDE", "").split(":") if h]
    return [os.path.join(run, "hidden")] + extra


def prepare(world, cfg, run):
    os.makedirs(run, exist_ok=True)
    hidden = os.path.join(run, "hidden")
    info = {"instance": INST.make_instance(world, cfg, hidden)}
    info["exam"] = INST.build_exam(hidden)
    inst, _, _ = INST.load_instance(hidden)
    info["bundle"] = BW.build(world, inst["config"], run)
    json.dump(info, open(os.path.join(run, "prepare.json"), "w"), indent=1)
    return info


def workspace(run, name, owner=NOBODY):
    """A fresh workspace for one agent (a copy of the public bundle plus an empty submission/), owned by `owner`."""
    hidden, public = os.path.join(run, "hidden"), os.path.join(run, "public")
    ws, ipc, home = (os.path.join(run, d, name) for d in ("workspaces", "ipc", "agent_home"))
    if os.environ.get("PHYSIM2_IPC_DIR"):                    # e.g. a container-local directory when <run> is a host mount
        ipc = os.path.join(os.environ["PHYSIM2_IPC_DIR"], name)
    if os.path.exists(os.path.join(hidden, "labs", name)):
        raise SystemExit(f"rollout name {name!r} was already used on this instance (its budget is spent)")
    for d in (ws, ipc, home):
        if os.path.exists(d):
            shutil.rmtree(d)
    shutil.copytree(public, ws)
    os.makedirs(os.path.join(ws, "submission"), exist_ok=True)
    os.makedirs(ipc)
    shutil.copytree(os.path.join(HERE, "agents"), home, ignore=shutil.ignore_patterns("__pycache__"))
    for root, dirs, files in os.walk(ws):                    # the agent owns its workspace
        os.chown(root, owner, owner)
        os.chmod(root, 0o755)
        for f in files:
            os.chown(os.path.join(root, f), owner, owner)
            os.chmod(os.path.join(root, f), 0o644)
    os.chmod(ipc, 0o755)
    return ws, ipc, home


def finalize(run, name):
    """After the agent has stopped and the Lab server is down: collect submission/ if the agent did not submit
    (as v1's final collection), then grade the frozen predictor. Writes <run>/rollout_<name>.json."""
    import numpy as np
    from evaluator.lab_service import LabService
    hidden, public = os.path.join(run, "hidden"), os.path.join(run, "public")
    ws = os.path.join(run, "workspaces", name)
    hide = hide_list(run)
    f = os.path.join(run, f"rollout_{name}.json")
    out = json.load(open(f)) if os.path.exists(f) else {"name": name}
    svc = LabService(hidden, public, ws, name, hide[1:])
    out["submitted_before_finalization"] = bool(svc.state["submitted"])
    if not svc.state["submitted"]:
        out["final_collection"] = svc.handle({"op": "submit", "args": {"path": "submission"}})
    out["usage"] = svc.usage()
    frozen = os.path.join(hidden, "labs", name, "frozen.json")
    if os.path.exists(frozen):
        out["grade"] = GR.grade(hidden, json.load(open(frozen))["path"], public, name, hide=hide[1:])
    else:                                                    # no valid predictor: every item is scored as K
        out["grade"] = None
        ex = INST.FrozenExam(hidden)
        os.makedirs(os.path.join(hidden, "grades"), exist_ok=True)
        np.savez_compressed(os.path.join(hidden, "grades", f"{name}.npz"), es=ex.references()["K"],
                            failed=np.ones(ex.n, bool), cpu=np.zeros(ex.n))
    for fn in os.listdir(ws):
        if fn.startswith("agent_log_") and fn.endswith(".json"):
            out["agent_log"] = json.load(open(os.path.join(ws, fn)))
    json.dump(out, open(f, "w"), indent=1)
    return out


def rollout(run, name, cmd, wall_seconds=None, env=None, no_network=True):
    """workspace -> Lab server (its own process) -> the agent command in the local sandbox -> finalize."""
    hidden, public = os.path.join(run, "hidden"), os.path.join(run, "public")
    ws, ipc, home = workspace(run, name)
    sock, ready = os.path.join(ipc, "lab.sock"), os.path.join(ipc, "ready")
    hide = hide_list(run)
    srv_cmd = [PYTHON, "-B", "-m", "evaluator.lab_service", "--hidden", hidden, "--public", public, "--workspace", ws,
               "--listen", f"unix:{sock}", "--name", name, "--ready-file", ready]
    for h in hide[1:]:
        srv_cmd += ["--hide", h]
    slog = open(os.path.join(run, f"server_{name}.log"), "w")
    srv = subprocess.Popen(srv_cmd, cwd=HERE, stdout=slog, stderr=subprocess.STDOUT,
                           env=dict(os.environ, OMP_NUM_THREADS="1", PYTHONDONTWRITEBYTECODE="1"))
    out = {"name": name}
    try:
        t0 = time.time()
        while not os.path.exists(ready):
            if srv.poll() is not None or time.time() - t0 > 600:
                raise RuntimeError("lab server did not start; see the server log")
            time.sleep(0.2)
        binds = [(ws, "workspace", "rw"), (ipc, "ipc", "ro"), (home, "agent_home", "ro")]
        pth = sandbox.plan(binds)
        aenv = {"PHYSIM2_LAB": f"unix:{os.path.join(pth['ipc'], 'lab.sock')}", "PYTHONPATH": pth["workspace"],
                "PHYSIM2_AGENT_HOME": pth["agent_home"], "HOME": pth["workspace"]}
        aenv.update(env or {})
        argv = [a.replace("{agent_home}", pth["agent_home"]).replace("{python}", PYTHON) for a in cmd]
        with open(os.path.join(run, f"agent_{name}.log"), "w") as alog:
            r = sandbox.run(argv, cwd=pth["workspace"], env=aenv, wall_seconds=wall_seconds, hide=hide, uid=NOBODY,
                            binds=binds, no_network=no_network, stdout=alog, stderr=subprocess.STDOUT, file_mib=2048)
        out["agent"] = {k: r[k] for k in ("returncode", "wall_s", "cpu_s", "timed_out", "layers")}
    finally:
        srv.terminate()
        try:
            srv.wait(timeout=20)
        except subprocess.TimeoutExpired:
            srv.kill()
        slog.close()
    json.dump(out, open(os.path.join(run, f"rollout_{name}.json"), "w"), indent=1)
    return finalize(run, name)


def bench(world, n=2):
    """CPU seconds per member-tick of the public simulator on this machine (one core, second call)."""
    W = INST.world_module(world)
    import numpy as np
    sim = W.Simulator(chunk=n)
    th = np.tile(W.PRIOR_MEAN, (n, 1))
    H = max(max(v) for v in W.QUERIES.values())
    sim.episodes(th, 1, W.P_PREFIX, H)
    c0, t0, m0 = time.process_time(), time.time(), sim.member_ticks
    sim.episodes(th, 2, W.P_PREFIX, H)
    mt = sim.member_ticks - m0
    return {"world": world, "member_ticks": mt, "cpu_s_per_member_tick": (time.process_time() - c0) / mt,
            "wall_s_per_member_tick": (time.time() - t0) / mt}


def scripted_cmd(policy, sizes, seed=0, theta=None):
    cmd = ["{python}", "-B", "{agent_home}/reference_agent.py", "--policy", policy, "--sizes", json.dumps(sizes),
           "--seed", str(seed)]
    return cmd + (["--theta", ",".join(repr(float(v)) for v in theta)] if theta is not None else [])


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="what", required=True)
    p = sub.add_parser("prepare")
    p.add_argument("--world", required=True)
    p.add_argument("--config", default=None)
    p.add_argument("--run", required=True)
    r = sub.add_parser("rollout")
    r.add_argument("--run", required=True)
    r.add_argument("--name", required=True)
    r.add_argument("--policy", default=None)
    r.add_argument("--sizes", default="{}")
    r.add_argument("--seed", type=int, default=0)
    r.add_argument("--cmd", default=None, help="agent command (shell words); {python} and {agent_home} are replaced")
    r.add_argument("--wall-hours", type=float, default=None)
    for nm in ("workspace", "finalize"):
        q = sub.add_parser(nm)
        q.add_argument("--run", required=True)
        q.add_argument("--name", required=True)
        q.add_argument("--owner", type=int, default=NOBODY)
    q = sub.add_parser("bench")
    q.add_argument("--world", required=True)
    t = sub.add_parser("table")
    t.add_argument("--run", required=True, action="append")
    t.add_argument("--names", required=True)
    a = ap.parse_args()
    if a.what == "prepare":
        cfg = json.load(open(a.config)) if a.config else None
        print(json.dumps(prepare(a.world, cfg, a.run), indent=1))
    elif a.what == "rollout":
        if a.policy:
            theta = None
            if a.policy == "C":                               # the designer's ceiling: the evaluator passes the truth
                theta = json.load(open(os.path.join(a.run, "hidden", "instance.json")))["theta"]
            cmd = scripted_cmd(a.policy, json.loads(a.sizes), a.seed, theta)
        else:
            import shlex
            cmd = shlex.split(a.cmd)
        out = rollout(a.run, a.name, cmd, None if a.wall_hours is None else a.wall_hours * 3600)
        print(json.dumps({k: out.get(k) for k in ("name", "agent", "usage", "grade")}, indent=1, default=str))
    elif a.what == "workspace":
        print(json.dumps(dict(zip(("workspace", "ipc", "agent_home"), workspace(a.run, a.name, a.owner)))))
    elif a.what == "finalize":
        out = finalize(a.run, a.name)
        print(json.dumps({k: out.get(k) for k in ("name", "submitted_before_finalization", "usage", "grade")}, indent=1, default=str))
    elif a.what == "bench":
        print(json.dumps(bench(a.world)))
    else:
        print(json.dumps(GR.table([os.path.join(x, "hidden") for x in a.run], a.names.split(",")), indent=1))


if __name__ == "__main__":
    main()
