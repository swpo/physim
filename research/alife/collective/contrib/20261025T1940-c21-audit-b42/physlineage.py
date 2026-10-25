"""(c21) Remnant-aware lineage deaths for pcell genealogy JSONs (genealogy.py output).
A genealogy 'death' followed within WIN steps by an 'appear' cell whose first ym and zm both lie within TOL of
the dead cell's last values (the remnant fingerprint used in c00's remnant.py) is a continuation, not a death:
the appear cell inherits the lineage. A lineage dies when its last cell dies with no such remnant. Mature =
lineage alive >= MATURE steps. For each mature lineage death: yield (ym) and marker (zm) percentiles among the
living cells at the last snapshot and at LAG steps earlier. Also counts deaths by the claim's raw criterion.
usage: physlineage.py gen.json[.gz] [MATURE=10000] [WIN=2000] [TOL=0.01] [LAG=2000]"""
import sys, json, gzip, numpy as np
fn = sys.argv[1]; MATURE = int(sys.argv[2]) if len(sys.argv) > 2 else 10000
WIN = int(sys.argv[3]) if len(sys.argv) > 3 else 2000; TOL = float(sys.argv[4]) if len(sys.argv) > 4 else 0.01
LAG = int(sys.argv[5]) if len(sys.argv) > 5 else 2000
d = json.load(gzip.open(fn) if fn.endswith(".gz") else open(fn)); S, E = d["series"], d["events"]
pos = {}
for a, x in enumerate(S):
    for i, c in enumerate(x["id"]): pos.setdefault(c, []).append((a, i))
T = [x["t"] for x in S]
def val(c, k, which):
    a, i = pos[c][which]; return S[a][k][i], S[a]["t"]
lin = {}  # cell -> lineage root
born = {}
for c in sorted(pos, key=lambda c: pos[c][0][0]):
    lin.setdefault(c, c); born.setdefault(lin[c], T[pos[c][0][0]])
appear = [(t, ch[0]) for t, ty, p, ch in E if ty == "appear" and ch[0] in pos]
for t, ty, p, ch in E:  # split daughters start new lineages (births); merges are 0 in this world
    for c in ch: lin.setdefault(c, c)
deaths = [(t, p[0]) for t, ty, p, ch in E if ty == "death" and p[0] in pos and t > 1000]
used = set(); cont = {}
for t, c in deaths:
    y0, _ = val(c, "ym", -1); z0, _ = val(c, "zm", -1)
    for ta, ca in appear:
        if ca in used or not (t <= ta <= t + WIN): continue
        if abs(val(ca, "ym", 0)[0] - y0) < TOL and abs(val(ca, "zm", 0)[0] - z0) < TOL:
            cont[c] = ca; used.add(ca); break
# propagate lineage roots through continuations (in time order)
for t, c in sorted(deaths):
    if c in cont: lin[cont[c]] = lin.get(c, c)
def pct(c, key, tq):
    a = max(k for k, _ in pos[c] if T[k] <= tq) if any(T[k] <= tq for k, _ in pos[c]) else None
    if a is None: return None
    x = S[a]; i = x["id"].index(c); y = x[key][i]; o = np.array([v for j, v in enumerate(x[key]) if j != i])
    return float(((o < y).sum() + 0.5 * (o == y).sum()) / max(len(o), 1))
out = []
for t, c in deaths:
    if c in cont: continue
    root = lin.get(c, c); age = val(c, "ym", -1)[1] - born.get(root, T[pos[c][0][0]])
    if age < MATURE: continue
    tl = val(c, "ym", -1)[1]
    out.append(dict(t=t, cell=c, age=age, y=pct(c, "ym", tl), z=pct(c, "zm", tl), y_lag=pct(c, "ym", tl - LAG), z_lag=pct(c, "zm", tl - LAG)))
m = lambda k: round(float(np.mean([o[k] for o in out if o[k] is not None])), 3) if out else None
print(json.dumps(dict(file=fn, raw_deaths=len(deaths), remnant_continuations=len(cont), lineage_deaths_mature=len(out),
                      y_pct=m("y"), z_pct=m("z"), y_pct_lag=m("y_lag"), z_pct_lag=m("z_lag"),
                      y_below_median=sum(1 for o in out if o["y"] is not None and o["y"] < 0.5))))
