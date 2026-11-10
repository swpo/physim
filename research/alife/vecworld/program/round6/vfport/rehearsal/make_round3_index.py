"""make_round3_index -- results/host_safety_round3.json: one entry per finding of the Mac session's review (M1 to
M3, m1 to m11) and for the coordinator's disk requirement (D1): status, where it was confirmed, what changed
(file and lines, found by text at the time this runs), the test, its result and the file that records it.
It also writes the round-3 part of results/summary.json (host_safety.round_3_of_fixes, .rehearsal_round_3), the
way rehearsal/make_round2_index.py did for round 2. It reads files and writes those two; nothing else.

usage: python3 -B rehearsal/make_round3_index.py --rehearsed-commit HASH
"""
import argparse
import hashlib
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
RES = os.path.join(ROOT, "results")


def line(path, text, nth=1):
    """`<path>:<line>` of the nth line of `path` that holds `text` (so that cited lines are the lines of this commit)."""
    k = 0
    for i, ln in enumerate(open(os.path.join(ROOT, path)), 1):
        if text in ln:
            k += 1
            if k == nth:
                return f"{path}:{i}"
    raise SystemExit(f"{path}: no line holds {text!r}")


def span(path, first, last):
    a, b = line(path, first), line(path, last)
    return f"{a}-{b.rsplit(':', 1)[1]}"


def load(name):
    f = os.path.join(RES, name)
    return json.load(open(f)) if os.path.exists(f) else None


def passed(doc, prefix):
    ks = [k for k in doc["checks"] if k.startswith(prefix)]
    return f"{sum(doc['checks'][k] is True for k in ks)} of {len(ks)}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rehearsed-commit", required=True)
    a = ap.parse_args()
    c3, rb, sh, si, reh = (load(n) for n in ("round3_checks.json", "safety_runbook_round3.json", "safety_host_round3.json",
                                              "safety_interrupt_round3.json", "rehearsal_round3.json"))
    pin = hashlib.sha256(open(os.path.join(ROOT, "PIN.sha256"), "rb").read()).hexdigest()
    V, R = "tools/vfrun.py", "RUNBOOK_MAC.md"
    vf = "verifiers 0.3.2.dev163, verifiers/v1/"
    probe = (reh or {}).get("probe_2b") or {}
    E = {}
    E["M1"] = {
        "finding": "the session's own environment is never checked; all of it reaches vf-eval, the docker client and the laboratory",
        "status": "closed", "confirmed": [f"{vf}runtimes/subprocess.py:104,134,151 (the laboratory gets vf-eval's environment minus *API_KEY*)",
                                          f"{vf}runtimes/container.py:44-57 (the docker client inherits it)", f"{vf}mcp/server.py:278-283 (MCP_HOST, MCP_PORT)",
                                          "physim2_env/_paths.py (PHYSIM2_AGENTENV)", "the old tools/vfrun.py child_env copied everything but PRIME_API_KEY"],
        "changed": "a step-0 command the session runs itself (names only, the docker context and its address); child_env is an allow-list of nine names; "
                   "a tool refuses an environment that holds a name of the step-0 list; a tool refuses a Docker context that is not a Unix socket of the "
                   "machine; every docker call of the tools gets the allow-listed environment; the laboratory binds 127.0.0.1 whatever MCP_HOST says",
        "files": [span(V, "ENV_PASS = (", "MODEL_ENV = "), span(V, "def refused_names", "Nothing was started. Stop and report.\")"),
                  span(V, "def child_env", "    return env"), span(V, "def endpoint_is_local", "    return r.stdout.strip()"),
                  line("physim2_env/lab_tools.py", 'os.environ["MCP_HOST"] = "127.0.0.1"'), line(R, "env | cut -d= -f1 | awk"),
                  line(R, "**What reaches those processes from your session (the environment).**")],
        "test": "tripwires: child_env, refused_names and require_clean_environment on a made-up session of 30 names; container: the stand-in for vf-eval "
                "writes down its environment; a session with DOCKER_HOST is refused before anything starts. Rehearsal: step 0 from a clean and from a "
                "deliberately dirty session",
        "result": {"round3_checks host_env_*": passed(c3, "host_env_"), "box": [k for k in c3["checks"] if "allow_list" in k or "docker_host" in k]},
        "record": ["results/round3_checks.json", "results/rehearsal_round3.json (label 0c-session, twice)"]}
    E["M2"] = {
        "finding": "section B's signal table is incomplete", "status": "closed (text re-derived from the source)",
        "confirmed": [f"{vf}runtimes/container.py:44-65 (SIGKILL of the client's process group whenever the call is cut: KeyboardInterrupt, cancel, timeout)",
                      f"{vf}runtimes/subprocess.py:103-129 (the probe `python -c` and `tail`), :45-53, 197-221 (the laboratory)",
                      f"{vf}utils/version.py:23-31 (git rev-parse, 5 s)", f"{vf}mcp/server.py:112-118 (PDEATHSIG, Linux only)",
                      "tools/vfrun.py, tools/check_probe.py, tools/prove.py: subprocess.run(..., timeout=) kills its own docker client"],
        "changed": "the table has ten rows, each with who can be the target; the status command shows verifiers' probe as PROBE",
        "files": [span(R, "**What is signalled or killed on the Mac.**", "| you | ONE process of the pilot")],
        "test": "the text against the source (read); rehearsal: after the hard kill of vf-eval the status listed exactly one PROBE line for some minutes",
        "result": {"check_runbook": f"{rb['n_passed']} of {rb['n_checks']}"}, "record": ["results/safety_runbook_round3.json", "results/rehearsal_round3.json"]}
    E["M3"] = {
        "finding": "the listener list is incomplete; the Prime key is loaded from ~/.prime/config.json although no model is called",
        "status": "closed; one more reader found here and closed too",
        "confirmed": [f"{vf}interception/server.py:346,444-447 (one TCP listener on 127.0.0.1 per vf-eval)",
                      f"{vf}configs/cli/eval.py:86 -> configs/client.py:37-57 -> utils/prime.py:9-20 (read when verifiers is imported)",
                      f"{vf}configs/client.py:93-104, clients/eval.py:67 (the key into the model client)",
                      f"NEW: {vf}utils/platform.py:93 -> prime_runs/run.py:456 -> prime_traces/core/config.py:25-32 (the SDK reads the file and its key "
                      "for every run, PRIME_RUNS_MODE=disabled included)", "physim2_env/access.py (the Unix socket io.sock)"],
        "changed": "section B lists six listeners with who can connect and what each needs; physim2_env/_nokey.py closes both readers before verifiers is "
                   "imported (first line of the package; tools/vfeval.py is the only way vf-eval is started and refuses without it); every scripted run "
                   "gets a stand-in client; PRIME_API_KEY is not on the allow-list; step 3 has --model-credentials prime on its one command",
        "files": ["physim2_env/_nokey.py", line("physim2_env/__init__.py", "_nokey.install()"), "tools/vfeval.py", span(V, "NO_MODEL_VAR = ", "NO_MODEL_CLIENT = "),
                  line(V, '"client": dict(NO_MODEL_CLIENT)'), span(V, "def check_config", "    return cfg"), line("configs/scripted_ring.toml", "[client]"),
                  span(R, "**What listens on the Mac.**", "**No model credential in steps 0 to 2.**")],
        "test": "a made-up credential file in a scratch home; Python's audit hook on every open (under tripwires): stock import and stock SDK call as "
                "controls, then through the package, as a laboratory in step-3 mode, and tools/vfeval.py --dry-run. Rehearsal: inotify on the folder of "
                "the made-up file for the whole rehearsal, with the stock import as a control at the end",
        "result": {"round3_checks nokey_*": passed(c3, "nokey_"), "host_config_*": passed(c3, "host_config_"),
                   "rehearsal": (reh or {}).get("made_up_credential_file")},
        "record": ["results/round3_checks.json", "results/rehearsal_round3.json: made_up_credential_file"]}
    E["m1"] = {"finding": "the hidden theta on a command line (and so in the status output)", "status": "closed",
               "confirmed": ["the old tools/prove.py:56-57: `--theta v1,v2,...` as an argument of round 5's reference_agent.py"],
               "changed": "tools/build_reference.py reads the parameters from a 0600 file in the store and runs the script in its own process; process "
                          "lines are cut at 160 characters, log lines at 200",
               "files": ["tools/build_reference.py", span("tools/prove.py", "theta_file = os.path.join", "r = vfrun.run_helper(cmd"), line(R, "substr($0, 1, 160)")],
               "test": "tripwires: read_theta on a 0600 file, a 0644 file, a link, a missing file; rehearsal: the record is scanned for the secret and the "
                       "first ten characters of each hidden parameter",
               "result": {"round3_checks host_theta_*": passed(c3, "host_theta_"), "hidden_values_in_the_rehearsal_record": (reh or {}).get("hidden_values_in_this_record")},
               "record": ["results/round3_checks.json", "results/rehearsal_round3.json"]}
    E["m2"] = {"finding": "grep -E reads the dots of the path as wildcards; the stop check accepts any process of the environment", "status": "closed",
               "confirmed": ["RUNBOOK_MAC.md of round 2, status and stop commands"],
               "changed": "awk with index(): the command line must be the interpreter's path followed by one of eight exact beginnings; every listed line "
                          "carries a word (TOOL, VF-EVAL, LAB, HELPER, PROBE, OTHER)",
               "files": [line(R, 'echo "processes:"'), line(R, "kill -TERM PID_FROM_THE_STATUS_LINE")],
               "test": "the two awk programs on made-up ps output (mawk): a neighbour path with another character for the dot, another checkout, pythonX, "
                       "the old console script are not matched; rehearsal: the stop command aimed at the waiting shell prints and sends nothing",
               "result": {"check_runbook": [k for k in rb["checks"] if k.startswith("r3_process") or k.startswith("r3_the_stop")]},
               "record": ["results/safety_runbook_round3.json", "results/rehearsal_round3.json (label I2-stop)"]}
    E["m3"] = {"finding": "the rm -rf guards follow a linked pilot folder", "status": "closed", "confirmed": ["RUNBOOK_MAC.md of round 2, point 6 and step 4"],
               "changed": "`test ! -L` on the pilot folder and its two subfolders before both rm -rf; step 0 and step 1 refuse links",
               "files": [line(R, "pilot folders reset"), line(R, "-results/\" && test -s")], "test": "text", "result": {"check_runbook": rb["checks"]["r3_no_rm_rf_follows_a_linked_pilot_folder"]},
               "record": ["results/safety_runbook_round3.json"]}
    E["m4"] = {"finding": "no interruption step for an orphaned make_instances or reference-agent helper", "status": "closed",
               "confirmed": ["the old tools/prove.py and tools/check_probe.py: subprocess.run without a handler; a SIGTERM to the tool left the helper running"],
               "changed": "vfrun.run_helper stops the helper with its tool; HELPER in the status and stop commands; point 4 of the section",
               "files": [span(V, "def run_helper", "    return subprocess.CompletedProcess"), line(R, "4. **A `LAB` or a `HELPER` line is still listed")],
               "test": "container: SIGTERM to a tool whose helper sleeps", "result": {"box_a_helper_is_stopped_with_its_tool": c3["checks"]["box_a_helper_is_stopped_with_its_tool"]},
               "record": ["results/round3_checks.json"]}
    E["m5"] = {"finding": "on macOS the laboratory does not die with vf-eval; vfrun went on after a SIGKILL", "status": "closed (macOS: inferred)",
               "confirmed": [f"{vf}mcp/server.py:112-118 (prctl, Linux only)", "the old tools/vfrun.py run_eval returned after any end of the child"],
               "changed": "a vf-eval that the tool stopped, or that died of a signal, ends the tool: status 98 (97 for the disk) and a line `refused to go on`; "
                          "section B and point 4 say what macOS does",
               "files": [span(V, "def end_of_child", "    raise SystemExit(EXIT_STOPPED)"), line(R, "**Not on macOS:**")],
               "test": "container: time limit, a stand-in that ignores SIGTERM, a stand-in that dies of SIGKILL; rehearsal: EXIT 98 after the hard kill",
               "result": {"round3_checks": [k for k in c3["checks"] if "status_98" in k or "sigkill" in k], "check_interrupt": f"{si['n_passed']} of {si['n_checks']}",
                          "check_safety": f"{sh['n_passed']} of {sh['n_checks']}"},
               "record": ["results/round3_checks.json", "results/safety_interrupt_round3.json", "results/safety_host_round3.json", "results/rehearsal_round3.json"]}
    E["m6"] = {"finding": "point 3's docker rm -f does not re-check the label", "status": "closed", "confirmed": ["RUNBOOK_MAC.md of round 2, point 3"],
               "changed": "the command reads the run label Docker has for that exact name and removes only if it is this pilot's",
               "files": [line(R, "docker rm -f NAME_FROM_THE_STATUS_LINE")],
               "test": "rehearsal: a name nobody has; a container of the rehearsal's own with another label; the pilot's leftover box",
               "result": {"check_runbook": rb["checks"]["r3_docker_rm_reads_the_label_back_first"]}, "record": ["results/rehearsal_round3.json (label I3-docker-rm, three times)"]}
    E["m7"] = {"finding": "on Docker Desktop any container can reach the laboratory's unauthenticated port", "status": "rule in the runbook now; the bearer is DEFERRED to before step 3",
               "confirmed": [f"{vf}runtimes/docker/__init__.py:224-225,336 (host.docker.internal off Linux)", "the laboratory's tool has no secret"],
               "changed": "a command before step 2 that must list no running container; section B says why; step 3 names the bearer as an open condition",
               "why_deferred": "the laboratory's address is handed to harnesses by verifiers and read by round 5's client; a bearer changes the tool's interface "
                               "in pinned files of two folders and needs its own audit",
               "files": [line(R, 'echo "RUNNING-LISTED"'), line(R, "- **A bearer for the laboratory.**")], "test": "text", "result": {"check_runbook": rb["checks"]["r3_no_other_container_runs_during_step_2"]},
               "record": ["results/safety_runbook_round3.json"]}
    E["m8"] = {"finding": "the proxy check never asks for 127.0.0.1, localhost, vf.host.internal or host.docker.internal", "status": "closed (measured on Linux)",
               "confirmed": ["the old agents/probe_grading.py:156-157 asked for example.com and the gateway address only"],
               "changed": "the probe asks the box's proxy, with the box's credentials, for the four names at the listener's port, by GET and by CONNECT (over a "
                          "plain socket: urllib would bypass the proxy for names on NO_PROXY); a new check requires HTTP 403 eight times",
               "files": [span("agents/probe_grading.py", "LOOPBACK_NAMES = (", "def box_report(host_port, lab_url, full):"), line("agents/probe_grading.py", '"proxy_loopback_names": {n:'),
                         line("tools/check_probe.py", '"c_agent_box_proxy_refuses_the_workers_own_loopback_names"')],
               "test": "rehearsal, step 2b: one real box", "result": probe.get("proxy_loopback_names"), "record": ["results/rehearsal_round3_probe.json"]}
    E["m9"] = {"finding": "hatchling is unpinned and runs on the Mac", "status": "closed for versions; hashes are not possible",
               "confirmed": ["the old pyproject.toml:18: hatchling>=1.27,<2"],
               "changed": "hatchling==1.33.0 and five packages under it as [tool.uv] build-constraint-dependencies; uv 0.11.32 records them in uv.lock "
                          "([manifest] build-constraints) and --locked refuses a pyproject.toml that differs",
               "files": [span("pyproject.toml", "[build-system]", '  "trove-classifiers=='), line("uv.lock", "build-constraints = [")],
               "test": "scratch copy: `uv lock --locked` with one changed constraint fails; rehearsal: the detached `uv sync --locked` ends EXIT 0",
               "result": "as expected", "record": ["results/rehearsal_round3.json (labels 1a-uv-dry-run, 1c-uv-sync, 1c-status)"]}
    E["m10"] = {"finding": "step 1's BuildKit cache is in no inventory", "status": "closed (text)", "confirmed": ["RUNBOOK_MAC.md of round 2"],
                "changed": "section B and step 4 name it; step 4 prints `docker system df`; removing it is the lead's",
                "files": [line(R, "the build cache of those two builds"), line(R, "&& docker system df")], "test": "text",
                "result": {"check_runbook": rb["checks"]["r3_build_cache_is_in_the_inventory_and_in_step_4"]}, "record": ["results/safety_runbook_round3.json"]}
    E["m11"] = {"finding": "the `| wc -l` counts of step 0 hide command failures", "status": "closed", "confirmed": ["RUNBOOK_MAC.md of round 2, steps 0 and 4"],
                "changed": "no count: each listing is followed by a word that is printed only if the listing command succeeded",
                "files": [line(R, 'echo "TREE-LISTED"'), line(R, 'echo "NO-PILOT-FOLDERS"')], "test": "text; rehearsal",
                "result": {"check_runbook": rb["checks"]["r3_no_count_can_hide_a_failed_command"]}, "record": ["results/safety_runbook_round3.json", "results/rehearsal_round3.json"]}
    E["D1"] = {"finding": "the coordinator's requirement: the pilot protects the disk itself (floor 8 GiB on the home folder's file system)", "status": "closed",
               "changed": "tools/vfrun.py: refusal before a run, a look every 15 s during a run, the one stop path (one SIGTERM to vf-eval), the reason in the "
                          "log and in <run>.stopped.json, status 97, nothing deleted; --disk-floor-gib on prove.py, check_probe.py and the command form; "
                          "runbook: rule 7, a disk command in step 0, the same check in front of the three starts of step 1, the lead's decision in step 3",
               "files": [span(V, "GIB = 1 << 30", "EXIT_STOPPED = 98"), span(V, "def free_bytes", "    return free"), span(V, "def run_child", "    return p.returncode, out or"),
                         line(R, "7. **The disk.**"), line(R, "DISK-OK"), line(R, "- **The lead's decision about Docker Desktop's disk.**")],
               "test": "tripwires: the floor and the refusal with the free space injected; container: refusal before a run, a stop during a run with the "
                       "stand-in, the command form under the floor; rehearsal: the runbook's own 8 GiB refused on this machine (1.8 GiB free), and a stop "
                       "during a real rollout after 48 MiB were written",
               "result": {"round3_checks host_disk_*": passed(c3, "host_disk_"), "box_watchdog_*": passed(c3, "box_watchdog_"),
                          "rehearsal": (reh or {}).get("disk_watchdog")},
               "record": ["results/round3_checks.json", "results/rehearsal_round3.json"]}
    out = {"what": "round 3 of fixes after the host-safety audit: the Mac session's read-only review of commit af767adbd (three major, eleven minor points) "
                   "and the coordinator's disk requirement, each confirmed against the code and the verifiers source first",
           "status": "RUNBOOK_MAC.md is ON HOLD: the round-2 GO is suspended and these changes have not been re-audited",
           "rehearsed_commit": a.rehearsed_commit, "sha256_of_PIN.sha256": pin, "files_in_PIN.sha256": len(open(os.path.join(ROOT, "PIN.sha256")).read().splitlines()),
           "rejected_findings": [], "deferred": ["m7: the laboratory's bearer (before step 3)"],
           "checks": {"tools/check_round3.py": f"{c3['n_passed']} of {c3['n_checks']}", "tools/check_safety.py": f"{sh['n_passed']} of {sh['n_checks']}",
                      "tools/check_interrupt.py": f"{si['n_passed']} of {si['n_checks']}", "tools/check_runbook.py": f"{rb['n_passed']} of {rb['n_checks']}",
                      "failed": c3["failed"] + sh["failed"] + si["failed"] + rb["failed"]},
           "evidence_labels": {"read": "the cited lines were read", "tripwires": "run on the cloud host in a process that installed tools/tripwires.py first",
                               "container": "run in a throwaway container without a host mount", "vf-eval": "scripted rollouts through vf-eval, no upload",
                               "inferred": "everything about macOS and Docker Desktop"},
           "findings": E}
    json.dump(out, open(os.path.join(RES, "host_safety_round3.json"), "w"), indent=1)
    f = os.path.join(RES, "summary.json")
    S = json.load(open(f))
    H = S["host_safety"]
    H["re_audit_round_2"] = {"file": "HOST_SAFETY_AUDIT.md, section 'Re-audit, round 2' (commit af767adbd)",
                             "verdict": "GO for steps 0 to 2 on the Mac, for that one commit; SUSPENDED on 10 Nov 2026 after the Mac session's own read-only review"}
    H["round_3_of_fixes"] = {k: out[k] for k in ("what", "status", "rehearsed_commit", "sha256_of_PIN.sha256", "files_in_PIN.sha256", "rejected_findings", "deferred", "checks")}
    H["round_3_of_fixes"]["findings"] = {k: {"status": v["status"], "changed": v["changed"]} for k, v in E.items()}
    H["round_3_of_fixes"]["index"] = "results/host_safety_round3.json"
    if reh:
        H["rehearsal_round_3"] = {k: reh.get(k) for k in ("outcome", "counts", "interruptions", "disk_watchdog", "made_up_credential_file", "mismatches", "deviations",
                                                           "not_rehearsed", "hidden_values_in_this_record") if k in reh}
        H["rehearsal_round_3"]["file"] = "results/rehearsal_round3.json"
    for k in ("runbook", "interruption", "tests_on_the_host"):
        if isinstance(H.get(k), dict):
            H[k]["stale_since_round_3"] = "this entry describes the code and the text before round 3; see round_3_of_fixes"
    json.dump(S, open(f, "w"), indent=1)
    print(json.dumps({"findings": len(E), "checks": out["checks"], "sha256_of_PIN.sha256": pin}))


if __name__ == "__main__":
    main()
