"""exam_units -- unit checks of round 4's exam-side changes. RUNS ONLY INSIDE A THROWAWAY CONTAINER.

    docker run -d --name NAME --network none --entrypoint sleep physim2-ring:2 infinity      (no mount, no socket)
    tar -cf - research/.../round6/vfport research/.../round5/agentenv research/.../vw1/vw | docker cp - NAME:/
    docker exec -w /research/alife/vecworld/program/round6/vfport NAME python -B tests/exam_units.py
    docker rm -f NAME

It refuses to start anywhere else (no /.dockerenv, or a mount that is not Docker's own): part 6 runs the item
driver with its uid drop and its cleanup, part 2 builds the bundle (which removes its own temporary files), and
the tests remove their own temporary folders. Nothing of this may run on a host. It needs numpy, scipy and jax
(the exam image); it does not need verifiers: the package's submodules are loaded without physim2_env/__init__.

Parts: 1 capture (hostile archives), 2 bundle and baseline, 3 the null policy through round 5's own grader
against grading.null_scores, 4 fallback reasons and records, 5 the laboratory client (log, argument check),
6 validation as graded (a predictor that reads /workspace passes by hand and fails through the laboratory's
route). Prints one JSON object; exit status 0 only if every check passed.
"""
import hashlib
import io
import json
import os
import subprocess
import sys
import tarfile
import tempfile
import time
import types

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)


def refuse_outside_a_container():
    if not os.path.exists("/.dockerenv") or os.geteuid() != 0:
        raise SystemExit("refused: tests/exam_units.py runs only as root inside a throwaway container (no /.dockerenv here)")
    bad = []
    with open("/proc/self/mountinfo") as f:
        for line in f:
            p = line.split(" ")
            mp, fs = p[4], p[p.index("-", 6) + 1]
            ok = (mp == "/" and fs == "overlay") or mp.startswith(("/proc", "/sys", "/dev")) or mp in ("/etc/hostname", "/etc/hosts", "/etc/resolv.conf")
            if not ok:
                bad.append(mp)
    if bad:
        raise SystemExit("refused: this container has mounts that are not Docker's own (" + ", ".join(bad[:4]) + "); start it without -v")


refuse_outside_a_container()
pkg = types.ModuleType("physim2_env")                        # the package without its __init__ (which imports verifiers)
pkg.__path__ = [os.path.join(ROOT, "physim2_env")]
sys.modules["physim2_env"] = pkg

import numpy as np  # noqa: E402

from physim2_env import bundle as BUNDLE  # noqa: E402
from physim2_env import capture as CAPTURE  # noqa: E402
from physim2_env import grading as GRADING  # noqa: E402
from physim2_env.public import _rules  # noqa: E402

CHECKS, T0 = [], time.time()
CFG = "ring_r4"                                              # the ring profile's exam config (256 samples per item, 17-tick reset)
M = 256


def check(name, ok, **detail):
    CHECKS.append({"check": name, "ok": bool(ok), **detail})
    print(("ok   " if ok else "FAIL ") + name + ("" if ok else " " + json.dumps(detail, default=str)[:400]), flush=True)


def tree(root):
    out = []
    for r, ds, fs in os.walk(root):
        for nm in ds + fs:
            p = os.path.join(r, nm)
            st = os.lstat(p)
            out.append((os.path.relpath(p, root), st.st_mode, st.st_size if not os.path.isdir(p) else 0))
    return sorted(out)


# ============================================================================= 1. capture
def member(name, data=b"", typ=tarfile.REGTYPE, link="", size=None, mode=0o644):
    ti = tarfile.TarInfo(name)
    ti.type, ti.linkname, ti.mode = typ, link, mode
    ti.size = len(data) if size is None else size
    return ti, data


def archive(members, cut=None):
    buf = io.BytesIO()
    with tarfile.open(fileobj=buf, mode="w", format=tarfile.GNU_FORMAT) as tar:
        for ti, data in members:
            tar.addfile(ti, io.BytesIO(data) if ti.isreg() else None)
    raw = buf.getvalue()
    return raw if cut is None else raw[:cut]


def part_capture():
    work = tempfile.mkdtemp(prefix="cap-")
    outside = os.path.join(work, "outside.txt")
    open(outside, "w").write("must stay as it is")
    before = tree(work)
    hostile = archive([
        member("workspace/submission", typ=tarfile.DIRTYPE, mode=0o755),
        member("workspace/submission/predict.py", b"print(1)\n"),
        member("workspace/submission/sub/model.npz", b"x" * 1000),
        member("workspace/submission/link", typ=tarfile.SYMTYPE, link="/etc/passwd"),
        member("workspace/submission/up", typ=tarfile.SYMTYPE, link="../../outside.txt"),
        member("workspace/submission/hard", typ=tarfile.LNKTYPE, link="workspace/submission/predict.py"),
        member("workspace/submission/dev", typ=tarfile.CHRTYPE),
        member("workspace/submission/blk", typ=tarfile.BLKTYPE),
        member("workspace/submission/pipe", typ=tarfile.FIFOTYPE),
        member("/etc/cron.d/evil", b"abs"),
        member("workspace/submission/../../outside.txt", b"overwritten"),
        member("../outside.txt", b"overwritten"),
        member("workspace/other/file.txt", b"not below the root"),
        member("workspace/submission/we ird\tna\x01me;$(x).py", b"odd"),
        member("workspace/submission/we_ird_na_me___x_.py", b"collides after sanitising"),
        member("workspace/submission/...", b"dots"),
        member("workspace/submission/" + "d/" * 20 + "deep.txt", b"deep"),
        member("workspace/submission/" + "n" * 300, b"long name"),
        member("workspace/submission/sub/model.npz", b"second copy of a name"),
        member("workspace/submission/café.txt", b"non-ascii"),
    ])
    dest = os.path.join(work, "out")
    man = CAPTURE.extract(hostile, "/workspace/submission", dest)
    got = {f["path"]: f for f in man["files"]}
    why = {}
    for sk in man["skipped"]:
        why.setdefault(sk["why"], []).append(sk["name"])
    check("1 capture: the two plain files are written with the right content",
          open(os.path.join(dest, "predict.py"), "rb").read() == b"print(1)\n" and os.path.getsize(os.path.join(dest, "sub", "model.npz")) == 1000,
          files=sorted(got))
    check("1 capture: sha256 and byte counts of the manifest are those of the files on disk",
          all(hashlib.sha256(open(os.path.join(dest, p), "rb").read()).hexdigest() == f["sha256"] and os.path.getsize(os.path.join(dest, p)) == f["bytes"]
              for p, f in got.items()) and man["bytes"] == sum(f["bytes"] for f in got.values()))
    kinds = {os.path.relpath(os.path.join(r, n), dest): os.lstat(os.path.join(r, n)).st_mode for r, ds, fs in os.walk(dest) for n in ds + fs}
    import stat as S
    check("1 capture: everything written is a regular file (0600) or a directory (0700); no link, device or fifo exists",
          all((S.S_ISREG(m) and S.S_IMODE(m) == 0o600) or (S.S_ISDIR(m) and S.S_IMODE(m) == 0o700) for m in kinds.values()), kinds={k: oct(v) for k, v in kinds.items()})
    for w in ("not a regular file: symbolic link", "not a regular file: hard link", "not a regular file: device", "not a regular file: fifo",
              "absolute path", "parent path", "outside the root", "too deep", "name collision"):
        check(f"1 capture: skipped and listed: {w}", w in why, why=sorted(why))
    check("1 capture: two symbolic links, two devices, two parent paths are each listed",
          len(why.get("not a regular file: symbolic link", [])) == 2 and len(why.get("not a regular file: device", [])) == 2 and len(why.get("parent path", [])) == 2)
    safe = all(all(c.isalnum() or c in "._+=@,-/" for c in p) and ".." not in p.split("/") and not p.startswith("/") for p in got)
    check("1 capture: every kept name is letters, digits and . _ + = @ , - only", safe and "we_ird_na_me___x_.py" in got and "caf_.txt" in got and "___" in got,
          files=sorted(got))
    check("1 capture: a name of 300 characters is cut to 120", any(len(p) == CAPTURE.MAX_NAME for p in got), lens=[len(p) for p in got])
    check("1 capture: nothing outside the destination changed", open(outside).read() == "must stay as it is"
          and [t for t in tree(work) if t[0] != "out" and not t[0].startswith("out/")] == before)
    check("1 capture: the listing escapes names to ASCII", all(all(32 <= ord(c) < 127 for c in sk["name"]) for sk in man["skipped"]))
    try:
        CAPTURE.extract(hostile, "/workspace/submission", dest)
        again = False
    except FileExistsError:
        again = True
    check("1 capture: a destination that exists is refused (never written into)", again)
    # caps: count
    many = archive([member(f"r/f{i:04d}", b"a") for i in range(30)])
    man = CAPTURE.extract(many, "r", os.path.join(work, "many"), max_files=10)
    check("1 capture: the file-count cap holds and the rest is listed", man["n_files"] == 10 and man["n_skipped"] == 20 and len(os.listdir(os.path.join(work, "many"))) == 10
          and not man["complete"])
    # caps: bytes (declared in the header)
    big = archive([member("r/a", b"a" * 600), member("r/b", b"b" * 600), member("r/c", b"c" * 100)])
    man = CAPTURE.extract(big, "r", os.path.join(work, "big"), max_bytes=1000)
    check("1 capture: the byte cap holds; a later file that fits is still taken", man["bytes"] == 700 and sorted(f["path"] for f in man["files"]) == ["a", "c"]
          and man["skipped"][0]["why"] == "size cap")
    # a header that declares more than the archive holds (cut archive)
    cut = archive([member("r/a", b"a" * 100), member("r/b", b"b" * 5000)], cut=512 * 2 + 512 + 700)
    man = CAPTURE.extract(cut, "r", os.path.join(work, "cut"))
    on_disk = sum(os.path.getsize(os.path.join(r, n)) for r, _, fs in os.walk(os.path.join(work, "cut")) for n in fs)
    check("1 capture: an archive cut in the middle of a file ends the pass; that file is not counted as captured",
          [f["path"] for f in man["files"]] == ["a"] and not man["complete"] and on_disk <= CAPTURE.MAX_BYTES, man={k: man[k] for k in ("n_files", "bytes", "archive", "n_skipped")})
    man = CAPTURE.extract(b"this is not a tar archive" * 100, "r", os.path.join(work, "junk"))
    check("1 capture: bytes that are no archive give an empty capture, not an exception", man["n_files"] == 0 and not man["complete"])
    man = CAPTURE.extract(None, "r", os.path.join(work, "none"))
    check("1 capture: no archive: nothing is created", man["n_files"] == 0 and not os.path.exists(os.path.join(work, "none")))
    # a sparse member and a negative size
    sp = member("r/sparse", b"s" * 10)
    sp[0].type = tarfile.GNUTYPE_SPARSE
    man = CAPTURE.extract(archive([sp, member("r/ok", b"ok")]), "r", os.path.join(work, "sparse"))
    check("1 capture: a sparse entry is not written", [f["path"] for f in man["files"]] == ["ok"], man=man["skipped"])
    # the frozen form of a real submission passes whole
    frozen, fman, err = _rules.freeze(archive([member("workspace/submission/predict.py", b"p"), member("workspace/submission/m/x.npz", b"m" * 50)]),
                                      "/workspace/submission", 64)
    man = CAPTURE.extract(frozen, "/workspace/submission", os.path.join(work, "frozen"))
    check("1 capture: a frozen submission is captured complete, file for file",
          man["complete"] and {f["path"]: f["sha256"] for f in man["files"]} == {f["path"]: f["sha256"] for f in fman["files"]})
    lst = CAPTURE.parse_listing("f 12 ./a.txt\nd 4096 ./sub\nl 3 ./ln\nx y z\nf 7 ./we ird\tname\n")
    check("1 capture: the workspace listing is parsed into type, size and an escaped name", lst["n"] == 4 and lst["file_bytes"] == 19 and lst["entries"][3][2] == "./we ird\\tname")
    # the box-side command, run here on a made-up workspace (this container is the box)
    ws = os.path.join(work, "ws")
    os.makedirs(os.path.join(ws, "physim2"))
    os.makedirs(os.path.join(ws, "submission"))
    os.makedirs(os.path.join(ws, "notes", "__pycache__"))
    open(os.path.join(ws, "notes", "plan.md"), "w").write("plan")
    open(os.path.join(ws, "predict.py"), "w").write("misplaced")
    open(os.path.join(ws, "physim2", "x.py"), "w").write("public")
    open(os.path.join(ws, "submission", "predict.py"), "w").write("sub")
    open(os.path.join(ws, "notes", "__pycache__", "c.pyc"), "w").write("cache")
    open(os.path.join(ws, "huge.bin"), "wb").write(b"\0" * (3 << 20))
    os.symlink("/etc/passwd", os.path.join(ws, "ln"))
    tarp = os.path.join(work, "ws.tar")
    r = subprocess.run(["sh", "-c", CAPTURE.workspace_command(ws, tarp)], capture_output=True, text=True)
    man = CAPTURE.extract(open(tarp, "rb").read(), "", os.path.join(work, "wsout"))
    check("1 capture: the workspace command packs small regular files only (no package, no submission/, no cache, no link, no 3 MiB file)",
          r.returncode == 0 and sorted(f["path"] for f in man["files"]) == ["notes/plan.md", "predict.py"], files=man["files"], err=r.stderr[-200:])
    r = subprocess.run(["sh", "-c", CAPTURE.listing_command(ws)], capture_output=True, text=True)
    lst = CAPTURE.parse_listing(r.stdout)
    check("1 capture: the listing command names every entry with type and size", any(e[2] == "./huge.bin" and e[1] == 3 << 20 for e in lst["entries"])
          and any(e[0] == "l" for e in lst["entries"]), n=lst["n"])


# ============================================================================= 2. bundle and baseline
def part_bundle():
    raw, info = BUNDLE.public_bundle("ring", CFG)
    names = tarfile.open(fileobj=io.BytesIO(raw)).getnames()
    check("2 bundle: submission/ holds the baseline predict.py and pool.npz", "submission/predict.py" in names and "submission/pool.npz" in names)
    pool = BUNDLE.null_pool("ring", CFG)
    check("2 bundle: the pool has 512 episodes per level in the exam's shapes", {l: a.shape for l, a in pool.items()} == {1: (512, 5, 6), 2: (512, 2, 3)}
          and all(a.dtype == np.float32 for a in pool.values()), shapes={l: a.shape for l, a in pool.items()})
    other = subprocess.run([sys.executable, "-B", "-c",
                            "import sys, types, os; pkg = types.ModuleType('physim2_env'); pkg.__path__ = [os.path.join(%r, 'physim2_env')]; sys.modules['physim2_env'] = pkg\n"
                            "from physim2_env import bundle as B\n"
                            "raw, info = B.public_bundle('ring', 'ring_r4'); print(info['baseline']['pool_sha256'], info['baseline']['files']['pool.npz'])" % ROOT],
                           capture_output=True, text=True)
    check("2 bundle: another process builds the same pool and the same pool.npz bytes",
          other.stdout.split() == [info["baseline"]["pool_sha256"], info["baseline"]["files"]["pool.npz"]], out=other.stdout[-200:], err=other.stderr[-300:])
    md = info["task_md"]
    for needle in ("**Turns: at most 150.**", "**Wall-clock time: 60 minutes**", "2 CPU cores, 4 GiB of memory",
                   "at most 512 processes and threads", "`/workspace` (1024 MiB) and `/tmp` (512 MiB) and nowhere else",
                   "Whatever is in `submission/` at the moment your run ends is graded", "the same 3 hidden numbers",
                   "/workspace/lab_log.jsonl", "A failed item is scored with the baseline's forecast", "an integer T for T ticks without input",
                   "from a clean copy of `submission/` alone", "`turns_used` and `turns_left`", "you never see their results",
                   "costs 17 ticks", "as much as the 17 observations of one item's history", "The grader asks for n_samples = 256",
                   "over pairs of DIFFERENT samples", "Your 256 samples are treated as independent draws", "how you are scored is public"):
        check(f"2 statement (default limits) says: {needle[:60]}", needle in md)
    check("2 statement: no sentence promises K for a failure", "scored as K" not in md)
    run = dict(BUNDLE.default_run("ring", CFG), max_turns=22, wall_minutes=45, max_output_tokens_per_turn=16384, max_context_tokens=70000,
               cap_usd=19.5, cpus=1.5, memory_gib=2, pids=512, measured=True)
    md2 = BUNDLE.statement("ring", CFG, run)
    for needle in ("**Turns: at most 22.**", "reply number 22", "**Wall-clock time: 45 minutes**", "**One reply: at most 16384 tokens**", "**Context: 70,000 tokens.**",
                   "**Spend: 19.5 US dollars**", "1.5 CPU cores, 2 GiB of memory", "at most 512 processes and threads", "(Measured in this box when it started.)",
                   "`context_tokens_used`"):
        check(f"2 statement (a run's own limits) says: {needle[:60]}", needle in md2)
    md3 = BUNDLE.statement("ring", CFG, dict(run, max_turns=None, max_context_tokens=None, cap_usd=None, pids=None, lab_counts_turns=False,
                                             workspace_mib=None, tmp_mib=None, read_only_root=False))
    check("2 statement: without a turn cap it says so, without a context cap it names the model's window, and an uncapped box is described as such",
          "no limit on the number of turns" in md3 and "must fit your model's context window" in md3 and "Spend" not in md3 and "does not count turns" in md3
          and "no limit of its own on the number of processes" in md3 and "no disk quota of its own" in md3)
    old = BUNDLE.statement("ring", "smoke_ring")
    check("2 statement: round 5's exam config still renders, with its own numbers (32 samples, a 1-tick reset)",
          "The grader asks for n_samples = 32" in old and "costs 1 ticks" in old and "as much as the" not in old)
    try:
        BUNDLE.null_pool("gliders", "smoke_gliders")
        guard = "no error"
    except RuntimeError as e:
        guard = str(e)
    check("2 bundle: a world this pin builds no baseline pool for is refused at once (no hours of simulation behind a config name)",
          guard.startswith("this pin builds no baseline pool for world 'gliders'"), guard=guard[:120])
    # ruling E15: what a box holds at start
    groups = info["file_groups"]
    listed = [f for g in groups for f in g["files"]]
    check("2 box contents: every file of the bundle is in exactly one named group", sorted(listed) == sorted(n for n in names if n not in ("physim2", "submission") and not n.endswith("/"))
          or sorted(listed) == sorted(set(listed)), n=len(listed), groups=[g["group"] for g in groups])
    check("2 box contents: the designers' closed-form library and the toy worlds are not shipped; the scoring code is, in its own group",
          not any("lingauss" in n or "toys" in n for n in names) and any(g["group"].endswith("scoring.py") and g["files"] for g in groups))
    # the baseline through the public runner, as a predictor process
    work = tempfile.mkdtemp(prefix="base-")
    with tarfile.open(fileobj=io.BytesIO(raw)) as tar:
        tar.extractall(work, filter="data")
    ex = np.load(os.path.join(work, "physim2", "examples.npz"))
    card = json.load(open(os.path.join(work, "physim2", "exam.json")))
    outs = []
    for seed in (0, 0, 1):
        rq, rp = os.path.join(work, f"rq{len(outs)}.npz"), os.path.join(work, f"rp{len(outs)}.npz")
        np.savez(rq, history=ex["history"][0], prefix=ex["prefix"][0], test=ex["test"][0], queries=json.dumps(card["exam"]["queries"]), n_samples=M, seed=seed)
        r = subprocess.run([sys.executable, "-I", "-B", os.path.join(work, "physim2", "predict_runner.py"), os.path.join(work, "submission"), rq, rp],
                           capture_output=True, text=True)
        outs.append(dict(np.load(rp)) if r.returncode == 0 else r.stderr)
    ok = all(isinstance(o, dict) for o in outs)
    check("2 baseline: runs through predict_runner.py and returns the exam's shapes", ok and outs[0]["level1"].shape == (M, 5, 6) and outs[0]["level2"].shape == (M, 2, 3),
          out=str(outs[0])[:200] if not ok else None)
    check("2 card: the public card states the price of a reset (17 ticks) and 256 samples", card["ticks"]["reset_cost"] == 17 and card["exam"]["n_samples"] == M)
    # ruling E15: the public simulator and the reference agents' own modules work in the trimmed box
    code = ("import sys, numpy as np; sys.path.insert(0, %r); sys.path.insert(0, %r)\n"
            "import physim2; W = physim2.load_world(); rng = np.random.default_rng(0)\n"
            "th = W.prior_sample(rng, 4); sim = W.Simulator(chunk=4); ep = sim.episodes(th, 3)\n"
            "fr = sim.free_run(th, 5, 8); w = W.build_world(W.PRIOR_MEAN); v = W.viable(th, seed=1)\n"
            "U = W.draw_program(W.program_mix().names[1], rng, ep['obs'][0, :17], 32); l2 = W.level(2, ep['obs']); sc = W.scales(); nb = W.nats_budget()\n"
            "import inference, ridge_family\n"
            "m = ridge_family.fit('ring', ep['obs'], ep['U'], {1: [1, 2], 2: [16]}, sc)\n"
            "print('SIM-OK', ep['obs'].shape, fr.shape, l2.shape, sorted(k for k in sys.modules if k.startswith('vw.')))\n"
            % (work, os.path.join(ROOT, "..", "..", "round5", "agentenv", "agents")))
    r = subprocess.run([sys.executable, "-I", "-B", "-c", code], capture_output=True, text=True)
    check("2 box contents: the public simulator (episodes, free_run, build_world, viable, draw_program, level, scales) and the reference "
          "agents' modules run in the trimmed box", "SIM-OK (4, 49, 6) (4, 9, 6)" in r.stdout and "vw.lingauss" not in r.stdout and "vw.scoring" in r.stdout,
          out=r.stdout[-300:], err=r.stderr[-400:])
    check("2 baseline: same seed, same samples; another seed, other samples",
          ok and np.array_equal(outs[0]["level1"], outs[1]["level1"]) and not np.array_equal(outs[0]["level1"], outs[2]["level1"]))
    return work, raw, info


# ============================================================================= 3. the null policy and round 5's grader
def part_null(work):
    sys.path.insert(0, os.path.join(ROOT, "..", "..", "round5", "agentenv"))
    from evaluator import acceptance as ACC
    from evaluator import build_workspace as BW
    from evaluator import grader as GR
    from evaluator import instance as INST
    store = tempfile.mkdtemp(prefix="inst-")
    hidden = os.path.join(store, "unit-w0", "hidden")
    os.makedirs(os.path.dirname(hidden))
    os.chmod(store, 0o755)                                   # round 5's sandbox runs the predictor as uid 65534: its request
    os.chmod(os.path.dirname(hidden), 0o755)                 # folder (<store>/<instance>/work) must be reachable; hidden/ stays 0700
    from physim2_env._paths import config_path
    cfg = json.load(open(config_path(CFG)))
    INST.make_instance("ring", cfg, hidden)
    INST.build_exam(hidden, log=lambda *_: None)
    ex = INST.FrozenExam(hidden)
    fb = GRADING.fallback(hidden, "ring", CFG, M, 0)
    pub = tempfile.mkdtemp(prefix="pub-")
    os.chmod(pub, 0o755)
    BW.build("ring", BUNDLE.load_config(CFG), pub)
    sub = os.path.join(work, "submission")
    for r_, ds, fs in os.walk(work):
        os.chmod(r_, 0o755)
    g = GR.grade(hidden, sub, os.path.join(pub, "public"), "null_round5", log=lambda *_: None)
    es5 = np.load(os.path.join(hidden, "grades", "null_round5.npz"))["es"]
    check("3 null: round 5's own grader (evaluator.grader.grade) runs the baseline on all 64 items without a failure", g["n_failed"] == 0, layers=g.get("layers"))
    check("3 null: grading.null_scores equals, item by item and cell by cell, what round 5's grader gives the baseline in submission/",
          es5.shape == fb["es"].shape and np.array_equal(es5, fb["es"]), max_abs_difference=float(np.abs(es5 - fb["es"]).max()))
    refs = ex.references()
    s = GRADING.summary(ex, fb["es"], refs)
    valid = np.array(s["valid_cells"], bool)
    L = lambda a: float(a[:, valid].sum(1).mean())  # noqa: E731
    want = (L(refs["K"]) - L(fb["es"])) / (L(refs["K"]) - L(refs["O"]))
    tab = ACC.skill({"K": refs["K"], "O": refs["O"], "agent": fb["es"]}, valid)["agent"]["vs_O"]
    check("3 null: its skill is (L(K) - L) / (L(K) - L(O)) on the K-to-O scale, K = 0 and O = 1 unchanged",
          abs(s["skill_vs_O"] - want) < 1e-12 and s["skill_vs_O"] == tab and GRADING.summary(ex, refs["K"], refs)["skill_vs_O"] == 0.0
          and abs(GRADING.summary(ex, refs["O"], refs)["skill_vs_O"] - 1.0) < 1e-12, skill_null=s["skill_vs_O"])
    check("3 null: the null policy is not K (it differs on every item) and scores below K here or near it", not np.array_equal(fb["es"], refs["K"]),
          skill_null=round(s["skill_vs_O"], 4))
    g = GRADING.score_as_null(hidden, "unit-all-null", "no predict.py", fb, detail="unit test")
    rec = json.load(open(os.path.join(hidden, "grades", "unit-all-null.json")))
    z = np.load(os.path.join(hidden, "grades", "unit-all-null.npz"))
    check("3 fallback: a run without a predictor gets the null policy's scores on every item, and the record says which and why",
          np.array_equal(z["es"], fb["es"]) and z["failed"].all() and g["skill_vs_O"] == s["skill_vs_O"] and rec["fallback"]["by_reason"] == {"no predict.py": 64}
          and len(rec["fallback_items"]) == 64 and rec["fallback"]["baseline_pool_sha256"] == fb["pool_sha256"] and rec["fallback"]["policy"] == "null")
    check("3 fallback: such a run no longer scores 0.000 (K)", g["skill_vs_O"] != 0.0, skill=g["skill_vs_O"])
    return hidden, fb


# ============================================================================= 4. fallback reasons
def part_reasons():
    R = GRADING.fallback_reason
    cases = [
        ({"skip": "grading ran out of time"}, None, "not run"),
        ({"ok": False, "why": "infrastructure", "stderr": "no box"}, None, "infrastructure"),
        ({"ok": False, "why": "driver error", "stderr": "x"}, None, "infrastructure"),
        ({"ok": False, "why": "wall-clock limit", "stderr": ""}, None, "timed out"),
        ({"ok": False, "why": "CPU-time limit", "stderr": ""}, None, "timed out"),
        ({"ok": False, "why": "no reply file (missing)", "stderr": ""}, None, "unreadable reply"),
        ({"ok": False, "why": "reply too large", "stderr": ""}, None, "unreadable reply"),
        ({"ok": False, "why": "exit code 2", "returncode": 2, "stderr": "ValueError: predict: level 1 has shape (3, 5, 6), expected (32, 5, d)\n"}, None, "wrong shape"),
        ({"ok": False, "why": "exit code 2", "returncode": 2, "stderr": "KeyError: 'predict: level 2 missing from the returned dict'\n"}, None, "wrong shape"),
        ({"ok": False, "why": "exit code 2", "returncode": 2, "stderr": "TypeError: predict must return a dict {level: array}\n"}, None, "wrong shape"),
        ({"ok": False, "why": "exit code 2", "returncode": 2, "stderr": "ValueError: predict: level 1 has non-finite values\n"}, None, "non-finite values"),
        ({"ok": False, "why": "exit code 2", "returncode": 2, "stderr": "ZeroDivisionError: division by zero\n"}, None, "raised"),
        ({"ok": False, "why": "exit code 2", "returncode": 2, "stderr": "MemoryError: Unable to allocate 64.0 GiB\n"}, None, "out of memory"),
        ({"ok": False, "why": "exit code -9", "returncode": -9, "stderr": ""}, None, "killed"),
        ({"ok": False, "why": "exit code 1", "returncode": 1, "stderr": "ValueError: predict: level 1 has non-finite values printed by the predictor itself\nRuntimeError: boom\n"}, None, "raised"),
        ({"ok": True}, "unreadable reply: the reply is not an .npz file", "unreadable reply"),
        ({"ok": True}, "level 1 has shape (32, 5, 7), expected (32, 5, 6)", "wrong shape"),
        ({"ok": True}, "level 2 missing", "wrong shape"),
        ({"ok": True}, "level 1 has non-finite values", "non-finite values"),
    ]
    bad = [(r, b, want, R(r, b)) for r, b, want in cases if R(r, b) != want]
    check(f"4 reasons: {len(cases)} driver records and verdicts map to the expected word", not bad, bad=bad[:3])
    check("4 reasons: every word is one of the fixed list", all(R(r, b) in GRADING.FALLBACK_REASONS for r, b, _ in cases))


# ============================================================================= 5. the laboratory client
def part_client(work):
    for k in [k for k in sys.modules if k == "physim2" or k.startswith("physim2.")]:
        del sys.modules[k]                                   # part 3 imported agentenv's own physim2; this part needs the bundle's
    sys.path.insert(0, work)
    os.environ["PHYSIM2_LAB_LOG"] = os.path.join(work, "lab_log.jsonl")
    os.environ["PHYSIM2_LAB"] = "http://127.0.0.1:9/mcp"
    import physim2
    from physim2 import labclient as LC
    lab = physim2.Lab()
    sent = []

    def fake(op, **args):
        sent.append((op, args))
        lab._n += 1
        if op == "advance" and "inputs" in args and np.abs(args["inputs"]).max() > 3:
            raise LC.LabError("violation: input out of bounds", "violation")
        T = args.get("n") or len(args.get("inputs", []))
        return {"ticks_used": 0} if op == "usage" else np.arange(6.0 * (T + (op == "experiment"))).reshape(-1, 6).tolist()
    lab._send = fake
    bad = []
    for call in (lambda: lab.experiment("e", None), lambda: lab.experiment("e", []), lambda: lab.experiment("e", "16"), lambda: lab.experiment("e", True),
                 lambda: lab.experiment("e", 0), lambda: lab.experiment("e", 5000), lambda: lab.experiment("e", np.zeros(24)), lambda: lab.experiment("e", np.zeros((4, 23))),
                 lambda: lab.experiment("e", np.full((2, 24), np.nan)), lambda: lab.experiment("e", [[1, 2], [3]]), lambda: lab.advance(None), lambda: lab.advance({"n": 3}),
                 lambda: lab.advance(-1)):
        try:
            call()
            bad.append("no error")
        except LC.LabError as e:
            if not str(e).startswith("usage: lab.") or "\n" in str(e) or "an integer T" not in str(e) or "(T, 24)" not in str(e):
                bad.append(str(e))
        except Exception as e:                               # a traceback from json or numpy is what round 4 removes
            bad.append(type(e).__name__)
    check("5 client: 13 bad inputs arguments each raise LabError with ONE line of usage that names the integer form and (T, 24)", not bad, bad=bad[:3])
    check("5 client: a bad argument sends nothing", sent == [])
    a = lab.experiment("free-1", 16)
    b = lab.experiment("push-1", np.zeros((4, 24)))
    c = lab.advance(np.int64(3))
    try:
        lab.advance(np.full((1, 24), 9.0))
    except LC.LabError:
        pass
    lab.usage()
    check("5 client: the integer form and the array form are sent as n and as inputs",
          sent[0] == ("experiment", {"label": "free-1", "n": 16}) and sent[1][0] == "experiment" and sent[1][1]["inputs"].shape == (4, 24) and sent[2] == ("advance", {"n": 3})
          and a.shape == (17, 6) and b.shape == (5, 6) and c.shape == (3, 6))
    log = physim2.Lab.read_log()
    check("5 client: every reply is appended to the log with its full arrays, and the rejected call with its error",
          [e["op"] for e in log] == ["experiment", "experiment", "advance", "advance", "usage"] and [e["ok"] for e in log] == [True, True, True, False, True]
          and np.array_equal(np.asarray(log[0]["result"]), a) and np.asarray(log[1]["args"]["inputs"]).shape == (4, 24) and log[3]["kind"] == "violation"
          and all(isinstance(e["t"], float) for e in log), ops=[e.get("op") for e in log])
    lab.log_path = "/proc/no-such-dir/log.jsonl"
    try:
        lab.advance(2)
        quiet = True
    except Exception:
        quiet = False
    check("5 client: a log that cannot be written never breaks a call", quiet)


# ============================================================================= 6. validation as graded
def part_validate(raw):
    ws = "/workspace"
    if os.path.exists(ws) and os.listdir(ws):
        check("6 validate: /workspace of this container is empty before the test", False)
        return
    os.makedirs(ws, exist_ok=True)
    os.makedirs("/etc/physim2", exist_ok=True)
    uid = 23456
    open("/etc/physim2/predictor_uid", "w").write(f"{uid}\n")
    os.chmod("/etc/physim2", 0o755)
    os.chmod("/etc/physim2/predictor_uid", 0o644)
    with tarfile.open(fileobj=io.BytesIO(raw)) as tar:
        tar.extractall(ws, filter="data")
    os.chmod(ws, 0o755)
    code = "import json, sys\nsys.path.insert(0, sys.argv[1])\nimport physim2.validate as V\nprint(json.dumps(V.check(sys.argv[2]), default=str))\n"
    route = dict(os.environ, PHYSIM2_BOX_CLEANUP="disposable-box")
    route.pop("PHYSIM2_LAB_LOG", None)

    def lab_route(path="submission"):
        r = subprocess.run([sys.executable, "-B", "-c", code, ws, path], capture_output=True, text=True, env=route)
        try:
            return json.loads(r.stdout.strip().splitlines()[-1])
        except Exception:
            return {"ok": None, "stderr": r.stderr[-500:], "stdout": r.stdout[-300:]}

    def by_hand(path="submission"):
        env = {k: v for k, v in os.environ.items() if k != "PHYSIM2_BOX_CLEANUP"}
        r = subprocess.run([sys.executable, "-B", "-m", "physim2.validate", path], capture_output=True, text=True, cwd=ws, env=env)
        try:
            return json.loads(r.stdout)
        except Exception:
            return {"ok": None, "stderr": r.stderr[-500:], "stdout": r.stdout[-300:]}

    rep = lab_route()
    check("6 validate: the baseline passes through the laboratory's route, as an unprivileged user, as graded",
          rep.get("ok") is True and rep.get("as_graded") is True and "fresh container that holds only submission/" in rep.get("grading", "")
          and "could not read /workspace" in rep.get("grading", ""), rep={k: rep.get(k) for k in ("ok", "stage", "error", "as_graded", "stderr")})
    import stat as S
    check("6 validate: /workspace has its mode back afterwards (0755)", S.S_IMODE(os.lstat(ws).st_mode) == 0o755)
    # the first rollout's mistake: a predictor that loads a file from /workspace, outside submission/
    np.save(os.path.join(ws, "episodes.npy"), np.zeros(3))
    os.makedirs(os.path.join(ws, "leaky"))
    open(os.path.join(ws, "leaky", "predict.py"), "w").write(
        "import numpy as np\n\ndef predict(history, program, queries, n_samples, seed):\n"
        "    np.load('/workspace/episodes.npy')\n"
        "    return {1: np.zeros((n_samples, 5, 6)), 2: np.zeros((n_samples, 2, 3))}\n")
    hand, route_rep = by_hand("leaky"), lab_route("leaky")
    check("6 validate: a predictor that reads /workspace/episodes.npy PASSES when the agent runs the check itself, and the reply says that this proves nothing",
          hand.get("ok") is True and hand.get("as_graded") is False and "YOUR rights" in hand.get("grading", ""), rep={k: hand.get(k) for k in ("ok", "error", "as_graded", "stderr")})
    check("6 validate: the same predictor FAILS through the laboratory's route, as it would in grading (round 4; before, it passed)",
          route_rep.get("ok") is False and route_rep.get("stage") == "example 0" and "PermissionError" in route_rep.get("error", ""),
          rep={k: str(route_rep.get(k))[:300] for k in ("ok", "stage", "error", "stderr")})
    check("6 validate: /workspace has its mode back after a failed check too", S.S_IMODE(os.lstat(ws).st_mode) == 0o755)
    # a predictor that names its own file by an absolute path below /workspace/submission
    os.makedirs(os.path.join(ws, "abs"))
    np.save(os.path.join(ws, "abs", "m.npy"), np.zeros(3))
    open(os.path.join(ws, "abs", "predict.py"), "w").write(
        "import os, numpy as np\n\ndef predict(history, program, queries, n_samples, seed):\n"
        "    np.load(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'm.npy'))\n"
        "    return {1: np.zeros((n_samples, 5, 6)), 2: np.zeros((n_samples, 2, 3))}\n")
    rep = lab_route("abs")
    check("6 validate: a predictor that loads its own file relative to predict.py passes as graded", rep.get("ok") is True and rep.get("as_graded") is True,
          rep={k: str(rep.get(k))[:300] for k in ("ok", "stage", "error")})
    # a changed public package is reported
    open(os.path.join(ws, "physim2", "world_ring.py"), "a").write("\n# edited by the agent\n")
    rep = lab_route()
    check("6 validate: an edited physim2/ is counted and the reply says the grader uses the original",
          rep.get("package_changed_files") == 1 and "the grader uses the original" in rep.get("grading", ""), n=rep.get("package_changed_files"))
    left = [p for p in os.listdir("/tmp") if p.startswith(("physim2-validate-", "physim2-req-", "physim2-io-"))]
    check("6 validate: no temporary folder of the check is left", not left, left=left)


def main():
    part_capture()
    work, raw, info = part_bundle()
    part_null(work)
    part_reasons()
    part_client(work)
    part_validate(raw)
    out = {"tool": "tests/exam_units.py", "where": "a throwaway container (no mount, no network), as root", "n_checks": len(CHECKS),
           "n_passed": sum(c["ok"] for c in CHECKS), "failed": [c["check"] for c in CHECKS if not c["ok"]], "seconds": round(time.time() - T0, 1),
           "baseline_pool_sha256": info["baseline"]["pool_sha256"], "checks": CHECKS}
    print(json.dumps({k: out[k] for k in ("n_checks", "n_passed", "failed", "seconds")}))
    with open("/tmp/exam_units.json", "w") as f:
        json.dump(out, f, indent=1, default=str)
    return 0 if out["n_checks"] == out["n_passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
