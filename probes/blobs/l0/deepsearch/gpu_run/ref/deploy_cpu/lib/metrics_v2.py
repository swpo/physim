"""metrics_v2.py — LOCKED complexity battery v2 (phase 6, 2026-02-25).
Frozen after calibration on ground-truth seeds 1-2 + champion re-audits; seed 3
runs are OUT-OF-SAMPLE (executed after this lock; see VALIDATION_V2.md).
Do not edit; a new calibration round must produce metrics_v3.py.
Builds ON metrics_v1 (LOCKED, imported verbatim — d2/d3/d4/d5 + tracking
reused unchanged).
Changes (each traceable to a v1 audit failure; see VALIDATION_V2.md):
 M1 interaction gate: species count toward ecology C6 weighted by interaction
    strength (density cross-corr x3, OR genome coupling incl. bilinear paths).
    Sphere-passenger fix: non-interacting persisters get ~0 weight.
 M2 segments vs organisms: population model + growth scored on ORGANISMS
    (connected structures at thr_lo = u0+0.30*(sqrt(lam)-u0)); both exposed.
    Worm fix: a worm = 1 organism, N segments.
 M3 bilinear-aware anatomy: K=0 channels with bilinear membership are ACTIVE
    wiring (ds3_014 fossil-vertex lesson). mem channels report read_K /
    read_bilin / mem_grade (0 none|1 write-only|2 read) + charging status.
 M5 succession detector: per-species logistic t_half fits on organism counts;
    n_stages = well-separated transition midpoints -> new component C8.
 M6 box-limit flag: organisms approaching domain scale (span > 0.6*L).
Input: soup_sim_v2 record (v1 records OK: org fields fall back to thr_hi
patches, spans unavailable). genome optional: without it M1 uses behavior
only, M3 read-grades default to write-only.
"""
import os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search")
import metrics_v1 as MV1
from metrics_v1 import (BURN, REC, CREC, MEM_ABS_FLOOR, window_mask, series_n,
                        min_image, build_tracks)
from hier_metrics import compact_top_fit, macro_period_quality

W_COUP_EPS = 1e-6      # genome coupling presence floor on |W|,|K|,|coef|
XC_GAIN = 3.0          # behavioral weight = min(1, |xcorr| * XC_GAIN)
GEN_W_DIRECT = 1.0     # direct coupling: j writes chan read by i (K or bilin)
GEN_W_SHARED = 0.5     # mediated only: both write a channel someone reads
                       # ("habitat, not conveyor" — ds3_014 yellow-blue)
TREND_FRAC = 0.05      # charging floor: |slope|*window / amp scale
WTURN = 2000.0         # turnover best-window width (post-burn span at T=2500)
ORG_TREND_ABS = 1.5    # organism trend floor: |slope|*window (counts)
ORG_TREND_REL = 0.15   # ... or rel. to mean count (whichever is larger)
STAGE_MIN_R2 = 0.5     # logistic fit acceptance
STAGE_MIN_A = 2.0      # min |amplitude| (organisms) for a transition
BOX_FRAC = 0.6         # span > BOX_FRAC*L -> box-limit flag
BOX_PERSIST = 0.05     # ... in >= this fraction of post-burn frames


# ------------------------------------------------------------- org series
def org_counts(rec):
    """Per-species organism-count series on the CREC grid + spans.
    Falls back to thr_hi patches for v1 records (spans -> None)."""
    ct = np.asarray(rec["ct"])
    if "orgs" in rec:
        n_i = {i: np.array([p["n"] for p in rec["orgs"][i]])
               for i in range(rec["na"])}
        spans = {i: [max(p["spans"]) if p["spans"] else 0.0
                     for p in rec["orgs"][i]] for i in range(rec["na"])}
        return ct, n_i, spans, True
    n_i = {i: np.array([p["n"] for p in rec["patches"][i]])
           for i in range(rec["na"])}
    return ct, n_i, None, False


def movavg(x, w=3):
    if len(x) < w:
        return np.asarray(x, float)
    k = np.ones(w) / w
    return np.convolve(np.asarray(x, float), k, mode="same")


def robust_slope(t, x):
    """Theil-Sen-lite slope (median of pairwise slopes on a subsample)."""
    t = np.asarray(t, float); x = np.asarray(x, float)
    n = len(x)
    if n < 4:
        return 0.0
    idx = np.linspace(0, n - 1, min(n, 40)).astype(int)
    ts_, xs_ = t[idx], x[idx]
    sl = []
    for a in range(len(idx)):
        dt_ = ts_[a + 1:] - ts_[a]
        ok = dt_ > 0
        sl += list((xs_[a + 1:][ok] - xs_[a]) / dt_[ok])
    return float(np.median(sl)) if sl else 0.0


# ------------------------------------------------------------- M5 staging
def _logistic(t, A, th, s, n0):
    return n0 + A / (1.0 + np.exp(-np.clip((t - th) / max(s, 1e-6), -50, 50)))


def fit_stage(t, x):
    """Logistic transition fit (rise or fall). Returns dict or None."""
    from scipy.optimize import curve_fit
    t = np.asarray(t, float); x = np.asarray(x, float)
    if len(x) < 12:
        return None
    xs = movavg(x, 3)
    A0 = xs[-4:].mean() - xs[:4].mean()
    if abs(A0) < STAGE_MIN_A:
        return None
    # t_half guess: first crossing of the midpoint
    mid = xs[:4].mean() + 0.5 * A0
    cross = np.where(np.diff(np.sign(xs - mid)) != 0)[0]
    th0 = t[cross[0]] if len(cross) else t[len(t) // 2]
    span = t[-1] - t[0]
    try:
        p, _ = curve_fit(_logistic, t, xs,
                         p0=[A0, th0, max(span / 20, 50.0), xs[:4].mean()],
                         bounds=([-1e4, t[0] - span, 10.0, -1e3],
                                 [1e4, t[-1] + span, span, 1e3]),
                         maxfev=4000)
    except Exception:
        return None
    fitv = _logistic(t, *p)
    ssr = float(np.sum((xs - fitv) ** 2))
    sst = float(np.sum((xs - xs.mean()) ** 2))
    r2 = 1.0 - ssr / max(sst, 1e-12)
    A, th, s, n0 = [float(v) for v in p]
    if (r2 < STAGE_MIN_R2 or abs(A) < STAGE_MIN_A
            or not (t[0] + 0.03 * span < th < t[-1] - 0.03 * span)):
        return None
    return dict(A=round(A, 2), t_half=round(th, 1), slope_scale=round(s, 1),
                r2=round(r2, 3))


def staging(rec):
    """M5: per-species logistic transitions on organism counts; count
    well-separated t_halfs. Returns dict(n_stages, stages=[...])."""
    ct, n_i, _, _ = org_counts(rec)
    cm = window_mask(ct)
    stages = []
    for i in n_i:
        x = n_i[i][cm]
        if len(x) < 12 or x.max() < 2:
            continue
        f = fit_stage(ct[cm], x)
        if f:
            f["sp"] = i
            stages.append(f)
    stages.sort(key=lambda f: f["t_half"])
    # absolute separation (NOT T-scaled: stages must not merge when the
    # horizon extends); 500tu ~ 2x typical transition slope_scale
    sep = 500.0
    groups = []
    for f in stages:
        if groups and f["t_half"] - groups[-1][-1]["t_half"] < sep:
            groups[-1].append(f)
        else:
            groups.append([f])
    return dict(n_stages=len(groups), sep=sep, stages=stages)


# ------------------------------------------------------------- M2 d1 v2
def d1_population_v2(rec):
    """v1 d1 (segments; verbatim) + organism-level model/growth + staging."""
    d1 = MV1.d1_population(rec)
    ct, n_i, spans, has_orgs = org_counts(rec)
    cm = window_mask(ct)
    n_tot = sum(n_i.values())
    d1["n_seg_end"] = d1.get("n_end")          # explicit alias
    if cm.sum() >= 8:
        x = n_tot[cm].astype(float)
        if MV1._resid_sd(x) < MV1.AMP_GATE["count"] and x.std() < 0.5:
            fit = dict(model="constant", r2=1.0, params={})
        else:
            fit = compact_top_fit(movavg(x, 3), dt=CREC)
        n0, n1 = float(x[:4].mean()), float(x[-4:].mean())
        d1.update(org_model=fit["model"], org_r2=fit["r2"],
                  n_org_start=n0, n_org_end=float(x[-1]), n_org_mean=float(x.mean()),
                  org_growth=bool(n1 >= 1.5 * max(n0, 1.0) and n1 - n0 >= 2.0),
                  org_dwell=(fit["params"].get("mean_dwell")
                             if fit["model"] == "switch" else None))
        pq = macro_period_quality(x, dt=CREC)
        d1.update(org_osc_q=float(pq["q"]), org_osc_cycles=float(pq["n_cycles"]))
    else:
        d1.update(org_model="short", org_r2=0.0, n_org_start=0.0,
                  n_org_end=0.0, n_org_mean=0.0, org_growth=False,
                  org_dwell=None, org_osc_q=0.0, org_osc_cycles=0.0)
    st = staging(rec)
    d1["n_stages"] = st["n_stages"]
    d1["stages"] = st["stages"]
    d1["has_orgs"] = has_orgs
    # windowed turnover (adaptive-T fix): a rate averaged over a long window
    # dilutes early episodes (extension must never punish); report the BEST
    # sliding WTURN-window rate. At T=2500 (span 2000tu) this equals v1.
    t = np.asarray(rec["t"])
    m = window_mask(t)
    tracks = rec["_tracks"]
    nT = len(t)
    if m.sum() >= 20:
        n_i2, n_tot2 = series_n(rec)
        births_t = np.array([t[tr["ks"][0]] for tr in tracks
                             if tr["ks"][0] > int(np.argmax(m))])
        deaths_t = np.array([t[tr["ks"][-1]] for tr in tracks
                             if tr["ks"][-1] < nT - 1 - MV1.GAP_TOL
                             and tr["ks"][0] <= nT - 1 - MV1.GAP_TOL])
        W = WTURN
        t0s = np.arange(BURN, max(t[-1] - W, BURN) + 1e-9, 250.0)
        best = 0.0
        for w0 in t0s:
            w1 = min(w0 + W, t[-1])
            nb = float(((births_t >= w0) & (births_t < w1)).sum())
            nd = float(((deaths_t >= w0) & (deaths_t < w1)).sum())
            sel = (t >= w0) & (t < w1)
            nbar = max(float(n_tot2[sel].mean()) if sel.sum() else 0.0, 1e-9)
            span_ktu = max((w1 - w0) / 1000.0, 1e-9)
            best = max(best, (nb + nd) / nbar / span_ktu)
        d1["turnover_best"] = float(best)
    else:
        d1["turnover_best"] = d1.get("turnover", 0.0)
    return d1


# ------------------------------------------------------------- M3 d6 v2
def genome_channel_reads(genome):
    """Per-channel read map: read_K (any K column entry), read_bilin
    (member of any bilinear vertex). K=0 + bilin => ACTIVE (ds3_014)."""
    if genome is None:
        return None
    K = np.asarray(genome["K"], float)
    reads = {}
    for c in range(K.shape[1]):
        rk = bool(np.any(np.abs(K[:, c]) > W_COUP_EPS))
        rb = any((abs(b[3]) > W_COUP_EPS and (int(b[1]) == c or int(b[2]) == c))
                 for b in genome.get("bilin", []))
        reads[c] = dict(read_K=rk, read_bilin=rb, read=bool(rk or rb))
    return reads


def mem_trend(rec, c):
    """Charging status of mem channel c: slope of spatial-mean |field| over
    the last 25% of the post-burn window, scaled by amplitude."""
    ct = np.asarray(rec["ct"]); cm = window_mask(ct)
    S = np.asarray(rec["memf"][c])[cm]
    tt = ct[cm]
    if len(S) < 8:
        return dict(charging=0, trend_frac=0.0)
    m = np.abs(S).mean(axis=(1, 2))
    k0 = int(0.75 * len(m))
    if len(m) - k0 < 4:
        k0 = max(len(m) - 4, 0)
    w_t, w_x = tt[k0:], m[k0:]
    sl = robust_slope(w_t, w_x)
    win = max(w_t[-1] - w_t[0], 1e-9)
    amp = max(float(np.percentile(m, 95)), MEM_ABS_FLOOR)
    tf = sl * win / amp
    ch = 0
    if abs(tf) > TREND_FRAC:
        ch = 1 if tf > 0 else -1
    return dict(charging=ch, trend_frac=round(float(tf), 4))


def d6_memory_v2(rec, genome=None):
    """v1 d6 + genome read-awareness + charging. mem_grade: 0 no realized
    structure | 1 write-only structure | 2 read memory (K or bilinear)."""
    d6 = MV1.d6_memory(rec)
    reads = genome_channel_reads(genome)
    grades = []
    for c, v in (d6.get("chans") or {}).items():
        r = (reads or {}).get(int(c), dict(read_K=False, read_bilin=False,
                                           read=None))
        v.update(read_K=r["read_K"], read_bilin=r["read_bilin"])
        if v.get("used"):
            v.update(mem_trend(rec, int(c)))
            g = 2 if r["read"] else (1 if r["read"] is not None else 1)
            v["grade"] = g
            grades.append(g)
        else:
            v["grade"] = 0
    d6["mem_grade"] = max(grades) if grades else 0
    if d6.get("has_mem") and genome is None:
        d6["mem_grade"] = max(d6["mem_grade"], 1)   # unknown wiring: >=1
    # charging of the scoring channel (v1 best-pick rule)
    used = [(c, v) for c, v in (d6.get("chans") or {}).items() if v.get("used")]
    if used:
        bc, bv = max(used, key=lambda cv: cv[1]["cover"] * (0.2 + cv[1]["elong"]))
        d6.update(best_chan=int(bc), best_read=bool(bv.get("read_K") or
                                                    bv.get("read_bilin")),
                  charging=bv.get("charging", 0),
                  trend_frac=bv.get("trend_frac", 0.0))
    return d6


# ------------------------------------------------------------- M1 d7
def species_density_maps(rec, block=8):
    """Per-species blob-density maps (Gaussian-smoothed, wrap) on the CREC
    frame grid, post-burn. Returns (nsp, nframes, nb, nb) array or None."""
    from scipy import ndimage
    L = rec["L"]; na = rec["na"]
    nb = max(int(round(L / block)), 4)
    t = np.asarray(rec["t"])
    stride = max(int(round(CREC / REC)), 1)
    ks = [k for k in range(0, len(t), stride) if t[k] >= BURN]
    if len(ks) < 8:
        return None
    M = np.zeros((na, len(ks), nb, nb))
    for i in range(na):
        for f, k in enumerate(ks):
            for (y, x, a, p) in rec["blobs"][i][k]:
                iy = int(y / L * nb) % nb
                ix = int(x / L * nb) % nb
                M[i, f, iy, ix] += a
        M[i] = ndimage.gaussian_filter(M[i], sigma=(0, 1.0, 1.0), mode="wrap")
    return M


def genome_coupling_pairs(genome):
    """Undirected species-pair genome coupling weight matrix:
    GEN_W_DIRECT if j writes a channel act i reads (linear K or bilinear
    vertex — the ds3_014 fossil-vertex path counts), GEN_W_SHARED if the only
    link is a co-written channel that anyone reads (mediated/habitat).
    None if no genome."""
    if genome is None:
        return None
    W = np.asarray(genome["W"], float)
    K = np.asarray(genome["K"], float)
    na = K.shape[0]; nc = K.shape[1]
    bil = [b for b in genome.get("bilin", []) if abs(b[3]) > W_COUP_EPS]
    reads = genome_channel_reads(genome)
    wr = np.abs(W) > W_COUP_EPS            # (nc, na) writer map
    cp = np.zeros((na, na))
    for i in range(na):
        for j in range(na):
            if i == j:
                continue
            # direct: j writes c, i reads c linearly
            if any(wr[c, j] and abs(K[i, c]) > W_COUP_EPS for c in range(nc)):
                cp[i, j] = GEN_W_DIRECT; continue
            # bilinear: j feeds a bilin input of act i
            if any(int(b[0]) == i and (wr[int(b[1]), j] or wr[int(b[2]), j])
                   for b in bil):
                cp[i, j] = GEN_W_DIRECT; continue
            # shared channel written by BOTH i and j, and read by anyone
            if any(wr[c, i] and wr[c, j] and reads[c]["read"]
                   for c in range(nc)):
                cp[i, j] = GEN_W_SHARED
    return np.maximum(cp, cp.T)


def d7_interactions(rec, genome=None):
    """M1: pairwise interaction strengths s_ij = max(behavioral, genome).
    behavioral = min(1, XC_GAIN * |time-mean spatial cross-corr of density
    maps|); genome coupling grants GEN_W_DIRECT (direct read path, incl.
    bilinear) or GEN_W_SHARED (mediated co-written channel). Species weight
    w_i = max_j s_ij; n_species_int = max(sum w_i over ALIVE, 1 if any alive).
    Sphere-passenger fix: no coupling + no correlation -> ~0 extra weight."""
    na = rec["na"]
    out = dict(n_species_int=0.0, w=[0.0] * na, xcorr=None, gen=None)
    M = species_density_maps(rec)
    X = np.zeros((na, na))
    if M is not None and na >= 2:
        F = M.reshape(na, M.shape[1], -1)
        Fc = F - F.mean(axis=2, keepdims=True)
        sd = F.std(axis=2)
        for i in range(na):
            for j in range(i + 1, na):
                ok = (sd[i] > 1e-9) & (sd[j] > 1e-9)
                if ok.sum() < 5:
                    continue
                cf = ((Fc[i][ok] * Fc[j][ok]).mean(axis=1)
                      / (sd[i][ok] * sd[j][ok]))
                X[i, j] = X[j, i] = float(np.mean(cf))
    cp = genome_coupling_pairs(genome)
    S = np.minimum(np.abs(X) * XC_GAIN, 1.0)
    if cp is not None:
        S = np.maximum(S, cp)
    np.fill_diagonal(S, 0.0)
    w = S.max(axis=1) if na >= 2 else np.zeros(na)
    # alive filter (v1 rule: mean of last 3 count records > 0.34)
    n_i, _ = series_n(rec)
    alive = [i for i in range(na) if n_i[i][-3:].mean() > 0.34]
    # n_species_int: 1st alive species is free (a lone species is a 1-species
    # world, not a 0-species one); EXTRA species count only via interaction.
    nsi_raw = float(sum(w[i] for i in alive))
    nsi = max(nsi_raw, 1.0) if alive else 0.0
    out.update(w=[round(float(v), 3) for v in w],
               xcorr=[[round(float(v), 3) for v in row] for row in X],
               gen=(np.round(cp, 2).tolist() if cp is not None else None),
               alive=alive, n_species_int=round(nsi, 3),
               n_species_int_raw=round(nsi_raw, 3))
    return out


# ------------------------------------------------------------- M6 box flag
def box_flag(rec):
    ct, n_i, spans, has_orgs = org_counts(rec)
    L = float(rec["L"])
    if spans is None:
        return dict(box_limit=None, box_span_frac=None, box_persist=None)
    cm = window_mask(ct)
    per_frame = []
    nF = int(cm.sum())
    idx = np.where(cm)[0]
    for f in idx:
        mx = max((spans[i][f] for i in spans if f < len(spans[i])), default=0.0)
        per_frame.append(mx)
    if not per_frame:
        return dict(box_limit=None, box_span_frac=None, box_persist=None)
    per_frame = np.asarray(per_frame)
    frac = per_frame / L
    persist = float((frac > BOX_FRAC).mean())
    return dict(box_limit=bool(persist >= BOX_PERSIST),
                box_span_frac=round(float(np.percentile(frac, 95)), 3),
                box_persist=round(persist, 3))


# ---------------------------------------------------- windowed rate metrics
# Rate metrics averaged over the whole post-burn span DILUTE when a world
# settles after a rich early epoch. Under adaptive T (M4) that would make
# extension punish scores. Rule: rate components score their BEST sliding
# W_BEST window (== whole window when T=2500, so decision-point continuity
# is exact). Structure metrics (memory cover, stages, growth) use all data.
W_BEST = 2000.0


def _tent_churn(c):
    """v1 C4 log-tent over churn100 (verbatim grading)."""
    if c <= 0.005:
        return 0.25
    if c < 0.05:
        return 0.25 + 0.75 * (np.log10(c / 0.005) / 1.0)
    if c <= 1.2:
        return 1.0
    if c <= 4.0:
        return 1.0 - 0.7 * (np.log10(c / 1.2) / np.log10(4.0 / 1.2))
    return 0.3


def churn_windowed(rec, r_bond=None):
    """Per-frame bond events (v1 d5 bond rules verbatim: 1.5*r_bond enter,
    1.15x leave hysteresis) -> best sliding-window tent score."""
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
    ev, ecnt, tfr = [], [], []
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
        if edges_prev is not None:
            ev.append(len(E - edges_prev) + len(edges_prev - E))
            ecnt.append(len(E))
            tfr.append(t[k])
        edges_prev = E
    if not ev:
        return dict(churn_best=0.0, c4_best=0.0)
    ev = np.asarray(ev, float); ecnt = np.asarray(ecnt, float)
    tfr = np.asarray(tfr)
    best_c4, best_churn = 0.0, 0.0
    t0s = np.arange(tfr[0], max(tfr[-1] - W_BEST, tfr[0]) + 1e-9, 250.0)
    for w0 in t0s:
        sel = (tfr >= w0) & (tfr < w0 + W_BEST)
        if sel.sum() < 8:
            continue
        em = ecnt[sel].mean()
        if em < 0.5:
            continue
        ch = (ev[sel].sum() / 2 / em / sel.sum()) * (100.0 / CREC)
        sc = _tent_churn(ch)
        if sc > best_c4:
            best_c4, best_churn = sc, ch
    return dict(churn_best=round(float(best_churn), 4),
                c4_best=round(float(best_c4), 4))


def moving_frac_windowed(rec):
    """Best sliding-window moving fraction from track speeds (v1 thresholds)."""
    from metrics_v1 import track_speeds, MOVE_THR
    t = np.asarray(rec["t"])
    kb = int(np.argmax(window_mask(t)))
    ks_all, mv_all = [], []
    for tr in rec["_tracks"]:
        sp, v, ks = track_speeds(tr)
        sel = ks >= kb
        ks_all += list(np.asarray(ks)[sel])
        mv_all += list(sp[sel] > MOVE_THR)
    if not ks_all:
        return 0.0
    tk = t[np.asarray(ks_all, int)]
    mv = np.asarray(mv_all, float)
    best = 0.0
    t0s = np.arange(tk.min(), max(tk.max() - W_BEST, tk.min()) + 1e-9, 250.0)
    for w0 in t0s:
        sel = (tk >= w0) & (tk < w0 + W_BEST)
        if sel.sum() >= 50:
            best = max(best, float(mv[sel].mean()))
    return round(best, 4)


# ------------------------------------------------------------- components
def components_v2(D, rec):
    """v1 components with M1/M2/M3 edits + new C8 (M5) + windowed rates
    (adaptive-T continuity: extension must never punish a component)."""
    C = MV1.components(D, rec)          # start from v1 (C6/C1/C5 overwritten)
    d1, d6, d7 = D["d1"], D["d6"], D["d7"]
    # windowed C4 (graph churn) and C3 translation part
    if D["d5"].get("phase") != "gas":
        cw = churn_windowed(rec, r_bond=(D["d3"]["gr"].get("r_bond")
                                         if D["d3"].get("gr") else None))
        D["d5"]["churn_best"] = cw["churn_best"]
        C["C4_graph"] = max(C["C4_graph"], cw["c4_best"])
    mvb = moving_frac_windowed(rec)
    D["d4"]["moving_frac_best"] = mvb
    vc = max(D["d4"].get("v_corr", 0.0), 0.0)
    trans_b = mvb * (0.6 + 0.4 * vc)
    C["C3_motion"] = max(C["C3_motion"], trans_b)
    # C1 v2 (M2): organism-level class primary; segment-level class kept as
    # secondary evidence (engine/cargo bind-unbind oscillations are real even
    # when organism count is flat) — but GROWTH claims require ORGANISM growth
    # (the worm fix: N segments of one worm are not population growth).
    ob = {"constant": 0.05, "short": 0.0, "relaxation": 0.25,
          "switch": 0.7, "oscillator": 1.0}.get(d1.get("org_model"), 0.2)
    if d1.get("org_model") == "relaxation" and d1.get("org_growth"):
        ob = 0.55
    if d1.get("org_model") == "switch" and (d1.get("org_dwell") or 0.0) < 50.0:
        ob = 0.1
    if d1.get("org_model") == "oscillator" and (d1.get("org_osc_cycles", 0) < 3
                                                or d1.get("org_osc_q", 0) < 0.35):
        ob = 0.4
    if d1.get("org_model") == "oscillator" and d1.get("org_osc_q", 0) < 0.05:
        ob = 0.05                        # no periodicity at all: not an oscillator
    if d1.get("org_growth") and ob < 0.55:
        ob = 0.55                        # organism growth is never boring
    sb = C["C1_popdyn"]                  # v1 segment-level base (already gated)
    if d1["model"] == "relaxation" and not d1.get("org_growth") and sb > 0.25:
        sb = 0.25                        # segment growth w/o organism growth
    C["C1_popdyn"] = max(ob, sb)
    # C5 v2 (M3): write-only memory slightly de-rated vs read (closed-loop)
    if C["C5_memory"] > 0 and d6.get("mem_grade", 0) == 1             and d6.get("best_read") is False:
        C["C5_memory"] *= 0.85
    # C6 v2 (M1): interaction-weighted survivors (1st alive species free;
    # passengers beyond it need interaction weight — sphere-passenger fix)
    surv_int = d7.get("n_species_int", 0.0) / max(
        d1.get("n_species_seeded", 1), 1)
    pop_ret = min(d1.get("n_end", 0.0) / max(d1.get("n_start", 1.0), 1.0), 1.0)
    turn = max(d1.get("turnover", 0.0), d1.get("turnover_best", 0.0))
    C["C6_ecology"] = min(turn / 2.0, 1.0) * surv_int * pop_ret
    # C8 (M5): succession staging
    ns = d1.get("n_stages", 0)
    C["C8_succession"] = float(np.clip((ns - 1) / 2.0, 0.0, 1.0))
    return C


W_V2 = dict(C1_popdyn=0.11, C2_timescale=0.12, C3_motion=0.14,
            C4_graph=0.09, C5_memory=0.17, C6_ecology=0.19, C7_roles=0.10,
            C8_succession=0.08)


def interest_v2(C, D):
    alive = (D["d1"].get("n_end", 0) >= 2)
    s = sum(W_V2[k] * C[k] for k in W_V2)
    return float(100.0 * s * (1.0 if alive else 0.0))


def full_battery(rec, genome=None):
    """v2 battery: v1 d2-d5 verbatim, d1/d6 extended, d7 new, C8, flags."""
    rec["_tracks"] = build_tracks(rec)
    d3 = MV1.d3_spatial(rec)
    r_bond = (d3["gr"].get("r_bond") if d3.get("gr") else None)
    d4 = MV1.d4_motion(rec, r_bond=r_bond)
    d5 = MV1.d5_graph(rec, r_bond=r_bond)
    d2 = MV1.d2_timescales(rec)
    d1 = d1_population_v2(rec)
    d6 = d6_memory_v2(rec, genome)
    d7 = d7_interactions(rec, genome)
    D = dict(d1=d1, d2=d2, d3=d3, d4=d4, d5=d5, d6=d6, d7=d7)
    C = components_v2(D, rec)
    return dict(D=D, C=C, interest=interest_v2(C, D), flags=box_flag(rec))


def lean_summary(out):
    D, C = out["D"], out["C"]
    d = dict(
        interest=round(out["interest"], 2),
        C={k: round(v, 4) for k, v in C.items()},
        d1=dict(model=D["d1"].get("model"), org_model=D["d1"].get("org_model"),
                n_end=D["d1"].get("n_end"), n_org_end=D["d1"].get("n_org_end"),
                org_growth=D["d1"].get("org_growth"),
                n_stages=D["d1"].get("n_stages"),
                turn=round(D["d1"].get("turnover", 0.0), 4),
                spp=D["d1"].get("n_species_alive")),
        d2=dict(slow=D["d2"].get("tau_slow"), obs=D["d2"].get("tau_slow_obs"),
                r_emerg=D["d2"].get("r_emerg")),
        d4=dict(mv=D["d4"].get("moving_frac"), vc=D["d4"].get("v_corr"),
                role=D["d4"].get("role_div")),
        d5=dict(phase=D["d5"].get("phase"),
                churn=D["d5"].get("churn100"),
                wind=D["d5"].get("winding_max"),
                com=D["d5"].get("wind_com_speed")),
        d6=dict(cover=D["d6"].get("cover"), elong=D["d6"].get("elong"),
                rmem=D["d6"].get("r_mem"), grade=D["d6"].get("mem_grade"),
                charging=D["d6"].get("charging")),
        d7=dict(nsi=D["d7"].get("n_species_int"), w=D["d7"].get("w")),
        flags=out.get("flags"))
    return d
