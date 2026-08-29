"""blobkit.soup.devrec_proto — device-side REC-grid records [PROTOTYPE-GATED].

PROTOTYPE-GATED (blobkit 0.3.3): verbatim promotion of the blobkit-perf
thread's proto_devrec.py (perf/ bench flag --devrec). 0.4 makes this
driver-native (record_mode="device" + _record_device in sim_gpu); until
then the fleet enables it via island_config {"record_mode": "device"}
(+ {"apply_mode": "async"} to compose with asyncapply_proto) —
pod_worker_batch calls install() before its shard loop.

Gates passed (perf/results/, 2026-08-29; DESIGN_DEVREC.md for the full
experiment chain E1-E4): gate_batch inline + async vs stock (ts/cts/
status/t_step/patches/orgs/snaps identical; blob sets identical, area/
peak EXACT, y/x/mass worst rel err 3.8e-13 vs 1e-12 tol; ZERO fallbacks);
assay-level decision identity; E4 x64-flag flip bit-safe for the f32
stepper. CLAIM ROW: t2 frozen workload 697bcb716916 on H100:
42.31 -> 92.20 w/h (2.18x, --devrec --asyncapply), 4779 device points /
14737 lane-records, 0 fallbacks, T_used ladder identical.

Pipeline (parity policy: exact ints/max/partition; f64-accumulated sums
tolerance-gated at 1e-12):
  REC-only points (driver pull signal full=False): NO host field pull.
  One jitted kernel fused over (B*na_max) fields: f64-threshold mask
  (host-exact), isfinite, scatter-min root-merge CCL (outer=5/jumps=8,
  device convergence flag), dense-rank f64 segment stats (MAXL=256 rows
  + overflow flag), on-device acts_snap for fallback lanes. Host: blob
  rows via np.angle f64 (verbatim blob_list_fast math) + the verbatim
  _record REC-grid stateful tail. CREC points / snapshots / fallback
  lanes (unconverged / overflow / non-finite): stock host path.

Usage:
    from blobkit.soup import devrec_proto as DR
    DR.install()                    # inline applies (sync, pull-less)
    DR.install(async_apply=True)    # + asyncapply_proto drain machinery
    ...
    DR.uninstall()
"""
import atexit
import os
import time

import numpy as np

from . import driver as DRV

CCL_OUTER = 5          # E1c converged at 4 on real+spiral; +1 margin
CCL_JUMPS = 8
MAXL = 256             # blob rows per field; overflow -> host fallback

_STATE = dict(orig=None, kernels={}, stats=dict(
    points_dev=0, points_host=0, lanes_dev=0, lanes_fallback=0,
    fb_unconv=0, fb_overflow=0, fb_nonfinite=0,
    dispatch_s=0.0, flags_s=0.0, rows_pull_s=0.0, assemble_s=0.0,
    apply_s=0.0))


# ------------------------------------------------------------ the kernel
def _get_kernel(N, na_max, dtype_str):
    """acts (B, na_max, N, N) -> per-field blob stats + flags + acts_snap.
    Cached per (N, na_max, dtype)."""
    key = (N, na_max, dtype_str)
    k = _STATE["kernels"].get(key)
    if k is not None:
        return k
    import jax
    import jax.numpy as jnp
    NN = N * N
    ang = 2 * np.pi * (np.arange(N) + 0.5) / N
    cy = jnp.asarray(np.cos(ang), jnp.float64)
    sy = jnp.asarray(np.sin(ang), jnp.float64)
    PYc = jnp.broadcast_to(cy[:, None], (N, N)).reshape(NN)
    PYs = jnp.broadcast_to(sy[:, None], (N, N)).reshape(NN)
    PXc = jnp.broadcast_to(cy[None, :], (N, N)).reshape(NN)
    PXs = jnp.broadcast_to(sy[None, :], (N, N)).reshape(NN)

    @jax.jit
    def kernel(acts, thr):
        """thr (B, na_max) f64 (+inf pads -> empty masks)."""
        B, na = acts.shape[0], acts.shape[1]
        F = acts.reshape(B * na, N, N)
        t = thr.reshape(B * na)
        finite = jnp.all(jnp.isfinite(F), axis=(-2, -1))
        u64 = F.astype(jnp.float64)
        mask = (u64 > t[:, None, None]) & finite[:, None, None]

        # CCL (E1c): flat table with a background sink slot at NN
        idx = jnp.arange(NN, dtype=jnp.int32).reshape(1, N, N)
        BIG = jnp.int32(NN)
        lab0 = jnp.where(mask, jnp.broadcast_to(idx, mask.shape), BIG)
        labf = jnp.concatenate(
            [lab0.reshape(-1, NN), jnp.full((B * na, 1), BIG, jnp.int32)],
            axis=1)
        brow = jnp.arange(B * na)[:, None]

        def compress(lf):
            def jmp(_, lf):
                tgt = jnp.take_along_axis(lf, lf[:, :NN], axis=1)
                return lf.at[:, :NN].set(jnp.minimum(lf[:, :NN], tgt))
            return jax.lax.fori_loop(0, CCL_JUMPS, jmp, lf)

        def outer_body(_, lf):
            lf = compress(lf)
            lab2 = lf[:, :NN].reshape(-1, N, N)
            n1 = jnp.roll(lab2, 1, axis=-1)
            n2 = jnp.roll(lab2, -1, axis=-1)
            n3 = jnp.roll(lab2, 1, axis=-2)
            n4 = jnp.roll(lab2, -1, axis=-2)
            nmin = jnp.minimum(jnp.minimum(n1, n2), jnp.minimum(n3, n4))
            nmin = jnp.where(mask, nmin, BIG).reshape(-1, NN)
            return lf.at[brow, lf[:, :NN]].min(nmin)

        labf = jax.lax.fori_loop(0, CCL_OUTER, outer_body, labf)
        labf = compress(labf)
        probe = compress(outer_body(0, labf))
        converged = jnp.all(probe[:, :NN] == labf[:, :NN], axis=1)
        flat = labf[:, :NN]

        # dense rank (E2b)
        order = jnp.argsort(flat, axis=1)
        sl = jnp.take_along_axis(flat, order, axis=1)
        newseg = jnp.concatenate([jnp.ones((B * na, 1), bool),
                                  sl[:, 1:] != sl[:, :-1]], axis=1)
        newseg = newseg & (sl < NN)
        rank_sorted = (jnp.cumsum(newseg, axis=1) - 1).astype(jnp.int32)
        rank = jnp.zeros_like(flat).at[brow, order].set(rank_sorted)
        rank = jnp.where(flat < NN, jnp.minimum(rank, MAXL), MAXL)
        nlab = jnp.where(jnp.any(newseg, axis=1), rank_sorted[:, -1] + 1, 0)
        overflow = nlab > MAXL

        # f64 segment stats (E2c policy)
        w = jnp.where(mask, jnp.clip(u64 - t[:, None, None], 0.0, None),
                      0.0).reshape(-1, NN)
        uf = u64.reshape(-1, NN)

        def seg(vals):
            out = jnp.zeros((B * na, MAXL + 1), jnp.float64)
            return out.at[brow, rank].add(vals)

        tot = seg(w)
        area = seg((flat < NN).astype(jnp.float64))
        zyr = seg(w * PYc[None]); zyi = seg(w * PYs[None])
        zxr = seg(w * PXc[None]); zxi = seg(w * PXs[None])
        peak = jnp.full((B * na, MAXL + 1), -jnp.inf, jnp.float64).at[
            brow, rank].max(uf)
        mass = jnp.sum(w, axis=1)          # order != np.sum -> tol-gated
        return dict(tot=tot[:, :MAXL], area=area[:, :MAXL],
                    zyr=zyr[:, :MAXL], zyi=zyi[:, :MAXL],
                    zxr=zxr[:, :MAXL], zxi=zxi[:, :MAXL],
                    peak=peak[:, :MAXL], nlab=nlab, mass=mass,
                    converged=converged, overflow=overflow, finite=finite,
                    acts_snap=acts)

    _STATE["kernels"][key] = kernel
    return kernel


# ----------------------------------------------------------- host halves
def _assemble_blobs(o, fi, N, dx):
    """Stat rows of field fi -> blob_list rows [[y, x, area, peak]...]
    (host f64 angle math, verbatim blob_list_fast)."""
    out = []
    tot = o["tot"][fi]; area = o["area"][fi]; peak = o["peak"][fi]
    zyr = o["zyr"][fi]; zyi = o["zyi"][fi]
    zxr = o["zxr"][fi]; zxi = o["zxi"][fi]
    for j in range(int(min(o["nlab"][fi], MAXL))):
        if tot[j] <= 0:
            continue
        y = (np.angle((zyr[j] + 1j * zyi[j]) / tot[j]) % (2 * np.pi)) \
            / (2 * np.pi) * N * dx
        x = (np.angle((zxr[j] + 1j * zxi[j]) / tot[j]) % (2 * np.pi)) \
            / (2 * np.pi) * N * dx
        out.append([float(y), float(x), float(area[j]) * dx * dx,
                    float(peak[j])])
    return out


def _apply_dev_record(S, rows_bl, mass_vals, t):
    """REC-grid stateful tail (verbatim _record REC branch). Caller
    guarantees t is NOT a CREC point and no snapshot is due."""
    tt = t * S["dt"]
    ntot = 0
    for i in range(S["na"]):
        S["blobs"][i].append(rows_bl[i])
        S["mass"][i].append(mass_vals[i])
        ntot += len(rows_bl[i])
    S["ts"].append(tt)
    if ntot == 0:
        if S["dead_since"] is None:
            S["dead_since"] = tt
        if tt - S["dead_since"] > 200.0 and tt > 400.0:
            S["status"] = "all_dead"
            return False
    else:
        S["dead_since"] = None
    return True


class _DevPoint:
    """Kernel outputs for one record point (device handles + lazy pulls)."""

    def __init__(self, out, na_max, N):
        self.out = out
        self.na_max = na_max
        self.N = N
        self._flags = None
        self._rows = None

    def flags(self):
        if self._flags is None:
            t0 = time.perf_counter()
            self._flags = dict(
                converged=np.asarray(self.out["converged"]),
                overflow=np.asarray(self.out["overflow"]),
                finite=np.asarray(self.out["finite"]))
            _STATE["stats"]["flags_s"] += time.perf_counter() - t0
        return self._flags

    def rows(self):
        if self._rows is None:
            t0 = time.perf_counter()
            self._rows = {k: np.asarray(self.out[k]) for k in
                          ("tot", "area", "zyr", "zyi", "zxr", "zxi",
                           "peak", "nlab", "mass")}
            _STATE["stats"]["rows_pull_s"] += time.perf_counter() - t0
        return self._rows

    def lane_state(self, S, b):
        """Fallback host state for lane b: acts + zero channels (the
        driver's acts-only pull convention; REC-grid _record only reads
        F[:na])."""
        acts = np.asarray(self.out["acts_snap"][b])       # (na_max, N, N)
        na, nc = S["na"], S["nc"]
        F = np.zeros((na + nc, self.N, self.N), acts.dtype)
        F[:na] = acts[:na]
        return F


class _LaneRef:
    __slots__ = ("point", "b")

    def __init__(self, point, b):
        self.point = point
        self.b = b


# ----------------------------------------------------------- installer
def install(async_apply=False, procs=None):
    if _STATE["orig"] is not None:
        return
    import jax
    jax.config.update("jax_enable_x64", True)     # f64 accumulators (E2c)
    import jax.numpy as jnp

    AA = None
    if async_apply:
        from . import asyncapply_proto as PA      # machinery only
        AA = PA
    orig = DRV.run_chunks
    _STATE["orig"] = orig
    st = _STATE["stats"]

    def run_chunks(worlds, steps_target, *, step_fn, pull_fn, record_fn,
                   rec_pool=None, **kw):
        G = worlds[0].get("_gpu")
        if G is None:                              # not a batched-GPU call
            return orig(worlds, steps_target, step_fn=step_fn,
                        pull_fn=pull_fn, record_fn=record_fn,
                        rec_pool=rec_pool, **kw)
        N = G["N"]
        na_max = G["struct"]["na_max"]
        dx = worlds[0]["dx"]
        kernel = _get_kernel(N, na_max, str(G["F"].dtype))
        B = G["F"].shape[0]
        thr = np.full((B, na_max), np.inf, np.float64)
        for b, S in enumerate(worlds):
            if b >= B:
                break
            thr[b, :S["na"]] = S["thr_a"]          # f64, host-exact
        thr_dev = jnp.asarray(thr)

        recorder = None
        if AA is not None:
            recorder = AA.AsyncRecorder(
                AA._ensure_pool(procs or min(8, os.cpu_count() or 1)),
                AA._STATE["stats"])

        def pull_fn2(full):
            if full:
                return pull_fn(True)               # stock host path
            t0 = time.perf_counter()
            out = kernel(G["F"][:, :na_max], thr_dev)   # pre-step buffer
            st["dispatch_s"] += time.perf_counter() - t0
            point = _DevPoint(out, na_max, N)
            return [_LaneRef(point, b) for b in range(len(worlds))]

        def host_record_fn(S, Fh, t_now):
            if recorder is not None:
                recorder.submit(S, Fh, t_now)
            else:
                record_fn(S, Fh, t_now)

        def dev_lane(S, ref, t_now):
            """Apply one dev lane (rows path) or fall back to host."""
            fl = ref.point.flags()
            b = ref.b
            sl = slice(b * na_max, b * na_max + S["na"])
            if not fl["finite"][sl].all():
                st["fb_nonfinite"] += 1
                return False
            if not fl["converged"][sl].all():
                st["fb_unconv"] += 1
                return False
            if fl["overflow"][sl].any():
                st["fb_overflow"] += 1
                return False
            rows = ref.point.rows()
            t0 = time.perf_counter()
            rows_bl, mass_vals = [], []
            for i in range(S["na"]):
                fi = b * na_max + i
                rows_bl.append(_assemble_blobs(rows, fi, N, dx))
                mass_vals.append(float(rows["mass"][fi]) * dx * dx)
            st["assemble_s"] += time.perf_counter() - t0
            t0 = time.perf_counter()
            ok = _apply_dev_record(S, rows_bl, mass_vals, t_now)
            if not ok:
                S["_t_stopped"] = t_now
            st["apply_s"] += time.perf_counter() - t0
            st["lanes_dev"] += 1
            return True

        class _Ready:
            __slots__ = ("point", "b", "S", "t")

            def __init__(self, point, b, S, t):
                self.point, self.b, self.S, self.t = point, b, S, t

            def result(self):
                # runs on the H-A drain thread: pull rows + assemble there
                rows = self.point.rows()
                S = self.S
                d = dict(t=self.t, rec=True, crec=False)
                blobs, mass, ntot = [], [], 0
                for i in range(S["na"]):
                    fi = self.b * self.point.na_max + i
                    bl = _assemble_blobs(rows, fi, self.point.N, S["dx"])
                    blobs.append(bl)
                    mass.append(float(rows["mass"][fi]) * S["dx"] ** 2)
                    ntot += len(bl)
                d["blobs"], d["mass"], d["ntot"] = blobs, mass, ntot
                return d

        class _Shim:
            """rec_pool: routes each record point. Dev lanes -> device
            rows (inline or via the H-A drain queue); fallback/host lanes
            -> stock fn(a). Rung-final barrier via recorder.point_done."""

            def map(self, fn, argss):
                argss = list(argss)
                if not argss:
                    return []
                t_now = argss[0][2]
                dev = isinstance(argss[0][1], _LaneRef)
                if not dev:
                    for a in argss:
                        fn(a)                      # stock/procrec path
                    if recorder is not None:
                        recorder.point_done(t_now, steps_target)
                    st["points_host"] += 1
                    return []
                # device point
                for (S, ref, t_) in argss:
                    if S["status"] != "ok" or S["recorded_at"] >= t_:
                        continue
                    fl = ref.point.flags()
                    b = ref.b
                    sl = slice(b * na_max, b * na_max + S["na"])
                    good = (fl["finite"][sl].all()
                            and fl["converged"][sl].all()
                            and not fl["overflow"][sl].any())
                    if not good:
                        st["lanes_fallback"] += 1
                        # count reason
                        if not fl["finite"][sl].all():
                            st["fb_nonfinite"] += 1
                        elif not fl["converged"][sl].all():
                            st["fb_unconv"] += 1
                        else:
                            st["fb_overflow"] += 1
                        Fh = ref.point.lane_state(S, b)
                        fn((S, Fh, t_))            # stock: pull-less state
                        continue
                    if recorder is not None:
                        with recorder.cv:
                            recorder.q.append((S, _Ready(ref.point, b, S,
                                                         t_), t_))
                            recorder.points[t_] = \
                                recorder.points.get(t_, 0) + 1
                            recorder._idle = False
                            recorder.cv.notify_all()
                        S["recorded_at"] = t_
                        st["lanes_dev"] += 1
                    else:
                        dev_lane(S, ref, t_)
                        S["recorded_at"] = t_
                if recorder is not None:
                    recorder.point_done(t_now, steps_target)
                st["points_dev"] += 1
                return []

        try:
            out = orig(worlds, steps_target, step_fn=step_fn,
                       pull_fn=pull_fn2, record_fn=host_record_fn,
                       rec_pool=_Shim(), **kw)
            if recorder is not None:
                recorder.barrier()
        finally:
            if recorder is not None:
                recorder.close()
        for S in worlds:
            if "_t_stopped" in S:
                S["t_step"] = S.pop("_t_stopped")
        return [S["status"] for S in worlds]

    DRV.run_chunks = run_chunks


def uninstall():
    if _STATE["orig"] is not None:
        DRV.run_chunks = _STATE["orig"]
        _STATE["orig"] = None


def stats():
    return dict(_STATE["stats"])


atexit.register(uninstall)


# ---------------------------------------------------------------- gates
def gate_batch(n=4, L=64.0, T=500.0, async_apply=False, verbose=True,
               tol=1e-12):
    """Stock vs devrec on a gpu-backend batch. Parity policy: ts/cts/
    status/t_step/patches/orgs/snaps identical; blobs same sets with
    area/peak EXACT and y/x <= tol; mass <= tol."""
    from .. import worlds as W
    from . import sim_gpu as SG

    def run(proto):
        names = (["m0", "pred"] * n)[:n]
        jobs = [(W.load(nm), 1 + i) for i, nm in enumerate(names)]
        master = SG.init_soup_gpu_batch(jobs, L=L, dtype="f32")
        if proto:
            install(async_apply=async_apply)
        try:
            SG.advance_gpu_batch(master, T)
        finally:
            if proto:
                uninstall()
        return master["worlds"]

    A = run(False)
    B = run(True)
    ok = True
    worst = 0.0
    for i, (Sa, Sb) in enumerate(zip(A, B)):
        lane_ok = (Sa["ts"] == Sb["ts"] and Sa["cts"] == Sb["cts"]
                   and Sa["status"] == Sb["status"]
                   and Sa["t_step"] == Sb["t_step"]
                   and Sa["patches"] == Sb["patches"]
                   and str(Sa["orgs"]) == str(Sb["orgs"])
                   and sorted(Sa["snaps"]) == sorted(Sb["snaps"]))
        why = [] if lane_ok else ["frame"]
        for a_i in Sa["blobs"]:
            for k, (bla, blb) in enumerate(zip(Sa["blobs"][a_i],
                                               Sb["blobs"][a_i])):
                if len(bla) != len(blb):
                    lane_ok = False
                    why.append(f"nblob@{a_i}/{k}:{len(bla)}vs{len(blb)}")
                    continue
                sa = sorted(bla); sb = sorted(blb)
                for ra, rb in zip(sa, sb):
                    if ra[2] != rb[2] or ra[3] != rb[3]:
                        lane_ok = False
                        why.append(f"area/peak@{a_i}/{k}")
                    for q in (0, 1):
                        err = abs(ra[q] - rb[q]) / max(abs(ra[q]), 1e-9)
                        worst = max(worst, err)
                        if err > tol:
                            lane_ok = False
                            why.append(f"pos@{a_i}/{k}:{err:.1e}")
        for a_i in Sa["mass"]:
            for ma, mb in zip(Sa["mass"][a_i], Sb["mass"][a_i]):
                err = abs(ma - mb) / max(abs(ma), 1e-9)
                worst = max(worst, err)
                if err > tol:
                    lane_ok = False
                    why.append(f"mass:{err:.1e}")
        ok &= lane_ok
        if verbose:
            print(f"[devrec gate lane{i}] {'PASS' if lane_ok else 'FAIL'} "
                  f"({len(Sa['ts'])} rec, {len(Sa['cts'])} crec)"
                  + ("" if lane_ok else f" why={why[:4]}"), flush=True)
    if verbose:
        print(f"[devrec gate] worst rel err {worst:.2e} (tol {tol}); "
              f"stats {stats()}", flush=True)
    return ok
