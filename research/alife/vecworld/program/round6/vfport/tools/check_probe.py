"""check_probe -- boundary checks of the verifiers route on a fresh ring instance (config probe_ring).

Part 1  agentenv's agents/probe_agent.py, unmodified, run in the agent's box by the scripted harness: the 34
        boundary checks of round 5 (results/probe_ring.json there), each evaluated where it now lives.
Part 2  four new probes:
        (a) a predictor that leaves files, a shared-memory segment and a background process on every item finds
            none of them on the next item; with the cleanup switched off (control) it finds all of them
        (b) with a canary value in the worker's environment under a token-like name (HF_TOKEN), scripts dump the
            environment and the files of both boxes and find no canary; the saved traces contain neither the
            canary nor a hidden value
        (c) network checks from inside both boxes: no route except the declared ones
        (d) deleting submission/ (and five other ways of breaking the collection) gives a K score, never an
            ungraded rollout
Every check is a named boolean with its evidence; the output holds no hidden value.

usage: python tools/check_probe.py --store DIR --scratch DIR --out results/probe_ring.json
"""
import argparse
import json
import os
import secrets
import socket
import subprocess
import sys
import threading
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)
sys.path.insert(0, HERE)
import vfrun  # noqa: E402
from physim2_env._paths import agentenv_root  # noqa: E402

HOSTILE = ["delete", "empty", "oversize", "huge", "no_tar", "symlinks", "junk"]
STOCK = ["delete", "huge", "no_tar", "symlinks", "junk"]


def listener():
    """A TCP listener on every host interface: the thing a box must NOT be able to reach."""
    srv = socket.socket()
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind(("0.0.0.0", 0))
    srv.listen(16)
    hits = []

    def loop():
        while True:
            try:
                c, addr = srv.accept()
                hits.append({"from": addr[0], "t": time.time()})
                c.close()
            except OSError:
                return
    threading.Thread(target=loop, daemon=True).start()
    return srv, srv.getsockname()[1], hits


def uncut_container(port, image):
    """Control: the same image WITHOUT verifiers' network policy reaches the listener through the bridge gateway."""
    code = ("import socket,struct\n"
            "gw=[socket.inet_ntoa(struct.pack('<L',int(l.split()[2],16))) for l in open('/proc/net/route').read().splitlines()[1:] if l.split()[1]=='00000000'][0]\n"
            f"try:\n socket.create_connection((gw,{port}),timeout=3).close(); print('REACHED')\nexcept Exception as e:\n print(type(e).__name__)\n")
    r = subprocess.run(["docker", "run", "--rm", image, "python3", "-c", code], capture_output=True, text=True, timeout=120)
    return r.stdout.strip() or r.stderr.strip()[-200:]


def probe_json(text):
    if not text or "PROBE" not in text:
        return None
    try:
        return json.loads(text[text.index("PROBE") + 5:text.rindex("}") + 1])
    except Exception:
        return None


def grade_record(store, iid, trace_id):
    f = os.path.join(store, iid, "hidden", "grades", f"{trace_id}.json")
    return json.load(open(f)) if os.path.exists(f) else {}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--store", required=True)
    ap.add_argument("--scratch", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--image", default="physim2-ring:1")
    ap.add_argument("--cpu", type=float, default=2)
    a = ap.parse_args()
    t0 = time.time()
    iid = "probe-ring-w0"
    idx = os.path.join(a.store, "index.json")
    if not (os.path.exists(idx) and any(r["instance_id"] == iid for r in json.load(open(idx)))):
        subprocess.run([sys.executable, "-B", os.path.join(HERE, "make_instances.py"), "--store", a.store, "--world", "ring",
                        "--config", "probe_ring", "--n", "1", "--prefix", "probe-ring"], check=True, env=vfrun.child_env())
    hidden = os.path.join(a.store, iid, "hidden")
    out_dir, notes = os.path.join(a.scratch, "runs"), os.path.join(a.scratch, "notes")
    canary = "physim2-" + "canary-" + secrets.token_hex(12)
    wenv = {"HF_TOKEN": canary}
    srv, port, hits = listener()
    control = uncut_container(port, a.image)
    control_hits = len(hits)
    ae, mine = agentenv_root(), os.path.join(ROOT, "agents")
    host_paths = [hidden, os.path.join(hidden, "instance.json"), os.path.join(hidden, "exam.npz"), ae, ROOT, a.store]
    common = dict(store=a.store, out_dir=out_dir, instances=[iid], cpu=a.cpu, env=wenv)
    runs = {}

    def go(name, harness, task=None, may_fail=False):
        r = vfrun.run_eval(name, harness=dict(harness, collect_dir=notes), task=task, **common)
        if len(r["episodes"]) != 1:
            if not may_fail:
                raise SystemExit(f"{name}: no episode saved\n{r['log_tail']}")
            runs[name] = {"graded": False, "ok": False, "reward_skill_vs_O": 0.0, "errors": ["no episode saved"], "episode_errors": [],
                          "grade": {}, "submission": None, "wall_s": {}, "cpu_s": {}, "info": {}, "invocation_wall_s": r["wall_s"],
                          "address_file_matches_tool_url": None, "run_dir": r["run_dir"]}
            print(f"{name}: no episode saved ({time.time() - t0:.0f}s)", flush=True)
            return runs[name]
        x = vfrun.rollout(r["episodes"][0])
        x["episode_errors"] = [e.get("type") for e in r["episodes"][0].get("errors", [])]
        x["episode_ok"] = r["episodes"][0].get("ok")
        x["invocation_wall_s"], x["run_dir"] = r["wall_s"], r["run_dir"]
        runs[name] = x
        print(f"{name}: graded={x['graded']} ok={x['ok']} reward={x['reward_skill_vs_O']:.3f} ({time.time() - t0:.0f}s)", flush=True)
        return x

    # ---- part 1: round 5's probe agent, unmodified ----
    A = go("probe-agent", {"agent_dir": os.path.join(ae, "agents"), "script": "probe_agent.py", "label": "probe_agent",
                           "env": {"PHYSIM2_PROBE_PATHS": ":".join(host_paths)}, "collect": ["probe_report.json"]})
    rep = json.load(open(os.path.join(notes, A["trace_id"], "probe_report.json")))
    # ---- part 2 ----
    B = go("probe-grading", {"agent_dir": mine, "script": "probe_grading.py", "label": "probe_grading",
                             "args": ["--host-port", str(port)], "collect": ["probe_grading_report.json"]})
    hits_after_probe = len(hits)
    B0 = go("probe-grading-nocleanup", {"agent_dir": mine, "script": "probe_grading.py", "label": "probe_grading_control",
                                        "args": ["--host-port", str(port)]}, task={"item_cleanup": False})
    for mode in HOSTILE:
        go(f"hostile-{mode}", {"agent_dir": mine, "script": "hostile_submission.py", "label": f"hostile_{mode}", "args": [mode]})
    for mode in STOCK:                                       # control: the same agents under verifiers' default collection
        go(f"stock-{mode}", {"agent_dir": mine, "script": "hostile_submission.py", "label": f"stock_{mode}", "args": [mode]},
           task={"stock_collection": True}, may_fail=True)
    # ---- operator guards (memo hole 4) ----
    G3 = go("guard-token-env", {"agent_dir": mine, "script": "hostile_submission.py", "label": "guard_token", "args": ["empty"],
                                "env": {"HF_TOKEN": "not-a-real-token"}}, may_fail=True)
    G4 = go("guard-single-use", {"agent_dir": mine, "script": "hostile_submission.py", "label": "guard_single_use", "args": ["empty"]},
            task={"single_use": True}, may_fail=True)
    labs_after = sorted(os.listdir(os.path.join(hidden, "labs")))
    srv.close()

    # ---- evaluate part 1 ----
    def rejected(name, kind=None, text=None):
        r = rep.get(name, {})
        return bool(r and not r["ok"] and (kind is None or r.get("kind") == kind) and (text is None or text in r.get("error", "")))

    def val(name):
        v = rep.get(name, {}).get("value")
        return v if isinstance(v, dict) else {}
    leak_txt = val("validate_leak").get("error", "")
    leak = probe_json(leak_txt) or {}
    hid = [p for p in host_paths if p.startswith(a.store)]

    def unreadable(v):
        return v in ("FileNotFoundError", "PermissionError", "NotADirectoryError") or v == []
    agent_reads = {p: rep.get(f"read:{p}", {}) for p in host_paths}
    gB = grade_record(a.store, iid, B["trace_id"])
    items = [probe_json(e["error"]) for e in gB.get("errors", [])]
    items = [i for i in items if i]
    gA = A["grade"]
    n_items = gB.get("n_items", 0)
    P = {  # the four predictor checks, where they hold: in the agent's box (validation) and in the grader's box
        "uid": {"validation": leak.get("uid"), "grading": sorted({i["box"]["uid"] for i in items})},
        "hidden": {"validation": {("hidden" + p[len(hidden):] if p.startswith(hidden) else os.path.basename(p)): str(leak.get(p)) for p in host_paths}},
        "net": {"validation": leak.get("net"), "grading": sorted({i["box"]["net"]["public_tcp"] for i in items})},
        "write_submission": {"validation": leak.get("write_submission"), "grading": sorted({i["write_submission"] for i in items})},
    }
    checks = {
        "agent_runs_unprivileged": None,
        "agent_cannot_read_hidden": all((not agent_reads[p].get("ok")) or agent_reads[p]["value"] == {"listing": []} for p in hid),
        "agent_cannot_read_evaluator_code": all(not agent_reads[p].get("ok") for p in (ae, ROOT)),
        "agent_sees_only_its_own_processes": rep.get("visible_pids", 99) <= 6,
        "agent_has_no_network": rejected("network"),
        "agent_cannot_write_outside_workspace": None,
        "advance_before_reset_rejected": rejected("advance_before_reset"),
        "tick_cap_rejected": rejected("tick_cap", "violation", "per-tick cap"),
        "bounds_rejected": rejected("bounds", "violation", "bound"),
        "episode_cap_rejected_as_a_block": rejected("episode_cap_whole_block", "violation", "episode"),
        "nan_rejected": rejected("nan_input"),
        "bad_shape_rejected": rejected("bad_shape"),
        "oversized_block_rejected": rejected("too_many_ticks"),
        "rejections_charged_nothing": rep.get("rejections_charged_nothing") is True,
        "accepted_block_charged": abs(rep.get("nats_after_accepted_block", 0) - 4 * 1.9) < 1e-6,
        "tick_budget_rejected": rejected("tick_budget", "budget"),
        "unknown_operation_rejected": rejected("unknown_op"),
        "extra_argument_rejected": rejected("extra_argument"),
        "submission_path_confined": rejected("submit_outside_workspace"),
        "missing_submission_reported": val("submit_missing").get("ok") is False,
        "symlink_not_followed": val("submit_symlink").get("ok") is False,
        "bad_shape_fails_validation": val("validate_bad_shape").get("ok") is False,
        "nondeterminism_fails_validation": val("validate_nondeterministic").get("stage") == "reproducibility",
        "cpu_limit_enforced": val("validate_slow").get("ok") is False and val("validate_slow").get("cpu_s", 99) < 6.0
        and "wall-clock" not in val("validate_slow").get("error", ""),
        "memory_limit_enforced": val("validate_memory").get("ok") is False,
        "size_limit_enforced": val("validate_oversize").get("ok") is False,
        "predictor_runs_unprivileged": leak.get("uid") == 1000 and P["uid"]["grading"] == [1000],
        "predictor_cannot_read_hidden": bool(leak) and all(unreadable(leak.get(p)) for p in hid),
        "predictor_has_no_network": leak.get("net") not in (None, "REACHABLE") and bool(items) and "REACHED" not in P["net"]["grading"],
        "predictor_cannot_write_submission": leak.get("write_submission") not in (None, "WRITABLE") and bool(items)
        and "WRITABLE" not in P["write_submission"]["grading"],
        "good_submission_validates": val("validate_good").get("ok") is True,
        "submit_freezes": val("submit_good").get("accepted") is True and bool(A["submission"]) and A["submission"]["source"] == "agent_submission",
        "lab_closed_after_submit": rejected("reset_after_submit", "closed"),
        "graded_without_failures": A["graded"] and gA.get("n_failed") == 0,
    }
    changed = {
        "agent_runs_unprivileged": f"not reproduced by design: the agent is root (uid {rep.get('uid')}) INSIDE its own disposable container, "
                                   "started by verifiers without NET_ADMIN/NET_RAW and with no-new-privileges; round 5 ran it as uid 65534 "
                                   "on the evaluator's machine. Nothing of the host is mounted in the box.",
        "agent_cannot_write_outside_workspace": f"not reproduced by design: the whole box is the agent's (probe result: "
                                                f"{rep.get('write_outside_workspace', {}).get('ok')}); what it cannot reach is anything "
                                                "outside the container, which the read and network checks cover.",
    }

    # ---- evaluate part 2 ----
    gB0 = grade_record(a.store, iid, B0["trace_id"])
    items0 = [i for i in (probe_json(e["error"]) for e in gB0.get("errors", [])) if i]
    cl = gB.get("cleanups", [])
    ab = json.load(open(os.path.join(notes, B["trace_id"], "probe_grading_report.json")))["agent_box"]
    lab_proc = json.load(open(os.path.join(hidden, "labs", B["trace_id"], "process.json")))
    inst = json.load(open(os.path.join(hidden, "instance.json")))
    needles = {"canary": canary, "canary_prefix": "physim2-" + "canary-", "secret_hex": inst["secret_hex"]}
    for n, v in zip(inst["theta_names"], inst["theta"]):
        needles[f"theta_{n}"] = repr(float(v))[:10]
    del inst
    found, scanned = {k: [] for k in needles}, 0
    for base in (out_dir, notes):
        for root, _, files in os.walk(base):
            for nm in files:
                p = os.path.join(root, nm)
                raw = open(p, "rb").read()
                scanned += 1
                for k, v in needles.items():
                    if v.encode() in raw:
                        found[k].append(os.path.relpath(p, a.scratch))
    vb_net = {k: sorted({i["box"]["net"][k] for i in items}) for k in (items[0]["box"]["net"] if items else {})}
    hostile = {m: runs[f"hostile-{m}"] for m in HOSTILE}
    stock = {m: runs[f"stock-{m}"] for m in STOCK}
    new = {
        # (a)
        "a_every_item_ran_the_probe": len(items) == n_items > 1,
        "a_no_item_found_a_file_left_earlier": bool(items) and all(i["found_files"] == [] for i in items),
        "a_no_item_found_the_background_process": bool(items) and all(i["daemon_alive"] is False and i["other_processes_of_my_user"] == 0 for i in items),
        "a_no_item_found_the_shared_memory_mark": bool(items) and all(i["found_shm"] is False for i in items),
        "a_cleanup_removed_something_after_every_item": len(cl) == n_items and all(c["killed"] >= 1 and c["removed"] >= 3 and c["ipc_removed"] >= 1 for c in cl),
        "a_box_clean_after_every_item": gB.get("box_not_clean_after_item") is None,
        "a_control_without_cleanup_finds_them": len(items0) > 1 and all(len(i["found_files"]) == 3 and i["daemon_alive"] and i["found_shm"] for i in items0[1:])
        and items0[0]["found_files"] == [],
        # (b)
        "b_canary_was_in_the_worker_environment": "HF_TOKEN" in lab_proc.get("scrubbed_variables", []),
        "b_lab_process_dropped_it_after_loading": lab_proc.get("token_values_left_in_environ") is False,
        "b_no_canary_in_agent_box": ab["env_needle"] == [] and ab["needle_hits"] == [] and ab["files_read"] > 1000,
        "b_no_token_like_variable_in_agent_box": ab["env_token_like"] == [],
        "b_no_canary_in_verifier_box": bool(items) and all(i["box"]["env_needle"] == [] and i["box"]["needle_hits"] == [] and i["box"]["files_read"] > 1000 for i in items),
        "b_no_token_like_variable_in_verifier_box": bool(items) and all(i["box"]["env_token_like"] == [] for i in items),
        "b_canary_absent_from_saved_traces": found["canary"] == [] and found["canary_prefix"] == [],
        "b_hidden_values_absent_from_saved_traces": all(found[k] == [] for k in found if k.startswith(("secret", "theta"))),
        # (c)
        "c_control_uncut_container_reaches_host_listener": control == "REACHED" and control_hits >= 1,
        "c_agent_box_no_public_route": ab["net"]["public_tcp"] != "REACHED" and ab["net"]["public_tcp_443"] != "REACHED" and ab["net"]["dns"] != "RESOLVED",
        "c_agent_box_cannot_reach_host_listener": ab["net"]["host_listener"] != "REACHED",
        "c_agent_box_proxy_refuses_other_destinations": ab["net"]["proxy_public"] == "HTTP 403" and ab["net"]["proxy_host_listener"] == "HTTP 403",
        "c_agent_box_reaches_the_lab": ab["net"]["lab"].startswith("HTTP ") and A["address_file_matches_tool_url"] is True,
        "c_verifier_box_no_public_route": bool(items) and all(i["box"]["net"]["public_tcp"] != "REACHED" and i["box"]["net"]["public_tcp_443"] != "REACHED"
                                                              and i["box"]["net"]["dns"] != "RESOLVED" for i in items),
        "c_verifier_box_cannot_reach_host_listener": bool(items) and all(i["box"]["net"]["host_listener"] != "REACHED" for i in items),
        "c_verifier_box_cannot_reach_the_lab": bool(items) and all(not i["box"]["net"]["lab"].startswith("HTTP ") for i in items),
        "c_host_listener_saw_no_box": hits_after_probe == control_hits and len(hits) == control_hits,
        # (d)
        "d_every_hostile_rollout_is_graded": all(h["graded"] and h["ok"] for h in hostile.values()),
        "d_deleted_submission_scores_K": hostile["delete"]["reward_skill_vs_O"] == 0.0 and hostile["delete"]["grade"].get("n_failed") == hostile["delete"]["grade"].get("n_items"),
        "d_empty_oversize_huge_and_broken_tar_score_K": all(hostile[m]["reward_skill_vs_O"] == 0.0 and hostile[m]["grade"].get("n_failed") == hostile[m]["grade"].get("n_items")
                                                            for m in ("empty", "oversize", "huge", "no_tar")),
        "d_control_default_collection_grades_a_deleted_submission": stock["delete"]["graded"] and stock["delete"]["reward_skill_vs_O"] == 0.0,
        "d_control_default_collection_leaves_the_others_ungraded": all(not stock[m]["graded"] for m in ("huge", "no_tar", "symlinks", "junk")),
        "d_links_are_left_out_and_the_rest_is_graded": hostile["symlinks"]["grade"].get("n_failed") == 0 and hostile["symlinks"]["submission"]["files"] == 1,
        "d_junk_in_logs_artifacts_does_not_matter": hostile["junk"]["grade"].get("n_failed") == 0,
        # (d') identity in the grader's box
        "predictor_cannot_write_request_or_runtime": bool(items) and all(i["write_request"] != "WRITABLE" and i["write_runtime"] != "WRITABLE"
                                                                         and i["write_workspace"] != "WRITABLE" for i in items),
        "one_request_in_the_box_at_a_time": bool(items) and all(i["requests_visible"] == ["item.py", "request.npz"] for i in items),
    }
    import asyncio
    import types

    import verifiers.v1 as vf
    from physim2_env import Physim2Task, Physim2TaskConfig
    from physim2_env.lab_tools import LabToolsConfig

    def refused(**kw):
        try:
            Physim2Task.toolsets(Physim2TaskConfig(tools=LabToolsConfig(**kw)))
            return False
        except ValueError:
            return True

    def setup_refused(rt):
        try:
            asyncio.run(Physim2Task.setup(types.SimpleNamespace(), None, rt))
            return False
        except vf.TaskError:
            return True
        except Exception:
            return False
    fake = lambda typ, restricted: types.SimpleNamespace(config=types.SimpleNamespace(type=typ, network_restricted=restricted), env={})  # noqa: E731
    used = {r["trace_id"] for r in runs.values() if r.get("trace_id")}
    new.update({
        "g_lab_placement_guard_refuses_colocated_url_and_sandbox": refused(colocated=True) and refused(url="http://127.0.0.1:1/mcp")
        and refused(runtime=vf.DockerConfig()) and not refused(),
        "g_setup_refuses_open_network_and_non_container": setup_refused(fake("docker", False)) and setup_refused(fake("subprocess", True)),
        "g_setup_refuses_token_like_harness_variable": not G3["graded"] and "TaskError" in G3["errors"] and G3.get("trace_id") not in labs_after,
        "g_single_use_refuses_an_instance_already_opened": not G4["graded"] and "TaskError" in G4["errors"] and G4.get("trace_id") not in labs_after,
    })
    del used
    res = {"checks_round5": checks, "n_checks_round5": len(checks), "n_reproduced": sum(v is True for v in checks.values()),
           "failed_round5": [k for k, v in checks.items() if v is False], "changed_by_design": changed,
           "checks_new": new, "n_checks_new": len(new), "n_passed_new": sum(v is True for v in new.values()),
           "failed_new": [k for k, v in new.items() if v is not True],
           "PILOT_NEVER_REUSE_AS_EXAM": True, "instance_id": iid,
           "route": "vf-eval physim2-env --env.id isolated-verifier, docker runtime, physim2-script harness, --no-push",
           "evidence": {
               "predictor_checks": P,
               "agent_reads": {("hidden" + p[len(hidden):] if p.startswith(hidden) else os.path.basename(p.rstrip("/"))):
                               (v.get("value") or v.get("kind")) for p, v in agent_reads.items()},
               "agent_uid": rep.get("uid"), "agent_visible_pids": rep.get("visible_pids"),
               "messages": {k: rep[k].get("error") for k in ("tick_cap", "bounds", "episode_cap_whole_block", "tick_budget",
                                                            "reset_after_submit", "submit_outside_workspace", "network") if k in rep},
               "validation_messages": {k: str(val(k).get("error"))[-160:] for k in ("submit_missing", "submit_symlink", "validate_bad_shape",
                                                                                     "validate_nondeterministic", "validate_oversize")},
               "slow": {k: val("validate_slow").get(k) for k in ("cpu_s", "wall_s")}, "slow_error": str(val("validate_slow").get("error"))[:60],
               "memory": str(val("validate_memory").get("error"))[-120:], "usage_end": rep.get("usage_end"),
               "probe_agent_grade": {k: gA.get(k) for k in ("n_items", "n_failed", "layers")},
               "a_first_item": {k: items[0][k] for k in ("found_files", "daemon_alive", "found_shm", "other_processes_of_my_user")} if items else None,
               "a_cleanup_per_item": cl, "a_control_item_2": {k: items0[1][k] for k in ("found_files", "daemon_alive", "found_shm", "other_processes_of_my_user")} if len(items0) > 1 else None,
               "a_control_marked_not_an_exam": B0["info"].get("NOT_AN_EXAM"),
               "b_lab_process": dict(lab_proc, scrubbed_variables={"count": len(lab_proc.get("scrubbed_variables", [])),
                                                                 "includes_HF_TOKEN": "HF_TOKEN" in lab_proc.get("scrubbed_variables", []),
                                                                 "note": "names withheld: they describe the worker's own environment"}), "b_agent_box": {k: ab[k] for k in ("uid", "env_names", "env_token_like", "env_needle", "needle_hits", "files_read", "environ_read")},
               "b_verifier_box_item_1": {k: items[0]["box"][k] for k in ("uid", "env_token_like", "env_needle", "needle_hits", "files_read", "environ_read")} if items else None,
               "b_trace_scan": {"files_scanned": scanned, "needles": sorted(needles), "found": found},
               "c_control": control, "c_agent_box_net": ab["net"], "c_verifier_box_net_all_items": vb_net,
               "c_listener_hits": {"control": control_hits, "during_box_runs": len(hits) - control_hits},
               "d_hostile": {m: {"graded": h["graded"], "ok": h["ok"], "reward": h["reward_skill_vs_O"], "errors": h["errors"],
                                 "n_failed": h["grade"].get("n_failed"), "n_items": h["grade"].get("n_items"), "reason": h["grade"].get("reason"),
                                 "submission": h["submission"]} for m, h in hostile.items()},
               "d_control_default_collection": {m: {"graded": h["graded"], "trace_ok": h["ok"], "episode_ok": h.get("episode_ok"), "trace_errors": h["errors"],
                                                    "episode_errors": h.get("episode_errors"), "reward_recorded_as": h["reward_skill_vs_O"],
                                                    "marked": h["info"].get("NOT_AN_EXAM")} for m, h in stock.items()},
               "g_guard_runs": {k: {"graded": v["graded"], "trace_ok": v["ok"], "trace_errors": v["errors"]} for k, v in (("token_env", G3), ("single_use", G4))},
               "verifier_box_identity_item_1": {k: items[0][k] for k in ("write_submission", "write_request", "write_runtime", "write_workspace", "requests_visible")} if items else None,
               "verifier_box_staging": B["verifier_box"],
           },
           "rollouts": {k: {"graded": v["graded"], "ok": v["ok"], "reward": v["reward_skill_vs_O"], "wall_s": v["wall_s"], "cpu_s": v["cpu_s"],
                            "invocation_wall_s": v["invocation_wall_s"], "address_file_matches_tool_url": v["address_file_matches_tool_url"]}
                        for k, v in runs.items()},
           "wall_s": time.time() - t0}
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    json.dump(res, open(a.out, "w"), indent=1)
    print(json.dumps({k: res[k] for k in ("n_checks_round5", "n_reproduced", "failed_round5", "n_checks_new", "n_passed_new", "failed_new")}))


if __name__ == "__main__":
    main()
