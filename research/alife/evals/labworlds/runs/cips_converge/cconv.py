"""Continuum convergence of c40's CIPS cells through physim.labworld (time step, grid, behaviour, cost).

World: /home/user/physim/research/alife/collective/contrib/20261026T1100-c40-cips-layered-divide-claim/world.py
(native dt 0.1 at 192^2, dx 1, Lsc 3). The prepared state, device sites, frozen score scales and port gains
are the previous runner's (../cips_runner). physim is imported from the pinned copy in ./pkg (see pkg/HEAD).

Resolution (dt, N) at fixed physical box 192 world units: overrides dt, and for N != 192 Lsc = 3 N / 192
(the world's length scale: every diffusivity and drift coefficient is multiplied by Lsc^2 in pixel units, so
this is the same continuum model on a grid of spacing 192/N) and rf_len = 16 N / 192; LabWorld dx = 192/N.
Noise: proportional, sd 0.01 per sqrt(native t) on all four fields, correlation length ELL world units.

Subcommands (OMP_NUM_THREADS=1, labkit FFT workers 1, one process at a time):
  det       zero noise, no ensembles: sham and fuel pulse at DT... (one member each), readouts cached
  ens       ensembles named on the command line, e.g.  ens c002:dt0.05:N192:T  (roles T, A, B: natives at
            seeds 71000/81000/91000 + case index; X: same seed base 61000, for the refined resolution)
  score     REF X : band and null ratios for ensembles at REF (roles T, A, B) and the null X
"""
from __future__ import annotations

import os

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"

import argparse
import json
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "pkg"))
sys.path.insert(1, "/home/user/physim/packages/blobkit")
from physim import labworld as LW  # noqa: E402
from physim import blobround6_eval as scoring  # noqa: E402

sys.path.insert(0, "/home/user/swpo/residency-environments/scripts/physim/labworlds")
RUNNER = HERE.parent / "cips_runner"
sys.path.insert(1, str(RUNNER))
import cips as C  # noqa: E402  (read-only reuse: prepared, devices, one_worker, FIELDS, CLIPS, plabel)
import labeval as E  # noqa: E402

assert Path(LW.__file__).resolve().is_relative_to(HERE / "pkg"), LW.__file__
OUT = HERE / "out"
FIELDS, CLIPS = C.FIELDS, C.CLIPS
GAINS = {"e": 0.01, "p": 0.1, "F": 0.1, "s": 0.1}
SD = 0.01
ELL = 2.0          # noise correlation length, world units (2 px at the native grid)
L_BOX = 192
TIMES, SCORE_TIMES, SENSORS = E.TIMES, E.SCORE_TIMES, E.SENSORS
WINDOWS = (10, 25, 50)
PULSE = dict(t=5, kind="inject", device=0, port=2, amp=3.0, dur=10.0)
CASES = {"c001": [], "c002": [PULSE]}
SEEDS = {"T": 71000, "A": 81000, "B": 91000, "X": 61000, "Y": 62000}


def world(dt=0.1, N=L_BOX, sd=SD, ell=ELL, overrides=None):
    spt = int(round(0.1 / dt))
    assert abs(spt * dt - 0.1) < 1e-12, dt
    over = {}
    if dt != 0.1:
        over["dt"] = dt
    if N != L_BOX:
        over["Lsc"] = 3.0 * N / L_BOX
        over["rf_len"] = 16.0 * N / L_BOX
    over.update(overrides or {})
    kw = {}
    if ell and sd > 0:
        kw["noise_corr"] = {f: float(ell) for f in FIELDS}
    return LW.LabWorld(path=C.WORLD, fields=FIELDS, steps_per_tick=spt, native_dt=dt,
                       ports={f: LW.Port(gain=float(GAINS[f]), clip=CLIPS[f]) for f in FIELDS},
                       noise={f: ("proportional", float(sd)) for f in FIELDS}, overrides=over, dx=L_BOX / N,
                       sys_path=(C.LAB,), carry=("t",), **kw)


def regrid(a, N):
    """Periodic cubic-spline resampling of a native 192^2 field onto N^2 (pixel centres at (i+0.5) dx)."""
    from scipy import ndimage
    if a.shape[0] == N:
        return a.copy()
    out = ndimage.zoom(a, N / a.shape[0], order=3, mode="grid-wrap", grid_mode=True)
    assert out.shape == (N, N), out.shape
    return out


def prepared(N=L_BOX):
    st, info = C.prepared()
    if N == L_BOX:
        return st, info
    out = {f: regrid(st[f], N) for f in FIELDS}
    for f in FIELDS:
        lo, hi = CLIPS[f]
        out[f] = np.clip(out[f], lo, hi)
    out["t"] = st["t"]
    return out, info


def oracle(w, N):
    st, info = prepared(N)
    o = LW.oracle(w, st, C.devices(info))
    C.one_worker(o._stepper.module)
    return o


def queries():
    return [dict(sensor=s, t=list(TIMES)) for s in SENSORS]


def parse_name(name):
    """c002:dt0.05:N192:T[:sd0.01][:ell2][:m8]"""
    parts = name.split(":")
    d = dict(case=parts[0], dt=0.1, N=L_BOX, role=None, sd=SD, ell=ELL, m=8)
    for p in parts[1:]:
        if p.startswith("dt"):
            d["dt"] = float(p[2:])
        elif p.startswith("N"):
            d["N"] = int(p[1:])
        elif p.startswith("sd"):
            d["sd"] = float(p[2:])
        elif p.startswith("ell"):
            d["ell"] = float(p[3:])
        elif p.startswith("m"):
            d["m"] = int(p[1:])
        else:
            d["role"] = p
    return d


def ens_path(name):
    return OUT / "ens" / (name.replace(":", "_") + ".npz")


def ensemble(name):
    d = parse_name(name)
    ci = list(CASES).index(d["case"])
    w = world(d["dt"], d["N"], d["sd"], d["ell"])
    seed = SEEDS[d["role"]] + ci
    req = dict(id=d["case"], actions=CASES[d["case"]], queries=queries())
    meta = dict(request=req, members=d["m"], seed=seed, world=w.declaration(), labworld=str(LW.__file__),
                pkg_head=(HERE / "pkg" / "HEAD").read_text().strip())
    (OUT / "ens").mkdir(parents=True, exist_ok=True)
    o = None

    def compute():
        nonlocal o
        o = oracle(w, d["N"])
        return o.sample_truth(req["actions"], req["queries"], d["m"], truth_seed=seed)

    return E.cached(ens_path(name), compute, meta=meta)


LEGACY = {"T": "truth/{cid}.npz", "A": "controls/{cid}/independent_native.npz", "B": "controls/{cid}/band_native.npz",
          "X": "controls/{cid}/numerical_null.npz"}


def load(name):
    if name.split(":")[1] == "legacy":   # the previous runner's white-noise ensembles (c001/c002, dt 0.1; X at dt 0.05)
        cid, _, role = name.split(":")[:3]
        with np.load(RUNNER / "out" / "suite" / LEGACY[role].format(cid=cid), allow_pickle=False) as z:
            return [z[f"query{i}"] for i in range(3)], float(z["cpu_s"])
    with np.load(ens_path(name), allow_pickle=False) as z:
        return [z[f"query{i}"] for i in range(3)], float(z["cpu_s"])


# ----------------------------------------------------------------------------- deterministic ladder

def cmd_det(args):
    (OUT / "det").mkdir(parents=True, exist_ok=True)
    for dt in args.dts:
        for cid, actions in CASES.items():
            path = OUT / "det" / f"{cid}_dt{dt:g}_N{args.N}.npz"
            if path.exists():
                continue
            t0 = time.process_time()
            o = oracle(world(dt, args.N, sd=0.0, ell=0.0), args.N)
            r = o.sample_truth(actions, queries(), 1, truth_seed=5)["samples"]
            cpu = time.process_time() - t0
            np.savez_compressed(path, cpu_s=cpu, **{f"query{i}": a for i, a in enumerate(r)})
            print(f"det {cid} dt={dt:g} N={args.N}: {cpu:.1f} cpu-s", flush=True)


def offsets(a, b, spread):
    """RMS over slots of (a - b) per (sensor, field, time), over the RMS-over-slots member std.
    Global: mean and variance slots separately."""
    out = {}
    for qi, s in enumerate(SENSORS):
        for p, f in enumerate(FIELDS):
            slots = [(0, "mean"), (1, "var")] if s == "global" else [(None, "")]
            for k, lab in slots:
                sel = slice(None) if k is None else slice(k, k + 1)
                off = np.sqrt(((a[qi][0, :, p, sel] - b[qi][0, :, p, sel]) ** 2).mean(-1))
                spr = np.sqrt((spread[qi][:, :, p, sel].std(axis=0) ** 2).mean(-1))
                out[f"{s}/{f}" + (f"/{lab}" if lab else "")] = off / np.maximum(spr, 1e-300)
    return out


def cmd_dettable(args):
    res = {}
    for cid in CASES:
        spread, _ = load(f"{cid}:dt{args.spread_dt:g}:N{args.N}:{args.spread_role}")
        runs = {}
        for dt in args.dts:
            with np.load(OUT / "det" / f"{cid}_dt{dt:g}_N{args.N}.npz") as z:
                runs[dt] = [z[f"query{i}"] for i in range(3)]
        for d1, d2 in zip(args.dts[:-1], args.dts[1:]):
            o = offsets(runs[d1], runs[d2], spread)
            for W in WINDOWS:
                ti = [i for i, t in enumerate(TIMES) if 0 < t <= W]
                res.setdefault(cid, {}).setdefault(f"dt{d1:g}_vs_{d2:g}", {})[f"{W}tu"] = {
                    k: round(float(v[ti].max()), 3) for k, v in o.items()}
            res[cid][f"dt{d1:g}_vs_{d2:g}"]["by_time_device0"] = {
                k: np.round(v, 2).tolist() for k, v in o.items() if k.startswith("device0")}
        if len(args.dts) >= 3:
            ratios = {}
            o1 = offsets(runs[args.dts[0]], runs[args.dts[1]], spread)
            o2 = offsets(runs[args.dts[1]], runs[args.dts[2]], spread)
            for k in o1:
                m = o2[k] > 0.02
                ratios[k] = round(float(np.median(o1[k][m] / o2[k][m])), 2) if m.any() else None
            res[cid]["order_ratio_median"] = ratios
    (OUT / f"dettable_N{args.N}.json").write_text(json.dumps(res, indent=1))
    for cid, per in res.items():
        print(cid)
        for pair, w in per.items():
            if pair in ("order_ratio_median",):
                print("  order ratio", w)
                continue
            for W in WINDOWS:
                v = w[f"{W}tu"]
                print(f"  {pair} {W}tu max offset/spread: " + " ".join(f"{k}={x:.2f}" for k, x in v.items()))


def cmd_spacetable(args):
    """Zero-noise grid ladder at one dt: offsets N[i] vs N[i+1] over the member spread of {spread_role} at (dt, 192)."""
    res = {}
    dt = args.dts[0]
    for cid in CASES:
        spread, _ = load(f"{cid}:dt{dt:g}:N{L_BOX}:{args.spread_role}")
        runs = {}
        for N in args.Ns:
            with np.load(OUT / "det" / f"{cid}_dt{dt:g}_N{N}.npz") as z:
                runs[N] = [z[f"query{i}"] for i in range(3)]
        for n1, n2 in zip(args.Ns[:-1], args.Ns[1:]):
            o = offsets(runs[n1], runs[n2], spread)
            for W in WINDOWS:
                ti = [i for i, t in enumerate(TIMES) if 0 < t <= W]
                res.setdefault(cid, {}).setdefault(f"N{n1}_vs_{n2}", {})[f"{W}tu"] = {k: round(float(v[ti].max()), 3) for k, v in o.items()}
            res[cid][f"N{n1}_vs_{n2}"]["by_time"] = {k: np.round(v, 2).tolist() for k, v in o.items()}
        if len(args.Ns) >= 3:
            o1 = offsets(runs[args.Ns[0]], runs[args.Ns[1]], spread); o2 = offsets(runs[args.Ns[1]], runs[args.Ns[2]], spread)
            res[cid]["ratio_offset1_over_offset2_median"] = {k: (round(float(np.median(o1[k][1:] / np.maximum(o2[k][1:], 1e-300))), 2)) for k in o1}
    (OUT / f"spacetable_dt{dt:g}.json").write_text(json.dumps(res, indent=1))
    for cid, per in res.items():
        print(cid)
        for pair, w in per.items():
            if not pair.startswith("N"):
                print("  ratio", w)
                continue
            for W in WINDOWS:
                print(f"  {pair} {W}tu max offset/spread: " + " ".join(f"{k}={x:.2f}" for k, x in w[f"{W}tu"].items()))


# ----------------------------------------------------------------------------- scoring

def scales():
    suite = json.loads((RUNNER / "out" / "suite" / "suite.json").read_text())
    return suite["calibration"]["scales"]


def group_features(arrays, W, sc):
    """{group id: (members, d)} of scaled coordinates for the window [.., W] (as cips.window_groups)."""
    ti = [TIMES.index(t) for t in SCORE_TIMES if t <= W]
    out = {}
    for qi, s in enumerate(SENSORS):
        for p, f in enumerate(FIELDS):
            a = arrays[qi]
            if s == "global":
                X = np.concatenate([a[:, ti, p, k] / sc[f"{s}/{f}/{lab}"]["scale"] for k, lab in ((0, "mean"), (1, "variance"))], 1)
            else:
                X = a[:, ti, p, :].reshape(len(a), -1) / sc[f"{s}/{f}"]["scale"]
            out[f"{s}/{f}"] = X
    return out


def pairwise(X):
    d = X.shape[1]
    return np.sqrt(((X[:, None, :] - X[None, :, :]) ** 2).sum(-1) / d)


def es(D, P, T):
    """Energy score of predictor members P against truth members T from the joint distance matrix."""
    return D[np.ix_(P, T)].mean() - 0.5 * D[np.ix_(P, P)].mean()


def summarize(Ds, P, T):
    g = {k: es(D, P, T) for k, D in Ds.items()}
    r = {"aggregate": float(np.mean(list(g.values())))}
    for s in SENSORS:
        r[s] = float(np.mean([v for k, v in g.items() if k.startswith(s + "/")]))
    return r, g


def cmd_score(args):
    """REF = 'dt0.05:N192' (roles T, A, B there); NULL = 'dt0.025:N192:A' etc. (any role)."""
    sc = scales()
    res = {}
    rng = np.random.default_rng(args.perm_seed)
    for cid in args.cases:
        T, _ = load(f"{cid}:{args.ref}:T")
        A, _ = load(f"{cid}:{args.ref}:A")
        B, _ = load(f"{cid}:{args.ref}:B")
        X, _ = load(f"{cid}:{args.null}")
        # sanity: the score_case path equals ours for (A vs T)
        n = len(T[0])
        pool = [np.concatenate([T[q], A[q], B[q], X[q]]) for q in range(3)]
        iT, iA, iB, iX = (np.arange(n), np.arange(n, 2 * n), np.arange(2 * n, 3 * n), np.arange(3 * n, 4 * n))
        perms = [rng.permutation(3 * n) for _ in range(args.perms)]
        for W in WINDOWS:
            F = group_features(pool, W, sc)
            Ds = {k: pairwise(v) for k, v in F.items()}
            keys = ["aggregate"] + list(SENSORS)
            sA, gA = summarize(Ds, iA, iT)
            # our energy score equals PhySim's score_case on the same groups (checked for A against T)
            from types import SimpleNamespace
            sp = SimpleNamespace(world=world(), devices=C.devices(C.prepared()[1]))
            r = scoring.score_case(dict(id=cid, actions=CASES[cid], queries=queries()), {"samples": A}, {"samples": T},
                                   groups=C.window_groups(sp, sc, W), n_samples=n, n_truth=n, roster=E.roster(sp))
            assert abs(r["joint_energy_equal_group_mean"] - sA["aggregate"]) <= 1e-9 * abs(sA["aggregate"]), (r, sA)
            sB, gB = summarize(Ds, iB, iT)
            sX, gX = summarize(Ds, iX, iT)
            fixed = {k: dict(null=sX[k] / sA[k], null_vs_B=sX[k] / sB[k], band_two_ensembles=sB[k] / sA[k]) for k in keys}
            band, null = {k: [] for k in keys}, {k: [] for k in keys}
            for p in perms:
                t_, a_, b_ = p[:n], p[n:2 * n], p[2 * n:]
                s_a = summarize(Ds, a_, t_)[0]
                s_b = summarize(Ds, b_, t_)[0]
                s_x = summarize(Ds, iX, t_)[0]
                for k in keys:
                    band[k].append(s_b[k] / s_a[k])
                    null[k].append(s_x[k] / s_a[k])
            row = {}
            for k in keys:
                bq = np.quantile(band[k], [0.05, 0.5, 0.95])
                nq = np.quantile(null[k], [0.05, 0.5, 0.95])
                row[k] = dict(band_q05_q50_q95=np.round(bq, 3).tolist(), null_q05_q50_q95=np.round(nq, 3).tolist(),
                              pass_median_in_band=bool(bq[0] <= nq[1] <= bq[2]),
                              frac_perm_null_above_band_q95=round(float(np.mean(np.asarray(null[k]) > bq[2])), 3),
                              fixed={kk: round(float(v), 3) for kk, v in fixed[k].items()},
                              native_score=round(float(sA[k]), 5))
            row["groups_null_over_A"] = {g: round(float(gX[g] / gA[g]), 3) for g in gA}
            row["groups_B_over_A"] = {g: round(float(gB[g] / gA[g]), 3) for g in gA}
            res.setdefault(cid, {})[f"{W}tu"] = row
    tag = f"score_{args.ref}__{args.null}".replace(":", "_") + ("" if list(args.cases) == list(CASES) else "_" + "_".join(args.cases))
    (OUT / f"{tag}.json").write_text(json.dumps(dict(ref=args.ref, null=args.null, perms=args.perms, scores=res), indent=1))
    print(f"ref {args.ref}  null {args.null}  ({args.perms} partitions of the 24 natives into T, A, B)")
    print("| case | window | sensor | band q05-q95 (median) | null median [q05-q95] | fixed null/A | fixed B/A | pass |")
    print("|---|---|---|---|---|---|---|---|")
    for cid, per in res.items():
        for W, row in per.items():
            for k in ["aggregate"] + list(SENSORS):
                r = row[k]
                b, x = r["band_q05_q50_q95"], r["null_q05_q50_q95"]
                print(f"| {cid} | {W} | {k} | {b[0]:.2f}-{b[2]:.2f} ({b[1]:.2f}) | {x[1]:.2f} [{x[0]:.2f}-{x[2]:.2f}] | "
                      f"{r['fixed']['null']:.2f} | {r['fixed']['band_two_ensembles']:.2f} | {'yes' if r['pass_median_in_band'] else 'NO'} |")


def cmd_ens(args):
    for name in args.names:
        t0 = time.process_time()
        ensemble(name)
        print(f"{name}: {time.process_time() - t0:.1f} cpu-s", flush=True)


def cmd_stats(args):
    """Ranges and body counts of one ensemble's members are not stored; this prints readout spread summaries."""
    for name in args.names:
        a, cpu = load(name)
        print(name, f"cpu {cpu:.0f}s", "global mean e/F/s at 50 tu, members:",
              np.round(a[2][:, -1, 0, 0], 4).tolist(), np.round(a[2][:, -1, 2, 0], 4).tolist(),
              "max e at device0 nodes over time:", round(float(a[0][:, :, 0, :].max()), 4))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["det", "dettable", "spacetable", "ens", "score", "stats"])
    ap.add_argument("names", nargs="*")
    ap.add_argument("--dts", type=float, nargs="*", default=[0.1, 0.05, 0.025])
    ap.add_argument("--N", type=int, default=L_BOX)
    ap.add_argument("--Ns", type=int, nargs="*", default=[192, 288, 384])
    ap.add_argument("--spread-dt", type=float, default=0.1)
    ap.add_argument("--spread-role", default="T")
    ap.add_argument("--ref", default="dt0.1:N192")
    ap.add_argument("--null", default="dt0.05:N192:X")
    ap.add_argument("--perms", type=int, default=300)
    ap.add_argument("--cases", nargs="*", default=list(CASES))
    ap.add_argument("--perm-seed", type=int, default=2029)
    a = ap.parse_args()
    dict(det=cmd_det, dettable=cmd_dettable, spacetable=cmd_spacetable, ens=cmd_ens, score=cmd_score, stats=cmd_stats)[a.cmd](a)
