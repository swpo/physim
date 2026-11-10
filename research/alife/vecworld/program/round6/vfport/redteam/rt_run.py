"""rt_run -- RED TEAM driver on the trusted worker: one attack = one `vf-eval` rollout through the port.

Route of every run: vf-eval physim2-env, --env.id isolated-verifier, docker runtime, physim2-script harness,
push = false and PRIME_RUNS_MODE=disabled (tools/vfrun.child_env), no retries, no model, no key.

    python redteam/rt_run.py --store S/store --scratch S/rt --instance rt-ring-w0 recon
    ... overflow | fifo | plainD | hedge --rule "<expr>" | hostile-exit1 | hostile-sigkill | hostile-killall | hostile-hangtar

Writes redteam/results/<attack>.json. The instance is a pilot made for these attacks: results carry
PILOT_NEVER_REUSE_AS_EXAM and no hidden value (no theta, no secret, no history; 16-bit fingerprints of exam
histories appear in the recon result as evidence of the between-item channel).

Host safety (audit of 10 Nov 2026, B5): this tool deletes nothing it did not make and removes no container by a
fixed name. The agent scripts are copied into a NEW directory of --scratch on every call; a run folder of an
earlier call is replaced only if it holds nothing but vf-eval's own files (vfrun.clear_run_dir); the sibling
container of `recon` gets a name of its own and is removed by exactly that name; vf-eval is stopped with SIGTERM
first (vfrun.run_child). VF_RUN_ID must be set (vfrun.run_label). For the cloud container only: not on the Mac.
"""
import argparse
import json
import os
import resource
import secrets
import shutil
import socket
import subprocess
import sys
import tempfile
import threading
import time

import tomli_w

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "tools"))
import vfrun  # noqa: E402
from physim2_env._paths import agentenv_root  # noqa: E402


def listener():
    srv = socket.socket()
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind(("0.0.0.0", 0))
    srv.listen(16)
    hits = []

    def loop():
        while True:
            try:
                c, addr = srv.accept()
                hits.append(addr[0])
                c.close()
            except OSError:
                return
    threading.Thread(target=loop, daemon=True).start()
    return srv, srv.getsockname()[1], hits


def sh(*cmd, timeout=120):
    return subprocess.run(list(cmd), capture_output=True, text=True, timeout=timeout)


def watch_boxes(seen, stop):
    """While the rollout runs: the settings Docker actually applied to each box verifiers started."""
    keys = ("PidsLimit", "Memory", "NanoCpus", "CapAdd", "CapDrop", "SecurityOpt", "ReadonlyRootfs", "StorageOpt", "Ulimits", "Binds", "Privileged",
            "NetworkMode", "UsernsMode", "Tmpfs")
    while not stop.is_set():
        r = sh("docker", "ps", "--format", "{{.Names}}")
        for nm in r.stdout.split():
            if nm.startswith("vf-") and nm not in seen:
                i = sh("docker", "inspect", "--format", "{{json .HostConfig}}|{{json .Mounts}}|{{json .Config.Env}}|{{json .Config.User}}", nm)
                try:
                    hc, mounts, env, user = i.stdout.strip().split("|")
                    hc = json.loads(hc)
                    seen[nm] = {"t": time.time(), "host_config": {k: hc.get(k) for k in keys}, "mounts": json.loads(mounts),
                                "env_names": [e.split("=")[0] for e in json.loads(env) or []], "user": json.loads(user)}
                except Exception:
                    pass
        stop.wait(0.7)


def run(name, a, harness, task=None, agent_timeout=None, timeout=1500):
    out_dir = os.path.join(a.scratch, "runs")
    cfg = {"model": "none/scripted", "num_rollouts": 1, "max_concurrent": 1, "push": False, "output_dir": out_dir, "run": {"name": name},
           "env": {"id": "isolated-verifier", "taskset": {"id": "physim2-env", "store": a.store, "instances": [a.instance]},
                   "agent": {"runtime": {"type": "docker", "cpu": 2}, "harness": dict({"id": "physim2-script"}, **harness),
                             "retries": {"max_retries": 0}},
                   "retries": {"max_retries": 0}, "verifier": {"retries": 0}}}
    # (fixer) single_use is on by default now and names the agent by `agent_key`: one key per attack
    cfg["env"]["taskset"]["task"] = dict({"agent_key": name}, **(task or {}))
    if agent_timeout:
        cfg["env"]["agent"]["timeout"] = agent_timeout
    vfrun.run_label()
    vfrun.require_docker()
    os.makedirs(out_dir, exist_ok=True)
    run_dir = os.path.join(out_dir, name)
    vfrun.clear_run_dir(run_dir, name)
    toml = os.path.join(out_dir, f"{name}.toml")
    with open(toml, "wb") as f:
        tomli_w.dump(cfg, f)
    seen, stop = {}, threading.Event()
    th = threading.Thread(target=watch_boxes, args=(seen, stop), daemon=True)
    th.start()
    t0, r0 = time.time(), resource.getrusage(resource.RUSAGE_CHILDREN)
    cmd = ["nice", "-n", "10", vfrun.VF_EVAL, "@", toml, "--no-rich"]
    try:
        rc, out, err, how = vfrun.run_child(cmd, env=vfrun.child_env(), cwd=out_dir, timeout=timeout)
        rc, log = (rc if how == "exited" else "TIMEOUT"), out + err
    finally:
        stop.set()
    th.join(3)
    r1 = resource.getrusage(resource.RUSAGE_CHILDREN)
    eps = []
    f = os.path.join(run_dir, "traces.jsonl")
    if os.path.exists(f):
        eps = [json.loads(line) for line in open(f)]
    return {"episodes": eps, "wall_s": time.time() - t0, "returncode": rc, "run_dir": run_dir, "log_tail": log[-2500:], "boxes": seen,
            "host_cpu_s": (r1.ru_utime + r1.ru_stime) - (r0.ru_utime + r0.ru_stime),
            "command": " ".join(cmd[2:]) + f"   # config: {os.path.relpath(toml, a.scratch)}", "config": cfg}


def needles(a):
    inst = json.load(open(os.path.join(a.store, a.instance, "hidden", "instance.json")))
    n = {"secret_hex": inst["secret_hex"]}
    for nm, v in zip(inst["theta_names"], inst["theta"]):
        n[f"theta_{nm}"] = repr(float(v))[:10]
    return n


def scan(paths, nd):
    found, files = {k: 0 for k in nd}, 0
    for base in paths:
        for root, _, fs in os.walk(base):
            for nm in fs:
                p = os.path.join(root, nm)
                raws = [open(p, "rb").read()]
                if nm.endswith(".tgz"):
                    import tarfile
                    try:
                        with tarfile.open(p) as t:
                            raws += [t.extractfile(m).read() for m in t.getmembers() if m.isfile()]
                    except Exception:
                        pass
                files += len(raws)
                for raw in raws:
                    for k, v in nd.items():
                        found[k] += v.encode() in raw
    return {"files_and_members_scanned": files, "hits": found}


def probe_items(rec):
    items = []
    for e in rec.get("errors", []):
        t = e["error"]
        if "PROBE" in t:
            try:
                items.append(dict(json.loads(t[t.index("PROBE") + 5:t.rindex("}") + 1]), item=e["item"]))
            except Exception:
                items.append({"item": e["item"], "unparsed": t[-200:]})
        else:
            items.append({"item": e["item"], "raw": t[:300]})
    return items


def analyse_vprobe(items):
    ok = [i for i in items if "fp" in i]
    out = {"items_reporting": len(ok)}
    if not ok:
        return out
    fps = [i["fp"] for i in ok]
    # access-time channel: item k must read exactly the fingerprints of items 0..k-1
    exact = [i["chan_seen"] == fps[:n] for n, i in enumerate(ok)]
    out["atime_channel"] = {"items_that_read_every_earlier_fingerprint_exactly": int(sum(exact)), "of": len(ok),
                            "bits_carried_to_last_item": 16 * len(ok[-1]["chan_seen"]) if isinstance(ok[-1]["chan_seen"], list) else 0,
                            "example_item_3_read": ok[3]["chan_seen"] if len(ok) > 3 else None, "fingerprints_of_items_0_2": fps[:3],
                            "idx_reported": [i.get("idx") for i in ok[:6]]}
    # pid counter: pid(k+1) - pid(k) - forked(k) should be a constant (the driver's own forks)
    d = [ok[n + 1]["pid"] - ok[n]["pid"] - ok[n]["forked"] for n in range(len(ok) - 1) if isinstance(ok[n].get("pid"), int)]
    out["pid_channel"] = {"residual_pid_step_minus_forks": sorted(set(d))[:12], "forked_range": [min(i["forked"] for i in ok), max(i["forked"] for i in ok)],
                          "decodable_if_residual_is_constant_per_section": True, "residual_counts": {str(v): d.count(v) for v in sorted(set(d))[:12]},
                          "sections": [i.get("sec") for i in ok[:8]], "residual_first_8": d[:8]}
    for dname in ("/var/tmp", "/dev/shm"):
        hit = [ok[n + 1]["mt"].get(dname) == ok[n]["mt_set"] for n in range(len(ok) - 1) if isinstance(ok[n + 1].get("mt"), dict)]
        out.setdefault("dir_mtime_channel", {})[dname] = {"next_item_read_the_phase_set": int(sum(hit)), "of": len(hit)}
    out["hardlink"] = {"results": sorted({str(i.get("hl")) for i in ok}), "later_items_saw_links": sum(bool(i.get("hl_seen")) for i in ok[1:])}
    out["mqueue"] = {"made": sorted({str(i.get("mq_made")) for i in ok}), "seen_by_later_items": sorted({str(i.get("mq_seen")) for i in ok[1:]})}
    out["sysv_shm_chowned_to_root"] = {"chown": sorted({str(i.get("shm_chown")) for i in ok}), "seen_by_later_items": sorted({str(i.get("shm_seen")) for i in ok[1:]})}
    out["atime_elsewhere"] = {"first_items": [i.get("at") for i in ok[:3]]}
    for sec in ("identity", "network", "files", "limits"):
        got = [i[sec] for i in ok if sec in i]
        out[sec] = got[0] if got else None
        out[f"{sec}_items"] = len(got)
    out["seconds_per_item"] = [min(i["s"] for i in ok), max(i["s"] for i in ok)]
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("attack")
    ap.add_argument("--store", required=True)
    ap.add_argument("--scratch", required=True)
    ap.add_argument("--instance", default="rt-ring-w0")
    ap.add_argument("--rule", default="not test.any()")
    ap.add_argument("--scoring-timeout", type=float, default=None)
    ap.add_argument("--finalize-timeout", type=float, default=None)
    ap.add_argument("--tag", default="")
    a = ap.parse_args()
    os.makedirs(a.scratch, exist_ok=True)
    # reference agents of round 5 + the red-team scripts, top level, in a directory made now (nothing is deleted)
    agents = tempfile.mkdtemp(prefix="agents-", dir=a.scratch)
    os.chmod(agents, 0o755)
    for d in (os.path.join(agentenv_root(), "agents"), HERE):
        for nm in os.listdir(d):
            if nm.endswith(".py"):
                shutil.copy(os.path.join(d, nm), os.path.join(agents, nm))
    notes = os.path.join(a.scratch, "notes")
    hidden = os.path.join(a.store, a.instance, "hidden")
    name = f"rt-{a.attack}{a.tag}"
    res = {"attack": a.attack, "PILOT_NEVER_REUSE_AS_EXAM": True, "instance_id": a.instance,
           "route": "vf-eval physim2-env --env.id isolated-verifier, docker runtime, physim2-script harness, push=false, PRIME_RUNS_MODE=disabled"}
    srv, port, hits = listener()
    sib, sib_name = None, None
    tmo = {k: v for k, v in (("scoring", a.scoring_timeout), ("finalize", a.finalize_timeout)) if v} or None
    try:
        if a.attack == "recon":
            sib_name = "rt-sibling-" + secrets.token_hex(6)      # a name of this call's own; no container is removed by a fixed name
            made = sh("docker", "run", "-d", "--rm", "--label", f"verifiers.run={vfrun.run_label()}", "--name", sib_name,
                      "python:3.12-slim", "python3", "-m", "http.server", "9000")
            if made.returncode:
                raise SystemExit("could not start the sibling container: " + made.stderr.strip()[-200:])
            time.sleep(1.5)
            ip = sh("docker", "inspect", "--format", "{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}", sib_name).stdout.strip()
            sib = f"{ip}:9000"
            ctl = sh("docker", "run", "--rm", "python:3.12-slim", "python3", "-c",
                     "import socket,struct\n"
                     "gw=[socket.inet_ntoa(struct.pack('<L',int(l.split()[2],16))) for l in open('/proc/net/route').read().splitlines()[1:] if l.split()[1]=='00000000'][0]\n"
                     f"o=[]\nfor h,p in ((gw,{port}),('{ip}',9000)):\n try:\n  socket.create_connection((h,p),timeout=3).close(); o.append('REACHED')\n except Exception as e:\n  o.append(type(e).__name__)\nprint(o)")
            res["control_uncut_container"] = {"gateway_host_listener, sibling": ctl.stdout.strip(), "listener_hits": len(hits)}
            h = {"agent_dir": agents, "script": "agent_rt.py", "args": ["recon", "--host-port", str(port), "--sibling", sib],
                 "collect": ["rt_report.json", "rt_box.tgz"], "collect_dir": notes}
        elif a.attack in ("overflow", "fifo"):
            h = {"agent_dir": agents, "script": "agent_rt.py", "args": [a.attack], "collect": ["rt_report.json"], "collect_dir": notes}
        elif a.attack == "hedge":
            h = {"agent_dir": agents, "script": "agent_rt.py", "args": ["hedge", "--rule", a.rule], "collect": ["rt_report.json"], "collect_dir": notes}
        elif a.attack == "plainD":
            h = {"agent_dir": agents, "script": "reference_agent.py", "args": ["--policy", "D", "--seed", "0"]}
        elif a.attack == "null":
            h = {"agent_dir": agents, "script": "reference_agent.py", "args": ["--policy", "null", "--seed", "0", "--sizes", '{"n_train": 256}']}
        elif a.attack.startswith("hostile-"):
            h = {"agent_dir": agents, "script": "agent_rt.py", "args": ["hostile", a.attack.split("-", 1)[1]], "collect": ["rt_report.json"], "collect_dir": notes}
        else:
            raise SystemExit("unknown attack")
        h["label"] = name
        hits0 = len(hits)
        r = run(name, a, h, agent_timeout=tmo)
    finally:
        srv.close()
        if sib_name:
            sh("docker", "rm", "-f", sib_name)               # exactly the container this call started
    res.update(command=r["command"], returncode=r["returncode"], wall_s=r["wall_s"], episodes_saved=len(r["episodes"]),
               timeouts_overridden=tmo, host_listener_hits_during_rollout=len(hits) - hits0, boxes=r["boxes"])
    if not r["episodes"]:
        res["log_tail"] = r["log_tail"]
    else:
        ep = r["episodes"][0]
        x = vfrun.rollout(ep)
        tr = ep["traces"][0]
        res["rollout"] = {k: x[k] for k in ("trace_id", "ok", "errors", "stop_condition", "graded", "reward_skill_vs_O", "scored_as_K_because_ungraded",
                                             "script_exit_code", "submission", "lab", "grade", "verifier_box", "wall_s")}
        res["rollout"]["reward_raw_in_trace"] = repr((tr.get("rewards", {}).get("skill") or {}).get("score"))
        res["rollout"]["trace_reward_field"] = repr(tr.get("reward"))
        res["rollout"]["trace_error_messages"] = [str(e.get("message"))[:300] for e in tr.get("errors", [])]
        res["rollout"]["episode_ok"], res["rollout"]["episode_errors"] = ep.get("ok"), [str(e.get("type")) + ": " + str(e.get("message"))[:200] for e in ep.get("errors", [])]
        res["rollout"]["script_log_tail"] = (tr.get("info", {}).get("physim2_script", {}).get("log_tail") or "")[-500:]
        tid = x["trace_id"]
        f = os.path.join(hidden, "grades", f"{tid}.json")
        rec = json.load(open(f)) if os.path.exists(f) else {}
        res["grade_record"] = {k: rec.get(k) for k in ("n_items", "n_failed", "reason", "box_not_clean_after_item", "seconds", "layers")}
        res["grade_record"]["first_errors"] = [str(e["error"])[:160] for e in rec.get("errors", [])[:2]] if a.attack != "recon" else None
        rep = os.path.join(notes, tid, "rt_report.json")
        if os.path.exists(rep):
            res["agent_report"] = json.load(open(rep))
        if a.attack == "recon":
            items = probe_items(rec)
            res["verifier_box_probe"] = analyse_vprobe(items)
            res["verifier_box_cleanups_first_3"] = rec.get("cleanups", [])[:3]
        if a.attack in ("plainD", "hedge", "null"):
            import numpy as np
            from physim2_env import grading as G
            ex = G.exam(hidden)
            refs = ex.references()
            z = np.load(os.path.join(hidden, "grades", f"{tid}.npz"))
            es, failed = z["es"], z["failed"]
            valid = np.array(x["grade"]["valid_cells"], bool)
            per = {}
            for c in sorted(set(ex.classes.tolist())):
                m = ex.classes == c
                per[c] = {"items": int(m.sum()), "failed": int(failed[m].sum()), "L_agent": float(es[m][:, valid].sum(1).mean()),
                          "L_K": float(refs["K"][m][:, valid].sum(1).mean()), "L_O": float(refs["O"][m][:, valid].sum(1).mean())}
            res["per_program_class"] = per
            cf = {}
            for c in per:                                    # counterfactual: the same scores with class c crashed (scored as K)
                e2 = es.copy()
                e2[ex.classes == c] = refs["K"][ex.classes == c]
                cf[c] = G.summary(ex, e2, refs)["skill_vs_O"]
            res["skill_if_this_class_had_crashed"] = cf
            worse = (es[:, valid].sum(1) > refs["K"][:, valid].sum(1))
            e3 = es.copy()
            e3[worse] = refs["K"][worse]
            res["items_where_agent_is_worse_than_K"] = int(worse.sum())
            res["skill_if_exactly_those_items_had_crashed"] = G.summary(ex, e3, refs)["skill_vs_O"]
            res["test_program_is_all_zero_by_class"] = {c: float(np.mean([not ex.test[i].any() for i in np.flatnonzero(ex.classes == c)])) for c in per}
            res["test_program_max_abs_by_class"] = {c: float(np.mean([np.abs(ex.test[i]).max() for i in np.flatnonzero(ex.classes == c)])) for c in per}
            res["test_program_nonzero_ticks_by_class"] = {c: float(np.mean([np.any(ex.test[i] != 0, axis=1).sum() for i in np.flatnonzero(ex.classes == c)])) for c in per}
        nd = needles(a)
        res["hidden_value_scan"] = scan([r["run_dir"]] + ([os.path.join(notes, tid)] if os.path.isdir(os.path.join(notes, tid)) else []), nd)
        blob = json.dumps(res)
        res["hidden_value_in_this_result_file"] = any(v in blob for v in nd.values())
    os.makedirs(os.path.join(HERE, "results"), exist_ok=True)
    out = os.path.join(HERE, "results", f"{a.attack}{a.tag}.json")
    text = json.dumps(res, indent=1, default=str)            # the per-rollout callback route of a finished box: not kept
    open(out, "w").write(__import__("re").sub(r"/\.vf-host/[A-Za-z0-9_\-]{20,}", "/.vf-host/<per-rollout-route-redacted>", text))
    ro = res.get("rollout", {})
    print(json.dumps({"attack": a.attack, "wall_s": round(r["wall_s"]), "rc": r["returncode"], "episodes": len(r["episodes"]), "graded": ro.get("graded"),
                      "ok": ro.get("ok"), "reward": ro.get("reward_raw_in_trace"), "errors": ro.get("errors"), "out": out}))


if __name__ == "__main__":
    main()
