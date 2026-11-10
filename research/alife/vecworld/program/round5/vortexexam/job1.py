"""job1 -- round 5, study vortexexam (track 2), GPU job 1: throughput, effective law, headroom scan.

PILOT ONLY (never to be reused as an exam): every parameter value here is public and written to the outputs.

Stages (each writes its outputs to --out as it finishes; progress in OUT/progress.txt):
  A bench    member-ticks per second of the fed-vortex world (float64, 250 native steps per tick) with the level-1
             vortex tracker, at H = 64, 96, 128 and several batch sizes; the tracker and the host level-1/2
             summaries alone; peak device memory.
  B size     H_exam = the largest H in (128, 96, 64) whose best throughput is >= --min-rate member-ticks/s
             (declared rule; override with --H).
  C law      eps in EPS_LAW x J_law members (keys shared across eps), T_law ticks from the declared initial law:
             level-1 summaries and level 2 per tick (the replicator check is analyse1.py on these arrays).
  D scan     one-at-a-time headroom scan: every candidate hidden parameter at the lower and the upper edge of its
             declared box (others at default) plus the null setting; J members each (keys shared), T ticks;
             at the anchor ticks, from every member's state: R truths under the setting's theta and Mc controls
             under theta_0 (the box centre = default), fresh noise, no input, HB ticks.
  E law128   (time permitting, if H_exam != 128) the law runs at 128^2 for 3 eps, fewer members.
--scan-only repeats stage D alone (used inside job 2: the first run's branch file held the level-1 rasters and, at
40 MB, stayed on the runner; the level-1 scores are now computed here and only they are saved).
usage: python -B job1.py --out DIR [--smoke] [--max-hours 0.8] [--H 64] [--scan-only --rate 400 --rate-json F --bmax 1024]
"""
from __future__ import annotations

import argparse
import gc
import json
import os
import platform
import sys
import time
import traceback

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import vxlib as VX  # noqa: E402

import jax  # noqa: E402
import jax.numpy as jnp  # noqa: E402
import numpy as np  # noqa: E402

from vw.world import make_key, member_keys  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("--out", required=True)
ap.add_argument("--smoke", action="store_true")
ap.add_argument("--max-hours", type=float, default=0.8)
ap.add_argument("--min-rate", type=float, default=100.0)
ap.add_argument("--H", type=int, default=0)
ap.add_argument("--scan-only", action="store_true", help="only stage D at --H (rate from --rate), compact branch outputs")
ap.add_argument("--rate", type=float, default=400.0)
ap.add_argument("--rate-json", default="", help="take 0.9 x 'rate' from this info.json (job 2's) when it exists")
ap.add_argument("--bmax", type=int, default=1024)
args = ap.parse_args()
OUT = args.out
os.makedirs(OUT, exist_ok=True)
T0 = time.time()

# declared prior boxes of the candidates (lo, hi); default = THETA0 (the centre, except eps and mut128: see note)
BOX = {"eps": (0.0, 0.4), "kF": (0.015, 0.025), "e": (7.0, 13.0), "nu": (0.07, 0.13), "mut128": (25.0, 100.0),
       "k": (0.45, 0.55), "mu": (0.09, 0.11), "kl": (1.0, 3.0), "dl": (0.03, 0.07), "Dl": (0.01, 0.04),
       "adv": (0.85, 1.15), "kY": (0.7, 1.3), "wi": (0.07, 0.13)}
FULL = dict(bench=[(64, 256), (128, 256), (96, 512), (64, 1024), (128, 64), (128, 1024), (64, 4096)], bench_ticks=2,
            eps_law=[0.0, 0.1, 0.2, 0.3, 0.4], J_law=[64, 48, 32, 24, 16, 12, 8], T_law=440,
            J=[12, 8, 6, 5, 4, 3], T=400, anchors=[200, 320], R=4, Mc=4, HB=32,
            chunk=40, law128_eps=[0.0, 0.2, 0.4], J_law128=[16, 12, 8, 6], n_sub=VX.N_SUB)
SMOKE = dict(bench=[(32, 2), (32, 4)], bench_ticks=2, eps_law=[0.0, 0.4], J_law=[3, 2], T_law=8, J=[2], T=8, anchors=[4, 6],
             R=3, Mc=2, HB=4, chunk=4, law128_eps=[0.0, 0.4], J_law128=[2], n_sub=5)
CFG = SMOKE if args.smoke else FULL
if args.smoke:
    VX.LAB_T = 0.3                     # labelling at tick 3 of the 5-step smoke ticks
    BOX = {"eps": (0.0, 0.4), "mut128": (0.00625, 0.025), "kF": (0.015, 0.025)}
    VX.THETA0["mut128"] = 0.0125
FAILED = []


def log(msg):
    line = f"{time.strftime('%H:%M:%S')} [{(time.time() - T0) / 60:6.1f} min] {msg}"
    print(line, flush=True)
    with open(os.path.join(OUT, "progress.txt"), "a") as f:
        f.write(line + "\n")


def jdump(name, obj):
    def conv(o):
        if isinstance(o, (np.floating, np.integer)):
            return o.item()
        if isinstance(o, np.ndarray):
            return o.tolist()
        if isinstance(o, np.bool_):
            return bool(o)
        return str(o)
    p = os.path.join(OUT, name)
    with open(p + ".tmp", "w") as f:
        json.dump(obj, f, indent=1, default=conv)
    os.replace(p + ".tmp", p)


def hours():
    return (time.time() - T0) / 3600


def left_s():
    return args.max_hours * 3600 - (time.time() - T0)


def release():
    jax.clear_caches()
    gc.collect()


def mem_stats():
    try:
        s = jax.devices()[0].memory_stats()
        return {k: int(v) for k, v in s.items() if "bytes" in k} if s else None
    except Exception:
        return None


INFO = {"study": "round5/vortexexam job1", "pilot_never_reusable_as_exam": True,
        "versions": {"python": platform.python_version(), "jax": jax.__version__, "numpy": np.__version__},
        "backend": jax.default_backend(), "devices": [str(d) for d in jax.devices()], "smoke": args.smoke,
        "config": CFG, "box": BOX, "theta0": VX.THETA0, "lab_t": VX.LAB_T, "sigma_a": VX.SIGMA_A,
        "precision": "float64 world, float32 stored vortex lists"}
log(f"backend {INFO['backend']} devices {INFO['devices']} jax {jax.__version__} smoke={args.smoke}")
if args.scan_only and not args.smoke:            # a CPU fallback must not spend GPU-pod time (the Mac's review, point 1)
    assert jax.default_backend() == "gpu", f"the scan needs the GPU backend, got {jax.default_backend()!r}"
jdump("info.json", INFO)


def save_npz(name, **arrays):
    """Atomic compressed npz in OUT (a kill mid-write must not leave a truncated file; the Mac's review)."""
    p = os.path.join(OUT, name)
    np.savez_compressed(p + ".tmp.npz", **arrays)
    os.replace(p + ".tmp.npz", p)


# ----------------------------------------------------------------------------- A bench
def bench_one(H, B, nT, track=True):
    RN = VX.Runner(H, n_sub=CFG["n_sub"], track=track)
    Q = VX.theta_batch(B)
    keys = member_keys(make_key(900, H), B)
    t0 = time.time()
    X, M = RN.init(Q, keys)
    kp = RN.proc_keys(keys)
    U = np.zeros((nT, B, RN.m))
    X, M, Y = RN.run(Q, X, M, kp, 0, U)
    t_first = time.time() - t0
    t0 = time.time()
    X, M, Y = RN.run(Q, X, M, kp, nT, U)
    t_run = time.time() - t0
    r = {"H": H, "B": B, "ticks": nT, "track": track, "first_call_s": t_first, "run_s": t_run,
         "member_ticks_per_s": B * nT / t_run, "native_steps_per_s": B * nT * CFG["n_sub"] / t_run,
         "memory": mem_stats(), "K": RN.K}
    if track:
        upd = jax.jit(lambda M_, X_: jax.vmap(lambda m, x: RN.bt.update_memory(m, RN.kinds_field(x)))(M_, X_))
        M2 = upd(M, X)
        M2.block_until_ready()
        t0 = time.time()
        for _ in range(5):
            M2 = upd(M2, X)
        M2.block_until_ready()
        r["tracker_update_s_per_member"] = (time.time() - t0) / (5 * B)
        t0 = time.time()
        VX.summaries(Y.transpose(1, 0, 2), RN.K)
        VX.level2(Y, RN.K)
        VX.raster(Y, RN.K, H)
        r["host_level12_s_per_member_tick"] = (time.time() - t0) / (B * nT)
    del RN, X, M, Y
    release()
    return r


def stage_bench():
    """Rows in the declared order (the first three always run); stops adding rows after 22% of the time budget;
    then one row without the tracker per size at its best batch, while the budget lasts."""
    rows = []
    lim = 0.22 * args.max_hours * 3600
    for i, (H, B) in enumerate(CFG["bench"]):
        if i >= 3 and (time.time() - T0) > lim and not args.smoke:
            log(f"  bench H={H} B={B} skipped (time)")
            continue
        try:
            r = bench_one(H, B, CFG["bench_ticks"])
            rows.append(r)
            log(f"  bench H={H} B={B}: {r['member_ticks_per_s']:.1f} member-ticks/s "
                f"(first call {r['first_call_s']:.0f}s, tracker {1e3 * r['tracker_update_s_per_member']:.3f} ms/member, "
                f"host level-1/2 {1e3 * r['host_level12_s_per_member_tick']:.3f} ms/member-tick, mem {r['memory']})")
        except Exception as exc:
            rows.append({"H": H, "B": B, "error": repr(exc)[:500]})
            log(f"  bench H={H} B={B} FAILED {repr(exc)[:300]}")
            release()
        jdump("bench.json", {"rows": rows})
    for H in sorted(set(h for h, _ in CFG["bench"])):
        b, _ = best_rate(rows, H)
        if b is None or ((time.time() - T0) > 1.25 * lim and not args.smoke):
            continue
        try:
            r = bench_one(H, b, CFG["bench_ticks"], track=False)
            rows.append(r)
            log(f"  bench H={H} B={b} no tracker: {r['member_ticks_per_s']:.1f} member-ticks/s")
        except Exception as exc:
            log(f"  bench no-tracker FAILED {repr(exc)[:300]}")
            release()
        jdump("bench.json", {"rows": rows})
    return rows


def best_rate(rows, H):
    ok = [r for r in rows if r.get("H") == H and "error" not in r and r.get("track")]
    if not ok:
        return None, 0.0
    b = max(ok, key=lambda r: r["member_ticks_per_s"])
    return b["B"], b["member_ticks_per_s"]


def rate_at(rows, H, B):
    """Member-ticks/s expected at batch B: log-log interpolation of the bench rows of size H (linear in B below
    the smallest measured batch, flat above the largest)."""
    ok = sorted([(r["B"], r["member_ticks_per_s"]) for r in rows
                 if r.get("H") == H and "error" not in r and r.get("track")])
    if not ok:
        return 0.0
    bs, rs = np.array([b for b, _ in ok], float), np.array([r for _, r in ok], float)
    if B <= bs[0]:
        return float(rs[0] * B / bs[0])
    if B >= bs[-1]:
        return float(rs[-1])
    return float(np.exp(np.interp(np.log(B), np.log(bs), np.log(rs))))


# ----------------------------------------------------------------------------- runs
def run_main(RN, Q, keys, T, bmax, tag, snaps=()):
    """Main runs in member chunks of bmax: summaries (B, T, 12), plus device states at the snapshot ticks."""
    B = keys.shape[0]
    S = np.zeros((B, T, len(VX.S1_NAMES)), np.float32)
    snap = {a: [] for a in snaps}
    ovf = np.zeros((B, 4))
    fin = np.ones(B, bool)
    cuts = sorted(set([a for a in snaps if 0 < a < T] + [T]))
    for s in range(0, B, bmax):
        e = min(s + bmax, B)
        Qc = {k: v[s:e] for k, v in Q.items()}
        kc = keys[s:e]
        X, M = RN.init(Qc, kc)
        kp = RN.proc_keys(kc)
        t = 0
        prev = None                          # the list before the chunk (turnover across chunk borders; review point 3)
        for c in cuts:
            while t < c:
                n = min(CFG["chunk"], c - t)
                X, M, Y = RN.run(Qc, X, M, kp, t, np.zeros((n, e - s, RN.m)))
                S[s:e, t:t + n] = VX.summaries(Y.transpose(1, 0, 2), RN.K, prev=prev)
                prev = Y[-1]
                t += n
            if c in snap:
                snap[c].append((X, M))
            log(f"    {tag}: members {s}-{e} of {B} at tick {t}/{T} ({hours():.2f} h)")
        ovf[s:e] = RN.overflow(M)
        fin[s:e] = np.isfinite(np.asarray(X["om"]).reshape(e - s, -1)).all(1)
    return S, snap, ovf, fin


def stage_law(H, rows, bmax, tag="law", eps_list=None, Js=None, T=None, budget_s=None):
    eps_list = CFG["eps_law"] if eps_list is None else eps_list
    Js = CFG["J_law"] if Js is None else Js
    T = CFG["T_law"] if T is None else T
    J = Js[-1]
    for j in Js:
        B = j * len(eps_list)
        r = rate_at(rows, H, min(B, bmax))
        if budget_s is None or r <= 0 or B * T / r <= budget_s:
            J = j
            break
    log(f"  {tag}: H={H} J={J} x {len(eps_list)} eps x T={T} (budget {budget_s if budget_s is None else round(budget_s)}s, "
        f"est {J * len(eps_list) * T / max(rate_at(rows, H, min(J * len(eps_list), bmax)), 1e-9):.0f}s)")
    RN = VX.Runner(H, n_sub=CFG["n_sub"])
    keys1 = member_keys(make_key(5101, H), J)
    keys = jnp.concatenate([keys1] * len(eps_list))
    Q = VX.theta_batch(J * len(eps_list), eps=np.repeat(eps_list, J))
    t0 = time.time()
    S, _, ovf, fin = run_main(RN, Q, keys, T, bmax, tag)
    dt = time.time() - t0
    save_npz(f"{tag}.npz", S=S.reshape(len(eps_list), J, T, -1), eps=np.array(eps_list),
                        overflow=ovf, finite=fin, names=np.array(VX.S1_NAMES))
    info = {"H": H, "eps": eps_list, "J": J, "T": T, "seconds": dt, "member_ticks": J * len(eps_list) * T,
            "member_ticks_per_s": J * len(eps_list) * T / dt, "keys": f"member_keys(make_key(5101, {H}), J), shared by all eps",
            "overflow_max": ovf.max(0).tolist(), "all_finite": bool(fin.all()),
            "s_b_end_mean_by_eps": S.reshape(len(eps_list), J, T, -1)[:, :, -20:, 1].mean((1, 2)).tolist(),
            "N_end_mean_by_eps": S.reshape(len(eps_list), J, T, -1)[:, :, -20:, 0].mean((1, 2)).tolist()}
    jdump(f"{tag}.json", info)
    log(f"  {tag}: {info['member_ticks_per_s']:.1f} member-ticks/s; s_b(end) by eps {np.round(info['s_b_end_mean_by_eps'], 3).tolist()} "
        f"N(end) {np.round(info['N_end_mean_by_eps'], 1).tolist()}")
    del RN
    release()
    return info


def stage_scan(H, rows, bmax, budget_s):
    names = ["null"] + [f"{p}@{e}" for p in BOX for e in ("lo", "hi")]
    T, R, Mc, HB = CFG["T"], CFG["R"], CFG["Mc"], CFG["HB"]
    nS = len(names)

    def est(J_, na):
        main = nS * J_ * T / max(rate_at(rows, H, min(nS * J_, bmax)), 1e-9)
        br = nS * J_ * na * (R + Mc) * HB / max(rate_at(rows, H, min(nS * J_ * (R + Mc), bmax)), 1e-9)
        return main + br
    J, anchors = CFG["J"][-1], list(CFG["anchors"])[:1]
    done = False
    for na in (len(CFG["anchors"]), 1):
        for j in CFG["J"]:
            if est(j, na) <= budget_s:
                J, anchors, done = j, list(CFG["anchors"])[:na], True
                break
        if done:
            break
    log(f"  scan: {nS} settings x J={J}, T={T}, anchors {anchors}, R={R}, Mc={Mc}, HB={HB}: "
        f"{nS * J * T + nS * J * len(anchors) * (R + Mc) * HB} member-ticks, est {est(J, len(anchors)):.0f}s of {budget_s:.0f}s")
    over = {k: np.full(nS * J, VX.THETA0[k]) for k in BOX}
    for i, nm in enumerate(names):
        if nm != "null":
            p, edge = nm.split("@")
            over[p][i * J:(i + 1) * J] = BOX[p][0 if edge == "lo" else 1]
    Q = VX.theta_batch(nS * J, **over)
    Q0 = VX.theta_batch(nS * J)
    keys1 = member_keys(make_key(5202, H), J)
    keys = jnp.concatenate([keys1] * nS)
    RN = VX.Runner(H, n_sub=CFG["n_sub"])
    t0 = time.time()
    S, snap, ovf, fin = run_main(RN, Q, keys, T, bmax, "scan main", snaps=anchors)
    save_npz("scan_main.npz", S=S.reshape(nS, J, T, -1), settings=np.array(names),
                        overflow=ovf.reshape(nS, J, 4), finite=fin.reshape(nS, J), names=np.array(VX.S1_NAMES))
    info = {"H": H, "settings": names, "J": J, "T": T, "anchors": anchors, "R": R, "Mc": Mc, "HB": HB,
            "main_seconds": time.time() - t0, "box": BOX,
            "keys": f"member_keys(make_key(5202, {H}), J) shared by all settings; branch keys make_key(5203, H, anchor) "
                    f"shared by all settings (truth replicate r and control c have different keys)"}
    jdump("scan.json", info)
    log(f"  scan main done in {info['main_seconds']:.0f}s")
    # branches: level 2 is saved in full; the level-1 block raster (2 x (H/16)^2 numbers per state) is scored
    # here and only the scores are saved (the rasters of the first run were 40 MB, over the 20 MB git limit)
    G2 = 2 * (H // 16) ** 2
    HS1 = [h for h in (1, 2, 4, 8) if h <= HB]
    nrep = R + Mc
    L2b = np.zeros((nS, J, len(anchors), nrep, HB, 2), np.float32)
    es_c1 = np.full((nS, J, len(anchors), len(HS1)), np.nan)         # ES_fair(controls, truths), level-1 raster
    es_o1 = np.full((nS, J, len(anchors), len(HS1)), np.nan)         # ES_loo(truths)
    es_k1 = np.full((nS, J, len(anchors), len(HS1)), np.nan)         # ES_fair(other members' truths, truths)
    sc1 = None
    for ai, a in enumerate(anchors):
        if left_s() < 240 and not args.smoke:
            log(f"  scan branches at anchor {a} skipped (time)")
            FAILED.append(f"skipped scan branches {a}")
            continue
        X = jax.tree_util.tree_map(lambda *xs: jnp.concatenate(xs), *[x for x, _ in snap[a]])
        M = jnp.concatenate([m for _, m in snap[a]])
        Bm = nS * J
        idx = np.repeat(np.arange(Bm), nrep)                       # member-major, replicate-minor
        is_ctl = np.tile(np.arange(nrep) >= R, Bm)
        Qb = {k: np.where(is_ctl, Q0[k][idx], Q[k][idx]) for k in Q}
        kb1 = member_keys(make_key(5203, H, a), J * nrep)           # shared by all settings
        kb = jnp.concatenate([kb1] * nS)
        kp = RN.proc_keys(kb, fresh=True)
        l2 = np.zeros((Bm * nrep, HB, 2), np.float32)
        r1 = np.zeros((Bm * nrep, len(HS1), G2), np.float32)
        for s in range(0, Bm * nrep, bmax):
            e = min(s + bmax, Bm * nrep)
            ii = idx[s:e]
            Xc, Mc_ = VX.take(X, ii), VX.take(M, ii)
            _, _, Y = RN.run({k: v[s:e] for k, v in Qb.items()}, Xc, Mc_, kp[s:e], a, np.zeros((HB, e - s, RN.m)))
            Yt = Y.transpose(1, 0, 2)
            l2[s:e] = VX.level2(Yt, RN.K)
            r1[s:e] = VX.raster(Yt[:, [h - 1 for h in HS1]], RN.K, H)
            log(f"    scan branches anchor {a}: {e}/{Bm * nrep} ({hours():.2f} h)")
        L2b[:, :, ai] = l2.reshape(nS, J, nrep, HB, 2)
        r1 = r1.reshape(nS, J, nrep, len(HS1), G2).astype(float)
        if sc1 is None:                                            # public scales: sd of the null truths per raster half
            g = G2 // 2
            sc1 = np.r_[np.full(g, max(r1[0, :, :R, :, :g].std(), 1e-6)), np.full(g, max(r1[0, :, :R, :, g:].std(), 1e-6))]
        for k in range(len(HS1)):
            es_c1[:, :, ai, k], es_o1[:, :, ai, k], es_k1[:, :, ai, k], _ = VX.raster_scores(r1[:, :, :, k], R, sc1)
        save_npz("scan_branch.npz", L2=L2b, es_c1=es_c1, es_o1=es_o1, es_k1=es_k1,
                            hs1=np.array(HS1), sc1=sc1, settings=np.array(names), anchors=np.array(anchors), R=R, Mc=Mc)
    info["seconds"] = time.time() - t0
    info["member_ticks"] = nS * J * T + nS * J * len(anchors) * (R + Mc) * HB
    jdump("scan.json", info)
    del RN, snap
    release()
    return info


def main():
    if args.scan_only:
        H_only = args.H or 128
        rate = args.rate
        if args.rate_json and os.path.exists(args.rate_json):
            try:
                rate = max(100.0, 0.9 * float(json.load(open(args.rate_json)).get("rate", rate)))
            except Exception as exc:
                log(f"  --rate-json unreadable ({exc!r}); using --rate {rate}")
        rows = [{"H": H_only, "B": args.bmax, "track": True, "member_ticks_per_s": rate}]
        INFO.update(H_exam=H_only, H_rule="--scan-only", bmax=args.bmax, rate=rate)
        stage_scan(H_only, rows, args.bmax, budget_s=max(left_s() - 90, 60))
        INFO["hours"], INFO["failed"] = hours(), FAILED
        jdump("info.json", INFO)
        log(f"done (scan only) in {hours():.2f} h; failed {FAILED}")
        return
    rows = stage_bench()
    hs = sorted(set(h for h, _ in CFG["bench"]), reverse=True)
    sizes = [h for h in (128, 96, 64) if h in hs] or hs
    H_exam, why = None, ""
    for h in sizes:
        b, rt = best_rate(rows, h)
        if rt >= args.min_rate:
            H_exam, why = h, f"largest size with >= {args.min_rate} member-ticks/s ({rt:.0f} at B={b})"
            break
    if H_exam is None:
        H_exam = sizes[-1]
        why = "no size reaches the minimum rate; the smallest is used"
    if args.H:
        H_exam, why = args.H, "--H override"
    bmax, rate = best_rate(rows, H_exam)
    if bmax is None:
        bmax, rate = 64, 0.0
    INFO["H_exam"], INFO["H_rule"], INFO["bmax"], INFO["rate"] = H_exam, why, bmax, rate
    jdump("info.json", INFO)
    log(f"== H_exam = {H_exam} ({why}); batch {bmax}, {rate:.1f} member-ticks/s")
    tot = left_s() - 120
    try:
        stage_law(H_exam, rows, bmax, budget_s=0.30 * tot)
    except Exception as exc:
        FAILED.append("law")
        log(f"law FAILED {exc!r}\n{traceback.format_exc()}")
        release()
    try:
        stage_scan(H_exam, rows, bmax, budget_s=max(left_s() - 420, 60))
    except Exception as exc:
        FAILED.append("scan")
        log(f"scan FAILED {exc!r}\n{traceback.format_exc()}")
        release()
    if H_exam != 128 and 128 in hs:
        b128, r128 = best_rate(rows, 128)
        if b128 and left_s() > 240:
            try:
                stage_law(128, rows, b128, tag="law128", eps_list=CFG["law128_eps"], Js=CFG["J_law128"],
                          budget_s=left_s() - 150)
            except Exception as exc:
                FAILED.append("law128")
                log(f"law128 FAILED {exc!r}")
        else:
            log(f"  law128 skipped: {left_s():.0f}s left")
    elif args.smoke:
        stage_law(hs[0], rows, 4, tag="law128", eps_list=CFG["law128_eps"], Js=CFG["J_law128"])
    INFO["hours"] = hours()
    INFO["failed"] = FAILED
    jdump("info.json", INFO)
    log(f"done in {hours():.2f} h; failed {FAILED}")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        log(f"FATAL {exc!r}\n{traceback.format_exc()}")
        INFO["fatal"] = repr(exc)
        jdump("info.json", INFO)
        sys.exit(1)
    if [f for f in FAILED if not f.startswith("skipped")]:
        sys.exit(2)
