"""make_summary -- results/summary.json: every number of this study with the file and key it comes from.

Reads results/proof_ring.json, probe_ring.json, units.json, units_before_fix.json, driver_container.json and
recomputed_table.json (this study), round 5's agentenv/results/proof_ring.json and probe_ring.json (the references
to reproduce), the red team's results, counts lines, asks Docker for the image sizes.
usage: python tools/make_summary.py [--store DIR --scratch DIR]    (with the store: scan for hidden values)
"""
import json
import os
import subprocess
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)
from physim2_env._paths import agentenv_root  # noqa: E402

AE = agentenv_root()
R5 = "round5/agentenv/results/"
POLS = ["S", "D", "P0", "PM", "C", "null", "O"]


def lines(path, lo=None, hi=None):
    n = sum(1 for _ in open(path))
    return n if lo is None else min(hi, n) - lo + 1


def count(files):
    return {os.path.relpath(f, ROOT): lines(f) for f in files}


def per_world(proof, pol):
    return [w["table"]["policies"][pol]["vs_C"] for w in proof["per_world"] if pol in w["table"]["policies"]]


def scan_for_hidden(store, scratch):
    """While the pilot's store still exists: do the committed results or any file the runs saved (traces, configs,
    logs, the scripts' notes) contain a secret or a hidden parameter of any instance? Returns counts only."""
    needles = {}
    for iid in sorted(os.listdir(store)):
        f = os.path.join(store, iid, "hidden", "instance.json")
        if os.path.isfile(f):
            inst = json.load(open(f))
            needles[f"{iid}:secret"] = inst["secret_hex"]
            for n, v in zip(inst["theta_names"], inst["theta"]):
                needles[f"{iid}:{n}"] = repr(float(v))[:10]
    files = [os.path.join(ROOT, "results", f) for f in os.listdir(os.path.join(ROOT, "results"))]
    for root, _, fs in os.walk(scratch):
        if os.path.abspath(root).startswith(os.path.abspath(store)):
            continue
        files += [os.path.join(root, f) for f in fs]
    hits = 0
    for f in files:
        raw = open(f, "rb").read()
        hits += sum(v.encode() in raw for v in needles.values())
    return {"instances": len([k for k in needles if k.endswith(":secret")]), "needles": len(needles),
            "what": "the 64-hex secret and the first 10 characters of every hidden parameter of every instance in the store",
            "files_scanned": len(files), "hits": hits,
            "where": "results/*.json and every file under the runs' scratch directories (traces.jsonl, configs, logs, notes)"}


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--store", default=None)
    ap.add_argument("--scratch", default=None)
    a = ap.parse_args()
    ours = json.load(open(os.path.join(ROOT, "results", "proof_ring.json")))
    ref = json.load(open(os.path.join(AE, "results", "proof_ring.json")))
    probe = json.load(open(os.path.join(ROOT, "results", "probe_ring.json")))
    probe5 = json.load(open(os.path.join(AE, "results", "probe_ring.json")))
    R = lambda f: json.load(open(os.path.join(ROOT, "results", f))) if os.path.exists(os.path.join(ROOT, "results", f)) else None  # noqa: E731
    pkg_commit = subprocess.run(["git", "log", "-1", "--format=%h", "--", "physim2_env", "physim2_script"], cwd=ROOT, capture_output=True,
                                text=True).stdout.strip()
    dirty = subprocess.run(["git", "status", "--porcelain", "--", "physim2_env", "physim2_script"], cwd=ROOT, capture_output=True,
                           text=True).stdout.strip()
    S = {"study": "program/round6/vfport: the PhySim v2 exam as a verifiers environment (after the fixes to the two reviews and round 1 "
                  "of the fixes to the host-safety audit)",
         "written_unix": time.time(), "PILOT_NEVER_REUSE_AS_EXAM": True,
         "what_was_run": "everything below was RUN in the cloud container (Linux x86_64, 4 cores, Docker) with scripted agents: no model "
                         "call, no GPU, no upload (--no-push equivalent: push = false, PRIME_RUNS_MODE=disabled, PRIME_API_KEY removed). "
                         "Nothing was run on a Mac. Which result file ran on which code: code_versions.",
         "code_versions": {"package (physim2_env, physim2_script) now": f"commit {pkg_commit}" + (" PLUS UNCOMMITTED CHANGES" if dirty else "")
                           + " (after round 1 of the host-safety fixes; pinned by PIN.sha256)",
                           "run on the package as it is now": "results/probe_ring.json (37 rollouts), units.json, driver_container.json, "
                           "safety_host.json, safety_interrupt.json, safety_runbook.json, rehearsal_round1.json (one world of the proof with the "
                           "Mac's arguments, the probes, one direct vf-eval rollout)",
                           "NOT run again after the host-safety fixes (package code of commit 743f6b75e)": "results/proof_ring.json and "
                           "proof_ring_items.npz (the 4-world table, cost per rollout, one box per item), recomputed_table.json, "
                           "gliders_smoke_D.json, units_before_fix.json, redteam/results/*. The driver, the staging and the worker gate changed "
                           "since; the arithmetic of scoring did not",
                           "builder's results": "replaced; the builder's numbers are in the history of this file (commit e4a30854d)"},
         "sources": {"ours_table": "results/proof_ring.json", "round5_table": R5 + "proof_ring.json",
                     "ours_probe": "results/probe_ring.json", "round5_probe": R5 + "probe_ring.json"}}

    # ---- the ring table ----
    tab = {}
    for pol in POLS:
        a_, b_ = ours["pooled"]["policies"].get(pol), ref["pooled"]["policies"].get(pol)
        if not a_ or not b_:
            continue
        xa, xb = np.array(per_world(ours, pol)), np.array(per_world(ref, pol))
        se = float(np.sqrt(xa.var(ddof=1) / len(xa) + xb.var(ddof=1) / len(xb))) if len(xa) > 1 and len(xb) > 1 else None
        tab[pol] = {"ours_vs_C": a_["vs_C"], "round5_vs_C": b_["vs_C"], "ours_L": a_["L"], "round5_L": b_["L"],
                    "ours_per_world_vs_C": xa.tolist(), "round5_per_world_vs_C": xb.tolist(),
                    "difference_of_world_means": float(xa.mean() - xb.mean()), "se_of_that_difference": se,
                    "z": None if not se else float((xa.mean() - xb.mean()) / se)}
    acc_a, acc_b = ours["pooled"].get("acceptance", {}), ref["pooled"].get("acceptance", {})
    zs = [abs(v["z"]) for v in tab.values() if v["z"] is not None]
    xs = [w.get("same_submission_through_round5_grader") for w in ours["per_world"]]
    S["ring_table"] = {
        "source_keys": "pooled.policies[policy].vs_C and .L; per_world[w].table.policies[policy].vs_C; pooled.acceptance",
        "size": {"n_worlds": ours["n_worlds"], "n_items": ours["pooled"]["n_items"], "sizes": ours["sizes"],
                 "round5_n_worlds": ref["n_worlds"], "round5_n_items": ref["pooled"]["n_items"], "round5_sizes": ref["sizes"]},
        "policies": tab,
        "acceptance": {k: {"ours": acc_a.get(k), "round5": acc_b.get(k)} for k in ("sigma", "rho", "null_is", "sigma_worlds", "rho_worlds")},
        "all_rollouts_graded": ours["all_graded"], "failed_items_total": ours["n_failed_items_total"],
        "max_abs_z_over_policies": max(zs) if zs else None,
        "verdict": "NOT identical numbers, and they cannot be: both runs draw fresh secrets and hidden parameters (os.urandom), and round 5 "
                   "deleted its instances. The comparison is between two samples of 4 hidden worlds; z is the difference of the "
                   "world means over its standard error. The arithmetic itself is identical: see same_submission_through_round5_grader.",
        "same_submission_through_round5_grader": {
            "source_key": "per_world[w].same_submission_through_round5_grader",
            "what": "the frozen C submission of each world graded twice: by round 5's evaluator.grader.grade in agentenv's local "
                    "sandbox on the worker, and by this study's reward in the verifier box; per-item, per-cell scores compared",
            "per_world": xs, "all_identical": all(bool(x and x.get("identical")) for x in xs)}}

    d = [abs(r["reward_skill_vs_O"] - w["table"]["policies"][p]["vs_O"]) for w in ours["per_world"] for p, r in w["rollouts"].items()]
    S["ring_table"]["reward_equals_table"] = {"what": "trace reward (rewards.skill) against per_world[w].table.policies[p].vs_O, 24 rollouts",
                                              "max_abs_difference": float(max(d))}
    S["ring_table"]["grading_mode"] = ours.get("grading_mode")
    S["ring_table"]["recomputed_from_per_item_scores"] = dict(R("recomputed_table.json") or {}, what="tools/recompute_table.py: numpy only, from "
                                                              "results/proof_ring_items.npz, no store, no vw library") or None
    S["one_box_per_item"] = {"source_key": "results/proof_ring.json:one_box_per_item_check_world_0",
                             "what": "the taskset's default grading mode (a fresh container per exam item, provisioned through verifiers) on the "
                                     "first world: the same frozen submission must get the same per-item scores as with all items in one box",
                             "checks": ours.get("one_box_per_item_check_world_0")}
    S["failed_item_is_K_counterfactual"] = dict(ours.get("failed_item_is_K_counterfactual") or {}, source_key="results/proof_ring.json:failed_item_is_K_counterfactual")
    old = os.path.join(ROOT, "results", "summary.json")
    prev_all = json.load(open(old)) if os.path.exists(old) else {}
    prev = prev_all.get("hidden_value_scan")
    S["hidden_value_scan"] = scan_for_hidden(a.store, a.scratch) if a.store and a.scratch else prev
    if a.store and a.scratch and prev and prev != S["hidden_value_scan"]:      # a new scan does not erase what an earlier one covered
        S["hidden_value_scan_of_earlier_runs"] = dict({k: v for k, v in prev.items() if k != "earlier"},
                                                      note="made while the store of those runs still existed; that store is deleted")
    elif prev_all.get("hidden_value_scan_of_earlier_runs"):
        S["hidden_value_scan_of_earlier_runs"] = prev_all["hidden_value_scan_of_earlier_runs"]
    if prev_all.get("checker") or prev_all.get("checker_of_the_builders_version"):
        S["checker_of_the_builders_version"] = prev_all.get("checker") or prev_all.get("checker_of_the_builders_version")

    # ---- boundary checks and probes ----
    ev = probe["evidence"]
    S["boundary_checks"] = {
        "source_keys": "checks_round5, changed_by_design, checks_new, evidence",
        "round5": {"n_checks": probe5["n_checks"], "n_passed": probe5["n_passed"]},
        "ours_on_the_same_34": {"reproduced": probe["n_reproduced"], "failed": probe["failed_round5"],
                                "changed_by_design": probe["changed_by_design"]},
        "new_checks": {"n": probe["n_checks_new"], "passed": probe["n_passed_new"], "failed": probe["failed_new"], "all": probe["checks_new"]},
        "probe_a_persistence": {"with_cleanup_first_item": ev["a_first_item"], "cleanup_per_item": ev["a_cleanup_per_item"],
                                "control_without_cleanup_item_2": ev["a_control_item_2"]},
        "probe_b_canary": {"lab_process": ev["b_lab_process"], "agent_box": {k: ev["b_agent_box"][k] for k in ("env_token_like", "env_needle", "needle_hits", "files_read")},
                           "verifier_box_item_1": ev["b_verifier_box_item_1"], "saved_files_scan": ev["b_trace_scan"]},
        "probe_c_network": {"control_uncut_container": ev["c_control"], "agent_box": ev["c_agent_box_net"],
                            "verifier_box_all_items": ev["c_verifier_box_net_all_items"], "host_listener_hits": ev["c_listener_hits"]},
        "probe_d_no_ungraded_rollout": {"defensive_collection": {m: {k: h[k] for k in ("graded", "reward", "n_failed", "n_items", "reason")} for m, h in ev["d_hostile"].items()},
                                        "control_verifiers_default_collection": ev.get("d_control_default_collection")},
        "probe_a2_state_of_a_box": {"one_box_per_item": ev.get("a2_channels_one_box_per_item"), "all_items_in_one_box": ev.get("a2_channels_all_items_in_one_box"),
                                    "grade": ev.get("a2_grade")},
        "probe_e_trusted_validation": ev.get("e_reports"),
        "probe_f_replies": {"grades": ev.get("f_grades"), "first_error": ev.get("f_first_error")},
        "probe_h_harness_dies": ev.get("h_harness_dies")}
    # ---- the offline checks and the host-safety checks ----
    u, ub, dc = R("units.json"), R("units_before_fix.json"), R("driver_container.json")
    S["unit_checks"] = {"source": "results/units.json (fixed code), results/units_before_fix.json (the builder's code, the same script)",
                        "fixed": None if not u else {k: u[k] for k in ("n_checks", "n_passed", "failed")},
                        "builders_code": None if not ub else {k: ub[k] for k in ("n_checks", "n_passed", "failed")}}
    S["host_safety"] = {
        "incident": {
            "when": "10 Nov 2026, about 04:31 to 04:34 UTC, in the cloud container",
            "what_ran": "the first version of tools/check_units.py started physim2_env/public/_item.py (the one-request driver) as root ON THE HOST, "
                        "outside any container, 14 times (7 test predictors, against the fixed and against the builder's package)",
            "what_it_did": "the driver's cleanup did on the host what it does in a box: SIGKILL to every process of uid 1000 and deletion of every "
                           "file owned by uid 1000 on the writable file systems (/ and /var/lib/docker)",
            "known_loss": "/home/ubuntu, the home directory of the unused default account (recreated from /etc/skel; its earlier content is "
                          "not known). The coordinator found no tracked file missing in the checkouts and worktrees; the Python environments "
                          "import; the three Docker images run. Sessions here run as root and own their files as root.",
            "cause": "the driver decided to drop privileges and to clean up from `euid == 0` alone; nothing told it that it was not in a box",
            "reported": "to the coordinator's channel at 04:34:53 UTC"},
        "first_fix": "commit 7e034be18: a box guard of four conditions in the driver (marker, sign of a container, route variable, the box's "
                     "own uid), require_container(runtime) by the runtime's type string, tests under 12 tripwires and in a throwaway container",
        "audit": {"file": "HOST_SAFETY_AUDIT.md", "verdict": "NO-GO for the Mac (10 Nov 2026): five major findings (A1 to A5), fifteen minor ones, "
                  "nine required changes, two hardening items"},
        "round_1_of_fixes": {
            "source": "results/host_safety_round1.json (one entry per required change: what changed, the audit's test, its result)",
            "driver": "physim2_env/public/_item.py: the guard now needs ALL of: a root caller; the marker /etc/physim2/predictor_uid (root-owned); a "
                      "sign of a container; PHYSIM2_BOX_CLEANUP=disposable-box; a target uid equal to the marker's and inside 20000-59999; and a "
                      "mount table that holds nothing but an overlay root, kernel file systems at or below /proc, /sys and /dev, and Docker's "
                      "three /etc files (an unreadable table refuses; no fallback to /). The wipe unlinks and rmdirs listed paths only (no "
                      "rmtree, never a mount point). The identity is verified after the set-id calls and before kill(-1). --uid has no "
                      "default. Outside a box nothing runs unless --no-box is given",
            "worker": "physim2_env/grading.py: container_gate accepts only verifiers' own DockerRuntime or PrimeRuntime object, not borrowed, "
                      "with a container name verifiers generated; physim2_script uses the same gate",
            "box_scripts": "agents/hostile_submission.py, agents/probe_grading.py, redteam/agent_rt.py exit at their first statement outside an "
                           "exam box, and ask again before each kill -9 -1",
            "tools": "tools/vfrun.py: VF_RUN_ID required (container label), SIGTERM before SIGKILL, Docker must answer; tools/check_units.py never "
                     "starts the driver as root; red-team tools delete nothing they did not make",
            "runbook": "RUNBOOK_MAC.md rewritten and pinned (PIN.sha256); ON HOLD until a re-audit",
            "summary": None if not R("host_safety_round1.json") else {k: R("host_safety_round1.json")[k] for k in ("status", "all_named_tests_pass")}},
        "tests_on_the_host": None if not u else {
            "source": "results/units.json: checks guard_*, evidence.guard_pure, .guard_on_this_machine, .guard_tripwires; results/safety_host.json",
            "checks": {k: v for k, v in u["checks"].items() if k.startswith("guard_")},
            "this_machine": u["evidence"].get("guard_on_this_machine"),
            "how": "tools/tripwires.py replaces 65 primitives of os, shutil, subprocess and pathlib (kill, unlink, rmdir, rename, chmod, chown, "
                   "set*id, fork, exec, rmtree, subprocess.run and Popen, ...) by recorders that raise, BEFORE the driver's file is imported; every "
                   "killing or deleting function is then called with the route variable set and must refuse",
            "driver_as_a_program_on_this_host": u["evidence"].get("driver_host_guard"),
            "safety_host": None if not R("safety_host.json") else {k: R("safety_host.json")[k] for k in ("tripwires_installed", "n_checks", "n_passed", "failed")},
            "the_builders_code_under_the_first_fixers_tripwires": None if not ub else ub["evidence"].get("guard_tripwires")},
        "tests_in_a_throwaway_container": None if not dc else {"source": "results/driver_container.json", "where": dc["where"],
                                                              "n_checks": dc["n_checks"], "n_passed": dc["n_passed"], "failed": dc["failed"],
                                                              "checks": dc["checks"]},
        "interruption": None if not R("safety_interrupt.json") else {k: R("safety_interrupt.json")[k] for k in ("n_checks", "n_passed", "failed", "checks")},
        "runbook": None if not R("safety_runbook.json") else {k: R("safety_runbook.json")[k] for k in ("copy", "n_checks", "n_passed", "failed")},
        "rehearsal": None if not R("rehearsal_round1.json") else {k: R("rehearsal_round1.json").get(k) for k in ("outcome", "commit_rehearsed", "where")}}
    # ---- the red team's attacks, run again through the route after the fixes ----
    rt = {}
    for nm in ("overflow", "fifo", "hostile-exit1"):
        f = os.path.join(ROOT, "redteam", "results", f"{nm}-after-fix.json")
        if os.path.exists(f):
            x = json.load(open(f))
            ro = x.get("rollout", {})
            rt[nm] = {"source": f"redteam/results/{nm}-after-fix.json", "wall_s": x.get("wall_s"), "graded": ro.get("graded"),
                      "reward_raw_in_trace": ro.get("reward_raw_in_trace"), "errors": ro.get("errors"),
                      "grade": {k: (ro.get("grade") or {}).get(k) for k in ("n_items", "n_failed", "reason", "skill_vs_O")},
                      "before_the_fix": f"redteam/results/{nm}.json"}
    S["red_team_attacks_after_the_fix"] = rt or None

    # ---- gliders: loadable, one rollout ----
    gf = os.path.join(ROOT, "results", "gliders_smoke_D.json")
    if os.path.exists(gf):
        g = json.load(open(gf))
        r = g["per_world"][0]["rollouts"]["D"]
        S["gliders_smoke"] = {
            "source": "results/gliders_smoke_D.json", "what": "ONE hidden gliders world (config smoke_gliders: 8 items, R 6, 132 lab ticks) and ONE "
            "scripted rollout (policy D) through the same route and the same image; a loadability check, not a measurement",
            "graded": r["graded"], "n_failed_items": r["grade"]["n_failed"], "n_items": r["grade"]["n_items"],
            "reward_skill_vs_O": r["reward_skill_vs_O"], "lab_ticks_used": r["lab_ticks_used"], "lab_episodes": r["lab_episodes"],
            "wall_s": r["wall_s"], "cpu_s": r["cpu_s"], "predictor_layers": r["grade"]["layers"],
            "whole_run_wall_s_including_instance_build": g["wall_s"]}

    # ---- cost ----
    S["cost_per_rollout"] = dict(ours["rollout_cost"], source_key="results/proof_ring.json:rollout_cost",
                                 round5_wall_s_whole_proof=ref["wall_s"], ours_wall_s_whole_proof=ours["wall_s"],
                                 probe_rollouts={k: {"wall_s_total": v["wall_s"].get("total"), "invocation_wall_s": v["invocation_wall_s"]}
                                                 for k, v in probe["rollouts"].items()})

    # ---- code ----
    ae = lambda *p: os.path.join(AE, *p)  # noqa: E731
    dropped = {"evaluator/sandbox.py": lines(ae("evaluator", "sandbox.py")), "run_rollout.py": lines(ae("run_rollout.py")),
               "evaluator/lab_service.py:230-295 (socket server)": 66, "physim2/wire.py": lines(ae("physim2", "wire.py")),
               "physim2/labclient.py": lines(ae("physim2", "labclient.py")), "mac/ (compose, Dockerfiles)": lines(ae("mac", "Dockerfile"))
               + lines(ae("mac", "Dockerfile.agent")) + lines(ae("mac", "compose.yaml")), "tests_tcp.py": lines(ae("tests_tcp.py")),
               "evaluator/submission.py:27-91 (snapshot, run_request)": 65}
    wrapped = {"evaluator/lab_service.py:43-227 (LabService)": 185, "evaluator/build_workspace.py": lines(ae("evaluator", "build_workspace.py")),
               "evaluator/grader.py:34-64 (grading loop)": 31, "prove.py": lines(ae("prove.py")), "check_probe.py": lines(ae("check_probe.py"))}
    total = int(subprocess.run("git ls-files . ':!results' | xargs cat | wc -l", shell=True, cwd=AE, capture_output=True, text=True).stdout or 0)
    pkg = sorted(os.path.join(ROOT, d, f) for d in ("physim2_env", os.path.join("physim2_env", "public"), "physim2_script")
                 for f in os.listdir(os.path.join(ROOT, d)) if f.endswith(".py"))
    S["boundary_checks"]["grading_mode_of_the_probes"] = "the taskset's default: one fresh box per exam item (probe-grading-shared and the cleanup-off control: one box)"
    tools = sorted(os.path.join(ROOT, "tools", f) for f in os.listdir(os.path.join(ROOT, "tools")) if f.endswith(".py")) \
        + [os.path.join(ROOT, "tools", "docker_shim", "docker")]
    agents = sorted(os.path.join(ROOT, "agents", f) for f in os.listdir(os.path.join(ROOT, "agents")) if f.endswith(".py"))
    other = [os.path.join(ROOT, "docker", "Dockerfile.ring"), os.path.join(ROOT, "docker", "Dockerfile.network"),
             os.path.join(ROOT, "configs", "scripted_ring.toml"), os.path.join(ROOT, "configs", "qwen_ring_bash.toml"),
             os.path.join(ROOT, "pyproject.toml")]
    new = {"package": count(pkg), "tools": count(tools), "agents": count(agents), "build_and_config": count(other)}
    S["code"] = {
        "agentenv_total_lines_tracked": total,
        "dropped_from_the_route": dict(dropped, total=sum(dropped.values()),
                                       note="not on the route any more; the files stay in round 5 untouched. evaluator/sandbox.py and "
                                            "submission.run_request are still used once, as the reference grader of the cross-check"),
        "wrapped": dict(wrapped, total=sum(wrapped.values())),
        "kept_by_import": {"lines": total - sum(dropped.values()) - sum(wrapped.values()),
                           "copied_verbatim": "32 lines (evaluator/submission.py:94-125) into physim2_env/public/validate.py; nothing else is copied"},
        "new": dict(new, totals={k: sum(v.values()) for k, v in new.items()}, total=sum(sum(v.values()) for v in new.values())),
        "memo_estimates": {"drop": 760, "wrap": 530, "keep": 2370, "new_including_sealer": 750, "scripted_harness": 60},
        "red_team_scripts_not_counted": "redteam/ (the red team's attack scripts; after the host-safety audit agent_rt.py got a box gate and "
                                        "rt_run.py and nproc_cross_box.sh stopped deleting paths and container names they did not make)"}

    # ---- images ----
    out = subprocess.run(["docker", "images", "--format", "{{.Repository}}:{{.Tag}} {{.Size}}"], capture_output=True, text=True).stdout.split("\n")
    df = subprocess.run(["docker", "system", "df", "--format", "{{.Type}} {{.Size}}"], capture_output=True, text=True).stdout.split("\n")
    S["docker"] = {"images": [x for x in out if x], "system_df": [x for x in df if x], "source": "docker images / docker system df at summary time",
                   "server": ours["platform"].get("docker"), "note": "classic image store (dockerd --feature containerd-snapshotter=false)"}
    if "gliders_smoke" in S:
        S["gliders_smoke"]["code"] = (R("gliders_smoke_D.json") or {}).get("grading_mode") and "fixed code" or "the builder's code (not run again after the fixes)"
    json.dump(S, open(os.path.join(ROOT, "results", "summary.json"), "w"), indent=1)
    print(json.dumps({p: {k: (round(v[k], 3) if isinstance(v[k], float) else v[k]) for k in ("ours_vs_C", "round5_vs_C", "z")} for p, v in tab.items()}))
    print(json.dumps(S["ring_table"]["acceptance"]))
    print(json.dumps({"identical": S["ring_table"]["same_submission_through_round5_grader"]["all_identical"],
                      "new_lines": S["code"]["new"]["totals"], "dropped": S["code"]["dropped_from_the_route"]["total"],
                      "wrapped": S["code"]["wrapped"]["total"], "kept": S["code"]["kept_by_import"]["lines"]}))


if __name__ == "__main__":
    main()
