"""metrics_v3.py — v3 Track B extension battery: C9 'spatial economy' + d7b
emergent species (2026-08-31, per V3_TRACKB_SPEC.md).

RELOCK PROTOCOL: extends the LOCKED metrics_v1/metrics_v2 (imported verbatim,
never edited). This module adds descriptors on TOP of a metrics_v2 battery
output; it never changes v2 numbers. New lock table: v3_lock_hashes.txt
(written after the validation gate passes; see VALIDATION_V3.md).

C9 SPATIAL ECONOMY = geometric mean of four [0,1] factors (spec: any zero
kills it; factors that cannot be computed from the available record streams
are None -> geometric mean over the AVAILABLE factors, partial=True):

 t9 TRAVERSAL      emptiness that is USED (void tent x percolation x
                   track-displacement-through-void per 100tu).
 s9 SURFACE        coupling-term flux density lives in the 2px boundary
                   shell (needs full-field snapshots; assay_v3 captures them).
 e9 EPISODIC       bond-lifetime mass in the 10-500tu band, frozen penalty
                   (d5 bond machinery verbatim: same r_bond/hysteresis).
 r9 DIVERSITY      d7b emergent phenotype clusters (k-means + silhouette on
                   per-blob features), n_eff = exp(entropy), takeover discount.

interest_v3 = 100 * (0.75 * sum(W_V2 * C) + 0.25 * C9) * alive
(v2 components keep their relative proportions; W9 = 0.25 of total).

Spatial class {mixed|structured|economy} from (s9, t9) — archive niche axis.

TUNABLE PRIORS (validated / to be re-tuned at the gate, see VALIDATION_V3.md):
  VOID_KNOTS, VOID_DILATE_PX, NEFF_LOG_TARGET, E9_BAND, class thresholds.

Input contract: full_battery_v3(rec, genome=None, fsnaps=None, v2_out=None).
  rec     : soup_sim_v2 record (mutated with _tracks by the v2 battery).
  fsnaps  : optional dict(t=[tu...], F=[(na+nc,N,N) arrays...]) late-window
            FULL-field snapshots (assay_v3 provides them). Without them:
            t9 falls back to a blob-disk mask reconstruction (mask_src=
            "disks"), s9 -> None (partial=True).
  v2_out  : optional precomputed metrics_v2.full_battery output (else run).
"""
import os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search")
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "stage2", "lib"))
import metrics_v1 as MV1
import metrics_v2 as MV2
from metrics_v1 import (BURN, REC, CREC, MOVE_THR, window_mask, series_n,
                        min_image, build_tracks, track_speeds)

# ---------------------------------------------------------------- tunables
# void band: TRAPEZOID knots (lo0, lo1, hi1, hi2) on the RAW void fraction
# (complement of union thr_a support, spec-literal). Rationale (documented
# prior, validated at the gate): raw void for ANY sparse blob world sits at
# 0.95-0.99 — a symmetric tent [0.35,0.9] would zero the sparse positives.
# Plateau credit for any void majority; kill only labyrinth-dense (< lo0)
# and blank/merely-dead (> hi2, C1 gate handles truly dead).
VOID_KNOTS = (0.35, 0.55, 0.97, 0.995)
VOID_DILATE_PX = 0.0       # optional support skirt (0 = spec-literal raw)
TRAV_WIN = 100.0           # tu per traversal window
TRAV_RADII = 3.0           # full credit at >= this many blob radii / window
TRAV_CHORD_PTS = 6         # interior sample points on each window chord
SHELL_PX = 2.0             # s9 boundary shell half-width (dilate xor erode)
E9_BAND = (10.0, 500.0)    # episodic bond-lifetime band (tu)
E9_FROZEN = 0.80           # pair bonded > this fraction of window = frozen
LATE_W_MIN = 1000.0        # d7b late window: last max(this, 0.2*span) tu
D7B_KMAX = 24              # k-means scan ceiling
D7B_MIN_ROWS = 6           # min feature rows to attempt clustering
D7B_MIN_TRACK = 8          # min REC frames a track needs in the late window
D7B_PERSIST = 500.0        # cluster time-coverage to count as a species (tu)
D7B_SIL_FLOOR = 0.25       # best silhouette below this -> single cluster
NEFF_LOG_TARGET = 24.0     # r9 = clip(log2(n_eff)/log2(this))
S9_CLASS, T9_CLASS = 0.50, 0.35   # spatial-class thresholds (prior)
W9 = 0.25                  # C9 weight share in interest_v3


# ---------------------------------------------------------------- helpers
def tent(v, lo0, lo1, hi1, hi2):
    """Trapezoid on (lo0, lo1, hi1, hi2): 0 below lo0/above hi2, 1 on
    [lo1, hi1], linear ramps between."""
    if v is None or not np.isfinite(v):
        return 0.0
    if v <= lo0 or v >= hi2:
        return 0.0
    if v < lo1:
        return float((v - lo0) / max(lo1 - lo0, 1e-9))
    if v <= hi1:
        return 1.0
    return float((hi2 - v) / max(hi2 - hi1, 1e-9))


def _wrap_binary(mask, op, iters):
    """Periodic binary dilation/erosion via padded scipy ops (wrap)."""
    from scipy import ndimage
    if iters <= 0:
        return mask.copy()
    p = iters
    big = np.pad(mask, p, mode="wrap")
    if op == "dil":
        big = ndimage.binary_dilation(big, iterations=iters)
    else:
        big = ndimage.binary_erosion(big, iterations=iters)
    return big[p:-p, p:-p]


def support_mask(F_acts, thr_a):
    """Union act support at thr_a from a full-field snapshot (acts block)."""
    m = np.zeros(F_acts.shape[1:], bool)
    for i in range(F_acts.shape[0]):
        m |= np.asarray(F_acts[i], np.float64) > thr_a[i]
    return m


def disk_mask_from_blobs(rec, k, dilate_cells=0):
    """Fallback support mask on the sim grid from blob lists at REC frame k
    (disks of radius sqrt(area/pi) at blob centroids). mask_src='disks'."""
    L = float(rec["L"])
    dx = 0.5
    N = int(round(L / dx))
    yy = (np.arange(N) + 0.5) * dx
    m = np.zeros((N, N), bool)
    for i in range(rec["na"]):
        for (y, x, a, p) in rec["blobs"][i][k]:
            r = max(np.sqrt(max(a, 1e-9) / np.pi), dx)
            dy = min_image(yy - y, L)[:, None]
            dxx = min_image(yy - x, L)[None, :]
            m |= (dy * dy + dxx * dxx) <= r * r
    if dilate_cells > 0:
        m = _wrap_binary(m, "dil", dilate_cells)
    return m


def blob_radius_med(rec, kb=None):
    """Median blob radius (px) over the post-burn window."""
    t = np.asarray(rec["t"])
    kb = int(np.argmax(window_mask(t))) if kb is None else kb
    areas = []
    for i in range(rec["na"]):
        for k in range(kb, len(t), 4):
            areas += [b[2] for b in rec["blobs"][i][k]]
    if not areas:
        return None
    return float(np.sqrt(np.median(areas) / np.pi))


def void_percolates(void):
    """True if the largest void component spans the box along EITHER axis.
    Periodic labeling (so a wrap-connected void counts once); span measured
    as touching every row (axis 0) or every column (axis 1)."""
    import genome as G
    lab, n = G.periodic_label(void)
    if n == 0:
        return False
    cnt = np.bincount(lab.ravel(), minlength=n + 1)[1:]
    j = int(np.argmax(cnt)) + 1
    m = lab == j
    rows = m.any(axis=1).all()
    cols = m.any(axis=0).all()
    return bool(rows or cols)


# ---------------------------------------------------------------- bonds
def bond_frames(rec, r_bond=None):
    """Per-CREC-frame bond edge sets over track ids (metrics_v1 d5 rules
    VERBATIM: 1.5*r_bond enter, 1.15x leave hysteresis). Returns
    (frame times tu, list of edge sets, deg: tid -> {frame_k: degree})."""
    tracks = rec["_tracks"]
    t = np.asarray(rec["t"]); L = rec["L"]
    kb = int(np.argmax(window_mask(t)))
    stride = int(round(CREC / REC))
    frames = list(range(kb, len(t), stride))
    pos_by_frame = {k: [] for k in frames}
    for tr in tracks:
        ks = np.asarray(tr["ks"]); raw = np.asarray(tr["yx"], float)
        for j, kk in enumerate(ks):
            if kk in pos_by_frame:
                pos_by_frame[kk].append((tr["tid"], raw[j][0] % L,
                                         raw[j][1] % L))
    rb = float(np.clip(r_bond if r_bond else 16.0, 10.0, 25.0)) * 1.5
    rb_out = 1.15 * rb
    edges_prev = None
    esets, tfr = [], []
    deg = {}
    for k in frames:
        rows = pos_by_frame[k]
        E = set()
        if len(rows) >= 2:
            ids = np.array([r[0] for r in rows])
            P = np.array([[r[1], r[2]] for r in rows], float)
            dm = P[:, None, :] - P[None, :, :]
            dd = np.hypot(min_image(dm[..., 0], L), min_image(dm[..., 1], L))
            iu = np.triu_indices(len(rows), 1)
            for a, b in zip(*iu):
                key = (min(ids[a], ids[b]), max(ids[a], ids[b]))
                thr_ab = rb_out if (edges_prev is not None
                                    and key in edges_prev) else rb
                if dd[a, b] <= thr_ab:
                    E.add(key)
        for (a, b) in E:
            deg.setdefault(a, {})[k] = deg.get(a, {}).get(k, 0) + 1
            deg.setdefault(b, {})[k] = deg.get(b, {}).get(k, 0) + 1
        esets.append(E)
        tfr.append(float(t[k]))
        edges_prev = E
    return np.asarray(tfr), esets, deg


def bond_lifetimes(tfr, esets):
    """Contiguous bonded intervals per pair -> list of
    (pair, lifetime_tu, censored_start, censored_end)."""
    if len(tfr) == 0:
        return []
    open_at = {}
    out = []
    prev = set()
    for j, E in enumerate(esets):
        for e in E - prev:
            open_at[e] = j
        for e in prev - E:
            j0 = open_at.pop(e)
            out.append((e, (j - j0) * CREC, j0 == 0, False))
        prev = E
    for e, j0 in open_at.items():
        out.append((e, (len(esets) - j0) * CREC, j0 == 0, True))
    return out


# ================================================================= t9
def t9_traversal(rec, v2_out, masks=None, mask_ts=None):
    """Traversal factor: void trapezoid x percolation x track-through-void
    displacement (median over moving tracks, per TRAV_WIN, in blob radii).
    masks: optional list of VOID boolean arrays (True = void) on the sim
    grid + times (from full snapshots); None -> disk-mask fallback."""
    D = v2_out["D"]
    alive = (D["d1"].get("n_end", 0) or 0) >= 2
    out = dict(t9=0.0, void_frac=None, percolates=None, disp_med=None,
               disp_score=None, r_blob=None, n_win=0, n_win_void=0,
               mask_src=None, alive=bool(alive))
    if not alive:
        return out
    t = np.asarray(rec["t"])
    L = float(rec["L"]); dx = 0.5
    dil = int(round(VOID_DILATE_PX / dx))
    # ---- void masks (True = void)
    if masks is None:
        ksel = sorted(k for k in range(len(t) - 1, -1, -8)
                      if t[k] >= BURN)[-6:]
        if not ksel:
            return out
        masks = [~disk_mask_from_blobs(rec, k, dilate_cells=dil)
                 for k in ksel]
        mask_ts = [float(t[k]) for k in ksel]
        out["mask_src"] = "disks"
    else:
        out["mask_src"] = "snaps"
        if mask_ts is None:
            mask_ts = [float(t[-1])] * len(masks)
    mask_ts = np.asarray(mask_ts, float)
    vf = float(np.mean([m.mean() for m in masks]))
    out["void_frac"] = round(vf, 4)
    tv = tent(vf, *VOID_KNOTS)
    out["void_tent"] = round(tv, 4)
    perc = void_percolates(masks[-1])
    out["percolates"] = bool(perc)
    rb = blob_radius_med(rec)
    out["r_blob"] = round(rb, 2) if rb else None
    if rb is None or tv <= 0.0 or not perc:
        return out
    # ---- track displacement through void per TRAV_WIN window
    kb = int(np.argmax(window_mask(t)))
    wrec = max(int(round(TRAV_WIN / REC)), 2)
    N = masks[0].shape[0]
    disps = []
    n_win = n_win_void = 0
    for tr in rec["_tracks"]:
        ks = np.asarray(tr["ks"])
        sel = ks >= kb
        if sel.sum() < wrec + 1:
            continue
        p = np.asarray(tr["yx"], float)[sel]
        kk = ks[sel]
        for j in range(0, len(p) - wrec, wrec // 2):
            a, b = p[j], p[j + wrec]
            d = float(np.hypot(*(b - a)))
            n_win += 1
            if d <= MOVE_THR * TRAV_WIN:
                continue                     # parked: not traversal
            # chord samples between the endpoints (exclusive) vs the
            # temporally nearest void mask
            tm = float(t[kk[j + wrec // 2]])
            mi = int(np.argmin(np.abs(mask_ts - tm)))
            m = masks[mi]
            fr = np.linspace(0.0, 1.0, TRAV_CHORD_PTS + 2)[1:-1]
            pts = a[None, :] + fr[:, None] * (b - a)[None, :]
            iy = np.floor((pts[:, 0] % L) / dx).astype(int) % N
            ix = np.floor((pts[:, 1] % L) / dx).astype(int) % N
            void_share = float(m[iy, ix].mean())
            if void_share >= 0.5:
                n_win_void += 1
                disps.append(d)
    out["n_win"], out["n_win_void"] = n_win, n_win_void
    if not disps:
        return out
    dmed = float(np.median(disps))
    out["disp_med"] = round(dmed, 2)
    ds = float(np.clip(dmed / (TRAV_RADII * rb), 0.0, 1.0))
    out["disp_score"] = round(ds, 4)
    out["t9"] = round(tv * ds, 4)
    return out


# ================================================================= s9
def coupling_flux_terms(F, genome):
    """Per-coupling |term| flux-density maps evaluated on a FULL snapshot
    F (na+nc, N, N), genome conventions verbatim (soup_sim op order):
      K linear:  |K[i,c] * x_c|            (activator i reads channel c)
      bilin:     |coef * x_c * x_c2|       (vertex on activator i)
      W drive:   |W[c,a] * g_c(u_a - u0_a)|  (activator a writes channel c)
    Returns list of (kind, label, map2d)."""
    na = len(genome["acts"])
    nc = len(genome["chans"])
    W = np.asarray(genome["W"], float)
    K = np.asarray(genome["K"], float)
    u0 = np.array([a["u0"] for a in genome["acts"]])
    U = np.asarray(F[:na], np.float64)
    X = np.asarray(F[na:na + nc], np.float64)
    eps = MV2.W_COUP_EPS
    terms = []
    for i in range(na):
        for c in range(nc):
            if abs(K[i, c]) > eps:
                terms.append(("K", f"K[{i},{c}]", np.abs(K[i, c] * X[c])))
    for b in genome.get("bilin", []):
        i, c, c2, coef = int(b[0]), int(b[1]), int(b[2]), float(b[3])
        if abs(coef) > eps:
            terms.append(("bilin", f"B[{i},{c},{c2}]",
                          np.abs(coef * X[c] * X[c2])))
    for c in range(nc):
        ch = genome["chans"][c]
        for a in range(na):
            if abs(W[c, a]) > eps:
                z = U[a] - u0[a]
                if ch["g"] == "id":
                    v = z
                else:
                    v = np.tanh(np.clip(z - ch.get("thr", 0.0), 0.0, None)
                                / max(ch.get("sc", 1.0), 1e-9))
                terms.append(("W", f"W[{c},{a}]", np.abs(W[c, a] * v)))
    return terms


def s9_surface(rec, genome, fsnaps):
    """Surface-locality: fraction of total coupling flux inside the 2px
    boundary shell of organism support, averaged over snapshots. Needs
    full-field snapshots + genome; else None (partial)."""
    if genome is None or not fsnaps or not fsnaps.get("F"):
        return dict(s9=None, why="no_snaps" if genome else "no_genome")
    na = rec["na"]
    thr_a = np.asarray(rec["thr"], float)
    dx = 0.5
    dil = int(round(SHELL_PX / dx))
    per_pair = {}
    s9_num = s9_den = 0.0
    shell_area = mask_area = 0.0
    n_used = 0
    for F in fsnaps["F"]:
        m = support_mask(np.asarray(F[:na]), thr_a)
        if not m.any() or m.all():
            continue
        shell = _wrap_binary(m, "dil", dil) ^ _wrap_binary(m, "ero", dil)
        n_used += 1
        shell_area += float(shell.mean())
        mask_area += float(m.mean())
        for kind, lab, tm in coupling_flux_terms(F, genome):
            num = float(tm[shell].sum())
            den = float(tm.sum())
            d = per_pair.setdefault(lab, dict(kind=kind, num=0.0, den=0.0))
            d["num"] += num
            d["den"] += den
            s9_num += num
            s9_den += den
    if n_used == 0 or s9_den <= 0:
        return dict(s9=None, why="empty_or_full_mask")
    s9 = s9_num / s9_den
    shell_frac = shell_area / n_used
    pairs = {lab: dict(kind=d["kind"],
                       s=round(d["num"] / max(d["den"], 1e-12), 4),
                       share=round(d["den"] / s9_den, 4))
             for lab, d in per_pair.items()}
    return dict(s9=round(float(s9), 4), shell_frac=round(shell_frac, 4),
                mask_frac=round(mask_area / n_used, 4), n_snaps=n_used,
                enrich=round(float(s9 / max(shell_frac, 1e-9)), 2),
                pairs=pairs)


# ================================================================= e9
def e9_episodic(rec, v2_out):
    """Episodic-encounter factor from bond lifetimes (d5 machinery verbatim).
    e9 = (bond-lifetime mass in [10,500]tu band / total mass) * (1-frozen)
    frozen = fraction of PAIRS bonded > 80% of the observed window."""
    D = v2_out["D"]
    r_bond = (D["d3"]["gr"].get("r_bond") if D["d3"].get("gr") else None)
    tfr, esets, deg = bond_frames(rec, r_bond=r_bond)
    out = dict(e9=0.0, n_bonds=0, mass_epi=0.0, mass_tot=0.0,
               frozen_frac=None, life_med=None)
    if len(tfr) < 4:
        return out
    lives = bond_lifetimes(tfr, esets)
    if not lives:
        return out
    win = float(tfr[-1] - tfr[0] + CREC)
    lo, hi = E9_BAND
    mass_tot = mass_epi = 0.0
    per_pair_bonded = {}
    Ls = []
    for (pair, Lt, c0, c1) in lives:
        mass_tot += Lt
        Ls.append(Lt)
        per_pair_bonded[pair] = per_pair_bonded.get(pair, 0.0) + Lt
        # censored-at-end bonds longer than the band top are NOT episodic;
        # censored bonds inside the band count (they lived >= Lt, and a bond
        # that has already outlived `lo` is at least an encounter).
        if lo <= Lt <= hi and not (c1 and Lt >= hi):
            mass_epi += Lt
    frozen = [p for p, b in per_pair_bonded.items() if b > E9_FROZEN * win]
    frozen_frac = len(frozen) / max(len(per_pair_bonded), 1)
    e9 = (mass_epi / max(mass_tot, 1e-9)) * (1.0 - frozen_frac)
    out.update(e9=round(float(e9), 4), n_bonds=len(lives),
               mass_epi=round(mass_epi, 1), mass_tot=round(mass_tot, 1),
               frozen_frac=round(float(frozen_frac), 4),
               life_med=round(float(np.median(Ls)), 1),
               epi_frac=round(float(mass_epi / max(mass_tot, 1e-9)), 4))
    return out


# ================================================================= d7b / r9
def _silhouette(Xz, lab, k):
    """Mean silhouette (subsampled for large n)."""
    n = len(lab)
    idx = np.arange(n)
    if n > 400:
        rs = np.random.default_rng(0)
        idx = rs.choice(n, 400, replace=False)
    S = []
    D = np.linalg.norm(Xz[idx][:, None, :] - Xz[None, :, :], axis=2)
    for r, i in enumerate(idx):
        li = lab[i]
        same = lab == li
        same_i = same.copy(); same_i[i] = False
        if same_i.sum() == 0:
            continue
        a = D[r][same_i].mean()
        b = np.inf
        for c in range(k):
            if c == li:
                continue
            selc = lab == c
            if selc.sum() == 0:
                continue
            b = min(b, D[r][selc].mean())
        if not np.isfinite(b):
            continue
        S.append((b - a) / max(a, b, 1e-12))
    return float(np.mean(S)) if S else -1.0


def d7b_species(rec, v2_out):
    """Emergent phenotype species: per-TRACK feature vectors in the late
    window -> k-means + silhouette -> persisting clusters -> n_eff, takeover.
    Features per track (late window): log-area, speed p50/p90, area CV,
    bond degree mean, bonded fraction, act one-hot, mem-field composition
    at the track centroid (CREC memf stream)."""
    t = np.asarray(rec["t"])
    if len(t) < 8:
        return dict(n_species=0, n_eff=0.0, r9=0.0, why="short")
    span = float(t[-1] - BURN)
    Wlate = max(LATE_W_MIN, 0.2 * span)
    t_lo = max(BURN, t[-1] - Wlate)
    kb = int(np.searchsorted(t, t_lo))
    D = v2_out["D"]
    r_bond = (D["d3"]["gr"].get("r_bond") if D["d3"].get("gr") else None)
    tfr, esets, deg = bond_frames(rec, r_bond=r_bond)
    # frozen/absent bond graph: degree is a POSITIONAL accident, not a
    # phenotype (static gas m0 lesson) — drop bond features from clustering.
    bond_alive = D["d5"].get("phase") in ("liquid", "flicker")
    # mem composition sampler (coarse CREC memf stream)
    memf = rec.get("memf", {}) or {}
    mem_cs = sorted(memf.keys())
    ct = np.asarray(rec["ct"])
    L = float(rec["L"])
    rows, meta = [], []
    na = rec["na"]
    for tr in rec["_tracks"]:
        ks = np.asarray(tr["ks"])
        sel = ks >= kb
        if sel.sum() < D7B_MIN_TRACK:
            continue
        areas = np.asarray(tr["area"], float)[sel]
        sp, v, ks_v = track_speeds(tr)
        sel_v = ks_v >= kb
        spd = sp[sel_v] if sel_v.sum() else np.zeros(1)
        # bond degree on CREC frames covered by this track
        dtr = deg.get(tr["tid"], {})
        ks_c = [k for k in dtr if k >= kb]
        deg_mean = float(np.mean([dtr[k] for k in ks_c])) if ks_c else 0.0
        n_crec = max(int(sel.sum() * REC / CREC), 1)
        bond_frac = min(len(ks_c) / n_crec, 1.0)
        # mem composition at track median position
        p = np.asarray(tr["yx"], float)[sel] % L
        my, mx = float(np.median(p[:, 0])), float(np.median(p[:, 1]))
        comp = []
        if mem_cs:
            cm_sel = np.where(ct >= t[ks[sel][0]])[0]
            f0 = int(cm_sel[0]) if len(cm_sel) else len(ct) - 1
            for c in mem_cs:
                S = np.asarray(memf[c])
                nb = S.shape[1]
                iy = min(int(my / L * nb), nb - 1)
                ix = min(int(mx / L * nb), nb - 1)
                comp.append(float(np.mean(S[f0:, iy, ix])))
        one_hot = [1.0 if tr["act"] == a else 0.0 for a in range(na)]
        rows.append([np.log(max(np.median(areas), 1e-3)),
                     float(np.std(areas) / max(np.mean(areas), 1e-9)),
                     float(np.median(spd)), float(np.percentile(spd, 90)),
                     deg_mean, bond_frac] + one_hot + comp)
        meta.append(dict(tid=tr["tid"], act=tr["act"],
                         k0=int(ks[sel][0]), k1=int(ks[sel][-1]),
                         nrec=int(sel.sum())))
    out = dict(n_tracks=len(rows), n_species=0, n_eff=0.0, takeover=0.0,
               r9=0.0, k_best=0, sil=None, features=None)
    if len(rows) < D7B_MIN_ROWS:
        # a world alive with ONE persistent blob is a 1-species world
        alive = (D["d1"].get("n_end", 0) or 0) >= 2
        if alive and rows:
            out.update(n_species=1, n_eff=1.0, r9=0.0)
        return out
    X = np.asarray(rows, float)
    # physical spread floors per feature: a feature enters clustering only
    # if its population spread exceeds measurement noise (identical-blob
    # worlds must NOT fake species out of tracker jitter — m0 lesson).
    floors = ([0.10,                        # log-area: 10% area spread
               0.03,                        # area CV
               MOVE_THR, MOVE_THR,          # speed p50 / p90 (px/tu)
               0.25, 0.10]                  # bond degree / bonded fraction
              + [0.25] * na                 # act one-hot (real if mixed)
              + [1e-3] * (X.shape[1] - 6 - na))   # mem composition
    sd = X.std(axis=0)
    keep = sd > np.asarray(floors[:X.shape[1]])
    if not bond_alive:
        keep[4] = keep[5] = False           # deg_mean, bond_frac out
    nfeat = int(keep.sum())
    out["features"] = nfeat
    if nfeat == 0:
        # nothing varies beyond noise: one phenotype
        out.update(n_species=1, n_eff=1.0, k_best=1, r9=0.0)
        return out
    Xz = (X[:, keep] - X[:, keep].mean(axis=0)) / sd[keep]
    # ---- k-means + silhouette scan
    from scipy.cluster.vq import kmeans2
    kmax = int(min(D7B_KMAX, len(rows) // 3))
    best = (1, None, -1.0)
    for k in range(2, max(kmax, 2) + 1):
        try:
            cent, lab = kmeans2(Xz, k, minit="++", seed=7, iter=30)
        except Exception:
            continue
        if len(np.unique(lab)) < 2:
            continue
        s = _silhouette(Xz, lab, k)
        if s > best[2]:
            best = (k, lab, s)
    k_best, lab, sil = best
    if lab is None or sil < D7B_SIL_FLOOR:
        k_best, lab, sil = 1, np.zeros(len(rows), int), sil
    out["k_best"] = int(k_best)
    out["sil"] = round(float(sil), 4) if sil is not None else None
    # ---- persistence per cluster (track-frame time coverage, tu)
    tt = t
    persist, occup = {}, {}
    for c in range(k_best):
        sel = lab == c
        if sel.sum() == 0:
            continue
        cov = np.zeros(len(tt), bool)
        occ = 0.0
        for m, s_ in zip(np.asarray(meta)[sel], X[sel]):
            cov[m["k0"]:m["k1"] + 1] = True
            occ += m["nrec"]
        persist[c] = float(cov.sum() * REC)
        occup[c] = occ
    species = [c for c, pv in persist.items() if pv >= D7B_PERSIST]
    out["n_species"] = len(species)
    out["persist"] = {int(c): round(v, 0) for c, v in persist.items()}
    # ---- n_eff over persisting clusters
    if species:
        w = np.array([occup[c] for c in species], float)
        p = w / w.sum()
        H = -np.sum(p * np.log(np.clip(p, 1e-12, None)))
        n_eff = float(np.exp(H))
    else:
        n_eff = 0.0
    out["n_eff"] = round(n_eff, 3)
    # ---- takeover: max monotone share-trend of any cluster (share gain
    # over the late window; winner-take-all detector)
    takeover = 0.0
    if k_best >= 2 and len(species) >= 1:
        nbins = 8
        edges = np.linspace(kb, len(tt) - 1, nbins + 1).astype(int)
        shares = np.zeros((k_best, nbins))
        for c in range(k_best):
            selc = np.where(lab == c)[0]
            for b in range(nbins):
                lo_k, hi_k = edges[b], edges[b + 1]
                tot = n_c = 0
                for j, m in enumerate(meta):
                    ov = min(m["k1"], hi_k) - max(m["k0"], lo_k)
                    if ov > 0:
                        tot += ov
                        if lab[j] == c:
                            n_c += ov
                shares[c, b] = n_c / max(tot, 1)
        tb = np.arange(nbins, dtype=float)
        for c in range(k_best):
            sl = MV2.robust_slope(tb, shares[c])
            gain = sl * (nbins - 1)
            # monotone check: correlation of share with time
            if gain > 0 and np.std(shares[c]) > 1e-9:
                r = float(np.corrcoef(tb, shares[c])[0, 1])
                if r > 0.6:
                    takeover = max(takeover, min(gain, 1.0))
    out["takeover"] = round(float(takeover), 4)
    r9 = float(np.clip(np.log2(max(n_eff, 1e-9))
                       / np.log2(NEFF_LOG_TARGET), 0.0, 1.0)) \
        * (1.0 - takeover)
    out["r9"] = round(max(r9, 0.0), 4)
    return out


# ================================================================= C9 + glue
def spatial_class(s9, t9):
    """{mixed|structured|economy} from (s9, t9). economy = interactions at
    surfaces AND used emptiness; structured = one of the two; mixed = neither.
    None s9 (no snapshots) grades on t9 alone (structured at best)."""
    s_hi = (s9 is not None) and (s9 >= S9_CLASS)
    t_hi = (t9 is not None) and (t9 >= T9_CLASS)
    if s_hi and t_hi:
        return "economy"
    if s_hi or t_hi:
        return "structured"
    return "mixed"


def c9_spatial_economy(rec, genome=None, fsnaps=None, v2_out=None,
                       void_masks=None, void_mask_ts=None):
    """Compute d8 (t9/s9/e9) + d7b (r9) + C9. Returns dict d9."""
    if v2_out is None:
        v2_out = MV2.full_battery(rec, genome=genome)
    # C1 gate: dead world -> C9 = 0 outright (spec bank c)
    alive = (v2_out["D"]["d1"].get("n_end", 0) or 0) >= 2
    t9 = t9_traversal(rec, v2_out, masks=void_masks, mask_ts=void_mask_ts)
    s9 = s9_surface(rec, genome, fsnaps)
    e9 = e9_episodic(rec, v2_out)
    d7b = d7b_species(rec, v2_out)
    factors = dict(t9=t9["t9"], s9=s9.get("s9"), e9=e9["e9"], r9=d7b["r9"])
    if not alive:
        factors = dict(t9=0.0, s9=s9.get("s9"), e9=0.0, r9=0.0)
    avail = {k: v for k, v in factors.items() if v is not None}
    partial = len(avail) < 4
    if not alive:
        C9 = 0.0
    elif not avail:
        C9 = 0.0
    else:
        vals = np.array([max(v, 0.0) for v in avail.values()], float)
        C9 = float(np.exp(np.mean(np.log(np.clip(vals, 1e-9, None))))) \
            if (vals > 0).all() else 0.0
    cls = spatial_class(factors.get("s9"), factors.get("t9"))
    return dict(C9=round(C9, 4), factors=factors, partial=partial,
                spatial_class=cls, alive=bool(alive),
                t9_detail=t9, s9_detail=s9, e9_detail=e9, d7b=d7b)


def interest_v3(v2_interest, C9):
    """interest_v3 = renormalized v2 + W9*C9 share (both on the 0-100 scale).
    v2 components keep relative proportions: total = (1-W9)*v2 + W9*100*C9."""
    return float((1.0 - W9) * v2_interest + W9 * 100.0 * C9)


def full_battery_v3(rec, genome=None, fsnaps=None, v2_out=None,
                    void_masks=None, void_mask_ts=None):
    """v2 battery (verbatim, unedited) + d9/C9 + interest_v3.
    Returns the v2 out dict EXTENDED with keys: d9, C9, interest_v2,
    interest (=v3), spatial_class."""
    if v2_out is None:
        v2_out = MV2.full_battery(rec, genome=genome)
    d9 = c9_spatial_economy(rec, genome=genome, fsnaps=fsnaps, v2_out=v2_out,
                            void_masks=void_masks, void_mask_ts=void_mask_ts)
    out = dict(v2_out)
    out["D"] = dict(v2_out["D"])
    out["D"]["d9"] = d9
    out["C"] = dict(v2_out["C"])
    out["C"]["C9_spatial"] = d9["C9"]
    out["interest_v2"] = v2_out["interest"]
    out["interest"] = round(interest_v3(v2_out["interest"], d9["C9"]), 3)
    out["spatial_class"] = d9["spatial_class"]
    return out


def lean_summary_v3(out):
    """v2 lean summary + the v3 block."""
    d = MV2.lean_summary(out)
    d9 = out["D"].get("d9", {})
    d["interest_v2"] = round(out.get("interest_v2", out["interest"]), 2)
    d["interest_v3"] = round(out["interest"], 2)
    d["d9"] = dict(C9=d9.get("C9"), cls=d9.get("spatial_class"),
                   partial=d9.get("partial"),
                   f=d9.get("factors"),
                   void=d9.get("t9_detail", {}).get("void_frac"),
                   n_eff=d9.get("d7b", {}).get("n_eff"),
                   k=d9.get("d7b", {}).get("k_best"),
                   frozen=d9.get("e9_detail", {}).get("frozen_frac"))
    return d
