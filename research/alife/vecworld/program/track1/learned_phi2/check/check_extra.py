"""Checker extras (appends to check/check_numbers.json): GL_closG4_c1 against globally whitened LH_closG4_c1 and tent1
(paired, same items), span alignment of GL's 16-dim window span to the tent / LH / pool1 spans, and which grid latents
the local ridge alone loses on."""
import json, sys, glob, os
sys.path.insert(0, "/home/user/evalwork/vecworld/program/track1/learned_phi2")
sys.path.insert(0, "/home/user/evalwork/vecworld/program/track1/learned_phi2/check")
import numpy as np
import lphi as L
import run as R

OUT = "/home/user/evalwork/vecworld/program/track1/learned_phi2"
CD = f"{OUT}/results/cert"
G = L.FAM_G
K = json.load(open(f"{OUT}/check/check_numbers.json"))
Hh = L.load_halves()
X = {}


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
    return (V0 - np.min([err[n][idx].mean(0) for n in names], 0)) / (V0 - Vu)


def gw_fn(name):
    def fn(fh, Y):
        Zf = R.phi_apply(name, fh, Hh[fh]["Y"])[0].reshape(-1, 16)
        m = Zf.mean(0); Lc = np.linalg.cholesky(np.cov(Zf.T))
        Z = R.phi_apply(name, fh, Y)[0]
        return np.linalg.solve(Lc, (Z.reshape(-1, 16) - m).T).T.reshape(Z.shape)
    return fn


eg, og, jg = items("GL_closG4_c1")
rng = np.random.default_rng(7)
uj = np.unique(jg); pos = {u: np.flatnonzero(jg == u) for u in uj}
boots = [np.concatenate([pos[u] for u in rng.choice(uj, uj.size)]) for _ in range(1000)]
for nm in ("LH_closG4_c1", "tent1"):
    hv = {}
    for h in "AB":
        Y, Bb = Hh[h]["Y"], Hh[h]["B"]
        fn = gw_fn(nm)
        hv[h] = L.certify(fn(L.other(h), Y), fn(L.other(h), Bb))
    ew = {k: np.concatenate([hv["A"]["err"][k], hv["B"]["err"][k]]) for k in G}
    ow = np.concatenate([hv["A"]["orac"], hv["B"]["orac"]])
    jw = np.concatenate([hv["A"]["item_j"], hv["B"]["item_j"] + 18])
    assert np.array_equal(jw, jg)
    al = np.arange(len(jg))
    d0 = ceil(eg, og, al, G) - ceil(ew, ow, al, G)
    se = np.std([ceil(eg, og, b, G) - ceil(ew, ow, b, G) for b in boots], 0)
    X[f"GL_closG4_c1-{nm}_globally_whitened"] = [np.round(d0, 4).tolist(), np.round(se, 4).tolist()]

# span alignment in standardised level-1 coordinates (fit-half normaliser of GL)
al = {}
for h in "AB":
    phi = L.load_phi(f"{R.PHI_DIR}/GL_closG4_c1__fit{h}.npz")
    Wg = np.asarray(phi["enc"][0]["W"], float)                       # (192, 16), standardised channel coords
    sd = phi["sd"]

    def window_matrix(w44, chw):
        """16 overlapping windows (stride 2) of a 4x4 profile; chw = raw weight per channel -> standardised coords."""
        M = np.zeros((3, 8, 8, 16))
        k = 0
        for I in range(4):
            for J in range(4):
                for a, dy in enumerate((-1, 0, 1, 2)):
                    for b, dx in enumerate((-1, 0, 1, 2)):
                        for ch in range(3):
                            M[ch, (2 * I + dy) % 8, (2 * J + dx) % 8, k] += w44[a, b] * chw[ch] * sd[ch]
                k += 1
        return M.reshape(192, 16)
    tent = np.outer([.5, 1, 1, .5], [.5, 1, 1, .5]); box2 = np.zeros((4, 4)); box2[1:3, 1:3] = 1
    Pt = window_matrix(tent, [1, 1, 0]); Pp = window_matrix(box2, [1, 1, 0])
    lh = L.load_phi(f"{R.PHI_DIR}/LH_closG4_c1__fit{h}.npz")
    Wl = np.asarray(lh["enc"][0]["W"], float).reshape(3, 4, 4)       # standardised coords of LH's own normaliser
    M = np.zeros((3, 8, 8, 16)); k = 0
    for I in range(4):
        for J in range(4):
            for a, dy in enumerate((-1, 0, 1, 2)):
                for b, dx in enumerate((-1, 0, 1, 2)):
                    M[:, (2 * I + dy) % 8, (2 * J + dx) % 8, k] += Wl[:, a, b] / lh["sd"] * sd
            k += 1
    Pl = M.reshape(192, 16)
    al[f"fit{h}"] = {"GL_vs_tent1_span": L.span_alignment(Wg, Pt), "GL_vs_pool1_span": L.span_alignment(Wg, Pp),
                     "GL_vs_LH_span": L.span_alignment(Wg, Pl), "tent1_vs_pool1_span": L.span_alignment(Pt, Pp)}
X["span_alignment_GL"] = al

# which grid latents does the local ridge alone lose on (tau 8)?
neg = {}
for f in sorted(glob.glob(f"{CD}/*__certA.npz")):
    nm = os.path.basename(f)[:-11]
    e, o, j = items(nm)
    if "lridge" not in e:
        continue
    a_ = np.arange(len(j))
    d = ceil(e, o, a_, ["lridge"])[3] - ceil(e, o, a_, [n for n in G if n in e])[3]
    if d < 0:
        neg[nm] = round(float(d), 4)
X["local_ridge_alone_loses_tau8"] = neg
K["X_extra"] = X
K["cpu_seconds_total_extra"] = __import__("time").process_time()
json.dump(L.jsonable(K), open(f"{OUT}/check/check_numbers.json", "w"), indent=1)
print(json.dumps(L.jsonable(X), indent=0))
