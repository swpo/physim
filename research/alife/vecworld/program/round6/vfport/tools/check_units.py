"""check_units -- offline regression checks of the rules the reviews attacked (no Docker, no verifiers run).

Each check is a named boolean with its evidence. They are written against the FIXED behaviour; run against the
builder's code (--package-root <its checkout>) the failing ones reproduce the findings:

  freeze_*    hostile submission archives (specification review 1): whatever the archive, `freeze` returns, and
              what it returns passes verifiers' own restore check and extracts with the system tar
  reply_*     hostile reply files (red team 1 and 5): float64 samples, thousands of members, lying headers
  score_*     the score of the red team's overflow samples (needs --store with one instance)
  lab_*       malformed laboratory requests (red team 9; needs --store)
  driver_*    the one-request driver, run here on the host: a named pipe or a link left as stderr.txt or reply.npz
              (red team 3) must not block or be followed. On a host the driver must NOT drop privileges or clean
              up (its cleanup deletes every file of one uid; see _item.in_box), which is checked first: these
              checks are skipped, loudly, if this process is root and the driver would not refuse.
  report_*    the validator's report from the agent's box is reduced to typed fields
  guard_*     HOST SAFETY. The driver's cleanup kills every process and deletes every file of one uid; it once ran
              on a development host. Here: (1) the guard's decision for every missing layer, as a pure function;
              (2) on THIS machine the guard refuses; (3) every function that kills or deletes is called with the
              route variable set and must refuse BEFORE touching anything. From before the driver's file is even
              imported until the last of these calls, every destructive primitive of this process is a tripwire
              (tools/tripwires.py: 65 names of os, shutil, subprocess and pathlib) and the walk is confined to an
              empty temporary directory, so that even a broken guard could do nothing here. If the code under
              --package-root has NO guard, its kill and delete functions are not called at all (audit B4).
              The real cleanup is tested in a throwaway container only (tools/check_driver.py).
  driver_*    (see above) are run ONLY when this process is not root: as root the driver is never started on a
              host, whatever its guard says (audit B4); tools/check_driver.py covers the same cases in a container.

usage: python tools/check_units.py [--store DIR --instance ID] [--package-root DIR] --out results/units.json
"""
import argparse
import io
import json
import os
import subprocess
import sys
import tarfile
import tempfile
import time
import zipfile

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import tripwires  # noqa: E402

if sys.platform != "linux" or os.environ.get("PHYSIM2_DEV_MACHINE") != "cloud-container":
    raise SystemExit("check_units.py is a development check for the Linux build container (it starts test predictors on the machine it "
                     "runs on). It is NOT part of the Mac runbook: do not run it on a personal machine. In the build container: "
                     "PHYSIM2_DEV_MACHINE=cloud-container python tools/check_units.py ...")
ap = argparse.ArgumentParser()
ap.add_argument("--store", default="")
ap.add_argument("--instance", default="")
ap.add_argument("--package-root", default=os.path.dirname(HERE))
ap.add_argument("--out", required=True)
a = ap.parse_args()
sys.path.insert(0, os.path.abspath(a.package_root))
from physim2_env import grading as G  # noqa: E402
from physim2_env._paths import agentenv_root, use_agentenv  # noqa: E402
from physim2_env.public import _rules  # noqa: E402
from verifiers.v1.utils.artifacts import _validate_restore  # noqa: E402

ROOT = "workspace/submission"
GOOD = b"def predict(history, program, queries, n_samples, seed):\n    return {}\n"
checks, evidence = {}, {}


def tar_of(entries):
    """entries: (name, kind, payload) with kind in file, dir, sym, hard, fifo, chr."""
    buf = io.BytesIO()
    with tarfile.open(fileobj=buf, mode="w", format=tarfile.PAX_FORMAT) as t:
        for name, kind, payload in entries:
            ti = tarfile.TarInfo(name)
            if kind == "file":
                ti.size = len(payload)
                t.addfile(ti, io.BytesIO(payload))
                continue
            ti.type = {"dir": tarfile.DIRTYPE, "sym": tarfile.SYMTYPE, "hard": tarfile.LNKTYPE, "fifo": tarfile.FIFOTYPE,
                       "chr": tarfile.CHRTYPE}[kind]
            if kind in ("sym", "hard"):
                ti.linkname = payload
            t.addfile(ti)
    return buf.getvalue()


def P(rel):
    return f"{ROOT}/{rel}"


base = [(ROOT, "dir", None), (P("predict.py"), "file", GOOD)]
CASES = {
    "plain": base + [(P("w/a.npy"), "file", b"x" * 10)],
    "duplicate_file": base + [(P("predict.py"), "file", b"raise SystemExit(1)\n")],
    "duplicate_through_dot": base + [(P("./predict.py"), "file", b"#\n")],
    "file_and_directory_same_name": base + [(P("a"), "file", b"1"), (P("a"), "dir", None)],
    "file_used_as_parent": base + [(P("a"), "file", b"1"), (P("a/b"), "file", b"2")],
    "path_5000_bytes": base + [(P("/".join(["d" * 200] * 25) + "/x"), "file", b"1")],
    "name_300_bytes": base + [(P("n" * 300), "file", b"1")],
    "depth_60": base + [(P("/".join(["d"] * 60) + "/x"), "file", b"1")],
    "control_character_name": base + [(P("a\nb"), "file", b"1"), (P("tab\there"), "file", b"1")],
    "links_and_special_files": base + [(P("s"), "sym", "/etc/passwd"), (P("loop"), "sym", "loop"), (P("h"), "hard", P("predict.py")),
                                       (P("f"), "fifo", None), (P("c"), "chr", None)],
    "file_below_a_link": base + [(P("s"), "sym", "/tmp"), (P("s/x"), "file", b"1")],
    "outside_root_and_dotdot": base + [("etc/passwd", "file", b"1"), (P("../../x"), "file", b"1"), ("/abs", "file", b"1")],
    "pycache": base + [(P("__pycache__/predict.cpython-312.pyc"), "file", b"1")],
    "many_members": base + [(P(f"m/{i}"), "file", b"") for i in range(_rules.__dict__.get("MAX_MEMBERS", 20000) + 5)],
    "no_predict": [(ROOT, "dir", None), (P("other.py"), "file", GOOD)],
    "predict_is_a_directory": [(ROOT, "dir", None), (P("predict.py"), "dir", None), (P("predict.py/x"), "file", b"1")],
    "unicode_name": base + [(P("données/π.txt"), "file", b"1")],
}
raw_plain = tar_of(CASES["plain"])
RAW = {k: tar_of(v) for k, v in CASES.items()}
RAW["truncated"] = raw_plain[:700]
RAW["garbage"] = os.urandom(4096)
RAW["empty"] = b""
RAW["none"] = None
buf = io.BytesIO()
with tarfile.open(fileobj=buf, mode="w", format=tarfile.GNU_FORMAT, encoding="utf-8", errors="surrogateescape") as t:
    for name, kind, payload in base:
        ti = tarfile.TarInfo(name)
        if kind == "file":
            ti.size = len(payload)
            t.addfile(ti, io.BytesIO(payload))
        else:
            ti.type = tarfile.DIRTYPE
            t.addfile(ti)
    ti = tarfile.TarInfo(P(b"\xff\xfe-bin".decode("utf-8", "surrogateescape")))
    ti.size = 1
    t.addfile(ti, io.BytesIO(b"1"))
RAW["undecodable_name"] = buf.getvalue()

freeze_ev = {}
for name, raw in RAW.items():
    rec = {}
    try:
        arc, man, err = _rules.freeze(raw, ROOT, 1.0)
        rec.update(refused=err, files=len(man.get("files", [])), skipped=man.get("skipped"))
    except Exception as e:
        rec["freeze_raised"] = type(e).__name__
        freeze_ev[name] = rec
        continue
    if arc is not None:
        try:
            _validate_restore("/" + ROOT, arc)
            rec["verifiers_restore_check"] = "passes"
        except Exception as e:
            rec["verifiers_restore_check"] = f"REFUSES: {str(e)[:90]}"
        with tempfile.TemporaryDirectory() as d:
            f = os.path.join(d, "a.tar")
            open(f, "wb").write(arc)
            os.makedirs(os.path.join(d, "x"))
            r = subprocess.run(["tar", "-xf", f, "-C", os.path.join(d, "x")], capture_output=True, text=True)
            rec["system_tar_exit"] = r.returncode
            rec["predict_extracted"] = os.path.isfile(os.path.join(d, "x", ROOT, "predict.py"))
            subprocess.run(["chmod", "-R", "u+w", d])
    freeze_ev[name] = rec
evidence["freeze"] = freeze_ev


def gradable(r):
    """Either refused by freeze (the rollout is then K), or frozen into something every later step accepts."""
    if "freeze_raised" in r:
        return False
    if r.get("refused"):
        return True
    return r.get("verifiers_restore_check") == "passes" and r.get("system_tar_exit") == 0 and r.get("predict_extracted")


checks["freeze_never_raises"] = all("freeze_raised" not in r for r in freeze_ev.values())
checks["freeze_output_always_passes_verifiers_restore_check_and_extracts"] = all(gradable(r) for r in freeze_ev.values())
for k in ("duplicate_file", "duplicate_through_dot", "file_and_directory_same_name", "file_used_as_parent", "path_5000_bytes",
          "name_300_bytes", "many_members", "no_predict", "predict_is_a_directory", "truncated", "garbage", "none"):
    checks[f"freeze_refuses_{k}"] = bool(freeze_ev[k].get("refused"))
for k in ("plain", "links_and_special_files", "control_character_name", "outside_root_and_dotdot", "pycache", "unicode_name", "undecodable_name",
          "file_below_a_link"):
    checks[f"freeze_keeps_the_rest_of_{k}"] = gradable(freeze_ev[k]) and not freeze_ev[k].get("refused")
checks["freeze_plain_keeps_2_files"] = freeze_ev["plain"].get("files") == 2
checks["freeze_links_keeps_1_file"] = freeze_ev["links_and_special_files"].get("files") == 1


# ----------------------------------------------------------------------------- replies
def npz(arrays, compress=False):
    buf = io.BytesIO()
    (np.savez_compressed if compress else np.savez)(buf, **arrays)
    return buf.getvalue()


m, dims = 32, {1: 6, 2: 3}
qs = {1: [1, 2, 4, 8, 16], 2: [16, 32]}
MAXV = m * sum(len(ts) * dims[l] for l, ts in qs.items())
good = {f"level{l}": np.random.default_rng(0).standard_normal((m, len(ts), dims[l])).astype(np.float32) for l, ts in qs.items()}
member = io.BytesIO()
np.save(member, np.zeros(4096 - 128, np.uint8))
bomb = io.BytesIO()
with zipfile.ZipFile(bomb, "w", zipfile.ZIP_DEFLATED) as z:
    for i in range(3000):
        z.writestr(f"level{i}.npy", member.getvalue())
lie = io.BytesIO()
with zipfile.ZipFile(lie, "w") as z:                          # a header that declares 2**40 numbers, with 16 bytes behind it
    hdr = io.BytesIO()
    np.lib.format.write_array_header_1_0(hdr, {"descr": "<f4", "fortran_order": False, "shape": (1 << 20, 1 << 10, 1 << 10)})
    z.writestr("level1.npy", b"\x93NUMPY\x01\x00"[:0] + hdr.getvalue() + b"\0" * 16)
REPLIES = {
    "good": npz(good), "good_compressed": npz(good, True),
    "float64": npz({k: v.astype(np.float64) for k, v in good.items()}),
    "overflow_float64": npz({"level1": np.where(np.arange(m)[:, None, None] % 2 == 0, 1e154, -1e154) * np.ones((m, 5, 6)),
                             "level2": np.zeros((m, 2, 3))}),
    "many_members": bomb.getvalue(), "lying_header": lie.getvalue(),
    "extra_member": npz(dict(good, extra=np.zeros(3, np.float32))),
    "not_a_zip": b"hello", "empty": b"",
    "four_axes": npz({"level1": np.zeros((m, 5, 6, 1), np.float32), "level2": good["level2"]}),
    "too_many_values": npz({"level1": np.zeros((m, 5, 6 * 64), np.float32), "level2": good["level2"]}),
    "int_array": npz({"level1": np.zeros((m, 5, 6), np.int32), "level2": good["level2"]}),
}
buf = io.BytesIO()
np.savez(buf, level1=np.array([{"a": 1}], dtype=object), allow_pickle=True)
REPLIES["object_array"] = buf.getvalue()
reply_ev = {}
for name, raw in REPLIES.items():
    t0, r0 = time.time(), __import__("resource").getrusage(__import__("resource").RUSAGE_SELF).ru_maxrss
    try:
        out = _rules.read_reply(raw, MAXV)
        reply_ev[name] = {"accepted": True, "levels": sorted(out), "dtypes": sorted({str(v.dtype) for v in out.values()}),
                          "held_mib": round(sum(v.nbytes for v in out.values()) / 2 ** 20, 2)}
    except Exception as e:
        reply_ev[name] = {"accepted": False, "error": f"{type(e).__name__}: {str(e)[:110]}"}
    reply_ev[name].update(seconds=round(time.time() - t0, 3),
                          rss_growth_mib=round((__import__("resource").getrusage(__import__("resource").RUSAGE_SELF).ru_maxrss - r0) / 1024, 1))
evidence["reply"] = reply_ev
checks["reply_good_accepted_and_equal"] = reply_ev["good"]["accepted"] and reply_ev["good_compressed"]["accepted"] and all(
    np.array_equal(_rules.read_reply(REPLIES["good"], MAXV)[l], good[f"level{l}"].astype(np.float64)) for l in qs)
for k in ("float64", "overflow_float64", "many_members", "lying_header", "extra_member", "object_array", "not_a_zip", "empty", "four_axes",
          "too_many_values", "int_array"):
    checks[f"reply_refuses_{k}"] = not reply_ev[k]["accepted"]
checks["reply_refusals_hold_little_memory"] = all(v["rss_growth_mib"] < 32 for v in reply_ev.values())

# ----------------------------------------------------------------------------- the validator's report
try:
    from physim2_env.access import clean_report
    rep = clean_report("noise\n" + json.dumps({"ok": 1, "stage": "x" * 9000, "error": {"nested": "object"}, "cpu_s": 1e99,
                                                "files": "3", "limits": {"a": [1] * 1000}, "__class__": "x", "note": "fine"}))
    evidence["report"] = {k: (v if not isinstance(v, str) else f"<{len(v)} characters>") for k, v in rep.items()}
    checks["report_ok_must_be_true_itself"] = rep["ok"] is False
    checks["report_keeps_typed_fields_only"] = set(rep) <= {"ok", "stage", "note"} and len(rep.get("stage", "")) <= 6000
    checks["report_garbage_is_a_failed_report"] = clean_report("not json")["ok"] is False and clean_report("[1, 2]")["ok"] is False
except ImportError:
    evidence["report"] = "not applicable to this package (no access.clean_report)"

# ----------------------------------------------------------------------------- the box guard, on this host
ITEM = os.path.join(os.path.abspath(a.package_root), "physim2_env", "public", "_item.py")
import importlib.util  # noqa: E402

# From here to TW.restore() below this process cannot kill, delete, re-own, change identity or start anything:
# the tripwires go in BEFORE the driver's file is imported.
empty = tempfile.mkdtemp(prefix="physim2-units-empty-")      # the only place a walk could go; removed after restore()
ww = os.path.join(empty, "world_writable")
open(ww, "w").close()
os.chmod(ww, 0o666)
os.chmod(empty, 0o755)
TW = tripwires.install()


def reached():
    return [h[0] for h in TW.take()]


def short(why):
    """Guard reasons without the layout of this machine: of the foreign mounts only the first and a count."""
    out = []
    for w in why:
        head, sep, tail = w.partition("does not have: ")
        out.append(head + sep + tail.split(", ")[0] + (f" and {len(tail.split(', ')) - 1} more" if ", " in tail else "") if sep else w)
    return out


trip_ev = {}
env_before = os.environ.get("PHYSIM2_BOX_CLEANUP")
try:
    _spec = importlib.util.spec_from_file_location("item_under_test", ITEM)
    item = importlib.util.module_from_spec(_spec)
    _spec.loader.exec_module(item)
    HAS_GUARD = hasattr(item, "guard_reasons")
    if HAS_GUARD:
        ok_in = dict(dedicated=31001, evidence=["/.dockerenv"], route=item.ROUTE_VALUE, caller=0, mounts=[])
        pure = {
            "all_layers_present_is_allowed": item.guard_reasons(31001, **ok_in) == [],
            "no_marker": item.guard_reasons(31001, **dict(ok_in, dedicated=None)),
            "no_sign_of_a_container": item.guard_reasons(31001, **dict(ok_in, evidence=[])),
            "no_route_variable": item.guard_reasons(31001, **dict(ok_in, route=None)),
            "wrong_route_value": item.guard_reasons(31001, **dict(ok_in, route="1")),
            "uid_0": item.guard_reasons(0, **dict(ok_in, dedicated=0)),
            "uid_is_the_caller": item.guard_reasons(31001, **dict(ok_in, caller=31001)),
            "caller_is_not_root": item.guard_reasons(31001, **dict(ok_in, caller=501)),
            "uid_is_not_the_box_predictor_uid": item.guard_reasons(31002, **ok_in),
            "uid_below_1000": item.guard_reasons(500, **dict(ok_in, dedicated=500)),
            "uid_1000_the_uid_of_the_incident": item.guard_reasons(1000, **dict(ok_in, dedicated=1000)),
            "uid_above_the_reserved_range": item.guard_reasons(60000, **dict(ok_in, dedicated=60000)),
            "a_mount_that_a_prepared_box_does_not_have": item.guard_reasons(31001, **dict(ok_in, mounts=["/workspace (ext4)"])),
            "an_unreadable_mount_table": item.guard_reasons(31001, **dict(ok_in, mounts=None)),
            "uid_not_a_number": item.guard_reasons(None, **ok_in),
            "uid_true": item.guard_reasons(True, **dict(ok_in, dedicated=1)),
        }
        evidence["guard_pure"] = pure
        checks["guard_allows_only_when_every_layer_is_present"] = pure["all_layers_present_is_allowed"] is True
        for k, v in pure.items():
            if k != "all_layers_present_is_allowed":
                checks[f"guard_refuses_{k}"] = isinstance(v, list) and len(v) == 1 if k not in ("uid_true", "uid_not_a_number", "uid_0", "uid_is_the_caller") else bool(v)
        here_guard = {str(u): item.box_guard(u) for u in (1000, 0, os.getuid(), 31001)}
        evidence["guard_on_this_machine"] = {"container_evidence": item.container_evidence(), "marker_uid": item.dedicated_uid(),
                                             "route_variable_set": os.environ.get(item.ROUTE_VAR) is not None,
                                             "decisions": {u: {"ok": g["ok"], "why": short(g["why"])} for u, g in here_guard.items()}}
        checks["guard_refuses_on_this_machine"] = all(not g["ok"] for g in here_guard.values())
        # every function that kills or deletes, called on this host under the tripwires (see the docstring)
        os.environ["PHYSIM2_BOX_CLEANUP"] = "disposable-box"         # the worst case: the route variable leaked onto a host
        item.mount_points = lambda mounts=None: [empty]
        item.box_mounts = lambda: [(empty, "tmpfs", "/")]
        for fn in ("kill_user", "wipe_user", "ipc_user", "cleanup"):
            for uid in (1000, 0, 31001):
                try:
                    getattr(item, fn)(uid)
                    out = "RETURNED"
                except RuntimeError as e:
                    out = "refused" if str(e).startswith("refused") else f"RuntimeError: {e}"[:80]
                except AssertionError as e:
                    out = str(e)
                except Exception as e:
                    out = f"{type(e).__name__}"
                trip_ev[f"{fn}({uid})"] = {"outcome": out, "destructive_calls_reached": reached()}
        try:
            item.as_user(31001, lambda: None)
            out = "RETURNED"
        except RuntimeError as e:
            out = "refused" if str(e).startswith("refused") else str(e)[:80]
        except AssertionError as e:
            out = str(e)
        trip_ev["as_user(31001)"] = {"outcome": out, "destructive_calls_reached": reached()}
        try:
            sc = item.scan(31001)
            trip_ev["scan(31001)"] = {"outcome": "returned", "fixing": sc.get("fixing"), "destructive_calls_reached": reached(),
                                      "file_still_world_writable": bool(os.stat(ww).st_mode & 0o002)}
        except AssertionError as e:
            trip_ev["scan(31001)"] = {"outcome": str(e), "destructive_calls_reached": reached()}
    else:
        evidence["guard_tripwires_skipped"] = ("the driver under --package-root has no box guard: its kill and delete functions are NOT called "
                                               "on this host, not even under tripwires")
finally:
    TW.restore()
    if env_before is None:
        os.environ.pop("PHYSIM2_BOX_CLEANUP", None)
    else:
        os.environ["PHYSIM2_BOX_CLEANUP"] = env_before
    os.unlink(ww)                                            # this test's own two entries, by name
    os.rmdir(empty)
evidence["guard_tripwires"] = dict(trip_ev, tripwires_installed=len(TW.names))
if HAS_GUARD:
    checks["guard_every_kill_and_delete_function_refuses_on_this_host"] = all(v["outcome"] == "refused" and not v["destructive_calls_reached"]
                                                                              for k, v in trip_ev.items() if not k.startswith("scan"))
    checks["guard_scan_changes_no_mode_on_this_host"] = trip_ev["scan(31001)"].get("fixing") is False and not trip_ev["scan(31001)"]["destructive_calls_reached"] \
        and trip_ev["scan(31001)"].get("file_still_world_writable") is True

# ----------------------------------------------------------------------------- the driver, without root
RUNNER = os.path.join(agentenv_root(), "physim2", "predict_runner.py")
PRED = {
    "fifo_as_stderr": "import os, sys\ndef predict(h, p, q, n, s):\n    io = os.path.dirname(sys.argv[3]); p = os.path.join(io, 'stderr.txt')\n"
                      "    os.unlink(p); os.mkfifo(p, 0o666); os._exit(1)\n",
    "fifo_as_reply": "import os, sys\ndef predict(h, p, q, n, s):\n    os.mkfifo(sys.argv[3], 0o666); os._exit(0)\n",
    "link_as_stderr": "import os, sys\ndef predict(h, p, q, n, s):\n    io = os.path.dirname(sys.argv[3]); p = os.path.join(io, 'stderr.txt')\n"
                      "    os.unlink(p); os.symlink('/etc/hostname', p); os._exit(1)\n",
    "link_as_reply": "import os, sys\ndef predict(h, p, q, n, s):\n    os.symlink('/etc/hostname', sys.argv[3]); os._exit(0)\n",
    "directory_as_reply": "import os, sys\ndef predict(h, p, q, n, s):\n    os.mkdir(sys.argv[3]); os._exit(0)\n",
    "float64_past_the_runner": "import os, sys, numpy as np\ndef predict(h, p, q, n, s):\n"
                               "    np.savez(sys.argv[3], **{f'level{l}': np.zeros((n, len(ts), {1: 6, 2: 3}[l])) for l, ts in q.items()}); os._exit(0)\n",
    "honest": "import numpy as np\ndef predict(h, p, q, n, s):\n    return {l: np.zeros((n, len(ts), {1: 6, 2: 3}[l])) for l, ts in q.items()}\n",
}
drv = {}
src_item = open(ITEM).read()
# the driver as a program is started on this host ONLY by a user who is not root (audit B4): as root it is never
# started here, whatever its guard says; tools/check_driver.py runs the same predictors in a throwaway container
SAFE = os.geteuid() != 0 and HAS_GUARD
evidence["driver_host_guard"] = {"euid": os.geteuid(), "driver_has_the_box_guard": HAS_GUARD, "driver_program_was_run_here": SAFE,
                                 "why_not": None if SAFE else "this process is root (or the driver has no guard): the driver is never started as "
                                                              "root on a host; see results/driver_container.json for the same cases in a container"}
del src_item
with tempfile.TemporaryDirectory() as d:
    req = os.path.join(d, "request.npz")
    np.savez(req, history=np.zeros((17, 6)), prefix=np.zeros((16, 24)), test=np.zeros((32, 24)), queries=json.dumps({"1": [1, 2], "2": [16]}),
             n_samples=4, seed=0)
    for name, src in (PRED.items() if SAFE else ()):
        sub = os.path.join(d, name)
        os.makedirs(sub)
        open(os.path.join(sub, "predict.py"), "w").write(src)
        t0 = time.time()
        try:
            p = subprocess.run([sys.executable, "-I", "-B", ITEM, "--submission", sub, "--runner", RUNNER, "--request", req, "--cpu", "20",
                                "--wall", "30", "--mem-gib", "4", "--uid", "31001", "--no-box"], capture_output=True, text=True, timeout=45,
                               env={k: v for k, v in os.environ.items() if k != "PHYSIM2_BOX_CLEANUP"})
            r = json.loads(p.stdout.strip().splitlines()[-1])
            rec = {"returned": True, "ok": r.get("ok"), "why": r.get("why"), "stderr_tail": (r.get("stderr") or "")[-60:],
                   "driver_error": r.get("driver_error"), "layers": r.get("layers")}
            if r.get("ok"):
                try:
                    out = _rules.read_reply(__import__("base64").b64decode(r["reply_b64"]), 4 * 3 * 6)
                    rec["worker_reads_reply"] = sorted(out)
                except Exception as e:
                    rec["worker_reads_reply"] = f"refused: {str(e)[:80]}"
        except subprocess.TimeoutExpired:
            rec = {"returned": False, "why": "the driver was still blocked after 45 s"}
        rec["seconds"] = round(time.time() - t0, 2)
        drv[name] = rec
evidence["driver"] = drv
if SAFE:
    checks["driver_returns_for_every_predictor"] = all(v["returned"] for v in drv.values())
    checks["driver_fifo_or_link_is_never_a_reply"] = all(drv[k].get("ok") is False for k in ("fifo_as_reply", "link_as_reply", "directory_as_reply")
                                                         if drv[k]["returned"]) and all(drv[k]["returned"] for k in ("fifo_as_reply", "link_as_reply"))
    checks["driver_does_not_follow_a_link_left_as_stderr"] = drv["link_as_stderr"].get("returned") and drv["link_as_stderr"].get("stderr_tail") == ""
    checks["driver_honest_predictor_passes"] = drv["honest"].get("ok") is True and drv["honest"].get("worker_reads_reply") == [1, 2]
    checks["worker_refuses_a_reply_written_past_the_runner"] = str(drv["float64_past_the_runner"].get("worker_reads_reply", "")).startswith("refused")
    checks["driver_on_a_host_did_not_drop_or_clean"] = all(v.get("layers", {}).get("uid") is None and v.get("layers", {}).get("cleanup") is False
                                                           for v in drv.values() if v["returned"])

# ----------------------------------------------------------------------------- with an instance: score and laboratory
if a.store and a.instance:
    hidden = os.path.join(a.store, a.instance, "hidden")
    use_agentenv()
    ex = G.exam(hidden)
    refs = ex.references()
    from evaluator import instance as INST
    W = INST.world_module(json.load(open(os.path.join(hidden, "instance.json")))["world"])
    scales = {int(l): np.asarray(s, float).ravel() for l, s in W.scales().items()}
    mm = 32
    S64, S32 = {}, {}
    for l, ts in ex.queries.items():
        q = float(np.sum(1.0 / scales[l] ** 2))
        x = np.zeros((ex.n, mm, len(ts), ex.dims[l]))
        x[:, ::2], x[:, 1::2] = 1.0e154 / q ** 0.5, -1.0e154 / q ** 0.5
        S64[l] = x
        y = np.zeros((ex.n, mm, len(ts), ex.dims[l]))
        y[:, ::2], y[:, 1::2] = np.finfo(np.float32).max, -np.finfo(np.float32).max
        S32[l] = y
    with np.errstate(all="ignore"):
        s64, s32 = ex.score(S64), ex.score(S32)
    sk64 = G.summary(ex, s64, refs)["skill_vs_O"]
    evidence["score"] = {"float64_overflow_samples": {"finite_scores": int(np.isfinite(s64).sum()), "of": int(s64.size), "minus_inf": int(np.isneginf(s64).sum()),
                                                      "skill_vs_O_if_scored_as_is": repr(sk64)},
                         "largest_float32_samples": {"finite_scores": int(np.isfinite(s32).sum()), "of": int(s32.size),
                                                     "skill_vs_O": repr(G.summary(ex, s32, refs)["skill_vs_O"])}}
    checks["score_of_float64_overflow_samples_is_not_finite"] = not np.isfinite(s64).all()        # the finding itself (vw/scoring.py)
    checks["score_of_any_float32_reply_is_finite"] = bool(np.isfinite(s32).all())
    checks["score_extreme_float32_reply_is_worse_than_K"] = G.summary(ex, s32, refs)["skill_vs_O"] < 0
    # the route's answer to such samples: the reply reader refuses float64, so they never reach the score
    one = npz({f"level{l}": S64[l][0] for l in ex.queries})
    try:
        _rules.read_reply(one, mm * sum(len(ts) * ex.dims[l] for l, ts in ex.queries.items()))
        checks["score_overflow_reply_is_refused_before_scoring"] = False
    except ValueError:
        checks["score_overflow_reply_is_refused_before_scoring"] = True

    from physim2_env.lab_tools import make_service
    svc = make_service(hidden, f"units-{os.getpid()}", None)
    n_in = svc.lab.world.n_in
    z = [0.0] * n_in
    fuzz = {
        "inputs_strings": {"op": "advance", "args": {"inputs": [["a"] * n_in]}},
        "inputs_ragged": {"op": "advance", "args": {"inputs": [z, z[:-1]]}},
        "inputs_dict": {"op": "advance", "args": {"inputs": {"a": 1}}},
        "inputs_null": {"op": "advance", "args": {"inputs": [[None] * n_in]}},
        "experiment_scalar_inputs": {"op": "experiment", "args": {"label": "u-d", "inputs": 5}},
        "experiment_bool_n": {"op": "experiment", "args": {"label": "u-b", "n": True}},
        "experiment_float_n": {"op": "experiment", "args": {"label": "u-c", "n": 2.0}},
        "experiment_width": {"op": "experiment", "args": {"label": "u-e", "inputs": [[1.0]]}},
        "experiment_strings": {"op": "experiment", "args": {"label": "u-f", "inputs": [["a"] * n_in]}},
        "experiment_no_block": {"op": "experiment", "args": {"label": "u-g"}},
        "validate_int_path": {"op": "validate", "args": {"path": 3}},
    }
    svc.handle({"op": "reset", "args": {"label": "u-0"}})
    lab_ev = {}
    for name, msg in fuzz.items():
        u0 = svc.usage()
        rep = svc.handle(msg)
        u1 = svc.usage()
        lab_ev[name] = {"ok": rep["ok"], "kind": rep.get("kind"), "error": str(rep.get("error"))[:70], "ticks": u1["ticks_used"] - u0["ticks_used"],
                        "resets": u1["resets"] - u0["resets"]}
    ok = svc.handle({"op": "experiment", "args": {"label": "u-ok", "n": 2}})
    lab_ev["experiment_ok"] = {"ok": ok["ok"], "rows": None if not ok["ok"] else len(ok["result"])}
    evidence["lab"] = lab_ev
    checks["lab_malformed_requests_are_format_rejections_not_infrastructure_errors"] = all(v["kind"] not in ("infrastructure", None) and not v["ok"]
                                                                                             for k, v in lab_ev.items() if k != "experiment_ok")
    checks["lab_rejected_requests_charge_nothing"] = all(v["ticks"] == 0 and v["resets"] == 0 for k, v in lab_ev.items() if k != "experiment_ok")
    checks["lab_good_experiment_still_runs"] = lab_ev["experiment_ok"]["ok"] and lab_ev["experiment_ok"]["rows"] == 3
    import shutil
    shutil.rmtree(svc.dir, ignore_errors=True)
    shutil.rmtree(svc.work, ignore_errors=True)

res = {"package_root": os.path.relpath(os.path.abspath(a.package_root), os.path.dirname(HERE)), "n_checks": len(checks),
       "n_passed": sum(v is True for v in checks.values()), "failed": [k for k, v in checks.items() if v is not True], "checks": checks,
       "evidence": evidence, "hidden_values_in_this_file": "none", "PILOT_NEVER_REUSE_AS_EXAM": bool(a.instance)}
os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
json.dump(res, open(a.out, "w"), indent=1, default=str)
print(json.dumps({k: res[k] for k in ("package_root", "n_checks", "n_passed", "failed")}))
