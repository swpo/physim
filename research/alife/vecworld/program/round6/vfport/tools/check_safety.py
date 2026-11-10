"""check_safety -- the HOST-side tests of the host-safety audit (HOST_SAFETY_AUDIT.md, section 4), run so that
they cannot harm the machine they run on.

Before this file imports anything of the package, every primitive through which Python code can kill a process,
delete, move, re-own or re-mode a file, change identity or start a program is replaced by a tripwire that records
the attempt and raises (tools/tripwires.py: 60 names of os, shutil, subprocess and pathlib). Nothing here starts
a process, a container or the item driver's cleanup; the real cleanup is tested inside a throwaway container
only (tools/check_driver.py), the real signal inside one too (tools/check_interrupt.py).

Each check is a named boolean with its evidence:

  R2  vfrun stops vf-eval with SIGTERM first: a recording stand-in for the process (no process is started) under
      timeout=1 sees SIGTERM and no SIGKILL; one that ignores SIGTERM sees SIGKILL only after the grace period;
      a stop request to the tool itself is passed on as SIGTERM. The tools refuse to start without VF_RUN_ID.
  R3  agents/hostile_submission.py, agents/probe_grading.py and redteam/agent_rt.py, started here in every mode
      through runpy: each ends in SystemExit("refused: ...") before it imports or touches anything, also when
      only one of the two signs of a box is present.
  R4  the mount allow-list as a pure function on stored mount tables (tools/fixtures/mounts); an unreadable table
      raises instead of falling back to "/"; the driver has no rmtree; on this machine every function that kills,
      deletes or changes a mode refuses with the route variable set; the wipe, with its guard switched off for
      the test and its inputs faked, reaches unlink for the deepest listed path first and never a mount point.
  R5  recording stand-ins for a verifiers runtime (typed "docker", typed "subprocess", a subclass of the real
      class, the real class borrowed or not started) receive ZERO commands from grading.stage, grading.run_request,
      Physim2Task._public_files, Physim2Task.setup, BoxAccess.check / announce / collect_frozen and the scripted
      harness.
  S1  the guard as a pure function: uid range 20000-59999 (1000 refused), a root caller, the mounts; --uid has
      no default; outside a box the driver and the validator run nothing.

usage: PHYSIM2_DEV_MACHINE=cloud-container python -B tools/check_safety.py --out results/safety_host.json
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import tripwires  # noqa: E402

TW = tripwires.install()                                     # BEFORE any code of the package is imported
N_WIRES = len(TW.names)

import argparse  # noqa: E402
import ast  # noqa: E402
import asyncio  # noqa: E402
import contextlib  # noqa: E402
import importlib.util  # noqa: E402
import io  # noqa: E402
import json  # noqa: E402
import runpy  # noqa: E402
import signal  # noqa: E402
import subprocess  # noqa: E402
import tempfile  # noqa: E402
import types  # noqa: E402

if sys.platform != "linux" or os.environ.get("PHYSIM2_DEV_MACHINE") != "cloud-container":
    raise SystemExit("check_safety.py is a development check for the Linux build container. It is NOT part of the Mac runbook: "
                     "do not run it on a personal machine. In the build container: PHYSIM2_DEV_MACHINE=cloud-container python "
                     "tools/check_safety.py --out ...")
ap = argparse.ArgumentParser()
ap.add_argument("--out", required=True)
a = ap.parse_args()
sys.path.insert(0, ROOT)
checks, evidence = {}, {}
TMP = tempfile.mkdtemp(prefix="physim2-safety-")             # this test's own files; removed at the end, after restore()


def hits():
    return [h[0] + " " + h[1] for h in TW.take()]


def short(why):
    """Guard reasons without the layout of this machine: of the foreign mounts only the first and a count."""
    out = []
    for w in why:
        head, sep, tail = w.partition("does not have: ")
        out.append(head + sep + tail.split(", ")[0] + (f" and {len(tail.split(', ')) - 1} more" if ", " in tail else "") if sep else w)
    return out


# ============================================================================= R2: SIGTERM before SIGKILL
import vfrun  # noqa: E402


class FakeProc:
    """A stand-in for subprocess.Popen that starts nothing and records what is done to it."""
    made = []

    def __init__(self, cmd, **kw):
        self.cmd, self.kw, self.log, self.returncode = list(cmd), kw, [], None
        self.obeys_sigterm, self.raise_in_communicate = FakeProc.obeys, FakeProc.raises
        FakeProc.made.append(self)

    def communicate(self, timeout=None):
        self.log.append(f"communicate(timeout={timeout})")
        if self.raise_in_communicate is not None and self.returncode is None:
            exc, self.raise_in_communicate = self.raise_in_communicate, None
            raise exc
        if timeout is not None and self.returncode is None:
            raise subprocess.TimeoutExpired(self.cmd, timeout)
        return "", ""

    def poll(self):
        return self.returncode

    def send_signal(self, sig):
        self.log.append("send_signal(" + signal.Signals(sig).name + ")")
        if sig == signal.SIGTERM and self.obeys_sigterm:
            self.returncode = 130

    def wait(self, timeout=None):
        self.log.append("wait" if timeout is None else "wait(timeout)")
        if self.returncode is None:
            raise subprocess.TimeoutExpired(self.cmd, timeout)
        return self.returncode

    def kill(self):
        self.log.append("kill(SIGKILL)")
        self.returncode = -9


def fake_run(obeys=True, raises=None, **kw):
    FakeProc.made, FakeProc.obeys, FakeProc.raises = [], obeys, raises
    real = subprocess.Popen                                  # the tripwire
    subprocess.Popen = FakeProc
    try:
        out = vfrun.run_child(["vf-eval-stub"], env={}, cwd=TMP, **kw)
        err = None
    except BaseException as e:                               # noqa: BLE001 - KeyboardInterrupt is one of the cases
        out, err = None, type(e).__name__
    finally:
        subprocess.Popen = real
    return {"returned": None if out is None else {"returncode": out[0], "ended": out[3]}, "raised": err,
            "calls_on_the_process": FakeProc.made[0].log if FakeProc.made else [], "processes_made": len(FakeProc.made),
            "tripwires_reached": hits()}


term_before = signal.getsignal(signal.SIGTERM)
r2 = {"timeout_1_obedient_stub": fake_run(timeout=1, grace=5),
      "timeout_1_stub_that_ignores_sigterm": fake_run(obeys=False, timeout=1, grace=0.05),
      "tool_itself_told_to_stop": fake_run(raises=KeyboardInterrupt(), timeout=1, grace=5),
      "normal_exit": None}
FakeProc.made, FakeProc.obeys, FakeProc.raises = [], True, None
_p = FakeProc(["x"])
_p.returncode = 0
r2["stop_child_on_a_process_that_has_exited"] = {"result": vfrun.stop_child(_p), "calls_on_the_process": _p.log}
r2.pop("normal_exit")
evidence["R2"] = r2
t1, t2, t3 = r2["timeout_1_obedient_stub"], r2["timeout_1_stub_that_ignores_sigterm"], r2["tool_itself_told_to_stop"]
checks["R2_timeout_sends_sigterm_and_no_sigkill"] = t1["calls_on_the_process"] == ["communicate(timeout=1)", "send_signal(SIGTERM)", "wait(timeout)",
                                                                                 "communicate(timeout=None)"] and t1["raised"] is None
checks["R2_sigkill_only_after_sigterm_and_the_grace_period"] = t2["calls_on_the_process"][:4] == ["communicate(timeout=1)", "send_signal(SIGTERM)",
                                                                                                  "wait(timeout)", "kill(SIGKILL)"]
checks["R2_a_stop_request_to_the_tool_is_passed_on_as_sigterm"] = t3["raised"] == "KeyboardInterrupt" \
    and t3["calls_on_the_process"][1:3] == ["send_signal(SIGTERM)", "wait(timeout)"] and "kill(SIGKILL)" not in t3["calls_on_the_process"]
checks["R2_an_exited_process_is_not_signalled"] = r2["stop_child_on_a_process_that_has_exited"] == {"result": "had exited", "calls_on_the_process": []}
checks["R2_sigterm_handler_of_this_process_restored"] = signal.getsignal(signal.SIGTERM) is term_before
# run_eval end to end with the stand-in: the label is required, Docker must answer, timeout=1 ends in SIGTERM
saved_env = os.environ.pop("VF_RUN_ID", None)
try:
    vfrun.run_eval("stub-run", store=TMP, out_dir=os.path.join(TMP, "runs"), harness={}, timeout=1)
    no_label = "RETURNED"
except SystemExit as e:
    no_label = str(e)[:60]
r2["run_eval_without_VF_RUN_ID"] = {"outcome": no_label, "tripwires_reached": hits(), "out_dir_created": os.path.exists(os.path.join(TMP, "runs"))}
os.environ["VF_RUN_ID"] = "physim2-safety-test"
try:
    vfrun.run_eval("stub-run", store=TMP, out_dir=os.path.join(TMP, "runs"), harness={}, timeout=1)
    no_docker = "RETURNED"
except SystemExit as e:
    no_docker = str(e)[:60]
except tripwires.Tripped as e:
    no_docker = str(e)
r2["run_eval_docker_check_is_a_subprocess"] = {"outcome": no_docker, "tripwires_reached": hits()}
real_docker, real_popen = vfrun.require_docker, subprocess.Popen
vfrun.require_docker = lambda: "stand-in"
FakeProc.made, FakeProc.obeys, FakeProc.raises = [], True, None
subprocess.Popen = FakeProc
try:
    res = vfrun.run_eval("stub-run", store=TMP, out_dir=os.path.join(TMP, "runs"), harness={}, timeout=1)
finally:
    subprocess.Popen, vfrun.require_docker = real_popen, real_docker
    if saved_env is None:
        os.environ.pop("VF_RUN_ID", None)
    else:
        os.environ["VF_RUN_ID"] = saved_env
r2["run_eval_timeout_1"] = {"ended": res["ended"], "run_label": res["run_label"], "command": [os.path.basename(c) for c in FakeProc.made[0].cmd[:4]],
                            "calls_on_the_process": FakeProc.made[0].log, "tripwires_reached": hits()}
checks["R2_tools_refuse_to_start_without_a_run_label"] = no_label.startswith("VF_RUN_ID is not set") and not r2["run_eval_without_VF_RUN_ID"]["out_dir_created"]
checks["R2_run_eval_under_timeout_1_records_sigterm"] = "send_signal(SIGTERM)" in r2["run_eval_timeout_1"]["calls_on_the_process"] \
    and "kill(SIGKILL)" not in r2["run_eval_timeout_1"]["calls_on_the_process"] and res["run_label"] == "physim2-safety-test"

# ============================================================================= R3: the box scripts refuse here
MODES = {
    "agents/hostile_submission.py": [[m] for m in ("delete", "empty", "oversize", "huge", "symlinks", "no_tar", "junk", "tar_duplicate", "tar_collision",
                                                   "tar_longpath", "raw_submit_broken", "fake_validator", "unsubmitted_nondeterministic",
                                                   "unsubmitted_partly_working", "submit_cap", "exit1", "killall", "item_overflow", "item_fifo",
                                                   "item_bomb", "item_extreme", "no-such-mode")] + [[]],
    "agents/probe_grading.py": [["--host-port", "9"], []],
    "redteam/agent_rt.py": [["recon", "--host-port", "9", "--sibling", "127.0.0.1:9"], ["overflow"], ["fifo"], ["hedge", "--rule", "True"],
                            ["hostile", "exit1"], ["hostile", "killall"], ["hostile", "hangtar"], ["hostile", "sigkill"], []],
}


def start(script, args):
    """Run a script as __main__ in this process. Returns (how it ended, tripwires reached, modules it imported)."""
    argv, cwd, mods = list(sys.argv), os.getcwd(), set(sys.modules)
    sys.argv = [os.path.join(ROOT, script), *args]
    os.chdir(TMP)
    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
            runpy.run_path(os.path.join(ROOT, script), run_name="__main__")
        end = "RAN TO THE END"
    except SystemExit as e:
        end = "SystemExit: " + str(e.code)[:70]
    except BaseException as e:                               # noqa: BLE001
        end = type(e).__name__ + ": " + str(e)[:70]
    finally:
        sys.argv = argv
        os.chdir(cwd)
    return end, hits(), sorted(set(sys.modules) - mods)


open(os.path.join(TMP, "warm.py"), "w").write("pass\n")
runpy.run_path(os.path.join(TMP, "warm.py"), run_name="__main__")   # whatever runpy itself imports is imported now
box_signs = {"/.dockerenv": os.path.exists("/.dockerenv"), "/etc/physim2/predictor_uid": os.path.lexists("/etc/physim2/predictor_uid")}
r3 = {"this_machine": box_signs, "runs": {}}
for script, modes in MODES.items():
    for args in modes:
        end, reached, imported = start(script, args)
        r3["runs"][f"{script} {' '.join(args)}".strip()] = {"ended": end, "tripwires_reached": reached, "modules_imported": imported}
# one sign of a box only (simulated by answering for ONE path; both together are never simulated on a host)
real_exists, real_lstat = os.path.exists, os.lstat
fake_stat = os.stat_result((0o100644, 1, 1, 1, 0, 0, 6, 0, 0, 0))    # a regular file owned by root
half = {}
for script in MODES:
    os.path.exists = lambda p, _r=real_exists: True if p == "/.dockerenv" else _r(p)
    try:
        half[f"{script}: /.dockerenv only"] = start(script, MODES[script][0])[:2]
    finally:
        os.path.exists = real_exists
    os.lstat = lambda p, *x, _r=real_lstat, **k: fake_stat if p == "/etc/physim2/predictor_uid" else _r(p, *x, **k)
    try:
        half[f"{script}: marker only"] = start(script, MODES[script][0])[:2]
    finally:
        os.lstat = real_lstat
r3["one_sign_only"] = {k: {"ended": v[0], "tripwires_reached": v[1]} for k, v in half.items()}
evidence["R3"] = r3
checks["R3_this_machine_is_not_a_box"] = not any(box_signs.values())
checks["R3_every_mode_of_every_script_ends_in_SystemExit_refused"] = all(v["ended"].startswith("SystemExit: refused:") for v in r3["runs"].values())
checks["R3_no_tripwire_reached_and_nothing_imported"] = all(not v["tripwires_reached"] and not v["modules_imported"] for v in r3["runs"].values())
checks["R3_one_sign_of_a_box_is_not_enough"] = all(v["ended"].startswith("SystemExit: refused:") and not v["tripwires_reached"]
                                                  for v in r3["one_sign_only"].values())
checks["R3_modes_started"] = len(r3["runs"]) == sum(len(v) for v in MODES.values())


def gate_positions(script):
    """Static: the gate call is the first statement that is neither the docstring, an import of os/stat nor the two
    gate functions, and `kill -9 -1` is always directly preceded by a gate call."""
    src = open(os.path.join(ROOT, script)).read()
    tree = ast.parse(src)
    body = tree.body[1:] if isinstance(tree.body[0], ast.Expr) and isinstance(getattr(tree.body[0], "value", None), ast.Constant) else tree.body
    first = None
    for node in body:
        if isinstance(node, ast.Import) and {al.name for al in node.names} <= {"os", "stat"}:
            continue
        if isinstance(node, ast.FunctionDef) and node.name in ("_in_exam_box", "_box_only"):
            continue
        first = node
        break
    gate_first = isinstance(first, ast.Expr) and isinstance(first.value, ast.Call) and getattr(first.value.func, "id", "") == "_box_only"
    lines = src.splitlines()
    kills = [i for i, ln in enumerate(lines) if 'os.system("kill -9 -1")' in ln]
    return {"gate_is_the_first_statement": gate_first, "kill_lines": [k + 1 for k in kills],
            "each_kill_directly_preceded_by_the_gate": all("_box_only(" in lines[k - 1] for k in kills)}


r3["static"] = {s: gate_positions(s) for s in MODES}
checks["R3_gate_is_the_first_statement_and_precedes_each_kill"] = all(v["gate_is_the_first_statement"] and v["each_kill_directly_preceded_by_the_gate"]
                                                                     for v in r3["static"].values()) \
    and len(r3["static"]["agents/hostile_submission.py"]["kill_lines"]) == 1 and len(r3["static"]["redteam/agent_rt.py"]["kill_lines"]) == 1

# ============================================================================= R4 + S1: the driver's guard and wipe
ITEM = os.path.join(ROOT, "physim2_env", "public", "_item.py")
spec = importlib.util.spec_from_file_location("item_under_test", ITEM)
item = importlib.util.module_from_spec(spec)
spec.loader.exec_module(item)
FIX = os.path.join(HERE, "fixtures", "mounts")
expected = json.load(open(os.path.join(FIX, "EXPECTED.json")))
tables = {}
for name, exp in expected.items():
    text = open(os.path.join(FIX, name)).read()
    try:
        notfile = set(exp.get("isfile_false_for", []))
        got = item.foreign_mounts(item.parse_mounts(text), isfile=lambda p, _n=notfile: p not in _n)
        tables[name] = {"foreign": got, "expected": exp.get("foreign"), "as_expected": got == exp.get("foreign"), "source": exp.get("captured") or exp.get("synthetic")}
    except ValueError as e:
        tables[name] = {"raised": "ValueError: " + str(e), "expected": exp.get("raises"), "as_expected": exp.get("raises") == "ValueError",
                        "source": exp.get("captured") or exp.get("synthetic")}
evidence["R4_mount_tables"] = tables
checks["R4_allow_list_on_every_stored_mount_table"] = all(v["as_expected"] for v in tables.values()) and len(tables) == 13
checks["R4_stock_docker_tables_have_no_foreign_mount"] = tables["docker_plain.mountinfo"].get("foreign") == [] \
    and tables["docker_verifiers_options.mountinfo"].get("foreign") == []
checks["R4_tmpfs_extra_and_host_folders_are_foreign"] = all(tables[k].get("foreign") for k in ("docker_tmpfs_extra.mountinfo", "synthetic_bind_workspace.mountinfo",
                                                                                              "synthetic_named_volume.mountinfo", "synthetic_bind_below_dev.mountinfo",
                                                                                              "synthetic_macos_share.mountinfo", "synthetic_linux_host.mountinfo"))
# (b) an unreadable table raises; nothing falls back to "/"
real_table = item.MOUNT_TABLE
item.MOUNT_TABLE = os.path.join(TMP, "no-such-table")
unread = {}
for fn, call in (("box_mounts", lambda: item.box_mounts()), ("mount_points", lambda: item.mount_points()), ("owned_by", lambda: item.owned_by(31001)),
                 ("scan", lambda: item.scan(31001))):
    try:
        out = call()
        unread[fn] = {"returned": (out.get("guard", {}).get("why") if isinstance(out, dict) else out)}
    except RuntimeError as e:
        unread[fn] = {"raised": str(e)[:90]}
unread["box_guard"] = short(item.box_guard(31001)["why"])
item.MOUNT_TABLE = real_table
unread["tripwires_reached"] = hits()
evidence["R4_unreadable_mount_table"] = unread
checks["R4_unreadable_mount_table_raises_and_never_falls_back_to_root"] = all(str(unread[k].get("raised", "")).startswith("refused: the mount table")
                                                                             for k in ("box_mounts", "mount_points", "owned_by")) \
    and "the mount table cannot be read" in unread["box_guard"] and "the mount table cannot be read" in (unread["scan"].get("returned") or []) \
    and not unread["tripwires_reached"]
# (a) no rmtree anywhere in the driver
tree = ast.parse(open(ITEM).read())
names = {n.attr for n in ast.walk(tree) if isinstance(n, ast.Attribute)} | {n.id for n in ast.walk(tree) if isinstance(n, ast.Name)}
imports = {al.name for n in ast.walk(tree) if isinstance(n, ast.Import) for al in n.names}
evidence["R4_driver_static"] = {"imports": sorted(imports), "uses_rmtree": "rmtree" in names, "imports_shutil": "shutil" in imports,
                                "destructive_calls_named": sorted(names & {"unlink", "rmdir", "remove", "rename", "chmod", "chown", "fchown", "kill", "killpg"})}
checks["R4_driver_has_no_rmtree_and_no_shutil"] = "rmtree" not in names and "shutil" not in imports
# the guard as a pure function
ok_in = dict(dedicated=31001, evidence=["/.dockerenv"], route=item.ROUTE_VALUE, caller=0, mounts=[])
pure = {
    "all_conditions_met": item.guard_reasons(31001, **ok_in),
    "foreign_mount": item.guard_reasons(31001, **dict(ok_in, mounts=["/workspace (ext4)"])),
    "mount_table_unreadable": item.guard_reasons(31001, **dict(ok_in, mounts=None)),
    "caller_not_root": item.guard_reasons(31001, **dict(ok_in, caller=501)),
    "uid_1000_the_incident_uid": item.guard_reasons(1000, **dict(ok_in, dedicated=1000)),
    "uid_19999": item.guard_reasons(19999, **dict(ok_in, dedicated=19999)),
    "uid_20000": item.guard_reasons(20000, **dict(ok_in, dedicated=20000)),
    "uid_59999": item.guard_reasons(59999, **dict(ok_in, dedicated=59999)),
    "uid_60000": item.guard_reasons(60000, **dict(ok_in, dedicated=60000)),
    "uid_0": item.guard_reasons(0, **dict(ok_in, dedicated=0)),
    "no_marker": item.guard_reasons(31001, **dict(ok_in, dedicated=None)),
    "no_container": item.guard_reasons(31001, **dict(ok_in, evidence=[])),
    "no_route": item.guard_reasons(31001, **dict(ok_in, route=None)),
    "not_the_box_uid": item.guard_reasons(31002, **ok_in),
}
evidence["guard_pure"] = pure
checks["R4_guard_refuses_a_foreign_mount_and_an_unreadable_table"] = pure["all_conditions_met"] == [] and len(pure["foreign_mount"]) == 1 \
    and len(pure["mount_table_unreadable"]) == 1
checks["S1_guard_uid_range_20000_to_59999"] = pure["uid_20000"] == [] and pure["uid_59999"] == [] and all(len(pure[k]) == 1 for k in ("uid_1000_the_incident_uid", "uid_19999", "uid_60000")) \
    and (item.MIN_UID, item.MAX_UID) == (20000, 59999)
checks["S1_guard_requires_a_root_caller"] = pure["caller_not_root"] == ["the caller is not root"]
checks["guard_each_missing_condition_is_one_reason"] = all(len(pure[k]) == 1 for k in ("no_marker", "no_container", "no_route", "not_the_box_uid")) and bool(pure["uid_0"])
# on this machine, with the route variable set (the worst case: it leaked onto a host)
env_before = os.environ.get(item.ROUTE_VAR)
os.environ[item.ROUTE_VAR] = item.ROUTE_VALUE
here = {"guard": {str(u): short(item.box_guard(u)["why"]) for u in (1000, 31001, 0, os.getuid())}, "calls": {}}
try:
    for fn in ("kill_user", "wipe_user", "ipc_user", "cleanup"):
        for uid in (1000, 31001, 0):
            try:
                getattr(item, fn)(uid)
                out = "RETURNED"
            except RuntimeError as e:
                out = "refused" if str(e).startswith("refused") else "RuntimeError"
            except BaseException as e:                       # noqa: BLE001
                out = type(e).__name__
            here["calls"][f"{fn}({uid})"] = {"outcome": out, "tripwires_reached": hits()}
    try:
        item.as_user(31001, lambda: None)
        out = "RETURNED"
    except RuntimeError as e:
        out = "refused" if str(e).startswith("refused") else "RuntimeError"
    except BaseException as e:                               # noqa: BLE001
        out = type(e).__name__
    here["calls"]["as_user(31001)"] = {"outcome": out, "tripwires_reached": hits()}
    sc = item.scan(31001)
    here["calls"]["scan(31001)"] = {"outcome": "returned without a walk" if sc["fixing"] is False and sc["writable_dirs"] == [] else "WALKED",
                                    "tripwires_reached": hits()}
    # the driver as its own main(), with the route variable: refuses, runs nothing
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        item.main(["--uid", "31001", "--submission", TMP, "--runner", os.path.join(TMP, "runner.py"), "--request", os.path.join(TMP, "request.npz")])
    here["driver_main_with_route_variable"] = {"reply": json.loads(buf.getvalue().strip().splitlines()[-1]).get("driver_error", "")[:70], "tripwires_reached": hits()}
finally:
    if env_before is None:
        os.environ.pop(item.ROUTE_VAR, None)
    else:
        os.environ[item.ROUTE_VAR] = env_before
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    item.main(["--uid", "31001", "--submission", TMP, "--runner", os.path.join(TMP, "runner.py"), "--request", os.path.join(TMP, "request.npz")])
here["driver_main_without_route_variable_and_without_no_box"] = {"reply": json.loads(buf.getvalue().strip().splitlines()[-1]).get("driver_error", "")[:70],
                                                                 "ends_with": json.loads(buf.getvalue().strip().splitlines()[-1]).get("driver_error", "")[-60:],
                                                                 "tripwires_reached": hits()}
buf = io.StringIO()
try:
    with contextlib.redirect_stderr(buf):
        item.main(["--scan"])
    no_uid = "ACCEPTED"
except SystemExit as e:
    no_uid = f"SystemExit({e.code}): " + buf.getvalue().strip().splitlines()[-1][-60:]
here["driver_main_without_uid"] = no_uid
evidence["on_this_machine"] = here
checks["R4_every_kill_and_delete_function_refuses_on_this_host"] = all(v["outcome"] == "refused" and not v["tripwires_reached"] for k, v in here["calls"].items()
                                                                      if not k.startswith("scan"))
checks["R4_scan_walks_nothing_on_this_host"] = here["calls"]["scan(31001)"] == {"outcome": "returned without a walk", "tripwires_reached": []}
checks["R4_guard_on_this_host_names_its_mounts"] = all(any("mounted file systems" in w for w in why) for why in here["guard"].values())
checks["S1_driver_runs_nothing_outside_a_box"] = here["driver_main_with_route_variable"]["reply"].startswith("RuntimeError: refused: not a disposable box") \
    and here["driver_main_without_route_variable_and_without_no_box"]["reply"].startswith("RuntimeError: refused: not a disposable box") \
    and not here["driver_main_with_route_variable"]["tripwires_reached"] and not here["driver_main_without_route_variable_and_without_no_box"]["tripwires_reached"]
checks["S1_uid_has_no_default"] = no_uid.startswith("SystemExit(2)") and "--uid" in no_uid
# the wipe's own logic, with its guard switched off FOR THIS TEST and every input faked: which primitive, which path first
tree_dir = os.path.join(TMP, "wipe")
os.makedirs(os.path.join(tree_dir, "owned", "deeper"))
os.makedirs(os.path.join(tree_dir, "mountpoint"))
for p in ("owned/deeper/file", "owned/file"):
    open(os.path.join(tree_dir, p), "w").close()
listed = [os.path.join(tree_dir, p) for p in ("owned", "owned/deeper", "owned/deeper/file", "owned/file", "mountpoint")]
FAKE_UID = 31001
for p in listed:                                             # the test's own files, made a moment ago in its own temporary directory
    TW.real(os, "chown")(p, FAKE_UID, FAKE_UID)
saved_fns = (item.require_box, item.box_mounts, item.owned_by)
item.require_box = lambda uid: None
item.box_mounts = lambda: [("/", "overlay", "/"), (os.path.join(tree_dir, "mountpoint"), "tmpfs", "/")]
wipe = {}
try:
    for case, paths in (("a tree of the uid", listed), ("a mount point of the uid", [os.path.join(tree_dir, "mountpoint")])):
        item.owned_by = lambda uid, mounts=None, _p=paths: list(_p)
        try:
            n, left = item.wipe_user(FAKE_UID)
            out = f"returned: {n} removed, {len(left)} left"
        except tripwires.Tripped as e:
            out = str(e)
        wipe[case] = {"outcome": out, "tripwires_reached": hits()}
finally:
    item.require_box, item.box_mounts, item.owned_by = saved_fns
wipe["everything_still_there"] = all(os.path.lexists(p) for p in listed)
evidence["R4_wipe_logic"] = dict(wipe, listed=[os.path.relpath(p, tree_dir) for p in listed],
                                 note="guard and inputs faked for this test only; the first destructive call is a tripwire, so nothing is removed")
checks["R4_wipe_reaches_unlink_for_the_deepest_listed_path_first"] = wipe["a tree of the uid"]["outcome"] == "tripwire: os.unlink" \
    and len(wipe["a tree of the uid"]["tripwires_reached"]) == 1 and "owned/deeper/file" in wipe["a tree of the uid"]["tripwires_reached"][0] \
    and wipe["everything_still_there"]
checks["R4_wipe_never_touches_a_mount_point"] = wipe["a mount point of the uid"] == {"outcome": "returned: 0 removed, 1 left", "tripwires_reached": []}

# ============================================================================= R5: the worker gate
import verifiers.v1 as vf  # noqa: E402
from physim2_env import access as ACCESS  # noqa: E402
from physim2_env import grading as G  # noqa: E402
from physim2_env.taskset import Physim2Task  # noqa: E402
from physim2_script import ScriptHarness  # noqa: E402
from verifiers.v1.runtimes import DockerConfig, DockerRuntime, SubprocessConfig, SubprocessRuntime  # noqa: E402

evidence["imports_reached_tripwires"] = hits()
evidence["package_under_test"] = {"physim2_env": os.path.relpath(os.path.dirname(G.__file__), ROOT), "vfrun": os.path.relpath(vfrun.__file__, ROOT),
                                  "verifiers": __import__("verifiers").__version__}


class Recording:
    """Looks like a verifiers runtime in every attribute the package reads; records every command it is given."""

    def __init__(self, typ, **extra):
        self.config = types.SimpleNamespace(type=typ, network_restricted=True, workdir="/workspace", image="physim2-ring:1")
        self.info = types.SimpleNamespace(borrowed=False, id="0" * 12)
        self._container, self._host, self.env, self.calls = "vf-" + "0" * 32, None, {}, []
        self.__dict__.update(extra)

    async def run(self, argv, env):
        self.calls.append(("run", argv[:3]))
        return types.SimpleNamespace(exit_code=0, stdout='{"guard": {"ok": true}}\nHAS_PREDICT', stderr="")

    run_program = run

    async def write(self, path, data):
        self.calls.append(("write", path))

    async def read(self, path, max_bytes=None):
        self.calls.append(("read", path))
        return b""

    def host_url(self, url):
        self.calls.append(("host_url", url))
        return url


class Subclassed(DockerRuntime):
    """A test double made by inheriting from the real class."""


def real_docker(container, borrowed=False):
    rt = DockerRuntime(DockerConfig(image="physim2-ring:1"))     # constructing starts nothing
    rt._container = container
    rt.info.borrowed = borrowed
    return rt


def outcome(coro):
    try:
        r = asyncio.run(coro)
        return "returned: " + json.dumps(r, default=str)[:400]
    except vf.TaskError as e:
        return "TaskError: " + str(e)[:90]
    except RuntimeError as e:
        return "RuntimeError: " + str(e)[:90]
    except BaseException as e:                               # noqa: BLE001
        return type(e).__name__ + ": " + str(e)[:90]


art = [types.SimpleNamespace(source="submission")]
fake_task = types.SimpleNamespace(data=types.SimpleNamespace(world="ring", config_name="smoke_ring"), config=types.SimpleNamespace())
harness = object.__new__(ScriptHarness)
harness.config = types.SimpleNamespace(agent_dir=TMP, script="x.py", args=[], python="python3", collect=[], collect_dir="", resolved_env={})
boxes = []


def through_every_entry(make):
    """Each entry point of the package that sends commands into a box, given a fresh stand-in each time."""
    out = {}

    def one(name, fn):
        rt = make()
        out[name] = {"outcome": outcome(fn(rt)), "commands_received": list(getattr(rt, "calls", [])), "tripwires_reached": hits()}
    one("grading.stage", lambda rt: G.stage(rt, "/workspace", 31001))
    one("grading.run_request", lambda rt: G.run_request(rt, ["python3", "/runtime/item.py"], b"request", 1.0))
    one("Physim2Task._public_files", lambda rt: Physim2Task._public_files(fake_task, rt))
    one("Physim2Task.setup", lambda rt: Physim2Task.setup(fake_task, types.SimpleNamespace(), rt))

    def box(rt):
        b = ACCESS.BoxAccess(rt, art, 1 << 20, 1.0)
        boxes.append(b)
        return b
    one("BoxAccess.check", lambda rt: box(rt).check("submission", False))
    one("BoxAccess.check(final)", lambda rt: box(rt).check("submission", True))
    one("BoxAccess.announce", lambda rt: box(rt).announce(1234))
    one("access.collect_frozen", lambda rt: ACCESS.collect_frozen(rt, art, 1 << 20, 1.0))
    one("ScriptHarness.setup", lambda rt: harness.setup(rt))
    one("ScriptHarness.install", lambda rt: harness.install(rt, TMP))
    return out


r5 = {
    "recording fake typed docker": through_every_entry(lambda: Recording("docker")),
    "recording fake typed subprocess": through_every_entry(lambda: Recording("subprocess")),
    "recording fake typed prime": through_every_entry(lambda: Recording("prime")),
}
evidence["R5"] = r5
gate = {
    "recording fake typed docker": G.container_gate(Recording("docker")),
    "recording fake typed subprocess": G.container_gate(Recording("subprocess")),
    "subclass of DockerRuntime": G.container_gate(object.__new__(Subclassed)),
    "real SubprocessRuntime": G.container_gate(SubprocessRuntime(SubprocessConfig())),
    "real DockerRuntime, never started": G.container_gate(real_docker(None)),
    "real DockerRuntime, borrowed (attach)": G.container_gate(real_docker("vf-" + "a" * 32, borrowed=True)),
    "real DockerRuntime, a hand-named container": G.container_gate(real_docker("my-debug-box")),
    "real DockerRuntime, nested in another runtime": (lambda rt: (setattr(rt, "_host", object()), G.container_gate(rt))[1])(real_docker("vf-" + "a" * 32)),
    "real DockerRuntime as verifiers starts it": G.container_gate(real_docker("vf-" + "a" * 32)),
    "its with_env view": G.container_gate(real_docker("vf-" + "a" * 32).with_env({"A": "b"})),
    "None": G.container_gate(None),
}
evidence["R5_gate"] = gate
evidence["R5_tripwires_reached"] = hits()
checks["R5_recording_fakes_receive_zero_commands"] = all(v["commands_received"] == [] and not v["tripwires_reached"] for d in r5.values() for v in d.values())
checks["R5_every_entry_point_was_exercised"] = all(len(d) == 10 for d in r5.values())
checks["R5_stage_public_files_setup_announce_and_harness_raise"] = all(d[k]["outcome"].startswith(("RuntimeError: ", "TaskError: "))
                                                                      for d in r5.values() for k in ("grading.stage", "Physim2Task._public_files",
                                                                                                     "Physim2Task.setup", "BoxAccess.announce",
                                                                                                     "ScriptHarness.setup", "ScriptHarness.install"))
checks["R5_run_request_and_check_report_a_failure_without_a_command"] = all('"ok": false' in d[k]["outcome"] for d in r5.values()
                                                                           for k in ("grading.run_request", "BoxAccess.check", "BoxAccess.check(final)",
                                                                                     "access.collect_frozen"))
checks["R5_gate_passes_only_the_real_unborrowed_runtime"] = gate["real DockerRuntime as verifiers starts it"] == [] and gate["its with_env view"] == [] \
    and all(v for k, v in gate.items() if k not in ("real DockerRuntime as verifiers starts it", "its with_env view"))
# S1 / B3: the validator outside a box
from physim2_env.public import validate as V  # noqa: E402

rep = V.check("submission", workspace=TMP)
evidence["S1_validator_on_this_machine"] = {"report": rep, "run_request": {k: v for k, v in V.run_request(TMP, TMP, {}, {}).items() if k in ("ok", "error")},
                                            "tripwires_reached": hits()}
checks["S1_validator_runs_nothing_outside_a_box"] = rep["ok"] is False and "inside an exam box only" in rep["error"] \
    and not evidence["S1_validator_on_this_machine"]["tripwires_reached"]

# ============================================================================= done
checks["no_tripwire_was_reached_outside_the_two_tests_that_expect_one"] = not evidence["imports_reached_tripwires"] and not hits() \
    and r2["run_eval_docker_check_is_a_subprocess"]["tripwires_reached"][0].startswith("subprocess.run")
TW.restore()
for b in boxes:
    b.directory.cleanup()
import shutil  # noqa: E402

shutil.rmtree(TMP)                                           # this test's own temporary directory
res = {"what": "host-side tests of HOST_SAFETY_AUDIT.md section 4, run with every destructive primitive of the process replaced by a "
               "tripwire before the package was imported; nothing was started, killed or deleted on this machine",
       "evidence_label": "tripwire", "tripwires_installed": N_WIRES, "n_checks": len(checks), "n_passed": sum(v is True for v in checks.values()),
       "failed": [k for k, v in checks.items() if v is not True], "checks": checks, "evidence": evidence, "hidden_values_in_this_file": "none"}
os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
json.dump(res, open(a.out, "w"), indent=1, default=str)
print(json.dumps({k: res[k] for k in ("tripwires_installed", "n_checks", "n_passed", "failed")}))
