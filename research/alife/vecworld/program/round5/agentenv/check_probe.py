"""check_probe -- run agents/probe_agent.py on a fresh ring instance and check what the boundary did.

usage: python check_probe.py --scratch DIR --out results/probe_ring.json
Every check is a named boolean with the evidence next to it; the output holds no hidden value.
"""
import argparse
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import run_rollout as RR  # noqa: E402
from evaluator import sandbox  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scratch", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    run = os.path.join(a.scratch, "probe")
    RR.prepare("ring", json.load(open(os.path.join(HERE, "configs", "probe_ring.json"))), run)
    hidden = os.path.join(run, "hidden")
    probes = [hidden, os.path.join(hidden, "instance.json"), os.path.join(hidden, "exam.npz"), HERE,
              os.path.join(run, "public")]
    out = RR.rollout(run, "probe", ["{python}", "-B", "{agent_home}/probe_agent.py"],
                     env={"PHYSIM2_PROBE_PATHS": ":".join(probes)}, wall_seconds=600)
    rep = json.load(open(os.path.join(run, "workspaces", "probe", "probe_report.json")))
    caps = sandbox.caps()

    def rejected(name, kind=None, text=None):
        r = rep.get(name, {})
        return bool(r and not r["ok"] and (kind is None or r.get("kind") == kind) and (text is None or text in r.get("error", "")))

    def val(name):
        return rep.get(name, {}).get("value") or {}
    leak = val("validate_leak")
    leak_txt = leak.get("error", "") if isinstance(leak, dict) else ""
    leak_obj = json.loads(leak_txt[leak_txt.index("PROBE") + 5:leak_txt.rindex("}") + 1]) if "PROBE" in leak_txt else {}
    hid = [p for p in probes if p.startswith(hidden)]

    def unreadable(v):
        return v in ("FileNotFoundError", "PermissionError", "NotADirectoryError") or v == []
    agent_reads = {p: rep.get(f"read:{p}", {}) for p in probes}
    checks = {
        "agent_runs_unprivileged": rep.get("uid") == 65534 if caps["setpriv"] else None,
        "agent_cannot_read_hidden": all((not agent_reads[p].get("ok")) or agent_reads[p]["value"] == {"listing": []} for p in hid),
        "agent_cannot_read_evaluator_code": (not agent_reads[HERE].get("ok")) or agent_reads[HERE]["value"] == {"listing": []},
        "agent_sees_only_its_own_processes": rep.get("visible_pids", 99) <= 3 if caps.get("pid_namespace") else None,
        "agent_has_no_network": rejected("network"),
        "agent_cannot_write_outside_workspace": rejected("write_outside_workspace"),
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
        "predictor_runs_unprivileged": leak_obj.get("uid") == 65534 if caps["setpriv"] else None,
        "predictor_cannot_read_hidden": bool(leak_obj) and all(unreadable(leak_obj.get(p)) for p in hid),
        "predictor_has_no_network": leak_obj.get("net") not in (None, "REACHABLE") if caps["namespaces"] else None,
        "predictor_cannot_write_submission": leak_obj.get("write_submission") not in (None, "WRITABLE"),
        "good_submission_validates": val("validate_good").get("ok") is True,
        "submit_freezes": val("submit_good").get("accepted") is True,
        "lab_closed_after_submit": rejected("reset_after_submit", "closed"),
        "graded_without_failures": bool(out["grade"]) and out["grade"]["n_failed"] == 0,
    }
    # a predictor that fails at grading time is scored as K, item by item
    S = np.load(os.path.join(hidden, "grades", "probe.npz"))
    res = {"checks": checks, "n_checks": sum(v is not None for v in checks.values()),
           "n_passed": sum(v is True for v in checks.values()), "failed": [k for k, v in checks.items() if v is False],
           "skipped_no_capability": [k for k, v in checks.items() if v is None],
           "sandbox_capabilities": caps, "agent_layers": out["agent"]["layers"], "predictor_layers": out["grade"]["layers"],
           "evidence": {"predictor_probe": {k: (v if not k.startswith("/") else str(v)) for k, v in leak_obj.items()},
                        "agent_reads": {("hidden" + p[len(hidden):] if p.startswith(hidden) else p): (v.get("value") or v.get("kind"))
                                        for p, v in agent_reads.items()},
                        "messages": {k: rep[k].get("error") for k in ("tick_cap", "bounds", "episode_cap_whole_block", "tick_budget",
                                                                     "reset_after_submit", "submit_outside_workspace") if k in rep},
                        "slow": {k: val("validate_slow").get(k) for k in ("error", "cpu_s", "wall_s")},
                        "memory": str(val("validate_memory").get("error"))[-200:],
                        "usage_end": rep.get("usage_end"), "graded_items": int(len(S["es"]))}}
    for k in list(res["evidence"]["predictor_probe"]):
        if k.startswith(hidden):
            res["evidence"]["predictor_probe"]["hidden" + k[len(hidden):]] = res["evidence"]["predictor_probe"].pop(k)
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    json.dump(res, open(a.out, "w"), indent=1)
    print(json.dumps({k: res[k] for k in ("n_checks", "n_passed", "failed", "skipped_no_capability")}))


if __name__ == "__main__":
    main()
