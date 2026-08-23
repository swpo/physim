"""metrics_dev.py — complexity descriptor battery D (d1-d6) + interest score.
DEV copy; frozen to metrics_v1.py after ground-truth validation (see VALIDATION.md).

Input: a soup_sim.run_soup record. Output: descriptor dict + component scores +
one interest scalar. All descriptors degrade gracefully (None -> component 0).
Reuses hier_metrics (world-search program): compact_top_fit, macro_period_quality,
powerlaw_tail. Conventions: burn-in 500tu; analysis window = t >= BURN.
"""
import sys, os
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search")
from hier_metrics import (macro_period_quality, compact_top_fit, powerlaw_tail)

BURN = 500.0
REC, CREC = 5.0, 25.0
JUMP_MAX = 6.0          # px per 5tu record for identity matching
GAP_TOL = 1            # records a track may coast unmatched
MOVE_THR = 0.02        # px/tu; ~4x the measured M0 jitter floor (see VALIDATION)
VWIN = 5               # records (25tu) for velocity estimates
MEM_ABS_FLOOR = 1e-3   # mem-field amplitude floor (else channel counted unused)


# ---------------------------------------------------------------- tracking
def min_image(d, L):
    return (d + L / 2) % L - L / 2


def build_tracks(rec):
    """Greedy identity tracking over the merged per-act blob lists.
    Returns list of tracks: dict(act, t0i, pos[(k,y,x)...] unwrapped, area[])."""
    L = rec["L"]
    tracks, active = [], {}   # active: tid -> (last_k, unwrapped yx, raw yx, miss)
    nT = len(rec["t"])
    next_id = 0
    for k in range(nT):
        cur = []   # (act, y, x, area)
        for i in range(rec["na"]):
            for (y, x, a, p) in rec["blobs"][i][k]:
                cur.append((i, y, x, a))
        used = set()
        # match active tracks (per act) to current blobs
        for tid in list(active):
            lk, unw, raw, miss, act = active[tid]
            best, bd = None, JUMP_MAX * (miss + 1)
            for j, (ai, y, x, a) in enumerate(cur):
                if j in used or ai != act:
                    continue
                d = np.hypot(*min_image(np.array([y - raw[0], x - raw[1]]), L))
                if d < bd:
                    bd, best = d, j
            if best is None:
                if miss + 1 > GAP_TOL:
                    del active[tid]
                else:
                    active[tid] = (lk, unw, raw, miss + 1, act)
                continue
            used.add(best)
            ai, y, x, a = cur[best]
            step = min_image(np.array([y - raw[0], x - raw[1]]), L)
            unw2 = (unw[0] + step[0], unw[1] + step[1])
            tracks[tid]["ks"].append(k)
            tracks[tid]["yx"].append(unw2)
            tracks[tid]["area"].append(a)
            active[tid] = (k, unw2, (y, x), 0, act)
        for j, (ai, y, x, a) in enumerate(cur):
            if j in used:
                continue
            tracks.append(dict(tid=next_id, act=ai, ks=[k], yx=[(y, x)],
                               area=[a]))
            active[next_id] = (k, (y, x), (y, x), 0, ai)
            next_id += 1
    return tracks


def track_speeds(tr, dt_rec=REC, win=VWIN):
    """Speed series (px/tu) on the track, displacement over win records."""
    p = np.asarray(tr["yx"], float)
    ks = np.asarray(tr["ks"])
    if len(p) <= win:
        return np.zeros(0), np.zeros((0, 2)), ks[:0]
    dp = p[win:] - p[:-win]
    dtv = (ks[win:] - ks[:-win]) * dt_rec
    v = dp / dtv[:, None]
    return np.hypot(v[:, 0], v[:, 1]), v, ks[win:]


# ---------------------------------------------------------------- helpers
def acf_tau(x, dt, detrend=True):
    """e-folding time of the ACF after LINEAR DETREND (kills IC-relaxation
    trends; oscillations and switching survive). Censored at window/3.
    Returns (tau, censored_flag)."""
    x = np.asarray(x, float)
    n = len(x)
    if n < 8 or np.std(x) < 1e-12:
        return None, False
    if detrend:
        t = np.arange(n, dtype=float)
        A = np.vstack([t, np.ones(n)]).T
        coef, *_ = np.linalg.lstsq(A, x, rcond=None)
        x = x - A @ coef
        if np.std(x) < 1e-12:
            return None, False
    x = x - x.mean()
    acf = np.correlate(x, x, "full")[n - 1:]
    acf /= acf[0]
    cap = n // 3
    below = np.where(acf[:cap] < np.exp(-1.0))[0]
    if len(below) == 0:
        return float(cap * dt), True
    return float(below[0] * dt), False


def series_n(rec):
    """Blob-count series per act + total on the REC grid."""
    nT = len(rec["t"])
    n_i = {i: np.array([len(rec["blobs"][i][k]) for k in range(nT)])
           for i in range(rec["na"])}
    n_tot = sum(n_i.values())
    return n_i, n_tot


def window_mask(t, burn=None):
    import metrics_dev as _M
    return np.asarray(t) >= (_M.BURN if burn is None else burn)


# ---------------------------------------------------------------- descriptors
def d1_population(rec):
    """n(t) dynamics class + turnover from track births/deaths."""
    n_i, n_tot = series_n(rec)
    t = np.asarray(rec["t"]); m = window_mask(t)
    out = dict()
    if m.sum() < 20:
        return dict(model="short", r2=0.0, n_mean=float(n_tot[-1]) if len(n_tot) else 0.0,
                    n_end=float(n_tot[-1]) if len(n_tot) else 0.0, cv=0.0,
                    osc_q=0.0, turnover=0.0, births=0, deaths=0)
    x = n_tot[m].astype(float)
    fit = compact_top_fit(x, dt=REC)
    pq = macro_period_quality(x, dt=REC)
    tracks = rec["_tracks"]
    kb = int(np.argmax(m))
    nT = len(t)
    births = sum(1 for tr in tracks if tr["ks"][0] > kb)
    deaths = sum(1 for tr in tracks if tr["ks"][-1] < nT - 1 - GAP_TOL
                 and tr["ks"][0] <= nT - 1 - GAP_TOL)
    span_ktu = (t[-1] - t[kb]) / 1000.0
    nbar = max(x.mean(), 1e-9)
    dwell = None
    if fit["model"] == "switch":
        dwell = fit["params"].get("mean_dwell")
    out.update(model=fit["model"], r2=fit["r2"], n_mean=float(x.mean()),
               n_start=float(x[:5].mean()), switch_dwell=dwell,
               n_end=float(x[-1]), cv=float(x.std() / nbar),
               osc_q=float(pq["q"]), osc_period=pq["period"],
               osc_cycles=float(pq["n_cycles"]),
               births=births, deaths=deaths,
               turnover=float((births + deaths) / nbar / max(span_ktu, 1e-9)),
               n_species_alive=int(sum(1 for i in n_i
                                       if n_i[i][-3:].mean() > 0.34)),
               n_species_seeded=int(len(set(rec["species_seeded"]))))
    return out


# amplitude gates: an observable enters d2 only if it REALLY fluctuates
# (detrended sd floors; else frozen worlds score long ACF times on noise).
AMP_GATE = dict(count=0.15, mass_cv=1.5e-3, cover_cv=1e-2,
                speed=0.005, bond=0.3, angle=0.05)


def _resid_sd(x):
    x = np.asarray(x, float); n = len(x)
    if n < 8:
        return 0.0
    t = np.arange(n, dtype=float)
    A = np.vstack([t, np.ones(n)]).T
    c, *_ = np.linalg.lstsq(A, x, rcond=None)
    return float(np.std(x - A @ c))


def d2_timescales(rec):
    """ACF e-folding times across coarse observables; hierarchy ratios."""
    t = np.asarray(rec["t"]); m = window_mask(t)
    ct = np.asarray(rec["ct"]); cm = window_mask(ct)
    n_i, n_tot = series_n(rec)
    obs = {"n_tot": (n_tot[m], REC, "count")}
    for i in n_i:
        obs[f"n{i}"] = (n_i[i][m], REC, "count")
        obs[f"mass{i}"] = (np.asarray(rec["mass"][i])[m], REC, "mass_cv")
    for i in range(rec["na"]):
        obs[f"np{i}"] = (np.array([p["n"] for p in rec["patches"][i]])[cm],
                         CREC, "count")
        obs[f"cover{i}"] = (np.array([p["cover"]
                                      for p in rec["patches"][i]])[cm],
                            CREC, "cover_cv")
    gate_kind = {"_speed_series": "speed", "_bond_series": "bond",
                 "_bondangle_series": "angle"}
    for k in gate_kind:
        if k in rec and len(rec[k][0]) > 8:
            obs[k.strip("_")] = (rec[k][0], rec[k][1], gate_kind[k])
    taus, amps = {}, {}
    for name, (x, dt, kind) in obs.items():
        sd = _resid_sd(x)
        thr = AMP_GATE[kind]
        if kind.endswith("_cv"):
            sd = sd / max(abs(np.mean(x)), 1e-9)
        elif kind == "bond":
            thr = max(AMP_GATE["bond"], 0.05 * abs(np.mean(x)))
        amps[name] = round(sd, 5)
        if sd < thr:
            continue
        tau, cens = acf_tau(x, dt)
        # oscillatory observables: the PERIOD is the emergent timescale
        # (ACF e-fold underestimates a clean oscillation's slowness)
        pq = macro_period_quality(np.asarray(x, float)
                                  - np.poly1d(np.polyfit(
                                      np.arange(len(x)), x, 1))(
                                      np.arange(len(x))), dt=dt)
        if pq["period"] and pq["q"] >= 0.4 and pq["n_cycles"] >= 3:
            per = pq["period"]
            if tau is None or per > tau:
                tau, cens = per, False
        if tau is not None:
            taus[name] = (round(tau, 1), bool(cens))
    if not taus:
        return dict(taus={}, amps=amps, tau_slow=None, tau_fast=None,
                    tau_genome_max=float(max(rec["taus"])),
                    r_spread=1.0, r_emerg=1.0)
    vals = [v[0] for v in taus.values()]
    tau_slow, tau_fast = max(vals), min(vals)
    slow_name = [k for k, v in taus.items() if v[0] == tau_slow][0]
    tau_gen = max(rec["taus"])
    return dict(taus=taus, amps=amps, tau_slow=tau_slow, tau_fast=tau_fast,
                tau_slow_obs=slow_name, tau_genome_max=float(tau_gen),
                censored=taus[slow_name][1],
                r_spread=float(tau_slow / max(tau_fast, 1e-9)),
                r_emerg=float(tau_slow / max(tau_gen, 1e-9)))


def d3_spatial(rec):
    """Patch statistics: stability/coarsening + end-state pair order g(r)."""
    ct = np.asarray(rec["ct"]); cm = window_mask(ct)
    np_tot = None
    for i in range(rec["na"]):
        v = np.array([p["n"] for p in rec["patches"][i]])
        np_tot = v if np_tot is None else np_tot + v
    x = np_tot[cm].astype(float)
    out = dict(np_mean=float(x.mean()) if len(x) else 0.0,
               np_end=float(x[-1]) if len(x) else 0.0)
    # coarsening: log-log slope if count declines >= 1.5x
    if len(x) > 10 and x[0] > 0 and x[:3].mean() >= 1.5 * max(x[-3:].mean(), .1):
        tt = ct[cm] - ct[cm][0] + CREC
        good = x > 0
        A = np.vstack([np.log(tt[good]), np.ones(good.sum())]).T
        (sl, b), *_ = np.linalg.lstsq(A, np.log(x[good]), rcond=None)
        pred = A @ np.array([sl, b])
        r2 = 1 - ((np.log(x[good]) - pred) ** 2).sum() / max(
            ((np.log(x[good]) - np.log(x[good]).mean()) ** 2).sum(), 1e-12)
        out.update(coarsen_slope=float(sl), coarsen_r2=float(r2))
    else:
        out.update(coarsen_slope=0.0, coarsen_r2=0.0)
    # patch-size tail pooled over last 20 coarse frames
    sizes = []
    for i in range(rec["na"]):
        for p in rec["patches"][i][-20:]:
            sizes += p["sizes"]
    out["size_tail"] = powerlaw_tail(sizes)
    # end-window g(r) from blob positions (REC grid, last 1000tu)
    t = np.asarray(rec["t"])
    ksel = np.where(t >= t[-1] - 1000.0)[0][::5]
    L = rec["L"]
    dists = []
    npair_frames = 0
    for k in ksel:
        pos = []
        for i in range(rec["na"]):
            pos += [(b[0], b[1]) for b in rec["blobs"][i][k]]
        pos = np.asarray(pos)
        if len(pos) < 2:
            continue
        npair_frames += 1
        d = pos[:, None, :] - pos[None, :, :]
        d = np.hypot(min_image(d[..., 0], L), min_image(d[..., 1], L))
        iu = np.triu_indices(len(pos), 1)
        dists += list(d[iu])
    out["gr"] = gr = pair_order(np.asarray(dists), L,
                                nframes=max(npair_frames, 1))
    return out


def pair_order(dists, L, nframes=1, rmax=40.0, dr=1.0, bond_rmax=28.0):
    """g(r) + first-peak order metric + bond cutoff estimate.
    Bond peak search restricted to r <= bond_rmax: certified d* wells and
    first binding shells all sit below ~26 px; peaks beyond that are the
    mean-spacing shell of a dilute repulsive gas (measured on gt_xv)."""
    if len(dists) < 10:
        return dict(peak=None, peak_h=0.0, r_bond=None, n=int(len(dists)))
    bins = np.arange(2.0, rmax + dr, dr)
    h, edges = np.histogram(dists, bins=bins)
    rc = 0.5 * (edges[1:] + edges[:-1])
    area = L * L
    n_pairs = len(dists) / nframes
    rho_pair = n_pairs / area
    g = h / nframes / (2 * np.pi * rc * dr) / max(rho_pair, 1e-12)
    g = np.convolve(g, np.ones(3) / 3, mode="same")
    sel = rc <= bond_rmax
    ipk = int(np.argmax(g[sel]))
    peak_h = float(g[sel][ipk])
    if peak_h < 1.5:
        return dict(peak=None, peak_h=peak_h, r_bond=None, n=int(len(dists)))
    # first minimum after the peak
    imin = ipk
    for j in range(ipk + 1, len(g) - 1):
        if g[j] <= g[j + 1]:
            imin = j
            break
    else:
        imin = min(ipk + 8, len(g) - 1)
    return dict(peak=float(rc[ipk]), peak_h=peak_h,
                r_bond=float(min(rc[imin], bond_rmax)), n=int(len(dists)))


def d4_motion(rec, r_bond=None):
    """Moving fraction, speeds, neighbor velocity correlation, net transport."""
    tracks = rec["_tracks"]
    t = np.asarray(rec["t"]); L = rec["L"]
    kb = int(np.argmax(window_mask(t)))
    speeds_all, disp_net, disp_path = [], np.zeros(2), 0.0
    vel_by_frame = {}   # k -> list of (y, x, vy, vx, act)
    for tr in tracks:
        sp, v, ks = track_speeds(tr)
        sel = ks >= kb
        if sel.sum() == 0:
            continue
        speeds_all += list(sp[sel])
        p = np.asarray(tr["yx"], float)
        k0 = max(np.searchsorted(np.asarray(tr["ks"]), kb), 0)
        if len(p) - k0 > VWIN:
            disp_net += p[-1] - p[k0]
            disp_path += np.abs(np.diff(p[k0:], axis=0)).sum()
        raw = np.asarray(tr["yx"], float)
        for j, kk in enumerate(ks):
            if kk < kb:
                continue
            idx = j + VWIN
            vel_by_frame.setdefault(int(kk), []).append(
                (raw[idx][0] % L, raw[idx][1] % L, v[j][0], v[j][1], tr["act"]))
    speeds_all = np.asarray(speeds_all)
    if len(speeds_all) == 0:
        return dict(moving_frac=0.0, v_mean=0.0, v_p90=0.0, v_corr=0.0,
                    transport=0.0, speed_series=None)
    moving = speeds_all > MOVE_THR
    # neighbor velocity correlation among moving blobs
    rb = r_bond or 22.0
    cos_list = []
    for k, rows in vel_by_frame.items():
        R = np.array([r[:4] for r in rows
                      if np.hypot(r[2], r[3]) > MOVE_THR], float)
        if len(R) < 2:
            continue
        dm = R[:, None, :2] - R[None, :, :2]
        dd = np.hypot(min_image(dm[..., 0], L), min_image(dm[..., 1], L))
        V = R[:, 2:4]
        nv = np.linalg.norm(V, axis=1)
        cosm = (V @ V.T) / np.clip(nv[:, None] * nv[None, :], 1e-12, None)
        iu = np.triu_indices(len(R), 1)
        sel = dd[iu] <= rb * 1.5
        cos_list += list(cosm[iu][sel])
    # mean-speed series for d2 (on REC grid)
    nT = len(t)
    sser = np.zeros(nT); cnt = np.zeros(nT)
    for k, rows in vel_by_frame.items():
        sser[k] = np.mean([np.hypot(r[2], r[3]) for r in rows])
        cnt[k] = len(rows)
    sel = cnt > 0
    rec["_speed_series"] = (sser[sel], REC)
    # role diversity: do the SPECIES behave differently? (division of labor)
    per_act = {}
    for tr in tracks:
        sp, v, ks = track_speeds(tr)
        sel = ks >= kb
        if sel.sum() < 8:
            continue
        a = per_act.setdefault(tr["act"], dict(sp=[], nrec=0))
        a["sp"] += list(sp[sel]); a["nrec"] += int(sel.sum())
    acts_alive = [i for i, a in per_act.items() if a["nrec"] >= 20]
    role_div = 0.0
    per_act_v = {i: float(np.mean(per_act[i]["sp"])) for i in acts_alive}
    per_act_mv = {i: float(np.mean(np.asarray(per_act[i]["sp"]) > MOVE_THR))
                  for i in acts_alive}
    if len(acts_alive) >= 2:
        vs = np.array([per_act_v[i] for i in acts_alive])
        ms = np.array([per_act_mv[i] for i in acts_alive])
        role_div = max(float(ms.max() - ms.min()),
                       float((vs.max() - vs.min()) / (vs.max() + 0.02)))
    return dict(moving_frac=float(moving.mean()),
                v_mean=float(speeds_all.mean()),
                v_p90=float(np.percentile(speeds_all, 90)),
                v_corr=float(np.mean(cos_list)) if cos_list else 0.0,
                v_corr_n=len(cos_list),
                transport=float(np.hypot(*disp_net) / max(disp_path, 1e-9)),
                per_act_v=per_act_v, per_act_mvfrac=per_act_mv,
                role_div=role_div)


def d5_graph(rec, r_bond=None):
    """Bond-network churn on the CREC grid using track identities."""
    tracks = rec["_tracks"]
    t = np.asarray(rec["t"]); L = rec["L"]
    kb = int(np.argmax(window_mask(t)))
    stride = int(round(CREC / REC))
    frames = range(kb, len(t), stride)
    pos_by_frame = {k: [] for k in frames}
    for tr in tracks:
        ks = np.asarray(tr["ks"]); raw = np.asarray(tr["yx"], float)
        for j, kk in enumerate(ks):
            if kk in pos_by_frame:
                pos_by_frame[kk].append((tr["tid"], raw[j][0] % L,
                                         raw[j][1] % L))
    rb = float(np.clip(r_bond if r_bond else 16.0, 10.0, 25.0)) * 1.5
    rb_out = 1.15 * rb        # hysteresis: leave-threshold (kills cutoff flicker)
    edges_prev, created, destroyed, e_counts = None, 0, 0, []
    n_frames = 0
    bser = []
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
            created += len(E - edges_prev)
            destroyed += len(edges_prev - E)
            n_frames += 1
        e_counts.append(len(E))
        bser.append(len(E))
        edges_prev = E
    e_mean = float(np.mean(e_counts)) if e_counts else 0.0
    churn100 = ((created + destroyed) / 2 / max(e_mean, 1e-9) /
                max(n_frames, 1) * (100.0 / CREC)) if e_mean > 0 else 0.0
    n_i, n_tot = series_n(rec)
    nbar = float(n_tot[window_mask(t)].mean()) if window_mask(t).sum() else 0.0
    coord = 2 * e_mean / nbar if nbar >= 0.5 else 0.0
    if e_mean < 0.5 or coord < 0.15:
        phase = "gas"
    elif churn100 < 0.02:
        phase = "frozen"
    elif churn100 <= 1.2:
        phase = "liquid"
    else:
        phase = "flicker"
    rec["_bond_series"] = (np.asarray(bser, float), CREC)
    # rotation detector: scan SUSTAINED pairs, keep max |winding| (unwrapped
    # relative angle; a rotor winds monotonically, noise pairs do not).
    life = {}
    for k in frames:
        rows = pos_by_frame[k]
        if len(rows) < 2:
            continue
        ids = np.array([r[0] for r in rows])
        P = np.array([[r[1], r[2]] for r in rows], float)
        dm = P[:, None, :] - P[None, :, :]
        dd = np.hypot(min_image(dm[..., 0], L), min_image(dm[..., 1], L))
        iu = np.triu_indices(len(rows), 1)
        for a, b in zip(*iu):
            if dd[a, b] <= rb:
                life.setdefault((min(ids[a], ids[b]), max(ids[a], ids[b])),
                                []).append(k)
    from hier_metrics import macro_period_quality as _mpq
    tr_by_id = {tr["tid"]: tr for tr in tracks}
    best = dict(winding=0.0, ang_period=None, ang_q=0.0, pair=None,
                sep=None, n_pts=0, com_speed=None)
    cands = sorted(life.items(), key=lambda z: -len(z[1]))[:60]
    for (ia, ib), ks_e in cands:
        if len(ks_e) < 15:
            continue
        ta, tb = tr_by_id[ia], tr_by_id[ib]
        ka = {k: j for j, k in enumerate(ta["ks"])}
        kbm = {k: j for j, k in enumerate(tb["ks"])}
        th, seps, coms, tts = [], [], [], []
        for k in ks_e:
            if k in ka and k in kbm:
                pa = np.asarray(ta["yx"][ka[k]])
                pb = np.asarray(tb["yx"][kbm[k]])
                d = min_image(pa - pb, L)
                th.append(np.arctan2(d[0], d[1]))
                seps.append(float(np.hypot(*d)))
                coms.append(pb + d / 2)     # unwrapped COM (b-frame)
                tts.append(k * REC)
        if len(th) < 15:
            continue
        th = np.unwrap(np.asarray(th))
        # winding = angular RANGE (direction-flipping rotors still wind)
        w = float((th.max() - th.min()) / (2 * np.pi))
        coms = np.asarray(coms)
        dur = max(tts[-1] - tts[0], 1e-9)
        com_speed = float(np.hypot(*(coms[-1] - coms[0])) / dur)
        if w > best["winding"]:
            pq = _mpq(np.cos(th), dt=CREC)
            best = dict(winding=w, ang_period=pq["period"],
                        ang_q=float(pq["q"]), pair=(int(ia), int(ib)),
                        pair_acts=(tr_by_id[ia]["act"], tr_by_id[ib]["act"]),
                        sep=float(np.median(seps)), n_pts=len(th),
                        com_speed=com_speed)
            rec["_bondangle_series"] = (np.cos(th), CREC)
    return dict(e_mean=e_mean, coord=float(coord), churn100=float(churn100),
                created=created, destroyed=destroyed, phase=phase,
                r_bond_used=rb, winding_max=best["winding"],
                wind_ang_period=best["ang_period"],
                wind_ang_q=best["ang_q"], wind_pair_acts=best.get("pair_acts"),
                wind_sep=best["sep"], wind_com_speed=best["com_speed"])


def d6_memory(rec):
    """Realized memory-channel structure: coverage, elongation, persistence."""
    memf = rec.get("memf", {})
    if not memf:
        return dict(has_mem=False)
    ct = np.asarray(rec["ct"]); cm = window_mask(ct)
    from scipy import ndimage
    out = dict(has_mem=True, chans={})
    for c, stack in memf.items():
        S = np.asarray(stack)[cm]
        if len(S) < 4:
            continue
        A = np.abs(S)
        amax = float(np.percentile(A, 99.5))
        if amax < MEM_ABS_FLOOR:
            out["chans"][int(c)] = dict(used=False, amax=amax)
            continue
        thr = 0.25 * amax
        cover = float((A > thr).mean())
        # elongation of patches in the LAST frame
        lab, n = ndimage.label(A[-1] > thr)
        elongs, wts = [], []
        for j in range(1, n + 1):
            ys, xs = np.nonzero(lab == j)
            if len(ys) < 4:
                continue
            cov = np.cov(np.vstack([ys, xs]))
            ev = np.linalg.eigvalsh(cov)
            elongs.append(1.0 - ev[0] / max(ev[1], 1e-12))
            wts.append(len(ys))
        elong = float(np.average(elongs, weights=wts)) if elongs else 0.0
        # persistence: field-pattern ACF in time -> e-fold vs channel tau
        v = S.reshape(len(S), -1)
        v = v - v.mean(axis=1, keepdims=True)
        norm = np.linalg.norm(v, axis=1)
        okf = norm > 1e-9
        Cts = []
        max_lag = len(S) // 2
        for lag in range(1, max_lag):
            a, b = v[:-lag], v[lag:]
            na_, nb_ = norm[:-lag], norm[lag:]
            sel = (na_ > 1e-9) & (nb_ > 1e-9)
            if sel.sum() < 3:
                break
            Cts.append(float(np.mean((a[sel] * b[sel]).sum(axis=1) /
                                     (na_[sel] * nb_[sel]))))
        tau_obs, cens = None, False
        if Cts:
            Cts = np.asarray(Cts)
            below = np.where(Cts < np.exp(-1.0))[0]
            if len(below):
                tau_obs = float((below[0] + 1) * CREC)
            else:
                tau_obs, cens = float(max_lag * CREC), True
        tau_chan = float(rec["taus"][int(c)])
        out["chans"][int(c)] = dict(
            used=True, amax=amax, cover=cover, elong=elong,
            tau_obs=tau_obs, tau_chan=tau_chan, censored=cens,
            r_mem=float(tau_obs / tau_chan) if tau_obs else None)
    used = [v for v in out["chans"].values() if v.get("used")]
    if used:
        bc = max(used, key=lambda v: v["cover"] * (0.2 + v["elong"]))
        out.update(cover=bc["cover"], elong=bc["elong"],
                   r_mem=bc.get("r_mem"), tau_obs=bc.get("tau_obs"),
                   censored=bc.get("censored", False))
    else:
        out["has_mem"] = False
    return out


# ---------------------------------------------------------------- interest
def components(D, rec):
    """Map descriptors to [0,1] components (v0 weights; see VALIDATION.md)."""
    d1, d2, d3, d4, d5, d6 = (D["d1"], D["d2"], D["d3"], D["d4"], D["d5"],
                              D["d6"])
    C = {}
    # C1 population dynamics class
    base = {"constant": 0.05, "short": 0.0, "relaxation": 0.25,
            "switch": 0.7, "oscillator": 1.0}.get(d1["model"], 0.2)
    if d1["model"] == "relaxation" and d1.get("n_end", 0) > 1.15 * d1.get(
            "n_start", d1.get("n_mean", 1)):
        base = 0.55                      # growing-saturating (logistic-like)
    if d1["model"] == "switch" and (d1.get("switch_dwell") or 0.0) < 50.0:
        base = 0.1                       # flicker, not a two-state process
    if d1["model"] == "oscillator" and (d1.get("osc_cycles", 0) < 3
                                        or d1.get("osc_q", 0) < 0.35):
        base = 0.4
    C["C1_popdyn"] = base
    # C2 emergent timescale (denominator floored at 2*CREC: grid resolution)
    denom = max(d2.get("tau_genome_max") or 0.0, 2 * CREC)
    r = (d2.get("tau_slow") or 0.0) / denom
    C["C2_timescale"] = float(np.clip(np.log10(max(r, 0.1)) / 1.5, 0.0, 1.0))
    # C3 motion structure: translation OR persistent rotation
    vc = max(d4.get("v_corr", 0.0), 0.0)
    trans = d4["moving_frac"] * (0.6 + 0.4 * vc)
    wind = d5.get("winding_max", 0.0)
    cs = d5.get("wind_com_speed")
    rot = 0.0
    # real rotation: >=1.5 turns of a pair whose COM is parked (else it is
    # a curving traveling bond and trans already counts it)
    if wind >= 1.5 and cs is not None and cs < 0.03:
        rot = 0.5 + 0.3 * min(wind / 6.0, 1.0) \
            + 0.2 * (1.0 if d5.get("wind_ang_q", 0) >= 0.5 else 0.0)
    C["C3_motion"] = max(trans, rot)
    # C4 graph churn — graded (log-tent over churn100), phase kept as label
    if d5["phase"] == "gas":
        C["C4_graph"] = 0.1 if d5["e_mean"] > 0 else 0.0
    else:
        c = max(d5["churn100"], 0.0)
        if c <= 0.005:
            v = 0.25
        elif c < 0.05:
            v = 0.25 + 0.75 * (np.log10(c / 0.005) / 1.0)
        elif c <= 1.2:
            v = 1.0
        elif c <= 4.0:
            v = 1.0 - 0.7 * (np.log10(c / 1.2) / np.log10(4.0 / 1.2))
        else:
            v = 0.3
        C["C4_graph"] = float(np.clip(v, 0.0, 1.0))
    # C5 memory
    if d6.get("has_mem") and d6.get("cover", 0) > 0.01:
        pers = min((d6.get("r_mem") or 0.0), 2.0) / 2.0
        C["C5_memory"] = min(d6["cover"] / 0.05, 1.0) * (
            0.4 * d6.get("elong", 0.0) + 0.3 + 0.3 * pers)
    else:
        C["C5_memory"] = 0.0
    # C6 ecology: turnover with survivors and retained population
    surv = d1.get("n_species_alive", 0) / max(d1.get("n_species_seeded", 1), 1)
    pop_ret = min(d1.get("n_end", 0.0) / max(d1.get("n_start", 1.0), 1.0), 1.0)
    C["C6_ecology"] = min(d1.get("turnover", 0.0) / 2.0, 1.0) * surv * pop_ret
    # C7 division of labor: species behave differently AND >=2 species persist
    if (d1.get("n_species_alive", 0) >= 2):
        C["C7_roles"] = d4.get("role_div", 0.0)
    else:
        C["C7_roles"] = 0.0
    return C


W_V0 = dict(C1_popdyn=0.12, C2_timescale=0.13, C3_motion=0.15,
            C4_graph=0.10, C5_memory=0.18, C6_ecology=0.20, C7_roles=0.12)


def interest(C, D):
    alive = (D["d1"].get("n_end", 0) >= 2)
    s = sum(W_V0[k] * C[k] for k in W_V0)
    return float(100.0 * s * (1.0 if alive else 0.0))


def full_battery(rec):
    """Run d1-d6 + score on a soup record. Mutates rec with _tracks etc."""
    rec["_tracks"] = build_tracks(rec)
    d3 = d3_spatial(rec)
    r_bond = (d3["gr"].get("r_bond") if d3.get("gr") else None)
    d4 = d4_motion(rec, r_bond=r_bond)
    d5 = d5_graph(rec, r_bond=r_bond)
    d2 = d2_timescales(rec)     # after d4/d5 attach series
    d1 = d1_population(rec)
    d6 = d6_memory(rec)
    D = dict(d1=d1, d2=d2, d3=d3, d4=d4, d5=d5, d6=d6)
    C = components(D, rec)
    return dict(D=D, C=C, interest=interest(C, D))
