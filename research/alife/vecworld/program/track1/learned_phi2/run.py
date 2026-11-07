"""E1 on real nonlinear data: learned level-2 coarse-grainings of the gliders block view.

usage: python -B run.py fit       fit every Phi2 on each half (results/phi/<name>__fit<H>.npz, results/train_info.json)
       python -B run.py cert [--rmlp NAME,NAME,...]
                                  certify every Phi2 on the other half; pool halves (results/cert/<name>.json)
       python -B run.py all       fit then cert

Phi2 catalogue (c = latent channels per 2 x 2 cell, q = 16 c numbers):
  fixed      L1 (level 1 itself, the stack reference), pool1/2/3 (2 x 2 block means: total mass;
             c0, c1; c0, c1, m2), pmom3 (total mass and its two first spatial moments per cell)
  closed     lpca{c} (local PCA = optimal local linear AE), gpca{q} (global PCA), ltica{lag}_{c}
             (local symmetrised TICA), rand_s{c}_{k} / rand_p1_{k} (random signed / positive windows)
  learned    {LL,LM,GM,GL}_{recon | closG<tau> | closL<tau> | closLlin<tau> | pib<tau>}_c{c}
             LL local linear, LM local MLP (12-64-64-c), GM unconstrained linear + MLP residual,
             GL unconstrained linear; recon = autoencoder; closG = whitened latent predicts its own
             future at tau from 2 lags with a GLOBAL linear head; closL / closLlin = same with a LOCAL
             (3 x 3 neighbourhood, shared weights) MLP / linear head; pib = predictive information
             bottleneck (whitened latent + N(0, 0.5^2) channel noise predicts the level-1 future).
"""
import json
import os
import sys
import time

sys.path.insert(0, "/home/user/evalwork/vecworld/program/track1/learned_phi2")
import numpy as np  # noqa: E402

import lphi as L  # noqa: E402

PHI_DIR = f"{L.RES}/phi"
CERT_DIR = f"{L.RES}/cert"
os.makedirs(PHI_DIR, exist_ok=True)
os.makedirs(CERT_DIR, exist_ok=True)


def learned_list():
    out = []
    for c in (1, 2, 3):
        for kind in ("LL", "LM"):
            out += [(kind, "recon", c, 0), (kind, "closG", c, 4), (kind, "closL", c, 4)]
        for kind in ("GM", "GL"):
            out += [(kind, "recon", c, 0), (kind, "closG", c, 4)]
    for c in (1, 3):
        out += [("LL", "closG", c, 1), ("LL", "closG", c, 16)]
    out += [("LL", "closLlin", 3, 4), ("LM", "closLlin", 3, 4), ("LL", "pib", 3, 4), ("LM", "pib", 3, 4),
            ("GM", "pib", 3, 4), ("GL", "pib", 3, 4)]
    return out


def lname(kind, obj, c, tau):
    return f"{kind}_{obj}{tau if obj != 'recon' else ''}_c{c}"


STEPS = {"LL": 5000, "LM": 2000, "GM": 2000, "GL": 2000, "LH": 5000}
EXTRA_LEARNED = [("LH", "closG", 1, 4), ("LH", "closG", 1, 16), ("LH", "recon", 1, 0), ("LH", "closG", 3, 4), ("LH", "recon", 3, 0)]
EXTRA_FIXED = ["pool3w", "pool2w", "tent1", "box4_1", "tent3"]
TENT = np.outer([0.5, 1, 1, 0.5], [0.5, 1, 1, 0.5])
RMLP_SUBSET = ["L1", "pool1", "pool3", "LL_closG4_c1", "LL_closG4_c3", "LM_closL4_c3", "LM_recon_c1", "LM_recon_c3",
               "GL_closG4_c1", "LH_closG4_c1", "LH_closG4_c3", "tent1"]
CLOSED = ([f"lpca{c}" for c in (1, 2, 3)] + [f"gpca{16 * c}" for c in (1, 2, 3)] +
          [f"ltica{lag}_{c}" for lag in (1, 4, 16) for c in (1, 2, 3)] +
          [f"rand_s{c}_{k}" for c in (1, 3) for k in (0, 1)] + [f"rand_p1_{k}" for k in (0, 1)])
FIXED = ["L1", "pool1", "pool2", "pool3", "pmom3"]


def fit(H, learned=None):
    info_path = f"{L.RES}/train_info.json"
    infos = json.load(open(info_path)) if os.path.exists(info_path) else {}
    t_all = time.time()
    for h in ("A", "B"):
        Ytr = H[h]["Y"]
        mu, sd = L.chan_norm(Ytr)
        if learned is not None:                    # extra stage: only the given learned configs
            todo = learned
        else:
            todo = learned_list()
        for c in ((1, 2, 3) if learned is None else ()):
            U, ev = L.local_pca(Ytr, mu, sd, c)
            L.save_phi(L.linear_phi(U, mu, sd), f"{PHI_DIR}/lpca{c}__fit{h}.npz")
            m, s, V = L.global_pca(Ytr, 16 * c)
            np.savez_compressed(f"{PHI_DIR}/gpca{16 * c}__fit{h}.npz", m=m, s=s, V=V)
            for lag in (1, 4, 16):
                W, lam = L.local_tica(Ytr, mu, sd, c, lag)
                L.save_phi(L.linear_phi(W, mu, sd), f"{PHI_DIR}/ltica{lag}_{c}__fit{h}.npz")
                infos[f"ltica{lag}_{c}__fit{h}"] = {"eigenvalues": lam.tolist()}
            infos[f"lpca{c}__fit{h}"] = {"eigenvalues": ev.tolist()}
        rng = np.random.default_rng(12345)          # the same random windows for both halves
        for c in ((1, 3) if learned is None else ()):
            for k in (0, 1):
                L.save_phi(L.linear_phi(rng.standard_normal((12, c)), mu, sd), f"{PHI_DIR}/rand_s{c}_{k}__fit{h}.npz")
        for k in ((0, 1) if learned is None else ()):
            L.save_phi(L.linear_phi(np.abs(rng.standard_normal((12, 1))), mu, sd), f"{PHI_DIR}/rand_p1_{k}__fit{h}.npz")
        # learned
        for kind, obj, c, tau in todo:
            nm = lname(kind, obj, c, tau)
            key = f"{nm}__fit{h}"
            if os.path.exists(f"{PHI_DIR}/{key}.npz") and key in infos:
                continue
            phi, info = L.train(kind, obj, c, tau, Ytr, seed=0, steps=STEPS[kind])
            L.save_phi(phi, f"{PHI_DIR}/{key}.npz")
            infos[key] = info
            json.dump(L.jsonable(infos), open(info_path, "w"), indent=1)
            L.log(f"fit {key}: {info['seconds']:.1f} s, val {info['val_init']:.4f} -> {info['val_best']:.4f}, "
                  f"min rel eig {info['min_rel_eig_latent_cov']:.2e}")
    json.dump(L.jsonable(infos), open(info_path, "w"), indent=1)
    L.log(f"fit done in {time.time() - t_all:.0f} s")


def all_names():
    return FIXED + CLOSED + [lname(*a) for a in learned_list()]


def phi_apply(name, fit_half, Y):
    """Apply Phi2 `name` (fitted on fit_half) to level-1 frames Y (..., 192); returns (z, grid_shape)."""
    if name == "L1":
        return Y, (3, 8, 8)
    if name in ("pool3w", "pool2w"):          # pooling followed by per-cell channel whitening (fit half)
        c = int(name[4])
        Yf = H_GLOBAL[fit_half]["Y"]
        Zf = L.pool(Yf, c).reshape(-1, c, 16).transpose(0, 2, 1).reshape(-1, c)
        m = Zf.mean(0)
        Lc = np.linalg.cholesky(np.cov(Zf.T))
        Z = L.pool(Y, c).reshape(Y.shape[:-1] + (c, 16))
        Zw = np.einsum("ij,...jk->...ik", np.linalg.inv(Lc), Z - m[:, None])
        return Zw.reshape(Y.shape[:-1] + (16 * c,)), (c, 4, 4)
    if name in ("tent1", "box4_1", "tent3"):   # designed overlapping windows (4 x 4 blocks, stride 2), raw units
        X = L.halo_patches(L.grid(Y)).reshape(Y.shape[:-1] + (4, 4, 3, 4, 4))
        w = np.ones((4, 4)) if name == "box4_1" else TENT
        w = w / w.sum()
        Z = np.einsum("...cyx,yx->...c", X, w)                                   # (..., 4, 4, 3)
        Z = Z[..., :1] + Z[..., 1:2] if name != "tent3" else Z
        return L.flat_latent(Z), (Z.shape[-1], 4, 4)
    if name.startswith("pool"):
        c = int(name[4:])
        return L.pool(Y, c), (c, 4, 4)
    if name == "pmom3":
        return L.pool_mom(Y), (3, 4, 4)
    if name.startswith("gpca"):
        d = np.load(f"{PHI_DIR}/{name}__fit{fit_half}.npz")
        return ((Y - d["m"]) / d["s"]) @ d["V"], None
    phi = L.load_phi(f"{PHI_DIR}/{name}__fit{fit_half}.npz")
    loc = phi["kind"] in ("LL", "LM", "LH")
    return L.apply_phi(phi, Y), ((phi["c"], 4, 4) if loc else None)


def linear_W(name, fit_half):
    """The 12 x c window of a local linear Phi2 (None otherwise)."""
    if name in FIXED or name in EXTRA_FIXED or name.startswith(("pool", "gpca")):
        return None
    phi = L.load_phi(f"{PHI_DIR}/{name}__fit{fit_half}.npz")
    if phi["kind"] == "LH":
        return "LH", np.asarray(phi["enc"][0]["W"], np.float64)
    if phi["kind"] != "LL":
        return None
    return np.asarray(phi["enc"][0]["W"], np.float64), phi["sd"]


def cert_one(name, H, rmlp=False):
    halves = {}
    extra = {}
    for h in ("A", "B"):
        fh = L.other(h)
        Y, B = H[h]["Y"], H[h]["B"]
        Zt, gs = phi_apply(name, fh, Y)
        ZB, _ = phi_apply(name, fh, B)
        sd1 = Y.reshape(-1, 192).std(0)
        Y1s = None if name == "L1" else [Y[j] / sd1 for j in range(L.NJ)]
        t0 = time.time()
        halves[h] = L.certify(Zt, ZB, gshape=gs, Y1s=Y1s, rmlp=rmlp)
        nt = L.nontriviality(Zt, Y, L.pool(Y, 3))
        nt["cert_seconds"] = time.time() - t0
        lw = linear_W(name, fh)
        if lw is not None and isinstance(lw[0], str):         # window profile of the halo encoder: inner 2 x 2 versus halo ring
            W = lw[1].reshape(3, 4, 4, -1)
            inner = (W[:, 1:3, 1:3] ** 2).sum()
            nt["halo_window"] = {"inner_power_share": float(inner / (W ** 2).sum()),
                                 "per_channel_profile_c1": W[..., 0].tolist() if W.shape[-1] == 1 else None}
        elif lw is not None:
            W, sd = lw
            Ps = L.pool_subspaces(sd)
            al = {k: L.span_alignment(W, P) for k, P in Ps.items() if P.shape[1] >= W.shape[1]}
            U, _ = L.local_pca(H[fh]["Y"], *L.chan_norm(H[fh]["Y"]), W.shape[1])
            al["lpca_same_c"] = L.span_alignment(W, U)
            nt["alignment"] = al
        extra[h] = nt
        np.savez_compressed(f"{CERT_DIR}/{name}__cert{h}.npz", orac=halves[h]["orac"], item_j=halves[h]["item_j"],
                            **{f"err_{k}": v.astype(np.float32) for k, v in halves[h]["err"].items()})
    res = L.combine(halves["A"], halves["B"])
    res["name"] = name
    res["per_half"] = extra
    res["tau_half_G"] = L.tau_half(res["G"]["ceiling"])
    if "GL" in res:
        res["tau_half_GL"] = L.tau_half(res["GL"]["ceiling"])
    res["ld_per_half"] = {h: halves[h]["ld"] for h in ("A", "B")}
    json.dump(L.jsonable(res), open(f"{CERT_DIR}/{name}{'_rmlp' if rmlp else ''}.json", "w"), indent=1)
    return res


def cert(H, rmlp_names=()):
    t_all = time.time()
    for name in all_names():
        if os.path.exists(f"{CERT_DIR}/{name}.json"):
            continue
        t0 = time.time()
        r = cert_one(name, H)
        cg = np.round(r["G"]["ceiling"], 3).tolist()
        cl = np.round(r["GL"]["ceiling"], 3).tolist() if "GL" in r else None
        L.log(f"cert {name}: c_G {cg}  c_GL {cl}  I_capt(1) {r['logdet']['I_capt'][0]:.1f} nats  ({time.time() - t0:.0f} s)")
    for name in rmlp_names:
        if os.path.exists(f"{CERT_DIR}/{name}_rmlp.json"):
            continue
        t0 = time.time()
        r = cert_one(name, H, rmlp=True)
        L.log(f"cert+rmlp {name}: c_G+rmlp {np.round(r['G+rmlp']['ceiling'], 3).tolist()} ({time.time() - t0:.0f} s)")
    L.log(f"cert done in {time.time() - t_all:.0f} s")


H_GLOBAL = None

if __name__ == "__main__":
    stage = sys.argv[1]
    H = L.load_halves()
    H_GLOBAL = H
    rm = []
    if "--rmlp" in sys.argv:
        rm = sys.argv[sys.argv.index("--rmlp") + 1].split(",")
    if stage in ("fit", "all"):
        fit(H)
    if stage in ("cert", "all"):
        cert(H, rm)
    if stage == "extra":                           # halo encoders, whitened pooling, rmlp subset
        fit(H, learned=EXTRA_LEARNED)
        for nm in EXTRA_FIXED + [lname(*a) for a in EXTRA_LEARNED]:
            if not os.path.exists(f"{CERT_DIR}/{nm}.json"):
                r = cert_one(nm, H)
                L.log(f"cert {nm}: c_G {np.round(r['G']['ceiling'], 3).tolist()}  c_GL {np.round(r['GL']['ceiling'], 3).tolist()}")
        cert(H, RMLP_SUBSET)
    import resource
    ru = resource.getrusage(resource.RUSAGE_SELF)
    L.log(f"process CPU seconds: user {ru.ru_utime:.0f} sys {ru.ru_stime:.0f}; max RSS {ru.ru_maxrss / 1024:.0f} MB")
