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
  step3_*    (change 9) the paid command stands alone between STOP lines, writes to a file, is read through
             tools/run_report.py only; no `claude_code` / `codex`
  hold       the first lines say ON HOLD

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
LABEL = "physim2-pilot-20261110"
PILOT = '"$HOME/physim2-pilot-20261110'


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
    starts = [c for c in cmds if re.search(r"tools/(prove|check_probe)\.py|bin/vf-eval\"", c)]
    dry = [c for c in starts if "--dry-run" in c]
    real = [c for c in starts if "--dry-run" not in c]
    ev["commands_that_start_a_rollout"] = [re.sub(r"\s+", " ", c[len(GUARD):])[:110] for c in real]
    checks["run_every_rollout_command_carries_the_run_label"] = len(real) == 4 and all(f"VF_RUN_ID={LABEL} " in c for c in starts)
    checks["run_every_rollout_command_is_detached_with_a_log_and_an_exit_line"] = all(
        "{ ( " in c and "nohup " in c and c.rstrip().endswith("> /dev/null 2>&1 < /dev/null & }") and 'echo "EXIT $?" >>' in c and ".log\" 2>&1 < /dev/null" in c
        for c in real)
    checks["run_every_detached_command_has_a_docker_info_gate"] = all("docker info --format '{{.ServerVersion}}' && { ( " in c for c in cmds if "nohup " in c)
    checks["run_the_dry_run_is_alone_in_its_block"] = len(dry) == 1 and dry[0].count("vf-eval") == 1
    ps = [c for c in cmds if "docker ps" in c]
    checks["run_containers_are_listed_by_the_run_label_only"] = len(ps) >= 4 and all(f"--filter label=verifiers.run={LABEL}" in c for c in ps) \
        and "name=vf-" not in "\n".join(cmds)
    checks["run_if_interrupted_section"] = all(k in text for k in ("## If a run was interrupted", "kill -TERM PID_FROM_THE_STATUS_LINE",
                                                                  "docker rm -f NAME_FROM_THE_STATUS_LINE", "pilot folders reset", "make_instances"))
    checks["run_processes_are_listed_by_this_checkouts_own_environment"] = text.count(f'grep "{PLACE}/.venv/bin/[p]ython"') >= 2
    checks["run_store_path_is_on_every_command_that_needs_it"] = all(f'--store {PILOT}/store"' in c for c in cmds if re.search(r"tools/(prove|check_probe|make_instances|run_report|settle)\.py", c)) \
        and all(f'PHYSIM2_STORE={PILOT}/store"' in c for c in cmds if 'bin/vf-eval"' in c)

    # ---- change 6: the text ----
    joined = "\n".join(cmds)
    banned = {"export": r"\bexport ", "sudo": r"\bsudo\b", "pkill / killall": r"(^|[\s;&|(])(pkill|killall)\s", "prune": r"\bprune\b", "--clean": r"--clean\b",
              "command substitution": r"\$\(|`", "a mount option": r"(^|\s)(-v|--volume|--mount)(\s|=)", "docker socket": r"docker\.sock",
              "removal by filter": r"docker (rm|rmi)[^\n]*(--filter|-q)", "kill -9 or -1": r"kill\s+(-9|-KILL|-1)\b", "docker_shim": r"docker_shim",
              "a variable as a path": r"\$\{?(STUDY|S|DIR|ROOT|V)\b"}
    found = {k: bool(re.search(v, joined)) for k, v in banned.items()}
    ev["banned_in_commands"] = found
    checks["text_no_banned_construct_in_any_command"] = not any(found.values())
    rm = [c for c in cmds if re.search(r"\brm -rf\b", c)]
    want_rm = f'rm -rf {PILOT}/store" {PILOT}/scratch"'
    checks["text_every_rm_rf_is_chained_behind_its_checks_and_names_the_two_pilot_folders"] = len(rm) == 2 and all(
        c.count("rm -rf") == 1 and f'test -f {PILOT}/store/index.json" && test -d {PILOT}/scratch"' in c.split("rm -rf")[0]
        and re.search(r"&& rm -rf ", c) and want_rm in c and "\n" not in c and ";" not in c for c in rm)
    checks["text_step_4_copies_the_results_out_before_it_deletes"] = any("cp " in c.split("rm -rf")[0] and "physim2-pilot-20261110-results" in c.split("rm -rf")[0]
                                                                        and "test -s " in c.split("rm -rf")[0] for c in rm)
    checks["text_the_shared_image_is_kept"] = "docker rmi" not in joined and "is not this pilot's to remove" in text
    never = ("`sudo`", "`docker run` with `-v`, `--mount`", "pasting the route's own commands", "`physim2_env/public/_item.py`", "`agents/*.py`",
             "`redteam/`", "round5/agentenv", "`pkill`, `killall`", "another harness", "`tools/docker_shim`", "`tools/check_units.py`")
    checks["text_the_never_table_is_there"] = all(k in text for k in never)
    inventory = ("What is signalled or killed on the Mac", "What is deleted on the Mac", "What is written and left on the Mac", "What listens on the Mac",
                 "~/.cache/verifiers/runtimes/subprocess", "/tmp/vf-port-", "docker/extra-ca.crt", "SIGTERM")
    checks["text_the_inventory_is_there"] = all(k in text for k in inventory)
    checks["text_stop_rule_and_the_known_macos_exception"] = "Stop rule" in text and "stop and report" in text.lower() \
        and '"failed_new": ["b_lab_process_dropped_it_after_loading"]' in text
    checks["text_extra_ca_is_created_only_if_absent"] = "(test -e docker/extra-ca.crt || : > docker/extra-ca.crt)" in joined

    # ---- change 9: step 3 ----
    paid = [c for c in real if "qwen_ring_bash.toml" in c]
    i_paid = text.index(paid[0].splitlines()[0]) if paid else -1
    before, after = text[:i_paid], text[i_paid:]
    checks["step3_the_paid_command_stands_alone_under_a_stop_line_with_the_price"] = len(paid) == 1 and before.rstrip().endswith("```sh") \
        and "STOP. THE NEXT COMMAND SPENDS MONEY" in before[-2500:] and "1.5 x p_in + 0.06 x p_out" in before[-2500:] and "bound = ______" in before[-2500:]
    checks["step3_output_goes_to_a_file_and_is_never_displayed"] = bool(paid) and "qwen.log\" 2>&1 < /dev/null" in paid[0] and "Never display `qwen.log`" in after \
        and "cut -c 1-12" in after
    checks["step3_the_run_is_read_through_the_report_tool"] = "tools/run_report.py" in after and os.path.isfile(os.path.join(HERE, "run_report.py"))
    checks["step3_no_other_harness_is_offered"] = "claude_code" not in text and "codex" not in text
    checks["step3_disk_limit_and_own_hold"] = "virtual disk limit is below the Mac's free disk space" in text.replace("\n", " ") and "SEPARATE HOLD" in text \
        and "NO-GO until steps 0 to 2 have passed on this Mac" in text

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
    checks["pin_block_names_the_hash_of_PIN_sha256"] = bool(pin_hash) and pin_hash in pin_block
    checks["pin_file_matches_the_files_on_disk"] = chk.returncode == 0
    checks["pin_commands_compare_commit_and_hashes"] = "git rev-parse HEAD && git status --porcelain" in joined \
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
    checks["hold"] = text.splitlines()[2].startswith("**ON HOLD. Run nothing from this file.**")
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
