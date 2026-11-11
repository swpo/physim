"""make_round4_step3 -- assemble results/round4_step3.json from the outputs of the round-4 checks of step 3.

    python -B tools/make_round4_step3.py --host FILE --caps FILE --route FILE [--first-route FILE] --runbook FILE
        [--issued FILE] [--probe FILE] --out results/round4_step3.json

A development tool for the cloud container (on the never-list of RUNBOOK_MAC.md with the other check tools). It
reads JSON files that the check tools wrote, replaces machine paths by words, searches everything for the VALUES
of the credentials in this process's environment (names and counts only are printed), and writes one file. It
starts nothing.
"""
import argparse
import base64
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CRED = ("PRIME_API_KEY", "HF_TOKEN", "WANDB_API_KEY", "PRIME_TEAM_ID")

CONDITIONS = {
    "1 a reply with missing or partial usage, a stream without a final usage chunk, an error reply: ONE worst-case call, never zero":
        ["C6", "C16", "C25", "C26", "C27", "C29", "C30", "D23"],
    "2 every HTTP attempt counts, retries included (verifiers' client does not retry: clients/base.py:14-16; the run's config allows no retry; a retry of the harness is a new, counted request)":
        ["C22", "C27", "D4"],
    "3 cache reads at the full input price unless the saved model entry lists a cache-read price (and prompt tokens at a listed cache-write price where that is higher)":
        ["C3", "C4", "D15b"],
    "4 counter and stop live in the host-side process only; one counted client; no model call without a meter, for another rollout or on another route":
        ["C13", "C14", "C36", "C37", "C38", "C39", "R12"],
    "5 prices and context window from the provider's listing at run start, written into the run's record (model_entry.json)":
        ["D13", "D15", "R9", "R24"],
    "6 max_turns stays a cap of its own: always set, compared with the config by the strict schema": ["D1", "D4"],
    "7 max_context_tokens is mandatory and enforced before each call; the one-call worst case uses it": ["D2", "D13", "D15", "C8", "C9", "C10", "C11", "C17", "C34", "C35"],
    "8 acceptance rule (cap_usd >= one worst-case call), bound = cap_usd + one worst-case call, the count per call and in total in the publication folder":
        ["D15", "C31", "C32", "R11", "R13", "D30", "R25"],
}


def load(path):
    if not path:
        return None
    with open(path) as f:
        return json.load(f)


def brief(checks):
    return [{"name": c["name"], "ok": bool(c["ok"])} for c in checks or []]


def main() -> int:
    ap = argparse.ArgumentParser()
    for k in ("host", "caps", "route", "first-route", "runbook", "issued", "probe", "out"):
        ap.add_argument("--" + k, default=None, required=k in ("host", "caps", "route", "runbook", "out"))
    ap.add_argument("--scratch", default="", help="the scratch folder of the runs, replaced by <scratch> in every string")
    a = ap.parse_args()
    host, caps, route, first, runbook = load(a.host), load(a.caps), load(a.route), load(a.first_route), load(a.runbook)
    by_id = {}
    for src in (host.get("checks"), caps.get("checks"), route.get("checks")):
        for c in src or []:
            by_id[c["name"].split(" ")[0]] = bool(c["ok"])
    conditions = {k: {"tests": v, "all_passed": all(by_id.get(t) is True for t in v), "missing": [t for t in v if t not in by_id]} for k, v in CONDITIONS.items()}
    issued = []
    if a.issued:
        with open(a.issued) as f:
            issued = [json.loads(x) for x in f if x.strip()]
    probe = load(a.probe)
    out = {
        "what": "round 4, fixer B (step 3 and host safety): the laboratory's bearer, the box caps, the spend stop, the request route, the strict "
                "config schema, the publication folder, the books of an interrupted job. PILOT_NEVER_REUSE_AS_EXAM: every instance made for "
                "these checks is pilot material in a scratch folder.",
        "evidence": {"host_checks": "TRIPWIRES: run on the host of the cloud container with every kill, delete, move, mode change and process start "
                                    "replaced by a tripwire before the package was imported (tools/check_round4.py; the last check is that no tripwire fired)",
                     "through_vf_eval": "VF-EVAL: run through vf-eval in containers that verifiers started (image physim2-ring:2, run label physim2-port4b), "
                                        "Linux x86_64, Docker 29.9.2; the model endpoint was tools/standin_model.py on 127.0.0.1 with a made-up key word",
                     "runbook_text": "READ: RUNBOOK_MAC.md checked as text (tools/check_runbook.py); its one failing check is the pin file, which this role does not regenerate",
                     "step3_shell_lines": "the commands of step 3 that were issued as `sh -c` lines, with a scratch folder as HOME",
                     "macos": "nothing ran on a Mac: everything about macOS and Docker Desktop is INFERRED",
                     "model": "no model was called and no credential was passed, loaded or read by any of these runs"},
        "commands": [
            "env -i PATH=$PATH HOME=$HOME .venv/bin/python -B tools/check_round4.py --scratch <scratch>/chk --out <scratch>/chk/round4_host.json",
            "env -i PATH=$PATH HOME=$HOME VF_RUN_ID=physim2-port4b nice -n 10 .venv/bin/python -B tools/check_step3.py --scratch <scratch>/e2e2 --out ... --dev-machine cloud-container --disk-floor-gib 1.2",
            "env -i PATH=$PATH HOME=$HOME VF_RUN_ID=physim2-port4b nice -n 10 .venv/bin/python -B tools/check_step3.py --scratch <scratch>/e2e3 --out ... --dev-machine cloud-container --only route --disk-floor-gib 1.2",
            ".venv/bin/python -B tools/check_runbook.py --out <scratch>/chk/runbook_check.json",
            "python3 <scratch>/reh/issue.py <key> [JOB_ID]    (one runbook command of step 3 as sh -c, HOME = a scratch folder)",
        ],
        "host_checks": {"tool": host.get("tool"), "n_checks": host.get("n_checks"), "n_failed": host.get("n_failed"), "failed": host.get("failed"),
                        "wall_s": host.get("wall_s"), "checks": brief(host.get("checks"))},
        "through_vf_eval": {
            "caps": {"n_checks": sum(1 for c in caps.get("checks", []) if c["name"].startswith("K")),
                     "n_failed": sum(1 for c in caps.get("checks", []) if c["name"].startswith("K") and not c["ok"]),
                     "checks": brief([c for c in caps.get("checks", []) if c["name"].startswith("K")]), "measured": caps.get("caps")},
            "route": {"n_checks": route.get("n_checks"), "n_failed": route.get("n_failed"), "failed": route.get("failed"), "wall_s": route.get("wall_s"),
                      "checks": brief(route.get("checks")), "measured": route.get("route")},
        },
        "mac_runner_conditions_on_the_spend_stop": conditions,
        "runbook_text_check": None if runbook is None else {k: runbook.get(k) for k in ("copy", "n_checks", "n_passed", "failed")},
        "step3_commands_issued_as_shell_lines": issued,
        "step2b_probe_at_this_code": None if probe is None else {k: probe.get(k) for k in ("n_checks_round5", "n_reproduced", "failed_round5", "n_checks_new", "n_passed_new", "failed_new", "wall_s")},
        "bounds_for_the_default_config": {
            "config": {"model": "qwen/qwen3.6-35b-a3b", "max_turns": 150, "max_output_tokens_per_turn": 8192, "max_context_tokens": 200000, "cap_usd": 1.0},
            "prices_usd_per_mtok_listed_on_2026-11-11": {"input": 0.11, "output": 1.01, "cache_read": 0.099, "context_window": 262144},
            "one_worst_case_call_usd": round((200000 * 0.11 + 8192 * 1.01) / 1e6, 6),
            "bound_on_the_bill_usd": round(1.0 + (200000 * 0.11 + 8192 * 1.01) / 1e6, 6),
            "crude_bound_without_the_spend_stop_usd": round(150 * (262144 * 0.11 + 8192 * 1.01) / 1e6, 4),
            "source": "the request check of step 3b, issued as a shell line against the provider's public model list (no credential): see step3_commands_issued_as_shell_lines"},
    }
    if first is not None:
        out["through_vf_eval"]["first_route_run"] = {
            "n_checks": sum(1 for c in first.get("checks", []) if c["name"].startswith("R")),
            "failed": [c["name"].split(" ")[0] for c in first.get("checks", []) if c["name"].startswith("R") and not c["ok"]],
            "why": "four faults of the TEST, found at its first complete run and fixed before the run reported above: R16 and R17 asked a laboratory "
                   "of a finished reference policy (its record is in the same folder; its port was closed and its process gone), R18 looked for a word "
                   "that its own script contains, R22 expected the model to see the result of its last tool call, which no agent ever sees (the note "
                   "that call wrote IS in the graded submission: R24b). The code under test did not change between the two runs, except that the "
                   "request now arrives through fetch and the stages take --shared-ledger."}
    text = json.dumps(out, indent=1, default=str)
    for old, new in ((a.scratch, "<scratch>"), (ROOT, "<study>"), (os.path.expanduser("~"), "<home>")):
        if old and len(old) > 3:
            text = text.replace(old, new)
    hits = {}
    for name in CRED:
        v = os.environ.get(name) or ""
        if len(v) >= 8:
            n = text.count(v) + text.count(base64.b64encode(v.encode()).decode().rstrip("="))
            if n:
                hits[name] = n
    if hits:
        print(json.dumps({"refused": "a credential's value is in the assembled text", "names_and_counts": hits}))
        return 3
    with open(a.out, "w") as f:
        f.write(text + "\n")
    print(json.dumps({"out": os.path.relpath(a.out, ROOT), "bytes": len(text), "credential_values_found": 0,
                      "conditions_all_passed": all(c["all_passed"] for c in conditions.values()),
                      "conditions_with_a_missing_test": {k[:1]: c["missing"] for k, c in conditions.items() if c["missing"]}}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
