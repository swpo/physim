"""check_round2 -- the tests the round-1 verdict names for its remaining changes 1 to 6, with STAND-INS.

HOST_SAFETY_AUDIT.md, "Re-audit, round 1", "What remains before GO for the smoke test". Two parts.

text_*      RUNBOOK_MAC.md read as text: the anchored process listing (change 1), the stop command that looks
            before it signals (2), `--managed-python`, the interpreter check and the "must show" rule (3), the
            detached `uv sync` and the new head of "If a run was interrupted" (4), the pin handover (5), the
            three log endings and the two small corrections (6), and which fenced commands differ from the
            round-1 runbook.
standin_*   the runbook's OWN command texts (2a, the status command, the stop command, the interpreter check, the
            pin comparison, the step-3 gate and the trace copy), issued the way a session issues them, as ONE
            `<shell> -c '<text>'` with sh and with bash, in the folder `/`, against a STAND-IN study folder that
            this tool builds below --scratch:
                .venv/bin/python   a link to this machine's Python (or, for the control, a launcher that re-executes
                                   it under another path, as a framework Python does on macOS)
                tools/prove.py     a script that prints one line and sleeps
                .venv/bin/vf-eval  a script that prints one line
            Nothing of the port is imported or executed. The only signal this tool causes is the SIGTERM of the
            runbook's stop command, which goes to the stand-in tool, and only after the command's own check of
            that pid's command line. `$HOME` in the texts is replaced by a folder below --scratch.

It creates files below --scratch only and removes nothing there except, in the pin test, ONE file of its own
copy. Not for the Mac (RUNBOOK_MAC.md, rule 7): it refuses without PHYSIM2_DEV_MACHINE=cloud-container.

usage: PHYSIM2_DEV_MACHINE=cloud-container python3 -B rehearsal/check_round2.py --scratch DIR --out results/session_mode_round2.json
"""
import argparse
import hashlib
import json
import os
import re
import shutil
import signal
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from issue import LABELS, PILOT, PLACE, blocks, pick  # noqa: E402

GUARD = f'cd "{PLACE}" && test -f RUNBOOK_MAC.md && test -f physim2_env/taskset.py && '
REAL_PY = os.path.realpath(sys.executable)
ROUND1_COMMIT = "971c66bc8d078ac0828ab29a47ca1b0d5a5ae6f6"      # the verdict's commit: the runbook it judged


def issue(shell, text, timeout=60, trace=False):
    """ONE `<shell> -c <text>` in `/`, no terminal; with trace=True as `<shell> -xc <text>` (the shell then
    writes every command it executes to stderr with a leading `+`)."""
    t0 = time.time()
    r = subprocess.run(["nice", "-n", "10", shell, "-xc" if trace else "-c", text], cwd="/", stdin=subprocess.DEVNULL,
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=timeout)
    return {"exit": r.returncode, "stdout": r.stdout, "stderr": r.stderr, "seconds": round(time.time() - t0, 2)}


def table(needle):
    r = subprocess.run(["ps", "axww", "-o", "pid=", "-o", "ppid=", "-o", "command="], capture_output=True, text=True)
    rows = []
    for ln in r.stdout.splitlines():
        p = ln.split(None, 2)
        if len(p) == 3 and needle in p[2]:
            rows.append({"pid": int(p[0]), "ppid": int(p[1]), "command": p[2]})
    return rows


def alive(pid):
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    try:                                                     # a zombie still answers signal 0
        return open(f"/proc/{pid}/stat").read().rsplit(")", 1)[1].split()[0] != "Z"
    except OSError:
        return False


def under(out, head, tail):
    lines = out.splitlines()
    if head not in lines or tail not in lines:
        return None
    return lines[lines.index(head) + 1:lines.index(tail)]


def build_standin(root, runbook_text, kind, sleep_s):
    study, home = os.path.join(root, "vfport"), os.path.join(root, "home")
    for d in ("physim2_env", "tools", ".venv/bin", "configs"):
        os.makedirs(os.path.join(study, d))
    open(os.path.join(study, "RUNBOOK_MAC.md"), "w").write(runbook_text)
    open(os.path.join(study, "physim2_env", "taskset.py"), "w").write("# stand-in: an empty file with the name the guard tests for\n")
    open(os.path.join(study, "tools", "prove.py"), "w").write(
        "import time\nprint('stand-in for tools/prove.py: it sleeps and starts nothing', flush=True)\n" f"time.sleep({sleep_s})\n")
    open(os.path.join(study, "tools", "run_report.py"), "w").write(
        "import json, os\nn = int(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'hits')).read())\n"
        "print(json.dumps({'6_hidden_values_in_the_run_folder': {'files_scanned': 1, 'needles': 3, 'hits': {}, 'total_hits': n}}))\n")
    py = os.path.join(study, ".venv", "bin", "python")
    if kind == "link":
        os.symlink(REAL_PY, py)
    else:                                                    # a launcher that re-executes under another path
        open(py, "w").write(f'#!/bin/sh\nexec "{REAL_PY}" "$@"\n')
        os.chmod(py, 0o755)
    vf = os.path.join(study, ".venv", "bin", "vf-eval")
    open(vf, "w").write('#!/bin/sh\necho "stand-in for vf-eval: it starts nothing and calls no model"\n')
    os.chmod(vf, 0o755)
    os.makedirs(os.path.join(home, PILOT, "scratch"))
    os.makedirs(os.path.join(home, PILOT, "store"))
    open(os.path.join(home, PILOT, "store", "index.json"), "w").write("[]\n")
    return study, home


def text_checks(text, checks, ev):
    B = blocks(text)
    status2, status3 = pick(text, "2-status"), pick(text, "3-status")
    listing = f'ps axww -o pid= -o command= | grep -E "^ *[0-9]+ {PLACE}/\\.venv/bin/python"'
    checks["text_1_both_status_commands_list_by_the_anchored_pattern"] = listing + " ; echo" in status2 and listing + " | cut -c 1-160 ; echo" in status3
    checks["text_1_the_old_pattern_is_gone"] = "[p]ython" not in text and "ps axo" not in text
    other_ps = [b for b in B if re.search(r"(^|[ ;&|({])(ps|pgrep) ", b.replace("docker ps", "docker_ps"))
                and b not in (status2, status3, pick(text, "I2-stop"))]
    checks["text_1_no_other_command_lists_processes"] = other_ps == []
    checks["text_1_section_C_checks_that_the_path_is_plain"] = "grep -E '^[A-Za-z0-9/._-]+$'" in text
    stop = pick(text, "I2-stop")
    want_stop = GUARD + f'ps -ww -p PID_FROM_THE_STATUS_LINE -o command= | grep -E "^{PLACE}/\\.venv/bin/python" && kill -TERM PID_FROM_THE_STATUS_LINE'
    kills = [b for b in B if re.search(r"(^|[ ;&|({])kill ", b)]
    checks["text_2_the_stop_command_looks_before_it_signals"] = stop == want_stop
    checks["text_2_it_is_the_only_command_that_signals"] = kills == [stop]
    uv = [b for b in B if re.search(r"(^|[ &|;(])uv ", b)]
    checks["text_3_both_uv_commands_require_a_managed_python"] = len(uv) == 2 and all("--python 3.12 --managed-python" in b for b in uv)
    order = [next(i for i, b in enumerate(B) if all((w[1:] not in b) if w.startswith("!") else (w in b) for w in LABELS[k]))
             for k in ("1a-uv-dry-run", "1b-mkdir-ca", "1c-uv-sync", "1c-status", "1d-import", "1e-interpreter", "1f-build", "1h-make-instances", "2a-prove")]
    ev["order_of_step_1"] = order
    checks["text_3_the_interpreter_check_follows_the_import_check"] = order == sorted(order) and "INTERPRETER-DIFFERS" in pick(text, "1e-interpreter") \
        and f"line.startswith('{PLACE}/.venv/bin/python -B -c ')" in pick(text, "1e-interpreter") and "['ps', '-ww', '-p', str(os.getpid()), '-o', 'command=']" in pick(text, "1e-interpreter")
    flat = re.sub(r"\s+", " ", text)
    checks["text_3_2a_says_what_processes_must_show_and_what_to_do_if_not"] = \
        f"it must show a line `<pid> {PLACE}/.venv/bin/python -B tools/prove.py ...`" in flat and "send no signal and start nothing" in flat
    sync = pick(text, "1c-uv-sync")
    checks["text_4_the_real_uv_sync_runs_detached_with_a_log_and_an_exit_line"] = \
        "{ ( nohup uv sync --project " in sync and f'> "$HOME/{PILOT}/scratch/sync.log" 2>&1 < /dev/null ; echo "EXIT $?" >> "$HOME/{PILOT}/scratch/sync.log" )' in sync \
        and sync.rstrip().endswith("> /dev/null 2>&1 < /dev/null & }") and pick(text, "1c-status") == GUARD + f'tail -n 3 "$HOME/{PILOT}/scratch/sync.log"'
    i = flat.index("## If a run was interrupted")
    head = flat[i:i + 700]
    checks["text_4_the_section_is_for_step_2_only_once_and_stops_on_a_docker_error"] = \
        "This section is for step 2 only" in head and "A cut or an unexpected output in step 0, 1 or 4: run nothing more, report, stop." in head \
        and "Use this section once." in head and "At a second interruption do points 1 to 5, then stop" in head \
        and "If Docker prints an error under `containers:`: stop and report" in flat
    checks["text_4_prints_nothing_means_stop_in_point_6_and_in_step_4"] = flat.count("If it prints nothing: stop and report.") == 2 \
        and "delete nothing and go on" not in flat and "nothing was deleted" not in flat
    m = re.search(r"<!-- PIN-BEGIN -->(.*?)<!-- PIN-END -->", text, re.S)
    pin_block = m.group(1) if m else ""
    hold = re.search(r"<!-- HOLD-BEGIN[^>]*-->(.*?)<!-- HOLD-END -->", text, re.S)
    pin_hash = hashlib.sha256(open(os.path.join(ROOT, "PIN.sha256"), "rb").read()).hexdigest()
    ev["sha256_of_PIN.sha256_on_disk"] = pin_hash
    checks["text_5_the_file_names_no_commit"] = not re.search(r"\b[0-9a-f]{40}\b", text) and pin_hash in pin_block
    a_rules = flat[flat.index("## A. Rules"):flat.index("## B. What the pilot does")]
    c_hand = flat[flat.index("## C. By hand"):flat.index("## 0. Verify the code")]
    step0 = flat[flat.index("## 0. Verify the code"):flat.index("## 1. Install")]
    checks["text_5_rule_A1_section_C_and_step_0_name_the_hash_of_the_GO_message"] = all("40-character" in s and "GO message" in s for s in (a_rules, c_hand, step0))
    checks["text_5_the_hold_notice_is_marked_as_the_only_text_a_verdict_edits"] = bool(hold) and "ON HOLD" in hold.group(1) \
        and text.splitlines()[2].startswith("**ON HOLD. Run nothing from this file.**")
    checks["text_5_step_0_says_what_a_failed_comparison_prints"] = "shasum: WARNING:" in step0 and "FAILED" not in step0
    i2 = flat[flat.index("2. **A tool or a vf-eval of the pilot is still running**"):flat.index("3. **Containers of the pilot are still listed")]
    checks["text_6_the_three_log_endings_after_a_stop"] = "`KeyboardInterrupt`, then `EXIT 130`" in i2 and "`EXIT 143`, no traceback" in i2 and "then `EXIT 130`; no traceback" in i2
    checks["text_6_2c_and_the_padded_numbers"] = "two lines of token counts and a closing `}`" in flat and flat.count("macOS pads") >= 4
    checks["text_same_pass_never_table_step3_gate_and_trace"] = "`--pid`, `--ipc`, `--tmpfs`, `--privileged`, `--volumes-from`" in text \
        and f'test -f "$HOME/{PILOT}/scratch/LEAD-GO-STEP3" && docker info' in pick(text, "3-paid") and "grep -c '\"total_hits\": 0' && mkdir" in pick(text, "3-trace")
    checks["text_every_fenced_command_starts_with_the_guard"] = len(B) >= 28 and all(b.startswith(GUARD) for b in B)
    ev["fenced_commands"] = len(B)
    # which commands differ from the runbook the round-1 verdict judged
    old = subprocess.run(["git", "show", f"{ROUND1_COMMIT}:./RUNBOOK_MAC.md"], cwd=ROOT, capture_output=True, text=True)
    if old.returncode == 0:
        OB = blocks(old.stdout)
        ev["against_the_round1_runbook"] = {
            "commit": ROUND1_COMMIT, "commands_then": len(OB), "commands_now": len(B),
            "unchanged": sum(b in OB for b in B),
            "new_or_changed": [re.sub(r"\s+", " ", b[len(GUARD):])[:90] for b in B if b not in OB],
            "gone_or_changed": [re.sub(r"\s+", " ", b[len(GUARD):])[:90] for b in OB if b not in B]}
    else:
        ev["against_the_round1_runbook"] = "commit not in this clone (shallow): not compared"


def standin_checks(text, scratch, checks, ev):
    for shell in ("sh", "bash"):
        root = os.path.join(scratch, f"standin-{shell}")
        study, home = build_standin(root, text, "link", 300)
        sub = lambda label, **kw: _sub(pick(text, label), study, home, **kw)  # noqa: E731
        e = ev[f"session_mode_{shell}"] = {"study": study, "issued_as": f"{shell} -c '<text>' in /, no terminal"}
        tool_prefix = f"{study}/.venv/bin/python -B tools/prove.py"
        # ---- change 1: 2a issued as one `<shell> -c`, then the status command ----
        start = issue(shell, sub("2a-prove"))
        t = time.time()
        while time.time() - t < 10 and not [r for r in table(study) if r["command"].startswith(tool_prefix)]:
            time.sleep(0.2)
        rows = table(study)
        tool = [r for r in rows if r["command"].startswith(tool_prefix)]
        waiting = [r for r in rows if r["command"].startswith(f'{shell} -c cd "{study}"') and "tools/prove.py" in r["command"]]
        e["2a"] = {"text": sub("2a-prove"), "returned": start, "process_table": [dict(r, command=r["command"][:150]) for r in rows]}
        ok_start = start["exit"] == 0 and start["stdout"].count("\n") == 1 and start["seconds"] < 10 and len(tool) == 1 and len(waiting) == 1
        checks[f"standin_1_{shell}_the_detached_2a_command_returns_at_once_and_leaves_the_tool_and_one_waiting_shell"] = ok_start
        if not ok_start:
            continue
        tool_pid, wait_pid = tool[0]["pid"], waiting[0]["pid"]
        st = issue(shell, sub("2-status"))
        listed = under(st["stdout"], "processes:", "status done")
        e["status"] = {"text": sub("2-status"), "output": st["stdout"], "listed_under_processes": listed, "tool_pid": tool_pid, "waiting_shell_pid": wait_pid}
        checks[f"standin_1_{shell}_the_status_lists_the_tool_and_not_the_waiting_shell"] = listed is not None and len(listed) == 1 \
            and re.fullmatch(rf" *{tool_pid} {re.escape(tool_prefix)} .*", listed[0]) is not None
        # control: the round-1 listing, same moment, same way of issuing
        old = f'cd "{study}" && test -f RUNBOOK_MAC.md && test -f physim2_env/taskset.py && {{ echo "processes:" ; ps axo pid=,command= | grep "{study}/.venv/bin/[p]ython" ; echo "status done" ; }}'
        oc = issue(shell, old)
        old_listed = under(oc["stdout"], "processes:", "status done") or []
        e["control_the_round1_listing"] = {"text": old, "lines": [ln[:150] for ln in old_listed]}
        checks[f"standin_1_{shell}_control_the_round1_listing_shows_the_waiting_shell_too"] = len(old_listed) >= 2 \
            and any(ln.split()[0] == str(wait_pid) for ln in old_listed) and any(ln.split()[0] == str(tool_pid) for ln in old_listed)
        # ---- change 2: the stop command aimed at the waiting shell's pid ----
        log = os.path.join(home, PILOT, "scratch", "prove.log")
        s1 = issue(shell, sub("I2-stop", pid=wait_pid))
        s1x = issue(shell, sub("I2-stop", pid=wait_pid), trace=True)
        time.sleep(1.0)
        executed = [ln for ln in s1x["stderr"].splitlines() if ln.startswith("+")]
        e["stop_aimed_at_the_waiting_shell"] = {"text": sub("I2-stop", pid=wait_pid), "stdout": s1["stdout"], "exit": s1["exit"],
                                                "commands_the_shell_executed_(-x)": executed,
                                                "tool_alive_after": alive(tool_pid), "waiting_shell_alive_after": alive(wait_pid),
                                                "log_after": open(log).read()}
        checks[f"standin_2_{shell}_aimed_at_the_waiting_shell_it_prints_nothing_and_signals_nothing"] = s1["stdout"] == "" and s1["exit"] != 0 \
            and any(re.match(r"\+ ps -ww -p", ln) for ln in executed) and not any(re.match(r"\++ kill", ln) for ln in executed) \
            and alive(tool_pid) and alive(wait_pid) and "EXIT" not in open(log).read()
        # a process of this user that is not the pilot's: a sleep this test starts
        other = subprocess.Popen(["sleep", "120"], stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        s2 = issue(shell, sub("I2-stop", pid=other.pid))
        time.sleep(0.3)
        e["stop_aimed_at_a_foreign_process"] = {"target": "sleep 120 (started by this test)", "stdout": s2["stdout"], "exit": s2["exit"], "alive_after": other.poll() is None}
        checks[f"standin_2_{shell}_aimed_at_a_process_that_is_not_the_pilots_it_signals_nothing"] = s2["stdout"] == "" and s2["exit"] != 0 and other.poll() is None
        other.terminate()                                    # this test's own child
        other.wait()
        # ---- change 2: the stop command aimed at the tool ----
        s3 = issue(shell, sub("I2-stop", pid=tool_pid))
        t = time.time()
        while time.time() - t < 10 and (alive(tool_pid) or alive(wait_pid)):
            time.sleep(0.2)
        after = issue(shell, sub("2-status"))
        e["stop_aimed_at_the_tool"] = {"text": sub("I2-stop", pid=tool_pid), "stdout": s3["stdout"], "exit": s3["exit"],
                                       "tool_alive_after": alive(tool_pid), "waiting_shell_alive_after": alive(wait_pid),
                                       "log_after": open(log).read(), "status_after": after["stdout"]}
        checks[f"standin_2_{shell}_aimed_at_the_tool_it_prints_its_command_line_and_stops_it"] = s3["exit"] == 0 \
            and s3["stdout"].startswith(tool_prefix + " ") and s3["stdout"].count("\n") == 1 and not alive(tool_pid) and not alive(wait_pid) \
            and open(log).read().splitlines()[-1] == "EXIT 143" and under(after["stdout"], "processes:", "status done") == []
        s4 = issue(shell, sub("I2-stop", pid=tool_pid))
        e["stop_aimed_at_a_pid_that_is_gone"] = {"stdout": s4["stdout"], "exit": s4["exit"]}
        checks[f"standin_2_{shell}_aimed_at_a_pid_that_is_gone_it_prints_nothing"] = s4["stdout"] == "" and s4["exit"] != 0
        # ---- change 3: the interpreter check, where the interpreter keeps its path ----
        ic = issue(shell, sub("1e-interpreter"))
        lines = ic["stdout"].splitlines()
        e["interpreter_check"] = {"text": sub("1e-interpreter"), "output": ic["stdout"]}
        checks[f"standin_3_{shell}_the_interpreter_check_passes_where_the_interpreter_keeps_its_path"] = len(lines) == 2 \
            and lines[0].startswith(f"{study}/.venv/bin/python -B -c import os, subprocess;"[:160]) and lines[1] == "INTERPRETER-OK"
        # ---- same pass: the step-3 file gate and the trace copy, with the stand-in vf-eval and report tool ----
        vf = open(os.path.join(study, ".venv", "bin", "vf-eval")).read()
        qlog = os.path.join(home, PILOT, "scratch", "qwen.log")
        if "stand-in for vf-eval" in vf and os.path.getsize(os.path.join(study, ".venv", "bin", "vf-eval")) < 200:
            g0 = issue(shell, sub("3-paid"))
            time.sleep(1.0)
            no_log = not os.path.exists(qlog)
            open(os.path.join(home, PILOT, "scratch", "LEAD-GO-STEP3"), "w").close()     # what the lead does by hand
            g1 = issue(shell, sub("3-paid"))
            t = time.time()
            while time.time() - t < 10 and not (os.path.exists(qlog) and "EXIT" in open(qlog).read()):
                time.sleep(0.2)
            e["step3_file_gate"] = {"without_the_file": {"stdout": g0["stdout"], "exit": g0["exit"], "log_created": not no_log},
                                    "with_the_file": {"stdout": g1["stdout"], "exit": g1["exit"], "log": open(qlog).read() if os.path.exists(qlog) else None}}
            checks[f"standin_same_pass_{shell}_the_paid_command_starts_nothing_without_the_leads_file"] = g0["stdout"] == "" and g0["exit"] != 0 and no_log \
                and g1["exit"] == 0 and g1["stdout"].count("\n") == 1 and os.path.exists(qlog) \
                and open(qlog).read().splitlines() == ["stand-in for vf-eval: it starts nothing and calls no model", "EXIT 0"]
        run = os.path.join(home, PILOT, "scratch", "qwen", "qwen")
        os.makedirs(run)
        open(os.path.join(run, "traces.jsonl"), "w").write("stand-in trace\n")
        trace_dir = os.path.join(home, f"{PILOT}-trace")
        open(os.path.join(study, "tools", "hits"), "w").write("3\n")
        c0 = issue(shell, sub("3-trace"))
        not_copied = not os.path.exists(trace_dir)
        open(os.path.join(study, "tools", "hits"), "w").write("0\n")
        c1 = issue(shell, sub("3-trace"))
        e["trace_copy"] = {"with_3_hidden_values": {"stdout": c0["stdout"], "exit": c0["exit"], "copied": not not_copied},
                           "with_0": {"stdout": c1["stdout"], "exit": c1["exit"], "copied": os.path.isfile(os.path.join(trace_dir, "qwen", "traces.jsonl"))}}
        checks[f"standin_same_pass_{shell}_the_trace_is_copied_only_when_the_report_counts_no_hidden_value"] = c0["stdout"] == "0\n" and c0["exit"] != 0 and not_copied \
            and c1["stdout"] == "1\nqwen\n" and c1["exit"] == 0 and os.path.isfile(os.path.join(trace_dir, "qwen", "traces.jsonl"))

    # ---- change 3, control: an interpreter that re-executes under another path (a framework Python does) ----
    root = os.path.join(scratch, "standin-reexec")
    study, home = build_standin(root, text, "reexec", 8)
    e = ev["interpreter_that_reexecutes"] = {"study": study, "launcher": open(os.path.join(study, ".venv", "bin", "python")).read()}
    ic = issue("sh", _sub(pick(text, "1e-interpreter"), study, home))
    lines = ic["stdout"].splitlines()
    e["interpreter_check"] = {"output": ic["stdout"]}
    checks["standin_3_control_the_interpreter_check_says_DIFFERS_for_a_reexecuting_interpreter"] = len(lines) == 2 and lines[1] == "INTERPRETER-DIFFERS" \
        and lines[0].startswith(REAL_PY + " -B -c ")
    start = issue("sh", _sub(pick(text, "2a-prove"), study, home))
    time.sleep(1.5)
    st = issue("sh", _sub(pick(text, "2-status"), study, home))
    running = [r for r in table(root) if r["command"].startswith(REAL_PY + " -B tools/prove.py --store " + home)]
    e["status_while_its_tool_runs"] = {"output": st["stdout"], "the_tool_really_runs": [dict(r, command=r["command"][:120]) for r in running]}
    checks["standin_3_control_the_status_lists_nothing_while_that_tool_runs_which_the_2a_rule_catches"] = start["exit"] == 0 and len(running) == 1 \
        and under(st["stdout"], "processes:", "status done") == []
    log = os.path.join(home, PILOT, "scratch", "prove.log")
    t = time.time()
    while time.time() - t < 30 and not (os.path.exists(log) and "EXIT" in open(log).read()):
        time.sleep(0.5)                                      # the rule: send no signal, wait for EXIT
    e["its_log_at_the_end"] = open(log).read()
    checks["standin_3_control_it_ends_by_itself_with_an_exit_line"] = open(log).read().splitlines()[-1] == "EXIT 0"

    # ---- change 5: what the pin comparison prints, on a copy of the three trees ----
    copy = os.path.join(scratch, "pincopy", "vecworld")
    cstudy = os.path.join(copy, "program", "round6", "vfport")
    ign = shutil.ignore_patterns(".venv", "__pycache__", ".git", "*.egg-info", "outputs", "extra-ca.crt")
    shutil.copytree(ROOT, cstudy, ignore=ign)
    shutil.copytree(os.path.join(ROOT, "..", "..", "round5", "agentenv"), os.path.join(copy, "program", "round5", "agentenv"), ignore=ign)
    shutil.copytree(os.path.join(ROOT, "..", "..", "..", "vw1", "vw"), os.path.join(copy, "vw1", "vw"), ignore=ign)
    cmd = pick(text, "0b-pin").replace(PLACE, cstudy)
    run = lambda: (lambda r: {"stdout": r["stdout"], "stderr": r["stderr"], "exit": r["exit"]})(issue("sh", cmd))  # noqa: E731
    intact = run()
    with open(os.path.join(cstudy, "tools", "settle.py"), "a") as f:
        f.write("\n# one line added by rehearsal/check_round2.py, in its own copy\n")
    changed = run()
    victim = os.path.join(cstudy, "tools", "recompute_table.py")
    assert victim.startswith(os.path.realpath(scratch) + os.sep)
    os.remove(victim)                                        # ONE file of this test's own copy
    missing = run()
    ev["pin_comparison"] = {"text": cmd, "intact": intact, "one_file_changed": changed, "one_changed_and_one_missing": missing,
                            "shasum": subprocess.run(["shasum", "--version"], capture_output=True, text=True).stdout.strip()}
    pin_hash = hashlib.sha256(open(os.path.join(ROOT, "PIN.sha256"), "rb").read()).hexdigest()
    checks["standin_5_intact_the_pin_comparison_prints_the_hash_and_PIN_OK"] = intact["stdout"] == f"{pin_hash}  PIN.sha256\nPIN-OK\n" and intact["exit"] == 0
    checks["standin_5_a_changed_file_gives_a_shasum_WARNING_line_and_no_PIN_OK"] = changed["exit"] != 0 and "PIN-OK" not in changed["stdout"] \
        and "FAILED" not in changed["stdout"] + changed["stderr"] and changed["stderr"].strip() == "shasum: WARNING: 1 computed checksum did NOT match"
    checks["standin_5_a_missing_file_gives_no_such_file_and_a_WARNING_line"] = missing["exit"] != 0 and "PIN-OK" not in missing["stdout"] \
        and "shasum: tools/recompute_table.py: No such file or directory" in missing["stderr"] and "shasum: WARNING: 1 listed file could not be read" in missing["stderr"]

    # nothing of the stand-ins may be left running
    left = [r for r in table(os.path.join(scratch, "standin-")) if "/.venv/bin/python" in r["command"] or " -c cd " in r["command"]]
    ev["standin_processes_left_at_the_end"] = [dict(r, command=r["command"][:120]) for r in left]
    checks["standin_no_process_of_a_standin_is_left"] = left == []


def _sub(block, study, home, pid=None):
    cmd = block.replace(PLACE, study).replace("$HOME", home)
    if pid is not None:
        cmd = cmd.replace("PID_FROM_THE_STATUS_LINE", str(pid))
    assert "$HOME" not in cmd and PLACE not in cmd and "PID_FROM_THE_STATUS_LINE" not in cmd
    return cmd


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scratch", required=True, help="an EMPTY folder of this test (it must not exist yet)")
    ap.add_argument("--out", required=True)
    ap.add_argument("--runbook", default=os.path.join(ROOT, "RUNBOOK_MAC.md"))
    ap.add_argument("--text-only", action="store_true")
    a = ap.parse_args()
    if os.environ.get("PHYSIM2_DEV_MACHINE") != "cloud-container" or sys.platform != "linux":
        raise SystemExit("refused: a development check for the cloud container (PHYSIM2_DEV_MACHINE=cloud-container, Linux); not for the Mac")
    text = open(a.runbook).read()
    checks, ev = {}, {}
    text_checks(text, checks, ev)
    if not a.text_only:
        scratch = os.path.realpath(a.scratch)
        if not re.fullmatch(r"[A-Za-z0-9/._-]+", scratch):
            raise SystemExit("refused: --scratch must be a path of plain characters")
        os.makedirs(scratch)                                 # fails if it exists: every run starts from nothing
        try:
            standin_checks(text, scratch, checks, ev)
        finally:                                             # stop what a failed run may have left: stand-in tools only, by pid, after a look
            for r in table(os.path.join(scratch, "standin-")):
                if re.match(rf"{re.escape(scratch)}/standin-[a-z]+/vfport/\.venv/bin/python -B tools/prove\.py ", r["command"]) \
                        or r["command"].startswith(REAL_PY + " -B tools/prove.py --store " + scratch):
                    os.kill(r["pid"], signal.SIGTERM)
    out = {"what": "the tests the round-1 verdict names for its remaining changes 1 to 6: RUNBOOK_MAC.md read as text, and its own command "
                   "texts issued as ONE `<shell> -c '<text>'` (sh and bash) against a stand-in study folder",
           "evidence_label": "read (text_*); run with stand-ins, no file of the port executed (standin_*)",
           "runbook_sha256": hashlib.sha256(text.encode()).hexdigest(),
           "machine": {"sh": os.path.realpath("/bin/sh"), "bash": subprocess.run(["bash", "--version"], capture_output=True, text=True).stdout.splitlines()[0],
                       "ps": subprocess.run(["ps", "--version"], capture_output=True, text=True).stdout.strip(), "python_of_the_standin": REAL_PY},
           "n_checks": len(checks), "n_passed": sum(v is True for v in checks.values()), "failed": [k for k, v in checks.items() if v is not True],
           "checks": checks, "evidence": ev}
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    json.dump(out, open(a.out, "w"), indent=1)
    print(json.dumps({k: out[k] for k in ("n_checks", "n_passed", "failed")}))


if __name__ == "__main__":
    main()
