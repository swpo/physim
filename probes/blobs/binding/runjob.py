"""Flexible job runner: python runjob.py '<json spec>'
Kinds: single (B1), pair (bond curve, optional noise/angle), multi (3-4 blobs),
escape (noise at d*), refine (dx=0.5 pair).
Writes JSON to spec["out"]; optionally saves field snapshots to spec["snap"] (npz).
"""
import sys, time, json
import numpy as np
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/blobs/binding")
from sim import run, relax_single, pair_experiment, make_stamped_world, homog_u0, pair_sep, min_image

spec = json.loads(sys.argv[1])
p = spec["params"]          # dial dict (Dv, tau, k3, k4, ...)
kind = spec["kind"]
out_path = spec["out"]
t0 = time.time()

def save(obj):
    obj["runtime_s"] = round(time.time() - t0, 1)
    obj["spec"] = spec
    json.dump(obj, open(out_path, "w"))
    print(json.dumps({k: obj[k] for k in obj if k not in ("series","seps","frames_kept","angles")})[:400])

if kind == "single":
    L = spec.get("L", 64.0); dx = spec.get("dx", 1.0); T = spec.get("T", 10000.0)
    noise = spec.get("noise", 0.0); seed = spec.get("seed", 0)
    series = []
    def cb(t, u, v, w, blobs):
        if len(blobs) == 1:
            b = blobs[0]
            series.append([round(t,1), b["area_px"], round(b["peak"],4), round(b["y"],3), round(b["x"],3)])
        else:
            series.append([round(t,1), -len(blobs), 0, 0, 0])
    r = run(L=L, dx=dx, T=T, bumps=[(L/2, L/2)], rec_tu=spec.get("rec_tu", 25.0),
            noise=noise, seed=seed, callback=cb, **p)
    ok = r["status"] == "ok"
    ncomps = [1 if s[1] > 0 else -s[1] for s in series]
    areas = [s[1] for s in series if s[1] > 0]
    disp = None
    if ok and ncomps[-1] == 1 and len(series) > 4:
        cy = [s[3] for s in series if s[1] > 0]; cx = [s[4] for s in series if s[1] > 0]
        h = len(cy)//2
        disp = round(float(np.hypot(min_image(cy[-1]-cy[h], L), min_image(cx[-1]-cx[h], L))), 3)
    save(dict(status=r["status"], ncomp_end=ncomps[-1] if ncomps else 0,
              ncomp_max=max(ncomps) if ncomps else 0,
              area_end=areas[-1] if areas else 0,
              area_med=float(np.median(areas)) if areas else 0,
              disp_2ndhalf=disp, series=series))

elif kind == "pair":
    L = spec.get("L", 96.0); dx = spec.get("dx", 1.0); T = spec.get("T", 4000.0)
    d0 = spec["d0"]; noise = spec.get("noise", 0.0); seed = spec.get("seed", 0)
    z = np.load(spec["stamp"])
    stamp = dict(du=z["du"], dv=z["dv"], dw=z["dw"])
    if dx != 1.0:
        # stamp was made at dx=1; regenerate at this dx by zoom
        from scipy import ndimage as ndi
        f = 1.0/dx
        stamp = {k: ndi.zoom(stamp[k], f, order=3) for k in stamp}
    u0h = homog_u0(p.get("lam",2.0), p.get("k1",-0.7), p.get("k3",1.0), p.get("k4",1.5))
    yc = L/2
    u, v, w = make_stamped_world(L, dx, u0h, stamp, [(yc, L/2 - d0/2), (yc, L/2 + d0/2)])
    seps = []
    snaps = {}
    snap_ts = set(spec.get("snap_ts", []))
    def cb(t, uu, vv, ww, blobs):
        if len(blobs) == 2:
            s, (dy, dxx) = pair_sep(blobs[0], blobs[1], L)
            ang = float(np.arctan2(dy, dxx))
            seps.append([round(t,1), round(s,4), 2, round(ang,4)])
        else:
            seps.append([round(t,1), None, len(blobs), None])
        if snap_ts:
            close = [st for st in snap_ts if abs(st - t) < 1e-6]
            for st in close:
                snaps[st] = uu.copy()
    r = run(L=L, dx=dx, T=T, u=u, v=v, w=w, noise=noise, seed=seed,
            rec_tu=spec.get("rec_tu", 10.0), callback=cb, **p)
    if spec.get("snap") and snaps:
        np.savez_compressed(spec["snap"], **{f"t{int(k)}": vv for k, vv in snaps.items()},
                            u0=u0h)
    ns = [s[2] for s in seps]
    save(dict(status=r["status"], d0=d0, ncomp_min=min(ns), ncomp_max=max(ns),
              sep_end=seps[-1][1], ncomp_end=ns[-1], seps=seps[::spec.get("thin",3)] + [seps[-1]]))

elif kind == "multi":
    L = spec.get("L", 96.0); dx = spec.get("dx", 1.0); T = spec.get("T", 3000.0)
    noise = spec.get("noise", 0.0); seed = spec.get("seed", 0)
    z = np.load(spec["stamp"])
    stamp = dict(du=z["du"], dv=z["dv"], dw=z["dw"])
    u0h = homog_u0(p.get("lam",2.0), p.get("k1",-0.7), p.get("k3",1.0), p.get("k4",1.5))
    pos = [tuple(q) for q in spec["positions"]]
    u, v, w = make_stamped_world(L, dx, u0h, stamp, pos)
    track = []
    snaps = {}
    snap_ts = sorted(spec.get("snap_ts", []))
    def cb(t, uu, vv, ww, blobs):
        track.append([round(t,1), len(blobs),
                      [[round(b["y"],2), round(b["x"],2), b["area_px"]] for b in blobs]])
        for st in snap_ts:
            if abs(st - t) < 1e-6:
                snaps[st] = uu.copy()
    r = run(L=L, dx=dx, T=T, u=u, v=v, w=w, noise=noise, seed=seed,
            rec_tu=spec.get("rec_tu", 20.0), callback=cb, **p)
    if spec.get("snap") and snaps:
        np.savez_compressed(spec["snap"], **{f"t{int(k)}": vv for k, vv in snaps.items()}, u0=u0h)
    ns = [s[1] for s in track]
    # final pairwise separations
    fin = track[-1][2]
    dists = []
    for i in range(len(fin)):
        for j in range(i+1, len(fin)):
            dy = min_image(fin[i][0]-fin[j][0], L); dxx = min_image(fin[i][1]-fin[j][1], L)
            dists.append(round(float(np.hypot(dy,dxx)),2))
    save(dict(status=r["status"], n_start=len(pos), ncomp_end=ns[-1],
              ncomp_min=min(ns), ncomp_max=max(ns), final_seps=sorted(dists),
              track=track[::spec.get("thin",5)] + [track[-1]]))

elif kind == "escape":
    # prepare bound pair by relaxing at d0 noiselessly for T_prep, then switch noise on
    L = spec.get("L", 96.0); dx = spec.get("dx", 1.0)
    d0 = spec["d0"]; noise = spec["noise"]; seed = spec.get("seed", 0)
    T_prep = spec.get("T_prep", 500.0); T_max = spec.get("T_max", 4000.0)
    band = spec.get("band", 5.0)   # escape when |sep-dstar| > band or ncomp != 2
    dstar = spec.get("dstar", d0)
    z = np.load(spec["stamp"])
    stamp = dict(du=z["du"], dv=z["dv"], dw=z["dw"])
    u0h = homog_u0(p.get("lam",2.0), p.get("k1",-0.7), p.get("k3",1.0), p.get("k4",1.5))
    yc = L/2
    u, v, w = make_stamped_world(L, dx, u0h, stamp, [(yc, L/2 - d0/2), (yc, L/2 + d0/2)])
    r1 = run(L=L, dx=dx, T=T_prep, u=u, v=v, w=w, rec_tu=50.0, **p)
    if r1["status"] != "ok" or len(r1["frames"][-1]) != 2:
        save(dict(status="prep_fail", ncomp=len(r1["frames"][-1]))); sys.exit()
    s_prep, _ = pair_sep(r1["frames"][-1][0], r1["frames"][-1][1], L)
    esc = {"t": None, "mode": None}
    seps = []
    def stop_fn(t, blobs):
        if len(blobs) != 2:
            esc["t"] = t; esc["mode"] = ("merge" if len(blobs) < 2 else "split")
            return True
        s, _ = pair_sep(blobs[0], blobs[1], L)
        seps.append([round(t,1), round(s,3)])
        if abs(s - dstar) > band:
            esc["t"] = t; esc["mode"] = ("out" if s > dstar else "in")
            return True
        return False
    r2 = run(L=L, dx=dx, T=T_max, u=r1["u"], v=r1["v"], w=r1["w"], noise=noise, seed=seed,
             rec_tu=spec.get("rec_tu", 5.0), stop_fn=stop_fn, **p)
    save(dict(status=r2["status"], sep_prep=round(s_prep,3), noise=noise, seed=seed,
              t_escape=esc["t"], mode=esc["mode"], censored=esc["t"] is None,
              T_max=T_max, seps=seps[::20] + seps[-3:]))
else:
    save(dict(status="unknown_kind"))
