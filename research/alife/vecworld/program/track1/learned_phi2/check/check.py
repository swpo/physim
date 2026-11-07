"""Independent checker for learned_phi2 (run on core 2). Writes check/check_numbers.json only; never
touches results/cert or results/phi.
  A  recompute ceilings and paired bootstrap differences from results/cert/*__cert[AB].npz (own code)
  B  pool3 channel correlations; LL/GL window inspection
  C  end-to-end: retrain LH_closG4_c1 on both halves (seed 0) and re-certify it and tent1; compare to saved
  D  span-level check: global 16 x 16 whitening (fit on the other half) of tent1, pool1, LH_closG4_c1, box4_1
  E  Prop. 6 split and I_capt(1) with the exactly conserved total-mass direction projected out
"""
import json, sys, time
sys.path.insert(0, "/home/user/evalwork/vecworld/program/track1/learned_phi2")
import numpy as np
import lphi as L
import run as R

OUT = "/home/user/evalwork/vecworld/program/track1/learned_phi2"
CD = f"{OUT}/results/cert"
G = L.FAM_G
res = {}
t00 = time.time()


def items(name):
    e, o, j = {}, [], []
    for h, off in (("A", 0), ("B", 18)):
        d = np.load(f"{CD}/{name}__cert{h}.npz")
        for k in d.files:
            if k.startswith("err_"):
                e.setdefault(k[4:], []).append(d[k].astype(np.float64))
        o.append(d["orac"]); j.append(d["item_j"] + off)
    return {k: np.concatenate(v) for k, v in e.items() if len(v) == 2}, np.concatenate(o), np.concatenate(j)


def ceil(err, orac, idx, names):
    V0 = err["mean"][idx].mean(0); Vu = orac[idx].mean(0)
    Vb = np.min([err[n][idx].mean(0) for n in names], 0)
    return (V0 - Vb) / (V0 - Vu)


rng = np.random.default_rng(2024)
BOOT = None


def boot_idx(ij):
    global BOOT
    if BOOT is None:
        uj = np.unique(ij); pos = {u: np.flatnonzero(ij == u) for u in uj}
        BOOT = [np.concatenate([pos[u] for u in rng.choice(uj, uj.size)]) for _ in range(1000)]
    return BOOT


def diff(a, b, fa=None, fb=None):
    ea, oa, ja = items(a); eb, ob, jb = items(b)
    assert np.array_equal(ja, jb)
    fa = fa or [n for n in G if n in ea]; fb = fb or [n for n in G if n in eb]
    al = np.arange(len(ja))
    d0 = ceil(ea, oa, al, fa) - ceil(eb, ob, al, fb)
    ds = [ceil(ea, oa, i, fa) - ceil(eb, ob, i, fb) for i in boot_idx(ja)]
    return np.round(d0, 4).tolist(), np.round(np.std(ds, 0), 4).tolist()


# ---- A
A = {"ceiling_G": {}, "diff": {}}
for nm in ["L1", "pool1", "pool3", "pool3w", "tent1", "box4_1", "LH_closG4_c1", "LH_recon_c1", "LH_closG4_c3", "LL_closG4_c1",
           "LL_recon_c1", "LL_closG4_c2", "LL_closG4_c3", "lpca1", "lpca2", "lpca3", "GL_closG4_c1", "LM_recon_c1", "LM_recon_c3"]:
    e, o, j = items(nm)
    A["ceiling_G"][nm] = np.round(ceil(e, o, np.arange(len(j)), [n for n in G if n in e]), 4).tolist()
pairs = [("LH_closG4_c1", "tent1"), ("tent1", "pool1"), ("LH_closG4_c1", "pool1"), ("tent1", "box4_1"), ("box4_1", "pool1"),
         ("LH_closG4_c3", "pool3"), ("GL_closG4_c1", "LH_closG4_c1"), ("pool3", "L1"), ("tent1", "L1"),
         ("LL_closG4_c1", "pool1"), ("LL_recon_c1", "pool1"), ("LL_closG4_c1", "LL_recon_c1"), ("LH_closG4_c1", "LH_recon_c1"),
         ("lpca1", "LL_closG4_c1"), ("lpca2", "LL_closG4_c2"), ("lpca3", "LL_closG4_c3"), ("LL_closG4_c3", "LL_recon_c3"),
         ("LM_closL4_c3", "LM_recon_c3")]
for a, b in pairs:
    A["diff"][f"{a}-{b}"] = diff(a, b)
# local ridge ALONE versus the global family, tau = 8 (GL >= G holds by construction, so GL - G cannot be negative)
import glob, os
lg = {}
for f in sorted(glob.glob(f"{CD}/*__certA.npz")):
    nm = os.path.basename(f)[:-11]
    e, o, j = items(nm)
    if "lridge" not in e:
        continue
    al = np.arange(len(j))
    cg = ceil(e, o, al, [n for n in G if n in e]); cl = ceil(e, o, al, ["lridge"]); cgl = ceil(e, o, al, [n for n in G if n in e] + ["lridge"])
    lg[nm] = {"cL_minus_cG": np.round(cl - cg, 4).tolist(), "cGL_minus_cG": np.round(cgl - cg, 4).tolist()}
H8 = L.HZ.index(8)
v8 = {k: v["cL_minus_cG"][H8] for k, v in lg.items()}
A["local_ridge_alone_vs_G_tau8"] = {"n": len(v8), "n_negative": int(sum(x < 0 for x in v8.values())),
                                    "min": min(v8.values()), "max": max(v8.values()), "median": float(np.median(list(v8.values()))),
                                    "L1": v8.get("L1"), "pool1": v8.get("pool1"), "pool3": v8.get("pool3"), "tent1": v8.get("tent1"),
                                    "LH_closG4_c1": v8.get("LH_closG4_c1"), "LL_closG4_c3": v8.get("LL_closG4_c3")}
A["GL_minus_G_tau8_min"] = min(v["cGL_minus_cG"][H8] for v in lg.values())
res["A_recompute"] = A
print("A done", time.time() - t00, flush=True)

# ---- B
Hh = L.load_halves()
B = {}
P3 = np.concatenate([L.pool(Hh[h]["Y"], 3) for h in "AB"]).reshape(-1, 3, 16).transpose(0, 2, 1).reshape(-1, 3)
C3 = np.corrcoef(P3.T)
B["pool3_channel_corr_pooled"] = {"c0_c1": C3[0, 1], "c0_m2": C3[0, 2], "c1_m2": C3[1, 2]}
P3c = np.concatenate([L.pool(Hh[h]["Y"], 3) for h in "AB"]).reshape(-1, 3, 16)
pc = [np.corrcoef(P3c[:, :, k].T) for k in range(16)]
B["pool3_channel_corr_per_cell_range"] = {k: [float(min(c[i, j] for c in pc)), float(max(c[i, j] for c in pc))]
                                          for k, (i, j) in {"c0_c1": (0, 1), "c0_m2": (0, 2), "c1_m2": (1, 2)}.items()}
for nm in ("LL_closG4_c1",):
    for h in "AB":
        phi = L.load_phi(f"{R.PHI_DIR}/{nm}__fit{h}.npz")
        W = np.asarray(phi["enc"][0]["W"], float).reshape(3, 2, 2)
        raw = W / phi["sd"][:, None, None]                    # weight per raw unit of each channel
        B[f"{nm}_fit{h}_raw_channel_weights_per_cell_pos"] = (raw / np.abs(raw[:2]).mean()).round(3).tolist()
        # share of the latent variance carried by m2 (raw contribution)
for h in "AB":
    phi = L.load_phi(f"{R.PHI_DIR}/GL_closG4_c1__fit{h}.npz")
    W = np.asarray(phi["enc"][0]["W"], float).reshape(3, 8, 8, 16)
    Pw = (W ** 2).sum(0)                                      # (8, 8, 16) spatial power per output
    neff = (Pw.sum((0, 1)) ** 2) / (Pw ** 2).sum((0, 1))
    share4 = []
    for k in range(16):
        p = Pw[..., k]
        best = 0
        for i in range(8):
            for j in range(8):
                s = np.roll(p, (-i + 1, -j + 1), (0, 1))[:4, :4].sum()
                best = max(best, s)
        share4.append(best / p.sum())
    B[f"GL_closG4_c1_fit{h}"] = {"eff_blocks_median": float(np.median(neff)), "eff_blocks_range": [float(neff.min()), float(neff.max())],
                                 "best_4x4_window_power_share_median": float(np.median(share4))}
res["B_inspect"] = B
print("B done", time.time() - t00, flush=True)

# ---- C  end-to-end for the headline learned Phi2
C = {}
phis = {}
for h in "AB":
    phi, info = L.train("LH", "closG", 1, 4, Hh[h]["Y"], seed=0, steps=5000)
    old = L.load_phi(f"{R.PHI_DIR}/LH_closG4_c1__fit{h}.npz")
    w_new, w_old = np.asarray(phi["enc"][0]["W"]).ravel(), np.asarray(old["enc"][0]["W"]).ravel()
    C[f"fit{h}"] = {"val_best": info["val_best"], "seconds": info["seconds"], "max_abs_w_diff": float(np.abs(w_new - w_old).max()),
                    "cos_w": float(w_new @ w_old / np.linalg.norm(w_new) / np.linalg.norm(w_old))}
    Wn = np.asarray(phi["enc"][0]["W"], float).reshape(3, 4, 4)
    C[f"fit{h}"]["inner_power_share"] = float((Wn[:, 1:3, 1:3] ** 2).sum() / (Wn ** 2).sum())
    phis[h] = phi


def cert_pair(fn, gshape, yr=True):
    halves = {}
    for h in "AB":
        Y, Bb = Hh[h]["Y"], Hh[h]["B"]
        Zt, ZB = fn(L.other(h), Y), fn(L.other(h), Bb)
        sd1 = Y.reshape(-1, 192).std(0)
        halves[h] = L.certify(Zt, ZB, gshape=gshape, Y1s=[Y[j] / sd1 for j in range(18)] if yr else None)
    return halves


def cmp_saved(halves, name):
    out = {}
    for h in "AB":
        d = np.load(f"{CD}/{name}__cert{h}.npz")
        out[h] = {nm: float(np.abs(halves[h]["err"][nm] - d[f"err_{nm}"]).max() / np.abs(d[f"err_{nm}"]).mean()) for nm in G}
    r = L.combine(halves["A"], halves["B"])
    return r, out


hv = cert_pair(lambda fh, Y: L.apply_phi(phis[fh], Y), (1, 4, 4))
r, dev = cmp_saved(hv, "LH_closG4_c1")
C["LH_closG4_c1_rerun_c_G"] = np.round(r["G"]["ceiling"], 4).tolist()
C["LH_closG4_c1_rerun_max_rel_err_dev_vs_saved"] = max(max(v.values()) for v in dev.values())
hv = cert_pair(lambda fh, Y: R.phi_apply("tent1", fh, Y)[0], (1, 4, 4))
r, dev = cmp_saved(hv, "tent1")
C["tent1_rerun_c_G"] = np.round(r["G"]["ceiling"], 4).tolist()
C["tent1_rerun_max_rel_err_dev_vs_saved"] = max(max(v.values()) for v in dev.values())
res["C_end_to_end"] = C
print("C done", time.time() - t00, flush=True)

# ---- D  global whitening of the 16-number latent (fit on the other half's base trajectories)
D = {}
item_err = {}


def gw(name):
    def fn(fh, Y):
        Zf = R.phi_apply(name, fh, Hh[fh]["Y"])[0].reshape(-1, 16)
        m = Zf.mean(0); w, U = np.linalg.eigh(np.cov(Zf.T))
        keep = w > 1e-9 * w.max()                      # box4_1 is rank deficient (its stride-2 Nyquist modes vanish)
        Wt = U[:, keep] / np.sqrt(w[keep])
        D.setdefault("rank", {})[name] = int(keep.sum())
        Z = R.phi_apply(name, fh, Y)[0]
        return ((Z.reshape(-1, 16) - m) @ Wt).reshape(Z.shape[:-1] + (int(keep.sum()),))
    return fn


for nm in ("tent1", "pool1", "LH_closG4_c1", "box4_1"):
    hv = cert_pair(gw(nm), None, yr=False)
    item_err[nm] = hv
    r = L.combine(hv["A"], hv["B"])
    D[nm] = {"c_G_globally_whitened": np.round(r["G"]["ceiling"], 4).tolist(), "se": np.round(r["G"]["se"], 4).tolist()}


def paired_items(ha, hb):
    ea = {k: np.concatenate([ha["A"]["err"][k], ha["B"]["err"][k]]) for k in G}
    eb = {k: np.concatenate([hb["A"]["err"][k], hb["B"]["err"][k]]) for k in G}
    oa = np.concatenate([ha["A"]["orac"], ha["B"]["orac"]]); ob = np.concatenate([hb["A"]["orac"], hb["B"]["orac"]])
    ij = np.concatenate([ha["A"]["item_j"], ha["B"]["item_j"] + 18])
    al = np.arange(len(ij))
    d0 = ceil(ea, oa, al, G) - ceil(eb, ob, al, G)
    ds = [ceil(ea, oa, i, G) - ceil(eb, ob, i, G) for i in boot_idx(ij)]
    return np.round(d0, 4).tolist(), np.round(np.std(ds, 0), 4).tolist()


D["diff_whitened"] = {"tent1-pool1": paired_items(item_err["tent1"], item_err["pool1"]),
                      "LH_closG4_c1-pool1": paired_items(item_err["LH_closG4_c1"], item_err["pool1"]),
                      "tent1-box4_1": paired_items(item_err["tent1"], item_err["box4_1"])}
res["D_global_whitening"] = D
print("D done", time.time() - t00, flush=True)

# ---- E  conserved-direction projection
E = {}


def proj(name, v):
    v = v / np.linalg.norm(v)
    Q = np.linalg.svd(np.eye(len(v)) - np.outer(v, v))[0][:, :len(v) - 1]   # orthonormal complement of v
    return lambda fh, Y: R.phi_apply(name, fh, Y)[0] @ Q


v16 = np.ones(16)
v48 = np.concatenate([np.ones(16), np.ones(16), np.zeros(16)])
for nm, v in (("tent1", v16), ("pool1", v16), ("pool3", v48), ("LH_closG4_c1", v16)):
    hv = cert_pair(proj(nm, v), None, yr=True)
    ld = {k: (0.5 * (np.asarray(hv["A"]["ld"][k], float) + np.asarray(hv["B"]["ld"][k], float))).round(3).tolist()
          for k in ("I_capt", "I_avail", "gapX", "gammaY", "inherit", "gapX_r2")}
    r = L.combine(hv["A"], hv["B"])
    E[nm] = {"logdet_projected": ld, "c_G_projected": np.round(r["G"]["ceiling"], 4).tolist()}
res["E_conserved_projected"] = E
res["cpu_seconds_total"] = time.process_time()
res["wall_seconds"] = time.time() - t00
json.dump(L.jsonable(res), open(f"{OUT}/check/check_numbers.json", "w"), indent=1)
print("all done", time.time() - t00, flush=True)
