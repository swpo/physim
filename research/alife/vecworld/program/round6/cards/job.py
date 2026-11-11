"""job -- the GPU job of study cards (requests r6-cards-*.json); also the CPU test at tiny size (CARDS_SIZE=tiny).

For every world of worlds.json and every declared run (A, B, late): simulate (cardlib.run_world), build the card
on the pod (cardlib.analyse), write $OUT/cards/<world>__<run>.json (the card, the derived numbers and the gates),
and $OUT/series/<world>__<run>.npz (population series, block-view member means, four frames of one member).
Order: PRESMOKE = the first run of every world kind at full shapes (any failure there ends the job at once with a
non-zero exit); then the remaining runs by priority. No new run starts after CARDS_T_LIMIT_S seconds; runs skipped
on the deadline are listed in job_state.json. A failed run after the presmoke (or a failed size check, priority
>= 4, in the presmoke) is recorded and the job goes on;
the exit code is non-zero if any run failed or any priority-1 run was skipped.
PILOT_NEVER_REUSE_AS_EXAM: every hidden part here is a public function of public seeds.
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
import numpy as np  # noqa: E402

import adapters as AD  # noqa: E402
import cardlib as CL  # noqa: E402
import gates as GT  # noqa: E402

SIZE = os.environ.get("CARDS_SIZE", "full")
TINY = SIZE == "tiny"
OUT = os.environ.get("OUT") or os.path.join(HERE, "out")
T_START = float(os.environ.get("CARDS_T_START", T0))
T_LIMIT = float(os.environ.get("CARDS_T_LIMIT_S", 6000))
REQUIRE_GPU = os.environ.get("CARDS_REQUIRE_GPU", "0") == "1"
ONLY = [s for s in os.environ.get("CARDS_ONLY", "").split(",") if s]          # world names (tests)
MAX_PRIORITY = int(os.environ.get("CARDS_MAX_PRIORITY", 9))
os.makedirs(os.path.join(OUT, "cards"), exist_ok=True)
os.makedirs(os.path.join(OUT, "series"), exist_ok=True)

if TINY:
    SZ = CL.Sizes(M=4, M_fit=2, T=48, n_snap=2, R=3, R2=2, n_dir=1, eps=(0.1, 1.0),
                  arms=(("aimed", 200.0), ("blind", 200.0)), R_u=2, HB=32, n_boot=20)
else:
    SZ = CL.Sizes()
W = json.load(open(os.path.join(HERE, "worlds.json")))
STATE = dict(size=SIZE, t_start=T_START, done=[], failed=[], skipped=[], presmoke=None, timing={}, errors=[],
             sizes=dict(M=SZ.M, M_fit=SZ.M_fit, T=SZ.T, NS=SZ.NS, R=SZ.R, R2=SZ.R2, n_dir=SZ.n_dir, eps=list(SZ.eps),
                        arms=[list(a) for a in SZ.arms], R_u=SZ.R_u, HB=SZ.HB, Bb=SZ.Bb))


def el():
    return time.time() - T_START


def P(msg):
    line = f"{time.strftime('%H:%M:%S')} [{el():7.0f}s] {msg}"
    print(line, flush=True)
    with open(os.path.join(OUT, "progress.txt"), "a") as f:
        f.write(line + "\n")


def save_state():
    tmp = os.path.join(OUT, "job_state.json.tmp")
    with open(tmp, "w") as f:
        json.dump(STATE, f, indent=1, default=float)
    os.replace(tmp, os.path.join(OUT, "job_state.json"))


def group_of(w):
    """Worlds of one group share one compiled program."""
    k = w["kind"]
    if k in ("foundry", "diffusion"):
        return f"foundry{w.get('H', 64)}"
    if k == "vortex":
        return f"vortex{w.get('H', 64)}"
    return k


def tiny_kw(kind):
    """Shorter ticks for the CPU code-path test (NOT the studied worlds)."""
    if not TINY:
        return {}
    return {"vortex": dict(n_sub=6, lab_t=0.12), "membrane": dict(n_sub=2)}.get(kind, {})


def adapter_of(w):
    k = w["kind"]
    if k == "foundry":
        return AD.foundry(AD.foundry_theta(W["prior_seed"], w["draw"]), index=w["draw"], H=w.get("H", 64), name=w["name"])
    if k == "diffusion":
        return AD.foundry(AD.diffusion_theta(W["prior_seed"] + 31, w["draw"]), index=w["draw"], H=64, name=w["name"],
                          nb_seed=W["prior_seed"] + 31)
    if k == "gliders":
        return AD.gliders()
    if k == "vortex":
        H = w.get("H", 64)
        if TINY:
            H = 64
        return AD.vortex(H, **tiny_kw("vortex"))
    if k == "membrane":
        return AD.membrane(**tiny_kw("membrane"))
    if k == "noise":
        return AD.noise_field()
    if k == "free":
        return AD.free_bodies()
    raise KeyError(k)


FNS = {}            # group -> [compiled functions, number of calls]
DEAD = set()        # groups whose presmoke failed (size checks only)


def run_one(w, run):
    ad = adapter_of(w)
    g = group_of(w)
    if g not in FNS:
        FNS[g] = [CL.make_fns(ad, SZ), 0]
    fns, ncall = FNS[g]
    seed = int(W["run_seeds"][run])
    burn = ad.burn + (ad.late_gap if run == "late" else 0)
    if TINY:
        burn = min(ad.burn, 6) + (10 if run == "late" else 0)
    rec = CL.run_world(ad, SZ, fns, ad.theta0, seed=seed, burn=burn)
    FNS[g][1] += 1
    rec["timing"]["first_call_of_program"] = bool(ncall == 0)
    meta = dict(Hpx=ad.Hpx, G=ad.G, sigma_u=ad.sigma_u, grid_names=ad.grid_names)
    t1 = time.time()
    card = CL.analyse(rec, SZ, meta, seed=seed)
    ta = time.time() - t1
    ps = card.pop("_per_state_grid")
    c = CL.strip(card)
    c.update(world=w["name"], run=run, role=w["role"], kind=w["kind"], family=ad.family, group=g, seed=seed, burn=int(burn),
             meta=dict(ad.meta, name=ad.name, m=ad.m, sigma_u=ad.sigma_u, G=ad.G, Hpx=ad.Hpx, K=int(ad.trk.K),
                       burn=ad.burn, late_gap=ad.late_gap), analyse_s=ta, r5_type=w.get("r5_type"),
             backend=jax.default_backend(), PILOT_NEVER_REUSE_AS_EXAM=True)
    d = GT.derive(c)
    c["derived"] = CL.strip(d)
    c["gates"] = CL.strip(GT.gates(d))
    name = f"{w['name']}__{run}"
    with open(os.path.join(OUT, "cards", name + ".json"), "w") as f:
        json.dump(c, f)
    # small series and frames for the figures
    pop = CL.pop_vector(rec["tab"]).astype(np.float32)                        # (T + 1, M, 6)
    gm = rec["g"].mean((3, 4)).astype(np.float32)                             # (T + 1, M, Q)
    fr = rec["snap_field"][::SZ.M_test][:4]                                   # test member 0 at the snapshots
    sc = np.percentile(np.abs(fr), 99.9) + 1e-30
    fr8 = np.clip(np.abs(fr) / sc * 255.0, 0, 255).astype(np.uint8)
    tb0 = rec["tab"][::max(1, SZ.T // 100), 0][..., [CL.P_, CL.CY_, CL.CX_, CL.UID_]].astype(np.float32)
    np.savez_compressed(os.path.join(OUT, "series", name + ".npz"), pop=pop, gmean=gm, frames=fr8, frame_scale=sc,
                        per_state_v_clim=ps["v_clim"], per_state_v_orc=ps["v_orc"], per_state_v_pred=ps["v_pred"],
                        tracks_member0=tb0)
    tm = rec["timing"]
    P(f"{name}: sim {tm['main_s']:.1f}+{tm['branch_s']:.1f}s analyse {ta:.1f}s | {c['gates']['verdict']} | "
      f"pf8 {d.get('grid.pf8', float('nan')):.2f} ceil8 {d.get('grid.ceil8', float('nan')):.2f} "
      f"sigma_hat {c['gates']['sigma_hat_best']} nb {d['s.nb_mean']:.1f}")
    STATE["timing"][name] = dict(tm, analyse_s=ta)
    return c


def main():
    P(f"PILOT_NEVER_REUSE_AS_EXAM cards job, size {SIZE}, backend {jax.default_backend()}, devices {jax.devices()}, "
      f"jax {jax.__version__}, numpy {np.__version__}")
    if REQUIRE_GPU and jax.default_backend() != "gpu":
        P("no GPU backend: abort")
        sys.exit(3)
    worlds = [w for w in W["worlds"] if (not ONLY or w["name"] in ONLY) and w["priority"] <= MAX_PRIORITY]
    if TINY and not ONLY:                         # one world per group, every run kind once
        seen, keep = set(), []
        for w in worlds:
            if group_of(w) not in seen and not (w["kind"] == "foundry" and w.get("H", 64) == 128):
                seen.add(group_of(w))
                keep.append(w)
        worlds = keep
    tasks = [(w, r) for w in worlds for r in w["runs"]]
    # presmoke: the first run of every program group
    first, seen = [], set()
    for w, r in tasks:
        if group_of(w) not in seen:
            seen.add(group_of(w))
            first.append((w, r))
    P(f"{len(worlds)} worlds, {len(tasks)} runs, presmoke of {len(first)} program groups: {[group_of(w) for w, _ in first]}")
    t_pre = time.time()
    for w, r in first:
        try:
            run_one(w, r)
            STATE["done"].append(f"{w['name']}__{r}")
        except Exception as e:  # noqa: BLE001
            P(f"PRESMOKE FAILED at {w['name']}__{r}: {type(e).__name__}: {str(e)[:500]}")
            traceback.print_exc()
            STATE["errors"].append(dict(run=f"{w['name']}__{r}", error=f"{type(e).__name__}: {str(e)[:2000]}"))
            if w["priority"] >= 4:                # a size check: recorded, its group is dropped, the job goes on
                STATE["failed"].append(f"{w['name']}__{r}")
                DEAD.add(group_of(w))
                FNS.pop(group_of(w), None)
                gc.collect()
                jax.clear_caches()
                save_state()
                continue
            STATE["presmoke"] = "failed"
            save_state()
            sys.exit(2)
        save_state()
    STATE["presmoke"] = "passed"
    STATE["presmoke_s"] = time.time() - t_pre
    P(f"presmoke passed in {time.time() - t_pre:.0f}s")
    save_state()
    rest = [(w, r) for w, r in tasks if f"{w['name']}__{r}" not in STATE["done"]]
    rest.sort(key=lambda t: (t[0]["priority"], group_of(t[0])))               # stable: world order kept inside a group
    for w, r in rest:
        name = f"{w['name']}__{r}"
        if el() > T_LIMIT or group_of(w) in DEAD:
            STATE["skipped"].append(dict(run=name, priority=w["priority"], why="deadline" if el() > T_LIMIT else "group failed"))
            continue
        try:
            run_one(w, r)
            STATE["done"].append(name)
        except Exception as e:  # noqa: BLE001
            P(f"FAILED {name}: {type(e).__name__}: {str(e)[:300]}")
            traceback.print_exc()
            STATE["failed"].append(name)
            STATE["errors"].append(dict(run=name, error=f"{type(e).__name__}: {str(e)[:2000]}"))
            gc.collect()
        save_state()
    STATE["elapsed_s"] = el()
    save_state()
    bad = len(STATE["failed"]) + sum(1 for s in STATE["skipped"] if s["priority"] == 1)
    P(f"done: {len(STATE['done'])} runs, failed {len(STATE['failed'])}, skipped {len(STATE['skipped'])}, exit {1 if bad else 0}")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
