"""check_runbook -- RUNBOOK_MAC.md checked as text, and its guard checked by running it with `echo`.

Host-safety audit, required changes 1, 2, 6, 7 and 9. This tool reads the runbook and PIN.sha256, starts `bash -c`
lines made of `cd`, `test` and `echo` only, and creates and removes one temporary folder of its own. It runs no
command of the runbook.

  guard_*    (change 1) every command block starts with the guard; the guard, with `echo WOULD-RUN` in place of
             the command, prints nothing when its path is a wrong folder: one that does not exist, the unfilled
             placeholder, another project with a pyproject.toml and a .venv, a folder holding a RUNBOOK_MAC.md
             only, the repository root, a subfolder of the study folder. With the study folder it prints.
  uv_*       (change 1) uv appears in two commands only, both name the project by its absolute path, the dry run
             comes first
  run_*      (change 2) every command that starts a rollout carries VF_RUN_ID, runs detached behind a `docker
             info` gate and writes a log; containers are listed by the run label only, never by name
  text_*     (change 6) no export, sudo, pkill, prune, command substitution, mount option or removal by filter in
             any command; every `rm -rf` is chained behind its checks and names the two pilot folders only; the
             "never" table and the inventory are there; the store path is on each command that needs it
  pin_*      (change 7) the pin block names the hash of PIN.sha256 as it is on disk, PIN.sha256 matches the
             files, and (in the copy at the head of the branch) names one commit
  step3_*    (change 9; round 4) the paid command is the request route's stage `rollout`, alone between STOP lines
             behind the lead's standing go, writes to a file, is read through tools/run_report.py and
             tools/pack_rollout.py only; the stages stand in their order; the block of facts (request shape,
             config schema, profiles with item counts, reference policies) equals what the code prints; no
             `claude_code` / `codex`
  r3_*       (round 3: the Mac session's review and the disk requirement) the pilot's processes are matched letter
             for letter and their lines cut; the stop command signals only after its own comparison; step 0 checks
             the session's own environment with the list the tools use; no command sets a variable but the run
             label or starts vf-eval itself; no count can hide a failed command; no rm -rf follows a linked folder;
             docker rm reads the label back; the disk floor is on every start; no other container during step 2;
             the build cache is named
  hold       the first lines say ON HOLD (in a copy a verdict released: GO for steps 0 to 2, or 0 to 3)

usage: python -B tools/check_runbook.py --out results/safety_runbook.json [--runbook RUNBOOK_MAC.md]
"""
import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
PLACE = "/ABSOLUTE/PATH/TO/vfport"
GUARD = f'cd "{PLACE}" && test -f RUNBOOK_MAC.md && test -f physim2_env/taskset.py && '
LABEL = "physim2-pilot-r5"
PILOT = '"$HOME/physim2-pilot-r5'
ROLLOUTS = '"$HOME/physim2-rollouts'


def blocks(text):
    """The fenced sh blocks, each as one string (a block is ONE command; a python -c "..." may span lines)."""
    out, cur = [], None
    for line in text.splitlines():
        s = line.strip()
        if cur is None and s == "```sh":
            cur = []
        elif cur is not None and s == "```":
            out.append("\n".join(cur))
            cur = None
        elif cur is not None:
            cur.append(line.strip() if not cur else line)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--runbook", default=os.path.join(ROOT, "RUNBOOK_MAC.md"))
    a = ap.parse_args()
    text = open(a.runbook).read()
    B = blocks(text)
    inline = re.findall(r"`(cd \"[^`]+)`", text)             # commands quoted inside a sentence
    cmds = B + inline
    checks, ev = {}, {"command_blocks": len(B), "inline_commands": len(inline)}

    # ---- change 1: the guard ----
    checks["guard_every_command_starts_with_the_guard"] = len(B) >= 20 and all(c.startswith(GUARD) for c in cmds)
    checks["guard_no_command_relies_on_an_earlier_cd"] = not any(re.search(r"(^|\n)\s*(uv|docker|rm|python|\./)", c) and not c.startswith(GUARD) for c in cmds)
    tmp = tempfile.mkdtemp(prefix="physim2-runbook-check-")
    try:
        other = os.path.join(tmp, "other-project")
        os.makedirs(os.path.join(other, ".venv"))
        os.makedirs(os.path.join(other, "sub"))
        open(os.path.join(other, "pyproject.toml"), "w").write("[project]\nname='other'\nversion='0'\n")
        open(os.path.join(other, ".venv", "marker"), "w").write("someone else's environment\n")
        only = os.path.join(tmp, "runbook-only")
        os.makedirs(only)
        open(os.path.join(only, "RUNBOOK_MAC.md"), "w").write("not the study folder\n")
        targets = {
            "a folder that does not exist": os.path.join(tmp, "nope"),
            "the placeholder, not replaced": PLACE,
            "another project (pyproject.toml, .venv)": other,
            "a subfolder of that other project": os.path.join(other, "sub"),
            "a folder with a RUNBOOK_MAC.md only": only,
            "the repository's round6 folder": os.path.dirname(ROOT),
            "a subfolder of the study folder (tools)": HERE,
            "an empty path": "",
            "the study folder": ROOT,
        }
        runs = {}
        for name, target in targets.items():
            line = GUARD.replace(PLACE, target) + "echo WOULD-RUN"
            for cwd_name, cwd in (("started in the other project", os.path.join(other, "sub")), ("started in /", "/")):
                r = subprocess.run(["bash", "-c", line], cwd=cwd, capture_output=True, text=True, timeout=30)
                runs[f"{name}; {cwd_name}"] = {"stdout": r.stdout.strip(), "exit": r.returncode}
        ev["guard_with_echo"] = {"line": GUARD + "echo WOULD-RUN", "runs": runs,
                                 "other_projects_environment_untouched": os.path.isfile(os.path.join(other, ".venv", "marker"))}
        wrong = {k: v for k, v in runs.items() if not k.startswith("the study folder")}
        right = {k: v for k, v in runs.items() if k.startswith("the study folder")}
        checks["guard_from_a_wrong_folder_prints_nothing"] = len(wrong) == 16 and all(v["stdout"] == "" and v["exit"] != 0 for v in wrong.values())
        checks["guard_with_the_study_folder_runs"] = all(v["stdout"] == "WOULD-RUN" for v in right.values()) and len(right) == 2
    finally:
        shutil.rmtree(tmp)                                   # this tool's own temporary folder

    # ---- change 1: uv ----
    uv = [c for c in cmds if re.search(r"(^|[ &|;(])uv ", c)]
    ev["uv_commands"] = [c[len(GUARD):][:150] for c in uv]
    checks["uv_only_two_commands_and_the_dry_run_first"] = len(uv) == 2 and "--dry-run" in uv[0] and "--dry-run" not in uv[1] \
        and "cd / && uv sync" in uv[0]
    checks["uv_names_the_project_by_its_absolute_path_and_is_locked"] = all(f'uv sync --project "{PLACE}" --locked --python 3.12' in c
                                                                          and "test -f pyproject.toml && test -f uv.lock" in c for c in uv)
    checks["uv_run_is_not_used"] = "uv run" not in text
    checks["uv_no_subagents_rule"] = "No subagents" in text

    # ---- change 2: runs ----
    START = r'nohup "[^"]+/\.venv/bin/python" -B tools/(prove|check_probe|vfrun)\.py '
    real = [c for c in cmds if re.search(START, c)]
    dry = [c for c in cmds if "tools/vfrun.py" in c and "--stage dry-run" in c]
    starts = real + dry
    ev["commands_that_start_a_rollout"] = [re.sub(r"\s+", " ", c[len(GUARD):])[:110] for c in real]
    vfrun_cmds = [c for c in cmds if re.search(r'python" -B tools/vfrun\.py ', c)]
    checks["run_every_rollout_command_carries_the_run_label"] = len(real) == 5 and len(dry) == 1 and all(f"VF_RUN_ID={LABEL} " in c for c in starts + vfrun_cmds)
    checks["run_every_rollout_command_is_detached_with_a_log_and_an_exit_line"] = all(
        "{ ( " in c and "nohup " in c and c.rstrip().endswith("> /dev/null 2>&1 < /dev/null & }") and 'echo "EXIT $?" >>' in c and ".log\" 2>&1 < /dev/null" in c
        for c in real)
    checks["run_every_detached_command_has_a_docker_info_gate"] = all("docker info --format '{{.ServerVersion}}' && { ( " in c for c in cmds if "nohup " in c)
    checks["run_the_dry_run_is_alone_in_its_block_and_carries_no_credential_option"] = len(dry) == 1 and dry[0].count("tools/vfrun.py") == 1 \
        and "nohup" not in dry[0] and "--model-credentials" not in dry[0] and "--shared-ledger " in dry[0]
    ps = [c for c in cmds if "docker ps" in c]
    labelled = [c for c in ps if "docker ps -a" in c]
    checks["run_containers_are_listed_by_the_run_label_only"] = len(labelled) >= 4 and all(f"docker ps -a --filter label=verifiers.run={LABEL}" in c for c in labelled) \
        and "name=vf-" not in "\n".join(cmds)
    checks["run_if_interrupted_section"] = all(k in text for k in ("## If a run was interrupted", "kill -TERM PID_FROM_THE_STATUS_LINE",
                                                                  "docker rm -f NAME_FROM_THE_STATUS_LINE", "pilot folders reset", "make_instances"))
    invoked = [c for c in cmds if re.search(r'\.venv/bin/python" -B tools/(prove|check_probe|make_instances|run_report|settle|vfrun)\.py ', c)]
    checks["run_store_path_is_on_every_command_that_needs_it"] = len(invoked) >= 12 and all(
        f'--store {PILOT}/store"' in c or f'--store {ROLLOUTS}/store"' in c or f'--pilot {ROLLOUTS}"' in c for c in invoked)

    # ---- round 3: exact matching of the pilot's processes (m2), cut output (m1) ----
    joined = "\n".join(cmds)
    status = [c for c in cmds if 'echo "processes:"' in c]
    stop = [c for c in cmds if "kill -TERM PID_FROM_THE_STATUS_LINE" in c]
    lits = lambda c: re.findall(r'index\(r, ((?:"[^"]*"|p| )+)\) == 1', c)  # noqa: E731
    want = ['"-B tools/prove.py "', '"-B tools/check_probe.py "', '"-B tools/vfrun.py "', '"-B " p "/tools/vfeval.py @ "', '"-m physim2_env.lab_tools"',
            '"-B " p "/tools/make_instances.py "', '"-B tools/make_instances.py "', '"-B " p "/tools/build_reference.py "']
    ev["process_matching"] = {"status_commands": len(status), "stop_commands": len(stop), "literals_of_the_stop_command": lits(stop[0]) if stop else None}
    checks["r3_processes_are_matched_letter_for_letter_not_by_a_pattern_of_the_path"] = len(status) == 2 and len(stop) == 1 \
        and all(lits(c) == want + ['"-c"'] for c in status) and lits(stop[0]) == want \
        and all(f'awk -v p="{PLACE}" ' in c and 'py = p "/.venv/bin/python "' in c for c in status + stop) \
        and not re.search(r'grep -E "\^[^"]*\.venv', joined) and "pgrep" not in joined
    checks["r3_the_stop_command_signals_only_after_its_own_comparison"] = bool(stop) and stop[0].count("kill") == 1 \
        and re.search(r"ps -ww -p PID_FROM_THE_STATUS_LINE -o command= \| awk .* END \{ exit !ok \}' && kill -TERM PID_FROM_THE_STATUS_LINE$", stop[0]) is not None
    checks["r3_process_lines_are_cut_at_160_characters_and_no_command_carries_theta"] = all(c.count("substr($0, 1, 160)") == 1 for c in status + stop) \
        and "--theta" not in joined and "cut -c 1-200" in status[0]
    # ---- round 3: the session's own environment and engine (M1) ----
    sys.path.insert(0, HERE)
    import vfrun
    envcheck = [c for c in cmds if "env | cut -d= -f1 | awk" in c]
    checks["r3_step_0_checks_the_sessions_own_environment_with_the_tools_own_list"] = len(envcheck) == 1 and f"awk '/{vfrun.ENV_REFUSE.pattern}/ " in envcheck[0] \
        and "docker context show && docker context inspect --format '{{.Endpoints.docker.Host}}'" in envcheck[0]
    assigns = sorted(set(re.findall(r"(?:^|[\s(;&])([A-Z][A-Z0-9_]*)=", joined)))
    ev["variables_set_on_commands"] = assigns
    checks["r3_no_command_sets_a_variable_but_the_run_label"] = assigns == ["VF_RUN_ID"]
    checks["r3_vf_eval_is_never_started_by_a_command_of_the_runbook"] = "bin/vf-eval" not in joined and not re.search(r'python" -B [^ ]*vfeval\.py', joined)
    # ---- round 3: counts that fail loudly (m11), links (m3), the label re-check (m6) ----
    checks["r3_no_count_can_hide_a_failed_command"] = "| wc -l" not in joined and joined.count("grep -c") == 0 \
        and all(k in joined for k in ('&& echo "TREE-LISTED"', '&& echo "CONTAINERS-LISTED"', '&& echo "IMAGES-LISTED"', '&& echo "NO-PILOT-FOLDERS"', '&& echo "RUNNING-LISTED"'))
    rm = [c for c in cmds if re.search(r"\brm -rf\b", c)]
    nolink = f'test ! -L {PILOT}" && test ! -L {PILOT}/store" && test ! -L {PILOT}/scratch" && '
    checks["r3_no_rm_rf_follows_a_linked_pilot_folder"] = len(rm) == 2 and all(nolink in c.split("rm -rf")[0] for c in rm) \
        and f'test ! -e {PILOT}" && test ! -L {PILOT}"' in joined and f'test ! -e {ROLLOUTS}" && test ! -L {ROLLOUTS}"' in joined
    drm = [c for c in cmds if "docker rm" in c]
    checks["r3_docker_rm_reads_the_label_back_first"] = len(drm) == 1 and drm[0].endswith(
        "docker inspect --format '{{index .Config.Labels \"verifiers.run\"}}' NAME_FROM_THE_STATUS_LINE | command grep -Fx " + LABEL + " && docker rm -f NAME_FROM_THE_STATUS_LINE")
    # ---- round 3: the disk floor (D1), other containers (m7), the build cache (m10) ----
    gate = "df -Pk \"$HOME\" | awk 'NR == 2 { free = $4 } END { if (free >= 8388608) exit 0 ; print \"refused: under 8 GiB free on the file system of the home folder\" ; exit 1 }' && "
    gated = [c for c in cmds if gate in c]
    checks["r3_disk_floor_is_on_every_start"] = all("--disk-floor-gib 8" in c for c in real + vfrun_cmds) and len(gated) == 4 \
        and all(any(k in c for c in gated) for k in ("--dry-run 2>&1 | command grep", "nohup uv sync", "nohup docker build")) \
        and any("DISK-OK" in c and "8388608" in c for c in cmds) and "**You never\n   make room:**" in text and "EXIT 97" in text
    quiet = [c for c in cmds if c.endswith("docker ps --format '{{.Names}} {{.Image}}' && echo \"RUNNING-LISTED\"")]
    checks["r3_no_other_container_runs_during_step_2"] = len(quiet) == 1 and text.index(quiet[0]) < text.index("### 2a.") \
        and "every request needs the rollout's bearer" in text and text.count("RUNNING-LISTED") >= 4
    checks["r3_build_cache_is_in_the_inventory_and_in_step_4"] = "the build cache of those two builds" in text and any(c.endswith("&& docker system df") for c in cmds) \
        and "docker builder\nprune" in text

    # ---- change 6: the text ----
    banned = {"export": r"\bexport ", "sudo": r"\bsudo\b", "pkill / killall": r"(^|[\s;&|(])(pkill|killall)\s", "prune": r"\bprune\b", "--clean": r"--clean\b",
              "command substitution": r"\$\(|`", "a mount option": r"docker [^|;&\n]*\s(-v|--volume|--mount)(\s|=)", "docker socket": r"docker\.sock",
              "removal by filter": r"docker (rm|rmi)[^\n]*(--filter|-q)", "kill -9 or -1": r"kill\s+(-9|-KILL|-1)\b", "docker_shim": r"docker_shim",
              "a variable as a path": r"\$\{?(STUDY|S|DIR|ROOT|V)\b"}
    found = {k: bool(re.search(v, joined)) for k, v in banned.items()}
    ev["banned_in_commands"] = found
    checks["text_no_banned_construct_in_any_command"] = not any(found.values())
    want_rm = f'rm -rf {PILOT}/store" {PILOT}/scratch"'
    checks["text_every_rm_rf_is_chained_behind_its_checks_and_names_the_two_pilot_folders"] = len(rm) == 2 and all(
        c.count("rm -rf") == 1 and f'test -f {PILOT}/store/index.json" && test -d {PILOT}/scratch"' in c.split("rm -rf")[0]
        and re.search(r"&& rm -rf ", c) and want_rm in c and "\n" not in c and ";" not in c.replace(gate, "") for c in rm)
    checks["text_step_4_copies_the_results_out_before_it_deletes"] = any("cp " in c.split("rm -rf")[0] and "physim2-pilot-r5-results" in c.split("rm -rf")[0]
                                                                        and "test -s " in c.split("rm -rf")[0] for c in rm)
    checks["text_the_shared_image_is_kept"] = "docker rmi" not in joined and "is not this pilot's to\nremove" in text
    never = ("`sudo`", "`docker run` with `-v`, `--mount`", "pasting the route's own commands", "`physim2_env/public/_item.py`", "`agents/*.py`",
             "`redteam/`", "round5/agentenv", "`pkill`, `killall`", "another harness", "`tools/docker_shim`", "`tools/check_units.py`",
             "`.venv/bin/vf-eval`, `tools/vfeval.py`", "opening `~/.prime/config.json`", "deleting anything to make room", "`docker context use`")
    checks["text_the_never_table_is_there"] = all(k in text for k in never)
    inventory = ("What is signalled or killed on the Mac", "What is deleted on the Mac", "What is written and left on the Mac", "What listens on the Mac",
                 "~/.cache/verifiers/runtimes/subprocess", "/tmp/vf-port-", "What is replaced in place", "SIGTERM",
                 "The model key (step 3 only): who holds it, and for how long", "A box cannot write to Docker's disk", "api.pinference.ai",
                 "What reaches those processes from your session", "at every stop of vf-eval", "verifiers' interception server", "io.sock", "git rev-parse",
                 "No model credential in steps 0 to 2", "**Not on macOS:**", "reference_C.theta.json")
    checks["text_the_inventory_is_there"] = all(k in text for k in inventory)
    checks["text_stop_rule_and_the_known_macos_exception"] = "Stop rule" in text and "stop and report" in text.lower() \
        and '"failed_new": ["b_lab_process_dropped_it_after_loading"]' in text
    checks["text_no_certificate_file_is_made"] = "extra-ca.crt" not in joined
    checks["text_the_six_points_of_the_round_3_notice_are_in_the_body"] = all(k in text for k in (
        "Before 2a, again before 2b, and again before 2c", "After a stop that does not end in point 6", "docker rm --force <its box>",
        "~/.docker/buildx/", "at least 11 GiB free", "except the image build and its status"))
    checks["text_the_three_rules_of_the_round_2_notice_are_in_the_body"] = "60 minutes have passed since the start" in text \
        and "treat the interruption as\nthe second one" in text and "may or may not be listed" in text

    # ---- change 9: step 3 ----
    paid = [c for c in real if "--stage rollout" in c]
    i_paid = text.index(paid[0].splitlines()[0]) if paid else -1
    before, after = text[:i_paid], text[i_paid:]
    checks["step3_the_paid_command_stands_alone_under_a_stop_line_with_the_price"] = len(paid) == 1 and before.rstrip().endswith("```sh") \
        and "STOP. THE NEXT COMMAND SPENDS MONEY" in before[-2500:] and "bound_on_the_bill_usd" in before[-2500:] \
        and "cap_usd`\nplus one worst-case call" in text and "is at least one worst-case call" in text
    checks["step3_output_goes_to_a_file_and_is_never_displayed"] = bool(paid) and "rollout.log\" 2>&1 < /dev/null" in paid[0] and "Never display `rollout.log`" in after \
        and "cut -c 1-12" in text
    order = ["tools/check_request.py --fetch", "--shared-ledger " + ROLLOUTS + '/shared-ledger.json" --prices', "--stage instance", "--stage reference",
             "--stage dry-run", "STOP. THE NEXT COMMAND SPENDS MONEY", "--stage rollout --shared-ledger", "tools/run_report.py --store " + ROLLOUTS,
             "tools/pack_rollout.py --request"]
    three = text[text.index("## 3. Model rollouts"):text.index("## 4. After the pilot")] if "## 3. Model rollouts" in text else ""
    at = [three.find(k) for k in order]
    ev["step3_order"] = dict(zip(order, at))
    checks["step3_the_stages_stand_in_their_order"] = all(i >= 0 for i in at) and at == sorted(at)
    sys.path.insert(0, HERE)
    import check_request as CR
    m3 = re.search(r"<!-- STEP3-FACTS-BEGIN -->\n```json\n(.*?)\n```\n<!-- STEP3-FACTS-END -->", text, re.S)
    try:
        facts_same = m3 is not None and json.loads(m3.group(1)) == json.loads(json.dumps(CR.facts()))
    except ValueError:
        facts_same = False
    checks["step3_the_block_of_facts_is_what_the_code_prints"] = facts_same
    checks["step3_every_request_command_names_the_job_by_its_placeholder"] = all(
        (f'--request {ROLLOUTS}/requests/JOB_ID.json" --pilot {ROLLOUTS}"' in c) != ("--fetch" in c) for c in cmds
        if re.search(r'python" -B tools/(vfrun|check_request|pack_rollout)\.py ', c) and "--config configs/" not in c) \
        and "A step-3 placeholder is replaced only by" in text
    checks["step3_the_crash_cleanup_is_in_the_interrupted_section"] = "what a crash in the middle of a model rollout leaves behind" in text \
        and "--stage close --disk-floor-gib 8" in joined and "One job at a time" in text
    checks["step3_the_run_is_read_through_the_report_tool"] = "tools/run_report.py" in after and os.path.isfile(os.path.join(HERE, "run_report.py"))
    checks["step3_no_other_harness_is_offered"] = "claude_code" not in text and "codex" not in text
    checks["step3_own_go"] = "SEPARATE GO" in text and 'Not released by a notice that says "steps 0 to 2"' in text \
        and "You create it ONLY when the lead tells you to in this session" in text
    checks["step3_model_credentials_only_on_the_paid_command_behind_the_leads_file"] = joined.count("--model-credentials prime") == 1 \
        and bool(paid) and "--model-credentials prime" in paid[0] and f'test -f {ROLLOUTS}/LEAD-GO-MODEL-SPEND.json" && ' in paid[0]

    # ---- change 7: the pin ----
    m = re.search(r"<!-- PIN-BEGIN -->(.*?)<!-- PIN-END -->", text, re.S)
    pin_block = m.group(1) if m else ""
    pin_file = os.path.join(ROOT, "PIN.sha256")
    pin_hash = hashlib.sha256(open(pin_file, "rb").read()).hexdigest() if os.path.isfile(pin_file) else None
    commit = re.search(r"\b[0-9a-f]{40}\b", pin_block)
    chk = subprocess.run([sys.executable, "-B", os.path.join(HERE, "pin.py"), "--check"], capture_output=True, text=True)
    ev["pin"] = {"sha256_of_PIN.sha256": pin_hash, "named_in_the_pin_block": bool(pin_hash and pin_hash in pin_block),
                 "commit_named": commit.group(0) if commit else None, "pin.py --check": chk.stdout.strip().splitlines()[:5], "files_listed": None}
    if pin_hash:
        ev["pin"]["files_listed"] = len(open(pin_file).read().splitlines())
    # ---- round 5: the Mac session's rulings (COORD, 11 Nov) ----
    checks["r5_every_grep_of_a_command_is_command_grep"] = all(re.sub(r"command grep", "", c).count("grep") == 0 for c in cmds) \
        and sum(c.count("command grep") for c in cmds) >= 3
    old_names = [c for c in cmds if "physim2-pilot-20261110" in c or "physim2-ring:2" in c]
    checks["r5_names_of_this_round_only"] = len(old_names) == 1 and "EARLIER PINS, HARMLESS:" in old_names[0] \
        and "rm " not in old_names[0] and "docker rmi" not in old_names[0] and "-t physim2-ring:3 docker/" in joined \
        and all("physim2-pilot-r5" in c for c in cmds if "VF_RUN_ID=" in c)
    checks["r5_the_dry_run_refuses_a_python_that_is_not_uvs_own"] = any(
        "--managed-python --dry-run" in c and "interpreter at:/ { print \"refused: uv chose a Python that is not its own\" }" in c for c in cmds) \
        and all("--managed-python" in c for c in cmds if re.search(r"(^|[ &|;(])uv ", c))
    checks["r5_step3_names_the_50_dollars_and_reads_exit_2_both_ways"] = text.count("at most **$50**") == 2 and "go on with 3g and 3h in both cases" in text \
        and "**Before each job (T19): the first two commands of step 0**" in text and "(point 8 does not apply: no model was called)" in text
    checks["pin_block_names_the_hash_of_PIN_sha256"] = bool(pin_hash) and pin_hash in pin_block
    checks["pin_file_matches_the_files_on_disk"] = chk.returncode == 0
    checks["pin_commands_compare_commit_and_hashes"] = f'git rev-parse HEAD && pwd -P | command grep -Fx "{PLACE}" && git --no-optional-locks status --porcelain --ignored' in joined \
        and "shasum -a 256 PIN.sha256 && shasum -a 256 -c PIN.sha256 > /dev/null && echo PIN-OK" in joined and "git checkout --detach" in text
    if commit:                                               # the copy at the head of the branch
        r = subprocess.run(["git", "cat-file", "-t", commit.group(0)], cwd=ROOT, capture_output=True, text=True)
        same = subprocess.run(["git", "show", f"{commit.group(0)}:./PIN.sha256"], cwd=ROOT, capture_output=True)
        there = subprocess.run(["git", "show", f"{commit.group(0)}:./RUNBOOK_MAC.md"], cwd=ROOT, capture_output=True, text=True)
        strip = lambda t: re.sub(r"<!-- PIN-BEGIN -->.*?<!-- PIN-END -->", "", t, flags=re.S)  # noqa: E731
        ev["pin"]["pinned_commit_is_a_commit"] = r.stdout.strip() == "commit"
        ev["pin"]["PIN.sha256_in_the_pinned_commit_is_this_one"] = hashlib.sha256(same.stdout).hexdigest() == pin_hash
        ev["pin"]["runbook_in_the_pinned_commit_differs_in_the_pin_block_only"] = strip(there.stdout) == strip(text)
        checks["pin_names_one_commit_that_holds_this_PIN_sha256"] = ev["pin"]["pinned_commit_is_a_commit"] and ev["pin"]["PIN.sha256_in_the_pinned_commit_is_this_one"]
        checks["pin_runbook_in_the_pinned_commit_differs_in_the_pin_block_only"] = ev["pin"]["runbook_in_the_pinned_commit_differs_in_the_pin_block_only"]
    first = text.splitlines()[2]
    go = [g for g in ("**GO for steps 0 to 2.**", "**GO for steps 0 to 3.**") if first.startswith(g)]
    ev["notice"] = "ON HOLD" if first.startswith("**ON HOLD") else (go[0].strip("*. ") if go else "?")
    checks["hold"] = first.startswith("**ON HOLD") or bool(go)
    out = {"what": "RUNBOOK_MAC.md checked as text (required changes 1, 2, 6, 7, 9 of HOST_SAFETY_AUDIT.md) and its guard run with echo in place "
                   "of the command; no command of the runbook was run by this tool",
           "evidence_label": "read (text checks); run (the guard line: cd, test, echo only)",
           "copy": "head of the branch (a commit is named)" if commit else "the pinned commit's own copy (no commit named)",
           "n_checks": len(checks), "n_passed": sum(v is True for v in checks.values()), "failed": [k for k, v in checks.items() if v is not True],
           "checks": checks, "evidence": ev}
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    json.dump(out, open(a.out, "w"), indent=1)
    print(json.dumps({k: out[k] for k in ("copy", "n_checks", "n_passed", "failed")}))


if __name__ == "__main__":
    main()
