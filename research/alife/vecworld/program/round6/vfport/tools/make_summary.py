"""make_summary -- results/summary.json: every number of this study with the file and key it comes from.

Reads results/proof_ring.json and results/probe_ring.json (this study), round 5's agentenv/results/proof_ring.json
and probe_ring.json (the references to reproduce), counts lines, asks Docker for the image sizes.
usage: python tools/make_summary.py
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


def main():
    ours = json.load(open(os.path.join(ROOT, "results", "proof_ring.json")))
    ref = json.load(open(os.path.join(AE, "results", "proof_ring.json")))
    probe = json.load(open(os.path.join(ROOT, "results", "probe_ring.json")))
    probe5 = json.load(open(os.path.join(AE, "results", "probe_ring.json")))
    S = {"study": "program/round6/vfport: the PhySim v2 exam as a verifiers environment", "written_unix": time.time(),
         "PILOT_NEVER_REUSE_AS_EXAM": True,
         "what_was_run": "everything below was RUN in the cloud container (Linux x86_64, 4 cores, Docker) with scripted agents: no model "
                         "call, no GPU, no upload (--no-push equivalent: push = false, PRIME_RUNS_MODE=disabled, PRIME_API_KEY removed). "
                         "Nothing was run on a Mac.",
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
                                        "control_verifiers_default_collection": ev.get("d_control_default_collection")}}

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
        "memo_estimates": {"drop": 760, "wrap": 530, "keep": 2370, "new_including_sealer": 750, "scripted_harness": 60}}

    # ---- images ----
    out = subprocess.run(["docker", "images", "--format", "{{.Repository}}:{{.Tag}} {{.Size}}"], capture_output=True, text=True).stdout.split("\n")
    df = subprocess.run(["docker", "system", "df", "--format", "{{.Type}} {{.Size}}"], capture_output=True, text=True).stdout.split("\n")
    S["docker"] = {"images": [x for x in out if x], "system_df": [x for x in df if x], "source": "docker images / docker system df at summary time",
                   "server": ours["platform"].get("docker"), "note": "classic image store (dockerd --feature containerd-snapshotter=false)"}
    json.dump(S, open(os.path.join(ROOT, "results", "summary.json"), "w"), indent=1)
    print(json.dumps({p: {k: (round(v[k], 3) if isinstance(v[k], float) else v[k]) for k in ("ours_vs_C", "round5_vs_C", "z")} for p, v in tab.items()}))
    print(json.dumps(S["ring_table"]["acceptance"]))
    print(json.dumps({"identical": S["ring_table"]["same_submission_through_round5_grader"]["all_identical"],
                      "new_lines": S["code"]["new"]["totals"], "dropped": S["code"]["dropped_from_the_route"]["total"],
                      "wrapped": S["code"]["wrapped"]["total"], "kept": S["code"]["kept_by_import"]["lines"]}))


if __name__ == "__main__":
    main()
