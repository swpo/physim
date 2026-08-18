"""metrics.py — M3 FLAVORS locked measurement + classification module.

LOCKED BEFORE CERTIFICATION (see LOCK stamp below). Any post-cert edit
invalidates the certificate.

World (pair "MAXC", arch vvw — 5 fields u1,v1,u2,v2,w):
  du_i/dt = Du lap u_i + lam u_i - u_i^3 - k3 v_i - k4_i w + k1_i
  dv_i/dt = (u_i - v_i)/tau + Dv lap v_i
  dw/dt   = ((u1+u2)/2 - w)/theta + Dw lap w
  lam=2, k3=1, tau=3, theta=0.7, Dv=1, Dw=20, Du_1=Du_2=0.65, L=96, dt=0.01
  species A: k1_1=-1.0,     k4_1=1.4
  species B: k1_2=-1.65067, k4_2=2.15    (iso-background line, ub=-0.86756)

Blob identity is MEASURED (threshold + connected components), never a state var.

Classifiers (constants frozen from clean lone-blob calibration, calib_portraits
+ calibrate() output stored in classifier_calib.json):
  classify_full : compare activator-channel patch amplitudes (du1 vs du2).
  classify_wport: w-field-only — w is the ONLY field shared between species,
                  i.e. the physical "port" other blobs can feel. Uses the
                  w-bump half-width footprint (A broad, B narrow).
  classify_size : field-agnostic size — total-activity half-width footprint.
Input to all: a probe-patch TIME SERIES (list of feature dicts over >=3 samples
spanning >=30 tu); features are time-averaged before thresholding.
"""
import numpy as np
from scipy import ndimage

LOCK = "2026-02-19 pre-certification lock (M3 flavors searcher)"

# ---- frozen calibration constants (geometric-mean midpoints, clean lone runs)
W_HALFWIDTH_STAR = 72.7393   # frozen by probe13_freeze.py
ACT_HALFWIDTH_STAR = 55.0000   # frozen by probe13_freeze.py

PATCH_HW = 2          # 5x5 patch
WIN_R = 10.5          # footprint window radius (px)


def patch_features(F, bg, cy, cx, L=96):
    """Features of a probe patch centred (cy,cx). F=(u1,v1? order: u1,u2,v1,v2,w)."""
    u1b, u2b, wb = bg["u1"], bg["u2"], bg["w"]
    yy, xx = np.meshgrid(np.arange(L), np.arange(L), indexing="ij")
    rr = np.hypot(((yy - cy + L/2) % L) - L/2, ((xx - cx + L/2) % L) - L/2)
    P = rr <= PATCH_HW + 0.6
    win = rr <= WIN_R
    du1 = float((F[0][P] - u1b).mean())
    du2 = float((F[1][P] - u2b).mean())
    dw = F[4] - wb
    dwc = float(dw[P].mean())
    act = (F[0] - u1b) + (F[1] - u2b)
    actc = float(act[P].mean())
    w_hw = int(((dw > 0.5 * dwc) & win).sum()) if dwc > 0 else 0
    act_hw = int(((act > 0.5 * actc) & win).sum()) if actc > 0 else 0
    return dict(du1=du1, du2=du2, dw_center=dwc, act_center=actc,
                w_halfwidth=w_hw, act_halfwidth=act_hw)


def _avg(series):
    keys = series[0].keys()
    return {k: float(np.mean([s[k] for s in series])) for k in keys}


def classify_full(series):
    """Activator-channel amplitudes: A iff channel-1 patch amplitude dominates."""
    f = _avg(series)
    return "A" if f["du1"] >= f["du2"] else "B"


def classify_wport(series, wstar=None):
    """w-only (shared-field port): A iff w-bump halfwidth footprint >= W*."""
    w = W_HALFWIDTH_STAR if wstar is None else wstar
    f = _avg(series)
    return "A" if f["w_halfwidth"] >= w else "B"


def classify_size(series, astar=None):
    """Field-agnostic size: A iff total-activity halfwidth footprint >= A*."""
    a = ACT_HALFWIDTH_STAR if astar is None else astar
    f = _avg(series)
    return "A" if f["act_halfwidth"] >= a else "B"


def oscillation_check(series, key="act_center"):
    """Temporal variability of patch amplitude (blobs here are non-oscillatory;
    reported as honest negative — frequency is NOT a usable signature)."""
    x = np.array([s[key] for s in series])
    return dict(mean=float(x.mean()), std=float(x.std()),
                rel_std=float(x.std() / max(abs(x.mean()), 1e-12)))


# ---- blob census (identity = connected components; per-species) -------------
def census(F, thr, L=96, min_area=8):
    """Count blobs per species and their centroids/areas/peaks."""
    out = {}
    for i, name in ((0, "A"), (1, "B")):
        m = F[i] > thr[i]
        lab, nc = ndimage.label(m)
        blobs = []
        for j in range(1, nc + 1):
            mj = lab == j
            a = int(mj.sum())
            if a < min_area:
                continue
            cy, cx = ndimage.center_of_mass(mj)
            blobs.append(dict(area=a, cy=float(cy), cx=float(cx),
                              peak=float(F[i][mj].max())))
        out[name] = blobs
    return out


def excess_mass(F, bg, L=96):
    """Integral of (u_i - bg_i): conservation bookkeeping across encounters."""
    return dict(A=float((F[0] - bg["u1"]).sum()), B=float((F[1] - bg["u2"]).sum()))


def sep_periodic(c1, c2, L=96):
    d = np.array(c1, float) - np.array(c2, float)
    d = (d + L / 2) % L - L / 2
    return float(np.hypot(*d))
