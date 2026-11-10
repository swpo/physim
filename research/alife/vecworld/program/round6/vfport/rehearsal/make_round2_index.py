"""make_round2_index -- results/host_safety_round2.json: for each remaining change of the round-1 verdict
(HOST_SAFETY_AUDIT.md, "Re-audit, round 1"), what was changed, where (file and lines, found by text), the test
the verdict names, its result and the file that records it. It reads result files and RUNBOOK_MAC.md and writes
one JSON file; it starts nothing.

usage: python3 -B rehearsal/make_round2_index.py --reruns DIR
       (DIR holds the reruns of tools/check_safety.py, check_driver.py and check_interrupt.py made from the
        rehearsal's clone: safety_host.json, driver_container.json, safety_interrupt.json; they are compared with
        the files of the same name under results/ and only their counts are kept)
"""
import argparse
import hashlib
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
RES = os.path.join(ROOT, "results")


def load(name, folder=RES):
    f = os.path.join(folder, name)
    return json.load(open(f)) if os.path.exists(f) else None


def update_summary(index, reh, rb):
    """results/summary.json is written by tools/make_summary.py, which is listed in PIN.sha256 and was not changed.
    Round 2 is added to that file here: three blocks under host_safety and two notes; nothing else is touched."""
    f = os.path.join(RES, "summary.json")
    S = json.load(open(f))
    H = S["host_safety"]
    H["re_audit_round_1"] = {
        "file": "HOST_SAFETY_AUDIT.md, section 'Re-audit, round 1' (commit 971c66bc8)",
        "verdict": "NO-GO for the Mac, narrowly: the code passed (A1, A3, A4, A5 closed; the verdict on the code holds for PIN.sha256 7aa9bbfc...f64c19), "
                   "the runbook's stop-and-recover text did not (A2: the waiting shell in the process listing, the interpreter's process line, no branch for a cut "
                   "in step 1, the pin handover, a rehearsal that hid the first of these)",
        "open_and_not_fixed_in_round_2": "two minor gaps of the guard on Linux hosts (a memory file system below /dev, /proc or /sys passes the mount condition; the "
                                         "guard ignores the process namespace) and two of the tools (the box scripts' gate does not look at mounts; check_units.py "
                                         "runs tar and chmod -R on a temp folder before its tripwires): they need a change of pinned files and a re-audit of its diff"}
    H["round_2_of_fixes"] = {
        "source": "results/host_safety_round2.json (one entry per remaining change: what changed, the lines, the verdict's test, its result)",
        "status": index["status"], "scope": index["scope"], "all_named_tests_pass": index["all_named_tests_pass"],
        "named_tests": {k: [v["result"].get("n_passed"), v["result"].get("n_checks")] for k, v in index["changes"].items() if "n_checks" in v["result"]},
        "stand_in_tests": "results/session_mode_round2.json: 47 of 47 (rehearsal/check_round2.py)",
        "pinned_text_checker": {"source": "results/safety_runbook_round2.json", "n_checks": rb["n_checks"], "n_passed": rb["n_passed"], "failed": rb["failed"],
                                "note": "the failing check asks for the round-1 process pattern, which change 1 replaces"},
        "regression": {k: ({kk: vv for kk, vv in v.items() if kk in ("n_checks", "n_passed", "failed", "every_check_equal_to", "rerun", "summary")} if isinstance(v, dict) else v)
                       for k, v in index["regression"].items()}}
    H["rehearsal_round_2"] = {k: reh.get(k) for k in ("outcome", "commit_rehearsed", "where", "counts", "hidden_values_in_this_record")}
    H["runbook"]["note"] = ("the pinned text checker on the ROUND-1 runbook; for the runbook as it is now see round_2_of_fixes.pinned_text_checker "
                            "and results/session_mode_round2.json")
    H["rehearsal"]["note"] = "the first rehearsal (round 1, commands run from files); the second, in session mode, is rehearsal_round_2"
    cv = S["code_versions"]
    cv["round 2 of the host-safety fixes"] = ("changed no file of the package, the tools, the agents or the configs (PIN.sha256 unchanged); it changed RUNBOOK_MAC.md and added "
                                              "rehearsal/ (cloud-only test tooling, not on the pilot's route) and results/*round2*")
    cv["run again in round 2 on the same code"] = ("results/rehearsal_round2_proof.json (one world of the proof with the Mac's arguments), rehearsal_round2_probe.json (the "
                                                   "probes, 37 rollouts), one direct vf-eval rollout, and reruns of check_safety.py, check_driver.py, check_interrupt.py "
                                                   "that equal the recorded files")
    n = 0
    for name in sorted(os.listdir(HERE)):
        if name.endswith(".py"):
            n += sum(1 for _ in open(os.path.join(HERE, name)))
    S["code"]["rehearsal_folder_round_2"] = {"lines_of_python": n, "note": "cloud-only test tooling of round 2; not counted in `new`, not listed in PIN.sha256"}
    json.dump(S, open(f, "w"), indent=1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--reruns", required=True)
    a = ap.parse_args()
    book = open(os.path.join(ROOT, "RUNBOOK_MAC.md")).read().splitlines()

    def line(needle, nth=1):
        hits = [i + 1 for i, ln in enumerate(book) if needle in ln]
        if len(hits) < nth:
            raise SystemExit(f"RUNBOOK_MAC.md has no line {nth} with: {needle}")
        return hits[nth - 1]

    sm, reh, rb = load("session_mode_round2.json"), load("rehearsal_round2.json"), load("safety_runbook_round2.json")
    ck = sm["checks"]

    def res(prefixes, source="results/session_mode_round2.json"):
        names = sorted(k for k in ck if any(k.startswith(p) for p in prefixes))
        return {"source": source, "n_checks": len(names), "n_passed": sum(ck[k] is True for k in names),
                "failed": [k for k in names if ck[k] is not True], "checks": names}

    t = reh["tests_named_by_the_verdict"]
    listing = 'ps axww -o pid= -o command= | grep -E "^ *[0-9]+ /ABSOLUTE/PATH/TO/vfport/\\.venv/bin/python"'
    changes = {
        "1 process listing (N1)": {
            "changed": "both status commands list the pilot's processes with `" + listing + "` (step 3's keeps its `cut -c 1-160`); "
                       "the round-1 pattern `[p]ython` is gone; section C has a by-hand check that the study path holds only letters, digits and / . _ - "
                       "(it is now a search pattern); point 1 of 'If a run was interrupted' forbids any other ps or pgrep",
            "files": [f"RUNBOOK_MAC.md line {line('ps axww -o pid= -o command=', 1)} (status command of step 2), line {line('ps axww -o pid= -o command=', 2)} (status command of step 3), "
                      f"line {line('path is plain')} (section C), lines {line('It prints the last lines of the logs that exist')}-{line('else. A Docker error under')} (what the status prints)"],
            "differs_from_the_verdicts_literal_text": "the verdict wrote `ps axwwo pid=,command=`. POSIX lets the header text after `=` run to the end of the argument, "
                                                       "and a BSD ps may then print the pid column only, under the header `,command=`. Two -o options mean the same and "
                                                       "are unambiguous. On this Linux both forms print the same lines (compared here: 77 lines, equal). macOS: inferred",
            "verdict_test": "the 2a command issued as one `sh -c '<text>'` lists the tool and not the waiting shell",
            "result": dict(res(["text_1_", "standin_1_"]), rehearsal=t["change_1"]),
            "evidence": "read (text_1_*); run with stand-ins, sh and bash, with the round-1 listing as a control that shows the waiting shell (standin_1_*); "
                        "vf-eval (the real tool, results/rehearsal_round2.json entries 16 to 18 and 63 to 65, the latter through the session's own command tool)"},
        "2 stop command (N1)": {
            "changed": "the stop command is `... && ps -ww -p PID_FROM_THE_STATUS_LINE -o command= | grep -E \"^/ABSOLUTE/PATH/TO/vfport/\\.venv/bin/python\" && "
                       "kill -TERM PID_FROM_THE_STATUS_LINE`: it prints the command line of the process it signals, and prints and signals nothing for any other pid; "
                       "the text says what to do when it prints nothing",
            "files": [f"RUNBOOK_MAC.md line {line('kill -TERM PID_FROM_THE_STATUS_LINE')} (the command), lines {line('2. **A tool or a vf-eval of the pilot is still running**')}-{line('Send the signal once; never')} (point 2), "
                      f"line {line('| you | ONE process of the pilot')} (inventory)"],
            "verdict_test": "aimed at the waiting shell's pid it prints nothing and signals nothing",
            "result": dict(res(["text_2_", "standin_2_"]), rehearsal=t["change_2"]),
            "evidence": "read; run with stand-ins (also `sh -xc`: the shell executed ps and grep and no kill; a foreign `sleep` and a pid that is gone: nothing); "
                        "vf-eval (the real waiting shell, the real tool twice, the real vf-eval of 2c, a live laboratory, a laboratory that was gone)"},
        "3 interpreter (N2)": {
            "changed": "`--managed-python` on both uv commands; the dry run's expected lines taken from the rehearsal (`Using CPython 3.12.<n>` without a path); "
                       "a new command after the import check prints the interpreter's own process line and INTERPRETER-OK or INTERPRETER-DIFFERS; after the start of 2a "
                       "(and 2b, 2c) the text says what `processes:` must show and: if not, send no signal, wait for EXIT, stop and report",
            "files": [f"RUNBOOK_MAC.md lines {line('--managed-python --dry-run')}-{line('so allow it a minute')} (dry run), line {line('nohup uv sync')} (sync), "
                      f"lines {line('The status and stop commands of step 2 find the pilot')}-{line('Nothing after this step could find or stop')} (interpreter check), "
                      f"lines {line('It prints Docker' + chr(39) + 's version and returns at once (the tool runs on, detached)')}-{line('line other than `EXIT 0`: stop and report.')} (2a)"],
            "found_on_the_way": "with --managed-python the DRY RUN already downloads uv's own Python when uv has none (33 MB here); the runbook now says so in step 1 and in the inventory",
            "verdict_test": "(the rehearsal) the interpreter's own process line begins with the study folder's .venv/bin/python",
            "result": dict(res(["text_3_", "standin_3_"]), rehearsal=t["change_3"]),
            "evidence": "read; run with stand-ins, including an interpreter that re-executes under another path, as a framework Python does: INTERPRETER-DIFFERS, and the "
                        "status lists nothing while its tool runs; run (the rehearsal's own .venv on uv's Python 3.12.13: INTERPRETER-OK). macOS: inferred"},
        "4 step 1 and the head of 'If a run was interrupted' (N3)": {
            "changed": "the pilot folders are made before the sync; the real `uv sync` runs detached with a log, an EXIT line and a status command; step 1 says: a cut "
                       "or an unexpected output: run nothing more, report, stop. 'If a run was interrupted' begins: for step 2 only; a cut in step 0, 1 or 4: stop; use it once, at a "
                       "second interruption points 1 to 5 and stop; a Docker error under containers: stop. Point 6 and step 4: 'If it prints nothing: stop and report'",
            "files": [f"RUNBOOK_MAC.md lines {line('A cut or an unexpected output anywhere in this step')}-{line('`EXIT 0`.', 1)} (step 1), "
                      f"lines {line('## If a run was interrupted')}-{line('particular do not start the step again before the end of this section.')} (head of the section), "
                      f"line {line('Expected: `pilot folders reset`. If it prints nothing: stop and report.')} (point 6), line {line('Expected: the five file names. If it prints nothing: stop and report.')} (step 4)"],
            "verdict_test": "(the rehearsal) the changed commands of step 1",
            "result": dict(res(["text_4_"]), rehearsal=t["change_4"]),
            "evidence": "read; run (the detached sync and its status in the rehearsal). The rule 'use this section once' was not exercised as a rule"},
        "5 pin handover (N4)": {
            "changed": "the file names no commit. Rule A.1, section C and step 0 say: the commit is the 40-character hash of the coordinator's GO message, the lead gives it "
                       "to the session, the first line of step 0 must equal it; the code is identified by the sha256 of PIN.sha256 (unchanged). The hold notice stands between "
                       "HOLD-BEGIN and HOLD-END and is the only text a verdict edits. Step 0 says what a failed comparison prints",
            "files": [f"RUNBOOK_MAC.md lines {line('<!-- HOLD-BEGIN')}-{line('<!-- PIN-END -->')} (hold notice and pin block), line {line('1. **Two things come from the lead before your first command:**')} (rule A.1), "
                      f"lines {line('| hold lifted |')}-{line('| right text |')} (section C), lines {line('Expected: two lines. The first is the 40-character hash')}-{line('hash in the first line: stop.')} (step 0)"],
            "verdict_test": "(none named) what `shasum -a 256 -c PIN.sha256 > /dev/null && echo PIN-OK` prints when a listed file was changed or is missing",
            "result": dict(res(["text_5_", "standin_5_"]), rehearsal=t["change_5"], pin={"sha256_of_PIN.sha256": hashlib.sha256(open(os.path.join(ROOT, "PIN.sha256"), "rb").read()).hexdigest(),
                                                                                         "tools/pin.py --check": rb["evidence"]["pin"]["pin.py --check"]}),
            "evidence": "read; run on a copy of the three trees in scratch (shasum 6.04, the Perl script that macOS also ships: inferred to print the same there)"},
        "6 text that would trip the stop rule": {
            "changed": "what each log shows after a stop, as seen in the rehearsal (a table in point 2); the end of single.log (two lines of token counts and a closing brace); "
                       "the numbers that macOS pads (four places); and the six places where this rehearsal differed from the text (results/rehearsal_round2.json, mismatches)",
            "files": [f"RUNBOOK_MAC.md lines {line('| stopped | the log ends with |')}-{line('| the vf-eval of 2c |')} (the three endings), line {line('and a closing `}`) and `EXIT 0`')} (2c), "
                      f"lines {line('The second is `0` (macOS pads')}, {line('macOS pads the two `wc` numbers')}, {line('Expected: `0 docker/extra-ca.crt` (macOS pads')}, {line('Expected: `0` (macOS pads it with spaces)')} (padding)"],
            "verdict_test": "(the rehearsal) take the log endings from it",
            "result": dict(res(["text_6_"]), rehearsal=t["change_6"], mismatches_found_and_corrected=len(reh["mismatches"])),
            "evidence": "read; vf-eval (the three endings were each seen once)"},
        "7 rehearsal in session mode": {
            "changed": "rehearsal/issue.py issues ONE fenced command of the runbook as `sh -c '<text>'` and records its literal text and complete output; "
                       "rehearsal/make_record.py writes the record; rehearsal/check_round2.py is the stand-in test",
            "files": ["rehearsal/issue.py", "rehearsal/make_record.py", "rehearsal/remarks_round2.json", "rehearsal/check_round2.py", "results/rehearsal_round2.json",
                      "results/rehearsal_round2_proof.json", "results/rehearsal_round2_probe.json"],
            "verdict_test": "at least: step 0; the changed commands of step 1; 2a with a status while it runs; one stop by points 1 and 2, first aimed at the waiting "
                            "shell's pid on purpose; one hard kill with points 3 to 6; 2a to its end; a status and a stop during 2c",
            "result": {"source": "results/rehearsal_round2.json", "commit_rehearsed": reh["commit_rehearsed"], "outcome": reh["outcome"], "counts": reh["counts"],
                       "interruptions": len(reh["interruptions"]), "deviations": len(reh["deviations"]), "mismatches": len(reh["mismatches"]),
                       "hidden_values_in_the_record": reh["hidden_values_in_this_record"]},
            "evidence": "run; vf-eval (42 finished and 4 cut rollouts, scripted harness, push = false, no model)"},
        "same pass, not gating (the audit file's list)": {
            "changed": "the never table forbids any `docker run` by hand for anything of this repository, whatever its options; the paid command of step 3 has "
                       "`test -f \"$HOME/physim2-pilot-20261110/scratch/LEAD-GO-STEP3\" &&` after its guard (a file the lead creates by hand); a command, used only if the lead "
                       "asks for it, copies the run folder of step 3 out before step 4, unread, and only when the report tool counts no hidden value (the lead decided that "
                       "pilot traces may be uploaded where that helps; the upload is the lead's own act)",
            "files": [f"RUNBOOK_MAC.md line {line('| `docker run` with `-v`, `--mount` or the Docker socket; any other')} (never table), line {line('LEAD-GO-STEP3\" && docker info')} (paid command), "
                      f"lines {line('**The trace of this rollout, only if the lead asks for it.**')}-{line('operator' + chr(39) + 's account; what happens to it')} (trace)"],
            "verdict_test": "(none named)",
            "result": res(["text_same_pass_", "standin_same_pass_"]),
            "evidence": "read; run with stand-ins for vf-eval and for the report tool. Step 3 was never run; the gate of the trace copy was also run once on the scripted "
                        "run of 2c (rehearsal entry 87)"},
    }
    regression = {}
    for name, tool, how in (("safety_host.json", "tools/check_safety.py", "host, 65 tripwires installed before the package is imported"),
                            ("driver_container.json", "tools/check_driver.py", "two throwaway containers without a host path, one with --tmpfs /extra"),
                            ("safety_interrupt.json", "tools/check_interrupt.py", "a throwaway container; two labelled containers of its own, removed by exact name")):
        new, old = load(name, a.reruns), load(name)
        regression[tool] = {"rerun_from_the_rehearsals_clone": True, "how": how, "n_checks": new["n_checks"], "n_passed": new["n_passed"], "failed": new["failed"],
                            "every_check_equal_to": f"results/{name}: {new['checks'] == old['checks']}"}
    regression["tools/check_probe.py"] = {"rerun": "step 2b of the rehearsal (37 rollouts through vf-eval; the driver, its wipe, the hostile agents)",
                                          "source": "results/rehearsal_round2_probe.json", "summary": reh["clean_pass"]["2b"]}
    regression["tools/prove.py"] = {"rerun": "one world with the Mac's arguments, step 2a of the rehearsal", "source": "results/rehearsal_round2_proof.json",
                                    "summary": reh["clean_pass"]["2a"]}
    regression["a direct vf-eval rollout"] = {"rerun": "step 2c of the rehearsal", "summary": reh["clean_pass"]["2c"]}
    regression["tools/check_runbook.py (pinned, unchanged)"] = {
        "source": "results/safety_runbook_round2.json", "n_checks": rb["n_checks"], "n_passed": rb["n_passed"], "failed": rb["failed"],
        "why_one_fails": "run_processes_are_listed_by_this_checkouts_own_environment asks for the round-1 pattern `grep \"<path>/.venv/bin/[p]ython\"`, which change 1 "
                         "replaces; the tool is listed in PIN.sha256 and was not changed. rehearsal/check_round2.py checks the new pattern (text_1_*)"}
    regression["NOT rerun"] = {
        "tools/check_units.py": "no file listed in PIN.sha256 changed since results/units.json (66 of 66) was made on this same code; and a part of this tool runs outside "
                                "its tripwires (the round-1 re-audit's N8), which this role may not do on this host",
        "tools/prove.py --worlds 4, the gliders rollout, the red team's attacks": "as before: not rerun by anyone on the code of the pin"}
    named = [v["result"] for k, v in changes.items() if "n_checks" in v["result"]]
    out = {"what": "round 2 of fixes after the host-safety audit: the seven remaining changes of the round-1 verdict (HOST_SAFETY_AUDIT.md, 'Re-audit, round 1', commit "
                   "971c66bc8), each with the test the verdict names, its result and the file that records it",
           "status": "RUNBOOK_MAC.md stays ON HOLD: these changes have not been re-audited",
           "scope": "runbook text and one rehearsal. No file listed in PIN.sha256 changed: " + rb["evidence"]["pin"]["pin.py --check"][0],
           "runbook_sha256": hashlib.sha256(("\n".join(book) + "\n").encode()).hexdigest(),
           "evidence_labels": {"read": "the cited text was read or checked as text",
                               "run with stand-ins": "the runbook's own command texts issued as one `<shell> -c '<text>'` against a stand-in study folder in scratch; no file of the port executed",
                               "run": "a command of the runbook run in the rehearsal's clone in the cloud container",
                               "tripwire": "run on the cloud host with every destructive primitive of the Python process replaced by a recorder that raises (tools/tripwires.py)",
                               "container": "run in a throwaway container started without any host mount, removed afterwards",
                               "vf-eval": "rollouts through vf-eval physim2-env --env.id isolated-verifier on Docker, scripted harness, no push",
                               "inferred": "every statement about macOS and Docker Desktop: nothing ran there"},
           "changes": changes, "regression": regression,
           "all_named_tests_pass": all(r["n_passed"] == r["n_checks"] for r in named),
           "hidden_values_in_this_file": "none"}
    json.dump(out, open(os.path.join(RES, "host_safety_round2.json"), "w"), indent=1)
    update_summary(out, reh, rb)
    print(json.dumps({"all_named_tests_pass": out["all_named_tests_pass"], "changes": {k: [v["result"].get("n_passed"), v["result"].get("n_checks")] for k, v in changes.items()},
                      "files": {k: v["files"][0][:200] for k, v in changes.items()}}, indent=1))


if __name__ == "__main__":
    main()
