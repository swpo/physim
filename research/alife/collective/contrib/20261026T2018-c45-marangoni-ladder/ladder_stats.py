"""(c45) Readouts for the three-kind Marangoni ladder (Q:marangoni-heritable-ladder).
usage: ladder_stats.py frames.npz world.py table.json metrics.json mut.jsonl label
Kind of a body at a rendered frame = argmax_k of the summed s_k over the body dilated by 2 px (render channels 2-4);
purity = that share. Tracks and components come from labkit's own segmentation and tracker (same calls as extract.py).
Reports: kind shares among bodies over time (purity >= 0.6); births (persistent splits, labkit metrics) by parent kind;
off-kind daughters (kind of the daughter at its first rendered frame >= birth + 5 differs from the parent's last kind);
kind changes along tracks between rendered frames (both purities >= 0.6) and how many coincide with a logged mutation of
that body; merges by product kind; and per kind the penetrance on dividing tracks (extract.py rows): n, median D,
90th percentile, share D >= 2.5 and >= 3 (rod lengths) and D_A >= 3 (sqrt(area)), median path speed and cycle."""
import sys, json, importlib.util, numpy as np
sys.path.insert(0, "/home/user/physim/research/alife")
from labkit import run as LR, metrics as M
from scipy import ndimage as ndi
fn, wpath, tabf, metf, mutf, label = sys.argv[1:7]
F = np.load(fn); mat = F["matter"].astype(np.float32); R = F["render"]; rf = [int(x) for x in F["render_f"]]
rindex = {f: i for i, f in enumerate(rf)}
spec = importlib.util.spec_from_file_location("w", wpath); W = importlib.util.module_from_spec(spec); spec.loader.exec_module(W)
mn, thr, lo, hi = LR._normalize_matter(mat, W.META, True, W.META.get("threshold")); H, Wd = mn.shape[1:]
comps, links = LR._segment_frames(mn, thr, LR._default_min_area(H, Wd), True)
tracks, ev = M.track(comps, links, (H, Wd), True); byid = {t["id"]: t for t in tracks}
T = len(comps)

def kind_of(f, comp):
    i = rindex.get(f)
    if i is None: return None
    m = comps[f]["lab"] == comp + 1
    mw = np.pad(m, 2, mode="wrap"); m2 = ndi.binary_dilation(mw, iterations=2)[2:-2, 2:-2]
    tot = np.array([R[i, 2 + k][m2].sum() for k in range(3)], float)
    if tot.sum() <= 0: return None
    return int(tot.argmax()), float(tot.max() / tot.sum())

TK = {}
for t in tracks:
    ks = []
    for k in range(len(t["comp"])):
        f = t["start"] + k; q = kind_of(f, t["comp"][k])
        if q: ks.append((f, q[0], q[1]))
    TK[t["id"]] = ks
out = []
def P(s): print(s); out.append(s)
P(f"== {label}: {T} frames, {len(tracks)} tracks")
# kind shares over time
P("frame  bodies  share k0 k1 k2 (pure >= 0.6)")
for f in rf[::10]:
    c = np.zeros(3); n = 0
    for j in range(len(comps[f]["area"])):
        q = kind_of(f, j)
        if q and q[1] >= 0.6: c[q[0]] += 1
        n += 1
    P(f"{f:5d} {n:6d}   " + " ".join(f"{x / max(c.sum(), 1):.2f}" for x in c))
# mutation events mapped to labkit components
muts = [json.loads(l) for l in open(mutf)] if mutf != "-" else []
mut_at = {}
nmut = 0
for e in muts:
    f = e["frame"]
    if f >= T: continue
    lab, n = W._bodies(mat[f])
    for x in e["events"]:
        nmut += 1
        m = lab == x["body"]
        cl = comps[f]["lab"][m]; cl = cl[cl > 0]
        if len(cl): mut_at.setdefault(f, set()).add(int(np.bincount(cl).argmax()) - 1)
P(f"mutation events: {nmut} (mapped to labkit bodies: {sum(len(v) for v in mut_at.values())})")
# kind changes along tracks
chg = expl = 0
for t in tracks:
    ks = [x for x in TK[t["id"]] if x[2] >= 0.6]
    for (f0, k0, _), (f1, k1, _) in zip(ks, ks[1:]):
        if k1 != k0:
            chg += 1
            hit = any(t["start"] <= g <= t["end"] and t["comp"][g - t["start"]] in mut_at.get(g, set()) for g in range(f0 + 1, f1 + 1))
            expl += hit
P(f"kind changes along tracks (pure >= 0.6 at both ends): {chg}; coinciding with a logged mutation of that body: {expl}; unexplained: {chg - expl}")
# births and off-kind daughters
births = np.zeros(3, int); off = 0; nd = 0
for e in json.load(open(metf)).get("persistent_splits", []):
    p = byid.get(e["parent"])
    if p is None or not TK[p["id"]]: continue
    pk = TK[p["id"]][-1][1]; births[pk] += 1
    for c in e["children"]:
        ct = byid.get(c)
        ks = [x for x in TK.get(c, []) if x[0] >= ct["start"] + 5] if ct else []
        if ks:
            nd += 1; off += ks[0][1] != pk
P(f"persistent splits by parent kind k0/k1/k2: {list(births)}; daughters checked {nd}, off-kind daughters {off}")
# merges by product kind
mk = np.zeros(3, int); mx = 0
for t in tracks:
    if t["birth"] == "merge" and TK[t["id"]]:
        mk[TK[t["id"]][0][1]] += 1
        pk = set(TK[p][-1][1] for p in t["parents"] if TK.get(p))
        mx += len(pk) > 1
P(f"merge products by kind: {list(mk)}; merges of two different kinds: {mx}")
# penetrance by kind
rows = json.load(open(tabf))["rows"]
P("kind  n_div  medD  p90D  sh>=2.5  sh>=3  shDA>=3  v_path  cycle")
for k in range(3):
    g = [r for r in rows if r["dividing"] and TK.get(r["id"]) and np.bincount([x[1] for x in TK[r["id"]]], minlength=3).argmax() == k]
    if not g: P(f"k{k}  0"); continue
    D = np.array([r["disp_rl"] for r in g]); DA = np.array([r["net"] / np.sqrt(r["A_mean"]) for r in g])
    P(f"k{k} {len(g):6d} {np.median(D):5.2f} {np.percentile(D, 90):5.2f} {np.mean(D >= 2.5):8.2f} {np.mean(D >= 3):6.2f} {np.mean(DA >= 3):8.2f} {np.median([r['vpath'] for r in g]):7.3f} {np.median([r['cycle'] for r in g]):6.0f}")
open(f"/tmp/claude-0/ld/{label}.txt", "w").write("\n".join(out) + "\n")
# per-dividing-track dump and mutant lineages
dump = []
for r in rows:
    if r["dividing"] and TK.get(r["id"]):
        k = int(np.bincount([x[1] for x in TK[r["id"]]], minlength=3).argmax())
        dump.append({"id": r["id"], "kind": k, "D": r["disp_rl"], "DA": r["net"] / np.sqrt(r["A_mean"]), "vpath": r["vpath"], "cycle": r["cycle"]})
json.dump(dump, open(f"/tmp/claude-0/ld/{label}_div.json", "w"))
# mutant lineages: tracks that changed kind at a logged mutation; follow persistent-split descendants 2 levels
psplit = {}
for e in json.load(open(metf)).get("persistent_splits", []):
    psplit[e["parent"]] = e["children"]
def last_kind(tid):
    ks = [x for x in TK.get(tid, []) if x[2] >= 0.6]
    return ks[-1][1] if ks else None
def cont(tid):
    """follow a track through non-split continuations (merges keep the largest parent's id in labkit? no: a merge starts a new track); stop at a persistent split"""
    return tid
mk_ok = mk_bad = 0; lines = []
for t in tracks:
    ks = [x for x in TK[t["id"]] if x[2] >= 0.6]
    for (f0, k0, _), (f1, k1, _) in zip(ks, ks[1:]):
        if k1 != k0 and any(t["start"] <= g <= t["end"] and t["comp"][g - t["start"]] in mut_at.get(g, set()) for g in range(f0 + 1, f1 + 1)):
            gen1 = psplit.get(t["id"], []); gen2 = [c2 for c in gen1 for c2 in psplit.get(c, [])]
            k_g1 = [last_kind(c) for c in gen1]; k_g2 = [last_kind(c) for c in gen2]
            lines.append(f"  track {t['id']} mutated {k0}->{k1} at frame ~{f1}; daughters kinds {k_g1}; granddaughters kinds {k_g2}")
P("mutant lineages (kind of persistent-split daughters and granddaughters):")
for l in lines: P(l)
open(f"/tmp/claude-0/ld/{label}.txt", "w").write("\n".join(out) + "\n")
