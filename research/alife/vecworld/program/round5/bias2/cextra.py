"""cextra -- two local follow-up readings of the `bias2` GPU outputs (numpy only; nothing here ran on the pod).

usage: python -B cextra.py FETCH_DIR OUT_JSON world=JOB_ID [world=JOB_ID ...]
FETCH_DIR holds `git archive origin/gpu-jobs jobs/<JOB_ID>/out/<world>/{latsub,windows}` unpacked.

1. global   What is the box-scale part of each latent? From latsub/*.npz (every 20th tick of the base run of the
            certification trajectories, both halves: 64 trajectories x 16 ticks x 64 blocks, float16). Per c = 1 Phi:
              pc1_share         share of the latent's variance on its first principal component over the 64 blocks
              box_mean_share    share of its variance carried by the box mean (1/64 for independent blocks)
              global scalar g   the box mean if box_mean_share > 0.1, else the PC1 score if pc1_share > 0.5, else none
              r2_g_from_box     cross-validated R^2 (ridge, folds = trajectories) of g from the box means of the block
                                hand designs: each alone, the level-0 fields jointly ("fields"), all jointly ("all")
              r2_g_from_box_sq  the same with the box means and box variances of the hand designs (2 numbers each)
            Latents of the two seeds and the two certification halves are separate Phi (different fits): numbers are
            means over the 4 replicas (2 for hand designs).
2. windows  Shape of the learned linear windows (windows/*.npz, W in standardised-field units, block-only encoders
            L0 and N0's linear part, c = 1). Per field the window is split into the flat block mean (DC), the two
            linear gradients (dipole), the three quadratic moments, and the rest; shares of the squared L2 norm. The
            `dipole_cos_with_first_field` = per replica, the signed cosine between a field's gradient direction and
            the first field's (+1: the same gradient; -1: the opposite, i.e. a gradient of the difference). The
            windows carry no weight decay, so directions the fields never excite (pixel-scale patterns) keep their
            initial noise: `smooth_share` = share of the window norm on spatial frequencies <= 2 cycles per block,
            and DC / dipole / quadratic shares are given relative to that smooth part. `replica_cos_smooth` = mean
            |cosine| between the smooth parts of the windows of different replicas (seed x fit half).
"""
import glob
import json
import os
import sys

import numpy as np

FETCH, OUTP = sys.argv[1], sys.argv[2]
JOBS = dict(a.split("=") for a in sys.argv[3:])
FIELDS = {"vortex": ("om", "Y", "a", "b"), "membrane": ("phi", "S", "K", "L"), "gliders": ("c0", "c1")}
r4 = lambda v: None if v is None else round(float(v), 4)   # noqa: E731


def cv_r2(X, y, groups, lam=1e-3, k=8):
    """Grouped k-fold ridge R^2 of y (n,) from X (n, d); features standardised on the training folds."""
    ug = np.unique(groups)
    fold = {g: i % k for i, g in enumerate(ug)}
    f = np.array([fold[g] for g in groups])
    res, tot = 0.0, 0.0
    for i in range(k):
        tr, te = f != i, f == i
        mu, sd = X[tr].mean(0), X[tr].std(0) + 1e-12
        A = np.c_[(X[tr] - mu) / sd, np.ones(tr.sum())]
        w = np.linalg.solve(A.T @ A + lam * tr.sum() * np.eye(A.shape[1]) * np.r_[np.ones(X.shape[1]), 0.0], A.T @ y[tr])
        p = np.c_[(X[te] - mu) / sd, np.ones(te.sum())] @ w
        res += ((y[te] - p) ** 2).sum()
        tot += ((y[te] - y[tr].mean()) ** 2).sum()
    return 1.0 - res / tot


def load_lat(d, stem):
    """{half: Zt (J, T', 64 c)} float64."""
    out = {}
    for h in ("A", "B"):
        p = os.path.join(d, f"{stem}__cert{h}.npz")
        if os.path.exists(p):
            out[h] = np.load(p)["Zt"].astype(np.float64)
    return out


def global_part(world, job):
    d = os.path.join(FETCH, "jobs", job, "out", world, "latsub")
    stems = sorted({os.path.basename(p).split("__cert")[0] for p in glob.glob(d + "/*.npz")})
    hand = [s for s in stems if s.startswith("hand_") and s.endswith("_h0")]
    H = {s[5:-3]: load_lat(d, s) for s in hand}
    res = {}
    for stem in stems:
        Z = load_lat(d, stem)
        rows = []
        for half, Zt in Z.items():
            if Zt.shape[-1] != 64:
                continue
            J, T, _ = Zt.shape
            X = Zt.reshape(J * T, 64)
            Xc = X - X.mean(0)
            ev, U = np.linalg.eigh(Xc.T @ Xc / len(Xc))
            pc1_share = float(ev[-1] / ev.sum())
            bm = X.mean(1)
            bm_share = float(bm.var() / X.var())
            if bm_share > 0.1:
                g, kind = bm, "box_mean"
            elif pc1_share > 0.5:
                g, kind = Xc @ U[:, -1], "pc1"
            else:
                g, kind = None, None
            row = {"pc1_share": pc1_share, "box_mean_share": bm_share, "kind": kind}
            if g is not None:
                groups = np.repeat(np.arange(J), T)
                B = {k: v[half].reshape(J * T, 64) for k, v in H.items() if half in v}
                m1 = {k: v.mean(1) for k, v in B.items()}
                m2 = {k: v.var(1) for k, v in B.items()}
                row["r2_g_from_box"] = {k: cv_r2(m1[k][:, None], g, groups) for k in B}
                fl = [k for k in FIELDS[world] if k in B]
                if len(fl) == len(FIELDS[world]):
                    row["r2_g_from_box"]["fields"] = cv_r2(np.stack([m1[k] for k in fl], 1), g, groups)
                row["r2_g_from_box"]["all"] = cv_r2(np.stack([m1[k] for k in B], 1), g, groups)
                row["r2_g_from_box_sq"] = {"all": cv_r2(np.stack([m1[k] for k in B] + [m2[k] for k in B], 1), g, groups)}
                row["r2_g_from_box_sq"].update({k: cv_r2(np.stack([m1[k], m2[k]], 1), g, groups) for k in B})
                # how slow is g: lag autocorrelation over 20 and 80 ticks (within trajectories)
                gt = g.reshape(J, T)
                gc = gt - gt.mean()
                row["g_autocorr"] = {str(20 * L): float((gc[:, L:] * gc[:, :-L]).mean() / gc.var()) for L in (1, 4)}
                row["g_within_traj_var_share"] = float(gt.var(1).mean() / gt.var())
            rows.append(row)
        if not rows:
            continue
        key = stem[:-3] if stem[-3:] in ("_s0", "_s1") else stem
        res.setdefault(key, []).extend(rows)
    out = {}
    for key, rows in res.items():
        e = {"n_replicas": len(rows), "pc1_share": r4(np.mean([r["pc1_share"] for r in rows])),
             "box_mean_share": r4(np.mean([r["box_mean_share"] for r in rows])),
             "kind": sorted({str(r["kind"]) for r in rows})}
        gr = [r for r in rows if r["kind"]]
        if gr:
            for fld in ("r2_g_from_box", "r2_g_from_box_sq"):
                keys = sorted(set.intersection(*[set(r[fld]) for r in gr]))
                e[fld] = {k: r4(np.mean([r[fld][k] for r in gr])) for k in keys}
                e[fld + "_min_over_replicas"] = {k: r4(np.min([r[fld][k] for r in gr])) for k in keys}
            e["g_autocorr"] = {k: r4(np.mean([r["g_autocorr"][k] for r in gr])) for k in gr[0]["g_autocorr"]}
            e["g_within_traj_var_share"] = r4(np.mean([r["g_within_traj_var_share"] for r in gr]))
            e["n_replicas_with_g"] = len(gr)
        out[key] = e
    return out


def lowpass(w, kmax=2):
    """Keep spatial frequencies with |kx|, |ky| <= kmax cycles per window."""
    F = np.fft.fft2(w)
    n = w.shape[0]
    k = np.abs(np.fft.fftfreq(n) * n)
    m = (k[:, None] <= kmax) & (k[None, :] <= kmax)
    return np.real(np.fft.ifft2(F * m))


def moments(w):
    """Shares of the squared norm of w on: DC, linear gradients, quadratic moments (orthonormalised in that order)."""
    n = w.shape[0]
    x = np.arange(n) - (n - 1) / 2
    X, Y = np.meshgrid(x, x)
    basis = [np.ones_like(X), X, Y, X * X, Y * Y, X * Y]
    Q = np.linalg.qr(np.stack([b.ravel() for b in basis], 1))[0]
    c = Q.T @ w.ravel()
    e = float((w ** 2).sum()) + 1e-300
    return {"dc": float(c[0] ** 2 / e), "dipole": float((c[1:3] ** 2).sum() / e), "quadratic": float((c[3:6] ** 2).sum() / e),
            "dipole_vec": c[1:3].tolist()}


def windows_part(world, job):
    d = os.path.join(FETCH, "jobs", job, "out", world, "windows")
    out = {}
    for cfg in sorted({os.path.basename(p).split("_s")[0] for p in glob.glob(d + "/*0_*_c1_s*__fit*.npz")}):
        Ws = []
        for p in sorted(glob.glob(f"{d}/{cfg}_s*__fit*.npz")):
            z = np.load(p, allow_pickle=False)
            if int(z["h"]) != 0 or int(z["c"]) != 1:
                continue
            Ws.append(np.asarray(z["W"], float)[0])                   # (fields, 16, 16), standardised units
        if not Ws:
            continue
        rows = []
        S = []
        for W in Ws:
            sm = np.stack([lowpass(W[f]) for f in range(W.shape[0])])
            S.append(sm)
            e_all, e_sm = (W ** 2).sum(), (sm ** 2).sum()
            row = {"smooth_share": float(e_sm / e_all), "fields": {}}
            mall = {"dc": 0.0, "dipole": 0.0, "quadratic": 0.0}
            for f, name in enumerate(FIELDS[world]):
                m = moments(sm[f])
                ef = float((sm[f] ** 2).sum() / e_sm)
                row["fields"][name] = dict(m, smooth_l2_share=ef, dc_sign=float(np.sign(sm[f].sum())))
                for k in mall:
                    mall[k] += ef * m[k]
            row["all_fields"] = mall
            # signed alignment of the fields' gradient (dipole) directions with the first field's
            d0 = np.asarray(row["fields"][FIELDS[world][0]]["dipole_vec"])
            row["dipole_cos_with_first_field"] = {
                name: float(np.asarray(row["fields"][name]["dipole_vec"]) @ d0
                            / (np.linalg.norm(row["fields"][name]["dipole_vec"]) * np.linalg.norm(d0) + 1e-300))
                for name in FIELDS[world][1:]}
            rows.append(row)
        cos = [abs(float(a.ravel() @ b.ravel() / (np.linalg.norm(a) * np.linalg.norm(b)))) for i, a in enumerate(S) for b in S[i + 1:]]
        e = {"n_replicas": len(Ws), "smooth_share": r4(np.mean([r["smooth_share"] for r in rows])),
             "replica_cos_smooth": r4(np.mean(cos)) if cos else None,
             "all_fields": {k: r4(np.mean([r["all_fields"][k] for r in rows])) for k in ("dc", "dipole", "quadratic")},
             "fields": {name: {k: r4(np.mean([r["fields"][name][k] for r in rows])) for k in ("smooth_l2_share", "dc", "dipole", "quadratic", "dc_sign")}
                        for name in FIELDS[world]}}
        e["all_fields"]["rest"] = r4(1 - sum(e["all_fields"].values()))
        e["dipole_cos_with_first_field"] = {name: [r4(r["dipole_cos_with_first_field"][name]) for r in rows] for name in FIELDS[world][1:]}
        out[cfg] = e
    return out


if __name__ == "__main__":
    res = {}
    for w, job in JOBS.items():
        res[w] = {"job": job, "source": f"{job}:out/{w}/latsub/*.npz and {job}:out/{w}/windows/*.npz (cextra.py)",
                  "global": global_part(w, job), "windows": windows_part(w, job)}
        print("==", w)
        for k, e in res[w]["global"].items():
            if k.endswith("_c2"):
                continue
            g = e.get("r2_g_from_box")
            top = sorted(g.items(), key=lambda kv: -kv[1])[:4] if g else None
            print(f"{k:16s} pc1 {e['pc1_share']:.3f} bm {e['box_mean_share']:.3f} {e['kind']} "
                  f"{top} sq_all {e.get('r2_g_from_box_sq', {}).get('all')} ac {e.get('g_autocorr')} wtv {e.get('g_within_traj_var_share')}")
        for k, e in res[w]["windows"].items():
            print(f"win {k:14s} smooth {e['smooth_share']} cos {e['replica_cos_smooth']} {e['all_fields']} "
                  + " ".join(f"{n}:{v['smooth_l2_share']}/dc{v['dc']}/dip{v['dipole']}" for n, v in e["fields"].items())
                  + f" dipcos {e['dipole_cos_with_first_field']}")
    json.dump(res, open(OUTP, "w"), indent=1)
