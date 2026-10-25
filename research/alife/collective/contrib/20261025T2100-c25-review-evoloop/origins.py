"""For the loops of kind K alive at time T in an evo_track.py JSON, walk each one's parent chain back to the first
ancestor of kind K whose own parent was of another kind (or an orphan): the mutation event that founded that K-clade.
Prints how many founding events the living K-loops descend from, and the share of the largest clade; a sweep that
selection carries descends from few events, one fed by repeated mutation inflow from many.
usage: origins.py trk.json K T"""
import sys, json, collections
d = json.load(open(sys.argv[1])); K = int(sys.argv[2]); T = int(sys.argv[3])
born = {}; died = {}; conv = collections.defaultdict(list)
for e in d["events"]:
    if e["type"] == "birth": born[e["id"]] = e
    elif e["type"] == "death": died[e["id"]] = e["t"]
    elif e["type"] == "convert": conv[e["id"]].append(e)
def kind_at(i, t):
    k = born[i]["area"] if i in born else None
    for c in conv.get(i, []):
        if c["t"] <= t: k = c["to"]
    return k
alive = [i for i, e in born.items() if e["t"] <= T and died.get(i, 10 ** 9) > T and kind_at(i, T) == K]
roots = collections.Counter(); via_conv = 0
for i in alive:
    j = i
    while True:
        e = born.get(j)
        if e is None: break
        if any(c["to"] == K and c["t"] <= T for c in conv.get(j, [])) and e["area"] != K: via_conv += 1; break
        p = e["parent"]
        if p is None or e["parent_area"] != K or p not in born: break
        j = p
    roots[(j, born[j]["t"] if j in born else None)] += 1
tot = sum(roots.values())
print(f"{sys.argv[1]}: kind {K} alive at t={T}: {tot}; founding events {len(roots)}; top clades {[(r[1], n) for r, n in roots.most_common(5)]}; largest share {roots.most_common(1)[0][1] / max(tot, 1):.2f}")
