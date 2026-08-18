"""cert_b3.py — B3 port-distinguishability: classify flavor from probe patches
over 20 encounters, using metrics.py LOCKED classifiers.

Protocol (pre-registered, before running):
  20 encounters = 10 A + 10 B, each: random world position, unique seed,
  sigma=2.5e-3 noise, T=300 settle, then probe patch time series sampled at
  t=300,315,...,360 tu (5 samples spanning 60 tu) at the TOTAL-ACTIVITY peak
  (the "port" location a probing agent would find). Classify with all three
  locked classifiers. PASS if >=19/20 (>=95%) for classify_full; report others.
  ALSO: two-blob worlds (one A + one B far apart), probe each blob -> 10 more
  paired classifications as a same-world check (bonus, reported).
"""
import sys, os, json, time
import numpy as np
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/blobs/flavors")
from flavors_core import default_params, run, make_state, stepper, thresholds
import metrics
from concurrent.futures import ProcessPoolExecutor

UB = -0.86756
def pair_params():
    p = default_params()
    p["k1_1"], p["k4_1"], p["Du_1"] = -1.0, 1.4, 0.65
    p["k1_2"], p["k4_2"], p["Du_2"] = -1.0 + 0.75*UB, 2.15, 0.65
    return p

def probe_series(p, spots, seed, T_settle=300.0, n_samp=5, gap_tu=15.0, noise=2.5e-3):
    """Run with noise; after settle, sample patch features at activity peak."""
    F, bg = make_state(p, L=96, arch="vvw", spots=spots)
    thr = thresholds(p, bg)
    step = stepper(p, arch="vvw")
    rng = np.random.default_rng(seed)
    dt = 0.01
    n_settle = int(T_settle/dt); n_gap = int(gap_tu/dt)
    for t in range(n_settle):
        F = step(F, dt, rng, noise)
    series = []
    peaks = []
    for k in range(n_samp):
        act = (F[0]-bg["u1"]) + (F[1]-bg["u2"])
        cy, cx = np.unravel_index(np.argmax(act), act.shape)
        series.append(metrics.patch_features(F, bg, cy, cx))
        peaks.append((int(cy), int(cx)))
        if k < n_samp-1:
            for t in range(n_gap):
                F = step(F, dt, rng, noise)
    return series, peaks, F, bg, thr

def one(job):
    idx, true_sp = job
    rng = np.random.default_rng(1000+idx)
    y, x = rng.integers(10, 86, 2)
    p = pair_params()
    series, peaks, F, bg, thr = probe_series(p, ((true_sp, float(y), float(x), 2.0, 3.0),),
                                             seed=2000+idx)
    truth = "AB"[true_sp-1]
    cf = metrics.classify_full(series)
    cw = metrics.classify_wport(series)
    cs = metrics.classify_size(series)
    osc = metrics.oscillation_check(series)
    return dict(idx=idx, truth=truth, at=[int(y), int(x)],
                full=cf, wport=cw, size=cs,
                full_ok=cf == truth, wport_ok=cw == truth, size_ok=cs == truth,
                osc_rel_std=round(osc["rel_std"], 4))

def one_pairworld(seed):
    """A and B in the same world (d=40 apart), probe each blob."""
    p = pair_params()
    rng = np.random.default_rng(seed)
    y = float(rng.integers(15, 81)); x1 = float(rng.integers(10, 40))
    x2 = (x1 + 40.0) % 96
    spots = ((1, y, x1, 2.0, 3.0), (2, y, x2, 2.0, 3.0))
    F, bg = make_state(p, L=96, arch="vvw", spots=spots)
    step = stepper(p, arch="vvw")
    dt = 0.01
    for t in range(int(300/dt)):
        F = step(F, dt, rng, 2.5e-3)
    out = []
    for truth, cx0 in (("A", x1), ("B", x2)):
        # local activity peak within r<12 of seeded site
        yy, xx = np.meshgrid(np.arange(96), np.arange(96), indexing="ij")
        rr = np.hypot(((yy-y+48)%96)-48, ((xx-cx0+48)%96)-48)
        act = (F[0]-bg["u1"]) + (F[1]-bg["u2"])
        actm = np.where(rr < 12, act, -1e9)
        cy, cx = np.unravel_index(np.argmax(actm), actm.shape)
        Fs = [metrics.patch_features(F, bg, cy, cx)]
        out.append(dict(truth=truth, full=metrics.classify_full(Fs),
                        wport=metrics.classify_wport(Fs)))
    return dict(seed=seed, results=out)

if __name__ == "__main__":
    jobs = [(i, 1 if i < 10 else 2) for i in range(20)]
    t0 = time.time(); out = []
    with ProcessPoolExecutor(max_workers=8) as ex:
        for rec in ex.map(one, jobs):
            out.append(rec); print(rec, flush=True)
    nfull = sum(r["full_ok"] for r in out)
    nwport = sum(r["wport_ok"] for r in out)
    nsize = sum(r["size_ok"] for r in out)
    print(f"ACCURACY: full {nfull}/20, wport {nwport}/20, size {nsize}/20", flush=True)
    pw = []
    with ProcessPoolExecutor(max_workers=5) as ex:
        for rec in ex.map(one_pairworld, [11, 22, 33, 44, 55]):
            pw.append(rec); print(rec, flush=True)
    npw_full = sum(x["full"] == x["truth"] for r in pw for x in r["results"])
    npw_wport = sum(x["wport"] == x["truth"] for r in pw for x in r["results"])
    print(f"PAIRWORLD: full {npw_full}/10, wport {npw_wport}/10", flush=True)
    json.dump(dict(encounters=out, acc_full=nfull/20, acc_wport=nwport/20,
                   acc_size=nsize/20, pairworld=pw,
                   pw_full=npw_full/10, pw_wport=npw_wport/10),
              open("/Users/spoho/Documents/prime/test/physim/probes/blobs/flavors/cert_b3.json","w"), indent=1)
    print("total %.0fs" % (time.time()-t0))
