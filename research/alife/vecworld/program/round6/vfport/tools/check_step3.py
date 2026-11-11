"""check_step3 -- round 4 end to end through vf-eval, in the cloud container: the box caps from inside a box, and
the request route of step 3 against a local stand-in for the model endpoint.

    VF_RUN_ID=<label> python -B tools/check_step3.py --scratch DIR --out results.json --dev-machine cloud-container [--only caps|route]

A DEVELOPMENT CHECK FOR THE CLOUD CONTAINER (Linux). It is on the never-list of RUNBOOK_MAC.md. It starts
containers through vf-eval only (they carry the run label of VF_RUN_ID), one stand-in server as a child of this
process (stopped by its exact pid), and the tools of this folder. It calls no model and uses no credential.

  caps    agents/probe_caps.py in the agent's box of a scripted rollout, with the box memory lowered to 2 GiB:
          what each cap does when it is hit, read back from the box; the rollout must still be graded.
  route   one rollout driven by a request file (tools/vfrun.py --request ... --stage instance | reference |
          dry-run | rollout, then tools/pack_rollout.py), with the stock bash harness in a capped box and
          tools/standin_model.py in place of the provider. Checked: the refusals of each stage out of order, the
          laboratory's bearer (from the host: no bearer, no answer; inside the box: nothing holds it), the spend
          stop (`spend_cap` ends the run, the run is graded, the ledger closes within its bound), the
          publication folder.

Everything is written under --scratch and left there. Every check is one line in the output JSON with the
numbers it rests on.
"""
import argparse
import datetime
import hashlib
import json
import os
import re
import socket
import subprocess
import sys
import threading
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import vfrun  # noqa: E402

vfrun.require_clean_environment()
CHECKS: list[dict] = []
PY = sys.executable


def check(name, ok, detail=None):
    CHECKS.append({"name": name, "ok": bool(ok), "detail": detail})
    print(("ok   " if ok else "FAIL ") + name + ("" if ok else f"   {json.dumps(detail, default=str)[:600]}"), flush=True)
    return bool(ok)


def tool(args, *, timeout=3600, log=None):
    """One tool of this folder as a child with the tools' own child environment; (status, output)."""
    r = subprocess.run([PY, "-B", *args], cwd=ROOT, env=vfrun.child_env(), capture_output=True, text=True, timeout=timeout, stdin=subprocess.DEVNULL)
    out = r.stdout + r.stderr
    if log:
        with open(log, "a") as f:
            f.write(f"$ {' '.join(args)}\n{out}\n[exit {r.returncode}]\n")
    return r.returncode, out


def last_json(text):
    for line in reversed(text.strip().splitlines()):
        try:
            return json.loads(line)
        except ValueError:
            continue
    return None


def make_instance(store, prefix, profile, log):
    rc, out = tool([os.path.join("tools", "make_instances.py"), "--store", store, "--world", profile["world"], "--config", profile["config_name"],
                    "--n", "1", "--prefix", prefix], log=log)
    return rc == 0, f"{prefix}-w0"


# ----------------------------------------------------------------------------- caps
def run_caps(scratch, tag, floor, log):
    import check_config as CC
    profile = CC.light("profiles").get("ring")
    store, out_dir, notes = os.path.join(scratch, "caps-store"), os.path.join(scratch, "caps-runs"), os.path.join(scratch, "caps-notes")
    ok, iid = make_instance(store, f"pilot-caps-{tag}", profile, log)
    if not check("K0 an instance for the caps probe was made", ok):
        return {}
    with open(os.path.join(store, "PILOT_NEVER_REUSE_AS_EXAM.txt"), "a") as f:
        f.write(f"PILOT_NEVER_REUSE_AS_EXAM: {iid} was made for tools/check_step3.py (caps), never an exam.\n")
    r = vfrun.run_eval(f"caps-{tag}", store=store, out_dir=out_dir, instances=[iid], cpu=2, memory=2, image=profile["image"],
                       harness={"agent_dir": os.path.join(ROOT, "agents"), "script": "probe_caps.py", "label": "caps", "collect": ["caps_report.json"], "collect_dir": notes},
                       task={"item_isolation": "shared"}, disk_floor_gib=floor, timeout=2400)
    if not check("K1 the scripted rollout with the caps probe ended and saved a trace", len(r["episodes"]) == 1, r["log_tail"][-600:]):
        return {}
    x = vfrun.rollout(r["episodes"][0])
    tr = r["episodes"][0]["traces"][0]
    ph = tr.get("info", {}).get("physim2", {})
    rep_f = os.path.join(notes, x["trace_id"], "caps_report.json")
    rep = json.load(open(rep_f)) if os.path.exists(rep_f) else {}
    caps = ph.get("box_caps") or {}
    check("K2 the box was started with the caps and they were read back from the engine (memory lowered to 2 GiB by the run's config)",
          caps.get("memory_gb") == 2 and caps.get("cpus") == 2 and caps.get("pids") == 512 and caps.get("read_only_root") is True
          and ph.get("verifier_box_caps") == caps, caps)
    lim = rep.get("limits_seen") or {}
    check("K3 inside the box: 512 processes, 2 GiB of memory, no swap beyond it, a quota of 2 CPUs",
          lim.get("pids_max") == "512" and lim.get("memory_max") == str(2 << 30) and lim.get("swap_max") in (str(2 << 30), "0", None)
          and re.sub(r"\s+", " ", str(lim.get("cpu_max"))) in ("200000 100000",), lim)
    w = rep.get("write_one_byte") or {}
    ro = {k: v for k, v in w.items() if k in ("/root", "/usr", "/etc", "/opt", "/var/tmp", "/home", "/")}
    check("K4 the root file system is read-only: one byte into /root, /usr, /etc, /opt, /var/tmp, /home or / gives EROFS",
          len(ro) == 7 and all(str(v).startswith("EROFS") for v in ro.values()), ro)
    check("K5 ... and /workspace, /tmp, /dev/shm (and the exam's own /etc/physim2, /runtime) take it",
          all(w.get(k) == "written" for k in ("/workspace", "/tmp", "/dev/shm", "/etc/physim2", "/runtime")), w)
    m = rep.get("mounts") or {}
    check("K6 the mount table of the box: an overlay root mounted read-only, tmpfs of 1 GiB at /workspace and 512 MiB at /tmp",
          (m.get("/") or {}).get("type") == "overlay" and "ro" in str((m.get("/") or {}).get("options")).split(",")
          and "size=1048576k" in str((m.get("/workspace") or {}).get("super")) and "size=524288k" in str((m.get("/tmp") or {}).get("super")), m)
    ft, fw, fs = rep.get("fill_tmp") or {}, rep.get("fill_workspace") or {}, rep.get("fill_shm") or {}
    check("K7 /tmp is full at 512 MiB and /dev/shm at 64 MiB: `No space left on device`",
          511 <= ft.get("mib_written", 0) <= 512 and str(ft.get("error")).startswith("ENOSPC") and 63 <= fs.get("mib_written", 0) <= 64
          and str(fs.get("error")).startswith("ENOSPC"), (ft, fs))
    check("K8 /workspace is full at 1 GiB (it fits into the 2 GiB of this box together with nothing else)",
          1023 <= fw.get("mib_written", 0) <= 1024 and str(fw.get("error")).startswith("ENOSPC"), fw)
    th, fk = rep.get("threads") or {}, rep.get("fork_in_a_shell") or {}
    check("K9 the process limit: threads stop at about 512 with `can't start new thread`; a shell loop gets `Cannot fork`",
          400 <= th.get("threads_started", 0) <= 512 and "can't start new thread" in str(th.get("error")) and "fork" in (str(fk.get("last_line")) + str(fk.get("stderr_last_line"))).lower(), (th, fk))
    mem = rep.get("memory") or {}
    check("K10 the memory limit: a process that touches more than the box has is killed by the kernel (status -9, `Killed`), and the box goes on",
          mem.get("returncode") == -9 and 1500 <= mem.get("mib_reached", 0) <= 2048 and (rep.get("after") or {}).get("write_workspace") == "written", (mem, rep.get("after")))
    g = x.get("grade") or {}
    check("K11 the rollout was graded all the same: the baseline predictor of the box on every item, in capped grading boxes",
          x["graded"] and x["ok"] and g.get("n_items") == 64 and (x.get("submission") or {}).get("ok") is True, {k: g.get(k) for k in ("n_items", "n_failed", "skill_vs_O", "reason")})
    check("K12 the laboratory required its bearer and no container of this run is left",
          ph.get("lab_bearer_required") is True and containers_left() == [], containers_left())
    return {"instance": iid, "trace_id": x["trace_id"], "box_caps": caps, "caps_report": rep, "reward": x["reward_skill_vs_O"], "wall_s": round(r["wall_s"], 1)}


def containers_left():
    r = subprocess.run(["docker", "ps", "-a", "--filter", f"label=verifiers.run={vfrun.run_label()}", "--format", "{{.Names}}"], capture_output=True, text=True,
                       timeout=60, env=vfrun.child_env())
    return [x for x in r.stdout.split() if x]


# ----------------------------------------------------------------------------- the request route
# What the stand-in "model" runs in its box to look for the laboratory's bearer: every 64-hex string in the
# environment and command line of every process and in every file of the writable places, as sha256 (the test
# compares them with the fingerprint the laboratory recorded; the box never learns what it is looking for).
SCAN = r"""python3 - <<'PY'
import hashlib, os, re
seen = set()
def take(b):
    for m in re.findall(rb"[0-9a-f]{64}", b):
        seen.add(hashlib.sha256(m).hexdigest())
take(repr(dict(os.environ)).encode())
for d in os.listdir("/proc"):
    if d.isdigit():
        for n in ("environ", "cmdline"):
            try:
                take(open(f"/proc/{d}/{n}", "rb").read())
            except OSError:
                pass
for root in ("/etc/physim2", "/tmp", "/workspace", "/runtime", "/dev/shm"):
    for base, dirs, names in os.walk(root):
        for n in names:
            p = os.path.join(base, n)
            try:
                if os.path.isfile(p) and os.path.getsize(p) < (8 << 20):
                    take(open(p, "rb").read())
            except OSError:
                pass
if len(seen) > 200:
    print("FINGERPRINTS_TOO_MANY", len(seen))
else:
    print("FINGERPRINTS", len(seen), " ".join(sorted(seen)))
print("ENVNAMES", " ".join(sorted(os.environ)))
print("LABJSON", open("/etc/physim2/lab.json").read())
PY"""
STEPS = [
    {"say": "Looking at the box.", "bash": "cd /workspace && ls && ls submission && python3 -c \"import physim2; lab = physim2.Lab(); print('USAGE', lab.usage())\"; (echo x > /root/x) 2>&1 | tail -n 1",
     "usage": {"prompt_tokens": 20000, "completion_tokens": 100}},
    {"bash": SCAN, "usage": {"prompt_tokens": 20000, "completion_tokens": 100}},
    {"bash": "sleep 25; echo waited", "usage": {"prompt_tokens": 20000, "completion_tokens": 100}},
    {"bash": "echo '# a note' > /workspace/submission/NOTE.txt; ls -la /workspace/submission",
     "usage": {"prompt_tokens": 20000, "completion_tokens": 100}},
    {"bash": "echo this call must never be answered: the cap is spent", "usage": {"prompt_tokens": 20000, "completion_tokens": 100}},
]
FLAT = """schema = "physim2-rollout/v1"
model = "standin/echo-1"
exam_profile = "ring"
instance = "{instance}"
max_turns = 12
max_output_tokens_per_turn = 512
max_context_tokens = 60000
wall_minutes = 10
box_memory_gb = 2
cap_usd = 0.13
reasoning_effort = "default"
push = false
"""


def http_status(port, headers=None, method="POST", path="/mcp", host=None):
    body = b"{}"
    lines = [f"{method} {path} HTTP/1.1", f"Host: {host or f'127.0.0.1:{port}'}", "Connection: close", "Content-Type: application/json", f"Content-Length: {len(body)}"]
    lines += [f"{k}: {v}" for k, v in (headers or {}).items()]
    try:
        with socket.create_connection(("127.0.0.1", port), timeout=10) as c:
            c.sendall(("\r\n".join(lines) + "\r\n\r\n").encode() + body)
            data = b""
            while chunk := c.recv(65536):
                data += chunk
        return int(data.split(b" ")[1]), len(data.partition(b"\r\n\r\n")[2])
    except (OSError, ValueError, IndexError) as e:
        return type(e).__name__, 0


def probe_lab(store, instance, result, stop):
    """While the rollout runs: find the laboratory's port in its own record and talk to it WITHOUT the bearer."""
    labs = os.path.join(store, instance, "hidden", "labs")
    while not stop.is_set():
        try:
            for name in os.listdir(labs):                    # the reference policies left their records here too: theirs are dead
                rec = json.load(open(os.path.join(labs, name, "process.json")))
                if rec.get("port") and "no_bearer" not in result and os.path.isdir(f"/proc/{rec.get('pid')}"):
                    port = rec["port"]
                    if not isinstance(http_status(port)[0], int):       # not listening yet: ask again in a moment
                        continue
                    result.update(port=port, bearer_sha256=rec.get("bearer_sha256"), bearer_required=rec.get("bearer_required"),
                                  no_bearer=http_status(port), get=http_status(port, method="GET"),
                                  random_bearer=http_status(port, {"Authorization": "Bearer " + os.urandom(32).hex()}),
                                  empty_bearer=http_status(port, {"Authorization": "Bearer "}),
                                  other_path=http_status(port, path="/"), lab_pid=rec.get("pid"))
                    try:                                     # the laboratory process itself: its command line and environment (Linux)
                        cmd = open(f"/proc/{rec['pid']}/cmdline", "rb").read()
                        envb = open(f"/proc/{rec['pid']}/environ", "rb").read()
                        cands = set(re.findall(rb"[0-9a-f]{64}", cmd + envb))
                        result["lab_process"] = {"cmdline_bytes": len(cmd), "environ_bytes": len(envb), "hex64_strings": len(cands),
                                                 "bearer_among_them": any(hashlib.sha256(c).hexdigest() == rec.get("bearer_sha256") for c in cands)}
                    except OSError as e:
                        result["lab_process"] = {"error": type(e).__name__}
        except (OSError, ValueError):
            pass
        stop.wait(1.0)


def fingerprints_in(path, target):
    """How many 64-hex strings in the files under `path` hash to `target` (the bearer's fingerprint); (files, strings, hits)."""
    files = strings = hits = 0
    for base, _, names in os.walk(path):
        for nm in names:
            try:
                with open(os.path.join(base, nm), "rb") as f:
                    data = f.read(64 << 20)
            except OSError:
                continue
            files += 1
            for m in set(re.findall(rb"[0-9a-f]{64}", data)):
                strings += 1
                hits += hashlib.sha256(m).hexdigest() == target
    return files, strings, hits


def run_route(scratch, tag, floor, log, skip_reference):
    import check_config as CC
    import check_request as CR
    profile = CC.light("profiles").get("ring")
    pilot = os.path.join(scratch, f"pilot-{tag}")
    os.mkdir(pilot, 0o700)
    os.mkdir(os.path.join(pilot, "configs"), 0o700)
    instance, job = f"pilot-s3-{tag}-w0", f"s3-{tag}"
    cfg = CC.REPO_PREFIX + "standin.toml"                    # the request names its config by the repository path
    script = os.path.join(pilot, "steps.json")
    with open(script, "w") as f:
        json.dump(STEPS, f)
    req = {"schema": "rollout-job/v1", "job_id": job, "purpose": "round-4 rehearsal of the request route against a stand-in endpoint", "requester": "tools/check_step3.py",
           "pin": CR.git_head(), "pin_sha256": CR.pin_sha256(), "config": cfg, "exam_profile": "ring", "instance": instance, "model": "standin/echo-1",
           "caps": {"max_turns": 12, "max_output_tokens": 512, "wall_minutes": 10, "box_memory_gb": 2}, "cap_usd": 0.13}
    rp = os.path.join(pilot, "requests", job + ".json")
    # A scratch repository of this test stands for the lab branch: ONE commit that holds the request, its config and
    # the shared ledger at their real paths. (The real repository never gets a file under rollouts/requests/ from here.)
    repo = os.path.join(scratch, f"repo-{tag}")
    shared = {"schema": "rollout-ledger/v1", "updated_utc": "2026-11-11T12:20:03Z", "billed_usd_total": 0.25, "reserved_usd_open": 0.1,
              "rows": [{"id": "a", "model": "m/x", "where": "cloud-container", "status": "done", "bound_usd": 1.0, "billed_usd": 0.25},
                       {"id": "b", "model": "m/x", "where": "cloud-container", "status": "running", "bound_usd": 0.1}]}
    for rel, textf in ((CR.REQUESTS_PREFIX + job + ".json", json.dumps(req, indent=1)), (cfg, FLAT.format(instance=instance)),
                       (CR.SHARED_LEDGER_PATH, json.dumps(shared, indent=1))):
        os.makedirs(os.path.dirname(os.path.join(repo, rel)), exist_ok=True)
        with open(os.path.join(repo, rel), "w") as f:
            f.write(textf)
    genv = dict(vfrun.child_env(), GIT_CONFIG_GLOBAL="/dev/null", GIT_CONFIG_SYSTEM="/dev/null")
    for argv in (["init", "-q"], ["add", "-A"], ["-c", "user.name=check_step3", "-c", "user.email=check_step3@example.invalid", "commit", "-q", "-m", "a scratch commit of tools/check_step3.py"]):
        subprocess.run(["git", "-C", repo, *argv], check=True, capture_output=True, env=genv, timeout=60)
    commit = subprocess.run(["git", "-C", repo, "rev-parse", "HEAD"], check=True, capture_output=True, text=True, env=genv, timeout=60).stdout.strip()
    from_repo = lambda c, path, limit: CR.git_show(c, path, limit, repo=repo)   # noqa: E731
    got = CR.fetch(pilot, commit, job, show=from_repo)
    check("F1 fetch (real git objects of a scratch repository): the request, its config and the shared ledger arrive in the pilot folder, byte for byte",
          open(rp).read() == json.dumps(req, indent=1) and open(os.path.join(pilot, "configs", "standin.toml")).read() == FLAT.format(instance=instance)
          and abs(got["shared_ledger"]["spent_elsewhere_usd"] - 0.35) < 1e-12 and got["source_commit"] == commit, got)
    try:
        CR.fetch(pilot, "0" * 40, job, show=from_repo)
        f2 = "accepted"
    except CR.Refused as e:
        f2 = str(e)
    check("F2 ... and a commit that the repository does not hold gives a refusal, with the files in the pilot folder untouched",
          "does not hold" in f2 and open(rp).read() == json.dumps(req, indent=1), f2)
    ledger_opt = ["--shared-ledger", os.path.join(pilot, "shared-ledger.json")]
    standin = subprocess.Popen([PY, "-B", os.path.join(HERE, "standin_model.py"), "--script", script, "--log", os.path.join(pilot, "standin_requests.jsonl")],
                               stdout=subprocess.PIPE, text=True, env=vfrun.child_env(), stdin=subprocess.DEVNULL)
    out = {"job_id": job, "instance": instance, "pilot": "<scratch>/" + os.path.basename(pilot)}
    try:
        hello = json.loads(standin.stdout.readline())
        endpoint = hello["base_url"]
        base = [os.path.join("tools", "vfrun.py"), "--request", rp, "--pilot", pilot, "--disk-floor-gib", str(floor), "--stand-in-endpoint", endpoint]

        def stage(name, extra=(), timeout=3600):
            return tool([*base, "--stage", name, *extra], log=log, timeout=timeout)

        rc, o = stage("instance")
        check("R1 without the lead's standing go nothing of step 3 starts", rc == 2 and "no LEAD-GO-MODEL-SPEND.json" in o and not os.path.exists(os.path.join(pilot, "store")), o[-300:])
        with open(os.path.join(pilot, CR.GO_FILE), "w") as f:
            json.dump({"schema": CR.GO_SCHEMA, "ceiling_usd": 5.0, "date": datetime.datetime.now(datetime.timezone.utc).date().isoformat(),
                       "note": "a test's own go for a stand-in endpoint: nothing is billed"}, f)
        rc, o = stage("rollout")
        check("R2 the rollout stage is refused before the instance exists", rc == 2 and "refused:" in o, o[-300:])
        rc, o = stage("instance")
        check("R4 stage instance: the name is registered to the job and the hidden instance is made", rc == 0 and (last_json(o) or {}).get("made") is True
              and CR.instance_state(CR.pilot_paths(pilot), instance) == {"job": job, "in_index": True, "in_store": True}, o[-400:])
        rc, o = stage("instance")
        check("R5 a second `instance` for the same name is refused: a name is used once", rc == 2 and "never used twice" in o, o[-300:])
        rc, o = stage("dry-run")
        check("R6 the dry run is refused before the reference table exists", rc == 2 and "reference table" in o, o[-300:])
        p = CR.pilot_paths(pilot, job)
        if skip_reference:
            with open(p["reference"], "w") as f:
                json.dump({"all_graded": True, "STUB": "written by tools/check_step3.py --skip-reference: the reference stage was not run in this test"}, f)
            out["reference"] = "stub"
        else:
            t0 = time.time()
            rc, o = stage("reference", timeout=5400)
            ref = vfrun.reference_done(p) or {}
            out["reference"] = {"wall_s": round(time.time() - t0, 1), "all_graded": ref.get("all_graded"), "pooled": {k: v.get("vs_O") for k, v in ((ref.get("pooled") or {}).get("policies") or {}).items()}}
            if not check("R7 stage reference: the profile's scripted policies on the job's instance, all graded", rc == 0 and ref.get("all_graded") is True, o[-900:]):
                with open(p["reference"] + ".stub", "w") as f:
                    f.write("the reference stage failed in this test; the route goes on with a stub\n")
                with open(p["reference"], "w") as f:
                    json.dump({"all_graded": True, "STUB": "the reference stage failed in this test (see R7); the route goes on with a stub"}, f)
        rc, o = stage("rollout")
        check("R8 the rollout stage is refused before the free dry run has passed", rc == 2 and "dry run" in o, o[-300:])
        rc, o = stage("dry-run", ledger_opt)
        d = next((json.loads(x) for x in o.splitlines() if x.startswith('{"job_id"')), {})
        worst = (60000 * 2.0 + 512 * 10.0) / 1e6
        check("R9 stage dry-run: listed prices read without a credential; one worst-case call = 60,000 x $2/M + 512 x $10/M = $0.12512; bound = cap + that; vf-eval resolves the config and exits",
              rc == 0 and abs(d.get("one_worst_case_call_usd", 0) - worst) < 1e-6 and abs(d.get("bound_on_the_bill_usd", 0) - 0.13 - worst) < 1e-6 and d.get("billed") is False
              and abs(d.get("crude_bound_without_the_spend_stop_usd", 0) - round(12 * (100000 * 2.0 + 512 * 10.0) / 1e6, 2)) < 0.011
              and abs(d.get("spent_elsewhere_usd", 0) - 0.35) < 1e-9, (rc, d, o[-300:]))
        rc, o = tool([os.path.join("tools", "vfrun.py"), "--request", rp, "--pilot", pilot, "--stage", "rollout", "--disk-floor-gib", str(floor), *ledger_opt], log=log)
        check("R3 the rollout stage WITHOUT the stand-in option and without the credentials option is refused (and the stand-in model is in no provider's list, "
              "if the list answers at all): nothing was started, the ledger is empty", rc == 2 and "refused:" in o and CR.ledger_rows(CR.pilot_paths(pilot, job)) == [], o[-300:])
        out["bounds"] = d
        probe, stop = {}, threading.Event()
        watcher = threading.Thread(target=probe_lab, args=(os.path.join(pilot, "store"), instance, probe, stop), daemon=True)
        watcher.start()
        t0 = time.time()
        rc, o = stage("rollout", ledger_opt, timeout=5400)
        stop.set()
        watcher.join(5)
        out["rollout_wall_s"] = round(time.time() - t0, 1)
        end = next((json.loads(x) for x in reversed(o.splitlines()) if x.startswith('{"job_id"') and '"ended"' in x), {})
        check("R10 stage rollout ran to its end (vf-eval exited by itself with status 0)", rc == 0 and end.get("ended") == "exited", (rc, end, o[-1500:]))
        eps = [json.loads(x) for x in open(os.path.join(p["run_dir"], "traces.jsonl"))] if os.path.exists(os.path.join(p["run_dir"], "traces.jsonl")) else []
        tr = eps[0]["traces"][0] if eps else {}
        ph = (tr.get("info") or {}).get("physim2") or {}
        reward = ((tr.get("rewards") or {}).get("skill") or {}).get("score")
        total = CR.spend_log_total(p["spend_log"])
        check("R11 THE SPEND STOP: four calls at $0.041 pass the cap of $0.13 after the fourth; the fifth is never sent; stop condition `spend_cap`",
              tr.get("stop_condition") == "spend_cap" and total["attempts"] == 4 and abs(total["counted_usd"] - 4 * (20000 * 2.0 + 100 * 10.0) / 1e6) < 1e-9
              and total["complete"], (tr.get("stop_condition"), total, [e.get("type") for e in tr.get("errors", [])]))
        seen = [json.loads(x) for x in open(os.path.join(pilot, "standin_requests.jsonl"))]
        chat = [x for x in seen if x["path"].endswith("/chat/completions")]
        check("R12 ... the stand-in endpoint saw exactly those four requests, each with the reply cap of the run, the rollout's id and a (made-up) key",
              len(chat) == 4 and all(x["max_tokens"] == 512 and x["session"] and x["has_authorization"] and x["model"] == "standin/echo-1" for x in chat), chat)
        check("R13 ... the counted cost is within cap_usd + one worst-case call, and the ledger holds the reservation and the closing row",
              total["counted_usd"] <= 0.13 + worst and [r["event"] for r in CR.ledger_rows(p) if r["job_id"] == job] == ["reserved", "ended"]
              and CR.ledger_rows(p)[-1]["status"] == "done" and CR.ledger_rows(p)[-1]["count_complete"] is True and CR.ledger_rows(p)[-1]["billed"] is False, CR.ledger_rows(p))
        g = ph.get("grade") or {}
        check("R14 RULING E1 through the stop path: the run was finalized and GRADED after the spend stop (64 items in capped boxes)",
              reward is not None and tr.get("ok") is True and g.get("n_items") == 64 and (ph.get("submission") or {}).get("ok") is True,
              {"reward": reward, "ok": tr.get("ok"), "grade": {k: g.get(k) for k in ("n_items", "n_failed", "reason")}, "submission": ph.get("submission")})
        check("R15 the trace records what the run cost as counted on the host", abs(((ph.get("spend") or {}).get("counted_usd") or 0) - total["counted_usd"]) < 1e-9
              and (ph.get("spend") or {}).get("stopped") is None and (ph.get("box_caps") or {}).get("memory_gb") == 2, ph.get("spend"))
        check("R16 THE BEARER, from the host while the run was alive: without it the laboratory answers 401 with an empty body (POST, GET, another path, a random bearer, an empty one)",
              probe.get("bearer_required") is True and all(probe.get(k) == [401, 0] or probe.get(k) == (401, 0) for k in ("no_bearer", "get", "random_bearer", "empty_bearer", "other_path")), probe)
        lp = probe.get("lab_process") or {}
        check("R17 ... the laboratory process holds the bearer neither on its command line nor in its environment", lp.get("bearer_among_them") is False and lp.get("cmdline_bytes", 0) > 0, lp)
        text = json.dumps(tr)
        fp = re.search(r"FINGERPRINTS (\d+) ([0-9a-f ]*)", text)
        box_prints = set((fp.group(2).split() if fp else []))
        check("R18 ... inside the box: of every 64-hex string in the environment of every process and in the files of /etc/physim2, /tmp and /workspace, none is the bearer",
              fp is not None and int(fp.group(1)) >= 0 and not re.search(r"FINGERPRINTS_TOO_MANY \d", text) and probe.get("bearer_sha256") not in box_prints and len(str(probe.get("bearer_sha256"))) == 64, {"strings": fp.group(1) if fp else None})
        names = re.search(r"ENVNAMES ([A-Za-z0-9_ ]*)", text)
        envnames = names.group(1).split() if names else []
        check("R19 ... and the box's environment holds no credential-like name besides the proxy settings verifiers gives a box",
              envnames and not [n for n in envnames if re.search(r"(?i)(api[-_]?key|token|secret|passw|credential|prime|bearer)", n)], envnames)
        check("R20 ... the laboratory was used from inside the box all the same (through the box's proxy, which carries the bearer)",
              (ph.get("lab") or {}).get("requests", 0) >= 1 and (ph.get("lab") or {}).get("infrastructure_errors") == 0 and "USAGE {" in text and "ticks" in text, ph.get("lab"))
        scans = {name: fingerprints_in(path, probe.get("bearer_sha256")) for name, path in (("job folder", p["job"]), ("store", os.path.join(pilot, "store")), ("pilot folder", pilot))}
        check("R21 ... and in the run's outputs (job folder, store, the whole pilot folder): no 64-hex string is the bearer", all(v[2] == 0 and v[0] > 0 for v in scans.values()), scans)
        out["bearer"] = {"probe": {k: v for k, v in probe.items() if k != "bearer_sha256"}, "box_hex64_strings": int(fp.group(1)) if fp else None,
                         "output_scans_files_strings_hits": scans}
        check("R22 the read-only root was what the model's shell saw (`Read-only file system`)", "Read-only file system" in text)
        rc, o = stage("rollout")
        check("R23 the job cannot be run a second time", rc == 2 and "runs once" in o, o[-300:])
        rc, o = stage("close")
        check("R23b stage close has nothing to close: the tool wrote the job's closing row itself", rc == 2 and "nothing to close" in o, o[-300:])
        rc, o = tool([os.path.join("tools", "pack_rollout.py"), "--request", rp, "--pilot", pilot], log=log)
        packed = last_json(o) or {}
        man = json.load(open(os.path.join(p["published"], "MANIFEST.json"))) if os.path.exists(os.path.join(p["published"], "MANIFEST.json")) else {}
        have = sorted(x["path"] for x in man.get("files", []))
        need = ["status.json", "transcript.md", "trace.redacted.jsonl", "lab_log.jsonl", "grades.json", "reference.json", "usage.json", "submission.json", "key_scan.json",
                "request.json", "config.toml", "resolved.toml", "model_entry.json", "PILOT_NEVER_REUSE_AS_EXAM.txt"]
        check("R24 the publication folder: every file of the protocol, a manifest with sha256 and size, a clean key scan",
              rc == 0 and packed.get("key_scan") == "clean" and not [n for n in need if n not in have] and any(h.startswith("submission/") for h in have)
              and man.get("total_bytes", 1 << 40) < 50 << 20, (rc, packed, [n for n in need if n not in have]))
        usage = json.load(open(os.path.join(p["published"], "usage.json"))) if "usage.json" in have else {}
        st = json.load(open(os.path.join(p["published"], "status.json"))) if "status.json" in have else {}
        check("R24b RULING E1: the note that the model's LAST tool call wrote (a call whose result it never saw) is in the frozen, graded submission",
              "submission/NOTE.txt" in have and "submission/predict.py" in have and (ph.get("submission") or {}).get("source") == "final_collection", have)
        check("R25 ... usage.json holds the cost per call and in total; status.json the stop condition, the reward and the caps",
              usage.get("attempts") == 4 and abs((usage.get("counted_usd") or 0) - total["counted_usd"]) < 1e-9 and (st.get("trace") or {}).get("stop_condition") == "spend_cap"
              and (st.get("trace") or {}).get("graded") is True, {"usage": {k: usage.get(k) for k in ("attempts", "counted_usd")}, "trace": st.get("trace", {}).get("stop_condition")})
        pub = fingerprints_in(p["published"], probe.get("bearer_sha256"))
        blob = b"".join(open(os.path.join(base_, n), "rb").read() for base_, _, ns in os.walk(p["published"]) for n in ns)
        check("R26 ... no published file holds the bearer, the scratch path of this machine or the stand-in's key word",
              pub[2] == 0 and scratch.encode() not in blob and vfrun.STAND_IN_VALUE.encode() not in blob, pub)
        check("R27 no container of this run is left", containers_left() == [], containers_left())
        out.update(stop_condition=tr.get("stop_condition"), reward=reward, spend=total, published_files=have, left_out=man.get("left_out"), lab=ph.get("lab"))
    finally:
        standin.terminate()                                  # this test's own child, by its exact pid
        try:
            standin.wait(10)
        except subprocess.TimeoutExpired:
            standin.kill()
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--scratch", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--dev-machine", required=True, choices=["cloud-container"], help="this tool is a development check: say where it runs")
    ap.add_argument("--only", default="caps,route")
    ap.add_argument("--skip-reference", action="store_true", help="route: write a stub reference table instead of running the scripted policies")
    ap.add_argument("--disk-floor-gib", type=float, default=vfrun.DISK_FLOOR_GIB)
    a = ap.parse_args()
    if sys.platform != "linux":
        raise SystemExit("refused: tools/check_step3.py is a development check for the Linux cloud container")
    vfrun.DISK_FLOOR_GIB = a.disk_floor_gib
    vfrun.run_label()
    os.makedirs(a.scratch, exist_ok=True)
    tag = time.strftime("%H%M%S")
    log = os.path.join(a.scratch, f"check_step3-{tag}.log")
    out = {"tool": "tools/check_step3.py", "run_label": vfrun.run_label(), "started_unix": int(time.time()),
           "evidence": "run through vf-eval in the cloud container (Linux x86_64); the model endpoint is tools/standin_model.py on 127.0.0.1; no model, no credential"}
    if "caps" in a.only:
        out["caps"] = run_caps(a.scratch, tag, a.disk_floor_gib, log)
    if "route" in a.only:
        out["route"] = run_route(a.scratch, tag, a.disk_floor_gib, log, a.skip_reference)
    failed = [c["name"] for c in CHECKS if not c["ok"]]
    out.update(n_checks=len(CHECKS), n_failed=len(failed), failed=failed, checks=CHECKS, wall_s=round(time.time() - out["started_unix"], 1))
    text = json.dumps(out, indent=1, default=str).replace(os.path.abspath(a.scratch), "<scratch>")
    with open(a.out, "w") as f:
        f.write(text)
    print(json.dumps({"n_checks": len(CHECKS), "n_failed": len(failed), "failed": failed}))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
