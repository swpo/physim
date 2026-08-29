"""recbench.py — t2record microbench: WHERE does the record path serialize?

H100 evidence (t2 instrumented, workload 697bcb716916): record tracking =
2299 s cumulative vs 1505 s wall (~1.5 effective threads from
BLOBGPU_REC_THREADS=8) = 60%+ of the batch wall. This microbench isolates
the record path from sim/battery and measures:

  A. scaling: the driver's exact record_all pattern (ThreadPoolExecutor.map
     over per-lane _record) at 1/2/4/8 threads, vs a PROCESS pool running a
     pure extract (apply on host), vs serial. -> effective parallelism.
  B. components (serial, per record point): f64 convert, ndimage.label,
     periodic union-find, bincounts, peak, org_patches, coarse — which op
     holds the GIL / burns the time.
  C. GIL probe: 2 threads on independent arrays for label / blob_list_fast /
     a known GIL-releasing control (np.dot big) — direct serialization test.

States are REAL: sim_cpu init_soup + advance to T_state (locked kernel, has
blobs), replicated to B lanes (same state per lane = identical work: clean
scaling denominators; records only read F + thresholds).

Also here: extract_record/apply_record — the process-pool-safe split of the
LOCKED sim_cpu._record (verbatim rules; extract is jax-free and picklable;
apply does the stateful/sequential part: dead_since, status, snaps pops).
identity_gate() proves stock _record vs extract+apply produce IDENTICAL
record streams on the same states. This is the shape of fix (a) in
GAINS.md; the engine change itself is 0.4 work, gated V1-style.
"""
import copy
import time
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor

import numpy as np

from blobkit import genome as G
from blobkit.soup import sim_cpu as SC
from blobkit.soup.sim_v1 import blob_list_fast, coarse


# ------------------------------------------------------- extract / apply
def extract_record(ctx, acts, chans_mem, t, want_snap_f64=False):
    """Pure half of sim_cpu._record (verbatim math, no S mutation).
    ctx: dict(na, dx, L, thr_a, thr_lo, memch, rec, crec).
    acts: (na, N, N) activator fields (any float dtype, natural layout).
    chans_mem: {c: (N, N) field} for ctx['memch'] (only needed on CREC).
    -> delta dict; apply_record() replays it into S (stateful rules)."""
    na, dx, L = ctx["na"], ctx["dx"], ctx["L"]
    rec, crec = ctx["rec"], ctx["crec"]
    d = dict(t=t, rec=(t % rec == 0), crec=(t % crec == 0))
    if d["rec"]:
        if not np.isfinite(acts).all():
            d["blowup"] = True
            return d
        blobs, mass, ntot = [], [], 0
        for i in range(na):
            u = np.asarray(acts[i], np.float64)
            bl = blob_list_fast(u, ctx["thr_a"][i], dx, L)
            blobs.append([[b["y"], b["x"], b["area"], b["peak"]]
                          for b in bl])
            mass.append(float(np.clip(u - ctx["thr_a"][i], 0, None)
                              .sum() * dx * dx))
            ntot += len(bl)
        d["blobs"], d["mass"], d["ntot"] = blobs, mass, ntot
    if d["crec"]:
        patches, orgs = [], []
        for i in range(na):
            u = np.asarray(acts[i], np.float64)
            labm, k = G.periodic_label(u > ctx["thr_a"][i])
            sz = [float((labm == j).sum()) * dx * dx for j in range(1, k + 1)]
            patches.append(dict(n=k, sizes=sz,
                                cover=float((u > ctx["thr_a"][i]).mean())))
            orgs.append(SC.org_patches(u, ctx["thr_lo"][i], dx, L))
        d["patches"], d["orgs"] = patches, orgs
        d["memf"] = {c: coarse(np.asarray(chans_mem[c], np.float64))
                     for c in ctx["memch"]}
    if want_snap_f64:
        d["acts_f64"] = np.asarray(acts, np.float64).copy()
    return d


def apply_record(S, d, t):
    """Stateful half of sim_cpu._record (verbatim order/rules). Returns
    False on blowup/dead exit, mirroring _record's return."""
    dt = S["dt"]
    tt = t * dt
    na = S["na"]
    if d["rec"]:
        if d.get("blowup"):
            S["status"] = "blowup"
            return False
        for i in range(na):
            S["blobs"][i].append(d["blobs"][i])
            S["mass"][i].append(d["mass"][i])
        S["ts"].append(tt)
        if d["ntot"] == 0:
            if S["dead_since"] is None:
                S["dead_since"] = tt
            if tt - S["dead_since"] > 200.0 and tt > 400.0:
                S["status"] = "all_dead"
                return False
        else:
            S["dead_since"] = None
    if d["crec"]:
        S["cts"].append(tt)
        for i in range(na):
            S["patches"][i].append(d["patches"][i])
            S["orgs"][i].append(d["orgs"][i])
        for c in S["memch"]:
            S["memf"][c].append(d["memf"][c])
    while S["snap_t"] and tt >= S["snap_t"][0] - 1e-9:
        S["snaps"][S["snap_t"].pop(0)] = d["acts_f64"]
    return True


def ctx_of(S):
    return dict(na=S["na"], dx=S["dx"], L=S["L"],
                thr_a=np.asarray(S["thr_a"]), thr_lo=np.asarray(S["thr_lo"]),
                memch=list(S["memch"]), rec=S["rec"], crec=S["crec"])


def payload_of(S, t):
    """(ctx, acts, chans_mem, snap_due) for extract at step t."""
    na = S["na"]
    F = S["F"]
    chans_mem = ({c: F[na + c] for c in S["memch"]}
                 if t % S["crec"] == 0 else {})
    tt = t * S["dt"]
    snap_due = bool(S["snap_t"] and tt >= S["snap_t"][0] - 1e-9)
    return ctx_of(S), F[:na], chans_mem, snap_due


def _extract_star(args):
    return extract_record(*args)


# ------------------------------------------------------------ identity
def identity_gate(worlds=("m0", "pred"), N_L=64.0, T_state=250.0, seed=1,
                  n_points=6, verbose=True):
    """Stock _record vs extract+apply on the same advanced states: record
    streams must be EXACTLY equal (== on lists incl. float repr identity:
    same ops, same order, same dtypes)."""
    from blobkit import worlds as W
    ok_all = True
    for wname in worlds:
        g = W.load(wname)
        S = SC.init_soup(g, L=N_L, seed=seed, workers=1)
        SC.advance(S, T_state)
        A = copy.deepcopy(S)
        B = copy.deepcopy(S)
        A["snap_t"] = list(B["snap_t"])
        t0 = ((S["t_step"] // S["crec"]) + 1) * S["crec"]
        for k in range(n_points):
            t = t0 + k * S["rec"]
            okA = SC._record(A, t)
            ctx, acts, chm, snap_due = payload_of(B, t)
            d = extract_record(ctx, acts, chm, t, want_snap_f64=snap_due)
            okB = apply_record(B, d, t)
            assert okA == okB, (wname, t, okA, okB)
        same = (A["ts"] == B["ts"] and A["cts"] == B["cts"]
                and A["mass"] == B["mass"] and A["blobs"] == B["blobs"]
                and A["patches"] == B["patches"]
                and str(A["orgs"]) == str(B["orgs"])
                and all(np.array_equal(A["memf"][c][i], B["memf"][c][i])
                        for c in A["memf"] for i in range(len(A["memf"][c])))
                and A["status"] == B["status"]
                and A["dead_since"] == B["dead_since"]
                and sorted(A["snaps"]) == sorted(B["snaps"])
                and all(np.array_equal(A["snaps"][k], B["snaps"][k])
                        for k in A["snaps"]))
        ok_all &= same
        if verbose:
            print(f"[identity {wname}] {'PASS' if same else 'FAIL'} "
                  f"({len(A['ts'])} rec points, {len(A['cts'])} crec, "
                  f"{len(A['snaps'])} snaps)", flush=True)
    return ok_all


# ------------------------------------------------------------- states
def build_lanes(profile):
    """B lanes of REAL advanced states (locked CPU kernel). Same state per
    world-class across lanes -> identical work, clean scaling."""
    from blobkit import worlds as W
    L = 64.0 if profile == "cpu" else 128.0
    T_state = 250.0
    specs = ["m0", "pred"]           # 1-act light + 3-act heavy (record-wise)
    B = 16
    bases = {}
    for wname in specs:
        g = W.load(wname)
        S = SC.init_soup(g, L=L, seed=1, workers=4)
        SC.advance(S, T_state)
        S["snap_t"] = []
        S["workers"] = 0
        bases[wname] = S
    lanes = [copy.deepcopy(bases[specs[i % len(specs)]]) for i in range(B)]
    return lanes, dict(L=L, T_state=T_state, B=B, specs=specs)


# -------------------------------------------------------------- scaling
def bench_scaling(lanes, rounds=6):
    """Driver-shaped record_all at various executors. Each round = one
    record point per lane (5:1 REC:CREC mix like the real grid).
    Returns dict of {mode: dict(wall_s, ms_per_record, speedup)}."""
    def points(S, r):
        # rounds hit fresh grid points; every 5th+1 is a CREC point
        base = ((S["t_step"] // S["crec"]) + 2 + r) * S["rec"]
        if r % 5 == 0:
            base = ((S["t_step"] // S["crec"]) + 2 + r) * S["crec"]
        return base

    def record_one(args):
        S, t = args
        SC._record(S, t)

    res = {}
    n_rec = len(lanes) * rounds

    def run_serial():
        for r in range(rounds):
            for S in lanes:
                record_one((S, points(S, r)))

    t0 = time.perf_counter()
    run_serial()
    serial_s = time.perf_counter() - t0
    res["serial"] = dict(wall_s=round(serial_s, 3),
                         ms_per_record=round(1e3 * serial_s / n_rec, 2),
                         speedup=1.0)

    for nT in (2, 4, 8):
        ex = ThreadPoolExecutor(nT)
        t0 = time.perf_counter()
        for r in range(rounds):
            list(ex.map(record_one,
                        [(S, points(S, r + 100)) for S in lanes]))
        w = time.perf_counter() - t0
        ex.shutdown()
        res[f"threads{nT}"] = dict(wall_s=round(w, 3),
                                   ms_per_record=round(1e3 * w / n_rec, 2),
                                   speedup=round(serial_s / w, 2))

    import multiprocessing as mp
    for nP in (2, 4, 8):
        ex = ProcessPoolExecutor(nP, mp_context=mp.get_context("spawn"))
        # warm the pool (spawn + imports out of the timed section)
        list(ex.map(_extract_star,
                    [payload_of(S, (S["t_step"] // S["crec"] + 50)
                                * S["crec"]) + ((S["t_step"] // S["crec"]
                                                 + 50) * S["crec"],)
                     for S in lanes[:nP]]))
        t0 = time.perf_counter()
        for r in range(rounds):
            args = []
            for S in lanes:
                t = points(S, r + 200)
                ctx, acts, chm, snap = payload_of(S, t)
                args.append((ctx, acts, chm, t, snap))
            deltas = list(ex.map(_extract_star, args))
            for S, dlt in zip(lanes, deltas):
                apply_record(S, dlt, dlt["t"])
        w = time.perf_counter() - t0
        ex.shutdown()
        res[f"procs{nP}"] = dict(wall_s=round(w, 3),
                                 ms_per_record=round(1e3 * w / n_rec, 2),
                                 speedup=round(serial_s / w, 2))
    return res


# ----------------------------------------------------------- components
def bench_components(lanes, reps=20):
    """Serial per-op timing on the heavy lane class (pred). -> ms each."""
    from scipy import ndimage as ndi
    S = next(ln for ln in lanes if ln["na"] > 1)
    na, dx, L = S["na"], S["dx"], S["L"]
    u_all = [np.asarray(S["F"][i], np.float64) for i in range(na)]
    out = {}

    def t_ms(fn, n=reps):
        t0 = time.perf_counter()
        for _ in range(n):
            fn()
        return round(1e3 * (time.perf_counter() - t0) / n, 3)

    out["f64_convert"] = t_ms(
        lambda: [np.asarray(S["F"][i], np.float64) for i in range(na)])
    out["ndimage_label"] = t_ms(
        lambda: [ndi.label(u > S["thr_a"][i])
                 for i, u in enumerate(u_all)])
    out["periodic_label"] = t_ms(
        lambda: [G.periodic_label(u > S["thr_a"][i])
                 for i, u in enumerate(u_all)])
    out["blob_list_fast"] = t_ms(
        lambda: [blob_list_fast(u, S["thr_a"][i], dx, L)
                 for i, u in enumerate(u_all)])
    out["mass_clip_sum"] = t_ms(
        lambda: [float(np.clip(u - S["thr_a"][i], 0, None).sum() * dx * dx)
                 for i, u in enumerate(u_all)])
    out["org_patches"] = t_ms(
        lambda: [SC.org_patches(u, S["thr_lo"][i], dx, L)
                 for i, u in enumerate(u_all)], n=max(reps // 2, 5))
    out["patches_sizes"] = t_ms(
        lambda: [[float((G.periodic_label(u > S["thr_a"][i])[0] == j).sum())
                  for j in range(1, G.periodic_label(u > S["thr_a"][i])[1]
                                 + 1)]
                 for i, u in enumerate(u_all)], n=max(reps // 2, 5))
    out["coarse_memf"] = t_ms(
        lambda: [coarse(np.asarray(S["F"][S["na"] + c], np.float64))
                 for c in S["memch"]])
    out["record_REC_total"] = t_ms(
        lambda: [(blob_list_fast(u, S["thr_a"][i], dx, L),
                  float(np.clip(u - S["thr_a"][i], 0, None).sum() * dx * dx))
                 for i, u in enumerate(u_all)])
    return out


def bench_gil(lanes, reps=12):
    """2 threads on INDEPENDENT copies vs serial x2: speedup ~2 = releases
    GIL; ~1 = serialized by GIL. np.dot control included."""
    from scipy import ndimage as ndi
    S = next(ln for ln in lanes if ln["na"] > 1)
    u1 = np.asarray(S["F"][0], np.float64)
    u2 = u1.copy()
    thr = S["thr_a"][0]
    dx, L = S["dx"], S["L"]
    big1 = np.random.default_rng(0).standard_normal((600, 600))
    big2 = big1.copy()

    cases = dict(
        ndimage_label=lambda u: [ndi.label(u > thr) for _ in range(reps)],
        periodic_label=lambda u: [G.periodic_label(u > thr)
                                  for _ in range(reps)],
        blob_list_fast=lambda u: [blob_list_fast(u, thr, dx, L)
                                  for _ in range(reps)],
        np_dot_control=lambda u: [np.dot(u, u.T) for _ in range(reps)],
    )
    out = {}
    for name, fn in cases.items():
        a1 = big1 if "control" in name else u1
        a2 = big2 if "control" in name else u2
        t0 = time.perf_counter()
        fn(a1); fn(a2)
        serial = time.perf_counter() - t0
        ex = ThreadPoolExecutor(2)
        t0 = time.perf_counter()
        list(ex.map(fn, [a1, a2]))
        par = time.perf_counter() - t0
        ex.shutdown()
        out[name] = dict(serial_s=round(serial, 3), par2_s=round(par, 3),
                         speedup=round(serial / par, 2))
    return out


def run(profile="cpu", verbose=True):
    t0 = time.time()
    gate = identity_gate(verbose=verbose)
    lanes, meta = build_lanes(profile)
    scal = bench_scaling(lanes)
    comp = bench_components(lanes)
    gil = bench_gil(lanes)
    detail = dict(meta=meta, identity_pass=bool(gate), scaling=scal,
                  components=comp, gil=gil,
                  build_and_bench_wall_s=round(time.time() - t0, 1))
    if verbose:
        print("[t2record] identity:", "PASS" if gate else "FAIL")
        for k, v in scal.items():
            print(f"[t2record scaling] {k:9s} {v['ms_per_record']:7.2f} "
                  f"ms/record  x{v['speedup']:.2f}")
        print("[t2record components(ms)]",
              {k: v for k, v in sorted(comp.items(), key=lambda x: -x[1])})
        for k, v in gil.items():
            print(f"[t2record gil] {k:16s} 2-thread speedup x{v['speedup']}")
    return detail
