"""In-situ test of M: are swimmers driven by the population-scale substrate gradient?
Run the claimed world from noise, record phi and S every 50 t to T. Overlap-track phi>1/2 cells
(stop a track at split/merge). For each step of each track: velocity v (centroid), the coarse
gradient G = grad(gauss(S, sigma=SIG px)) at the centroid with the cell and its 2-cell-radius
neighbourhood's own depletion INCLUDED (a lower bound for collective gradient), and cos(v, G).
Report, for tracks that move >= 3 BL (BL = 2 sqrt(A/pi)), the mean cos and the share of the
path projected on G. usage: python align.py world.py seed T out [SIG]"""
import sys, json, os
import numpy as np
from scipy import ndimage
world, seed, T, out = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
SIGS = [12.0, 24.0, 48.0]
os.environ.setdefault("WORLD_P", json.dumps({"drive": "kernel", "mu": 1.0, "kd": 0.08, "chi": 5}))
sys.path.insert(0, "/home/user/physim/research/alife")
from labkit.world import load_world
W = load_world(world); H = W.META["size"][0]; dt = W.P["dt"]
s = W.init(seed, (H, H))
def label(phi):
    lab, n = ndimage.label(phi > 0.5)
    for a, b in ((lab[0], lab[-1]), (lab[:, 0], lab[:, -1])):
        for u, w in set(zip(a.tolist(), b.tolist())):
            if u and w and u != w: lab[lab == w] = u
    return lab
def cent(mask):
    ys, xs = np.nonzero(mask)
    return np.array([np.angle(np.exp(2j*np.pi*ys/H).mean())*H/(2*np.pi) % H, np.angle(np.exp(2j*np.pi*xs/H).mean())*H/(2*np.pi) % H])
every = int(50 / dt); frames_c = {}; tracks = {}; kids = {}; live = {}; nid = 0; prevlab = None
for i in range(int(T / dt) + 1):
    if i % every == 0:
        lab = label(s["phi"])
        GG = []
        for SIG in SIGS:
            Sg = ndimage.gaussian_filter(s["S"], SIG, mode="wrap")
            GG.append((0.5 * (np.roll(Sg, -1, 0) - np.roll(Sg, 1, 0)), 0.5 * (np.roll(Sg, -1, 1) - np.roll(Sg, 1, 1))))
        ids = [l for l in np.unique(lab)[1:] if (lab == l).sum() >= 15]
        newlive = {}
        if prevlab is not None:
            # parents of each current cell, children of each previous cell
            par = {l: [p for p in np.unique(prevlab[lab == l]) if p] for l in ids}
            chil = {}
            for l, ps in par.items():
                for p in ps: chil.setdefault(p, []).append(l)
        for l in ids:
            m = lab == l; c = cent(m); A = m.sum()
            cy, cx = int(round(c[0])) % H, int(round(c[1])) % H
            g = [v for gy, gx in GG for v in (gy[cy, cx], gx[cy, cx])]
            if prevlab is not None and len(par[l]) == 1 and len(chil.get(par[l][0], [])) == 1 and par[l][0] in live:
                k = live[par[l][0]]
            else:
                k = nid; nid += 1; tracks[k] = []
                if prevlab is not None and len(par[l]) == 1 and len(chil.get(par[l][0], [])) >= 2 and par[l][0] in live:
                    kids.setdefault(live[par[l][0]], []).append(k)
            tracks[k].append((i * dt, c[0], c[1], A, *g)); newlive[l] = k
            frames_c.setdefault(i * dt, []).append((c[0], c[1], k))
        live = newlive; prevlab = lab
    if i < int(T / dt): s = W.step(s)

summ = {"seed": seed, "T": T}; allsw = {}
for j, SIG in enumerate(SIGS):
    rows = []; allcos = []
    for k, tr in tracks.items():
        tr = np.array(tr)
        if len(tr) < 4: continue
        d = (np.diff(tr[:, 1:3], axis=0) + H/2) % H - H/2
        BL = 2*np.sqrt(tr[:, 3].mean()/np.pi)
        net = np.linalg.norm(d.sum(0)) / BL
        G = 0.5 * (tr[1:, 4+2*j:6+2*j] + tr[:-1, 4+2*j:6+2*j]); gn = np.linalg.norm(G, axis=1) + 1e-12
        step = np.linalg.norm(d, axis=1); proj = (d * G).sum(1) / gn; ok = step > 0.2
        cos = proj[ok] / step[ok]
        rows.append(dict(track=int(k), t0=float(tr[0, 0]), t1=float(tr[-1, 0]), BL_px=float(BL), net_BL=float(net),
                         path_BL=float(step.sum()/BL), proj_share=float(proj.sum()/max(step.sum(), 1e-9)),
                         mean_cos=float(cos.mean()) if ok.any() else None))
        if net >= 1: allcos += list(cos)
    sw = [r for r in rows if r["net_BL"] >= 3]
    summ["sig%d" % SIG] = {"tracks": len(rows), "n_ge1BL": sum(r["net_BL"] >= 1 for r in rows), "swimmers_ge3BL": len(sw),
        "swimmers_mean_cos": float(np.mean([r["mean_cos"] for r in sw])) if sw else None,
        "swimmers_proj_share_median": float(np.median([r["proj_share"] for r in sw])) if sw else None,
        "ge1BL_steps_cos_mean": float(np.mean(allcos)) if allcos else None,
        "ge1BL_steps_frac_cos_gt0.5": float(np.mean(np.array(allcos) > 0.5)) if allcos else None}
    allsw["sig%d" % SIG] = sorted(sw, key=lambda r: -r["net_BL"])
# swimmers that end in a split whose >= 2 daughters each live >= 400 t (as a track, or splitting again after >= 200 t)
def lasts(k):
    tr = tracks[k]; return tr[-1][0] - tr[0][0] >= 400 or (k in kids and tr[-1][0] - tr[0][0] >= 200)
sd = []
for k, tr in tracks.items():
    tr = np.array(tr)
    if len(tr) < 4: continue
    d = (np.diff(tr[:, 1:3], axis=0) + H/2) % H - H/2
    BL = 2*np.sqrt(tr[:, 3].mean()/np.pi)
    if np.linalg.norm(d.sum(0)) / BL >= 3 and k in kids and sum(lasts(c) for c in kids[k]) >= 2:
        sd.append({"track": int(k), "t0": float(tr[0, 0]), "t_split": float(tr[-1, 0]), "net_BL": float(np.linalg.norm(d.sum(0)) / BL), "daughters": kids[k]})
summ["swim_then_divide"] = {"n": len(sd), "examples": sd[:8]}
# neighbour test: cos(v, direction away from the mean of other cells within RN px)
for RN in (20.0, 40.0):
    cs = []; shares = []
    for k, tr in tracks.items():
        tr = np.array(tr)
        if len(tr) < 4: continue
        d = (np.diff(tr[:, 1:3], axis=0) + H/2) % H - H/2
        BL = 2*np.sqrt(tr[:, 3].mean()/np.pi)
        if np.linalg.norm(d.sum(0)) / BL < 3: continue
        num = 0.0; den = 0.0; cc = []
        for j in range(len(d)):
            t = tr[j, 0]; me = tr[j, 1:3]
            oth = np.array([(y, x) for y, x, kk in frames_c[t] if kk != k])
            if not len(oth): continue
            r = (me - oth + H/2) % H - H/2; dist = np.linalg.norm(r, axis=1); m = dist < RN
            if not m.any(): continue
            a = (r[m] / dist[m, None]).sum(0); a /= np.linalg.norm(a) + 1e-12
            st = np.linalg.norm(d[j])
            if st > 0.2: cc.append((d[j] @ a) / st)
            num += d[j] @ a; den += st
        if cc: cs.append(np.mean(cc)); shares.append(num / max(den, 1e-9))
    summ["away_from_neighbours_R%d" % RN] = {"swimmers": len(cs), "mean_cos": float(np.mean(cs)) if cs else None, "median_proj_share": float(np.median(shares)) if shares else None}
json.dump({"summary": summ, "swimmers": allsw}, open(out + ".json", "w"), indent=1)
print(json.dumps(summ, indent=1))
for r in allsw["sig48"][:10]: print(r)
