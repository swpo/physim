"""h9_dev.py — prototype: regional composition segregation (h9) from recs.
h9 = corrected uncertainty coefficient I(patch;species)/H(species) x persistence.
Reuses d7b's track features + clustering verbatim (copied path) so "species"
means exactly what r9 means. Validation: synthetic controls per rec.
Usage: bk3 python h9_dev.py <rec.npz> [P]
"""
import json, sys, os
import numpy as np
sys.path.insert(0, "/Users/spoho/v3work/v3bundle/lib")
sys.path.insert(0, "/Users/spoho/v3work/v3bundle")
import metrics_v3 as MV3
import metrics_v2 as MV2
from scipy.cluster.vq import kmeans2

BURN = MV3.BURN if hasattr(MV3, "BURN") else 250.0
LATE_W_MIN = getattr(MV3, "LATE_W_MIN", 500.0)
D7B_MIN_TRACK = getattr(MV3, "D7B_MIN_TRACK", 6)
D7B_MIN_ROWS = getattr(MV3, "D7B_MIN_ROWS", 8)
D7B_KMAX = getattr(MV3, "D7B_KMAX", 4)
D7B_SIL_FLOOR = getattr(MV3, "D7B_SIL_FLOOR", 0.35)
MOVE_THR = getattr(MV3, "MOVE_THR", 0.05)


def track_table(rec, v2_out):
    """(labels, frames) via d7b's exact feature path. frames: list per track of
    (yx array in late window, t values). Returns None if <2 species."""
    t = np.asarray(rec["t"]); span = float(t[-1] - BURN)
    Wlate = max(LATE_W_MIN, 0.2 * span); t_lo = max(BURN, t[-1] - Wlate)
    kb = int(np.searchsorted(t, t_lo))
    D = v2_out["D"]
    r_bond = (D["d3"]["gr"].get("r_bond") if D["d3"].get("gr") else None)
    tfr, esets, deg = MV3.bond_frames(rec, r_bond=r_bond)
    bond_alive = D["d5"].get("phase") in ("liquid", "flicker")
    memf = rec.get("memf", {}) or {}; mem_cs = sorted(memf.keys())
    ct = np.asarray(rec["ct"]); L = float(rec["L"]); na = rec["na"]
    rows, pos, times = [], [], []
    for tr in rec["_tracks"]:
        ks = np.asarray(tr["ks"]); sel = ks >= kb
        if sel.sum() < D7B_MIN_TRACK: continue
        areas = np.asarray(tr["area"], float)[sel]
        sp, v, ks_v = MV3.track_speeds(tr); sel_v = ks_v >= kb
        spd = sp[sel_v] if sel_v.sum() else np.zeros(1)
        dtr = deg.get(tr["tid"], {}); ks_c = [k for k in dtr if k >= kb]
        deg_mean = float(np.mean([dtr[k] for k in ks_c])) if ks_c else 0.0
        REC = getattr(MV3, "REC", 25.0); CREC = getattr(MV3, "CREC", 250.0)
        n_crec = max(int(sel.sum() * REC / CREC), 1)
        bond_frac = min(len(ks_c) / n_crec, 1.0)
        p = np.asarray(tr["yx"], float)[sel] % L
        my, mx = float(np.median(p[:, 0])), float(np.median(p[:, 1]))
        comp = []
        if mem_cs:
            cm_sel = np.where(ct >= t[ks[sel][0]])[0]
            f0 = int(cm_sel[0]) if len(cm_sel) else len(ct) - 1
            for c in mem_cs:
                S = np.asarray(memf[c]); nb = S.shape[1]
                iy = min(int(my / L * nb), nb - 1); ix = min(int(mx / L * nb), nb - 1)
                comp.append(float(np.mean(S[f0:, iy, ix])))
        one_hot = [1.0 if tr["act"] == a else 0.0 for a in range(na)]
        rows.append([np.log(max(np.median(areas), 1e-3)),
                     float(np.std(areas) / max(np.mean(areas), 1e-9)),
                     float(np.median(spd)), float(np.percentile(spd, 90)),
                     deg_mean, bond_frac] + one_hot + comp)
        pos.append(p); times.append(t[ks[sel]])
    if len(rows) < D7B_MIN_ROWS: return None, "few_tracks", None, None
    X = np.asarray(rows, float)
    floors = ([0.10, 0.03, MOVE_THR, MOVE_THR, 0.25, 0.10] + [0.25] * na
              + [1e-3] * (X.shape[1] - 6 - na))
    sd = X.std(axis=0); keep = sd > np.asarray(floors[:X.shape[1]])
    if not bond_alive: keep[4] = keep[5] = False
    if int(keep.sum()) == 0: return None, "no_features", None, None
    Xz = (X[:, keep] - X[:, keep].mean(axis=0)) / sd[keep]
    kmax = int(min(D7B_KMAX, len(rows) // 3))
    if int(keep.sum()) == 1: kmax = min(kmax, 2)
    best = (1, None, -1.0)
    for k in range(2, max(kmax, 2) + 1):
        try: cent, lab = kmeans2(Xz, k, minit="++", seed=7, iter=30)
        except Exception: continue
        if len(np.unique(lab)) < 2: continue
        s = MV3._silhouette(Xz, lab, k)
        if s > best[2]: best = (k, lab, s)
    k_best, lab, sil = best
    if lab is None or (sil is not None and sil < D7B_SIL_FLOOR):
        return None, f"one_species(sil={sil})", None, None
    return lab, None, pos, times


def h9_from_frames(lab, pos, times, L, P=4, B=60, seed=0):
    """MI-based segregation with permutation null + cross-half persistence."""
    rng = np.random.default_rng(seed)
    frames = []          # (species, patch, half)
    tmid = np.median(np.concatenate(times))
    for s, (p, tt) in enumerate(zip(pos, times)):
        lab_s = lab[s]
        iy = np.minimum((p[:, 0] / L * P).astype(int), P - 1)
        ix = np.minimum((p[:, 1] / L * P).astype(int), P - 1)
        pid = iy * P + ix
        half = (tt >= tmid).astype(int)
        for j in range(len(pid)):
            frames.append((lab_s, pid[j], half[j]))
    F = np.asarray(frames, int)
    if len(F) < 50: return dict(h9=0.0, why="few_frames")
    def mi_uc(F):
        M = np.zeros((P * P, int(F[:, 0].max()) + 1))
        for sp, pid in zip(F[:, 0], F[:, 1]): M[pid, sp] += 1
        Pj = M / M.sum()
        ps = Pj.sum(0); pp = Pj.sum(1)
        Hs = -np.sum(ps[ps > 0] * np.log(ps[ps > 0]))
        if Hs <= 1e-12: return 0.0, 0.0
        I = 0.0
        for a in range(Pj.shape[0]):
            for b in range(Pj.shape[1]):
                if Pj[a, b] > 0:
                    I += Pj[a, b] * np.log(Pj[a, b] / (pp[a] * ps[b]))
        return I, Hs
    I, Hs = mi_uc(F)
    # permutation null: shuffle labels ACROSS TRACKS (track-level exchangeability)
    Inull = []
    ntr = len(pos)
    counts = [len(p) for p in pos]
    for _ in range(B):
        perm = rng.permutation(lab[:ntr])
        Fp = F.copy()
        # rebuild species col by track blocks
        col = np.concatenate([np.full(c, perm[s], int) for s, c in enumerate(counts)])
        Fp[:, 0] = col
        Inull.append(mi_uc(Fp)[0])
    I0 = float(np.mean(Inull))
    uc = max(0.0, (I - I0)) / max(Hs - I0, 1e-9)
    # persistence: patch species-mix JS between halves
    js_list, w_list = [], []
    for pid in range(P * P):
        m = {}
        for h in (0, 1):
            sel = (F[:, 1] == pid) & (F[:, 2] == h)
            if sel.sum() < 5: m[h] = None; continue
            v = np.bincount(F[sel, 0], minlength=int(F[:, 0].max()) + 1).astype(float)
            m[h] = v / v.sum()
        if m[0] is None or m[1] is None: continue
        avg = 0.5 * (m[0] + m[1])
        def kl(a, b):
            s = (a > 0)
            return float(np.sum(a[s] * np.log(a[s] / b[s])))
        js = 0.5 * kl(m[0], avg) + 0.5 * kl(m[1], avg)
        js_list.append(js); w_list.append((F[:, 1] == pid).sum())
    if not js_list: return dict(h9=0.0, why="no_stable_patches", uc=round(uc, 4))
    w = np.asarray(w_list, float); w /= w.sum()
    pers = 1.0 - float(np.sum(w * np.asarray(js_list))) / np.log(2)
    pers = max(0.0, min(1.0, pers))
    return dict(h9=round(uc * pers, 4), uc=round(uc, 4), pers=round(pers, 4),
                I=round(I, 4), I0=round(I0, 4), Hs=round(Hs, 4), n_frames=len(F))


def controls(lab, pos, times, L, P=4):
    """positional relabel (pos-control) + random relabel (neg-control) + mixing curve."""
    rng = np.random.default_rng(1)
    medx = np.array([np.median(p[:, 1]) for p in pos])
    lab_pos = (medx >= np.median(medx)).astype(int)     # perfect positional species
    out = {"seg_control": h9_from_frames(lab_pos, pos, times, L, P)["h9"]}
    lab_rand = rng.permutation(lab)
    out["shuffle_control"] = h9_from_frames(lab_rand, pos, times, L, P)["h9"]
    curve = []
    for f in (0.25, 0.5, 0.75):
        lb = lab_pos.copy()
        idx = rng.choice(len(lb), int(f * len(lb)), replace=False)
        lb[idx] = rng.integers(0, 2, len(idx))
        curve.append((f, h9_from_frames(lb, pos, times, L, P)["h9"]))
    out["mixing_curve"] = curve
    return out


if __name__ == "__main__":
    path = sys.argv[1]; P = int(sys.argv[2]) if len(sys.argv) > 2 else 4
    z = np.load(path, allow_pickle=True); rec = dict(z["run"].item())
    v2 = MV2.full_battery(rec, genome=None)
    lab, why, pos, times = track_table(rec, v2)
    name = os.path.basename(path)
    if lab is None:
        print(json.dumps(dict(rec=name, h9=0.0, why=why))); sys.exit(0)
    res = h9_from_frames(lab, pos, times, float(rec["L"]), P)
    res["k_species"] = int(lab.max()) + 1
    res["n_tracks"] = len(pos)
    ctl = controls(lab, pos, times, float(rec["L"]), P)
    print(json.dumps(dict(rec=name, P=P, **res, **ctl)))
