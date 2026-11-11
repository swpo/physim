"""The reward's work: the frozen predictor on the frozen exam, request by request in a verifier box, scored on
the worker.

Order of work (all of it after the agent's box is gone):

  1. validation     the three public example calls of round 5 (evaluator/submission.py:105-125: example 0 twice
                    with the same seed, example 1), run in the verifier box verifiers gave us and compared ON THE
                    WORKER. A predictor that fails one of them is not graded item by item (round 5's rule: only
                    a validated predictor is frozen, run_rollout.py:97-108): every item falls back (below).
  2. the exam       one request at a time (memo hole 1). `isolation="box"` (default): every item gets a FRESH box
                    from verifiers' `provision_runtime` with the verifier's own resolved config (same image, same
                    network policy), staged like the verifier box and destroyed after its one request, so that
                    nothing in a box can carry from one item to the next. `isolation="shared"`: all items in the
                    one verifier box, with the driver's cleanup between them (cheaper; a pilot mode, because
                    timestamps, the process-id counter and kernel counters of a box survive that cleanup).
  3. scoring        agentenv's arithmetic, unchanged and by import -- FrozenExam.request / score / references
                    (evaluator/instance.py:149-172), check_shapes (evaluator/submission.py:94-102), pooled L and
                    skill (evaluator/acceptance.py:61-68). Added: a reply must be what predict_runner.py writes
                    (float32, one array per level; _rules.read_reply) and an item whose score is not finite is a
                    failed item.

THE FALLBACK (round 4, ruling E3). Round 5 scored a failed item as K, the climatology of the HIDDEN world, which
no agent can know: failing was paid (an empty submission scored 0.000, the honest null agent -0.040). Now an
item without a valid forecast -- no predictor, a failed validation, an error, a time-out, a wrong shape,
non-finite values, an unreadable reply, a score that is not finite, no box -- is scored with the forecast of
the NULL policy for that item: the baseline every box starts with (bundle.null_pool; public prior only),
computed here on the worker by the baseline's own predict function (null_scores). Never K. The grade record
lists every item that fell back and one word from FALLBACK_REASONS for why. The scale (K = 0, O = 1) and the
arithmetic of every valid forecast are untouched.

Truths, the climatology pool, item ids and program classes never enter a box. In every box the predictor runs
through public/_item.py as an unprivileged user (a random uid per rollout) under the declared limits.
"""
from __future__ import annotations

import asyncio
import base64
import contextlib
import io
import json
import os
import re
import secrets
import time

import numpy as np

from ._paths import use_agentenv
from .public import _rules

RUNTIME_DIR = "/runtime"
BOX_DIR = "/etc/physim2"                                     # the marker of a prepared box (public/_item.py: require_box)
ROUTE_ENV = {"PHYSIM2_BOX_CLEANUP": "disposable-box"}        # set on the grading route's own commands, nowhere else
CONTAINER_RUNTIMES = ("docker", "prime")
VF_CONTAINER_NAME = re.compile(r"^vf-[0-9a-f]{32}$")         # the name verifiers gives a container it creates itself


def container_gate(runtime) -> list[str]:
    """Why `runtime` is NOT a box that verifiers itself provisioned (empty list = it is). Every command this
    package sends through a verifiers Runtime changes files as root (mkdir, chown, chmod -R, tar -x, rm, the
    driver's cleanup), so the object must be the real thing, not something that merely says "docker":
      class     exactly verifiers' DockerRuntime or PrimeRuntime (a `with_env` view keeps the class); never a
                test double, the subprocess runtime (the worker itself) or another engine
      type      its config says the same ("docker" for DockerRuntime, "prime" for PrimeRuntime)
      owned     not borrowed (`info.borrowed`): `DockerRuntime.attach` wraps a container somebody else started,
                for example by hand with a host folder mounted; verifiers' own `start()` passes no mount
      docker    not nested in another runtime, and the container carries the name verifiers generated"""
    why = []
    try:
        from verifiers.v1.runtimes import DockerRuntime, PrimeRuntime
    except Exception as e:                                   # no verifiers, no gate that could pass
        return [f"verifiers' runtime classes cannot be imported ({type(e).__name__})"]
    cls = type(runtime)
    typ = getattr(getattr(runtime, "config", None), "type", None)
    want = {DockerRuntime: "docker", PrimeRuntime: "prime"}.get(cls)
    if want is None:
        why.append(f"{cls.__module__}.{cls.__qualname__} is not verifiers' Docker or Prime runtime")
    elif typ != want:
        why.append(f"runtime type {typ!r} does not belong to {cls.__name__}")
    if getattr(getattr(runtime, "info", None), "borrowed", True) is not False:
        why.append("the box was not provisioned by verifiers for this run (borrowed, or no runtime info)")
    if cls is DockerRuntime:
        if getattr(runtime, "_host", None) is not None:
            why.append("a Docker engine nested in another runtime")
        if not VF_CONTAINER_NAME.match(str(getattr(runtime, "_container", None) or "")):
            why.append("the container does not carry a name verifiers generated")
    return why


def require_container(runtime) -> None:
    """Refuse (RuntimeError) unless `runtime` is a container verifiers itself provisioned: see container_gate.
    Called before EVERY command this package sends into a box."""
    why = container_gate(runtime)
    if why:
        raise RuntimeError("refused: not a box provisioned by verifiers (" + "; ".join(why) + "); nothing of physim2_env runs "
                           "anywhere else")
SLACK_S = 120.0                                              # worker-side allowance per request beyond the wall limit
BOX_S = 240.0                                                # ... and for provisioning and staging a fresh box


UID_RANGE = (20000, 59999)                                   # the driver accepts no other uid (public/_item.py: MIN_UID, MAX_UID)


def new_uid() -> int:
    """The predictor's uid in the boxes of ONE rollout (and, drawn again, in the agent's box). Process limits are
    counted per uid across every container that shares the host's user namespace, so a fixed uid would let one
    rollout's predictor starve another's."""
    return UID_RANGE[0] + secrets.randbelow(UID_RANGE[1] - UID_RANGE[0] + 1)


def exam(hidden: str):
    use_agentenv()
    from evaluator import instance as INST
    return INST.FrozenExam(hidden)


def npz_bytes(req: dict) -> bytes:
    buf = io.BytesIO()
    np.savez(buf, **req)
    return buf.getvalue()


def save(hidden: str, name: str, es, failed, cpu, record: dict) -> None:
    """Per-item scores stay on the worker, in the format evaluator.grader.table() reads."""
    os.makedirs(os.path.join(hidden, "grades"), exist_ok=True)
    np.savez_compressed(os.path.join(hidden, "grades", f"{name}.npz"), es=es, failed=failed, cpu=cpu)
    json.dump(record, open(os.path.join(hidden, "grades", f"{name}.json"), "w"), indent=1)


def summary(ex, es, refs) -> dict:
    """Pooled L of this predictor, of K and of O, and the skill on the K-to-O scale, over the cells whose
    K-to-O gap is significant (vw.scoring.cells_ok, decided on the references before any agent): the same
    number as policies[...]["vs_O"] of evaluator.grader.table for this world."""
    use_agentenv()
    from evaluator import acceptance as ACC
    from vw.scoring import cells_ok
    valid = np.asarray(cells_ok(refs["K"], refs["O"], 3.0), bool)
    if not valid.any():
        valid = np.ones(len(valid), bool)
    s = ACC.skill({"K": refs["K"], "O": refs["O"], "agent": es}, valid)
    return {"L": s["agent"]["L"], "L_K": s["K"]["L"], "L_O": s["O"]["L"], "skill_vs_O": s["agent"]["vs_O"],
            "valid_cells": valid.tolist()}


# ---- the fallback (ruling E3) ----
FALLBACK_REASONS = ("no predict.py", "no submission", "validation failed", "raised", "killed", "timed out", "out of memory",
                    "wrong shape", "non-finite values", "unreadable reply", "score not finite", "not reproducible",
                    "infrastructure", "not run", "grading error", "ungraded run")
_SHAPE = re.compile(r"^(ValueError: predict: level -?\d+ has shape|KeyError: .predict: level -?\d+ missing|TypeError: predict must return a dict)")
_NONFINITE = re.compile(r"^ValueError: predict: level -?\d+ has non-finite values")


def fallback_reason(r: dict | None, bad: str | None) -> str:
    """One word from FALLBACK_REASONS for a request that gave no valid forecast: `r` is the driver's record (or a
    skip), `bad` the worker's verdict on the reply. Decided from fixed patterns only; the predictor's own text is
    never copied into the reason."""
    r = r or {}
    if "skip" in r:
        return "not run"
    if r.get("why") in ("infrastructure", "driver error") or r.get("driver_error"):
        return "infrastructure"
    if not r.get("ok"):
        why = str(r.get("why") or "")
        if why in ("wall-clock limit", "CPU-time limit"):
            return "timed out"
        if why.startswith("no reply file") or why == "reply too large":
            return "unreadable reply"
        lines = [x for x in str(r.get("stderr") or "").splitlines() if x.strip()]
        last = lines[-1].strip() if lines else ""
        if _SHAPE.match(last):
            return "wrong shape"
        if _NONFINITE.match(last):
            return "non-finite values"
        if last.startswith("MemoryError") or "MemoryError" in last[:80]:
            return "out of memory"
        rc = r.get("returncode")
        return "killed" if isinstance(rc, int) and rc < 0 else "raised"
    bad = str(bad or "")
    if bad.startswith("unreadable reply"):
        return "unreadable reply"
    if "non-finite" in bad:
        return "non-finite values"
    if "has shape" in bad or bad.endswith("missing"):
        return "wrong shape"
    return "raised"


def null_scores(ex, pool: dict, m: int, seed: int = 0) -> np.ndarray:
    """Fair energy score per (item, cell) of the NULL policy's forecast: what the baseline in submission/ returns
    for the grader's request (n_samples = m, the grader's seed), scored like any forecast. The forecast is made by
    the baseline's OWN predict function (public/baseline_predict.py, a file of this package: no submitted code)
    on the pool the box was given, and passes through the same float32 reply format as a graded predictor.
    The null policy ignores history and program, so every item gets the same samples; the scores differ with
    the item's real futures."""
    import importlib.util
    spec = importlib.util.spec_from_file_location("physim2_baseline_predict", os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                                                         "public", "baseline_predict.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    mod._P = {f"level{l}": np.asarray(pool[l]) for l in pool}
    out = mod.predict(None, None, {l: list(ts) for l, ts in ex.queries.items()}, int(m), int(seed))
    S = {}
    for l, ts in ex.queries.items():
        a = np.asarray(out[l], np.float64).astype(np.float32).astype(np.float64)     # the reply's round trip
        if a.shape != (m, len(ts), ex.dims[l]) or not np.all(np.isfinite(a)):
            raise RuntimeError("the null policy's pool does not fit the exam")
        S[l] = np.broadcast_to(a[None], (ex.n,) + a.shape)
    with np.errstate(all="ignore"):
        sc = ex.score(S)
    if not np.all(np.isfinite(sc)):
        raise RuntimeError("the null policy's score is not finite")
    return sc


def fallback(hidden: str, world: str, config_name: str, m: int | None = None, seed: int = 0) -> dict:
    """{"es": the null policy's scores (items, cells), "pool_sha256": which pool}: what a failed item is scored with."""
    from . import bundle as BUNDLE
    ex = exam(hidden)
    pool = BUNDLE.null_pool(world, config_name)
    m = int(m or BUNDLE.load_config(config_name)["predictor"]["n_samples"])
    return {"es": null_scores(ex, pool, m, seed), "pool_sha256": BUNDLE.pool_sha256(pool), "policy": "null"}


def fallback_summary(reasons: dict, fb: dict) -> dict:
    """What a trace says about the fallback: counts by reason, never an item or a predictor's text."""
    by = {}
    for why in reasons.values():
        by[why] = by.get(why, 0) + 1
    return {"policy": fb.get("policy", "null"), "baseline_pool_sha256": fb.get("pool_sha256"), "n_items": len(reasons), "by_reason": by}


def score_as_null(hidden: str, name: str, reason: str, fb: dict, extra: dict | None = None, detail: str | None = None) -> dict:
    """No usable predictor: EVERY item is scored with the null policy's forecast (ruling E3; round 5 scored K
    here, run_rollout.finalize, lines 103-108). `reason` is one word of FALLBACK_REASONS, optionally followed by
    ": " and a second one; `detail` (free text, may quote a predictor) stays in the store's record."""
    ex = exam(hidden)
    refs = ex.references()
    es = np.array(fb["es"], float)
    reasons = {i: reason for i in range(ex.n)}
    rec = dict({"name": name, "n_items": ex.n, "n_failed": ex.n, "reason": reason, "detail": detail, "errors": [], "seconds": 0.0,
                "fallback": fallback_summary(reasons, fb), "fallback_items": [{"item": i, "reason": reason} for i in range(ex.n)]},
               **(extra or {}))
    save(hidden, name, es, np.ones(ex.n, bool), np.zeros(ex.n), rec)
    return dict(summary(ex, es, refs), n_items=ex.n, n_failed=ex.n, reason=reason, fallback=rec["fallback"])


async def box_cpu_seconds(runtime) -> float | None:
    """CPU seconds consumed so far by every process of the box (its cgroup counter; cgroup v2, then v1), read by
    a command INSIDE the box: trustworthy for a verifier box (root is ours there), not for the agent's box."""
    try:
        r = await asyncio.wait_for(runtime.run(["sh", "-c", "cat /sys/fs/cgroup/cpu.stat 2>/dev/null | awk '$1==\"usage_usec\"{print $2/1e6; f=1} END{exit !f}' "
                                                            "|| awk '{print $1/1e9}' /sys/fs/cgroup/cpuacct/cpuacct.usage"], {}), 30)
        return float(r.stdout.strip().splitlines()[-1]) if r.exit_code == 0 else None
    except Exception:
        return None


async def stage(runtime, workdir: str, uid: int) -> dict:
    """Trusted staging after the artifacts are restored: the driver and its directory, root-owned and
    read-only; the restored submission read-only and owned by root. No submitted code runs here."""
    require_container(runtime)
    here = os.path.dirname(os.path.abspath(__file__))
    await runtime.write(f"{RUNTIME_DIR}/item.py", open(os.path.join(here, "public", "_item.py"), "rb").read())
    sub = f"{workdir}/submission"
    r = await runtime.run(["sh", "-c",
                           f'umask 022; mkdir -p {RUNTIME_DIR} {BOX_DIR} && chown -R 0:0 {RUNTIME_DIR} {BOX_DIR} && chmod 755 {RUNTIME_DIR} {BOX_DIR} && '
                           f'chmod 644 {RUNTIME_DIR}/item.py && echo {int(uid)} > {BOX_DIR}/predictor_uid && chmod 644 {BOX_DIR}/predictor_uid; '
                           f'if [ -d {sub} ]; then chown -R -h 0:0 {sub} && chmod -R a-w,a+rX {sub}; fi; '
                           f'chown -R -h 0:0 {workdir}/physim2 {workdir}/TASK.md && chmod -R go-w {workdir}; '
                           f'test -f {sub}/predict.py && echo HAS_PREDICT || echo NO_PREDICT; '
                           f'python3 -I -B {RUNTIME_DIR}/item.py --scan --uid {int(uid)}'], dict(ROUTE_ENV))
    if r.exit_code:
        raise RuntimeError("staging the verifier box failed")
    try:
        rep = json.loads(r.stdout.strip().splitlines()[-1])
    except Exception:
        rep = {}
    if not (rep.get("guard") or {}).get("ok"):               # the driver would refuse to drop privileges and to clean up
        raise RuntimeError("the box is not recognised as a disposable box: " + "; ".join((rep.get("guard") or {}).get("why", ["no report"])))
    return {"has_predict": "HAS_PREDICT" in r.stdout, "scan": rep}


def driver_cmd(limits: dict, workdir: str, uid: int, cleanup: bool = True) -> list[str]:
    return ["python3", "-I", "-B", f"{RUNTIME_DIR}/item.py", "--submission", f"{workdir}/submission",
            "--runner", f"{workdir}/physim2/predict_runner.py", "--request", f"{RUNTIME_DIR}/request.npz",
            "--cpu", str(limits.get("cpu_seconds") or 0), "--wall", str(limits.get("wall_seconds") or 0),
            "--mem-gib", str(limits.get("memory_gib") or 0), "--uid", str(int(uid))] + ([] if cleanup else ["--no-cleanup"])


async def run_request(runtime, cmd: list[str], request: bytes, wall: float) -> dict:
    """ONE request in `runtime`: the driver's JSON line, or a "driver error" record. Never raises; never waits
    longer than the predictor's wall limit plus SLACK_S (a hung box is then a failed request, not a hung reward)."""
    try:
        require_container(runtime)
        async with asyncio.timeout(float(wall or 0) + SLACK_S):
            await runtime.write(f"{RUNTIME_DIR}/request.npz", request)
            out = await runtime.run(cmd, dict(ROUTE_ENV))
        return json.loads(out.stdout.strip().splitlines()[-1])
    except TimeoutError:
        return {"ok": False, "why": "driver error", "stderr": "the box did not answer in time", "cpu_s": 0.0, "wall_s": 0.0, "hung": True}
    except Exception as e:                                   # the box or the driver, not the predictor
        return {"ok": False, "why": "driver error", "stderr": type(e).__name__, "cpu_s": 0.0, "wall_s": 0.0}


def judge(r: dict, queries: dict, dims: dict, m: int, max_values: int):
    """(samples | None, error text | None) from one driver record. The reply is parsed on the worker."""
    use_agentenv()
    from evaluator import submission as SUB
    if not r.get("ok"):
        return None, f"predictor failed ({r.get('why')}): {r.get('stderr', '')}"
    try:
        smp = _rules.read_reply(base64.b64decode(r["reply_b64"]), max_values)
    except ValueError as e:
        return None, f"unreadable reply: {e}"
    except Exception as e:
        return None, f"unreadable reply: {type(e).__name__}"
    bad = SUB.check_shapes(smp, queries, dims, m)
    return (None, bad) if bad else (smp, None)


async def validate(run_one, examples: dict, queries: dict, dims: dict, limits: dict, max_values: int) -> dict:
    """evaluator/submission.py:105-125 (validate), with each request run in the verifier box: example 0 twice
    with the same seed, example 1; shapes, finite values, same seed -> same samples."""
    n = int(limits["n_samples"])
    q = json.dumps({str(l): v for l, v in queries.items()})
    runs, recs = [], []
    for i, seed in ((0, 0), (0, 0), (1, 1)):
        req = {"history": examples["history"][i], "prefix": examples["prefix"][i], "test": examples["test"][i],
               "queries": q, "n_samples": n, "seed": seed}
        r = await run_one(npz_bytes(req))
        recs.append(r)
        smp, bad = judge(r, queries, dims, n, max_values)
        if bad:
            return {"ok": False, "stage": f"example {i}", "error": bad[:2000], "records": recs}
        runs.append(smp)
    if not all(np.array_equal(runs[0][l], runs[1][l]) for l in queries):
        return {"ok": False, "stage": "reproducibility", "error": "the same request and seed gave different samples", "records": recs}
    return {"ok": True, "cpu_s_per_request": max(r.get("cpu_s", 0.0) for r in recs), "wall_s_per_request": max(r.get("wall_s", 0.0) for r in recs),
            "records": recs}


@contextlib.asynccontextmanager
async def fresh_box(config, prepare):
    """A new box from verifiers' own provisioning, with the verifier box's resolved config, prepared by the task
    (public files, restored submission, staging) and cut from the network before anything of the predictor runs:
    the sequence of IsolatedVerifierEnv.grade (envs/isolated_verifier/env.py:148-173)."""
    from verifiers.v1.runtimes import provision_runtime
    async with provision_runtime(config, env={}) as rt:
        if not rt.network_restricted:
            raise RuntimeError("a per-item box without the network policy")
        await rt.prepare_setup()
        await prepare(rt)
        await rt.prepare_execution([])
        yield rt


async def grade(runtime, hidden: str, name: str, limits: dict, workdir: str, *, uid: int, examples: dict, fb: dict, seed: int = 0,
                cleanup: bool = True, deadline: float | None = None, prepare=None, parallel: int = 1) -> dict:
    """The loop of evaluator/grader.py:34-64. `prepare` (async: stage a fresh box) selects one box per item;
    None runs every item in `runtime`. `fb` (fallback()) holds the null policy's scores for the same grading
    seed: an item without a valid forecast gets its row."""
    ex = exam(hidden)
    m = int(limits["n_samples"])
    wall = float(limits.get("wall_seconds") or 0)
    refs = ex.references()
    S = {l: np.zeros((ex.n, m, len(ts), ex.dims[l])) for l, ts in ex.queries.items()}
    max_values = m * sum(len(ts) * ex.dims[l] for l, ts in ex.queries.items())
    failed, cpu, wall_s, errors = np.zeros(ex.n, bool), np.zeros(ex.n), np.zeros(ex.n), []
    cleanups, layers, dirty, infra, box_cpu, box_s, fatal = [], None, None, [], 0.0, [], None
    isolation = "box" if prepare is not None else "shared"
    cmd = driver_cmd(limits, workdir, uid, cleanup)
    t0 = time.time()

    # ---- 1. validation, in the verifier box ----
    val = await validate(lambda req: run_request(runtime, cmd, req, wall), examples, ex.queries, ex.dims, limits, max_values)
    vrecs = val.pop("records")
    for r in vrecs:
        c = r.get("cleanup")
        if c is not None and (c["left_pids"] or c["left_files"] or c.get("left_ipc")):
            dirty = -1
    val_layers = next((r.get("layers") for r in vrecs if r.get("layers")), None)
    if not val["ok"]:
        sub = "not reproducible" if val["stage"] == "reproducibility" else fallback_reason(vrecs[-1] if vrecs else None, val["error"])
        reason = f"validation failed: {sub}"
        g = score_as_null(hidden, name, reason, fb, {"validation": val, "layers": val_layers, "isolation": isolation},
                          detail=f"validation failed ({val['stage']}): {val['error']}"[:4000])
        return dict(g, validation={"ok": False, "stage": val["stage"]}, layers=val_layers, isolation=isolation,
                    seconds=time.time() - t0)

    # ---- 2. the exam ----
    async def one_shared(i):
        return await run_request(runtime, cmd, npz_bytes(ex.request(i, m, seed)), wall)

    async def one_box(i):
        """Item i in a box of its own. A box that cannot be provisioned or staged is the evaluator's failure:
        tried twice, then recorded as an infrastructure failure of that item (it falls back, and is counted)."""
        last = "?"
        for attempt in range(2):
            started, r = False, None
            tb = time.time()
            try:
                async with asyncio.timeout(wall + SLACK_S + BOX_S):
                    async with fresh_box(runtime.config, prepare) as rt:
                        started = True
                        r = await run_request(rt, cmd, npz_bytes(ex.request(i, m, seed)), wall)
            except Exception as e:                           # includes TimeoutError
                last = type(e).__name__
            if r is not None:                                # the request was answered; a slow or failed teardown changes nothing
                box_s.append(time.time() - tb)
                return r
            if started:
                break
        infra.append(i)
        return {"ok": False, "why": "infrastructure", "stderr": f"no box for this item ({last})", "cpu_s": 0.0, "wall_s": 0.0}

    async def one(i):
        if fatal:
            return {"skip": fatal}
        if dirty is not None and prepare is None:            # one box for all items: an unclean box serves no later item
            return {"skip": "the box could not be cleaned after an earlier request"}
        if deadline is not None and time.time() > deadline:
            return {"skip": "grading ran out of time"}
        return await (one_box(i) if prepare is not None else one_shared(i))

    sem = asyncio.Semaphore(max(1, int(parallel)) if prepare is not None else 1)

    async def guarded(i):
        async with sem:
            return await one(i)

    reasons: dict[int, str] = {}                             # item -> one word of FALLBACK_REASONS

    async def handle(i, r):
        bad = await handle_one(i, r)
        if bad:
            reasons[i] = "infrastructure" if bad == fatal else fallback_reason(r, bad)
        return bad

    async def handle_one(i, r):
        nonlocal layers, dirty, box_cpu, fatal
        if "skip" in r:
            return r["skip"]
        cpu[i], wall_s[i] = r.get("cpu_s", 0.0), r.get("wall_s", 0.0)
        layers = r.get("layers") or layers
        if prepare is not None:
            box_cpu += float(r.get("box_cpu_s") or 0.0)
        c = r.get("cleanup")
        if c is not None:
            cleanups.append({"item": i, "killed": c["killed"], "removed": c["removed"], "ipc_removed": c["ipc_removed"]})
            if prepare is None and (c["left_pids"] or c["left_files"] or c.get("left_ipc")):
                dirty = i
        if r.get("hung") and prepare is None:
            dirty = i                                        # a shared box that stopped answering serves no later item
        if r.get("ok") and (r.get("layers") or {}).get("uid") != uid and cleanup:
            fatal = "the driver did not run the predictor as the box's unprivileged user"    # never accept such a reply
            return fatal
        smp, bad = judge(r, ex.queries, ex.dims, m, max_values)
        if bad is None:
            for l in ex.queries:
                S[l][i] = smp[l]
        return bad

    if prepare is not None and parallel > 1:
        results = await asyncio.gather(*(guarded(i) for i in range(ex.n)))
        bads = [await handle(i, r) for i, r in enumerate(results)]
    else:
        bads = []
        for i in range(ex.n):
            bads.append(await handle(i, await one(i)))
    for i, bad in enumerate(bads):
        if bad:
            failed[i] = True
            errors.append({"item": i, "error": bad[:4000]})

    # ---- 3. scoring ----
    with np.errstate(all="ignore"):
        sc = ex.score(S)
    wild = ~np.isfinite(sc).all(1) & ~failed                 # a reply whose score overflows is a failed item
    for i in np.flatnonzero(wild):
        failed[i] = True
        reasons[int(i)] = "score not finite"
        errors.append({"item": int(i), "error": "the samples give a score that is not finite"})
    sc[failed] = np.asarray(fb["es"], float)[failed]         # ruling E3: the null policy's forecast for that item, never K
    fbs = fallback_summary(reasons, fb)
    out = dict(summary(ex, sc, refs), n_items=ex.n, n_failed=int(failed.sum()), fallback=fbs, cpu_s_mean=float(cpu.mean()),
               cpu_s_max=float(cpu.max()), wall_s_mean=float(wall_s.mean()), seconds=time.time() - t0, layers=layers or val_layers,
               items_with_leftovers=sum(1 for c in cleanups if c["killed"] or c["removed"] or c["ipc_removed"]),
               box_not_clean_after_item=dirty, cleanup_between_items=cleanup, isolation=isolation,
               validation={"ok": True, "cpu_s_per_request": val["cpu_s_per_request"]},
               infrastructure_failed_items=len(infra), non_finite_items=int(wild.sum()))
    if prepare is not None:
        out.update(item_boxes=len(box_s), item_box_wall_s_mean=float(np.mean(box_s)) if box_s else None, item_boxes_cpu_s=box_cpu,
                   item_boxes_parallel=int(parallel))
    rec = {"name": name, "n_items": ex.n, "n_failed": int(failed.sum()), "cpu_s_mean": float(cpu.mean()),
           "cpu_s_max": float(cpu.max()), "wall_s_mean": float(wall_s.mean()), "seconds": time.time() - t0,
           "errors": errors, "layers": layers or val_layers, "cleanups": cleanups, "box_not_clean_after_item": dirty,
           "cleanup_between_items": cleanup, "isolation": isolation, "validation": val, "infrastructure_failed_items": infra,
           "non_finite_items": [int(i) for i in np.flatnonzero(wild)], "fallback": fbs,
           "fallback_items": [{"item": int(i), "reason": reasons[i]} for i in sorted(reasons)]}
    save(hidden, name, sc, failed, cpu, rec)
    return out
