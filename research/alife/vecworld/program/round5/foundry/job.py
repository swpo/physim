"""job -- the GPU job of study foundry (requests r5-foundry-*.json). Also runs on CPU at tiny size.

Stages (each writes small files under $OUT; a later stage is skipped, and recorded as skipped, when its
deadline has passed):
  checks    conservation and positivity of the family on this platform; vmap against single-world runs;
            run-to-run determinism of one compiled chunk
  wstats    statistics of the weights alone (linear stability of the uniform state, affinity Jacobian)
  screen    N draws from the prior in chunks: the cheap certificates of screen.py
  controls  the same certificates on no-affinity worlds (beta = 0, kappa = 0: diffusion with noise)
  select    types, gates and score (criteria.py); the top candidates
  certify   the candidates at larger size (more members, test states and replicas), three sizes of the
            weight neighbourhood, frames of one member for posters and videos
  gliders   the same certificates on the Flow-Lenia gliders world (reference by the same estimator)

Sizes and deadlines come from the environment (FOUNDRY_*), defaults = the full job.
No network or subprocess use.
"""
from __future__ import annotations

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

import criteria as CR  # noqa: E402
import screen as SC  # noqa: E402
import tnca as TN  # noqa: E402
from vw.core import Noise  # noqa: E402


def env(name, default, cast=int):
    return cast(os.environ.get("FOUNDRY_" + name, default))


SIZE = os.environ.get("FOUNDRY_SIZE", "full")
TINY = SIZE == "tiny"
OUT = os.environ.get("OUT") or os.path.join(HERE, "out")
T_START = env("T_START", str(T0), float)          # job.sh passes its own start time
PRIOR_SEED = env("PRIOR_SEED", 2026)
RUN_SEED = env("RUN_SEED", 5150)
N_DRAWS = env("N_DRAWS", 16 if TINY else 4096)
N_MIN = env("N_MIN", 8 if TINY else 2048)
CHUNK = env("CHUNK", 8 if TINY else 128)
N_THUMB = env("N_THUMB", 8 if TINY else 1024)
N_CERT = env("N_CERT", 4 if TINY else 24)
N_CTRL = env("N_CTRL", 4 if TINY else 32)
N_GLID = env("N_GLID", 2 if TINY else 16)
EPS = 0.1
T_SCREEN = env("T_SCREEN_S", 2400, float)          # no new screen chunk after this (once N_MIN is done)
T_SCREEN_HARD = env("T_SCREEN_HARD_S", 3000, float)  # no new screen chunk after this at all
T_LATE = env("T_LATE_S", 3700, float)              # no new stage after this
DO_GLIDERS = env("GLIDERS", 1)

if TINY:
    SZ = SC.Sizes(M=3, M_fit=2, M_trk=1, burn=6, T=40, n_snap=2, R=2, R2=2, HB=32)
    SZC = SC.Sizes(M=4, M_fit=2, M_trk=1, burn=6, T=40, n_snap=2, R=3, R2=2, HB=32, frame_every=2)
    SZG = SC.Sizes(M=3, M_fit=2, M_trk=1, burn=2, T=36, n_snap=1, R=2, R2=2, HB=32)
else:
    SZ = SC.Sizes(M=6, M_fit=4, M_trk=2, burn=50, T=240, n_snap=4, R=4, R2=2, HB=32)
    SZC = SC.Sizes(M=16, M_fit=8, M_trk=4, burn=50, T=400, n_snap=4, R=6, R2=2, HB=32, frame_every=2)
    SZG = SZ

os.makedirs(os.path.join(OUT, "screen"), exist_ok=True)
os.makedirs(os.path.join(OUT, "cert"), exist_ok=True)
STATE = dict(size=SIZE, stages={}, errors=[], t_start=T_START)


def el():
    return time.time() - T_START


def P(msg):
    line = f"{time.strftime('%H:%M:%S')} [{el():7.0f}s] {msg}"
    print(line, flush=True)
    with open(os.path.join(OUT, "progress.txt"), "a") as f:
        f.write(line + "\n")


def save_state():
    with open(os.path.join(OUT, "job_state.json"), "w") as f:
        json.dump(STATE, f, indent=1, default=float)


def dev(tree):
    return {k: jnp.asarray(v) for k, v in tree.items()}


def take(ths, idx):
    return {k: v[idx] for k, v in ths.items()}


def neighbours(ths, indices, eps, hyper=False):
    out = [TN.perturb_theta({k: v[i] for k, v in ths.items()}, PRIOR_SEED, int(j), eps, hyper=hyper)
           for i, j in enumerate(indices)]
    return {k: np.stack([o[k] for o in out]) for k in out[0]}


def draw_keys(seed, indices):
    base = jax.random.key(seed)
    return jax.vmap(lambda i: jax.random.fold_in(base, i))(jnp.asarray(np.asarray(indices), jnp.uint32))


def member_ticks(sz, n):
    return n * (sz.M * (sz.burn + sz.T) + sz.NS * (sz.R + sz.R2) * sz.HB)


def release(*names):
    gc.collect()
    jax.clear_caches()


# ----------------------------------------------------------------------------- stage: checks
def stage_checks():
    fam = TN.FAM
    n, T = (4, 20) if TINY else (16, 200)
    ths = TN.draw_thetas(PRIOR_SEED + 1, range(n))
    keys = draw_keys(RUN_SEED + 1, range(n))

    def one(th, key):
        x0 = TN.init(th, jax.random.fold_in(key, 1))

        def body(x, t):
            xn = TN.tick_free(th, x, Noise(key, t))
            return xn, (xn.sum((1, 2)), xn.min())
        x, (m, mn) = jax.lax.scan(body, x0, jnp.arange(T))
        return x0.sum((1, 2)), m, mn, x
    f = jax.jit(jax.vmap(one))
    m0, m, mn, x = [np.asarray(a) for a in f(dev(ths), keys)]
    tot = np.abs(m.sum(-1) - m0.sum(-1)[:, None]).max(1) / m0.sum(-1)
    k0 = ths["kappa"] == 0
    kind = (np.abs(m - m0[:, None]) / m0[:, None]).max((1, 2))
    # the same worlds one at a time (vmap against single-world runs)
    f1 = jax.jit(one)
    dmax = 0.0
    for i in range(min(n, 3)):
        xi = np.asarray(f1(dev(take(ths, i)), keys[i])[3])
        dmax = max(dmax, float(np.abs(xi - x[i]).max() / np.abs(x[i]).max()))
    # determinism of the batched program on this platform
    x2 = np.asarray(f(dev(ths), keys)[3])
    res = dict(n_worlds=n, ticks=T, substeps=T * fam.NSUB,
               total_mass_rel_drift_max=float(tot.max()),
               kind_mass_rel_drift_max_kappa0=float(kind[k0].max()) if k0.any() else None,
               n_kappa0=int(k0.sum()), min_cell=float(mn.min()), all_finite=bool(np.isfinite(x).all()),
               vmap_vs_single_rel_max=dmax, rerun_bit_identical=bool((x2 == x).all()),
               rerun_rel_max=float(np.abs(x2 - x).max() / np.abs(x).max()))
    del f, f1
    return res


# ----------------------------------------------------------------------------- stage: weight statistics
def stage_wstats(ths_all):
    f = jax.jit(jax.vmap(lambda th: TN.weight_stats(th)))
    n = len(ths_all["beta"])
    step = 8 if TINY else 512
    parts = []
    for a in range(0, n, step):
        b = min(n, a + step)
        idx = np.arange(a, b)
        if b - a < step:                                   # keep one compiled shape
            idx = np.concatenate([idx, np.full(step - (b - a), a)])
        r = f(dev(take(ths_all, idx)))
        parts.append({k: np.asarray(v)[:b - a] for k, v in r.items()})
    ws = {k: np.concatenate([p[k] for p in parts]) for k in parts[0]}
    np.savez_compressed(os.path.join(OUT, "wstats.npz"), **ws)
    del f
    return dict(n=n, n_unstable=int((ws["lin_growth"] > 1e-6).sum()), keys=sorted(ws))


# ----------------------------------------------------------------------------- stage: screen
def run_chunk(fn, ths, ths2, keys):
    t = time.time()
    res = fn(dev(ths), dev(ths2), keys)
    res = SC.to_host(res)
    return res, time.time() - t


def stage_screen(ths_all):
    global CHUNK
    wd = SC.tnca_world()
    fn = SC.make_chunk_fn(wd, SZ)
    done, c, times = 0, 0, []
    info = dict(sizes=vars(SZ) | dict(NS=SZ.NS), chunk=CHUNK, chunks=[], eps=EPS)
    while done < N_DRAWS:
        if (done >= N_MIN and el() > T_SCREEN) or el() > T_SCREEN_HARD:
            P(f"screen: deadline, stopping at {done} draws")
            break
        idx = np.arange(done, min(N_DRAWS, done + CHUNK))
        pad = idx if len(idx) == CHUNK else np.concatenate([idx, np.full(CHUNK - len(idx), idx[0])])
        ths = take(ths_all, pad)
        ths2 = neighbours(ths, pad, EPS)
        try:
            res, dt = run_chunk(fn, ths, ths2, draw_keys(RUN_SEED, pad))
        except Exception as e:                              # most likely out of memory: halve the chunk once or twice
            msg = repr(e)[:300]
            P(f"screen: chunk of {CHUNK} failed: {msg}")
            STATE["errors"].append(dict(stage="screen", chunk=CHUNK, error=msg))
            if CHUNK <= 16 and not TINY or CHUNK <= 2:
                raise
            del fn
            release()
            CHUNK //= 2
            fn = SC.make_chunk_fn(wd, SZ)
            continue
        n = len(idx)
        res = {k: v[:n] for k, v in res.items()}
        thumb = res.pop("thumb")
        keep = idx < N_THUMB
        if keep.any():
            u, sc = SC.quantise(thumb[keep])
            res["thumb_u8"], res["thumb_scale"], res["thumb_index"] = u, sc, idx[keep]
        np.savez_compressed(os.path.join(OUT, "screen", f"chunk_{c:04d}.npz"), index=idx, **res)
        mt = member_ticks(SZ, n)
        times.append(dt)
        info["chunks"].append(dict(chunk=c, n=n, seconds=dt, member_ticks=mt))
        P(f"screen chunk {c}: draws {idx[0]}-{idx[-1]} in {dt:.1f}s ({mt / dt:.0f} member-ticks/s"
          f"{', incl. compile' if len(times) == 1 else ''}); finite {int(res['finite'].sum())}/{n}")
        done += n
        c += 1
        STATE["stages"]["screen"] = dict(done=done, chunks=c)
        save_state()
    info.update(n_done=done, n_chunks=c, chunk_final=CHUNK)
    if len(times) > 1:
        info["member_ticks_per_s_steady"] = float(member_ticks(SZ, CHUNK) / np.median(times[1:]))
    del fn
    return info


def load_screen():
    files = sorted(f for f in os.listdir(os.path.join(OUT, "screen")) if f.startswith("chunk_"))
    parts = [dict(np.load(os.path.join(OUT, "screen", f))) for f in files]
    skip = ("thumb_u8", "thumb_scale", "thumb_index")
    return {k: np.concatenate([p[k] for p in parts]) for k in parts[0] if k not in skip}


# ----------------------------------------------------------------------------- stage: controls
def stage_controls(ths_all):
    """No-affinity worlds: the first N_CTRL draws with beta = 0, gam = 0, kappa = 0 (noisy diffusion with
    crowding): the floor of every measure."""
    idx = np.arange(N_CTRL)
    ths = take(ths_all, idx)
    ths = dict(ths, beta=0 * ths["beta"], gam=0 * ths["gam"], kappa=0 * ths["kappa"])
    wd = SC.tnca_world()
    fn = SC.make_chunk_fn(wd, SZ)
    res, dt = run_chunk(fn, ths, ths, draw_keys(RUN_SEED + 2, idx))
    res.pop("thumb")
    np.savez_compressed(os.path.join(OUT, "controls_diffusion.npz"), index=idx, **res)
    d = CR.derive(res, SZ.T)
    t = CR.classify(d)
    del fn
    return dict(n=int(N_CTRL), seconds=dt, types={CR.TYPES[i]: int((t == i).sum()) for i in range(len(CR.TYPES))},
                cv_cell_max=float(d["cv_cell"].max()), cv_cell_median=float(np.median(d["cv_cell"])),
                vp_main1_median=float(np.median(d["vp_main1"])), pl8_max=float(np.nanmax(d["pl8"])))


# ----------------------------------------------------------------------------- stage: select
def stage_select():
    m = load_screen()
    d = CR.derive(m, SZ.T)
    t = CR.classify(d)
    g = CR.gates(d, t)
    s = CR.score(d, t)
    order = np.argsort(-s, kind="stable")
    top = [int(m["index"][i]) for i in order[:N_CERT] if s[i] > 0]
    if len(top) < N_CERT:                                   # fill with the most active remaining worlds
        rest = [int(m["index"][i]) for i in np.argsort(-np.nan_to_num(d["moved"])) if int(m["index"][i]) not in top]
        top += rest[:N_CERT - len(top)]
    sel = dict(n=len(t), types={CR.TYPES[i]: int((t == i).sum()) for i in range(len(CR.TYPES))},
               gates={k: int(v.sum()) for k, v in g.items()}, top=top,
               top_score=[float(s[list(m["index"]).index(i)]) for i in top], thresholds=CR.THRESHOLDS)
    with open(os.path.join(OUT, "selection.json"), "w") as f:
        json.dump(sel, f, indent=1)
    return sel


# ----------------------------------------------------------------------------- stage: certify
def stage_certify(ths_all, top):
    wd = SC.tnca_world()
    fn = SC.make_chunk_fn(wd, SZC, map_batch=8)
    idx = np.asarray(top)
    ths = take(ths_all, idx)
    keys = draw_keys(RUN_SEED + 3, idx)
    info = dict(sizes=vars(SZC) | dict(NS=SZC.NS), index=[int(i) for i in idx], runs=[])
    for name, eps, hyper in (("eps010", 0.1, False), ("eps003", 0.03, False), ("eps030", 0.3, False),
                             ("hyp010", 0.1, True)):
        if el() > T_LATE:
            P(f"certify: deadline before {name}")
            break
        ths2 = neighbours(ths, idx, eps, hyper)
        res, dt = run_chunk(fn, ths, ths2, keys)
        res.pop("thumb")
        fr = res.pop("frames")
        tab = res.pop("tab")
        if name == "eps010":
            u, sc = SC.quantise(fr)
            np.savez_compressed(os.path.join(OUT, "cert", "frames.npz"), index=idx, frames=u, scale=sc,
                                tab=tab.astype(np.float32), frame_every=SZC.frame_every)
        np.savez_compressed(os.path.join(OUT, "cert", f"{name}.npz"), index=idx, eps=eps, hyper=hyper, **res)
        mt = member_ticks(SZC, len(idx))
        info["runs"].append(dict(name=name, eps=eps, hyper=hyper, seconds=dt, member_ticks=mt))
        P(f"certify {name}: {len(idx)} worlds in {dt:.1f}s ({mt / dt:.0f} member-ticks/s)")
    del fn
    return info


# ----------------------------------------------------------------------------- stage: gliders reference
def stage_gliders():
    wd, p = SC.gliders_world()
    n = N_GLID
    ths = {k: np.broadcast_to(np.asarray(v), (n,) + np.shape(v)).copy() for k, v in p.items()} \
        if isinstance(p, dict) else None
    if ths is None:
        ths = jax.tree_util.tree_map(lambda v: np.broadcast_to(np.asarray(v), (n,) + np.shape(v)).copy(), p)
    fn = SC.make_chunk_fn(wd, SZG, map_batch=4)
    keys = draw_keys(RUN_SEED + 4, range(n))
    t = time.time()
    thd = jax.tree_util.tree_map(jnp.asarray, ths)
    res = SC.to_host(fn(thd, thd, keys))
    dt = time.time() - t
    res.pop("thumb")
    np.savez_compressed(os.path.join(OUT, "ref_gliders.npz"), **res)
    d = CR.derive(res, SZG.T)
    ty = CR.classify(d)
    mt = member_ticks(SZG, n)
    del fn
    return dict(n=n, sizes=vars(SZG) | dict(NS=SZG.NS), seconds=dt, member_ticks=mt, member_ticks_per_s=mt / dt,
                types={CR.TYPES[i]: int((ty == i).sum()) for i in range(len(CR.TYPES))},
                ceil_mean={str(h): float(np.nanmean(d[f"ceil{h}"])) for h in SZG.hz},
                note="theta' = theta here, so pl is a null check of the plug-in loss estimator")


# ----------------------------------------------------------------------------- main
def run_stage(name, fn, *a, optional=False):
    if el() > T_LATE:
        P(f"{name}: skipped (deadline)")
        STATE["stages"][name] = dict(skipped="deadline")
        save_state()
        return None
    P(f"{name}: start")
    t = time.time()
    try:
        r = fn(*a)
    except Exception as e:
        tb = traceback.format_exc()
        print(tb, flush=True)
        P(f"{name}: FAILED {repr(e)[:300]}")
        STATE["errors"].append(dict(stage=name, error=repr(e)[:1000], optional=optional))
        STATE["stages"][name] = dict(failed=True, seconds=time.time() - t)
        save_state()
        release()
        return None
    r = dict(r or {}, seconds_total=time.time() - t)
    STATE["stages"][name] = r
    save_state()
    release()
    P(f"{name}: done in {time.time() - t:.1f}s")
    return r


def main():
    P(f"job.py size={SIZE} python {sys.version.split()[0]} jax {jax.__version__} numpy {np.__version__} "
      f"devices {jax.devices()} x64 {jax.config.jax_enable_x64}")
    STATE["platform"] = dict(jax=jax.__version__, numpy=np.__version__, python=sys.version.split()[0],
                             devices=[str(d) for d in jax.devices()], backend=jax.default_backend(), dtype="float64")
    STATE["config"] = dict(prior_seed=PRIOR_SEED, run_seed=RUN_SEED, n_draws=N_DRAWS, n_min=N_MIN, chunk=CHUNK,
                           eps=EPS, family=vars(TN.FAM), prior=TN.PRIOR, thresholds=CR.THRESHOLDS)
    if os.environ.get("FOUNDRY_REQUIRE_GPU", "0") == "1" and jax.default_backend() != "gpu":
        P("no GPU backend: abort")
        save_state()
        return 2
    ths_all = TN.draw_thetas(PRIOR_SEED, range(N_DRAWS))
    np.savez_compressed(os.path.join(OUT, "thetas_scalars.npz"),
                        **{k: ths_all[k] for k in ("beta", "gam", "alpha", "mu", "kappa", "gr", "dens", "wq")})
    run_stage("checks", stage_checks)
    run_stage("wstats", stage_wstats, ths_all)
    scr = run_stage("screen", stage_screen, ths_all)
    ok = scr is not None and scr.get("n_done", 0) >= min(N_MIN, N_DRAWS)
    sel = run_stage("select", stage_select) if scr else None
    if sel:
        run_stage("certify", stage_certify, ths_all, sel["top"])
    run_stage("controls", stage_controls, ths_all, optional=True)
    if DO_GLIDERS:
        run_stage("gliders", stage_gliders, optional=True)
    hard = [e for e in STATE["errors"] if not e.get("optional") and e.get("stage") != "screen"]
    STATE["seconds_total"] = el()
    STATE["ok"] = bool(ok and sel is not None and not hard)
    save_state()
    P(f"job.py end: ok={STATE['ok']} errors={len(STATE['errors'])}")
    return 0 if STATE["ok"] and not STATE["errors"] else 1


if __name__ == "__main__":
    sys.exit(main())
