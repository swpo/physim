"""job2 -- the second GPU job of study foundry (request r5-foundry-002). Also runs on CPU at tiny size.

Four follow-ups to the screen r5-foundry-001, each an "arm" = a list of prior draws measured with the
certificates of screen.py (same code; arms differ in the draws, the sizes or one public constant):

  late     draws of prior seed 2026 (every active world of job 1, plus samples of its frozen and uniform
           worlds) with a burn-in of 2000 ticks instead of 50: is the type a transient?
  enrich   fresh draws of prior seed 2027 chosen by their weight statistics alone (select_enriched.py,
           fitted on job 1) and a random control arm from the same pool: a prospective test of the predictor
  sigma010, sigma100
           draws 0..N of prior seed 2026 with the logit noise at 0.1 and 1.0 instead of 0.3: does the type
           belong to the weights or to the public noise level?
  cert     every candidate of job 1 at the certification size (16 members x 450 ticks, 32 test states x 8
           replicas), no frames

Inputs: job2_inputs.json (index lists, written by make_job2_inputs.py). Outputs under $OUT/<arm>/chunk_*.npz
and $OUT/job2_state.json (rewritten after every chunk, so a killed job leaves analysable outputs).
Deadlines in seconds from the start of job.sh (FOUNDRY_T_LATE_S: no new chunk after it). No network or
subprocess use.
"""
from __future__ import annotations

import dataclasses
import gc
import json
import os
import sys
import time
import traceback

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

T0 = time.time()
import jax  # noqa: E402
import jax.numpy as jnp  # noqa: E402
import numpy as np  # noqa: E402

import screen as SC  # noqa: E402
import tnca as TN  # noqa: E402


def env(name, default, cast=int):
    return cast(os.environ.get("FOUNDRY_" + name, default))


SIZE = os.environ.get("FOUNDRY_SIZE", "full")
TINY = SIZE == "tiny"
OUT = os.environ.get("OUT") or os.path.join(HERE, "out2")
T_START = env("T_START", str(T0), float)
RUN_SEED = env("RUN_SEED", 5150)
CHUNK = env("CHUNK", 8 if TINY else 128)
CHUNK_CERT = env("CHUNK_CERT", 4 if TINY else 24)
T_LATE = env("T_LATE_S", 1500, float)
BURN_LATE = env("BURN_LATE", 30 if TINY else 2000)
ARMS = os.environ.get("FOUNDRY_ARMS", "late,enrich,cert,sigma010,sigma100").split(",")
EPS = 0.1

if TINY:
    SZ = SC.Sizes(M=3, M_fit=2, M_trk=1, burn=6, T=40, n_snap=2, R=2, R2=2, HB=32)
    SZC = SC.Sizes(M=4, M_fit=2, M_trk=1, burn=6, T=40, n_snap=2, R=3, R2=2, HB=32)
else:
    SZ = SC.Sizes(M=6, M_fit=4, M_trk=2, burn=50, T=240, n_snap=4, R=4, R2=2, HB=32)
    SZC = SC.Sizes(M=16, M_fit=8, M_trk=4, burn=50, T=400, n_snap=4, R=6, R2=2, HB=32)

os.makedirs(OUT, exist_ok=True)
STATE = dict(size=SIZE, arms={}, errors=[], t_start=T_START)


def el():
    return time.time() - T_START


def P(msg):
    line = f"{time.strftime('%H:%M:%S')} [{el():7.0f}s] {msg}"
    print(line, flush=True)
    with open(os.path.join(OUT, "progress.txt"), "a") as f:
        f.write(line + "\n")


def save_state():
    tmp = os.path.join(OUT, "job2_state.json.tmp")
    with open(tmp, "w") as f:
        json.dump(STATE, f, indent=1, default=float)
    os.replace(tmp, os.path.join(OUT, "job2_state.json"))


def dev(tree):
    return {k: jnp.asarray(v) for k, v in tree.items()}


def draw_keys(seed, indices):
    base = jax.random.key(seed)
    return jax.vmap(lambda i: jax.random.fold_in(base, i))(jnp.asarray(np.asarray(indices), jnp.uint32))


def member_ticks(sz, n):
    return n * (sz.M * (sz.burn + sz.T) + sz.NS * (sz.R + sz.R2) * sz.HB)


def run_arm(name, ids, prior_seed, sz, fam=TN.FAM, chunk=None, key_seed=None, n_thumb=0, map_batch=16):
    """Measure the draws `ids` of `prior_seed`; one npz per chunk under OUT/<name>/."""
    chunk = chunk or CHUNK
    key_seed = RUN_SEED if key_seed is None else key_seed
    ids = np.asarray(ids, np.int64)
    d = os.path.join(OUT, name)
    os.makedirs(d, exist_ok=True)
    info = dict(prior_seed=prior_seed, sizes=vars(sz) | dict(NS=sz.NS), family=vars(fam), chunk=chunk, n_planned=len(ids),
                n_done=0, chunks=[], eps=EPS, key_seed=key_seed)
    STATE["arms"][name] = info
    save_state()
    wd = SC.tnca_world(fam)
    fn = SC.make_chunk_fn(wd, sz, map_batch=map_batch)
    done, c = 0, 0
    while done < len(ids):
        if el() > T_LATE:
            P(f"{name}: deadline, stopping at {done} of {len(ids)} draws")
            info["stopped"] = "deadline"
            break
        pos = np.arange(done, min(len(ids), done + chunk))
        pad = pos if len(pos) == chunk else np.concatenate([pos, np.full(chunk - len(pos), pos[0])])
        idx = ids[pos]
        ths = TN.draw_thetas(prior_seed, ids[pad], fam)
        nb = [TN.perturb_theta({k: v[i] for k, v in ths.items()}, prior_seed, int(j), EPS, fam) for i, j in enumerate(ids[pad])]
        ths2 = {k: np.stack([o[k] for o in nb]) for k in nb[0]}
        t = time.time()
        try:
            res = SC.to_host(fn(dev(ths), dev(ths2), draw_keys(key_seed, ids[pad])))
        except Exception as e:                              # out of memory: halve the chunk (down to 8), else give up the arm
            msg = repr(e)[:300]
            P(f"{name}: chunk of {chunk} failed: {msg}")
            STATE["errors"].append(dict(arm=name, chunk=chunk, error=msg))
            if chunk <= (2 if TINY else 8):
                info["failed"] = msg
                break
            del fn
            gc.collect()
            jax.clear_caches()
            chunk //= 2
            fn = SC.make_chunk_fn(wd, sz, map_batch=min(map_batch, chunk))
            continue
        dt = time.time() - t
        n = len(idx)
        res = {k: v[:n] for k, v in res.items()}
        thumb = res.pop("thumb")
        keep = pos < n_thumb
        if keep.any():
            u, sc = SC.quantise(thumb[keep])
            res["thumb_u8"], res["thumb_scale"], res["thumb_index"] = u, sc, idx[keep]
        np.savez_compressed(os.path.join(d, f"chunk_{c:04d}.npz"), index=idx, **res)
        mt = member_ticks(sz, n)
        info["chunks"].append(dict(chunk=c, n=n, seconds=dt, member_ticks=mt))
        done += n
        c += 1
        info["n_done"] = done
        save_state()
        if c <= 2 or c % 8 == 0 or done == len(ids):
            P(f"{name} chunk {c - 1}: {done}/{len(ids)} draws, {dt:.1f}s ({mt / dt:.0f} member-ticks/s)")
    info["seconds"] = float(sum(ch["seconds"] for ch in info["chunks"]))
    rates = [ch["member_ticks"] / ch["seconds"] for ch in info["chunks"][1:]]
    if rates:
        info["member_ticks_per_s_steady"] = float(np.median(rates))
    save_state()
    del fn
    gc.collect()
    jax.clear_caches()
    return info


def main():
    P(f"job2.py size={SIZE} arms={ARMS} python {sys.version.split()[0]} jax {jax.__version__} numpy {np.__version__} "
      f"devices {jax.devices()} x64 {jax.config.jax_enable_x64}")
    STATE["platform"] = dict(jax=jax.__version__, numpy=np.__version__, python=sys.version.split()[0],
                             devices=[str(d) for d in jax.devices()], backend=jax.default_backend(), dtype="float64")
    if os.environ.get("FOUNDRY_REQUIRE_GPU", "0") == "1" and jax.default_backend() != "gpu":
        P("no GPU backend: abort")
        save_state()
        return 2
    inp = json.load(open(os.path.join(HERE, os.environ.get("FOUNDRY_INPUTS", "job2_inputs.json"))))
    cut = (lambda v, n: v[:n]) if TINY else (lambda v, n: v)
    plan = {
        "late": lambda: run_arm("late", cut(inp["late"]["index"], 12), inp["late"]["prior_seed"],
                                dataclasses.replace(SZ, burn=BURN_LATE)),
        "enrich": lambda: run_arm("enrich", cut(inp["enrich"]["index"], 16), inp["enrich"]["prior_seed"], SZ, n_thumb=256),
        "cert": lambda: run_arm("cert", cut(inp["cert"]["index"], 6), inp["cert"]["prior_seed"], SZC, chunk=CHUNK_CERT,
                                key_seed=RUN_SEED + 3, map_batch=8),
        "sigma010": lambda: run_arm("sigma010", cut(inp["sigma"]["index"], 8), inp["sigma"]["prior_seed"], SZ,
                                    fam=dataclasses.replace(TN.FAM, sigma=0.1)),
        "sigma100": lambda: run_arm("sigma100", cut(inp["sigma"]["index"], 8), inp["sigma"]["prior_seed"], SZ,
                                    fam=dataclasses.replace(TN.FAM, sigma=1.0)),
    }
    for name in ARMS:
        if el() > T_LATE:
            P(f"{name}: skipped (deadline)")
            STATE["arms"][name] = dict(skipped="deadline")
            save_state()
            continue
        P(f"{name}: start")
        t = time.time()
        try:
            info = plan[name]()
            P(f"{name}: {info['n_done']}/{info['n_planned']} draws in {time.time() - t:.1f}s")
        except Exception as e:
            print(traceback.format_exc(), flush=True)
            P(f"{name}: FAILED {repr(e)[:300]}")
            STATE["errors"].append(dict(arm=name, error=repr(e)[:1000]))
            STATE["arms"].setdefault(name, {})["failed"] = repr(e)[:300]
            save_state()
            gc.collect()
            jax.clear_caches()
    STATE["seconds_total"] = el()
    complete = all(STATE["arms"].get(a, {}).get("n_done", 0) == STATE["arms"].get(a, {}).get("n_planned", -1) for a in ARMS)
    STATE["ok"] = bool(complete and not STATE["errors"])
    save_state()
    P(f"job2.py end: ok={STATE['ok']} errors={len(STATE['errors'])}")
    return 0 if STATE["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
