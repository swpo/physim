"""make_safety_summary -- results/host_safety_round1.json: for each required change of the host-safety audit
(HOST_SAFETY_AUDIT.md, section 4) what was changed, which test the audit named, where that test is, and what it
gave. Reads result files only:

    results/safety_host.json        tools/check_safety.py     host, every destructive primitive a tripwire
    results/driver_container.json   tools/check_driver.py     two throwaway containers, no host path mounted
    results/safety_interrupt.json   tools/check_interrupt.py  a throwaway container; two containers of its own
    results/safety_runbook.json     tools/check_runbook.py    the runbook as text; its guard run with echo
    results/units.json              tools/check_units.py      host, tripwires around the driver's functions
    results/probe_ring.json         tools/check_probe.py      37 rollouts through vf-eval on Docker
    results/rehearsal_round1.json   (written by hand from the rehearsal's logs)   if it exists

usage: python -B tools/make_safety_summary.py
"""
import hashlib
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
RES = os.path.join(ROOT, "results")


def load(name):
    f = os.path.join(RES, name)
    return json.load(open(f)) if os.path.isfile(f) else None


def pick(res, prefixes, source):
    """The checks of one result file whose names start with one of the prefixes, with the count that passed."""
    if res is None:
        return {"source": source, "missing": True}
    checks = res.get("checks") or res.get("checks_new") or {}
    got = {k: v for k, v in checks.items() if k.startswith(tuple(prefixes))}
    return {"source": source, "n_checks": len(got), "n_passed": sum(v is True for v in got.values()),
            "failed": [k for k, v in got.items() if v is not True], "checks": sorted(got)}


def main():
    host, drv, intr, book = load("safety_host.json"), load("driver_container.json"), load("safety_interrupt.json"), load("safety_runbook.json")
    units, probe, reh = load("units.json"), load("probe_ring.json"), load("rehearsal_round1.json")
    pin = os.path.join(ROOT, "PIN.sha256")
    changes = {
        "1 working directory (A1)": {
            "changed": "RUNBOOK_MAC.md: every command starts with `cd \"<absolute study folder>\" && test -f RUNBOOK_MAC.md && test -f "
                       "physim2_env/taskset.py &&`; uv is used in two commands only, both with --project <absolute path>, the dry run first "
                       "(started from / so that uv prints the environment's absolute path); no `uv run`; rule 'no subagents'",
            "files": ["RUNBOOK_MAC.md (rules A.1 to A.3, step 1)", "tools/check_runbook.py"],
            "audit_test": "from a wrong folder, the guarded line with echo in place of uv prints nothing",
            "result": pick(book, ["guard_", "uv_"], "results/safety_runbook.json"), "evidence": "run (cd, test, echo only); uv's wording read from a dry run in the cloud container"},
        "2 interruption (A2)": {
            "changed": "tools/vfrun.py: VF_RUN_ID is required (it becomes the container label verifiers.run), Docker must answer before a "
                       "run, vf-eval is stopped with ONE SIGTERM and killed only 120 s later, a stop request to the tool is passed on; "
                       "RUNBOOK_MAC.md: long commands run detached with a log and an EXIT line, a status command lists the pilot's containers "
                       "by label and the pilot's processes by this checkout's own .venv path, a section 'If a run was interrupted' "
                       "(stop by pid, remove by exact name, delete the two pilot folders, restart from make_instances), step 4 lists by label",
            "files": ["tools/vfrun.py (run_label, require_docker, clear_run_dir, stop_child, run_child, run_eval)", "tools/check_probe.py (label on its control container)",
                      "RUNBOOK_MAC.md (step 2, 'If a run was interrupted', step 4)", "tools/check_interrupt.py", "tools/check_safety.py (R2)"],
            "audit_test": "a stub for vf-eval records SIGTERM under timeout=1; in the cloud container a foreign vf-other is absent from the label listing",
            "result": {"stand-in without a process, host under tripwires": pick(host, ["R2_"], "results/safety_host.json"),
                       "a real process and real signals in a throwaway container; label listing": pick(intr, ["stop_", "label_"], "results/safety_interrupt.json"),
                       "runbook text": pick(book, ["run_"], "results/safety_runbook.json")},
            "evidence": "tripwire; container; read"},
        "3 box scripts (A3)": {
            "changed": "agents/hostile_submission.py, agents/probe_grading.py, redteam/agent_rt.py: the first statement exits unless /.dockerenv "
                       "exists and /etc/physim2/predictor_uid is a root-owned regular file; asked again directly before each `kill -9 -1`, "
                       "before the box's tar is removed or replaced and before the mount attempt",
            "files": ["agents/hostile_submission.py", "agents/probe_grading.py", "redteam/agent_rt.py", "tools/check_safety.py (R3)", "tools/check_probe.py (two checks)"],
            "audit_test": "runpy.run_path under recorders, every mode: SystemExit, empty recorder; the harness-killall rollout still passes",
            "result": {"runpy on the host under tripwires (34 starts, and 6 with one sign of a box simulated)": pick(host, ["R3_"], "results/safety_host.json"),
                       "through vf-eval: the kill is issued inside the box (exit status 137), every box script gets past its gate there":
                           pick(probe, ["h_", "box_scripts_"], "results/probe_ring.json: checks_new")},
            "evidence": "tripwire; vf-eval"},
        "4 driver (A4, A5)": {
            "changed": "physim2_env/public/_item.py: (a) wipe_user unlinks and rmdirs exactly the paths owned_by listed, deepest first, never a "
                       "mount point; shutil is no longer imported and the reply directory is removed through its handle (remove_io); "
                       "(b) the mount table is read from /proc/self/mountinfo and an unreadable table raises (box_mounts, mount_points; "
                       "no fallback to /); (c) the guard has a mount condition: anything but an overlay root, kernel file systems at or "
                       "below /proc, /sys, /dev and Docker's three /etc files is refused (parse_mounts, foreign_mounts, guard_reasons); "
                       "scan walks nothing outside a box",
            "files": ["physim2_env/public/_item.py", "tools/fixtures/mounts/ (3 captured tables, 10 written by hand, EXPECTED.json)", "tools/check_driver.py",
                      "tools/check_safety.py (R4)", "tools/check_units.py (guard block)"],
            "audit_test": "the pure function on stored mount tables; in the check_driver.py container a root-owned canary below a uid-owned "
                          "directory survives, --tmpfs /extra makes everything refuse, the 19 existing checks pass",
            "result": {"pure function, unreadable table, no rmtree, refusals on this host, wipe logic (host under tripwires)": pick(host, ["R4_"], "results/safety_host.json"),
                       "in two throwaway containers (the 19 earlier checks are among them)": None if drv is None else
                           {"source": "results/driver_container.json", "n_checks": drv["n_checks"], "n_passed": drv["n_passed"], "failed": drv["failed"],
                            "the_audits_three": {k: drv["checks"].get(k) for k in ("cleanup_leaves_a_root_owned_file_below_a_directory_of_the_uid",
                                                                                 "guard_refuses_everything_with_a_tmpfs_mounted_at_extra",
                                                                                 "mount_driver_on_the_grading_route_runs_nothing", "cleanup_never_removes_a_mount_point")}},
                       "guard block of the unit checks (host under tripwires)": pick(units, ["guard_"], "results/units.json")},
            "evidence": "tripwire; container"},
        "5 worker gate (A4)": {
            "changed": "physim2_env/grading.py: container_gate / require_container accept only an object whose class is exactly verifiers' "
                       "DockerRuntime or PrimeRuntime, with the matching config type, not borrowed (info.borrowed), for Docker not nested and "
                       "with a container name verifiers generated (vf-<32 hex>); called by stage, run_request, _public_files, setup, "
                       "BoxAccess.check / announce, collect_frozen and by the scripted harness (setup, install, launch)",
            "files": ["physim2_env/grading.py (container_gate, require_container)", "physim2_env/taskset.py (setup, _public_files)", "physim2_script/__init__.py (require_box)",
                      "tools/check_safety.py (R5)"],
            "audit_test": "recording fakes typed docker and subprocess receive zero commands from stage, run_request, _public_files, BoxAccess.check",
            "result": pick(host, ["R5_"], "results/safety_host.json"), "evidence": "tripwire; and 37 rollouts through vf-eval pass the gate with real runtimes (results/probe_ring.json)"},
        "6 runbook text (B3, B6 to B9, B12)": {
            "changed": "RUNBOOK_MAC.md rewritten: an inventory of what is signalled, deleted, written and listening on the Mac; the store path "
                       "on each command; 'stop and report' replaces the Docker shim; a docker info gate before each run; step 4 is one && "
                       "chain that copies the results out first and keeps the images; the one expected macOS failure is named and any other "
                       "deviation is a stop; the 'never' table",
            "files": ["RUNBOOK_MAC.md", "tools/check_runbook.py"],
            "audit_test": "review against section 3 of the audit (a reading task; the mechanical part is checked as text)",
            "result": pick(book, ["text_", "hold"], "results/safety_runbook.json"), "evidence": "read"},
        "7 pin (B11)": {
            "changed": "PIN.sha256 lists the sha256 of every tracked file the pilot executes or imports (this folder's package, tools, agents, "
                       "configs, Dockerfiles, pyproject.toml, uv.lock; round 5's agentenv; the vw library); the runbook's pin block carries the "
                       "hash of that list and, in the copy at the head of the branch, one commit; the lead checks that commit out detached, "
                       "step 0 compares commit, status and hashes",
            "files": ["PIN.sha256", "tools/pin.py", "RUNBOOK_MAC.md (pin block, by-hand table, step 0)"],
            "audit_test": "(none named) the comparison commands of step 0 were run in the rehearsal",
            "result": dict(pick(book, ["pin_"], "results/safety_runbook.json"),
                           sha256_of_PIN=hashlib.sha256(open(pin, "rb").read()).hexdigest() if os.path.isfile(pin) else None,
                           commit_named=((book or {}).get("evidence", {}).get("pin") or {}).get("commit_named")),
            "evidence": "run"},
        "8 rehearsal (B10)": {
            "changed": "steps 0 to 2 (and step 4) of the rewritten runbook were run once in the cloud container from a fresh clone of the pushed "
                       "commit with its own .venv, the commands copied from the runbook, with one deliberate interruption",
            "files": ["results/rehearsal_round1.json"],
            "audit_test": "the rehearsal itself",
            "result": {"source": "results/rehearsal_round1.json", "missing": True} if reh is None else
                      {"source": "results/rehearsal_round1.json", "outcome": reh.get("outcome"), "commit_rehearsed": reh.get("commit_rehearsed"),
                       "deviations": len(reh.get("deviations", [])), "mismatches_of_text_and_behaviour": len(reh.get("mismatches", []))},
            "evidence": "run; vf-eval"},
        "9 step 3 only (B13 to B15)": {
            "changed": "RUNBOOK_MAC.md step 3: its own hold; the paid command alone between STOP lines with the price formula and a line the "
                       "lead fills in; output to a file that is never displayed; tools/run_report.py prints fixed fields and counts, never "
                       "message text; no claude_code / codex; Docker Desktop's disk limit below the free space. Step 3 was not run",
            "files": ["RUNBOOK_MAC.md (step 3)", "tools/run_report.py", "configs/qwen_ring_bash.toml (comment)"],
            "audit_test": "(none named) text checks; the report tool was run on scripted rollouts only",
            "result": pick(book, ["step3_"], "results/safety_runbook.json"), "evidence": "read; the report tool run on scripted traces"},
        "S1 driver hardening (B1 to B3)": {
            "changed": "_item.py: uid range 20000-59999 (MIN_UID, MAX_UID); --uid required, no default; the guard requires a root caller; the "
                       "identity is verified after the set-id calls, before kill(-1) (as_user, is_only) and before the predictor starts; "
                       "outside a box nothing runs unless --no-box is given. taskset.py: the agent box's marker is drawn from the reserved "
                       "range instead of 1000. validate.py: runs only where the marker exists and passes --uid and --no-box",
            "files": ["physim2_env/public/_item.py", "physim2_env/public/validate.py", "physim2_env/taskset.py", "physim2_env/grading.py (UID_RANGE)"],
            "result": {"host under tripwires": pick(host, ["S1_"], "results/safety_host.json"),
                       "in the container": None if drv is None else {k: drv["checks"].get(k) for k in (
                           "guard_refuses_uid_1000_with_a_marker_that_says_1000", "guard_refuses_uid_19999_just_below_the_reserved_range",
                           "guard_refuses_uid_60000_just_above_the_reserved_range", "cleanup_signals_nothing_when_the_identity_did_not_change",
                           "driver_without_route_variable_and_without_no_box_runs_nothing", "driver_uid_has_no_default")},
                       "through vf-eval": None if probe is None else {"predictor_runs_unprivileged": probe["checks_round5"].get("predictor_runs_unprivileged"),
                                                                      "uids": probe["evidence"]["predictor_checks"]["uid"]}},
            "evidence": "tripwire; container; vf-eval"},
        "S2 tools (B4, B5)": {
            "changed": "tools/check_units.py: the driver is never started as a program by root, the guard block runs under tools/tripwires.py "
                       "(65 names, installed before the driver is imported) and is skipped for code without a guard. redteam/rt_run.py: a "
                       "new agents directory per call instead of deleting one, run folders through vfrun.clear_run_dir, a sibling container "
                       "with a name of its own. redteam/nproc_cross_box.sh: container names of its own (not rerun)",
            "files": ["tools/check_units.py", "tools/tripwires.py", "redteam/rt_run.py", "redteam/nproc_cross_box.sh"],
            "result": None if units is None else {"source": "results/units.json", "n_checks": units["n_checks"], "n_passed": units["n_passed"], "failed": units["failed"],
                                                  "driver_as_a_program_on_this_host": units["evidence"]["driver_host_guard"]},
            "evidence": "tripwire (check_units); read only (rt_run.py, nproc_cross_box.sh were not run)"},
    }
    regression = {
        "tools/check_units.py": None if units is None else {"source": "results/units.json", "n_checks": units["n_checks"], "n_passed": units["n_passed"],
                                                            "failed": units["failed"], "how": "host; tripwires around every call into the driver"},
        "tools/check_driver.py": None if drv is None else {"source": "results/driver_container.json", "n_checks": drv["n_checks"], "n_passed": drv["n_passed"],
                                                           "failed": drv["failed"], "how": "two throwaway containers"},
        "tools/check_probe.py": None if probe is None else {"source": "results/probe_ring.json", "round5_checks": [probe["n_reproduced"], probe["n_checks_round5"]],
                                                            "failed_round5": probe["failed_round5"], "new_checks": [probe["n_passed_new"], probe["n_checks_new"]],
                                                            "failed_new": probe["failed_new"], "rollouts": len(probe["rollouts"]), "wall_s": probe["wall_s"],
                                                            "how": "vf-eval, Docker, scripted harness, no push"},
        "tools/prove.py": "one world with the Mac's arguments, in the rehearsal (results/rehearsal_round1.json)",
        "not_rerun": ["tools/prove.py --worlds 4 (results/proof_ring.json, recomputed_table.json: package code of commit 743f6b75e)",
                      "the gliders smoke rollout (results/gliders_smoke_D.json)", "the red team's attacks (redteam/results/*)",
                      "anything on macOS, any model rollout"],
    }
    out = {"what": "round 1 of fixes after the host-safety audit's NO-GO (HOST_SAFETY_AUDIT.md, commit 3fda8505a): the nine required changes and "
                   "the two hardening items, each with the test the audit named and its result",
           "status": "RUNBOOK_MAC.md stays ON HOLD: these changes have not been re-audited",
           "evidence_labels": {"read": "the cited text was read or checked as text", "tripwire": "run on the cloud host with every destructive primitive "
                               "of the Python process replaced by a recorder that raises (tools/tripwires.py)",
                               "container": "run in a throwaway container started without any host mount, removed afterwards",
                               "vf-eval": "rollouts through vf-eval physim2-env --env.id isolated-verifier on Docker, scripted harness, no push",
                               "inferred": "every statement about macOS and Docker Desktop: nothing ran there"},
           "changes": changes, "regression": regression,
           "all_named_tests_pass": all(r is not None and not r.get("missing") and not r.get("failed") for r in (
               changes["1 working directory (A1)"]["result"], changes["5 worker gate (A4)"]["result"], changes["6 runbook text (B3, B6 to B9, B12)"]["result"],
               changes["9 step 3 only (B13 to B15)"]["result"], *changes["2 interruption (A2)"]["result"].values(),
               *changes["3 box scripts (A3)"]["result"].values(), changes["4 driver (A4, A5)"]["result"]["pure function, unreadable table, no rmtree, refusals on this host, wipe logic (host under tripwires)"],
               changes["4 driver (A4, A5)"]["result"]["in two throwaway containers (the 19 earlier checks are among them)"])),
           "hidden_values_in_this_file": "none"}
    json.dump(out, open(os.path.join(RES, "host_safety_round1.json"), "w"), indent=1)
    print(json.dumps({"all_named_tests_pass": out["all_named_tests_pass"], "rehearsal": changes["8 rehearsal (B10)"]["result"]}))


if __name__ == "__main__":
    main()
