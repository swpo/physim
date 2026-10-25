"""Swim-divide tracker for Allen-Cahn cell worlds (phi field, periodic).

Runs a world (WORLD_P honoured), labels cells phi > 1/2 every `rec` steps (periodic labels merged
across edges), links cells frame to frame by pixel overlap, and records per cell segment
(between birth and its split/merge/death): unwrapped centroid path, equivalent radius, and the
L-ring contrast rim/core (rim = 0.6 < r/R < 1.3 region, core r/R < 0.4).
Writes segments.json and prints swim-divide events: a segment born by a SPLIT whose net
displacement >= 3 body lengths (2 R) and which itself ends in a split with both daughters
surviving >= `keep` steps without merging.
usage: python swimtrack.py world.py out_dir seed T [rec]
"""
import sys, os, json, importlib.util, numpy as np
from scipy import ndimage

def plabel(mask):
    lab, n = ndimage.label(mask)
    par = list(range(n + 1))
    def f(a):
        while par[a] != a: par[a] = par[par[a]]; a = par[a]
        return a
    for a, b in ((lab[0], lab[-1]), (lab[:, 0], lab[:, -1])):
        for u, v in set(zip(a.tolist(), b.tolist())):
            if u and v: par[f(u)] = f(v)
    roots = np.array([f(i) for i in range(n + 1)]); roots[0] = 0
    u, inv = np.unique(roots, return_inverse=True)
    return inv.reshape(-1)[lab].reshape(lab.shape) if False else inv[lab], len(u) - 1

def pcentroid(m):
    H, W = m.shape; ys, xs = np.nonzero(m)
    cy = np.angle(np.exp(2j * np.pi * ys / H).mean()) * H / (2 * np.pi) % H
    cx = np.angle(np.exp(2j * np.pi * xs / W).mean()) * W / (2 * np.pi) % W
    return cy, cx

def ring(L, m, cy, cx):
    H, W = m.shape; R = np.sqrt(m.sum() / np.pi)
    yy, xx = np.mgrid[0:H, 0:W]
    dy = (yy - cy + H / 2) % H - H / 2; dx = (xx - cx + W / 2) % W - W / 2
    r = np.sqrt(dy * dy + dx * dx) / max(R, 1e-9)
    core = L[r < 0.4]; rim = L[(r > 0.6) & (r < 1.3)]
    return float(rim.mean() / max(core.mean(), 1e-9)) if len(core) and len(rim) else None

def ringw(L, phi, m):
    """L in the cell's own wall band (0.3 < phi < 0.7, within 3 px of the body) over L in its
    deep core (phi > 0.9 and >= 3 px inside the body edge)."""
    near = ndimage.binary_dilation(m, iterations=3)
    deep = ndimage.binary_erosion(m, iterations=3) & (phi > 0.9)
    band = near & (phi > 0.3) & (phi < 0.7)
    if deep.sum() < 3 or band.sum() < 3: return None
    return float(L[band].mean() / max(L[deep].mean(), 1e-9))


def main():
    wp, out, seed, T = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
    rec = int(sys.argv[5]) if len(sys.argv) > 5 else 25
    keep, minA = 500, 12
    spec = importlib.util.spec_from_file_location("w", wp); w = importlib.util.module_from_spec(spec); spec.loader.exec_module(w)
    s = w.init(seed, w.META["size"]); H, W = w.META["size"]
    segs = {}; prev = None; nid = 0
    for t in range(T + 1):
        if t % rec == 0:
            lab, n = plabel(s["phi"] > 0.5)
            cur = {}
            for i in range(1, n + 1):
                m = lab == i
                if m.sum() < minA: continue
                cy, cx = pcentroid(m)
                cur[i] = (m, cy, cx, float(np.sqrt(m.sum() / np.pi)), ringw(s["L"], s["phi"], m))
            ids = {}
            if prev is not None:
                plab, pmap = prev
                # overlap graph
                fwd = {}; bwd = {}
                for i, (m, *_r) in cur.items():
                    ov = np.bincount(plab[m], minlength=plab.max() + 1); ov[0] = 0
                    for j in np.nonzero(ov)[0]:
                        if j in pmap: fwd.setdefault(pmap[j], []).append(i); bwd.setdefault(i, []).append(pmap[j])
                for i in cur:
                    par = bwd.get(i, [])
                    if len(par) == 1 and len(fwd[par[0]]) == 1:
                        ids[i] = par[0]  # continuation
                    else:
                        ids[i] = nid; segs[nid] = dict(id=nid, t0=t, parents=par, kids=[], path=[], R=[], ring=[], end=None)
                        nid += 1
                        for p in par: segs[p]["kids"].append(ids[i])
                for sid, kids in fwd.items():
                    if not (len(kids) == 1 and len(bwd.get(kids[0], [])) == 1):
                        segs[sid]["end"] = ("split" if len(kids) > 1 else "merge", t)
                cont = set(ids.values())
                for sid in pmap.values():
                    if sid not in fwd and segs[sid]["end"] is None: segs[sid]["end"] = ("death", t)
            else:
                for i in cur:
                    ids[i] = nid; segs[nid] = dict(id=nid, t0=t, parents=[], kids=[], path=[], R=[], ring=[], end=None); nid += 1
            for i, (m, cy, cx, R, rg) in cur.items():
                sg = segs[ids[i]]
                if sg["path"]:
                    py, px = sg["path"][-1][1:]
                    dy = (cy - py + H / 2) % H - H / 2; dx = (cx - px + W / 2) % W - W / 2
                    cy, cx = py + dy, px + dx
                sg["path"].append((t, cy, cx)); sg["R"].append(R); sg["ring"].append(rg)
            prev = (lab, {i: ids[i] for i in cur})
        if t < T: s = w.step(s)
    os.makedirs(out, exist_ok=True)
    for sg in segs.values():
        p = np.array([q[1:] for q in sg["path"]]) if sg["path"] else np.zeros((0, 2))
        sg["disp"] = float(np.hypot(*(p[-1] - p[0]))) if len(p) > 1 else 0.0
        sg["plen"] = float(np.hypot(*np.diff(p, axis=0).T).sum()) if len(p) > 1 else 0.0
        sg["Rmed"] = float(np.median(sg["R"])) if sg["R"] else 0.0
        rg = [x for x in sg["ring"] if x is not None]
        sg["ring_med"] = float(np.median(rg)) if rg else None
        sg["BL"] = sg["disp"] / max(2 * sg["Rmed"], 1e-9)
    def daughters_ok(sg):
        if not sg["end"] or sg["end"][0] != "split": return False
        ks = [segs[k] for k in sg["kids"]]
        good = [k for k in ks if len(k["parents"]) == 1 and k["path"] and (k["path"][-1][0] - k["t0"] >= keep or k["end"] is None or (k["end"][0] == "split"))]
        return len(good) >= 2
    born_split = lambda sg: len(sg["parents"]) == 1 and segs[sg["parents"][0]]["end"] and segs[sg["parents"][0]]["end"][0] == "split"
    ev = [sg for sg in segs.values() if born_split(sg) and sg["BL"] >= 3 and daughters_ok(sg)]
    allsw = [sg for sg in segs.values() if sg["BL"] >= 3]
    dv = [sg for sg in segs.values() if daughters_ok(sg)]
    summ = dict(segments=len(segs), swimmers_3BL=len(allsw), ring_swimmers=float(np.median([x["ring_med"] for x in allsw if x["ring_med"]] or [0])), ring_all=float(np.median([x["ring_med"] for x in segs.values() if x["ring_med"]] or [0])), dividers=len(dv), swim_divide=len(ev),
                ring_med_swimdiv=[sg["ring_med"] for sg in ev], ev=[(sg["id"], sg["t0"], sg["end"], round(sg["BL"], 1), round(sg["Rmed"], 1), sg["kids"]) for sg in ev])
    # generation depth over swim-divide chain
    def depth(sid, seen=()):
        sg = segs[sid]; ok = sg in ev
        return (1 if ok else 0) + max([depth(k) for k in sg["kids"] if len(segs[k]["parents"]) == 1] or [0]) if ok else max([depth(k) for k in sg["kids"] if len(segs[k]["parents"]) == 1] or [0])
    summ["max_chain"] = max([0] + [depth(r) for r, sg in segs.items() if not sg["parents"]])
    json.dump(dict(summary=summ, segs=list(segs.values())), open(os.path.join(out, "segments.json"), "w"))
    print(json.dumps(summ))

if __name__ == "__main__":
    main()
