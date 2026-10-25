"""Loop-level genealogy for evoloop: each loop is identified by its enclosed hole (empty cells it surrounds).
Every `dt` steps: label holes (periodic), match to previous holes by pixel overlap. A new hole is a birth;
its parent is the living loop whose hole centroid is nearest (periodic) within `rmax`. A vanished hole is a
death. A matched hole whose area changes is a conversion (kind change of a living loop).
Kind = hole side, round(sqrt(hole area)). Writes JSON with events and per-kind tallies."""
import sys, os, json, importlib.util, numpy as np
SNAP = (2000, 20000, 50000, 80000, 90000, 100000, 120000, 150000, 200000)
from scipy import ndimage

def periodic_label(z):
    lab, n = ndimage.label(z)
    par = np.arange(n + 1)
    def find(a):
        while par[a] != a:
            par[a] = par[par[a]]; a = par[a]
        return a
    for a, b in [(lab[0], lab[-1]), (lab[:, 0], lab[:, -1])]:
        m = (a > 0) & (b > 0)
        for x, y in set(zip(a[m].tolist(), b[m].tolist())):
            rx, ry = find(x), find(y)
            if rx != ry: par[ry] = rx
    roots = np.array([find(i) for i in range(n + 1)])
    return roots[lab]

def holes(g):
    lab = periodic_label(g == 0)
    area = np.bincount(lab.ravel()); area[0] = 0
    area[np.argmax(area)] = 0  # the background
    ids = np.nonzero(area >= 4)[0]
    return lab, ids, area

def pcent(ii, jj, L):
    th_i = 2 * np.pi * ii / L; th_j = 2 * np.pi * jj / L
    ci = (np.arctan2(np.sin(th_i).mean(), np.cos(th_i).mean()) * L / (2 * np.pi)) % L
    cj = (np.arctan2(np.sin(th_j).mean(), np.cos(th_j).mean()) * L / (2 * np.pi)) % L
    return ci, cj

def run(world, params, T, seed, L, dt=20, rmax=40, out=None):
    os.environ["WORLD_P"] = json.dumps(params)
    spec = importlib.util.spec_from_file_location("w", world); w = importlib.util.module_from_spec(spec); spec.loader.exec_module(w)
    s = w.init(seed, (L, L))
    live = {}  # id -> dict(area, pix(set of flat idx), c, born, parent)
    nid = 0; events = []; census = []
    for t in range(0, T + 1):
        if t % dt == 0:
            lab, ids, area = holes(s["g"])
            flat = lab.ravel()
            cur = {}
            for h in ids:
                pix = np.nonzero(flat == h)[0]
                cur[h] = pix
            # match by overlap
            used = set(); newlive = {}
            pix2id = {}
            for k, v in live.items():
                for p in v["pixs"][:5]: pix2id[p] = k
            for h, pix in cur.items():
                hit = None
                for p in pix:
                    if p in pix2id and pix2id[p] not in used: hit = pix2id[p]; break
                if hit is None:
                    # check full overlap against any live hole
                    for k, v in live.items():
                        if k in used: continue
                        if np.intersect1d(v["pix"], pix, assume_unique=True).size: hit = k; break
                ii, jj = np.divmod(pix, L); c = pcent(ii, jj, L); a = int(round(np.sqrt(len(pix))))  # kind = hole side
                if hit is not None:
                    used.add(hit); v = live[hit]
                    if a != v["area"]:
                        events.append({"t": t, "type": "convert", "id": hit, "from": v["area"], "to": a, "age": t - v["born"]})
                        v["area"] = a
                    v["pix"] = pix; v["pixs"] = pix[np.linspace(0, len(pix) - 1, 5).astype(int)].tolist(); v["c"] = c
                    newlive[hit] = v
                else:
                    best, bd = None, rmax
                    for k, v in live.items():
                        d = np.abs(np.array(c) - np.array(v["c"])); d = np.minimum(d, L - d); d = float(np.hypot(*d))
                        if d < bd: best, bd = k, d
                    nid += 1
                    pa = live[best]["area"] if best is not None else None
                    events.append({"t": t, "type": "birth", "id": nid, "parent": best, "area": a, "parent_area": pa, "dist": round(bd, 1) if best is not None else None, "c": [round(float(c[0]), 1), round(float(c[1]), 1)], "pc": [round(float(x), 1) for x in live[best]["c"]] if best is not None else None})
                    newlive[nid] = {"area": a, "pix": pix, "pixs": pix[np.linspace(0, len(pix) - 1, 5).astype(int)].tolist(), "c": c, "born": t, "parent": best}
                    if best is not None: live[best].setdefault("kids", 0); live[best]["kids"] = live[best].get("kids", 0) + 1
            for k, v in live.items():
                if k not in used:
                    events.append({"t": t, "type": "death", "id": k, "area": v["area"], "age": t - v["born"], "kids": v.get("kids", 0), "c": [round(float(v["c"][0]), 1), round(float(v["c"][1]), 1)]})
            live = newlive
            if t % 1000 == 0:
                ar = [v["area"] for v in live.values()]
                census.append({"t": t, "n": len(ar), "areas": np.unique(ar, return_counts=True)[0].tolist(), "counts": np.unique(ar, return_counts=True)[1].tolist()})
                if t % 10000 == 0: print(t, len(ar), dict(zip(*np.unique(ar, return_counts=True))), flush=True)
        if out and t in SNAP: np.save(out.replace('.json', f'_g{t}.npy'), s['g'])
        if t < T: w.step(s)
    res = {"params": params, "seed": seed, "L": L, "T": T, "dt": dt, "events": events, "census": census}
    if out: json.dump(res, open(out, "w"), default=int)
    return res

if __name__ == "__main__":
    world, params, T, seed, L, out = sys.argv[1], json.loads(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), sys.argv[6]
    run(world, params, T, seed, L, out=out)
